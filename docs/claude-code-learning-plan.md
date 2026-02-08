# Claude Code 学習計画（2025年9月以降の新機能キャッチアップ）

> 作成日: 2026-02-08
> 対象: Claude Code経験者（基本操作習得済み、hooks/カスタムコマンド作成経験あり）
> 言語: Python 3.14（uv / Ruff / ty）
>
> **ツールチェーン参照:**
> - [uv](https://docs.astral.sh/uv/) - パッケージ管理・仮想環境
> - [Ruff](https://docs.astral.sh/ruff/) - リンター/フォーマッター
> - [ty](https://docs.astral.sh/ty/) - 型チェッカー

## 学習目標

日々の開発作業を効率化するため、Claude Codeの最新機能を習得し、実践的なワークフローを構築する。

## 進捗管理

各フェーズの完了後、以下のチェックリストを更新してください：

- [x] フェーズ1: 基盤の更新
- [ ] フェーズ2: Hooksの高度な活用
- [ ] フェーズ3: Skills & Subagents
- [ ] フェーズ4: MCP統合
- [ ] フェーズ5: プラグイン
- [ ] フェーズ6: 高度なワークフロー
- [ ] フェーズ7: 統合と最適化

---

## フェーズ1: 基盤の更新（0.5-1日）

### 1.0 事前学習（公式ドキュメントを読む）

**公式ドキュメント:**
- [Memory](https://code.claude.com/docs/en/memory) — CLAUDE.mdの配置レベル（4種）、`.claude/rules/`、`@import`構文、再帰的メモリ検索
- [Settings](https://code.claude.com/docs/en/settings) — 設定スコープの優先順位、permissions、環境変数設定

**日本語参考リソース:**
- [Claude Code の6種類のメモリと優先順位を理解して効率的に活用しよう](https://zenn.dev/kenfdev/articles/a8f8c5a24fd739) — 6種類のメモリの優先順位とLazy-Loadの仕組みを体系的に解説
- [脱・ファット・CLAUDE.md](https://zenn.dev/smartshopping/articles/refactor-fat-claude-md) — CLAUDE.mdの肥大化を`.claude/rules/`やインポートで解決する手法

### 1.1 CLAUDE.mdの最適化

**学習内容:**
- CLAUDE.mdの階層構造と配置場所
- `@path/to/import`によるファイルインポート
- `.claude/rules/*.md`によるモジュール化（paths frontmatterでの条件付きルール）

**CLAUDE.mdの配置場所:**
| メモリタイプ | 場所                                       | 用途                                        |
| ------------ | ------------------------------------------ | ------------------------------------------- |
| Managed      | OS固有のシステムディレクトリ               | 組織全体のポリシー（IT管理）                |
| User         | `~/.claude/CLAUDE.md`                      | 全プロジェクト共通の個人設定                |
| Project      | `./CLAUDE.md` または `./.claude/CLAUDE.md` | チーム共有（git管理）                       |
| Local        | `./CLAUDE.local.md`                        | プロジェクト固有・個人用（自動でgitignore） |

> **Note:** すべてのメモリファイルは起動時に自動読み込みされ、階層の上位が優先される。

**ベストプラクティス:**
- CLAUDE.mdは100-200行以内に収める
- よく使うコマンド（build, test, lint）を明記
- コーディング規約と命名規則を文書化
- アーキテクチャパターンを記載

**ルールファイルの配置場所:**
| 場所                   | 優先度 | 用途                                   |
| ---------------------- | ------ | -------------------------------------- |
| `.claude/rules/*.md`   | 高     | プロジェクト固有のルール（チーム共有） |
| `~/.claude/rules/*.md` | 低     | 全プロジェクト共通の個人ルール         |

> **Note:** User-level rules（`~/.claude/rules/`）はProject rulesより先にロードされ、Project rulesが優先される。

**なぜやるのか:**

Claude Codeはセッション開始時にCLAUDE.mdを読み込み、あなたの開発コンテキストを理解します。しかし、CLAUDE.mdが肥大化すると：
- 毎回のセッションでトークンを大量消費し、コストが増加する
- 重要な指示が埋もれて、Claudeが的確に従えなくなる
- チームメンバーと個人設定が混在し、管理が困難になる

この課題では、CLAUDE.mdを階層化・モジュール化することで「必要な情報だけを必要なタイミングで読み込む」構造を作ります。これにより、トークン効率が上がり、Claudeの指示遵守精度も向上します。

**実践課題:**
1. 現在のプロジェクトのCLAUDE.mdをレビューし、100-200行に最適化
2. `.claude/rules/`を作成し、以下のファイルを追加:
   - `code-style.md` - Pythonコードスタイル（Ruff/ty連携）
   - `testing.md` - pytest規約
   - `git-workflow.md` - Git運用ルール
3. `~/.claude/CLAUDE.md`にユーザーレベルの設定を作成
4. `~/.claude/rules/`に個人用の共通ルールを作成（オプション）

**検証:**
- Claudeに「Pythonのコードを書いて」と依頼し、`code-style.md` のルール（snake_case、型ヒント等）が適用されるか確認
- Claudeに「READMEを更新して」と依頼し、`code-style.md` が適用されない（`.py`のみ対象）ことを確認
- `.claude/rules/git-workflow.md` のコミットメッセージ規約に従ってコミットされるか確認

### 1.2 設定ファイルの理解

**学習内容:**
- `.claude/settings.json` - プロジェクト設定（チームで共有）
- `.claude/settings.local.json` - ローカル設定（gitignore対象）
- `~/.claude/settings.json` - ユーザー設定（全プロジェクト共通）

**設定スコープの優先順位（高→低）:**
1. **Managed** - システム管理者が設定（上書き不可）
2. **Command line arguments** - セッション一時的な上書き
3. **Local** (`.claude/settings.local.json`) - 個人のプロジェクト設定
4. **Project** (`.claude/settings.json`) - チーム共有設定
5. **User** (`~/.claude/settings.json`) - 個人のグローバル設定（最低優先度）

> **重要:** LocalがProjectを上書きするため、個人設定はLocal、チーム設定はProjectに配置。

**重要な設定項目:**
```json
{
  "permissions": {
    "allow": ["Bash(uv *)"],
    "deny": ["Bash(rm -rf *)"]
  },
  "hooks": {},
  "statusLine": {}
}
```

**なぜやるのか:**

Claude Codeの動作を制御するsettings.jsonは、どのスコープに設定するかで挙動が変わります。例えば：
- 特定プロジェクトでは`rm -rf`を禁止したいが、他のプロジェクトでは許可したい
- チーム全体の設定と個人の好みを分離したい
- CIパイプラインでの自動許可ルールを設定したい

設定の優先順位を理解することで、「なぜ設定が反映されないのか」というトラブルを防ぎ、チームと個人の設定を適切に共存させられるようになります。

**実践課題:**
1. 現在の`~/.claude/settings.json`のpermissionsを確認
2. プロジェクト固有のpermissionsを`.claude/settings.local.json`に設定

**検証:**
- `settings.local.json` の allow リストにあるコマンドが許可プロンプトなしで実行されることを確認
- `claude --debug` で読み込まれている設定ファイルを確認

**確認コマンド:**
```bash
# 設定ファイルの場所確認
ls -la ~/.claude/
ls -la .claude/

# Python環境確認
uv run ruff check app/
uv run ty check app/
```

### 1.3 既知の不具合と注意事項

**重要:** フェーズ1で扱うCLAUDE.mdとrulesシステムには、2026年2月時点で複数の既知の不具合があります。これらを理解した上で学習を進めてください。

#### 1.3.1 パスベースのルールがWrite操作で適用されない（重大）

**問題:** `.claude/rules/`で定義したpath-basedルールが、ファイル作成時（Write操作）に読み込まれない。

- **GitHubイシュー:** [#23478](https://github.com/anthropics/claude-code/issues/23478), #16853, #21858, #24112
- **影響:** ファイル作成規約の強制という主要ユースケースが機能しない
- **現象:**
  ```yaml
  ---
  paths:
    - "**/*.md"
  ---
  # Markdownファイル作成時は先頭に`# created`を追加する
  ```
  このようなルールを定義しても、`Write`ツールでの新規ファイル作成時には無視される。

**発生タイミング:**
- ✅ **Read操作**: ルールが正しく読み込まれる
- ✅ **Edit操作**: 既存ファイル編集前にReadが発生するため適用される
- ❌ **Write操作**: ルールが読み込まれず無視される
- ❌ **MultiEdit操作**: 同様に無視される可能性

**ワークアラウンド（暫定対処）:**
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
PostToolUseフックでWriteをトリガーし、手動でReadを実行してルールを強制読み込みする3ステップのワークアラウンドが必要。

**影響範囲:**
- ファイル作成規約を`.claude/rules/`で強制できない
- CLAUDE.mdにルールを重複記載するか、フックで対処する必要がある

#### 1.3.2 CLAUDE.mdのルールが無視される

**問題:** Claude CodeがCLAUDE.mdのルールを読み込んで確認応答した後も、繰り返しルールに違反する。

- **GitHubイシュー:** [#19635](https://github.com/anthropics/claude-code/issues/19635), [#20401](https://github.com/anthropics/claude-code/issues/20401)
- **影響:** ルール遵守の信頼性が低い、トークン浪費、手動修正の繰り返し
- **現象例:**
  - 「gitコミット前に必ず確認を求める」というルール → 確認なしでコミット・プッシュを3回繰り返す
  - 1セッションで14回以上のルール違反が発生したケースあり

**対処法:**
- Stop hookでルールリマインダーを表示（Zennの[ルール忘れる問題の解決](https://zenn.dev/kazuph/articles/483d6cf5f3798c)記事参照）
- PreToolUseフックで危険な操作を事前ブロック
- ルールを短く明確に記述し、重複して強調する

#### 1.3.3 `.claudeignore`が機能しない（セキュリティ問題）

**問題:** `.claudeignore`にファイルを追加しても、Claude Codeがそのファイルを読み込んでしまう。

- **報告:** [The Register記事](https://www.theregister.com/2026/01/28/claude_code_ai_secrets_files/)
- **影響:** `.env`など機密情報を含むファイルが保護されない
- **現象:**
  ```
  # .claudeignore
  .env
  ```
  このように設定しても、Claude Codeは`.env`ファイルの内容を読み取れる。

**対処法（暫定）:**
- `permissions.deny`を使用（ただし、メモリロードは防げない可能性あり）
- 機密ファイルをプロジェクトディレクトリ外に配置
- PreToolUseフックで特定ファイルへのアクセスをブロック
- **根本対策:** この問題が修正されるまで、機密情報をプロジェクト内に置かない

#### 1.3.4 設定の構文と挙動の問題

**問題:** 設定ファイルの構文や挙動に複数の問題がある。

1. **絶対パスの構文**
   - Linux/macOSでは`/`で始まるはずだが、Claude Codeでは`//`が必要
   - 例: `//home/user/project`（`/home/user/project`ではない）

2. **`@`ファイル参照構文**
   - settings.jsonでの`@import`構文に問題報告あり

3. **`permissions.deny`の制限**
   - ファイルをメモリにロードすることは防げない可能性
   - ツール実行のみブロック

**対処法:**
- 絶対パスは`//`で始める
- `@import`構文は慎重にテストする
- permissions.denyは「実行防止」と理解し、「読み込み防止」には別の手段を使う

#### 1.3.5 品質劣化（2026年1月下旬以降）

**問題:** 2026年1月26日以降、Claude Codeの応答品質が低下した報告あり。

- **GitHubイシュー:** [#21431](https://github.com/anthropics/claude-code/issues/21431)
- **現象:**
  - 問題を深く考えずに複数の壊れた試行を繰り返す
  - 思考プロセスが浅くなった

**対処法:**
- より明確で詳細な指示を与える
- 段階的なアプローチを指示する
- 計画モード（`--permission-mode plan`）を活用

#### 1.3.6 実践課題への影響

これらの不具合を踏まえ、フェーズ1の実践課題では：

1. **CLAUDE.md最適化時:**
   - ルールが無視される前提で、重要なルールは短く明確に記述
   - フック併用を検討

2. **`.claude/rules/`作成時:**
   - path-basedルールはWrite操作で機能しないことを認識
   - ファイル作成規約はCLAUDE.mdにも記載するか、PostToolUseフックで対処

3. **`.claudeignore`の使用:**
   - セキュリティ上重要なファイルは、ignoreに頼らず物理的に分離
   - `.env`などはプロジェクト外で管理

4. **検証時の注意:**
   - ルールが適用されない場合、不具合の可能性を考慮
   - ワークアラウンドの実装を学習の一環とする

---

## フェーズ2: Hooksの高度な活用（1.5-2日）

> 既にhooks経験があるため、2025/9以降に追加された新機能に注力

### 2.0 事前学習（公式ドキュメントを読む）

**公式ドキュメント:**
- [Hooks Guide](https://code.claude.com/docs/en/hooks-guide) — Hooksの概要、設定方法、実践例
- [Hooks Reference](https://code.claude.com/docs/en/hooks) — 全12イベントのリファレンス、3種のフックタイプ、matcher、async、出力JSON仕様

**日本語参考リソース:**
- [Claude Codeの「すぐルール忘れる問題」をHooksで解決する](https://zenn.dev/kazuph/articles/483d6cf5f3798c) — Stop Hookでルールリマインダーを実装する実践例
- [【コピペOK】Claude Codeのデータ削除・危険コマンドを防止するHooksの使い方](https://zenn.dev/tmasuyama1114/articles/claude_code_hooks_guard_bash_command) — PreToolUseでの危険コマンドブロック実装

### 2.1 フックイベント一覧

**全イベント一覧（公式ドキュメント準拠）:**

| イベント             | 発火タイミング                 | 用途                             |
| -------------------- | ------------------------------ | -------------------------------- |
| `SessionStart`       | セッション開始/再開時          | 環境変数設定、コンテキスト注入   |
| `UserPromptSubmit`   | プロンプト送信後、Claude処理前 | プロンプト検証、コンテキスト追加 |
| `PreToolUse`         | ツール実行前                   | ツール呼び出しのブロック/許可    |
| `PermissionRequest`  | 許可ダイアログ表示時           | 自動許可/拒否                    |
| `PostToolUse`        | ツール成功後                   | 結果検証、追加処理               |
| `PostToolUseFailure` | ツール失敗後                   | エラーログ、アラート             |
| `Notification`       | 通知送信時                     | カスタム通知                     |
| `SubagentStart`      | サブエージェント起動時         | コンテキスト注入                 |
| `SubagentStop`       | サブエージェント終了時         | 結果検証                         |
| `Stop`               | Claude応答完了時               | 完了通知、追加タスク             |
| `PreCompact`         | コンパクション前               | コンテキスト保存                 |
| `SessionEnd`         | セッション終了時               | クリーンアップ、ログ保存         |

**SessionStartのmatcher値:**
| matcher   | 発火タイミング                                      |
| --------- | --------------------------------------------------- |
| `startup` | 新規セッション開始                                  |
| `resume`  | `--resume`、`--continue`、`/resume`でセッション再開 |
| `clear`   | `/clear`実行後                                      |
| `compact` | 自動/手動コンパクション後                           |

> **CHANGELOG情報:** `--init`、`--init-only`、`--maintenance`フラグで`Setup`イベントが発火するとの記載あり（hooks referenceには未掲載、要確認）。

### 2.2 フックの種類（重要な新機能）

**command hooks** - 従来のシェルコマンド実行
```json
{
  "type": "command",
  "command": "./scripts/format.sh"
}
```

**prompt hooks** - LLMによる評価（新機能）
```json
{
  "type": "prompt",
  "prompt": "Evaluate if Claude should stop: $ARGUMENTS. Check if all tasks are complete.",
  "timeout": 30
}
```

**agent hooks** - ツール使用可能な検証エージェント（新機能）
```json
{
  "type": "agent",
  "prompt": "Verify that all unit tests pass. Run the test suite and check the results. $ARGUMENTS",
  "timeout": 120
}
```

### 2.3 SessionStartでの環境変数永続化

**`CLAUDE_ENV_FILE`の活用:**

> **重要:** `CLAUDE_ENV_FILE`は**SessionStart hookでのみ**利用可能。他のhookでは使用不可。

```bash
#!/bin/bash
# ~/.claude/hooks/session-setup.sh

if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=development' >> "$CLAUDE_ENV_FILE"
  echo 'export DEBUG=true' >> "$CLAUDE_ENV_FILE"
fi
exit 0
```

### 2.4 async hooks（バックグラウンド実行）

> **重要:** `async: true`は**command hookのみ**に適用可能。prompt hookやagent hookでは使用不可。

```json
{
  "type": "command",
  "command": "./scripts/run-tests.sh",
  "async": true,
  "timeout": 300
}
```

- Claudeをブロックせずにバックグラウンドで実行
- 完了時の結果は次の会話ターンでClaudeに通知
- `decision`や`permissionDecision`などの制御は効果なし（アクションは既に完了済み）

### 2.5 実践課題

**なぜやるのか:**

Hooksは「Claudeの行動に対するガードレールと自動化」です。手動で毎回行っている作業を自動化できます：
- **Stop通知**：長時間タスクの完了をMac通知で知る → ターミナルを見張る必要がなくなる
- **自動フォーマット**：ファイル編集後に自動でprettier/ESLintを実行 → 手動フォーマットの手間を省く
- **完了検証**：prompt hookでタスク完了度をLLMが判定 → 「まだ終わってないのに完了した」問題を防ぐ
- **危険コマンドブロック**：`rm -rf`等をPreToolUseで事前に止める → 事故を未然に防ぐ

各フックを1つずつ作りながら、Hooksの仕組みを体験的に理解していきます。

1. **Mac通知フック（Stop）**
```bash
#!/bin/bash
# ~/.claude/hooks/notify-stop.sh
osascript -e 'display notification "Claude has finished" with title "Claude Code" sound name "Glass"'
exit 0
```

2. **自動フォーマットフック（PostToolUse）** - Ruffで自動フォーマット
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "cd \"$CLAUDE_PROJECT_DIR/app\" && uv run ruff format --quiet"
          }
        ]
      }
    ]
  }
}
```

3. **prompt hookでのStop検証**
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Analyze if all user tasks are complete: $ARGUMENTS. Respond with {\"ok\": true} or {\"ok\": false, \"reason\": \"...\"}",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

4. **危険なコマンドブロック（PreToolUse）**

> **exit codeの使い分け:**
> - `exit 0`: 成功。stdoutのJSONが処理される
> - `exit 2`: ブロック。stdoutは**無視**され、stderrがエラーメッセージとしてClaudeに返される

```bash
#!/bin/bash
# ~/.claude/hooks/block-dangerous.sh
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if echo "$COMMAND" | grep -qE 'rm -rf|git push --force'; then
  # exit 2時はstderrにシンプルなテキストを出力（JSONは不要）
  echo "Dangerous command blocked: $COMMAND" >&2
  exit 2
fi
exit 0
```

**exit 0でJSON制御する場合（公式hooks reference準拠）:**

> **Note:** PreToolUseは`hookSpecificOutput`で`permissionDecision`（allow/deny/ask）を使用。
> これはPreToolUse専用フィールドで、PermissionRequest向けではない。

```bash
#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if echo "$COMMAND" | grep -qE 'rm -rf'; then
  # exit 0でJSONを出力して制御
  jq -n '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: "Destructive command blocked"
    }
  }'
else
  exit 0
fi
```

**PreToolUseのpermissionDecision値:**
| 値      | 効果                                           |
| ------- | ---------------------------------------------- |
| `allow` | 許可システムをバイパスしてツール実行を許可     |
| `deny`  | ツール呼び出しをブロック（理由をClaudeに表示） |
| `ask`   | ユーザーに確認を求める                         |

**検証:**
- Stop通知: Claudeにタスクを依頼し、完了時にターミナルにベル音と視覚的メッセージが表示されることを確認
- 自動フォーマット: Pythonファイルを編集させ、Ruff formatが自動実行されることを確認（インデントやクォートの変換で判断）
- prompt hook: 不完全なタスク指示でClaudeが「まだ終わっていない」と判定するか確認
- 危険コマンドブロック: Claudeに `rm -rf /tmp/test` を実行させようとし、ブロックされることを確認

---

## フェーズ3: Skills & Subagents（2-3日）

### 3.0 事前学習（公式ドキュメントを読む）

**公式ドキュメント:**
- [Skills](https://code.claude.com/docs/en/skills) — SKILL.mdの構造、フロントマター、動的コンテキスト注入、配置場所
- [Sub-agents](https://code.claude.com/docs/en/sub-agents) — ビルトイン/カスタムエージェント、frontmatter設定、CLIフラグ

**日本語参考リソース:**
- [濫立するClaude Codeの機能の使い分け](https://zenn.dev/notahotel/articles/a175aa95629d0b) — Skills/Subagents/Hooks/CLAUDE.mdの役割分担を体系的に整理
- [Claude Code でカスタムサブエージェントを作成する](https://azukiazusa.dev/blog/create-custom-sub-agent-in-claude-code/) — `/agents`からの作成手順とYAMLフロントマター構成

### 3.1 Skills システム

**SKILL.mdの構造:**
```yaml
---
name: my-skill
description: Skillの説明（Claudeが自動選択に使用）
disable-model-invocation: true  # ユーザーのみ呼び出し可能（Claudeが自動実行しない）
allowed-tools: Read, Grep, Glob  # 許可プロンプトなしで使用可能なツール（事前許可）
context: fork  # サブエージェントで実行
agent: Explore  # 使用するエージェントタイプ
model: sonnet  # モデル指定
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
---

# Skill本体（Claudeへの指示）

ここにSkillの内容を記述...
```

**Skillフロントマターの主要フィールド:**
| フィールド                 | 説明                                          |
| -------------------------- | --------------------------------------------- |
| `name`                     | 表示名（省略時はディレクトリ名）              |
| `description`              | 用途説明（Claudeが自動選択に使用）            |
| `disable-model-invocation` | `true`でユーザーのみ呼び出し可能              |
| `user-invocable`           | `false`でメニューから非表示（Claudeのみ使用） |
| `allowed-tools`            | 許可プロンプトなしで使用可能なツール          |
| `context`                  | `fork`でサブエージェントとして実行            |
| `agent`                    | 使用するエージェントタイプ（Explore, Plan等） |
| `model`                    | 使用モデル（sonnet, opus, haiku）             |

**動的コンテキスト注入:**
```yaml
---
name: pr-summary
description: PRの要約を作成
context: fork
---

## PRコンテキスト
- PR diff: !`gh pr diff`
- 変更ファイル: !`gh pr diff --name-only`

## タスク
このPRを要約してください...
```

**Skillの保存場所:**
| 場所                               | 用途               |
| ---------------------------------- | ------------------ |
| `~/.claude/skills/<name>/SKILL.md` | 全プロジェクト共通 |
| `.claude/skills/<name>/SKILL.md`   | プロジェクト固有   |

### 3.2 カスタムサブエージェント

**.claude/agents/code-reviewer.md:**
```yaml
---
name: code-reviewer
description: コードレビュー専門。コード変更後に積極的に使用。
tools: Read, Grep, Glob, Bash
model: sonnet
permissionMode: dontAsk
---

あなたはシニアコードレビュアーです。

レビュー時の観点:
1. コードの可読性
2. エラーハンドリング
3. セキュリティ
4. テストカバレッジ
5. パフォーマンス

優先度別にフィードバックを整理:
- Critical（必須修正）
- Warning（推奨修正）
- Suggestion（提案）
```

**CLIでのエージェント指定:**
```bash
claude --agents '{
  "quick-reviewer": {
    "description": "高速レビュー",
    "prompt": "重要な問題のみ報告",
    "tools": ["Read", "Grep"],
    "model": "haiku"
  }
}'
```

### 3.3 組み込みエージェント

**主要エージェント:**
| エージェント    | モデル | 用途                                   |
| --------------- | ------ | -------------------------------------- |
| Explore         | Haiku  | コードベース探索（読み取り専用、高速） |
| Plan            | 継承   | 計画モードでの調査（読み取り専用）     |
| general-purpose | 継承   | 複雑な多段階タスク（全ツール使用可）   |

**その他のヘルパーエージェント:**
| エージェント      | モデル | 用途                                     |
| ----------------- | ------ | ---------------------------------------- |
| Bash              | 継承   | ターミナルコマンドを別コンテキストで実行 |
| statusline-setup  | Sonnet | `/statusline`でステータスライン設定      |
| claude-code-guide | Haiku  | Claude Codeの機能についての質問応答      |

**エージェントの無効化:**
```json
{
  "permissions": {
    "deny": ["Task(Explore)", "Task(my-custom-agent)"]
  }
}
```

### 3.4 実践課題

**なぜやるのか:**

日常の開発作業には「何度も繰り返すパターン」があります：
- コード変更後にレビューする → 毎回同じプロンプトを打つのは非効率
- エラーが出たらデバッグする → 毎回「分析して」と指示するのが手間
- テストを実行して結果を確認する → 手順が決まっているのに毎回説明する

Skills（`/review`のようなスラッシュコマンド）とカスタムエージェントを作ることで、これらの定型作業をワンコマンドで実行できるようになります。また、`context: fork`でサブエージェントとして実行すれば、メインの会話コンテキストを消費せずに処理を委譲できます。

1. **コードレビューSkill（/review）**
```yaml
---
name: review
description: コード変更のレビュー
disable-model-invocation: true
context: fork
agent: Explore
---

!`git diff`

上記の変更をレビューし、問題点を報告してください。
```

2. **デバッグエージェント**
```yaml
---
name: debugger
description: エラー解析とデバッグ
tools: Read, Edit, Bash, Grep, Glob
model: sonnet
---

エラーの根本原因を分析し、修正を提案してください。
```

3. **テスト実行Skill**
```yaml
---
name: test
description: テストを実行して結果を報告
disable-model-invocation: true
allowed-tools: Bash(uv run pytest *)
---

テストスイートを実行し、失敗したテストの原因を分析してください。
```

**検証:**
- `/review` を実行し、Skillが認識されて差分レビューが実行されることを確認
- カスタムエージェントが `/agents` コマンドで表示されることを確認
- `context: fork` のSkillがサブエージェントとして実行され、メインコンテキストを消費しないことを確認

---

## フェーズ4: MCP統合（2日）

### 4.0 事前学習（公式ドキュメントを読む）

**公式ドキュメント:**
- [MCP](https://code.claude.com/docs/en/mcp) — トランスポート、スコープ、OAuth認証、Tool Search、MCP Resources/Prompts、`claude mcp serve`

**日本語参考リソース:**
- [Claude CodeからMCPを利用する、Claude CodeをMCPとして利用する](https://qiita.com/nokonoko_1203/items/99b9965d1eb63476b18c) — MCPの双方向連携を解説
- [Claude CodeでMCPを快適に使う設定術](https://zenn.dev/kuxu/articles/c832ccf26b7cce) — `--mcp-config`やTool Searchによるコンテキスト節約テクニック

### 4.1 MCPサーバーの追加

**HTTPトランスポート（推奨）:**
```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp
```

**SSEトランスポート（⚠️ 非推奨）:**
> **Warning:** SSE (Server-Sent Events) トランスポートは非推奨。可能な限りHTTPを使用。

```bash
claude mcp add --transport sse sentry https://mcp.sentry.dev/mcp
```

**STDIOトランスポート:**
```bash
claude mcp add --transport stdio --env GITHUB_TOKEN=$GITHUB_TOKEN github \
  -- npx -y @modelcontextprotocol/server-github
```

### 4.2 スコープ

| スコープ  | 保存場所                                 | 用途                                   | 共有 |
| --------- | ---------------------------------------- | -------------------------------------- | ---- |
| `local`   | `~/.claude.json`（プロジェクトパスごと） | プロジェクト固有・個人用（デフォルト） | No   |
| `project` | `.mcp.json`                              | チーム共有（git管理）                  | Yes  |
| `user`    | `~/.claude.json`（mcpServersフィールド） | 全プロジェクト共通                     | No   |

```bash
# スコープ指定例
claude mcp add --scope local notion --transport http https://mcp.notion.com/mcp   # デフォルト
claude mcp add --scope project sentry --transport http https://mcp.sentry.dev/mcp  # チーム共有
claude mcp add --scope user github --transport http https://api.githubcopilot.com/mcp/  # 全プロジェクト
```

> **Note:** project scopeの`.mcp.json`を使用する場合、Claude Codeは初回使用時に承認を求める。

### 4.3 Claude Code自体をMCPサーバーとして公開

```bash
claude mcp serve
```

**Claude Desktopから接続:**
```json
{
  "mcpServers": {
    "claude-code": {
      "type": "stdio",
      "command": "claude",
      "args": ["mcp", "serve"]
    }
  }
}
```

### 4.4 実用的なMCPサーバー

1. **GitHub MCP** - PR/Issue操作
```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

2. **Sentry MCP** - エラー監視
```bash
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
```

3. **Database MCP** - データベースクエリ
```bash
claude mcp add --transport stdio db -- npx -y @bytebase/dbhub \
  --dsn "postgresql://user:pass@host:5432/db"
```

### 4.5 実践課題

**なぜやるのか:**

MCPサーバーを使うと、Claude Codeが外部サービスに直接アクセスできるようになります：
- **GitHub MCP**：ブラウザを開かずにPR作成・Issue管理 → コンテキストスイッチを減らす
- **Sentry MCP**：エラー情報をClaudeが直接取得して分析 → 「エラーログをコピペして」の手間を省く
- **`.mcp.json`でチーム共有**：新メンバーがMCPの設定を手動でする必要がなくなる

この課題ではGitHub MCPを実際に設定し、Claudeがターミナル内でPR操作できることを確認します。

1. GitHub MCPを設定してPR操作を試す
2. `.mcp.json`でプロジェクト固有のMCPサーバーを設定
3. `/mcp`コマンドで接続状態を確認

**検証:**
- `/mcp` でMCPサーバーの接続状態が「connected」と表示されることを確認
- MCPツール（例: GitHub MCPのPR一覧取得）を実際に呼び出して結果が返ることを確認
- `.mcp.json` でproject scopeに追加したサーバーが新規セッションで承認プロンプトが出ることを確認

---

## フェーズ5: プラグイン（2日）

### 5.0 事前学習（公式ドキュメントを読む）

**公式ドキュメント:**
- [Plugins](https://code.claude.com/docs/en/plugins) — プラグインの概要と使い方
- [Plugins Reference](https://code.claude.com/docs/en/plugins-reference) — plugin.jsonマニフェスト、ディレクトリ構造の詳細リファレンス

**日本語参考リソース:**
- [続・Claude Code公式Pluginのすすめ+α](https://zenn.dev/modokkin/articles/zenn-2026-01-06-claude-code-plugins-update) — 2026年1月時点の最新情報、13個の公式プラグインの活用法
- [Claude Code Plugin を開発するプラグイン plugin-dev で自作プラグイン開発のハードルを下げる](https://zenn.dev/ashita_team/articles/claude-code-plugin-dev) — 公式plugin-devを使った対話形式でのプラグイン作成

### 5.1 プラグインの管理

**CLIコマンド:**
```bash
# インストール（マーケットプレイス指定あり/なし）
claude plugin install formatter --scope user
claude plugin install formatter@my-marketplace --scope project

# リスト表示
claude plugin list

# 有効化/無効化
claude plugin enable formatter
claude plugin disable formatter

# アンインストール（エイリアス: remove, rm）
claude plugin uninstall formatter

# 更新
claude plugin update formatter --scope user
```

> **Note:** `/plugin`コマンドでインタラクティブにプラグインを探索・管理可能。

**スコープ:**
| スコープ | 用途                                |
| -------- | ----------------------------------- |
| user     | 個人用（デフォルト）                |
| project  | チーム共有（.claude/settings.json） |
| local    | プロジェクト固有・gitignore         |

### 5.2 プラグインの構造

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json      # マニフェスト
├── skills/              # Skills
│   └── my-skill/
│       └── SKILL.md
├── agents/              # エージェント
│   └── my-agent.md
├── hooks/               # Hooks
│   └── hooks.json
├── .mcp.json            # MCPサーバー
└── scripts/             # スクリプト
```

**plugin.json:**
```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "プラグインの説明",
  "author": {
    "name": "Your Name"
  },
  "skills": "./skills/",
  "agents": "./agents/",
  "hooks": "./hooks/hooks.json",
  "mcpServers": "./.mcp.json"
}
```

### 5.3 LSPプラグイン

LSPプラグインでコード補完と定義ジャンプを有効化:

**.lsp.json:**
```json
{
  "typescript": {
    "command": "typescript-language-server",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".ts": "typescript",
      ".tsx": "typescriptreact"
    }
  }
}
```

### 5.4 実践課題

**なぜやるのか:**

プラグインは、Skills・Hooks・エージェント・MCPサーバーを1つのパッケージにまとめる仕組みです：
- **配布と再利用**：チームや個人の設定をパッケージ化して簡単にインストール
- **マーケットプレイス**：コミュニティが作った便利な設定を`claude plugin install`で即座に使える
- **一貫性**：プロジェクトに必要なClaude Code設定を丸ごとgit管理

この課題では、まず公式マーケットプレイスのプラグインを体験してから、自分用のプラグインパッケージを作成します。これにより、今後新しいプロジェクトでも設定を即座に再現できるようになります。

1. 公式マーケットプレイスからプラグインを探索・インストール
2. 自分用のプラグインパッケージを作成（skills + hooks）
3. `/plugin`でプラグイン状態を確認

**検証:**
- `claude plugin list` でインストール済みプラグインが表示されることを確認
- プラグインのSkillが `/` コマンドで表示されることを確認
- `claude plugin disable <name>` → `claude plugin enable <name>` のライフサイクルが正常に動作することを確認

---

## フェーズ6: 高度なワークフロー（2-3日）

### 6.0 事前学習（公式ドキュメントを読む）

**公式ドキュメント:**
- [Headless Mode](https://code.claude.com/docs/en/headless) — `-p`オプション、Agent SDK、出力フォーマット、セッション継続
- [GitHub Actions](https://code.claude.com/docs/en/github-actions) — GitHub Actionsでの`@claude`メンション統合
- [CLI Reference](https://code.claude.com/docs/en/cli-reference) — 全CLIフラグのリファレンス

**日本語参考リソース:**
- [Claude Code ベストプラクティス](https://zenn.dev/farstep/articles/claude-code-best-practices) — CI/CDでのファンアウト/パイプライニングパターンを解説
- [[翻訳] Anthropic ハッカソン優勝者による Claude Code 完全ガイド【応用編】](https://zenn.dev/studypocket/articles/claude-code-complete-guide-advanced) — トークンエコノミクス、並列化戦略など高度テクニック

### 6.1 ヘッドレスモード（CI/CD統合）

**基本使用:**
```bash
claude -p "失敗しているテストを修正して" --allowedTools "Read,Edit,Bash"
```

**構造化出力:**
```bash
claude -p "List all API endpoints" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"endpoints":{"type":"array","items":{"type":"string"}}}}'
```

**ストリーミング:**
```bash
claude -p "Explain this code" --output-format stream-json --verbose
```

**セッション継続:**
```bash
# 最新セッションを継続（-c または --continue）
claude -c -p "Continue the review"

# 特定セッションを再開（-r または --resume）
claude -r "$SESSION_ID" -p "Continue"

# セッションIDを取得して後で再開
session_id=$(claude -p "Start a review" --output-format json | jq -r '.session_id')
claude -r "$session_id" -p "Continue that review"
```

**--allowedToolsと--toolsの違い:**
- `--allowedTools`: 許可プロンプトなしで実行してよいツール
- `--tools`: 使用可能なツール自体を制限（省略時は全ツール）

### 6.2 並列処理とコンテキスト管理

**チェックポイントと/rewind:**
- `Esc` + `Esc` でrewindメニューを開く
- `/rewind`コマンドでも同様
- 会話のみ/コードのみ/両方を復元可能

**コンパクション:**
- `/compact` で手動コンパクション
- 自動コンパクションは95%で発動（`CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`で変更可能）

### 6.3 ステータスラインカスタマイズ

**/statusline または settings.json:**
```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh",
    "padding": 0
  }
}
```

**statusline.sh:**
```bash
#!/bin/bash
input=$(cat)

MODEL=$(echo "$input" | jq -r '.model.display_name')
CURRENT_DIR=$(echo "$input" | jq -r '.workspace.current_dir')
PERCENT_USED=$(echo "$input" | jq -r '.context_window.used_percentage // 0')
COST=$(echo "$input" | jq -r '.cost.total_cost_usd // 0')

# Git branch
GIT_BRANCH=""
if git rev-parse --git-dir > /dev/null 2>&1; then
  BRANCH=$(git branch --show-current 2>/dev/null)
  if [ -n "$BRANCH" ]; then
    GIT_BRANCH=" | 🌿 $BRANCH"
  fi
fi

printf "[$MODEL] 📁 ${CURRENT_DIR##*/}$GIT_BRANCH | 📊 %.0f%% | 💰 \$%.4f" "$PERCENT_USED" "$COST"
```

### 6.4 環境統合

**Zellij連携:**
```bash
# 新しいペインでClaude Code
zellij action new-pane -- claude

# セッション再開
zellij action new-pane -- claude --resume
```

**yazi連携（カスタムコマンド）:**
```bash
# yazi.tomlに追加
[[manager.prepend_keymap]]
on = ["c", "c"]
run = '''shell --interactive 'claude -p "Analyze this file: $1" "$@"' '''
desc = "Claude Codeで分析"
```

### 6.5 実践課題

**なぜやるのか:**

ここまでに学んだ個々の機能を、実際の開発ワークフローに統合します：
- **ステータスライン**：モデル名・コスト・Git情報を常時表示 → トークン消費を意識しながら作業できる
- **ヘッドレスモード（CI/CD）**：GitHub Actionsからコードレビューや修正を自動実行 → 人手を介さない品質チェック
- **ターミナル連携**：Zellij/tmuxのペインでClaudeを並列起動 → 複数タスクを同時進行

これらを組み合わせることで、「Claudeを呼び出す → 結果を待つ → 次の指示」という直列作業から、「複数のClaudeが並列で動く効率的なワークフロー」へ移行できます。

1. statusline.shを作成してGit情報とコスト表示
2. GitHub Actionsワークフローでヘッドレスモード使用
3. Zellij/tmuxとの連携スクリプト作成

**検証:**
- ステータスラインにモデル名・コスト・Git branch が表示されることを確認
- `claude -p "echo hello" --output-format json` でJSON出力が得られることを確認
- セッション継続: `claude -p "..." --output-format json` でsession_id取得 → `claude -r $session_id -p "..."` で会話が継続することを確認

---

## フェーズ7: 統合と最適化（1日）

### 7.0 事前学習（公式ドキュメントを読む）

**公式ドキュメント:**
- [Features Overview](https://code.claude.com/docs/en/features-overview) — 全機能の使い分け・コンテキストコスト・組み合わせパターンの比較一覧

### 7.1 日常開発ワークフロー

**推奨パターン:**
1. 新機能開始時: 新しいGitブランチ作成
2. 複雑なタスク: Planモード（`claude --permission-mode plan`）で調査
3. 実装中: サブエージェントで詳細調査を委譲
4. 完了後: /reviewスキルでコードレビュー
5. コミット前: hooksで自動フォーマット・テスト

**コンテキスト管理:**
- `/clear`を頻繁に使用（新タスク開始時）
- サブエージェントで大量の出力を分離
- チェックポイントで安全にロールバック

### 7.2 トラブルシューティング

**デバッグモード:**
```bash
claude --debug
```

**よくある問題:**

| 問題                       | 原因                 | 解決法                   |
| -------------------------- | -------------------- | ------------------------ |
| プラグインが読み込まれない | 無効なplugin.json    | `/plugin validate`で検証 |
| hooksが発火しない          | スクリプトが実行不可 | `chmod +x script.sh`     |
| MCPサーバー接続失敗        | パス/認証エラー      | `claude --debug`で確認   |
| Skillが見つからない        | 間違ったディレクトリ | `~/.claude/skills/`確認  |

### 7.3 パフォーマンス最適化

- CLAUDE.mdは100-200行以内
- 不要なMCPサーバーは切断
- `/mcp`でトークンコスト確認
- `disable-model-invocation: true`でSkillのコンテキストコスト削減

---

## 補足: 2025年9月以降の主な新機能

CHANGELOGに基づく、学習計画に含まれていない追加機能：

### タスク管理システム
```bash
# 環境変数で無効化可能
CLAUDE_CODE_ENABLE_TASKS=false claude
```
- 依存関係追跡付きタスクリスト
- TaskCreate、TaskUpdate、TaskListツール

### カスタマイズ可能なキーバインド
```bash
/keybindings  # 設定インターフェースを開く
```
- コードシーケンス対応
- `~/.claude/keybindings.json`で設定

### 言語設定
```json
{
  "language": "japanese"  // Claudeの応答言語を設定（言語名を使用、コードではない）
}
```
> **Note:** 値は言語コード（"ja"）ではなく、言語名（"japanese", "spanish", "french"等）を使用。

### PRリンク機能
```bash
claude --from-pr  # 特定のGitHub PRにリンクしたセッションを再開
```
- `gh pr create`で自動リンク
- PRレビューステータスのインジケーター表示

### MCPの新機能
- **list_changed通知**: MCPサーバーがツール/プロンプト/リソースを動的に更新可能
- **Tool Search**: MCPツールが多い場合に自動有効化（コンテキストの10%超過時）
  ```bash
  ENABLE_TOOL_SEARCH=auto:5 claude  # 5%閾値で有効化
  ENABLE_TOOL_SEARCH=false claude   # 無効化
  ```

### その他の設定
- `spinnerVerbs`: スピナーテキストのカスタマイズ
- `showTurnDuration`: ターン所要時間表示の制御
- `plansDirectory`: 計画ファイルの保存場所指定
- `respectGitignore`: プロジェクトごとのgitignore設定制御

---

## 学習リソース

### 公式ドキュメント
- [Claude Code Docs](https://code.claude.com/docs/en/)
- [CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
- [ドキュメントインデックス](https://code.claude.com/docs/llms.txt)

### コミュニティリソース
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) - Skills, Hooks, プラグイン集
- [claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery) - Hooksの実践例
- [claude-code-showcase](https://github.com/ChrisWiles/claude-code-showcase) - 設定例

### 参考記事
- [Claude Code Best Practices (Anthropic)](https://www.anthropic.com/engineering/claude-code-best-practices)
- [How Claude Code's Creator Uses It](https://medium.com/@rub1cc/how-claude-codes-creator-uses-it-10-best-practices-from-the-team-e43be312836f)
- [Claude Code Complete Guide](https://www.siddharthbharath.com/claude-code-the-complete-guide/)
- [Top 10 MCP Servers for Claude Code](https://apidog.com/blog/top-10-mcp-servers-for-claude-code/)

### 日本語参考記事
- [Claude Codeの全てのCHANGELOGを追ってきて](https://zenn.dev/oikon/articles/claude-code-2025) — 2025年の全CHANGELOGの時系列まとめ
- [Claude Codeベストプラクティス2026](https://qiita.com/dai_chi/items/63b15050cc1280c45f86) — Skills/MCP/Hooksの統合活用パターン

---

## 次回の学習再開方法

このファイルを開いて、上部の進捗チェックリストを確認し、次のフェーズから開始してください。

```bash
# 学習を再開する際のコマンド
claude

# 最初のプロンプト例
"学習を再開しす"
```
