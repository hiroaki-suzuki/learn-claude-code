#!/usr/bin/env bash
# Stopフック: 応答終了時にプロジェクトルートに戻る
#
# このフックは、作業中にディレクトリを移動した場合でも、
# 応答終了時に必ずプロジェクトルートに戻ることを保証します。
#
# 仕組み:
# - フックはサブプロセスで実行されるため、直接cdできない
# - ディレクトリが異なる場合、decision: "block"を返す
# - reasonでClaudeに`cd`コマンドを実行させる

set -euo pipefail

# 標準入力からJSON入力を読み込み
INPUT=$(cat)

# 無限ループを防ぐ: stop_hook_activeがtrueの場合は何もしない
STOP_HOOK_ACTIVE=$(echo "$INPUT" | jq -r '.stop_hook_active // false')
if [[ "${STOP_HOOK_ACTIVE}" == "true" ]]; then
  exit 0
fi

# 現在のディレクトリを取得
CURRENT_DIR=$(echo "$INPUT" | jq -r '.cwd')

# プロジェクトルートと異なる場合、Claudeにcdコマンドを実行させる
if [[ "${CURRENT_DIR}" != "${CLAUDE_PROJECT_DIR}" ]]; then
  # 構造化JSON出力で応答をブロックし、Claudeにディレクトリ移動を指示
  cat << EOF
{
  "decision": "block",
  "reason": "作業ディレクトリをプロジェクトルートに戻してください。次のコマンドを実行してください: cd \\"${CLAUDE_PROJECT_DIR}\\""
}
EOF
  exit 0
fi

# 既にプロジェクトルートにいる場合は何もしない
exit 0
