#!/usr/bin/env bash
# Pythonファイルを自動フォーマットするPostToolUseフック

set -euo pipefail

INPUT=$(cat)
FILE_PATH=$(echo "${INPUT}" | jq -r '.tool_input.file_path')

# Pythonファイルのみフォーマット
if [[ "${FILE_PATH}" == *.py ]]; then
  cd "${CLAUDE_PROJECT_DIR}/app" || exit 1
  uv run ruff format --quiet "${FILE_PATH}"
fi

exit 0
