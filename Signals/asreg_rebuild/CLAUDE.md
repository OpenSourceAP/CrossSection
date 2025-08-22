# asreg_rebuild project

Goal of this project is to build a Python version of the asreg command in Stata.

The steps are:
    1. Make a Python function `regress`  that replicates Stata's `regress` command for datasets with collinearity.
        - This function should replicate MWE 1 through 3.
    2. Make a Python function `asreg` that replicates Stata's `asreg` command for datasets with collinearity.
        - This function should use the Python `regress` function.
        - This function should replicate MWE 4.
    3. Optimize these functions for speed


Minimal Working Examples:
    - Found in `mwe/tf_mwe*`
    - Each example has 
        - A `.log` file produced by Stata
        - A `.csv` file used as input

These examples were created by `mwe/debug_trendfactor.do`

Virtual environment:
    - `source ../pyCode/.venv/bin/activate`

Programming philosophy:
    - Be minimalistic.
    - Don't worry about trailing whitespace linting errors.