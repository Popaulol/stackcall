from __future__ import annotations

import string
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import IntEnum
from fractions import Fraction
from numbers import Rational
from typing import NoReturn

type stack_value = Fraction


class DebugMode(IntEnum):
    NO_DEBUG = 0
    CALL_STEP = 1
    WORD_STEP = 2


@dataclass
class Token:
    tok: str
    line: int
    column: int


class Parser:
    file: str
    line: int
    column: int
    idx: int

    interpreter: Interpreter

    def __init__(self, file: str, interpreter: Interpreter):
        self.line = 1
        self.column = 1
        self.idx = 0
        self.file = file
        self.interpreter = interpreter
        with open(self.file, "r") as f:
            self.content = f.read()

    def get_char(self) -> str:
        if self.idx > len(self.content) - 1:
            return ""
        c = self.content[self.idx]

        self.idx += 1

        self.column += 1
        if c == "\n":
            self.line += 1
            self.column = 0

        if c == "#":
            while self.get_char() not in ["\n", ""]:
                pass
            c = " "

        return c

    def get_token(self):
        token: str | list[str] = []
        line = self.line
        column = self.column
        while True:
            c = self.get_char()
            if c == "": break
            if c in string.whitespace:
                if len(token) == 0: continue
                break
            token.append(c)

        token = "".join(token)
        return Token(token, line, column)

    def parse(self):
        self.line = 1
        self.column = 1
        self.idx = 0

        functions: dict[int, Function] = {}

        while self.idx < len(self.content):
            tok = self.get_token()

            if tok.tok == "":
                break

            if tok.tok != "def":
                self.interpreter.error(
                    "A File can only contain Function definitions on the top level",
                    tok.line,
                    tok.column,
                )

            index_token = self.get_token()
            try:
                function_index = int(index_token.tok)
            except ValueError:
                self.interpreter.error(
                    "A File can only contain Function definitions on the top level",
                    index_token.line,
                    index_token.column,
                )

            if function_index in functions.keys():
                self.interpreter.error(
                    "Every Function can only be defined once",
                    index_token.line,
                    index_token.column,
                )

            commands = []
            while (command_tok := self.get_token()).tok != "end":
                if command_tok.tok == "":
                    self.interpreter.error("Input ended Unexpectedly", self.line, self.column)
                try:
                    value = Fraction(command_tok.tok)
                    commands.append(Number(value, command_tok.line, command_tok.column))
                except ValueError:
                    commands.append(Word(command_tok.tok, command_tok.line, command_tok.column))

            functions[function_index] = Function(commands)

        return functions


class Interpreter:
    current_stack: list[stack_value]
    stacks: dict[stack_value, list[stack_value]]
    functions: dict[int, Function]
    file: str
    call_stack: list[int]
    debug_mode: DebugMode

    def __init__(
            self,
            file: str,
            debug_mode: DebugMode = DebugMode.NO_DEBUG,
    ):
        self.file = file
        self.current_stack = []
        self.stacks = {0: self.current_stack}
        self.functions = {}
        self.call_stack = []
        self.debug_mode = debug_mode

        self.parse()

    def parse(self):
        self.functions = Parser(self.file, self).parse()

    def run(self):
        self.call(0, 0, 0)

    def call(self, i: int, line: int, column: int):
        if self.debug_mode >= DebugMode.CALL_STEP:
            input(f"Function {i} was called from {self.file}:{line}:{column}")

        if 0 not in self.functions.keys():
            self.error(f"No Function {i} exists!", line, column)

        self.call_stack.append(i)
        self.functions[i].run(self)
        self.call_stack.pop()

    def error(self, message: str, line: int, column: int) -> NoReturn:
        print(f"{self.file}:{line}:{column}: {message}")

        for i in self.call_stack:
            print(f"at {i}")

        self.dump()
        breakpoint()
        exit()

    def push(self, value: stack_value):
        self.current_stack.append(value)

    def pop(self) -> stack_value:
        return self.current_stack.pop()

    def render(self) -> str:
        return "\n".join(f"{i}: {f.render()}" for i, f in self.functions.items())

    def clear(self):
        self.current_stack.clear()

    def change_stack(self, i: stack_value):
        self.current_stack = self.stacks.get(i, list())
        self.stacks[i] = self.current_stack

    def set_debug(self, mode: int):
        self.debug_mode = DebugMode(mode)

    def dump(self):
        print()
        max_stack_size = max(len(stack) for _, stack in self.stacks.items())
        for row in range(max_stack_size, 0, -1):
            print(
                " | ".join(
                    f"{("" if len(stack) - 1 < row else str(stack[row])).center(10)}" for _, stack in sorted(self.stacks.items(), key=lambda i: i[0],)
                )
            )
        print("-"*(13*len(self.stacks.keys()) - 3))
        print(" | ".join(f"{str(stack).center(10)}" for stack in sorted(self.stacks.keys())))


class Function:
    commands: list[Command]

    def __init__(self, commands: list[Command]):
        self.commands = commands

    def run(self, interpreter: Interpreter):
        for command in self.commands:
            command.run(interpreter)

    def render(self) -> str:
        return "\n\t".join(command.render() for command in self.commands)


class Command(ABC):
    line: int
    column: int

    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

    @abstractmethod
    def run(self, interpreter: Interpreter):
        pass

    @abstractmethod
    def render(self) -> str:
        pass


class Number(Command):
    value: Fraction

    def __init__(self, value: Rational, line: int, column: int):
        super().__init__(line, column)
        self.value = Fraction(value)

    def run(self, interpreter: Interpreter):
        interpreter.push(self.value)

    def render(self) -> str:
        return str(self.value)


class Word(Command):
    word: str

    def __init__(self, word: str, line: int, column: int):
        super().__init__(line, column)
        self.word = word

    def run(self, interpreter: Interpreter):
        if interpreter.debug_mode >= DebugMode.WORD_STEP:
            input(f"Word `{self.word}` at {interpreter.file}:{self.line}:{self.column}")
            interpreter.dump()
        match self.word:
            case "+":
                interpreter.push(interpreter.pop() + interpreter.pop())
            case "-":
                interpreter.push(interpreter.pop() - interpreter.pop())
            case "*":
                interpreter.push(interpreter.pop() * interpreter.pop())
            case "/":
                interpreter.push(interpreter.pop() / interpreter.pop())
            case "//":
                interpreter.push(interpreter.pop() // interpreter.pop())
            case "%":
                interpreter.push(interpreter.pop() % interpreter.pop())
            case "call":
                interpreter.call(interpreter.pop(), self.line, self.column)
            case "swap":
                value1 = interpreter.pop()
                value2 = interpreter.pop()
                interpreter.push(value1)
                interpreter.push(value2)
            case "dup":
                value1 = interpreter.pop()
                interpreter.push(value1)
                interpreter.push(value1)
            case "rot":
                value1 = interpreter.pop()
                value2 = interpreter.pop()
                value3 = interpreter.pop()
                interpreter.push(value1)
                interpreter.push(value3)
                interpreter.push(value2)
            case "drop":
                interpreter.pop()
            case "clear":
                interpreter.clear()
            case "exit":
                exit()
            case "getchar":
                interpreter.push(Fraction(ord(input())))
            case "putchar":
                print(chr(int(interpreter.pop())), end="")
            case "in":
                interpreter.push(Fraction(input()))
            case "out":
                print(str(interpreter.pop()), end="")
            case "change":
                interpreter.change_stack(interpreter.pop())
            case "debug":
                interpreter.set_debug(int(interpreter.pop()))
            case "dump":
                interpreter.dump()
            case word:
                interpreter.error(f"Unkown Word: `{word}`", self.line, self.column)

    def render(self) -> str:
        return self.word


if __name__ == '__main__':
    inp = Interpreter(sys.argv[1])
    inp.run()
