# How to use
1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
2. Clone this repo
3. Run `uv sync` <!--- todo: make this pypi installable -->
4. Create `./ids.txt` file (or any file, but/and then you have to provide `-f path` argument)
    - a list of newline-separated discord IDs (or profile IDs) of the profiles you wish to fetch.
5. Run `zoo`/`zoo.exe`
    - (on windows) `.\.venv\Scripts\zoo.exe` (or `zooo.exe`)
    - (on linux) `./.venv/bin/zoo` (or `zooo`)

*Run `zoo --help` for more detailed help*



# How to contribute
1. This project uses the [uv](https://docs.astral.sh/uv/getting-started/installation/), install it.
2. Run `uv sync --all-extras`
3. Run `.venv/bin/pre-commit install`
4. Use github pull requests feature (make an issue if it's a large change, or one that might be controversial)
	- I'm not making any guarantees your code will be merged, but all PRs and issues (except fully AI generated ones) are welcome.


# AI Policy
- Using simple AI autocomplete is ok
- Asking an AI assistant to help, debug, write some simple tedious function is fine
- **Generating large patches of code, or fully generating code is __not allowed__**
- You should disclose usage of AI more significant than simple autocomplete (you may do this as a non-missable comment in PR description)
