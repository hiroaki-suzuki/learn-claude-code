#!/bin/bash
# 危険なコマンドをブロックするPreToolUseフック

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')

# ブロックする危険なコマンドパターン
DANGEROUS_PATTERNS=(
  'rm -rf'              # 再帰的な強制削除
  'git push --force'    # 強制プッシュ
  'git push -f'         # 強制プッシュ（短縮形）
)

# 配列を正規表現パターン（|区切り）に変換
PATTERN=$(IFS='|'; echo "${DANGEROUS_PATTERNS[*]}")

if echo "$COMMAND" | grep -qE "$PATTERN"; then
  # JSON構造化レスポンスでブロック
  jq -n --arg cmd "$COMMAND" '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: ("危険なコマンドがブロックされました: " + $cmd)
    }
  }'
else
  exit 0
fi
