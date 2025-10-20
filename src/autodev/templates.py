# File templates for AutoDev CLI

README_TEMPLATE = """
# {project_name}

A new project created with AutoDev CLI.
"""

GITIGNORE_TEMPLATE = """
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
.Python
env/
venv/
.venv/
pip-log.txt
pip-delete-this-directory.txt

# IDEs
.vscode/
.idea/
"""

REQUIREMENTS_TEMPLATE = """
# Add your project dependencies here
"""

MAIN_PY_TEMPLATE = """
def main():
    print("Hello from {project_name}!")

if __name__ == "__main__":
    main()
"""

TEST_INIT_TEMPLATE = """
# Package initialization for tests
"""

TEST_MAIN_TEMPLATE = """
# Write your tests here
def test_example():
    assert True
"""

MIT_LICENSE_TEMPLATE = """
MIT License

Copyright (c) {year} [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""