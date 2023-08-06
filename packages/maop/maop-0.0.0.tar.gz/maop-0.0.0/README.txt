 maop- MAth OPerations is a simple python package that takes to numbers and either add, subtracts, multiply or divide them.

 USAGE:

 to install:

 pip install maop

 to add:

 import maop


 maop.add(4, 5) - takes two numbers and adds them, same goes for other operations.


 NOTE- PLEASE READ THIS:

 In this package, there are two types of divisions: divide1 and divide2

 divide1 takes two numbers and returns the EXACT answer of the division.
 example:
 import maop

 maop.divide1(4, 5)

 output: 0.8 - this is the exact answer to 4 divided by 5

divide2 takes two numbers and DOES NOT return the EXACT answer, instead it returns either the integer or a float numbers
example:
import maop

maop.divide2(4, 5)

output: 0- this is ONLY THE integer taken from the EXACT answer from 4 divided by 5.

Thanks
