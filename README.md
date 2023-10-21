# Stacklang

Stacklang is an esotheric Stack based Programming language created by Strawberry.
It is currently unkown if it is Turing complete.

It features the ability to have an Infinite amount of Stacks whilst simultanously not having any control Flow except for Function Calls.

## Execution details
Every Program consists of a list of Functions with integer IDs assigned to them by the Programmer.
If function IDs may be negative or not is implementation defined.

The Programmer has access to an Infinite amount of Stacks. With Each Stack having a rational Number as its ID.
Every value on the Stack, is a Rational Number, with every Rational Number being Representable.

When a Program start up, function 0 is called as the entry point to the Program, with Stack 0 active as the stack.

## Syntax
On the top level of a file, only a single construct exists: Functions

A Function Definition starts with the `def` keyword followed by its numeric Identifier.
Afterwards follows a list of Commands that is terminated with the `end` block

A Command is either a numeric Integer Value, or one of the Instructions in the Table below.

If a Word is neither of the above, the behavior is implementation defined.

## Instructions
| Instruction | Effect                                                                                                                                                                                           |
|-------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| +           | Pops the top two Values of the currently active Stack and pushes their sum onto the stack.                                                                                                       |
| -           | Pops the top two values of the currently active Stack and pushes their difference onto the stack with the value on top of the Stack being the minuend and the second value being the subtrahend. |                                                                          
| *           | Pops the top two Values of the currently active Stack and pushes their Product onto the stack.                                                                                                   |
| /           | Pops the top two values of the currently active Stack and pushes their Quotient onto the stack with the value on top of the Stack being the dividend and the second value being the divisor.     |                                                                          
| //          |                                                                                                                                                                                                  |
| %           |                                                                                                                                                                                                  |
| call        | Pops a Value from the currently active stack, converts it to an integer using the floor function and calls the corresponding function.                                                           |
| swap        |                                                                                                                                                                                                  |
| dup         |                                                                                                                                                                                                  |
| rot         |                                                                                                                                                                                                  |
| drop        |                                                                                                                                                                                                  |
| clear       |                                                                                                                                                                                                  |
| exit        | exits the program                                                                                                                                                                                |
| getchar     |                                                                                                                                                                                                  |
| putchar     |                                                                                                                                                                                                  |
| in          |                                                                                                                                                                                                  |
| out         |                                                                                                                                                                                                  |
| change      | Pops a value from the currently active Stacks and switches the currently active stack to the one with that ID                                                                                    |
| debug       |                                                                                                                                                                                                  |
| dump        |                                                                                                                                                                                                  |

## Examples