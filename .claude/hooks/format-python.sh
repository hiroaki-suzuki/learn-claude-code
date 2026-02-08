#!/bin/bash
# Pythonファイルを自動フォーマットするPostToolUseフック

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path')

# Pythonファイルのみフォーマット
if [[ "$FILE_PATH" == *.py ]]; then
  cd "$CLAUDE_PROJECT_DIR/app"
  uv run ruff format --quiet "$FILE_PATH"
fi

exit 0
