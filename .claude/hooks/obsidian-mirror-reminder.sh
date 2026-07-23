#!/bin/bash
input=$(cat)
if echo "$input" | grep -q "チャット終了"; then
  cat <<'EOF'
{"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":"ユーザーが「チャット終了」の合図を出しました。このセッションできぼうオンライン(kibou-online)プロジェクトの自動メモリー（~/.claude/projects/.../memory/）を新規保存・更新した場合は、プロジェクトCLAUDE.mdの取り決めに従い、同じ内容をObsidianの『業務/きぼうオンライン (1)/』フォルダにも必ずミラーしてください（該当する更新がなければスキップしてよい）。ミラーした場合は何を書いたか一言だけユーザーに伝えてください。"}}
EOF
fi