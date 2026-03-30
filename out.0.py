import re

class Stack(list):
    def push(my, *items):
        my.extend(items)

class StateClass:
    def __init__ (self):
        self.S = Stack()
        self.R = Stack()
        self.RAM = []
        self.LAST = -1
        self.IP = None
        self.W = None;
        self.BUFF = ""
        self.BUFP = 0
        self.compiling = [False]

State = StateClass ()

                                                       #line 1
def create ():
    global State                                       #line 2 #line 3

    code( xxx)                                         #line 4

                                                       #line 5
                                                       #line 6

def doconst ():
    global State# method for const                     #line 12


    parameter =  State.RAM [ State.W +  1]             #line 13

    State.S.push ( parameter)                          #line 14

                                                       #line 15
                                                       #line 16
                                                       #line 17

def docreate ():
    global State                                       #line 18


    parameterAddress =  len( State.RAM)  +  4          #line 19

    State.S.push ( parameterAddress)                   #line 20

                                                       #line 21
                                                       #line 22


def _walk ():
    global State
    opcode = State.R.pop ()
    match opcode:
        case "drop":                                   #line 7
            # ( a -- )                                 #line 8

            State.S.pop ()                             #line 9

                                                       #line 10
                                                       #line 11




code( "drop",  0,  "drop")                             #line 23

ok()                                                   #line 24
                                                       #line 25