# Git運用ルール

## コミットメッセージ規約

### 基本フォーマット

```
<type>: <subject>

<body>

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### Type（種類）

- `add` - 新機能追加
- `update` - 既存機能の改善・更新
- `fix` - バグ修正
- `refactor` - リファクタリング（機能変更なし）
- `docs` - ドキュメント更新のみ
- `test` - テストの追加・修正
- `chore` - ビルドタスク、設定ファイルの変更

### Subject（件名）

- 50文字以内
- 日本語で簡潔に記述
- 文末にピリオド不要
- 命令形で記述（「〜を追加」「〜を修正」）

### Body（本文）

- subjectで説明しきれない詳細を記述
- 「何を」だけでなく「なぜ」変更したかを説明
- 72文字で改行

### 良いコミットメッセージ例

```
add: ユーザー認証機能を追加

JWTトークンベースの認証システムを実装。
セッション管理よりもスケーラブルな設計を実現。

- /api/auth/loginエンドポイント追加
- トークンの有効期限を24時間に設定
- リフレッシュトークン機能を実装

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

```
fix: ログインフォームのバリデーションエラーを修正

空のメールアドレスでもsubmitできてしまう問題を解消。
フロントエンド側で必須チェックを追加。

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### 悪いコミットメッセージ例

```
update code  # 何を更新したか不明
```

```
色々修正  # 具体性がない
```

```
WIP  # Work In Progressは避ける（コミット前に整理）
```

## コミット粒度

### 原則
- 1つのコミットは1つの論理的な変更を表す
- 複数の異なる変更は分割してコミット
- 不完全な変更はコミットしない

### 良い例
- ✅ ユーザー認証機能の追加
- ✅ ログインバリデーションの修正
- ✅ READMEにAPIドキュメントを追加

### 悪い例
- ❌ 認証機能追加とバグ修正とドキュメント更新を1つのコミットに含める
- ❌ テストが通らない状態でコミット
- ❌ 半分だけ実装した機能をコミット

## コミット前のチェックリスト

コミット前に必ず確認してください：

- [ ] コードが正しく動作する
- [ ] 関連するテストが通る
- [ ] リントエラーがない（`uv run ruff check app/`）
- [ ] フォーマットが適用されている（`uv run ruff format app/`）
- [ ] 型チェックが通る（`uv run ty check app/`）
- [ ] 不要なコメントアウトや`console.log`を削除した
- [ ] コミットメッセージが規約に従っている

## 禁止事項

- ❌ 大量の無関係なファイルを含むコミット
- ❌ コミットメッセージなしのコミット
- ❌ `.env`や認証情報を含むコミット
- ❌ `git add .`の無計画な使用（意図しないファイルを含めない）

## よく使うコマンド

### 差分確認
```bash
git status                    # 変更されたファイル一覧
git diff                      # 変更内容の詳細
git diff --staged             # ステージング済みの差分
```

### コミット操作
```bash
git add <file>                # 特定ファイルをステージング
git add -p                    # 対話的にステージング
git commit -m "message"       # コミット
git commit --amend            # 直前のコミットを修正
```

### ブランチ操作
```bash
git branch                    # ブランチ一覧
git checkout -b <branch>      # ブランチ作成＆切り替え
git branch -d <branch>        # ブランチ削除
```

### リモート操作
```bash
git pull origin main          # mainの最新を取得
git push origin <branch>      # ブランチをpush
git push -u origin <branch>   # 初回push（upstream設定）
```

### 履歴確認
```bash
git log --oneline             # コミット履歴（簡潔版）
git log --graph --all         # ブランチ構造を表示
```

## トラブルシューティング

### 間違ってコミットした場合
```bash
# 直前のコミットを取り消し（変更は残る）
git reset --soft HEAD^

# 直前のコミットを完全に取り消し
git reset --hard HEAD^
```

### コンフリクト解決
```bash
git pull origin main          # 最新を取得（コンフリクト発生）
# ファイルを編集してコンフリクト解消
git add <resolved-file>
git commit                    # コンフリクト解消をコミット
```

### 間違ったブランチで作業してしまった場合
```bash
git stash                     # 変更を一時退避
git checkout <correct-branch> # 正しいブランチへ移動
git stash pop                 # 変更を復元
```
