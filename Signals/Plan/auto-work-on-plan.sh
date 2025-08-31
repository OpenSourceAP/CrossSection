#! /bin/zsh

# - `claude --model claude-opus-4-20250514`    
# - `claude --model claude-opus-4-1-20250805`    
# - `claude --model claude-sonnet-4-20250514`    
# - `claude --model claude-3-7-sonnet-20250219`

# Usage: ./auto-work-on-plan.sh 5
# (where 5 is the number of iterations)


alias claude="/Users/chen1678/.claude/local/claude"

cd ..

# Take the first argument, default to 1 if not provided
NUM_ITERS=${1:-1}

for i in {1..$NUM_ITERS}
do
  echo "working on iteration $i"  

  claude -p --model claude-sonnet-4-20250514 "
  Work on Plan/plan-fastxtile-removal.md. Continue where we left off previously. Work on only one script. 
  "
done

/usr/bin/osascript -e 'tell application "Messages" to send "auto-work-on-plan.sh done" to buddy "+12404465313"'