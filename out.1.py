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
        self.compiling = False

State = StateClass ()

                                                       #line 1
def pushasinteger (word):                              #line 3

        State.S.push (int ( word))                     #line 4

                                                       #line 5

                                                       #line 6
                                                       #line 7

def drop ():                                           #line 10
        # ( a -- )                                     #line 11

        State.S.pop ()                                 #line 12

                                                       #line 13

                                                       #line 14
                                                       #line 15

                                                       #line 16
ok                                                     #line 17
                                                       #line 18