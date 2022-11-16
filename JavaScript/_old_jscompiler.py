from utils import strlist
_builtin_SyntaxError = SyntaxError
from JavaScript.jsutils import SyntaxError

__all__ = ['compile_code']

stacks = {'{': 0, '(': 0, '[': 0}
dicts = 0

def _latest_index(obj, item):
    if len(item) == 1:
        l = 0
        for j, i in enumerate(obj):
            if i == item:
                l = j
        return l
    else:
        i = obj.index(item)
        if item in obj[i + len(item) + 1:]:
            return _latest_index(obj[i + len(item) + 1:], item) + len(item) + 1
        else:
            return i

def _q(l):
    l = l.replace('"', "StringType($", 1).replace('"', '$)', 1)
    if l.count('"') > 0:
        #l = l[:latest_index(l, 'StringType(')] + q(l[latest_index(l, 'StringType('):]) FAIL (RecursionError)
        lat = _latest_index(l, '$)') + 2
        #l[lat:] = q(l[lat:]) FAIL (TypeError)
        l = l[:lat] + _q(l[lat:])
    return l.replace('$', '"')

def conv_to_python_phase_4(code):
    SEARCHING_DICT = False
    STR_COUNT = 0
    for index, line in enumerate(code):
        lline = line
        if "{" in line and "def" not in line:
            line = line.replace("{", "DictType({")
            SEARCHING_DICT = True
        if SEARCHING_DICT:
            line = line.replace(':', '=')
        if "}" in line and SEARCHING_DICT:
            line = line.replace("}", "})")
            SEARCHING_DICT = False
        if "[" in line: line = line.replace("[", "ArrayType([")
        if "]" in line: line = line.replace("]", "])")
        if '"' in line or "'" in line:
            """if STR_COUNT % 2 == 0:
                ind = line.index('"')
                if line[ind - 1] != 'f':
                    line = line.replace("'", 'StringType("').replace('"', 'StringType("')
                else:
                    line = line[:ind - 2] + 'StringType(f' + line[index:]
            else:
                line = line.replace('"', '")').replace('"', '")')
            STR_COUNT += 1""" # FAIL
            line = _q(line)
        if line != lline: code[index] = line
    for index, line in enumerate(code):
        isFirst = True
        isEnd = False
        lline = line
        for index2, char in enumerate(line):
            if char in '1234567890.':
                if isEnd:
                    isEnd = False
                    isFirst = True
                if isFirst:
                    isFirst = False
                    line = line[:index2 - 1] + 'NumericType(' + char + line[index2:]
                    print('start found')
            else:
                if index2 + 1 >= len(line):
                    continue
                if line[index2 + 1] in '123567890.':
                    line = line[:index2] + char + ')' + line[index2 + 1:]
                    isEnd = True
                    print('end found')
                else:
                    isEnd = True
        for index2, char in enumerate(line):
            if char in '1234567890.':
                if index2 == len(line) - 1:
                    line = line[:index2 - 1] + char + ')'
                    print('end found v2')
                else:
                    if line[index2 + 1] not in '1234567890.':
                        line = line[:index2] + char + ')' + line[index2 + 1:]
                        print('end found v3')
            """else:
                if index2 + 1 >= len(line): continue
                if line[index2 + 1] in '1234567890.':
                    line = line[:index2 + 1] + ')' + line[index2 + 2:]
                    print('end found v3')"""
        if line != lline: code[index] = line
    return code

def conv_to_python_phase_5(code):
    import_from_js = []
    import_from_js_lib = []
    for line in code:
        if ('console.log(' in line or 'console.error(' in line) and 'console' not in import_from_js:
            import_from_js.append('console')
        if 'throw' in line and 'throw' not in import_from_js:
            import_from_js.append('throw')
        if 'NumericType' in line and 'NumericType' not in import_from_js:
            import_from_js.append('NumericType')
        if 'StringType' in line and 'StringType' not in import_from_js:
            import_from_js.append('StringType')
        if 'DictType' in line and 'DictType' not in import_from_js:
            import_from_js.append('DictType')
        if 'ArrayType' in line and 'ArrayType' not in import_from_js:
            import_from_js.append('ArrayType')
        if 'BooleanType' in line and 'BooleanType' not in import_from_js:
            import_from_js.append('BooleanType')
        if 'NoneType' in line and 'NoneType' not in import_from_js:
            import_from_js.append('NoneType')
        if 'isNaN' in line and 'isNaN' not in import_from_js:
            import_from_js.append('isNaN')
        if 'setDelay' in line and 'setDelay' not in import_from_js:
            import_from_js.append('setDelay')
        if 'setTimeout' in line and 'setTimeout' not in import_from_js:
            import_from_js.append('setTimeout')
        if 'SyntaxError' in line and 'SyntaxError' not in import_from_js:
            import_from_js.append('SyntaxError')
        if 'RuntimeError' in line and 'RuntimeError' not in import_from_js:
            import_from_js.append('RuntimeError')
        if 'RangeError' in line and 'RangeError' not in import_from_js:
            import_from_js.append('RangeError')
        if 'EvalError' in line and 'EvalError' not in import_from_js:
            import_from_js.append('EvalError')
        if 'URLError' in line and 'URLError' not in import_from_js:
            import_from_js.append('URLError')
        if 'TypeError' in line and 'TypeError' not in import_from_js:
            import_from_js.append('TypeError')
        if 'ReferenceError' in line and 'ReferenceError' not in import_from_js:
            import_from_js.append('ReferenceError')
        if 'math' in line and 'math' not in import_from_js_lib:
            import_from_js_lib.append('math')
        if 'MathJS' in line and 'MathJS' not in import_from_js_lib:
            import_from_js_lib.append('MathJS')
        if 'RequireJS' in line and 'RequireJS' not in import_from_js_lib:
            import_from_js_lib.append('RequireJS')
        if 'Chart' in line and 'Chart' not in import_from_js_lib:
            import_from_js_lib.append('Chart')
    linedelay = 0
    if import_from_js:
        code = ['from JavaScript.jsutils import ' + ', '.join(import_from_js)] + code
        linedelay += 1
    if import_from_js_lib:
        code = ['from JavaScript.lib import ' + ', '.join(import_from_js_lib)] + code
        linedelay += 1
    if 'Chart' in import_from_js_lib:
        code = code[:linedelay] + ['\nChart.initialize()\n'] + code[linedelay:]
        linedelay += 1
    return code[:linedelay] + code[linedelay:]

def conv_to_python_phase_3(code):
    def get(index=None):
        if index:
            return code[index]
        return code[li]
    def set_(code_, index=None):
        if index:
            code[index] = code_
        else:
            code[li] = code_
    for li in range(len(code)):
        if '=' in get() and 'def ' in get():
            for i in range(len(get())):
                if get()[i:i + 4] == 'def ':
                    break
            for j in range(len(get())):
                if get()[j] == '=':
                    break
            set_('def ' + get()[:j][:-1] + get()[i + 4:])
            if 'this.' in get():
                set_(get().replace('this.', '').replace('(', '(self, ').replace('def \t', '\tdef '))
                for ji in range(li):
                    if 'def ' in get(ji) and '\tdef ' not in get(ji) and ji in range(li - 5, li):
                        set_('class ' + get(ji)[4:], index=ji)
                        break
            break
        if '\tthis.' in get():
            for ji in range(li):
                if 'def ' in get(ji) and '\tdef ' not in get(ji) and ji in range(li - 5, li):
                    set_('class ' + get(ji)[4:], index=ji)
                    break
        if '\tdef ' in get():
            set_(get().replace('(', '(self, '))
        if get().startswith('\tthis.'):
            set_(get().replace('this.', ''))
        elif '\tthis.' in get():
            set_(get().replace('this.', 'self.'))
    return code

def conv_to_python_phase_2(obj):
    global dicts
    obj = strlist.delitems(obj, ['var ', 'let ', 'const ', 'new '])
    obj = obj.replace('){', ') {').replace('===', '==').replace('!==', '!=').replace("'", '"')
    obj = obj.replace(') {', 'onyua').replace('={', 'dja').replace('= {', 'dja').replace('{', 'onyua').replace('dja', '= {').replace('onyua', ') {')
    if obj.endswith(';'):
        obj = obj[:-1]
    if '`' in obj:
        count = 0
        for i in range(len(obj)):
            if obj[i] == '`':
                count += 1
                if count % 2 == 0:
                    obj = obj.replace('`', 'f"', 1)
        else:
            obj = obj.replace('`', '"', 1)
    if '= {' in obj or '={' in obj:
        dicts += 1
    obj = obj.replace('true', 'BooleanType(True)').replace('false', 'BooleanType(False)').replace('null', 'NoneType()')
    #if (obj.startswith('catch (') or obj.startswith('} catch (')):#(obj.replace('} catch (', 'except Exception as ') != obj) or (obj.replace('catch (', 'except Exception as ') != obj):
    if not obj.startswith('for '):
        obj = obj.replace('try {', 'try:').replace('++ ', '+= ').replace('++', '+= 1').replace('function ', 'def ').replace(') {', '):').replace('} else {', 'else:').replace('if (', 'if ').replace('while (', 'while ')
    obj == obj.replace('} catch (', 'except Exception as ').replace('catch (', 'except Exception as ').replace(') {', '):').replace('${', '{')
    if 'except Exception as ' in obj:
        obj = obj.replace('):', ':')
    if (obj.replace('} catch (', 'except Exception as ') != obj) or (obj.replace('catch (', 'except Exception as ') != obj):
        obj == obj.replace('} catch (', 'except Exception as ').replace('catch (', 'except Exception as ').replace(') {', ':')
    if obj.startswith('for '):
        if ' in ' in obj:
            range_obj = obj.replace('(', '').replace(') {', ':')
            return range_obj
        obj = strlist.delitems(obj, ['for ', '(', ') {'])
        l_obj = obj.split(';')
        range_obj = f'for '
        for i in range(len(l_obj[0])):
            if l_obj[0][i] == '=':
                var_name = l_obj[0][:i - 1], i
        for i in range(len(l_obj[1])):
            if l_obj[1][i] not in ['<', '=', '>', ' '] + list('abcdefghijklmnopqrstuvwxyz'):
                range_count = l_obj[1][i - 1:], i
                print(i)
        for i in range(len(l_obj[2])):
            if l_obj[2][i] in '+-1234567890':
                range_step = l_obj[2][i:], i
        range_step = range_step[0].replace('++ ', '').replace('++', '1')
        range_obj += f'{var_name[0]} in range(0, {range_count[0]}, {range_step}):'
        range_obj = range_obj.replace('++ ', '+= ').replace('++', '+= 1').replace(') {', '')
        return range_obj
    if '} catch (' in obj:
        obj = obj.replace('} catch (', 'except Exception as ').replace('):', ':')
    obj = obj.replace('//', '#').replace('/*', '#').replace('*/', '')
    obj = obj.replace('throw(', 'raise RuntimeError(')
    if dicts == 0:
        if obj.endswith('}') or obj.endswith('} '):
            obj = obj.replace('}', '')
    elif dicts > 0 and '}' in obj:
        dicts -= 1
    elif dicts > 0:
        pass
    return obj

def conv_to_python_phase_1(obj):
    global stacks
    for i in range(len(obj)):
        if obj[i] == '{':
            stacks['{'] += 1
        if obj[i] == '}':
            if stacks['{'] >= 1:
                stacks['{'] -= 1
            else:
                raise SyntaxError(f"Unmatched '" + '}' + "' at column {i}, line {obj[i]}")
        if obj[i] == '(':
            stacks['('] += 1
        if obj[i] == ')':
            if stacks['('] >= 1:
                stacks['('] -= 1
            else:
                raise SyntaxError(f"Unmatched ')' at column {i}, line {obj[i]}")
        if obj[i] == '[':
            stacks['['] += 1
        if obj[i] == ']':
            if stacks['['] >= 1:
                stacks['['] -= 1
            else:
                raise SyntaxError(f"Unmatched ']' at column {i}, line {obj[i]}")
    checksyntax(obj)
    if stacks['{'] >= 1:
        if ':' in obj:
            conv = ''
            for i in range(len(obj)):
                if obj[i] == ':':
                    break
                conv += obj[i]
            obj = obj.replace(conv, f"'{conv}'", 1)
    return obj

def checksyntax(obj, full=False, ind=0):
    global stacks
    if not full:
        if obj == '' or obj == ' ':
            return
        if stacks['{'] == 0 and stacks['['] == 0 and not strlist.endis(obj, [';', '{', '[', '}', ']']):
            raise SyntaxError(f'Invalid syntax in line {ind} ({obj})')
        elif stacks['{'] >= 1 and stacks['['] == 0 and not strlist.endis(obj, [';', '{', '[', ', ', '', ',', '}']):
            raise SyntaxError(f'Invalid syntax in line {ind} ({obj})')
        elif stacks['{'] == 0 and stacks['['] >= 1 and not strlist.endis(obj, [';', '{', '[', ', ', '', ',', ']']):
            raise SyntaxError(f'Invalid syntax in line {ind} ({obj})')
        elif stacks['{'] >= 1 and stacks['['] >= 1 and not strlist.endis(obj, [';', '{', '[', ', ', '', ',', ']', '}']):
            raise SyntaxError(f'Invalid syntax in line {ind} ({obj})')
    elif full:
        if (stacks['{'] != 0) or (stacks['('] != 0) or (stacks['['] != 0):
            raise SyntaxError(f'Invalid syntax in {obj}')

def compile_line(line, ind=0):
    line = conv_to_python_phase_1(line)
    checksyntax(line, ind=ind)
    line = conv_to_python_phase_2(line)
    return line

def compile_code(code):
    code = code.split('\n')
    lines = []
    for ind, line in enumerate(code):
        lines.append(compile_line(line, ind=ind))
    lines = conv_to_python_phase_3(lines)
    lines = conv_to_python_phase_4(lines)
    lines = conv_to_python_phase_5(lines)
    code = '\n'.join(lines)
    checksyntax(code, full=True)
    return code
