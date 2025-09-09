#! /bin/zsh
# Usage: ./auto-work-on-plan.sh plan-dl-streamline.md 5 "Think carefully."
# default to 1 iteration and no think instruction
#        ./auto-work-on-plan.sh plan-comment-update.md

# - `claude --model claude-opus-4-20250514`    
# - `claude --model claude-opus-4-1-20250805`    
# - `claude --model claude-sonnet-4-20250514`    
# - `claude --model claude-3-7-sonnet-20250219`

# Usage: ./auto-work-on-plan.sh 5
# (where 5 is the number of iterations)

alias claude="/Users/chen1678/.claude/local/claude"
PLAN_NAME=$1 # e.g. "plan-dl-streamline.md"
THINK_INSTRUCTION=${3:-""} # e.g. "", "Think.", "Ultrathink.'", default to ""
OUTPUT_FORMAT="stream-json" # text, stream-json

cd ..

# Take the second argument, default to 1 if not provided
NUM_ITERS=${2:-1}

for i in {1..$NUM_ITERS}
do
  echo "================================================"
  echo "working on iteration $i out of $NUM_ITERS for $PLAN_NAME"
  echo "================================================"

  claude -p "
  Work on Plan/$PLAN_NAME. Continue where we left off previously. Work on only one script. $THINK_INSTRUCTION
  "\
    --model claude-sonnet-4-20250514 \
    --permission-mode acceptEdits \
    --verbose \
    --output-format $OUTPUT_FORMAT | jq -C '.' | sed -l 's/\\n/\n/g'
done