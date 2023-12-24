import argparse
import fileinput
import subprocess
from datetime import date
from tkinter.tix import _dummyExFileSelectBox

DEFAULT_AUTHOR = "Yurii Cherkasov"
DEFAULT_EMAIL = "strategarius@protonmail.com"


def replace_in_file(file_path, old_text, new_text):
    """
    Replace single line in file
    """
    with fileinput.FileInput(file_path, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace(old_text, new_text), end='')


def replace_content_file(file_path, new_content):
    """
    Replace entire file with new content
    """
    with open(file_path, 'w') as file:
        file.write(new_content)


def replace_template_name(template_name, new_module_name, new_description, author):
    """
    Replace template name with new module name in all files
    """
    # Replace in setup.cfg
    replace_in_file('setup.cfg', f'name = {template_name}', f'name = {new_module_name}')

    # Replace in README.md
    replace_content_file('README.md', '# Python Module Repo\n\n')

    # Replace copyright in LICENSE
    current_year = date.today().year
    replace_in_file('LICENSE', f'Copyright (c) 20xx {author}', f'Copyright (c) {current_year} {author}')

    # Replace in setup.py description
    replace_in_file('setup.py', 'description="",', f'description="{new_description}",')

    # Git move src/python_module to src/new_module_name
    subprocess.run(['git', 'mv', f'src/{template_name}', f'src/{new_module_name}'])

    # Git move test/python_module_test.py to test/new_module_name_test.py
    subprocess.run(['git', 'mv', f'test/{template_name}_test.py', f'test/{new_module_name}_test.py'])

    # In renamed file test/new_module_name_test.py
    replace_in_file(f'test/{new_module_name}_test.py', 'class PythonModuleTest(unittest.TestCase):',
                    f'class {capitalize_name(new_module_name)}Test(unittest.TestCase):')


def capitalize_name(name):
    # Capitalize each word in the name
    return '_'.join(word.capitalize() for word in name.split('_'))


def main():
    """
    :return: system exit code
    """
    parser = argparse.ArgumentParser(description='Update GitHub Python module template')
    parser.add_argument('new_module_name', help='New name for the Python module (with underscores)')
    parser.add_argument('--description', help='New description for the Python module', default='')
    parser.add_argument('--author', help='New author name', default=DEFAULT_AUTHOR)
    parser.add_argument('--email', help='New author email', default=DEFAULT_EMAIL)
    args = parser.parse_args()

    template_name = 'python_module'

    # Replace with the actual template name
    replace_template_name(template_name=template_name,
                          new_module_name=args.new_module_name,
                          new_description=args.description,
                          author=args.author)

    # Git commit
    subprocess.run(['git', 'commit', '--all', '--message',
                    f'Initialize template with name {args.new_module_name} and description "{args.description}"'])
    return 0


if __name__ == '__main__':
    main()
