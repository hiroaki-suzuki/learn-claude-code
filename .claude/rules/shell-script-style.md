# シェルスクリプト コーディングルール

このプロジェクトでは **Google Shell Style Guide** に準拠します。

## 基本原則

### シバン（Shebang）
```bash
#!/usr/bin/env bash
```

### エラーハンドリング
```bash
set -euo pipefail
```

### コードフォーマット

すべてのシェルスクリプトは`shfmt`でフォーマットすること。

**フォーマットコマンド:**
```bash
# 単一ファイル
shfmt -i 2 -bn -ci -sr -w <script.sh>

# ディレクトリ全体
shfmt -i 2 -bn -ci -sr -w .
```

**shfmtオプション:**
- `-i 2`: インデント2スペース（Google Style準拠）
- `-bn`: バイナリオプション（`&&`, `||`を行頭に配置）
- `-ci`: switch文のcaseをインデント
- `-sr`: リダイレクト演算子の後にスペースを追加
- `-w`: ファイルに書き込む（デフォルトは標準出力）

**フォーマット確認（CI用）:**
```bash
# 差分があるかチェック（終了コード0=差分なし）
shfmt -i 2 -bn -ci -sr -d .
```

## インデント

Google Shell Styleに従い、**2スペース**でインデントする。

```bash
if [[ -f "${file}" ]]; then
  echo "ファイルが存在"
fi
```

## 変数

### 命名規則
```bash
# 定数は大文字
readonly MAX_RETRIES=3
readonly CONFIG_FILE="/etc/app/config.conf"

# 変数は小文字（スネークケース）
user_name="example"
file_count=0
```

### 引用符の使用（重要）
```bash
# 基本は常にダブルクォートで囲む
echo "${variable}"
cd "${directory_path}"

# コマンド置換
current_date=$(date +%Y-%m-%d)
files_count=$(find "${directory}" -type f | wc -l)

# 展開しない場合はシングルクォート
echo 'Hello, $USER'  # $USERは展開されない

# 例外：グロブ展開を意図する場合はクォートしない
for file in *.txt; do
    echo "${file}"
done

# 算術式はクォート不要
result=$((x + 1))
```

### 配列
```bash
# 配列の定義
files=("file1.txt" "file2.txt" "file3.txt")

# 配列の参照
echo "${files[0]}"        # 最初の要素
echo "${files[@]}"        # すべての要素
echo "${#files[@]}"       # 要素数
```

## 関数

### 基本構造
```bash
# 関数名は小文字、スネークケース
# functionキーワードは省略可能（使用しても良いが一貫性を保つ）
check_file_exists() {
  local file_path="$1"

  if [[ -f "${file_path}" ]]; then
    return 0
  else
    return 1
  fi
}

# 呼び出し
if check_file_exists "/path/to/file"; then
  echo "ファイルが存在します"
fi
```

### ローカル変数
```bash
process_data() {
  local input="$1"   # 引数はローカル変数に格納
  local result=""    # 関数内変数は必ずlocal宣言

  result=$(echo "${input}" | tr '[:lower:]' '[:upper:]')
  echo "${result}"
}
```

## 条件分岐

### [[ ]] を使用
```bash
if [[ "${status}" == "success" ]]; then
  echo "成功"
elif [[ "${status}" == "failed" ]]; then
  echo "失敗"
else
  echo "不明"
fi

# ファイルチェック
if [[ -f "${file}" ]]; then
  echo "ファイルが存在"
fi

# 文字列チェック
if [[ -n "${var}" ]]; then  # 空でない
  echo "変数に値がある"
fi
```

## ループ

```bash
# ファイルのループ
for file in *.txt; do
  echo "処理中: ${file}"
done

# 配列のループ
for item in "${array[@]}"; do
  echo "要素: ${item}"
done

# 範囲のループ
for i in {1..5}; do
  echo "カウント: ${i}"
done
```

## コメント

```bash
# 関数の説明コメント
# 引数: $1 - 処理対象のファイルパス
# 戻り値: 0 - 成功, 1 - 失敗
process_file() {
  # 実装
  :
}

# 複雑なロジックには説明を追加
# 一時ファイルを作成してソート結果を保存
temp_file=$(mktemp)
```

## ベストプラクティス

### コマンド置換
```bash
# $() を使用（`` ではなく）
output=$(command arg1 arg2)
```

### パイプと組み合わせ
```bash
# 不要なcatは避ける（Useless Use of Cat）
# ❌ 非推奨
cat "${file}" | grep "pattern" | sort | uniq

# ✅ 推奨
grep "pattern" "${file}" | sort -u

# 複数のフィルタを組み合わせる場合
grep "pattern" "${file}" | sed 's/old/new/' | sort -u
```

### 一時ファイル
```bash
# mktemp を使用
temp_file=$(mktemp)
trap 'rm -f "${temp_file}"' EXIT  # スクリプト終了時に削除
```

### エラーメッセージ
```bash
# エラーは標準エラー出力に
echo "エラー: ファイルが見つかりません" >&2
exit 1
```

## アンチパターン（避けるべき）

```bash
# ❌ 引用符なし（スペースを含むパスでエラー）
cd $directory

# ✅ 正しい
cd "${directory}"

# ❌ [ ] は罠が多い（単語分割、グロブ展開、未クォート）
if [ $status == "ok" ]; then
  echo "OK"
fi

# ✅ Bash では [[ ]] を推奨
if [[ "${status}" == "ok" ]]; then
  echo "OK"
fi

# ❌ グローバル変数の乱用
my_func() {
  result="value"  # グローバル変数を変更
}

# ✅ 正しい
my_func() {
  local result="value"  # ローカル変数
  echo "${result}"      # 戻り値
}
```

## Lintとフォーマットの自動化

### ShellCheck（静的解析）

すべてのスクリプトは`shellcheck`で検証すること。

```bash
# 単一ファイル
shellcheck script.sh

# ディレクトリ全体
find . -name "*.sh" -exec shellcheck {} \;
```

警告を無視する場合は理由をコメントで記載:

```bash
# shellcheck disable=SC2086
# 理由: 意図的に単語分割を使用
command $unquoted_var
```

### 推奨ワークフロー

```bash
# 1. フォーマット
shfmt -i 2 -bn -ci -sr -w script.sh

# 2. 静的解析
shellcheck script.sh

# 3. 実行テスト
bash -n script.sh  # 構文チェック
./script.sh        # 実行
```
