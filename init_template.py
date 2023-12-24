import os
import shutil
import argparse
import fileinput
import re
import subprocess

def replace_in_file(file_path, old_text, new_text):
    with fileinput.FileInput(file_path, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace(old_text, new_text), end='')

def replace_template_name(template_name, new_module_name, new_description):

    # Replace in setup.cfg
    replace_in_file('setup.cfg', f'name = {template_name}', f'name = {new_module_name}')

    # Replace in README.md
    replace_in_file('README.md', '# Python Module Repo', f'# {new_module_name}')

    # Replace copyright in LICENSE
    current_year = date.today().year
    replace_in_file('LICENSE', 'Copyright (c) 20xx Yurii Cherkasov', f'Copyright (c) {current_year} Yurii Cherkasov')

    # Replace in setup.py description
    replace_in_file('setup.py', 'description="",', f'description="{new_description}",')

    # Git move src/python_module to src/new_module_name
    subprocess.run(['git', 'mv', f'src/{template_name}', f'src/{new_module_name}'])

    # Git move test/python_module_test.py to test/new_module_name_test.py
    subprocess.run(['git', 'mv', f'test/{template_name}_test.py', f'test/{new_module_name}_test.py'])

    # In renamed file test/new_module_name_test.py
    replace_in_file(f'test/{new_module_name}_test.py', 'class PythonModuleTest(unittest.TestCase):', f'class {capitalize_name(new_module_name)}Test(unittest.TestCase):')

def capitalize_name(name):
    # Capitalize each word in the name
    return '_'.join(word.capitalize() for word in name.split('_'))

def main():
    parser = argparse.ArgumentParser(description='Update GitHub Python module template')
    parser.add_argument('new_module_name', help='New name for the Python module (with underscores)')
    parser.add_argument('--description', help='New description for the Python module', default='')
    args = parser.parse_args()

    template_name = 'python_module'

    # Replace with the actual template name
    replace_template_name(template_name, args.new_module_name, args.description)

    # Git commit
    subprocess.run(['git', 'commit', '--all', '--message', f'Initialize template with name {args.new_module_name} and description "{args.description}"'])

if __name__ == '__main__':
    main()
