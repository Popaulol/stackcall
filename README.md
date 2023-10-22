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
| Instruction | Effect                                                                                                                                                                                               |
|-------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| +           | Pops the top two Values of the currently active Stack and pushes their sum onto the stack.                                                                                                           |
| -           | Pops the top two values of the currently active Stack and pushes their difference onto the stack with the value on top of the Stack being the minuend and the second value being the subtrahend.     |                                                                          
| *           | Pops the top two Values of the currently active Stack and pushes their Product onto the stack.                                                                                                       |
| /           | Pops the top two values of the currently active Stack and pushes their Quotient onto the stack with the value on top of the Stack being the dividend and the second value being the divisor.         |                                                                          
| //          | Pops the top two values of the currently active Stack and pushes their Integer Quotient onto the stack with the value on top of the Stack being the dividend and the second value being the divisor. |
| %           | Pops the top two values of the currently active Stack and pushes their Remainder onto the stack with the value on top of the Stack being the dividend and the second value being the divisor.        |
| call        | Pops a Value from the currently active stack, converts it to an integer using the floor function and calls the corresponding function.                                                               |
| swap        | Swaps the top 2 value of the currently active stack                                                                                                                                                  |
| dup         | Duplicates the top value of the currently active Stack                                                                                                                                               |
| rot         | Rotates the top 3 values of the currently active Stack                                                                                                                                               |
| drop        | Drops the top value from the currently active Stack                                                                                                                                                  |
| clear       | Clears the currently active Stack                                                                                                                                                                    |
| exit        | exits the program                                                                                                                                                                                    |
| getchar     | gets a single character of input from the user and pushes it's ascii value on top the stack                                                                                                          |
| putchar     | Pops a single value from the currently active stack and prints out the character corresponding to the ascii value of the result of the floor function on the value.                                  |
| in          | Takes an Integer as input from the user and pushes it onto the currently active stack                                                                                                                |
| out         | Pops the top value from the currently active stack and outputs it to the user, the exact output format is implementation defined                                                                     |
| change      | Pops a value from the currently active Stacks and switches the currently active stack to the one with that ID                                                                                        |
| debug       | Pops a value from the Stack and sets the current debug mode to it, 0 is no debugging and every other mode is implementation defined                                                                  |
| dump        | Dumps an implementation defined representation of all of the Stacks to the User                                                                                                                      |
| nret        | Pops a value of the stack and returns upwards the amount of Callframes the floor function returns for the popped value.                                                                              |                                                                                                                                  |
| rerun       | Restarts execution of the current function without adding another callframe to the call stack.                                                                                                       |

## Examples
### Hello World
```
def 0
    72 putchar
    101 putchar
    108 putchar
    108 putchar
    111 putchar
    32 putchar
    87 putchar
    111 putchar
    114 putchar
    108 putchar
    100 putchar
    33 putchar
end
```

## Abbriviated 99 Bottles of Beer
Made by [Sebosh](https://github.com/sebosh)
```
def 0
      1  2  3  4  5  6  7  8  9
  10 11 12 13 14 15 16 17 18 19
  20 21 22 23 24 25 26 27 28 29
  30 31 32 33 34 35 36 37 38 39
  40 41 42 43 44 45 46 47 48 49
  50 51 52 53 54 55 56 57 58 59
  60 61 62 63 64 65 66 67 68 69
  70 71 72 73 74 75 76 77 78 79
  80 81 82 83 84 85 86 87 88 89
  90 91 92 93 94 95 96 97 98 99

  1 call
end

# main loop
def 1
  dup        # 99, 98, 97, ...,  2,  1
  100 -      #  1,  2,  3, ..., 98, 99
  99 swap // #  0,  0,  0, ...,  0,  1
  2 +        #  2,  2,  2, ...,  2,  3
  call
  1 call
end

# print lyrics for one iteration
def 2
  5  call    # _ BoBotW
  32 putchar # <space>
  4  call    # _ BoB
  32 putchar # <space>
  6  call    # T1DPiA
  32 putchar # <space>
  1  swap -
  5  call    # _-1 BoBotW
  10 putchar # \n
  drop
end

# last and exit
def 3
  5   call    # 1 BoBotW
  32  putchar # <space>
  4   call    # 1 BoB
  32  putchar # <space>
  6   call    # T1DPiA
  32  putchar # <space>
  78  putchar # N
  77  putchar # M
  66  putchar # B
  111 putchar # o
  66  putchar # B
  111 putchar # o
  116 putchar # t
  87  putchar # W
  exit
end

# _ BoB
def 4
  dup
  out         # _
  32  putchar # <space>
  66  putchar # B
  111 putchar # o
  66  putchar # B
end

# _ BoBotW
def 5
  4   call    # _ BoB
  111 putchar # o
  116 putchar # t
  87  putchar # W
end

# T1DPiA
def 6
  84  putchar # T
  49  putchar # 1
  68  putchar # D
  80  putchar # P
  105 putchar # i
  65  putchar # A
end

```

## Example Implementation
The Implementation in this repository requires Python 3.12 to run.
