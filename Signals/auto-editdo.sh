#! /bin/zsh

# - `claude --model claude-opus-4-20250514`    
# - `claude --model claude-opus-4-1-20250805`    
# - `claude --model claude-sonnet-4-20250514`    
# - `claude --model claude-3-7-sonnet-20250219`


alias claude="/Users/Idrees/.nvm/versions/node/v18.20.8/bin/claude"

cd ..

for i in {1..5}
  claude -p --model claude-sonnet-4-20250514 "
  Work on Plan/0819n1-placebos-plan.md. Refer to CLAUDE.md for instructions. 
  If the stata .do file column is empty, populate it based on Code/Placebos/.
  "
done

/usr/bin/osascript -e 'tell application "Messages" to send "auto-editdo.sh done" to buddy "+16303926661"'