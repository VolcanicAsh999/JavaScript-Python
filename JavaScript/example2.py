'''
This file was created using JavaScript 0.1.0.
'''
from JavaScript.jsutils import StringType, console, NumericType, ArrayType, DictType
myString = StringType("Hello World!")
myOtherString = StringType("How are you?")

myMsg = myString + myOtherString

def printMsg(msg):
    console.log(msg)


printMsg(myMsg)

num1 = NumericType(5.6)
num2 = NumericType(9.3)

num3 = num1 + num2

printMsg(num3)

myArray = ArrayType([
    NumericType(1),
    NumericType(6),
    StringType("Hello"),
])

for item in myArray:
    console.error(item)


myDict = DictType({
    "a": NumericType(1),
})
printMsg(myDict)

for i in range(0, 7, 1):
    console.log(i)


