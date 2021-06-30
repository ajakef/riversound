### Organization:
See the "gemlog" repository as an example of a mature, portable python package.

- The riversound folder will contain several .py files that collectively define all the user functions. Each .py file is a module within the riversound package. Each module defines multiple functions that are related to each other and can be used mostly independently of the other modules. Once functions become mature and stable, documentation will be added as "docstrings" at the top of the function; this is currently a low priority because the code is not mature and we have no users.

- The "old" folder contains non-functional code available as a reference (e.g., to translate).

- The "tests" folder contains automated tests for the functions in "riversound".

- The "data" folder includes data to be used in automated tests or in examples provided for users.

- "LICENSE" is just legalese to make this open-source, no software code inside.

- Eventually, a "setup.py" file will be placed in the main folder to make the package installable.

