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

## よく使うコマンド

```bash
# アプリ実行
uv run python app/main.py

# リント・フォーマット・型チェック
uv run ruff check app/
uv run ruff format app/
uv run ty check app/
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