PACKAGE_NAME
=====

# Creating a package
Fork this repo.
Next up make sure there are 2 remote repositories connected.
In vscode:
- ctrl + shift + P
- Git: Add remote
- `origin_basic_function_package`
- `https://cytosmart.visualstudio.com/CytoSmartImageAnalysis/_git/basic_function_package`

Next steps are only if you need to connect it to an existing repo.
- Open terminal (ctrl + shift + `)
- git pull origin_basic_function_package master --allow-unrelated-histories

You now can `git > pull from..` and choose to pull from `origin` or `origin_basic_function_package`.
By choosing `origin_basic_function_package` you will update your package.

# Rename variables
- Search for 'PACKAGE_NAME' and replace it with the package name of your choosing.
- - Don't forget to change the folder name too!
- Search for 'AUTHOR_NAME' and replace it with your name. 
- Search for 'SMALL_DESCRIPTION' and replace it with a small description of what the package does

# Adding code to the package

The __init__.py will be used to navigate easily through functions.
You can also add a function of collection.

You import the whole function in PACKAGE_NAME.__init__.py.
Every function has its own folder.
Within this folder is a:
- `main.py` for the function itself.
- `__init__.py` for importing the code 
- `test_FUNCTION_NAME.py` for the unit tests

Example **function**:

```
# PACKAGE_NAME folder
- __init__.py
-- from .FUNCTION_NAME import FUNCTION_NAME
- FUNCTION_NAME (folder)
-- __init__.py
--- from .main import FUNCTION_NAME
-- main.py
--- def FUNCTION_NAME(...):
-- test_FUNCTION_NAME.py
--- class test_FUNCTION_NAME(TestCase)
```
This will import all function on COLLECTION_NAME to PACKAGE_NAME.
Using PACKAGE_NAME will now look like this
```
# Using of PACKAGE_NAME
from PACKAGE_NAME import FUNCTION_NAME
```

Example **collection**:
```
# PACKAGE_NAME folder
- __init__.py
-- from .FUNCTION_NAME import FUNCTION_NAME
- FUNCTION_NAME (folder)
-- __init__.py
--- from .main import FUNCTION_NAME
-- main.py
--- def FUNCTION_NAME(...):
-- test_FUNCTION_NAME.py
--- class test_FUNCTION_NAME(TestCase)
```

This will import all function on COLLECTION_NAME to PACKAGE_NAME.
Using PACKAGE_NAME will now look like this
```
# Using of PACKAGE_NAME
from PACKAGE_NAME.COLLECTION_NAME import FUNCTION_NAME
```

# testing the build of your package
To test if you function build correctly open your terminal.
- Go to the root folder of your package (where setup.py is located)
- run 'python setup.py sdist'

You will now get a /dist/PACKAGE_NAME-0.0.1.tar.gz
- copy its location
- create a new empty python environment (e.q. conda create -n NAMENEWENV python=3.7)
- Go in this new env (e.q. conda activate NAMENEWENV)
- Install your package (pip install [pathToPackage]/dist/PACKAGE_NAME-0.0.1.tar.gz)
- Try importing function from your package
- - python
- - from PACKAGE_NAME import PACKAGE_NAME
- - PACKAGE_NAME.calculate
- - should return <function PACKAGE_NAME.calculate at [pointer]>
- - expands these test to make sure it works
- Possible errors:
- - missing package [depPackage]
- - - add [depPackage] to setup.py -> requirements
- - ImportError: cannot import name 'PACKAGE_NAME'
- - - check if __init__.py imports the function

# testing your code
You should have writing some unit test well creating your functions.
In order to run them you can use pytest in the terminal or with the vscode extension.

# setup build pipeline
The file 'azure-pipelines.yml' contains the full pipeline.
- To activate it go to devops (cytosmart.visualstudio.com)
- goto Pipelines -> builds -> new -> new build pipeline
- Select your repo
- Done
- possible errors
- - pytest 1 error code '5'
- - - This happens if you have zero unit tests
  
# Last step
Delete all instruction from `creating a package` till here.

# Usage


SMALL_DESCRIPTION

# Install
To install this package follow the these steps:

    1. Create/Edit your pip configuration file:
            a. Windows users: %APPDATA%\pip\pip.ini
            b. MacOS users: $HOME/Library/Application Support/pip/pip.conf 
                if directory $HOME/Library/Application Support/pip exists 
                else $HOME/.config/pip/pip.conf
            c. Linux users: $HOME/.config/pip/pip.conf
    
    2. Press 'Connect to feed' button on the chosen package feed of ImageAnalysis

    3. Press 'Generate Python credentials' and copy contents to pip conf file

    4. Save conf file

    5. Set env variable to config file:
            a. Windows users: PIP_CONFIG_FILE
            b. MacOS users: XDG_CONFIG_HOME

    6. Run pip install <package name==version>

    7. Code with happiness.

    

# Features

* 

# Credits

- AUTHOR_NAME
