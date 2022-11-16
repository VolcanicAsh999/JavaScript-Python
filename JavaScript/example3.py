'''
This file was created using JavaScript 0.1.0.
'''
from JavaScript.jsutils import console, NumericType, StringType
def doSomeThing(num):
	console.log(num)
	console.log(num + NumericType(3))
	console.log(StringType("Hello!"))
	i = NumericType(0)
	console.log(i + NumericType(5))


doSomeThing(NumericType(5))

