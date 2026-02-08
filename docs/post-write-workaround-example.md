# PostToolUse フックでのWrite規約適用ワークアラウンド

## 問題の背景

`.claude/rules/`のpath-basedルールは、Write操作（新規ファイル作成）時に読み込まれません。
このワークアラウンドは、ファイル作成後に強制的にルールを適用するための仕組みです。

## 理論的な実装（hooks/post-write-rules-loader.sh）

```bash
#!/bin/bash
# hooks/post-write-rules-loader.sh
# Write操作後にpath-basedルールを強制適用するワークアラウンド

# 標準入力からPostToolUseのJSONを取得
INPUT=$(cat)

# ツール名とファイルパスを抽出
TOOL=$(echo "$INPUT" | jq -r '.tool_name // empty')
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Writeツールでない場合は何もしない
if [ "$TOOL" != "Write" ]; then
  exit 0
fi

# ファイルパスが取得できない場合は何もしない
if [ -z "$FILE_PATH" ] || [ "$FILE_PATH" = "null" ]; then
  exit 0
fi

# ファイルが存在しない場合は何もしない
if [ ! -f "$FILE_PATH" ]; then
  exit 0
fi

# Claudeにファイルを読み直させてルールを適用させるメッセージを出力
# hookSpecificOutputで追加のコンテキストを注入
jq -n --arg file "$FILE_PATH" '{
  hookSpecificOutput: {
    hookEventName: "PostToolUse",
    userMessage: "⚠️  新規ファイルが作成されました。path-basedルールを確認してください。",
    contextToInject: "IMPORTANT: ファイル \($file) が作成されました。\n\n該当するpath-basedルール（.claude/rules/）を確認し、ルールに従っているか検証してください。違反している場合は即座に修正してください。"
  }
}'

exit 0
```

## 設定（.claude/settings.local.json）

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash hooks/post-write-rules-loader.sh"
          }
        ]
      }
    ]
  }
}
```

## この実装の問題点

1. **完全な自動化は困難**
   - スクリプトはClaudeに「確認してください」と依頼するだけ
   - Claudeが実際にルールを適用する保証はない

2. **ルールの無視問題**
   - イシュー#19635（CLAUDE.mdのルールが無視される）と同じ問題が発生する可能性

3. **トークンの浪費**
   - 毎回のWrite操作で追加のコンテキストが注入される

4. **複雑性の増加**
   - 本来シンプルであるべき仕組みが複雑になる

## より実用的な代替案

### 1. CLAUDE.mdに重要なルールを重複記載（推奨）

**メリット:**
- シンプル
- 確実に読み込まれる
- フック不要

**デメリット:**
- path-basedの細かい制御ができない
- CLAUDE.mdが肥大化する可能性

**実装例:**

```markdown
# CLAUDE.md

## ファイル作成規約

### Pythonファイル（*.py）
- 必ず型ヒントを使用
- docstringは必須
- モジュールレベルのdocstringを先頭に配置

### Markdownファイル（*.md）
- 先頭にYAML frontmatter（タイトル、日付）を追加
- 見出しは#から開始（##ではない）

### 設定ファイル（*.json, *.yaml）
- コメント付きのサンプルを含める
- 本番用と開発用を明確に区別
```

### 2. prompt hookで事後検証（半自動）

**メリット:**
- LLMによる柔軟な判定
- ルールの意図を理解して適用

**デメリット:**
- 追加のAPI呼び出しが発生（コスト増）
- 検証のみで自動修正はしない

**実装例（.claude/settings.local.json）:**

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "新規ファイルが作成されました: $ARGUMENTS。\n\n.claude/rules/内のpath-basedルールに違反していないか確認してください。違反があれば {\"ok\": false, \"reason\": \"理由\"} を返し、問題なければ {\"ok\": true} を返してください。",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### 3. agent hookで自動検証・修正（最も高度）

**メリット:**
- ツール使用可能（Read, Edit）
- 自動的にルール違反を検出して修正

**デメリット:**
- 最もコストが高い
- 複雑な設定

**実装例（.claude/settings.local.json）:**

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "agent",
            "prompt": "新規ファイルが作成されました: $ARGUMENTS。\n\n1. ファイルを読み込む\n2. .claude/rules/のpath-basedルールに違反していないか確認\n3. 違反があればEditツールで修正\n4. 結果を報告",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

## 推奨アプローチ

現時点では、**代替案1（CLAUDE.mdへの重複記載）** が最も実用的です：

1. **シンプルで確実**
2. **追加コストなし**
3. **メンテナンスが容易**

path-basedルールは、現時点では以下の用途に限定して使用するのが賢明です：

- ✅ **既存ファイルの編集規約**（Edit時に適用される）
- ✅ **ファイル読み込み時のコンテキスト注入**（Read時に適用される）
- ❌ **新規ファイルの作成規約**（Write時に適用されない）← これはCLAUDE.mdで対応

## まとめ

`post-write-rules-loader.sh`のような複雑なワークアラウンドよりも、以下の方針を推奨します：

1. 重要なファイル作成規約は **CLAUDE.mdに記載**
2. path-basedルールは **Edit/Read用途に限定**
3. どうしても自動化したい場合は **agent hook** を使用（コスト増に注意）

この問題が公式に修正されるまでは、シンプルな対処法を選ぶのが最善です。
