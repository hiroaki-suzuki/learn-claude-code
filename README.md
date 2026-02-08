# Claude Codeの再学習

Claude Codeの再学習のための学習プロジェクト。
Claude Codeが先生となり、学習計画を立てて、私が生徒となり学習を進める。

## 学習内容

2025年9月以降に追加されたClaude Codeの新機能をキャッチアップし、日々の開発作業を効率化するワークフローを構築する。

### 学習フェーズ

1. 基盤の更新 — CLAUDE.md最適化、`.claude/rules/`、settings.json
2. Hooksの高度な活用 — prompt/agent hooks、async hooks
3. Skills & Subagents — SKILL.md作成、カスタムエージェント
4. MCP統合 — MCPサーバー接続、GitHub/Sentry連携
5. プラグイン — マーケットプレイス、カスタムプラグイン
6. 高度なワークフロー — ヘッドレスモード、CI/CD、環境統合
7. 統合と最適化 — ワークフロー統合、トラブルシューティング

## 技術スタック

- **[Python 3.14](https://docs.python.org/3.14/)**: Python 
- **[uv](https://docs.astral.sh/uv/)**: Pythonパッケージマネージャー
- **[Ruff](https://docs.astral.sh/ruff/)**: Pythonのlinter/formatter
- **[Ty](https://docs.astral.sh/ty/)**: Python型チェッカー
- **[Claude Code](https://code.claude.com/docs/ja/overview/)**: コーディングエージェント

## コマンド

```bash
# アプリ実行
uv run python app/main.py

# リント・フォーマット・型チェック
uv run ruff check app/
uv run ruff format app/
uv run ty check app/
```
