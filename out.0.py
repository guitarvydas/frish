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

def docreate ():
    global State                                       #line 1


    parameterAddress =  len( State.RAM) + 4            #line 2

    State.S.push ( parameterAddress)                   #line 3

                                                       #line 4

def create (name):
    global State                                       #line 5 #line 6

    code( name,  normal,  docreate)                    #line 7

                                                       #line 8
                                                       #line 9


def _walk ():
    global State
    opcode = State.R.pop ()
    match opcode:
        case "drop":                                   #line 10
            # ( a -- )                                 #line 11

            State.S.pop ()                             #line 12

                                                       #line 13
                                                       #line 14




code( "drop",  0,  "drop")                             #line 15

ok()                                                   #line 16
                                                       #line 17