from __future__ import division
import sys, builtins, threading, math

__all__ = ['BooleanType', 'StringType', 'NumericType', 'ArrayType', 'DictType', 'SyntaxError', 'URLError', 'TypeError', 'ReferenceError', 'RangeError', 'EvalError', 'RuntimeError', 'isNaN', 'throw', 'console', 'setTimeout', 'setDelay']

class SyntaxError(builtins.SyntaxError):
    def __init__(self, msg, *args):
        super().__init__(msg, *args)
        self.message = msg

class URLError(builtins.UnicodeError):
    def __init__(self, msg, *args):
        super().__init__(msg, *args)
        self.message = msg

class TypeError(builtins.TypeError):
    def __init__(self, msg, *args):
        super().__init__(msg, *args)
        self.message = msg

class ReferenceError(builtins.ReferenceError):
    def __init__(self, msg, *args):
        super().__init__(msg, *args)
        self.message = msg

class RangeError(builtins.ValueError):
    def __init__(self, msg, *args):
        super().__init__(msg, *args)
        self.message = msg

class EvalError(builtins.Exception):
    def __init__(self, msg, *args):
        super().__init__(msg, *args)
        self.message = msg

class RuntimeError(builtins.RuntimeError):
    def __init__(self, msg, *args):
        super().__init__(msg, *args)
        self.message = msg

def throw(msg, type_=RuntimeError):
    raise type_(msg)

def isNaN(obj):
    return (type(obj) != int)

def setTimeout(func, timeout, *args):
    def q(*args):
        time.sleep(args[1] / 1000)
        args[0](*args[2:])
    t = threading.Thread(target=q, args=(func, timeout) + args)
    return t.start()

def setDelay(func, timeout, *args):
    def q(*args):
        time.sleep(args[1] / 1000)
        args[0](*args[2:])
        q(*args)
    t = threading.Thread(target=q, args=(func, timeout) + args)
    return t.start()

class console:
    def log(msg):
        print(msg)
        return msg

    def error(msg):
        print(msg, file=sys.stderr)
        return msg

class _Type(object):
    def __init__(self, val):
        self._ = val._ if hasattr(val, '_') else val
        self._type = type(self)

    def __str__(self):
        return str(self._)

    def __int__(self):
        return int(self._)

    def __bool__(self):
        return bool(self._)

    def __add__(self, other):
        return self._type(self._ + other._)

    def __sub__(self, other):
        return self._type(self._ - other._)

    def __mul__(self, other):
        return self._type(self._ * other._)

    def __truediv__(self, other):
        return self._type(self._ / other._)

    def __div__(self, other):
        return self._type(self._ / other._)

    def __repr__(self):
        return str(self._)

    def __del__(self):
        return

    def __eq__(self, other):
        return BooleanType(self._ == other._)

    def __ne__(self, other):
        return BooleanType(not self.__eq__(other))

    def __le__(self, other):
        return BooleanType(self._ <= other._)

    def __lt__(self, other):
        return BooleanType(self._ < other._)

    def __ge__(self, other):
        return BooleanType(not self.__lt__(other))

    def __gt__(self, other):
        return BooleanType(not self.__le__(other))

    def __abs__(self):
        return NumericType(abs(self._))

    def __round__(self, n=0):
        return NumericType(round(self._, n))

    def __floor__(self):
        return NumericType(math.floor(self._))

    def __ceil__(self):
        return NumericType(math.ceil(self._))

    def __trunc__(self):
        return NumericType(math.trunc(self._))

    def __floordiv__(self, other):
        return NumericType(self._ // other._)

    def __mod__(self, other):
        return NumericType(self._ % other._)

    def __divmod__(self, other):
        return ArrayType(list(divmod(self._, other._)))

    def __rshift__(self, other):
        return NumericType(self._ >> other._)

    def __lshift__(self, other):
        return NumericType(self._ << other._)

    def __and__(self, other):
        return NumericType(self._ & other._)

    def __or__(self, other):
        return NumericType(self._ | other._)

    def __xor__(self, other):
        return NumericType(self._ ^ other._)

    def __pow__(self, n=1):
        return NumericType(self._ ** n)

    def __iadd__(self, other):
        self._ += other._

    def __isub__(self, other):
        self._ -= other._

    def __imul__(self, other):
        self._ *= other._

    def __idiv__(self, other):
        self._ /= other._

    def __imod__(self, other):
        self._ %= other._

    def __ifloordiv__(self, other):
        self._ //= other._

    def __itruediv__(self, other):
        self._ /= other._

    def __ilshift__(self, other):
        self._ <<= other._

    def __irshift__(self, other):
        self._ >>= other._

    def __iand__(self, other):
        self._ &= other._

    def __ior__(self, other):
        self._ |= other._

    def __ixor__(self, other):
        self._ ^= other._

    def __ipow__(self, other):
        self._ **= other._

    def __float__(self):
        return NumericType(float(self._))

    def __complex__(self, imag=0):
        return NumericType(complex(self._, imag=imag))

    def __sizeof__(self):
        return NumericType(sys.getsizeof(self._))

    def __len__(self):
        return NumericType(len(self._))

    def __contains__(self, other):
        return BooleanType(other in self._)

    def __getitem__(self, item):
        return self._[item]

    def __setitem__(self, item, value):
        self._[item] = value

    def __delitem__(self, item):
        del self._[item]

class StringType(_Type):
    """String-like object."""
    @property
    def length(self):
        return NumericType(len(self._))

    def indexOf(self, segment):
        if segment._ in self._:
            length = segment.length
            for index in range(self.length):
                if self._[index] == segment._[0]:
                    if self._[index:index + length] == segment._:
                        return NumericType(index)
        return NumericType(0)

    def slice(self, start, end):
        if start._ < 0 or end._ >= self.length:
            return StringType("")
        return StringType(self._[start._:end._])

    def substr(self, start, length):
        if start._ < 0 or length._ + start._ >= self.length:
            return StringType("")
        return StringType(self._[start._:start._ + length._])

    def split(self, char):
        return StringType(self._.split(char))

    def __repr__(self):
        return f'"{self._}"'

class NumericType(_Type):
    """Number-like object."""
    def __init__(self, *val):
        super().__init__(val[0] if val else exec("""raise TypeError("__init__() missing 1 required positional argument: 'val'")"""))

class ArrayType(_Type):
    """Array-like object."""
    def push(self, item):
        self._.append(item)

    def spread(self, *items):
        if len(items) == 1:
            items = items[0]
        self._.extend(*items)

    def sort(self, sortFunction=sorted):
        return ArrayType(list(sortFunction(self._)))

    def __setitem__(self, item, value):
        try:
            self._[item] = value
        except IndexError:
            for i in range(len(self._) - 1, item):
                self._.append(NoneType())
            self._[item] = value

class DictType(_Type):
    """Dictionary-like object."""
    def __init__(self, *args, **kwargs):
        """Can be initalized two ways:
    *DictType(a=1, ...)
    *DictType({"a": 1, ...})
Both will work the same."""
        if kwargs and args:
            self._ = kwargs
        elif kwargs:
            self._ = kwargs
        elif args:
            self._ = args[0]
        else:
            self._ = {}
        self._type = DictType

    def __getattr__(self, name):
        try:
            return self._[name]
        except:
            return self.__dict__[name]

    def __setattr__(self, name, value):
        if name in ['_', '_type']:
            self.__dict__[name] = value
        else:
            self._[name] = value

    def __delattr__(self, name):
        try:
            del self._[name]
        except:
            del self.__dict__[name]

    def __repr__(self):
        text = '{\n'
        c = 0
        for key, value in self._.items():
            text += '\t' + (str(key).replace('"', '') + ': ' + str(value))
            c += 1
            if c == len(self._.values()):
                break
            text += ',\n'
        return text + '\n}'

class BooleanType(_Type):
    """Boolean-like object."""
    def __repr__(self):
        return 'true' if self._ else 'false'

    def __str__(self):
        return 'true' if self._ else 'false'

class NoneType(_Type):
    """None-like object"""
    def __init__(self):
        super().__init__(None)

    def __repr__(self):
        return 'null'

    def __str__(self):
        return 'null'
