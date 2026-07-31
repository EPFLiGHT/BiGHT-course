# bight-course

## How to run this website

0. Make a new virtual environment for this project, and activate it.
  
1. Install the dependencies with `python3 -m pip install -r requirements.txt`.

2. Run the command `streamlit run Home.py`.

### To make sure your code is pretty, this repo has a `pre-commit` configuration file that runs linters (`isort`, `black`)

1. Install pre-commit if you haven't already

`pip install pre-commit`

2. Set up the git hook scripts

`pre-commit install`

3. Run the checks manually (optional but good before first commit)

`pre-commit run --all-files`

We also use `pyright` to type-check the code base, please make sure your Pull Requests are type-checked.
