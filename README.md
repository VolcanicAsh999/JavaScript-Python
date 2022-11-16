# JavaScript-Python
A program that can convert (some) JavaScript code into Python code.

Usage:

import JavaScript

JavaScript.run_code(code: str, debug: bool = False)

JavaScript.run_js_file(filename: str, *extensions: tuple[str], debug: bool=False)

JavaScript.convert_js_file(filename: str, *extensions: tuple[str], debug: bool = False)

JavaScript.save_js_file_as_python_file(filename: str, *extensions: tuple[str], debug: bool = False)

JavaScript.print_code(code: str, debug: bool = False)

JavaScript.print_js_file(filename: str, *extensions: tuple[str], debug: bool = False)
