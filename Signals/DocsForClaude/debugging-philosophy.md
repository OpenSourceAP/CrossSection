# Critical Debugging Philosophy

## **Traditional Debugging Approaches are Inefficient**
When predictor validation fails with "Python missing X Stata observations", the issue could be anywhere in the data pipeline:
- Input data differences
- Merge logic errors  
- Calculation problems
- Save/filtering issues

Traditional debugging approaches (reading logs, checking data) are inefficient for complex pipelines.

## **Focus on Specific Problematic Observations and Find the Exact Line**
- **❌ WRONG**: Debug by modifying code without understanding why
- **✅ RIGHT**: Pick a specific permno-yyyymm observation and trace it through every step
- **Method**: Systematically check each step of the processing pipeline to identify exactly where observations disappear.
- **Example**: permno=11545, yyyymm=199706 led to discovering the calendar lag bug

## **Understand Stata's Exact Behavior First**
- **❌ WRONG**: Assume Python pandas methods match Stata operators
- **✅ RIGHT**: Research StataDocs and trace Stata's exact processing logic
- **Method**: Check DocsForClaude/stata_*.md to understand Stata's exact behavior. Use context7 to understand the python version. 
- **Examples**: 
    - Stata's `l6.` uses calendar-based lags, not position-based `shift(6)`
    - (tbc: explain null handling)

## **Match the Stata Logic Line-by-Line**
- **❌ WRONG**: Deviate from the Stata logic in order to pass a test
- **✅ RIGHT**: Match the Stata logic line-by-line, preserving exact order

## **Never Speculate About Data Differences**
- **❌ WRONG**: "This must be due to data availability issues or historical differences"
- **✅ RIGHT**: Keep investigating the exact logic causing specific observations to fail
- **Lesson**: In the past, predictors had **logic bugs**, not data availability issues
- **Example**: EP's "missing" observations actually existed with valid data—the bug was position vs calendar lag logic




