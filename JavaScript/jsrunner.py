from JavaScript import jscompiler as js
from JavaScript import jsutils as jsu
from JavaScript.jsutils import console
from JavaScript import __version__ as _version_num
import os

__all__ = ['run_code', 'run_js_file', 'convert_js_file', 'save_js_file_as_python_file', 'print_code', 'print_js_file']

class _DeprecationError(Exception):
    """Feature is deprecated"""

def run_code(code, debug=False):
    try:
        code = js.compile_code(code, debug=debug)
        exec(code)
    except NameError as e:
        raise jsu.ReferenceError(e)
    except (ValueError, SyntaxError, TypeError) as e:
        raise e
    except jsu.SyntaxError as e:
        raise e
    except Exception:
        raise jsu.RuntimeError(e)
    return #code

def print_code(code, debug=False):
    print(js.compile_code(code, debug=debug))

def print_js_file(filename, *extensions, debug=False):
    filename = os.path.join(*extensions, filename)
    with open(filename, mode='r') as file:
        code = file.readlines()
    return print_code(''.join(code), debug=debug)

def run_js_file(filename, *extensions, debug=False):
    filename = os.path.join(*extensions, filename)
    with open(filename, mode='r') as file:
        code = file.readlines()
    return run_code(''.join(code), debug=debug)

def convert_js_file(filename, *extensions, debug=False):
    filename = os.path.join(*extensions, filename)
    with open(filename, mode='r') as file:
        code = file.readlines()
    return js.compile_code(''.join(code), debug=debug)

def save_js_file_as_python_file(filename, *extensions, debug=False):
    filename = os.path.join(*extensions, filename)
    with open(filename, mode='r') as file:
        code = file.readlines()
    filename = filename.replace('.js', '.py')
    with open(filename, mode='w') as file:
        code = js.compile_code(''.join(code), debug=debug)
        _copyright = f"""'''
This file was created using JavaScript {_version_num}.
'''
"""
        file.writelines([_copyright] + [sym + '\n' for sym in code.split('\n')])

def run_code_input():
    raise _DeprecationError('run_code_input is deprecated, do not use')
    code = ''
    while True:
        new = input('next line: ')
        if new == 'quit':
            break
        code += new + '\n'
    return run_code(code)
