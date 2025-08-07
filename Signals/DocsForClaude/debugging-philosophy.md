# Critical Debugging Philosophy

## 1. **Never Speculate About Data Differences**
- **❌ WRONG**: "This must be due to data availability issues or historical differences"
- **✅ RIGHT**: Keep investigating the exact logic causing specific observations to fail
- **Lesson**: In the past, predictors had **logic bugs**, not data availability issues
- **Example**: EP's "missing" observations actually existed with valid data—the bug was position vs calendar lag logic

## 2. **Focus on Specific Problematic Observations**
- **❌ WRONG**: Debug by modifying code without understanding why
- **✅ RIGHT**: Pick a specific permno-yyyymm observation and trace it through every step
- **Method**: Use bisection strategy to isolate exactly where observations are lost
- **Example**: permno=11545, yyyymm=199706 led to discovering the calendar lag bug

## 3. **Understand Stata's Exact Behavior First**
- **❌ WRONG**: Assume Python pandas methods match Stata operators
- **✅ RIGHT**: Research StataDocs and trace Stata's exact processing logic
- **Method**: Check DocsForClaude/stata_*.md to understand Stata's exact behavior. Use context7 to understand the python version. 
- **Key Discovery**: Stata's `l6.` uses calendar-based lags, not position-based `shift(6)`