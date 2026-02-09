# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Claude Codeの機能を学習するためのプロジェクト。2025年9月以降の新機能をキャッチアップし、日々の開発作業を効率化するワークフローを構築する。

## Learning Context

- 対象者: Claude Code経験者（基本操作習得済み、hooks/カスタムコマンド作成経験あり）
- 学習計画: `docs/claude-code-learning-plan.md`

## Current Progress

学習進捗は`docs/claude-code-learning-plan.md`の冒頭チェックリストで管理。
学習再開時は進捗を確認し、次のフェーズから開始する。
 
## Learning Phases (7 Phases, ~9-14 days)

1. **基盤の更新** - CLAUDE.md最適化、.claude/rules/、settings.json
2. **Hooksの高度な活用** - prompt/agent hooks、async hooks、新イベント
3. **Skills & Subagents** - SKILL.md作成、カスタムエージェント
4. **MCP統合** - MCPサーバー接続、GitHub/Sentry連携
5. **プラグイン** - マーケットプレイス、カスタムプラグイン
6. **高度なワークフロー** - ヘッドレスモード、CI/CD、環境統合
7. **統合と最適化** - ワークフロー統合、トラブルシューティング

## ルール
- CLAUDE.mdや.claude/rules/などのサンプルのMarkdownは日本語とする
- サンプルコードのコメントは日本語とする

### 新規ファイル作成時のルール
- 1. 必ず最初に空のファイルを`touch /path/to/file`で作成する
- 2. 内容を書き込む

## プロジェクト構造

```
/workspaces/learn-claude-code/    ← Gitリポジトリのルート
└── app/                          ← Pythonプロジェクトのルート（pyproject.toml、.envがここにある）
    ├── pyproject.toml
    ├── .env
    ├── utils/
    └── tests/
```

**重要**: `pyproject.toml`と`.env`が`app/`ディレクトリにあるため、**すべてのuvコマンドは`app/`ディレクトリから実行**してください。

## よく使うコマンド

**前提**: 以下のコマンドはすべて`app/`ディレクトリから実行してください。

```bash
# ディレクトリ移動
cd /workspaces/learn-claude-code/app

# アプリ実行
uv run python main.py

# リント・フォーマット・型チェック
uv run ruff check .
uv run ruff format .
uv run ty check .

# テスト実行
uv run pytest tests/ -v

# カバレッジ付きテスト
uv run pytest tests/ --cov=app --cov-report=term-missing

# 特定のテストファイルを実行
uv run pytest tests/utils/test_text.py -v
```

## Key Commands for Learning

```bash
# 学習再開
claude
# → "学習を再開します"

# フック確認
/hooks

# MCP確認
/mcp

# プラグイン確認
/plugin

# エージェント確認
/agents

# 設定確認
ls -la ~/.claude/
ls -la .claude/
```

## 学習の再開

「学習を再開します」と言われたら`docs/claude-code-learning-plan.md`を読んで、進捗管理チェックリストを確認し、次のフェーズから開始してください。

## 既知の不具合（2026年2月時点）

**重要:** Claude Codeには以下の既知の不具合があります。作業時は注意してください。

### 1. パスベースのルールがWrite操作で適用されない
- **イシュー:** [#23478](https://github.com/anthropics/claude-code/issues/23478)
- **影響:** `.claude/rules/`のpath-basedルールが新規ファイル作成時に無視される
- **対処:** 重要なファイル作成規約はCLAUDE.mdにも記載する、またはPostToolUseフックで対処

### 2. CLAUDE.mdのルールが無視される場合がある
- **イシュー:** [#19635](https://github.com/anthropics/claude-code/issues/19635), [#20401](https://github.com/anthropics/claude-code/issues/20401)
- **対処:** 重要なルールは短く明確に記述し、Stop hookでリマインダーを実装

### 3. `.claudeignore`が機能しない（セキュリティ問題）
- **影響:** `.env`など機密ファイルがignoreされない
- **対処:** 機密ファイルはプロジェクト外で管理する、PreToolUseフックでブロック

### 4. 設定の構文問題
- 絶対パスは`//`で始める必要がある（`/`ではない）
- `permissions.deny`はファイルのメモリロードを防げない可能性

**詳細:** `docs/claude-code-learning-plan.md`のセクション1.3参照