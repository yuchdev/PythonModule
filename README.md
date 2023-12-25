# Python Module Template

## Description

This is a template for a Python module. It is intended to be used as a starting point for creating a new module.

## Template Initialisation

The script `init_template.py` can be used to initialise the template. 
It will accept for the name of the module and then rename the template files to match the module name.
The list of files and lines to be changed:

* Replace module name in `setup.cfg`
* Replace description in `setup.py`
* Replace entire content name in `README.md`
* Replace copyright in `LICENSE`
* Git move `src/python_module` to `src/new_module_name`
* Git move `test/python_module_test.py` to `test/new_module_name_test.py`
* In renamed file `test/new_module_name_test.py` rename `class PythonModuleTest(unittest.TestCase)`

Example usage:

```bash
python init_template.py new_module_name --module-description "New module description" --author-name "Author Name" --author-email "author.email@domain.com"
```

## Release Package

The script `release_package.py` can be used to create the release pipeline of any complexity for the module.
It includes the following steps:

* Build, install, reinstall, uninstall and install in developer mode
* Upload release to PyPI
* Upload release to AWS S3
* Create git tag for release
* Publish release on GitHub
* Create Release Notes
* Increment version number in `setup.cfg`

Example usage:

```bash
python release_package.py --mode install --upload-s3 --publish-pypi --create-release --increment-version
``` 
