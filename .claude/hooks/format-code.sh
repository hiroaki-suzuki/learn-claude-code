#!/usr/bin/env bash
# Pythonとシェルスクリプトを自動フォーマットするPostToolUseフック

set -euo pipefail

INPUT=$(cat)
FILE_PATH=$(echo "${INPUT}" | jq -r '.tool_input.file_path')

# Pythonファイルのフォーマット
if [[ "${FILE_PATH}" == *.py ]]; then
  cd "${CLAUDE_PROJECT_DIR}/app" || exit 1
  uv run ruff format --quiet "${FILE_PATH}"
fi

# シェルスクリプトのフォーマット
if [[ "${FILE_PATH}" == *.sh ]]; then
  shfmt -i 2 -bn -ci -sr -w "${FILE_PATH}"
fi

exit 0
