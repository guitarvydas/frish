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


undefined
def fvget (name) undefined{
    , , , , , , undefined
    , , , , , ,

    fobjaddress =  _find(State.S.pop ()undefinedundefined)
    , , , , , , undefined
    , , , , , , undefinedundefined
    return  State.RAM [ fobjaddress+ 1]
    , , undefined
    , , undefined
}
undefined
                                                       #line 11
undefineddef fvset (name,v) undefined{
    , , , , , , undefined
    , , , , , ,

    fobjaddress =  _find(State.S.pop ()undefinedundefined)
    , , , , , , undefined
    , , , , , , undefinedundefined

    namefieldaddress =  fobjaddress+ 1
    , , , , , , undefined
    , , , , , ,
    State.RAM [ namefieldaddress] =  v
    , , undefined
    , , undefinedundefined
}
undefined
                                                       #line 17
                                                       #line 18
undefineddef doword () undefined{
    , , undefined
    , , #⎩20⎭
    #  Execute a colon-defined word using indirect threaded code interpretation.⎩21⎭
    #⎩22⎭
    #  This function implements the inner interpreter for threaded code execution.⎩23⎭
    #  Threaded code words store their definitions as arrays of code field addresses⎩24⎭
    #  (CFAs) in the parameter field area (PFA) immediately following the word header.⎩25⎭
    #⎩26⎭
    #  The execution model maintains two critical registers:⎩27⎭
    #⎩28⎭
    #  1. IP (Instruction Pointer): References the current position within the⎩29⎭
    #     threaded code array being interpreted. Since threaded words may invoke⎩30⎭
    #     other threaded words, IP must be preserved in a reentrant manner via⎩31⎭
    #     the return stack on each invocation.⎩32⎭
    #⎩33⎭
    #  2. W (Word Pointer): References the CFA of the currently executing primitive.⎩34⎭
    #     This global register serves an analogous function to 'self' in object-oriented⎩35⎭
    #     languages, enabling subroutines to access word header fields through fixed⎩36⎭
    #     offsets from the CFA.⎩37⎭
    #⎩38⎭
    #  Optimization rationale: W is positioned to reference the CFA rather than the⎩39⎭
    #  word header base. This design eliminates offset arithmetic for CFA access—the⎩40⎭
    #  most frequent header operation—at the cost of requiring offset adjustments⎩41⎭
    #  for other header fields (NFA: W-2, flags: W-1, PFA: W+1). This represents a⎩42⎭
    #  deliberate trade-off favoring the common case.⎩43⎭
    #⎩44⎭
    #  The inner interpreter loop performs the following operations:⎩45⎭
    #  - Fetch the next CFA from RAM[IP] into W (performing the first indirection)⎩46⎭
    #  - Increment IP to advance through the threaded code array⎩47⎭
    #  - Execute the primitive via RAM[W]() (performing the second indirection)⎩48⎭
    #⎩49⎭
    #  By caching the dereferenced CFA in W, we amortize the cost of double⎩50⎭
    #  indirection: both primitive execution and header field access within⎩51⎭
    #  subroutines utilize the same cached reference, avoiding redundant⎩52⎭
    #  dereferences. This is functionally equivalent to parameter passing in⎩53⎭
    #  object-oriented method invocation, but eliminates the overhead of⎩54⎭
    #  explicitly passing 'self' to each primitive.⎩55⎭
    #⎩56⎭
    #  Note: Ws state is only defined during primitive execution (within RAM[W]()).⎩57⎭
    #  Between loop iterations, W may reference a stale CFA, but this is⎩58⎭
    #  architecturally sound since W is unconditionally updated before each⎩59⎭
    #  primitive invocation.⎩60⎭
    #                                                  #line 61
                                                       #line 62

    State.R.append ( State.IP)
    , , , , , , undefined
    , , , , , , undefined
    State.IP =  State.W+ 1
    , , , , , , undefined
    , , , , , ,
    while ( -1!= State.RAM [ State.IP]):undefined{
        ,	, , undefined
        ,	, ,
        State.W =  State.RAM [ State.IP]
        ,	, , undefined
        ,	, ,
        State.IP =  State.IP+ 1
        ,	, , undefined
        ,	, ,
        State.RAM [ State.W]()
        , , , , , , undefined
        , , , , , , undefinedundefined
    }
    , , , , , , undefined
    , , , , , , undefined
    State.IP = State.R.pop ()
    , , undefined
    , , undefinedundefinedundefinedundefined
}
undefined
                                                       #line 72
                                                       #line 73
undefineddef notfound (word) undefined{
    , , , , , , undefined
    , , , , , ,

    State.S.clear()
    , , , , , , undefined
    , , , , , , undefined

    State.R.clear()
    , , , , , , undefined
    , , , , , , undefined
    print ( word, end="")
    , , , , , , undefined
    , , , , , , undefined
    print ( "?", end="")
    , , , , , , undefined
    , , , , , , undefined
    print ()
    , , undefined
    , , undefinedundefinedundefinedundefinedundefined
}
undefined
                                                       #line 81
undefineddef exec (xt) undefined{
    , , , , , , undefined
    , , , , , , # found and compiling and immediate    #line 83

    State.W =  xt
    , , , , , , undefined
    , , , , , ,
    State.IP =  -1undefined# Dummy to hold place in return stack. 	#line 85

    State.RAM [ xt]()undefined# Execute code.          #line 86
    undefinedundefined
}
undefined
                                                       #line 88
undefineddef compile_word (xt) undefined{
    , , , , , , undefined
    , , , , , , # found and not compiling              #line 90

    State.W =  xt
    , , , , , , undefined
    , , , , , ,
    State.IP =  -1undefined# Dummy to hold place in return stack. 	#line 92

    State.RAM [ xt]()undefined# Execute code.          #line 93
    undefinedundefined
}
undefined
                                                       #line 95
undefineddef pushasinteger (word) undefined{
    , , , , , , undefined
    , , , , , ,
    State.S.push (int ( word)undefined)
    , , undefined
    , , undefined
}
undefined
                                                       #line 99
undefineddef pushasfloat (word) undefined{
    , , , , , , undefined
    , , , , , ,
    State.S.push (float ( word)undefined)
    , , undefined
    , , undefined
}
undefined
                                                       #line 103
undefineddef compileinteger (word) undefined{
    , , , , , , undefined
    , , , , , ,
    pushasinteger( wordundefined)
    , , , , , , undefined
    , , , , , , undefinedundefined
    literalize()
    , , undefined
    , , undefined
}
undefined
                                                       #line 108
undefineddef compilefloat (word) undefined{
    , , , , , , undefined
    , , , , , ,
    pushasfloat( wordundefined)
    , , , , , , undefined
    , , , , , , undefinedundefined
    literalize()
    , , undefined
    , , undefined
}
undefined
                                                       #line 113
undefineddef code (name,flags,does) undefined{
    , , , , , , undefined
    , , , , , , # Add new word to RAM dictionary. We create a word (Forth "object") in RAM with 5 fields and extend the⎩115⎭
    #	the dictionary by linking back to the head of the dictionary list #line 116

    x =  len( State.RAMundefined)
    undefined
                                                       #line 118
    undefinedundefined

    State.RAM.append ( State.LAST)undefined# (LFA) link to previous word in dictionary list #line 119
    undefined

    State.RAM.append ( name)undefined# (NFA) name of word #line 120
    undefined

    State.RAM.append ( flags)undefined#       0 = normal word, 1 = immediate word #line 121
    undefined

    State.RAM.append ( does)undefined# (CFA) function pointer that points to code that executes the word #line 122
                                                       #line 123
    undefined
    State.LAST =  xundefined# LAST is the pointer to the head of the dictionary list, set it to point to⎩124⎭
    #					this new word                                #line 125
    undefinedundefinedundefinedundefinedundefined
}
undefined
                                                       #line 127
undefineddef literalize () undefined{
    , , , , , , undefined
    , , , , , , # Compile literal into definition.     #line 129


    State.RAM.append ( _find( "(literal)"undefined)undefinedundefined)undefined## Compile address of doliteral. #line 130
    undefined

    State.RAM.append (State.S.pop ()undefined)undefined# # Compile literal value. #line 131
    undefinedundefined
}
undefined
                                                       #line 133
undefineddef ok () undefined{
    , , , , , , undefined
    , , , , , , # ( --) Interaction loop -- REPL       #line 135


    blank =  32
    , , , , , , undefined
    , , , , , ,
    while  True:undefined{
        ,	, , undefined
        ,	, ,

        State.BUFF = input("OK ")
        State.BUFP = 0

        ,	, , undefined
        ,	, , undefined
        while not (State.BUFP >= len(State.BUFF))undefined:undefined{
            ,	, , , , , undefined
            ,	, , , , ,
            xinterpret()
            ,	, , undefined
            ,	, ,
        }
        , , , , , , undefined
        , , , , , , undefinedundefined
    }
    , , undefined
    , , undefinedundefined
}
undefined
                                                       #line 144
undefineddef doconst () undefined{undefined# method for const #line 145


    parameter =  State.RAM [ State.W+ 1]
    , , , , , , undefined
    , , , , , ,
    State.S.push ( parameter)
    , , undefined
    , , undefinedundefined
}
undefined
                                                       #line 149
                                                       #line 150
undefineddef docreate () undefined{
    , , , , , , undefined
    , , , , , ,

    parameterAddress =  len( State.RAMundefined)undefinedundefined+ 4
    , , , , , , undefined
    , , , , , ,
    State.S.push ( parameterAddress)
    , , undefined
    , , undefinedundefined
}
, , undefined
, ,  undefineddef create (name) undefined{
    , , , , , , undefined
    , , , , , ,

    normal =  0
    , , , , , , undefined
    , , , , , ,
    code( name,undefined normal,undefined docreateundefined)
    , , undefined
    , , undefinedundefinedundefined
}
, , undefined
, ,  undefineddef comma (value) undefined{
    , , , , , , undefined
    , , , , , ,

    State.RAM.append ( value)
    , , undefined
    , , undefined
}
undefined
                                                       #line 162
undefineddef fvar (name,value) undefined{
    , , , , , , undefined
    , , , , , ,
    create( nameundefined)
    , , , , , , undefined
    , , , , , , undefinedundefined
    comma( valueundefined)
    , , undefined
    , , undefinedundefinedundefined
}
undefined
                                                       #line 167
undefineddef _find (name) undefined{
    , , , , , , undefined
    , , , , , , # "( name -- cfa|0) Find CFA of word name." #line 169


    x =  State.LAST
    , , , , , , undefined
    , , , , , ,
    while ( x >=  0):undefined{
        ,	, , undefined
        ,	, , # ## print(f"-- {x} : {RAM[x]}, {RAM[x + 1]}")  # Debug. #line 172

        if ( name ==  State.RAM [ x+ 1]):undefined{undefined# # Match! #line 173

            return  x+ 3
            ,	, , undefined
            ,	, ,
        }undefined
        else:undefined{
            ,	, , , , , , undefined
            ,	, , , , , ,
            x =  State.RAM [ x]undefined# # Get next link. #line 176

        }
        , , , , , , undefined
        , , , , , , undefined
    }
    , , , , , , undefined
    , , , , , , undefined
    return  0undefined# # Nothing found.               #line 179
    undefinedundefined
}
undefined
                                                       #line 181
undefineddef debugok () undefined{
    , , , , , , undefined
    , , , , , , # ( --) Interaction loop -- REPL       #line 183


    blank =  32
    ,	, , undefined
    ,	, ,

    State.BUFF = "7 ."
    State.BUFP = 0

    ,	, , undefined
    ,	, , undefined
    while not (State.BUFP >= len(State.BUFF))undefined:undefined{
        ,	, , , , , undefined
        ,	, , , , ,
        if ( xinterpret()):undefined{
            ,	,	, , , , , undefined
            ,	,	, , , , ,
            print ( " ok", end="")
            ,	,	, , , , , undefined
            ,	,	, , , , , undefined
            print ()
            ,	, , , , , undefined
            ,	, , , , , undefinedundefined
        }
        ,	, , , , , undefined
        ,	, , , , , undefined
        print ( State.BUFP, end="")undefinedundefined
        print ( " -- ", end="")undefinedundefined
        print ( State.BUFF, end="")undefinedundefined
        print ()
        ,	, , , , , undefined
        ,	, , , , , undefined
        xdots()
        ,	, , undefined
        ,	, , undefinedundefinedundefinedundefinedundefined
    }
    ,	, , , , , undefined
    ,	, , , , , undefined
    print ( State.BUFP, end="")undefinedundefined
    print ( " == ", end="")undefinedundefined
    print ( State.BUFF, end="")undefinedundefined
    print ()
    ,	, , , , , undefined
    ,	, , , , , undefined
    xdot()
    ,	, , , , , undefined
    ,	, , , , ,
    xdots()
    , , undefined
    , , undefinedundefinedundefinedundefinedundefinedundefinedundefinedundefined
}
undefined
undefined
undefined
                                                       #line 199

undefineddef create undefined{
    , , , , , , undefined
    , , , , , ,

    blank =  32
    , , , , , , undefined
    , , , , , ,
    State.S.push ( blank)
    , , , , , , undefined
    , , , , , , undefined
    xword()
    , , , , , , undefined
    , , , , , ,

    name = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined
    create( nameundefined)
    , , undefined
    , , undefinedundefinedundefinedundefinedundefinedundefined
}
undefined
                                                       #line 209
undefineddef drop undefined{
    , , , , , , undefined
    , , , , , , # ( a -- )                             #line 211

    State.S.pop ()
    , , undefined
    , , undefined
}
undefined
                                                       #line 214
undefineddef dup undefined{
    , , , , , , undefined
    , , , , , , # ( a -- a a )                         #line 216


    A = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined
    State.S.push ( A)
    , , , , , , undefined
    , , , , , , undefined
    State.S.push ( A)
    , , undefined
    , , undefinedundefinedundefined
}
undefined
                                                       #line 221
undefineddef negate undefined{
    , , , , , , undefined
    , , , , , , # ( n -- (-n) )                        #line 223


    n = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined
    State.S.push ( -n)
    , , undefined
    , , undefinedundefined
}
undefined
                                                       #line 227
undefineddef emit undefined{
    , , , , , , undefined
    , , , , , , # ( c -- ) emit specified character    #line 229


    c = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined
    print (chr (int ( c)), end="")
    , , undefined
    , , undefinedundefined
}
undefined
                                                       #line 233
undefineddef cr undefined{undefined
    print ()undefinedundefined
}
, , undefined
, ,  undefineddef . undefined{undefined# ( n --) Print TOS
    print (State.S.pop ()undefined, end="")undefinedundefined
    print ()undefinedundefinedundefined
}
, , undefined
, ,  undefineddef .s undefined{undefined# ( --) Print stack contents
    print (State.Sundefined, end="")undefinedundefined
    print ()undefinedundefinedundefined
}
undefined
                                                       #line 237
undefineddef + undefined{
    , , , , , , undefined
    , , , , , , # ( a b -- sum)                        #line 239


    B = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined

    A = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined
    State.S.push ( A+ B)
    , , undefined
    , , undefinedundefinedundefined
}
undefined
                                                       #line 244
undefineddef * undefined{
    , , , , , , undefined
    , , , , , , # ( a b -- product )                   #line 246


    B = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined

    A = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined
    State.S.push ( A* B)
    , , undefined
    , , undefinedundefinedundefined
}
undefined
                                                       #line 251
undefineddef = undefined{
    , , , , , , undefined
    , , , , , , # ( a b -- bool )                      #line 253


    B = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined

    A = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined
    State.S.push ( A ==  B)
    , , undefined
    , , undefinedundefinedundefined
}
undefined
                                                       #line 258
undefineddef < undefined{
    , , , , , , undefined
    , , , , , , # ( a b -- bool )                      #line 260


    B = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined

    A = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined
    State.S.push ( A <  B)
    , , undefined
    , , undefinedundefinedundefined
}
undefined
                                                       #line 265
undefineddef > undefined{
    , , , , , , undefined
    , , , , , , # ( a b -- bool )                      #line 267


    B = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined

    A = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined
    State.S.push ( A >  B)
    , , undefined
    , , undefinedundefinedundefined
}
undefined
                                                       #line 272
undefineddef 0= undefined{
    , , , , , , undefined
    , , , , , , # ( a -- bool )                        #line 274


    a = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined
    State.S.push ( a ==  0)
    , , undefined
    , , undefinedundefined
}
undefined
                                                       #line 278
undefineddef 0<" undefined{
    , , , , , , undefined
    , , , , , , # ( a -- bool )                        #line 280


    a = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined
    State.S.push ( 0 <  a)
    , , undefined
    , , undefinedundefined
}
undefined
                                                       #line 284
undefineddef 0> undefined{
    , , , , , , undefined
    , , , , , , # ( a -- bool )                        #line 286


    a = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined
    State.S.push ( 0 >  a)
    , , undefined
    , , undefinedundefined
}
undefined
                                                       #line 290
undefineddef not undefined{
    , , , , , , undefined
    , , , , , , # ( a -- bool )                        #line 292


    a = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined
    State.S.push (not  a)
    , , undefined
    , , undefinedundefined
}
undefined
                                                       #line 296
undefineddef and undefined{
    , , , , , , undefined
    , , , , , , # ( a b -- bool )                      #line 298


    b = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined

    a = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined
    State.S.push ( a and  b)
    , , undefined
    , , undefinedundefinedundefined
}
undefined
                                                       #line 303
undefineddef or undefined{
    , , , , , , undefined
    , , , , , , # ( a b -- bool )                      #line 305


    b = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined

    a = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined
    State.S.push ( a or  b)
    , , undefined
    , , undefinedundefinedundefined
}
undefined
                                                       #line 310
undefineddef >r undefined{
    , , , , , , undefined
    , , , , , , # ( a --  )                            #line 312


    a = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined
    State.R.append ( a)
    , , undefined
    , , undefinedundefined
}
undefined
                                                       #line 316
undefineddef r> undefined{
    , , , , , , undefined
    , , , , , , # ( -- x )                             #line 318


    x = State.R.pop ()
    , , , , , , undefined
    , , , , , , undefined
    State.S.push ( x)
    , , undefined
    , , undefinedundefined
}
undefined
                                                       #line 322
undefineddef i undefined{
    , , , , , , undefined
    , , , , , , # ( -- i ) get current loop index from R stack #line 324


    i = State.R [-1]
    , , , , , , undefined
    , , , , , , undefined
    State.S.push ( i)
    , , undefined
    , , undefinedundefined
}
undefined
                                                       #line 328
undefineddef i' undefined{
    , , , , , , undefined
    , , , , , , # ( -- i ) get outer loop limit from R stack #line 330


    i = State.R [-2]
    , , , , , , undefined
    , , , , , , undefined
    State.S.push ( i)
    , , undefined
    , , undefinedundefined
}
undefined
                                                       #line 334
undefineddef j undefined{
    , , , , , , undefined
    , , , , , , # ( -- j ) get outer loop index from R stack #line 336


    j = State.R [-3]
    , , , , , , undefined
    , , , , , , undefined
    State.S.push ( j)
    , , undefined
    , , undefinedundefined
}
undefined
                                                       #line 340
undefineddef swap undefined{
    , , , , , , undefined
    , , , , , , # ( a b -- b a)                        #line 342


    B = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined

    A = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined
    State.S.push ( B)
    , , , , , , undefined
    , , , , , , undefined
    State.S.push ( A)
    , , undefined
    , , undefinedundefinedundefinedundefined
}
, , undefined
, ,  undefineddef - undefined{
    , , , , , , undefined
    , , , , , , # ( a b -- diff)                       #line 349


    B = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined

    A = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined
    State.S.push ( A- B)
    , , undefined
    , , undefinedundefinedundefined
}
, , undefined
, ,  undefineddef / undefined{
    , , , , , , undefined
    , , , , , , # ( a b -- div)                        #line 355

    xswap()
    , , , , , , undefined
    , , , , , ,

    B = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined

    A = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined
    State.S.push ( B [A])
    , , undefined
    , , undefinedundefinedundefinedundefined
}
undefined
                                                       #line 361
undefineddef word undefined{
    , , , , , , undefined
    , , , , , , # (char -- string) Read in string delimited by char #line 363


    wanted = chr(State.S.pop ())
    , , , , , , undefined
    , , , , , , undefined

    found = ""
    while State.BUFP < len(State.BUFF):
        x = State.BUFF[State.BUFP]
        State.BUFP += 1
        if wanted == x:
            if 0 == len(found):
                continue
            else:
                break
        else:
            found += x
    State.S.append(found)

    , , undefined
    , , undefinedundefined
}
undefined
                                                       #line 367
# Example of state-smart word, which Brodie sez not to do. Sorry, Leo... #line 368
# This sin allows it to be used the same way compiling or interactive. #line 369
undefineddef ' undefined{
    , , , , , , undefined
    , , , , , , # ( -- string) Read up to closing dquote, push to stack #line 371
    # A string in Forth begins with the word " (followed by a space) then all characters up to the next " #line 372
    # E.G. " abc"                                      #line 373


    DQ =  34
    , , , , , , undefined
    , , , , , ,
    State.S.push ( DQ)
    , , , , , , undefined
    , , , , , , undefined
    xword()
    , , , , , , undefined
    , , , , , ,
    if State.compilingundefined:undefined{
        ,	, , undefined
        ,	, ,
        literalize()
        , , , , , , undefined
        , , , , , , undefined
    }
    , , undefined
    , , undefinedundefinedundefinedundefined
}
undefined
                                                       #line 381
undefineddef .' undefined{
    , , , , , , undefined
    , , , , , , # ( --) Print string.                  #line 383

    xquote()
    , , , , , , undefined
    , , , , , ,
    print (State.S.pop ()undefined, end="")
    , , undefined
    , , undefinedundefined
}
undefined
                                                       #line 387
                                                       #line 388
                                                       #line 389
undefineddef (literal) undefined{
    , , , , , , undefined
    , , , , , , #⎩391⎭
    #   Inside definitions only, pushes compiled literal to stack ⎩392⎭
    #⎩393⎭
    #       Certain Forth words are only applicable inside compiled sequences of subroutines ⎩394⎭
    #       Literals are handled in different ways when interpreted when in the REPL vs⎩395⎭
    #       compiled into sequences of subrs ⎩396⎭
    #       In the REPL, when we encounter a literal, we simply push it onto the stack ⎩397⎭
    #       In the compiler, though, we have to create an instruction that pushes ⎩398⎭
    #	 the literal onto the stack. ⎩399⎭
    #	 Compiled code doesn't do what the REPL does, we have to hard-wire and ⎩400⎭
    #	 bake in code that pushes the literal when the time comes to run the sequence. ⎩401⎭
    #⎩402⎭
    #       This word - "(literal)" - is a simple case and one could actually type this ⎩403⎭
    #	 instruction into the REPL, but, that would be redundant.  Other kinds of words, ⎩404⎭
    #	 e.g. some control-flow words, tend to be messier and the code below only handles ⎩405⎭
    #	 the compiled aspects and ignores the REPL aspects ⎩406⎭
    #⎩407⎭
    #       "IP" is the current word index in a sequence of words being compiled. ⎩408⎭
    #                                                  #line 409


    lit =  State.RAM [ State.IP]
    , , , , , , undefined
    , , , , , ,
    State.S.push ( lit)
    , , , , , , undefined
    , , , , , , undefined
    State.IP =  State.IP+ 1undefined# move past this item (the literal) - we're done with it #line 412
    undefinedundefined
}
undefined
                                                       #line 414
undefineddef branch undefined{
    , , , , , , undefined
    , , , , , , # This instruction appears only inside subroutine sequences, jump to address in next cell #line 416
    # This instruction is inserted into a subr sequence when compiling control-flow words, like "else" see below) #line 417

    State.IP =  State.RAM [ State.IP]
    , , , , , , undefined
    , , , , , , # normally, we just execute an instruction then move the IP sequentially forward by 1 unit, i.e. IP ⇐ IP + 1 #line 419
    #   in this case, though, we explicitly change the IP to some other value and don't just increment it #line 420

}
undefined
                                                       #line 422
undefineddef 0branch undefined{
    , , , , , , undefined
    , , , , , , # This instruction appears only inside subroutine sequences, jump on false to address in next cell #line 424


    test = bool (State.S.pop ()undefined)
    , , , , , , undefined
    , , , , , , undefined
    if ( test):undefined{
        ,	, , undefined
        ,	, ,
        State.IP =  State.IP+ 1
        , , , , , , undefined
        , , , , , ,
    }undefined
    else:undefined{
        ,	, undefined
        ,	,
        State.IP =  State.RAM [ State.IP]
        , , , , , , undefined
        , , , , , ,
    }
    , , undefined
    , , undefinedundefined
}
undefined
                                                       #line 432
                                                       #line 433
# "immediate" words are fully operational even when in compile mode. Some (not all) of these words are meant to⎩434⎭
#      work /only/ in compile mode. At the REPL prompt ("interpret" mode), they produce unwanted results.⎩435⎭
#    immediate words: xif, xelse, xthen, xquote, xcomment, xsemi⎩436⎭
#    immediate words that only have meaning in compile mode: xif, xelse, xthen, xsemi⎩437⎭
#                                                      #line 438
                                                       #line 439
                                                       #line 440
# IF, ELSE and THEN are "immediate" words - they should only be used inside of ":" (colon compiler) #line 441
                                                       #line 442
# see diagram compiling-IF-THEN.drawio.png             #line 443
undefinedState.compiling = False
def if undefined{
    , , , , , , undefined
    , , , , , , # This instruction appears only inside subroutine sequences, ( f -- ) compile if test and branchFalse  #line 445
    # Step. 1: generate conditional branch to yet-unknown target1  #line 446


    branchFalseAddress =  _find( "0branch"undefined)
    , , , , , , undefined
    , , , , , , undefinedundefined

    State.RAM.append ( branchFalseAddress)undefined# insert branch-if-false opcode (word)  #line 448
    undefined
    State.R.append (len (Stack.RAM)undefined)undefined# target1 onto r-stack as memo for later fixup  #line 449
    undefined

    target1 =  -1
    , , , , , , undefined
    , , , , , ,

    State.RAM.append ( target1)undefined# branch target will be fixed up later  #line 451
    # Step. 2: generate code for true branch - return to compiler which will compile the following words  #line 452
    # THEN or ELSE will do the fixup of target1        #line 453
    undefinedundefinedundefinedundefinedundefined
}
undefined
                                                       #line 455
# see diagram compiling-IF-ELSE-THEN.drawio.png        #line 456
undefinedState.compiling = False
def else undefined{
    , , , , , , undefined
    , , , , , , # Step. 1: fixup target1 from IF-true, retrieving memo from R-stack #line 458


    target1 = State.R.pop ()
    , , , , , , undefined
    , , , , , , undefined
    State.RAM [ target1] = len (Stack.RAM)
    , , , , , , undefined
    , , , , , , # Step. 2: generate unconditional branch for preceding IF, creating new memo for target2 on R-stack #line 461
    undefined

    brAddress =  _find( "branch"undefined)
    , , , , , , undefined
    , , , , , , undefinedundefined
    State.R.append (len (Stack.RAM)undefined)undefined# target2 address on R-stack as memo for later fixup #line 463
    undefined

    target2 =  -1
    , , , , , , undefined
    , , , , , ,

    State.RAM.append ( target2)undefined# branch target will be fixed up later #line 465
    # Step. 3: generate code for false branch - return to compiler which will compile the following words #line 466
    # THEN will do the fixup of target2                #line 467
    undefinedundefinedundefinedundefinedundefinedundefined
}
undefined
                                                       #line 469
# see diagrams compiling-IF-THEN.drawio.png and compiling-IF-ELSE-THEN.drawio.png #line 470
undefinedState.compiling = False
def then undefined{
    , , , , , , undefined
    , , , , , , # Step. 1: fixup target (from IF or from ELSE, above), retrieving memo from R-stack #line 472


    target = State.R.pop ()
    , , , , , , undefined
    , , , , , , undefined
    State.RAM [ target] = len (Stack.RAM)
    , , undefined
    , , undefinedundefined
}
undefined
                                                       #line 476
undefineddef (do) undefined{
    , , , , , , undefined
    , , , , , , # ( limit index --) Puts limit and index on return stack. #line 478

    xswap()
    , , , , , , undefined
    , , , , , ,

    index = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined

    limit = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined
    State.R.append ( index)
    , , , , , , undefined
    , , , , , , undefined
    State.R.append ( limit)
    , , undefined
    , , undefinedundefinedundefinedundefinedundefined
}
undefined
                                                       #line 485
undefinedState.compiling = False
def do undefined{
    , , , , , , undefined
    , , , , , , # (  limit index --) Begin counted loop. #line 487


    State.RAM.append ( _find( "(do)"undefined)undefinedundefined)undefined# Push do loop handler. #line 488
    undefined
    State.R.append (len (Stack.RAM)undefined)undefined# Push address to jump back to. #line 489
    undefinedundefined
}
undefined
                                                       #line 491
undefineddef (loop) undefined{
    , , , , , , undefined
    , , , , , , # (  -- f) Determine if loop is done.  #line 493


    index = State.R.pop ()
    , , , , , , undefined
    , , , , , , undefined

    limit = State.R.pop ()
    , , , , , , undefined
    , , , , , , undefined

    cond = ( index >=  limit)
    , , , , , , undefined
    , , , , , ,
    State.S.push ( cond)
    , , , , , , undefined
    , , , , , , undefined
    if ( cond):undefined{undefined# clean up rstack if index >= limit #line 498

        State.R.pop ()
        ,	, , undefined
        ,	, , undefined
        State.R.pop ()
        , , , , , , undefined
        , , , , , , undefinedundefined
    }
    , , undefined
    , , undefinedundefinedundefinedundefinedundefined
}
undefined
                                                       #line 503
undefinedState.compiling = False
def +loop undefined{
    , , , , , , undefined
    , , , , , , # ( --) Close counted loop.            #line 505


    State.RAM.append ( _find( "(loop)"undefined)undefinedundefined)undefined# Compile in loop test. #line 506
    undefined

    State.RAM.append ( _find( "0branch"undefined)undefinedundefined)undefined# Compile in branch check. #line 507
    undefined

    State.RAM.append (State.R.pop ()undefined)undefined# Address to jump back to. #line 508
    undefinedundefinedundefined
}
undefined
                                                       #line 510
undefinedState.compiling = False
def loop undefined{
    , , , , , , undefined
    , , , , , , # (  --) Close counted loop.           #line 512

    State.S.push ( 1)
    , , , , , , undefined
    , , , , , , undefined
    literalize()undefined# Default loop increment for x_loop. #line 514


    State.RAM.append ( _find( "(loop)"undefined)undefinedundefined)undefined# Compile in loop test. #line 515
    undefined

    State.RAM.append ( _find( "0branch"undefined)undefinedundefined)undefined# Compile in branch check. #line 516
    undefined

    State.RAM.append (State.R.pop ()undefined)undefined# Address to jump back to. #line 517
    undefinedundefinedundefinedundefinedundefined
}
undefined
                                                       #line 519
undefinedState.compiling = False
def begin undefined{
    , , , , , , undefined
    , , , , , ,
    State.R.append (len (Stack.RAM)undefined)undefined# ( --) Start indefinite loop. #line 521
    undefined
}
undefined
                                                       #line 523
undefinedState.compiling = False
def until undefined{
    , , , , , , undefined
    , , , , , , # (  f --) Close indefinite loop with test. #line 525


    State.RAM.append ( _find( "0branch"undefined)undefinedundefined)undefined# Expects result of test on stack. #line 526
    undefined

    State.RAM.append (State.R.pop ()undefined)undefined# Address to jump back to. #line 527
    undefinedundefined
}
undefined
                                                       #line 529
                                                       #line 530
                                                       #line 531
#  "... 123 constant K ..."                            #line 532
#  at interpretation time: 123 is on the Stack, we have consumed "constant" from BUFF, BUFF now contains "K ..." #line 533
#  invoke 'word' which parses "K" and pushed it. The stack becomes [... 123 "K"] #line 534
#  pop "K", pop 123, create a new word called 'K' with its PFA set to 123 and its CFA set to a subr that⎩535⎭
#       gets 123 from its PFA and pushes it onto the stack #line 536
undefineddef const undefined{
    , , , , , , undefined
    , , , , , , #  get next word - the name - from BUFF #line 538


    blank =  32
    , , , , , , undefined
    , , , , , ,
    State.S.push ( blank)
    , , , , , , undefined
    , , , , , , undefined
    xword()
    , , , , , , undefined
    , , , , , , #  stack is now: ( NNNN name -- )      #line 542


    name = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined

    value = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined

    normal =  0
    , , , , , , undefined
    , , , , , ,

    fobj =  code( name,undefined normal,undefined doconstundefined)
    , , , , , , undefined
    , , , , , , undefinedundefined

    State.RAM.append ( value)
    , , undefined
    , , undefinedundefinedundefinedundefinedundefinedundefinedundefinedundefined
}
undefined
                                                       #line 549
undefineddef , undefined{
    , , , , , , undefined
    , , , , , ,
    comma(State.S.pop ()undefinedundefined)
    , , undefined
    , , undefinedundefined
}
undefined
                                                       #line 553
undefineddef variable undefined{
    , , , , , , undefined
    , , , , , ,

    blank =  32
    , , , , , , undefined
    , , , , , ,
    State.S.push ( blank)
    , , , , , , undefined
    , , , , , , undefined
    xword()
    , , , , , , undefined
    , , , , , ,

    name = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined

    value = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined
    fvar( name,undefined valueundefined)
    , , undefined
    , , undefinedundefinedundefinedundefinedundefinedundefinedundefined
}
undefined
                                                       #line 562
undefineddef dump undefined{
    , , , , , , undefined
    , , , , , ,

    n = int (State.S.pop ()undefined)
    , , , , , , undefined
    , , , , , , undefined

    start = int (State.S.pop ()undefined)
    , , , , , , undefined
    , , , , , , undefined
    print ( "----------------------------------------------------------------", end="")
    , , , , , , undefined
    , , , , , , undefined

    a =  start
    , , , , , , undefined
    , , , , , ,
    while ( a <  start+( min( n,undefined( len( State.RAMundefined)undefinedundefined- start)undefined)undefinedundefined)):undefined{
        ,	, , undefined
        ,	, ,
        print ( a, end="")
        ,	, , undefined
        ,	, , undefined
        print ( ": ", end="")
        ,	, , undefined
        ,	, , undefined
        print ( State.RAM [ a], end="")
        ,	, , undefined
        ,	, , undefined
        print ()
        ,	, , undefined
        ,	, , undefined

        a =  a+ 1
        , , , , , , undefined
        , , , , , , undefinedundefinedundefinedundefined
    }
    , , undefined
    , , undefinedundefinedundefinedundefinedundefined
}
undefined
                                                       #line 576
undefineddef ! undefined{
    , , , , , , undefined
    , , , , , ,

    b = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined

    a = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined
    State.RAM [ b] =  a
    , , undefined
    , , undefinedundefined
}
undefined
                                                       #line 582
undefineddef bye undefined{undefined# ( --) Leave interpreter

    raise SystemExitundefinedundefined
}
undefined
                                                       #line 584
                                                       #line 585
undefineddef find undefined{
    , , , , , , undefined
    , , , , , , # "( name | -- (name 0)|(xt 1)|(xt -1)) Search for word name." #line 587
    # 3 possible results: 1. (name 0) if not found, 2. (xt 1) if found and word is immediate, 3. (xt -1) if found and word is normal #line 588

    State.S.push ( 32)
    , , , , , , undefined
    , , , , , , undefined
    xword()
    , , , , , , undefined
    , , , , , ,

    found =  _find(State.S[-1]undefinedundefined)
    , , , , , , undefined
    , , , , , , undefinedundefined
    if ( 0 ==  found):undefined{
        ,	, , undefined
        ,	, ,
        State.S.push ( 0)
        , , , , , , undefined
        , , , , , , undefined
    }undefined
    else:undefined{
        ,	, , undefined
        ,	, ,
        State.S.pop ()undefined# # Get rid of name on stack. #line 595
        undefined
        State.S.push ( found)
        ,	, , undefined
        ,	, , undefined

        immediate =  -1
        ,	, , undefined
        ,	, ,
        if ( State.RAM [State.S[-1]undefined- 1] &  1):undefined{undefined
            immediate =  1undefined
        }
        ,	, , undefined
        ,	, , undefined
        State.S.push ( immediate)
        , , , , , , undefined
        , , , , , , undefinedundefinedundefinedundefinedundefined
    }
    , , undefined
    , , undefinedundefinedundefinedundefined
}
undefined
                                                       #line 602
undefineddef ' undefined{
    , , , , , , undefined
    , , , , , , # "( name -- xt|-1) Search for execution token of word name." #line 604

    State.S.push ( 32)
    , , , , , , undefined
    , , , , , , undefined
    xword()
    , , , , , , undefined
    , , , , , ,

    name = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined

    found =  _find( nameundefined)
    , , , , , , undefined
    , , , , , , undefinedundefined
    State.S.push ( found)
    , , undefined
    , , undefinedundefinedundefinedundefinedundefined
}
undefined
                                                       #line 611
undefineddef None undefined{
    , , , , , , undefined
    , , , , , ,

    State.S.append (None)
    , , undefined
    , , undefined
}
undefined
                                                       #line 615
undefineddef words undefined{
    , , , , , , undefined
    , , , , , , # print words in dictionary            #line 617


    x =  State.LAST
    , , , , , , undefined
    , , , , , ,
    while ( x >  -1):undefined{
        ,	, , undefined
        ,	, ,
        print ( State.RAM [ x+ 1], end="")
        ,	, , undefined
        ,	, , undefined
        print ( " ", end="")
        , , , , , , undefined
        , , , , , , undefinedundefined
    }
    , , , , , , undefined
    , , , , , , undefined
    print ()
    , , undefined
    , , undefinedundefinedundefined
}
undefined
                                                       #line 625
                                                       #line 626
undefineddef execute undefined{
    , , , , , , undefined
    , , , , , , # invoke given word                    #line 628


    wordAddress = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined
    wordAddress()
    , , undefined
    , , undefined
}
undefined
                                                       #line 632
                                                       #line 633
undefineddef : undefined{
    , , , , , , undefined
    , , , , , , # ( name | --) Start compilation.      #line 635


    blank =  32
    , , , , , , undefined
    , , , , , ,
    State.S.push ( blank)
    , , , , , , undefined
    , , , , , , undefined
    xword()
    , , , , , , undefined
    , , , , , ,

    name = State.S.pop ()
    , , , , , , undefined
    , , , , , , undefined
    code( name,undefined 0,undefined dowordundefined)
    , , , , , , undefined
    , , , , , , undefinedundefined
    State.compiling = True
    , , undefined
    , , undefinedundefinedundefinedundefinedundefinedundefined
}
undefined
                                                       #line 643
undefinedState.compiling = False
def ; undefined{
    , , , , , , undefined
    , , , , , , # ( --) Finish definition.             #line 645
                                                       #line 646


    State.RAM.append ( -1)undefined# Marker for end of definition. #line 647
    undefined
    State.compiling = False
    , , undefined
    , , undefinedundefined
}
undefined
                                                       #line 650
undefineddef interpret undefined{
    , , , , , , undefined
    , , , , , , # ( string --) Execute word.           #line 652
                                                       #line 653

    xfind()
    , , , , , , undefined
    , , , , , , # 3 possible results from xfind:⎩655⎭
    #	  1. (name 0) if not found,⎩656⎭
    #	  2. (xt 1) if found and word is immediate,⎩657⎭
    #	  3. (xt -1) if found and word is normal         #line 658


    result = State.S.pop ()undefinedundefined

    foundimmediate = ( result ==  1)
    , , , , , , undefined
    , , , , , ,

    item = State.S.pop ()undefinedundefined

    foundnormal = ( result ==  -1)
    ,	,	,	,	,	,	,	,	, , , , , , undefined
    ,	,	,	,	,	,	,	,	, , , , , ,

    notfound = ( result ==  0)
    ,	,	,	,	,	,	,	,	, , , , , , undefined
    ,	,	,	,	,	,	,	,	, , , , , ,

    found = ( foundimmediate or  foundnormal)
    undefined
                                                       #line 663

    if ( found):undefined{
        , , , , undefined
        , , , ,
        if (State.compilingundefined):undefined{
            , , , , , , , , undefined
            , , , , , , , ,
            if ( foundimmediate):undefined{
                , , , , , , , , , , , , undefined
                , , , , , , , , , , , ,
                exec( itemundefined)
                , , , , , , , , undefined
                , , , , , , , , undefinedundefined
            }undefined
            else:undefined{
                , , , , , , , , , , , , undefined
                , , , , , , , , , , , ,
                compileword( itemundefined)
                , , , , , , , , undefined
                , , , , , , , , undefinedundefined
            }
            , , , , , , , , undefined
            , , , , , , , ,                            #line 671
            undefined
        }undefined
        else:undefined{
            , , , , , , , , undefined
            , , , , , , , ,
            exec( itemundefined)
            , , , , undefined
            , , , , undefinedundefined
        }
        , , , , undefined
        , , , ,                                        #line 675
        undefined
    }undefined
    else:undefined{
        , , , , undefined
        , , , ,
        if (State.compilingundefined):undefined{
            , , , , , , , , undefined
            , , , , , , , ,
            if (re.match(r"^-?\d*$",  item)undefined):undefined{
                , , , , , , , , , , , , undefined
                , , , , , , , , , , , ,
                compileinteger( itemundefined)
                , , , , , , , , undefined
                , , , , , , , , undefinedundefined
            }undefined
            else:undefined{
                , , , , , , , , , , , , undefined
                , , , , , , , , , , , ,
                if (re.match(r"^-?d*\.?\d*$",  item)undefined):undefined{
                    , , , , , , , , , , , , , , , , undefined
                    , , , , , , , , , , , , , , , ,
                    compilefloat( itemundefined)
                    , , , , , , , , , , , , undefined
                    , , , , , , , , , , , , undefinedundefined
                }undefined
                else:undefined{
                    , , , , , , , , , , , , , , , , undefined
                    , , , , , , , , , , , , , , , ,
                    returnFalse()
                    , , , , , , , , , , , , undefined
                    , , , , , , , , , , , ,
                }
                , , , , , , , , , , , , undefined
                , , , , , , , , , , , ,                #line 686
                undefined
            }
            , , , , , , , , undefined
            , , , , , , , ,                            #line 688
            undefined
        }undefined
        else:undefined{
            , , , , , , , , undefined
            , , , , , , , ,
            if (re.match(r"^-?\d*$",  item)undefined):undefined{
                , , , , , , , , , , , , undefined
                , , , , , , , , , , , ,
                pushasinteger( itemundefined)
                , , , , , , , , undefined
                , , , , , , , , undefinedundefined
            }undefined
            else:undefined{
                , , , , , , , , , , , , undefined
                , , , , , , , , , , , ,
                if (re.match(r"^-?d*\.?\d*$",  item)undefined):undefined{
                    , , , , , , , , , , , , , , , , undefined
                    , , , , , , , , , , , , , , , ,
                    pushasfloat( itemundefined)
                    , , , , , , , , , , , , undefined
                    , , , , , , , , , , , , undefinedundefined
                }undefined
                else:undefined{
                    , , , , , , , , , , , , , , , , undefined
                    , , , , , , , , , , , , , , , ,
                    returnFalse()
                    , , , , , , , , , , , , undefined
                    , , , , , , , , , , , ,
                }
                , , , , , , , , , , , , undefined
                , , , , , , , , , , , ,                #line 698
                undefined
            }
            , , , , , , , , undefined
            , , , , , , , ,                            #line 700
            undefined
        }
        , , , , undefined
        , , , ,                                        #line 702
        undefined
    }
    undefined
                                                       #line 704
    undefined
    return  True
    undefined
    undefinedundefinedundefinedundefinedundefinedundefinedundefinedundefined
}
undefined
undefined
undefined
                                                       #line 708

undefinedundefined
, , undefined
, , ok
undefined
undefined