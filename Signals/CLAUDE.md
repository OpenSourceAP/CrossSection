# CrossSection Signals - Python Translation Project

## Project Overview
This project aims to translate Stata code in `Code/` to Python equivalents in `pyCode/`, replicating the exact data processing pipeline while outputting to Parquet/CSV format instead of DTA/CSV.

# Project Structure

There are four main legs of the project:
- Download data (`DataDownloads/`)
- Create signal master table (`SignalMasterTable`)
- Generate predictors (`Predictors/`)
- Generate placebos (`Placebos/`)

**IMPORTANT**: work on each leg in isolation. do not run validation scripts from the DownloadData leg when working on the Predictors leg.

The `pyCode/` folder contains the Python equivalents of the Stata code.
The `pyData/` folder contains the Python data files.

## Files

```
Signals/
├── Code/                    # Original Stata code
│   ├── DataDownloads/      # Stata data download scripts
│   ├── Predictors/         # Stata predictor generation
│   └── Placebos/          # Stata placebo generation
├── Data/                   # Stata data files
│   ├── Intermediate/       # Processed data from Stata (.dta/.csv)
│   ├── Prep/              # Preprocessed inputs
│   ├── Predictors/         # Stata predictor generation
│   ├── Placebos/          # Stata placebo generation
│   └── temp/              # Temporary Stata files
├── pyCode/                 # Python equivalent code (WORKING DIRECTORY)
│   ├── .venv/              # Python virtual environment
│   ├── DataDownloads/      # Python data download scripts
│   ├── Predictors/         # Python predictor generation
│   ├── Placebos/          # Python placebo generation (tbc)
│   ├── requirements.txt    # Python dependencies
│   ├── 01_DownloadData.py  # Main download orchestrator
|   ├── utils/              # Utility functions and persistent testing scripts
├── pyData/                 # Python data files
│   ├── Intermediate/       # Processed data from Python (.parquet)
│   ├── Prep/              # Preprocessed inputs
│   ├── Predictors/         # Python predictor generation
│   ├── Placebos/          # Python placebo generation
│   └── temp/              # Temporary Python files
├── Logs/                   # Processing logs
├── Journal/                # Claude's Journal
├── DocsForClaude/          # Claude's Docs
├── Plan/                   # Claude's Planning docs
├── Debug/                  # Debugging scripts
```

# Coding Environment, Tools, and Docs

## Working Directory
- **All Python scripts must be executed from `pyCode/`**
- **Virtual environment is located at `pyCode/.venv/`**
- **Data paths are relative to `pyCode/` (e.g., `../pyData/Intermediate/`)**
- Before running any python script, `source .venv/bin/activate`

## Environment Setup
```bash
# Initial setup (from pyCode/ directory)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Virtual Environment Management
- **Only one .venv folder**: Located in `pyCode/.venv/`
- **Always activate before running scripts**: `source .venv/bin/activate`
- **Install packages in venv**: `pip install package_name`

## Tools 
- Do not use long Bash commands. 
  - If a Bash command is more then 3 lines, write a py script in `Debug/` that generates test output instead.
  - This ensures that the permissions are correct and avoids unneeded user intervention.

## Docs
- `DocsForClaude/` contains long-term docs about the project
  - `stata_*.md` are docs about Stata commands
  - `leg*.md` are docs about the project legs
- `Journal/` contains messy notes about the project
  - Recent Journal/ entries may be helpful for passing tests.

# Translation Philosophy

## **Line-by-Line Translation**
- **❌ NEVER**: Add functions, abstractions, or "improvements" during translation
- **✅ ALWAYS**: Translate Stata code line-by-line, preserving exact order
- **✅ ALWAYS**: Use linear, procedural structure matching Stata
- **Lesson**: Overengineering caused 40% data loss in CompustatAnnual

## **Execution Order is Critical**
- **❌ NEVER**: Change the timing of data saves or processing steps
- **✅ ALWAYS**: Match exact execution order from Stata script
- **Example**: Stata saves CSV immediately after download, Python must do same
- **Lesson**: Wrong save timing caused major shape mismatches

## **Missing Data Handling**
- **Stata**: Missing dates often mean "infinity" or "still active" → TRUE
- **Python**: `datadate <= NaT` → FALSE  
- **✅ ALWAYS**: Use explicit null handling: `(condition) | column.isna()`
- **Lesson**: Missing data logic differences lost 19% of records

## **Simplicity Over Cleverness**  
- **❌ NEVER**: Add complex dtype handling, YAML standardization, helper functions
- **✅ ALWAYS**: Keep code simple, direct, and readable
- **Principle**: **EXACT REPLICATION BEATS CLEVER ENGINEERING**

## **Immediate Validation**
- **✅ ALWAYS**: Run test script after every translation
- **✅ ALWAYS**: Fix shape mismatches before data mismatches
- **✅ ALWAYS**: Achieve 99%+ row count match with Stata

## **Do Not Add Unrequested Features**
- **❌ NEVER**: Add command-line options, modes, or features unless explicitly requested
- **✅ ALWAYS**: Keep code simple and focused on the specific requirements
- **Principle**: **ONLY BUILD WHAT IS ASKED FOR**

## **Write Test py Scripts**
- **WRONG**: Run a long Bash command that to generate test output.
- **RIGHT**: Write a py script in `Debug/` that generates test output.

# Debugging Philosophy

## **Do Not Speculate That the Test Failed Because of Real Data Differences**
- **❌ NEVER**: Stop debugging because of "data availability issues," "historical data differences," or "real data differences"
- **✅ ALWAYS**: Keep checking the logic for what is causing the test to fail
- **✅ ALWAYS**: For missing observations, use bisection strategy (Journal/2025-07-16_AnalystRevision_bisection_debugging.md) before giving up.
- **✅ ALWAYS**: Check with the user before giving up.

## **Debug by Understanding Problematic Observations**
- **✅ ALWAYS**: Focus on a specific permno-yyyymm observation that is causing the test to fail. Understand what step of the code is causing this specific observation to be problematic.
- **❌ NEVER**: Debug my modifying code without understanding why the modification may affect a specific problematic observation.

## **Never Speculate About Data Differences**
- **❌ WRONG**: "This must be due to data availability issues or historical differences"
- **✅ RIGHT**: Keep investigating the exact logic causing specific observations to fail

## **Understand Stata's Exact Behavior First**
- **❌ WRONG**: Assume Python pandas methods match Stata operators
- **✅ RIGHT**: Research StataDocs and trace Stata's exact processing logic
- **Key Discovery**: Stata's `l6.` uses calendar-based lags, not position-based `shift(6)`

## **Never Assume Convenient Data Patterns**
- **❌ WRONG**: "The issue must be missing data because my logic expects perfect monthly coverage"
- **✅ RIGHT**: Investigate what the code actually does with irregular time series data, don't assume `1 obs = 1 month`

## **Never Make Up Data To Resolve Missing Rows**
- **❌ WRONG**: "There are missing rows in this predictor's output, so let me create placeholder data"
- **❌ WRONG**: "If I hardcode rows that match stata's output, I'll have resolved the missing rows issue."
- **✅ RIGHT**: Investigate why those rows are missing to decipher the issue in the translation.

## **Write Debugging py scripts**
- **WRONG**: Run a long bash command that to generate test output.
- **RIGHT**: Write a py script in `Debug/` that generates test output.


# Interaction 

## Our relationship

- We're coworkers. When you think of me, think of me as your colleague
- We are a team of people working together. Your success is my success, and my success is yours.
- I'm smart, but not infallible.
- You are much better read than I am. I have more experience of the physical world than you do. Our experiences are complementary and we work together to solve problems.
- Neither of us is afraid to admit when we don't know something or are in over our head.
- When we think we're right, it's _good_ to push back, but we should cite evidence.

# Writing code

- CRITICAL: NEVER USE --no-verify WHEN COMMITTING CODE
- We prefer simple, clean, maintainable solutions over clever or complex ones, even if the latter are more concise or performant. Readability and maintainability are primary concerns.
- Make the smallest reasonable changes to get to the desired outcome. You MUST ask permission before reimplementing features or systems from scratch instead of updating the existing implementation.
- When modifying code, match the style and formatting of surrounding code, even if it differs from standard style guides. Consistency within a file is more important than strict adherence to external standards.
- NEVER make code changes that aren't directly related to the task you're currently assigned. If you notice something that should be fixed but is unrelated to your current task, document it in a new issue instead of fixing it immediately.
- NEVER remove code comments unless you can prove that they are actively false. Comments are important documentation and should be preserved even if they seem redundant or unnecessary to you.
- All code files should start with a brief 2 line comment explaining what the file does. Each line of the comment should start with the string "ABOUTME: " to make it easy to grep for.
- After ABOUTME, describe the file in more detail
  - How do run the script, including examples with arguments
  - Inputs
  - Outputs
- When writing comments, avoid referring to temporal context about refactors or recent changes. Comments should be evergreen and describe the code as it is, not how it evolved or was recently changed.
- NEVER implement a mock mode for testing or for any purpose. We always use real data and real APIs, never mock implementations.
- When you are trying to fix a bug or compilation error or any other issue, YOU MUST NEVER throw away the old implementation and rewrite without expliict permission from the user. If you are going to do this, YOU MUST STOP and get explicit permission from the user.
- NEVER name things as 'improved' or 'new' or 'enhanced', etc. Code naming should be evergreen. What is new today will be "old" someday.
- When creating final versions of translated code files, do NOT create multiple versions with endings like "_fixed". Keep a 1-to-1 matching between original and translated.
- When debugging, if you create code to debug, place it in ClaudeDebug/ and no where else.
- NEVER create "placeholder" data when you are struggling to debug code. If you are instructed to debug code and are having a hard time, let me know and keep trying. Creating "placeholder" data is unacceptable.

# Getting help

- ALWAYS ask for clarification rather than making assumptions.
- If you're having trouble with something, it's ok to stop and ask for help. Especially if it's something your human might be better at.

# Testing

- Tests MUST cover the functionality being implemented.
- NEVER ignore the output of the system or the tests - Logs and messages often contain CRITICAL information.
- TEST OUTPUT MUST BE PRISTINE TO PASS
- If the logs are supposed to contain errors, capture and test it.
- NO EXCEPTIONS POLICY: Under no circumstances should you mark any test type as "not applicable". Every project, regardless of size or complexity, MUST have unit tests, integration tests, AND end-to-end tests. If you believe a test type doesn't apply, you need the human to say exactly "I AUTHORIZE YOU TO SKIP WRITING TESTS THIS TIME"

## We practice TDD. That means:

- Write tests before writing the implementation code
- Only write enough code to make the failing test pass
- Refactor code continuously while ensuring tests still pass

### TDD Implementation Process

- Write a failing test that defines a desired function or improvement
- Run the test to confirm it fails as expected
- Write minimal code to make the test pass
- Run the test to confirm success
- Refactor code to improve design while keeping tests green
- Repeat the cycle for each new feature or bugfix

# Journal, Documentation, and Planning

We keep organized by making notes in md format. **IMPORTANT**: all notes filenames have the format "[MMDD]-n[id]-[title].md" (e.g. "0808-n1-asreg-plan.md")

The notes go in the following folders:
- `Journal/`
  - This is a messy folder, put whatever you want in it.
- `DocsForClaude/`
  - This folder has long-term docs about the project. It includes important lessons from `Journal/`
- `Plan/`
  - This folder contains plans for coding across Claude Code sessions. If one session gets too long, put the next steps and required context for the next Claude Code session in this folder.
  - Each md file here should be one self-contained plan.


