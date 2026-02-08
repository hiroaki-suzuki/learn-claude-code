# Claude Code 既知の不具合と注意事項

> 最終更新: 2026-02-08
>
> このドキュメントでは、Claude Codeのメモリシステム（CLAUDE.md、.claude/rules/）に関連する既知の不具合と回避策をまとめています。

## 概要

フェーズ1で扱うCLAUDE.mdとrulesシステムには、2026年2月時点で複数の既知の不具合があります。これらを理解した上で学習を進めてください。

---

## 1. パスベースのルールがWrite操作で適用されない（重大）

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

---

## 2. CLAUDE.mdのルールが無視される

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

---

## 3. `.claudeignore`が機能しない（セキュリティ問題）

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

---

## 4. 設定の構文と挙動の問題

**問題:** 設定ファイルの構文や挙動に複数の問題がある。

### 4.1 絶対パスの構文
- Linux/macOSでは`/`で始まるはずだが、Claude Codeでは`//`が必要
- 例: `//home/user/project`（`/home/user/project`ではない）

### 4.2 `@`ファイル参照構文
- settings.jsonでの`@import`構文に問題報告あり

### 4.3 `permissions.deny`の制限
- ファイルをメモリにロードすることは防げない可能性
- ツール実行のみブロック

**対処法:**
- 絶対パスは`//`で始める
- `@import`構文は慎重にテストする
- permissions.denyは「実行防止」と理解し、「読み込み防止」には別の手段を使う

---

## 5. 品質劣化（2026年1月下旬以降）

**問題:** 2026年1月26日以降、Claude Codeの応答品質が低下した報告あり。

- **GitHubイシュー:** [#21431](https://github.com/anthropics/claude-code/issues/21431)
- **現象:**
  - 問題を深く考えずに複数の壊れた試行を繰り返す
  - 思考プロセスが浅くなった

**対処法:**
- より明確で詳細な指示を与える
- 段階的なアプローチを指示する
- 計画モード（`--permission-mode plan`）を活用

---

## 6. DevContainer環境でのStop hook制約

**問題:** DevContainerとClaude Codeの組み合わせでは、Stop hookによる完了通知が動作しない。

- **検証日:** 2026-02-08
- **影響:** タスク完了時のターミナル通知（ベル音、視覚的メッセージ）が表示されない
- **現象:**
  - Stop hookでターミナルベル音（`\a`）を鳴らそうとしても無音
  - 視覚的な通知メッセージも表示されない
  - `printf '\a'`を直接実行しても同様に動作しない

**原因推測:**
- DevContainer（Linuxコンテナ）環境での音声/出力の制約
- ホストOSとコンテナ間の音声デバイスの未接続

**検証内容:**
```bash
# 試したが動作しなかった
printf '\a'  # ベル音なし
echo -e "\a" >&2  # ベル音なし
```

**対処法:**
- DevContainer環境では、Stop hookによる完了通知は使用しない
- macOSネイティブ環境やLinux環境で再検証する
- 代替として、他のhooks（PostToolUse、PreToolUse）は正常動作する

**動作する環境:**
- macOSネイティブ環境（`osascript`を使った通知が可能）
- Linux GUI環境（`notify-send`等が使用可能）

---

## 実践課題への影響

これらの不具合を踏まえ、フェーズ1の実践課題では：

### 1. CLAUDE.md最適化時
- ルールが無視される前提で、重要なルールは短く明確に記述
- フック併用を検討

### 2. `.claude/rules/`作成時
- path-basedルールはWrite操作で機能しないことを認識
- ファイル作成規約はCLAUDE.mdにも記載するか、PostToolUseフックで対処

### 3. `.claudeignore`の使用
- セキュリティ上重要なファイルは、ignoreに頼らず物理的に分離
- `.env`などはプロジェクト外で管理

### 4. 検証時の注意
- ルールが適用されない場合、不具合の可能性を考慮
- ワークアラウンドの実装を学習の一環とする

---

## 関連リソース

- [Claude Code GitHub Issues](https://github.com/anthropics/claude-code/issues)
- [Zenn: Claude Codeの「すぐルール忘れる問題」をHooksで解決する](https://zenn.dev/kazuph/articles/483d6cf5f3798c)
- [The Register: Claude Code secrets files issue](https://www.theregister.com/2026/01/28/claude_code_ai_secrets_files/)
