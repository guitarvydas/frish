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

                                                       #line 1#line 2
# fvget and fvset assume that the forth object (word) is a set of contiguous slots, each 1 machine word wide⎩3⎭
#  these functions use direct integer offsets to access the fields of the fojbect, whereas in higher level languages⎩4⎭
#  we'd use class fields instead - todo: fix this in the future (or not? at what point is customization better than⎩5⎭
#  generalization?)                                    #line 6

def fvget (name):
    global State                                       #line 7

    fobjaddress =  _find(State.S.pop ())               #line 8
    return  State.RAM [ fobjaddress+ 1]                #line 9#line 10#line 11


def fvset (name,v):
    global State                                       #line 12

    fobjaddress =  _find(State.S.pop ())               #line 13

    namefieldaddress =  fobjaddress+ 1                 #line 14
    State.RAM [ namefieldaddress] =  v                 #line 15#line 16#line 17
                                                       #line 18

def doword ():
    global State                                       #line 19
    #⎩20⎭
    #Execute a colon-defined word using indirect threaded code interpretation.⎩21⎭
    #⎩22⎭
    #This function implements the inner interpreter for threaded code execution.⎩23⎭
    #Threaded code words store their definitions as arrays of code field addresses⎩24⎭
    #(CFAs) in the parameter field area (PFA) immediately following the word header.⎩25⎭
    #⎩26⎭
    #The execution model maintains two critical registers:⎩27⎭
    #⎩28⎭
    #1. IP (Instruction Pointer): References the current position within the⎩29⎭
    #   threaded code array being interpreted. Since threaded words may invoke⎩30⎭
    #   other threaded words, IP must be preserved in a reentrant manner via⎩31⎭
    #   the return stack on each invocation.⎩32⎭
    #⎩33⎭
    #2. W (Word Pointer): References the CFA of the currently executing primitive.⎩34⎭
    #   This global register serves an analogous function to 'self' in object-oriented⎩35⎭
    #   languages, enabling subroutines to access word header fields through fixed⎩36⎭
    #   offsets from the CFA.⎩37⎭
    #⎩38⎭
    #Optimization rationale: W is positioned to reference the CFA rather than the⎩39⎭
    #word header base. This design eliminates offset arithmetic for CFA access—the⎩40⎭
    #most frequent header operation—at the cost of requiring offset adjustments⎩41⎭
    #for other header fields (NFA: W-2, flags: W-1, PFA: W+1). This represents a⎩42⎭
    #deliberate trade-off favoring the common case.⎩43⎭
    #⎩44⎭
    #The inner interpreter loop performs the following operations:⎩45⎭
    #- Fetch the next CFA from RAM[IP] into W (performing the first indirection)⎩46⎭
    #- Increment IP to advance through the threaded code array⎩47⎭
    #- Execute the primitive via RAM[W]() (performing the second indirection)⎩48⎭
    #⎩49⎭
    #By caching the dereferenced CFA in W, we amortize the cost of double⎩50⎭
    #indirection: both primitive execution and header field access within⎩51⎭
    #subroutines utilize the same cached reference, avoiding redundant⎩52⎭
    #dereferences. This is functionally equivalent to parameter passing in⎩53⎭
    #object-oriented method invocation, but eliminates the overhead of⎩54⎭
    #explicitly passing 'self' to each primitive.⎩55⎭
    #⎩56⎭
    #Note: W's state is only defined during primitive execution (within RAM[W]()).⎩57⎭
    #Between loop iterations, W may reference a stale CFA, but this is⎩58⎭
    #architecturally sound since W is unconditionally updated before each⎩59⎭
    #primitive invocation.⎩60⎭
    #                                                  #line 61#line 62
    State.R.append ( State.IP)                         #line 63
    State.IP =  State.W+ 1                             #line 64
    while ( -1!= State.RAM [ State.IP]):               #line 65
        State.W =  State.RAM [ State.IP]               #line 66
        State.IP =  State.IP+ 1                        #line 67
        State.RAM [ State.W]()                         #line 68#line 69
    State.IP = State.R.pop ()                          #line 70#line 71#line 72
                                                       #line 73

def notfound (word):
    global State                                       #line 74

    State.S.clear()                                    #line 75

    State.R.clear()                                    #line 76
    print ( word, end="")                              #line 77
    print ( "?", end="")                               #line 78
    print ()                                           #line 79#line 80#line 81


def exec (xt):
    global State                                       #line 82
    # found and compiling and immediate                #line 83
    State.W =  xt                                      #line 84
    State.IP =  -1
    # Dummy to hold place in return stack.             #line 85
    State.RAM [ xt]()
    # Execute code.                                    #line 86#line 87#line 88


def compile_word (xt):
    global State                                       #line 89
    # found and not compiling                          #line 90
    State.W =  xt                                      #line 91
    State.IP =  -1
    # Dummy to hold place in return stack.             #line 92
    State.RAM [ xt]()
    # Execute code.                                    #line 93#line 94#line 95


def pushasinteger (word):
    global State                                       #line 96
    State.S.push (int ( word))                         #line 97#line 98#line 99


def pushasfloat (word):
    global State                                       #line 100
    State.S.push (float ( word))                       #line 101#line 102#line 103


def compileinteger (word):
    global State                                       #line 104
    pushasinteger( word)                               #line 105
    literalize()                                       #line 106#line 107#line 108


def compilefloat (word):
    global State                                       #line 109
    pushasfloat( word)                                 #line 110
    literalize()                                       #line 111#line 112#line 113


def code (name,flags,does):
    global State                                       #line 114
    # Add new word to RAM dictionary. We create a word (Forth "object") in RAM with 5 fields and extend the⎩115⎭
    #      the dictionary by linking back to the head of the dictionary list #line 116
    x =  len( State.RAM)                               #line 117#line 118

    State.RAM.append ( State.LAST)
    # (LFA) link to previous word in dictionary list   #line 119

    State.RAM.append ( name)
    # (NFA) name of word                               #line 120

    State.RAM.append ( flags)
    #       0 = normal word, 1 = immediate word        #line 121

    State.RAM.append ( does)
    # (CFA) function pointer that points to code that executes the word #line 122#line 123
    State.LAST =  x
    # LAST is the pointer to the head of the dictionary list, set it to point to⎩124⎭
    #                                      this new word #line 125#line 126#line 127


def literalize ():
    global State                                       #line 128
    # Compile literal into definition.                 #line 129

    State.RAM.append ( _find( "(literal)"))
    ## Compile address of doliteral.                   #line 130

    State.RAM.append (State.S.pop ())
    # # Compile literal value.                         #line 131#line 132#line 133


def ok ():
    global State                                       #line 134
    # ( --) Interaction loop -- REPL                   #line 135

    blank =  32                                        #line 136
    while  True:                                       #line 137

        State.BUFF = input("OK ")
        State.BUFP = 0
                                                       #line 138
        while not (State.BUFP >= len(State.BUFF)):     #line 139
            xinterpret()                               #line 140#line 141#line 142#line 143#line 144


def doconst ():
    global State
    # method for const                                 #line 145

    parameter =  State.RAM [ State.W+ 1]               #line 146
    State.S.push ( parameter)                          #line 147#line 148#line 149
                                                       #line 150

def docreate ():
    global State                                       #line 151

    parameterAddress =  len( State.RAM)+ 4             #line 152
    State.S.push ( parameterAddress)                   #line 153#line 154


def create (name):
    global State                                       #line 155

    normal =  0                                        #line 156
    code( name, normal, docreate)                      #line 157#line 158


def xcreate ():
    global State                                       #line 159#line 160
    State.S.push (( 32))                               #line 161
    xword()                                            #line 162

    name = State.S.pop ()                              #line 163
    create( name)                                      #line 164#line 165#line 166
code("create",0,  xcreate)


def comma (value):
    global State                                       #line 167

    State.RAM.append ( value)                          #line 168#line 169#line 170


def fvar (name,value):
    global State                                       #line 171
    create( name)                                      #line 172
    comma( value)                                      #line 173#line 174#line 175


def _find (name):
    global State                                       #line 176
    # "( name -- cfa|0) Find CFA of word name."        #line 177

    x =  State.LAST                                    #line 178
    while ( x >=  0):                                  #line 179
        # ## print(f"-- {x} : {RAM[x]}, {RAM[x + 1]}")  # Debug. #line 180
        if ( name ==  State.RAM [ x+ 1]):
            # # Match!                                 #line 181
            return  x+ 3                               #line 182
        else:                                          #line 183
            x =  State.RAM [ x]
            # # Get next link.                         #line 184#line 185#line 186
    return  0
    # # Nothing found.                                 #line 187#line 188#line 189


def debugok ():
    global State                                       #line 190
    # ( --) Interaction loop -- REPL                   #line 191

    blank =  32                                        #line 192

    State.BUFF = "7 ."
    State.BUFP = 0
                                                       #line 193
    while not (State.BUFP >= len(State.BUFF)):         #line 194
        if ( xinterpret()):                            #line 195
            print ( " ok", end="")                     #line 196
            print ()                                   #line 197#line 198
        print ( State.BUFP, end="")
        print ( " -- ", end="")
        print ( State.BUFF, end="")
        print ()                                       #line 199
        xdots()                                        #line 200#line 201
    print ( State.BUFP, end="")
    print ( " == ", end="")
    print ( State.BUFF, end="")
    print ()                                           #line 202
    xdot()                                             #line 203
    xdots()                                            #line 204#line 205#line 206
                                                       #line 207#line 208

def xdrop ():
    global State                                       #line 209
    # ( a -- )                                         #line 210
    State.S.pop ()                                     #line 211#line 212#line 213
code("drop",0,  xdrop)


def xdup ():
    global State                                       #line 214
    # ( a -- a a )                                     #line 215

    A = State.S.pop ()                                 #line 216
    State.S.push ( A)                                  #line 217
    State.S.push ( A)                                  #line 218#line 219#line 220
code("dup",0,  xdup)


def xnegate ():
    global State                                       #line 221
    # ( n -- (-n) )                                    #line 222

    n = State.S.pop ()                                 #line 223
    State.S.push ( -n)                                 #line 224#line 225#line 226
code("negate",0,  xnegate)


def xemit ():
    global State                                       #line 227
    # ( c -- ) emit specified character                #line 228

    c = State.S.pop ()                                 #line 229
    print (chr (int ( c)), end="")                     #line 230#line 231#line 232
code("emit",0,  xemit)


def xcr ():
    global State
    print ()                                           #line 233
code("cr",0,  xcr)


def xdot ():
    global State
    # ( n --) Print TOS
    print (State.S.pop (), end="")
    print ()                                           #line 234
code(".",0,  xdot)


def xdots ():
    global State
    # ( --) Print stack contents
    print (State.S, end="")
    print ()                                           #line 235#line 236
code(".s",0,  xdots)


def xadd ():
    global State                                       #line 237
    # ( a b -- sum)                                    #line 238

    B = State.S.pop ()                                 #line 239

    A = State.S.pop ()                                 #line 240
    State.S.push ( A+ B)                               #line 241#line 242#line 243
code("+",0,  xadd)


def xmul ():
    global State                                       #line 244
    # ( a b -- product )                               #line 245

    B = State.S.pop ()                                 #line 246

    A = State.S.pop ()                                 #line 247
    State.S.push ( A* B)                               #line 248#line 249#line 250
code("*",0,  xmul)


def xeq ():
    global State                                       #line 251
    # ( a b -- bool )                                  #line 252

    B = State.S.pop ()                                 #line 253

    A = State.S.pop ()                                 #line 254
    State.S.push ( A ==  B)                            #line 255#line 256#line 257
code("=",0,  xeq)


def xlt ():
    global State                                       #line 258
    # ( a b -- bool )                                  #line 259

    B = State.S.pop ()                                 #line 260

    A = State.S.pop ()                                 #line 261
    State.S.push ( A <  B)                             #line 262#line 263#line 264
code("<",0,  xlt)


def xgt ():
    global State                                       #line 265
    # ( a b -- bool )                                  #line 266

    B = State.S.pop ()                                 #line 267

    A = State.S.pop ()                                 #line 268
    State.S.push ( A >  B)                             #line 269#line 270#line 271
code(">",0,  xgt)


def xeq0 ():
    global State                                       #line 272
    # ( a -- bool )                                    #line 273

    a = State.S.pop ()                                 #line 274
    State.S.push ( a ==  0)                            #line 275#line 276#line 277
code("0=",0,  xeq0)


def x0lt ():
    global State                                       #line 278
    # ( a -- bool )                                    #line 279

    a = State.S.pop ()                                 #line 280
    State.S.push ( 0 <  a)                             #line 281#line 282#line 283
code("0<",0,  x0lt)


def x0gt ():
    global State                                       #line 284
    # ( a -- bool )                                    #line 285

    a = State.S.pop ()                                 #line 286
    State.S.push ( 0 >  a)                             #line 287#line 288#line 289
code("0>",0,  x0gt)


def xnot ():
    global State                                       #line 290
    # ( a -- bool )                                    #line 291

    a = State.S.pop ()                                 #line 292
    State.S.push (not  a)                              #line 293#line 294#line 295
code("not",0,  xnot)


def xand ():
    global State                                       #line 296
    # ( a b -- bool )                                  #line 297

    b = State.S.pop ()                                 #line 298

    a = State.S.pop ()                                 #line 299
    State.S.push ( a and  b)                           #line 300#line 301#line 302
code("and",0,  xand)


def xor ():
    global State                                       #line 303
    # ( a b -- bool )                                  #line 304

    b = State.S.pop ()                                 #line 305

    a = State.S.pop ()                                 #line 306
    State.S.push ( a or  b)                            #line 307#line 308#line 309
code("or",0,  xor)


def xStoR ():
    global State                                       #line 310
    # ( a --  )                                        #line 311

    a = State.S.pop ()                                 #line 312
    State.R.append ( a)                                #line 313#line 314#line 315
code(">r",0,  xStoR)


def xRtoS ():
    global State                                       #line 316
    # ( -- x )                                         #line 317

    x = State.R.pop ()                                 #line 318
    State.S.push ( x)                                  #line 319#line 320#line 321
code("r>",0,  xRtoS)


def xi ():
    global State                                       #line 322
    # ( -- i ) get current loop index from R stack     #line 323

    i = State.R [-1]                                   #line 324
    State.S.push ( i)                                  #line 325#line 326#line 327
code("i",0,  xi)


def xiquote ():
    global State                                       #line 328
    # ( -- i ) get outer loop limit from R stack       #line 329

    i = State.R [-2]                                   #line 330
    State.S.push ( i)                                  #line 331#line 332#line 333
code("i'",0,  xiquote)


def xj ():
    global State                                       #line 334
    # ( -- j ) get outer loop index from R stack       #line 335

    j = State.R [-3]                                   #line 336
    State.S.push ( j)                                  #line 337#line 338#line 339
code("j",0,  xj)


def xswap ():
    global State                                       #line 340
    # ( a b -- b a)                                    #line 341
    x = Stack [-1]
    Stack [-1] = Stack [-2]
    Stack [-2] = x                                     #line 342#line 346
code("swap",0,  xswap)


def xsub ():
    global State                                       #line 347
    # ( a b -- diff)                                   #line 348

    B = State.S.pop ()                                 #line 349

    A = State.S.pop ()                                 #line 350
    State.S.push ( A- B)                               #line 351#line 352
code("-",0,  xsub)


def xdiv ():
    global State                                       #line 353
    # ( a b -- div)                                    #line 354
    xswap()                                            #line 355

    B = State.S.pop ()                                 #line 356

    A = State.S.pop ()                                 #line 357
    State.S.push ( B [A])                              #line 358#line 359#line 360
code("/",0,  xdiv)


def xword ():
    global State                                       #line 361
    # (char -- string) Read in string delimited by char #line 362

    wanted = chr(State.S.pop ())                       #line 363

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
                                                       #line 364#line 365#line 366
code("word",0,  xword)

# Example of state-smart word, which Brodie sez not to do. Sorry, Leo... #line 367
# This sin allows it to be used the same way compiling or interactive. #line 368

def xquote ():
    global State                                       #line 369
    # ( -- string) Read up to closing dquote, push to stack #line 370
    # A string in Forth begins with the word " (followed by a space) then all characters up to the next " #line 371
    # E.G. " abc"                                      #line 372#line 373
    State.S.push (( 34))                               #line 374
    xword()                                            #line 375
    if State.compiling:                                #line 376
        literalize()                                   #line 377#line 378#line 379#line 380
code("'",0,  xquote)


def xdotquote ():
    global State                                       #line 381
    # ( --) Print string.                              #line 382
    xquote()                                           #line 383
    print (State.S.pop (), end="")                     #line 384#line 385#line 386
code(".'",0,  xdotquote)
                                                       #line 387#line 388

def xdoliteral ():
    global State                                       #line 389
    #⎩390⎭
    # Inside definitions only, pushes compiled literal to stack ⎩391⎭
    #    ⎩392⎭
    #     Certain Forth words are only applicable inside compiled sequences of subroutines ⎩393⎭
    #     Literals are handled in different ways when interpreted when in the REPL vs⎩394⎭
    #     compiled into sequences of subrs ⎩395⎭
    #     In the REPL, when we encounter a literal, we simply push it onto the stack ⎩396⎭
    #     In the compiler, though, we have to create an instruction that pushes ⎩397⎭
    #       the literal onto the stack. ⎩398⎭
    #       Compiled code doesn't do what the REPL does, we have to hard-wire and ⎩399⎭
    #       bake in code that pushes the literal when the time comes to run the sequence. ⎩400⎭
    #⎩401⎭
    #     This word - "(literal)" - is a simple case and one could actually type this ⎩402⎭
    #       instruction into the REPL, but, that would be redundant.  Other kinds of words, ⎩403⎭
    #       e.g. some control-flow words, tend to be messier and the code below only handles ⎩404⎭
    #       the compiled aspects and ignores the REPL aspects ⎩405⎭
    #⎩406⎭
    #     "IP" is the current word index in a sequence of words being compiled. ⎩407⎭
    #                                                  #line 408#line 409
    State.S.push ( State.RAM [( State.IP)])            #line 410
    State.IP =  State.IP+ 1
    # move past this item (the literal) - we're done with it #line 411#line 412#line 413
code("(literal)",0,  xdoliteral)


def xbranch ():
    global State                                       #line 414
    # This instruction appears only inside subroutine sequences, jump to address in next cell #line 415
    # This instruction is inserted into a subr sequence when compiling control-flow words, like "else" see below) #line 416
    State.IP =  State.RAM [ State.IP]                  #line 417
    # normally, we just execute an instruction then move the IP sequentially forward by 1 unit, i.e. IP ⇐ IP + 1 #line 418
    #   in this case, though, we explicitly change the IP to some other value and don't just increment it #line 419#line 420#line 421
code("branch",0,  xbranch)


def x0branch ():
    global State                                       #line 422
    # This instruction appears only inside subroutine sequences, jump on false to address in next cell #line 423

    test = bool (State.S.pop ())                       #line 424
    if ( test):                                        #line 425
        State.IP =  State.IP+ 1                        #line 426
    else:                                              #line 427
        State.IP =  State.RAM [ State.IP]              #line 428#line 429#line 430#line 431
code("0branch",0,  x0branch)
                                                       #line 432
# "immediate" words are fully operational even when in compile mode. Some (not all) of these words are meant to⎩433⎭
#    work /only/ in compile mode. At the REPL prompt ("interpret" mode), they produce unwanted results.⎩434⎭
#  immediate words: xif, xelse, xthen, xquote, xcomment, xsemi⎩435⎭
#  immediate words that only have meaning in compile mode: xif, xelse, xthen, xsemi⎩436⎭
#                                                      #line 437#line 438#line 439
# IF, ELSE and THEN are "immediate" words - they should only be used inside of ":" (colon compiler) #line 440#line 441
# see diagram compiling-IF-THEN.drawio.png             #line 442

def xif ():
    global State                                       #line 443
    State.compiling = False
    # This instruction appears only inside subroutine sequences, ( f -- ) compile if test and branchFalse #line 444
    # Step. 1: generate conditional branch to yet-unknown target1 #line 445

    branchFalseAddress =  _find( "0branch")            #line 446

    State.RAM.append ( branchFalseAddress)
    # insert branch-if-false opcode (word)             #line 447
    State.R.append (len (Stack.RAM))
    # target1 onto r-stack as memo for later fixup     #line 448#line 449

    State.RAM.append (( -1))
    # branch target will be fixed up later             #line 450
    # Step. 2: generate code for true branch - return to compiler which will compile the following words #line 451
    # THEN or ELSE will do the fixup of (-1)           #line 452#line 453#line 454
code("if",0,  xif)

# see diagram compiling-IF-ELSE-THEN.drawio.png        #line 455

def xelse ():
    global State                                       #line 456
    # Step. 1: fixup target1 from IF-true, retrieving memo from R-stack #line 457

    target1 = State.R.pop ()                           #line 458
    State.RAM [ target1] = len (Stack.RAM)             #line 459
    # Step. 2: generate unconditional branch for preceding IF, creating new memo for target2 on R-stack #line 460

    brAddress =  _find( "branch")                      #line 461
    State.R.append (len (Stack.RAM))
    # target2 address on R-stack as memo for later fixup #line 462

    target2 =  -1                                      #line 463

    State.RAM.append ( target2)
    # branch target will be fixed up later             #line 464
    # Step. 3: generate code for false branch - return to compiler which will compile the following words #line 465
    # THEN will do the fixup of target2                #line 466#line 467#line 468
code("else", 1, xelse)

# see diagrams compiling-IF-THEN.drawio.png and compiling-IF-ELSE-THEN.drawio.png #line 469

def xthen ():
    global State                                       #line 470
    # Step. 1: fixup target (from IF or from ELSE, above), retrieving memo from R-stack #line 471

    target = State.R.pop ()                            #line 472
    State.RAM [ target] = len (Stack.RAM)              #line 473#line 474#line 475
code("then", 1, xthen)


def x_do ():
    global State                                       #line 476
    # ( limit index --) Puts limit and index on return stack. #line 477
    xswap()                                            #line 478

    index = State.S.pop ()                             #line 479

    limit = State.S.pop ()                             #line 480
    State.R.append ( index)                            #line 481
    State.R.append ( limit)                            #line 482#line 483#line 484
code("(do)",0,  x_do)


def xdo ():
    global State                                       #line 485
    # (  limit index --) Begin counted loop.           #line 486

    State.RAM.append ( _find( "(do)"))
    # Push do loop handler.                            #line 487
    State.R.append (len (Stack.RAM))
    # Push address to jump back to.                    #line 488#line 489#line 490
code("xdo", 1, xdo)


def x_loop ():
    global State                                       #line 491
    # (  -- f) Determine if loop is done.              #line 492

    index = State.R.pop ()                             #line 493

    limit = State.R.pop ()                             #line 494#line 495
    State.S.push ((( index >= ( limit))))              #line 496
    if ((( index >= ( limit)))):
        # clean up rstack if index >= limit            #line 497
        State.R.pop ()                                 #line 498
        State.R.pop ()                                 #line 499#line 500#line 501#line 502
code("(loop)",0,  x_loop)


def xploop ():
    global State                                       #line 503
    # ( --) Close counted loop.                        #line 504

    State.RAM.append ( _find( "(loop)"))
    # Compile in loop test.                            #line 505

    State.RAM.append ( _find( "0branch"))
    # Compile in branch check.                         #line 506

    State.RAM.append (State.R.pop ())
    # Address to jump back to.                         #line 507#line 508#line 509
code("+loop", 1, xploop)


def xloop ():
    global State                                       #line 510
    # (  --) Close counted loop.                       #line 511
    State.S.push ( 1)                                  #line 512
    literalize()
    # Default loop increment for x_loop.               #line 513

    State.RAM.append ( _find( "(loop)"))
    # Compile in loop test.                            #line 514

    State.RAM.append ( _find( "0branch"))
    # Compile in branch check.                         #line 515

    State.RAM.append (State.R.pop ())
    # Address to jump back to.                         #line 516#line 517#line 518
code("xloop", 1, xloop)


def xbegin ():
    global State                                       #line 519
    State.R.append (len (Stack.RAM))
    # ( --) Start indefinite loop.                     #line 520#line 521#line 522
code("begin", 1, xbegin)


def xuntil ():
    global State                                       #line 523
    # (  f --) Close indefinite loop with test.        #line 524

    State.RAM.append ( _find( "0branch"))
    # Expects result of test on stack.                 #line 525

    State.RAM.append (State.R.pop ())
    # Address to jump back to.                         #line 526#line 527#line 528
code("until", 1, xuntil)
                                                       #line 529#line 530
#  "... 123 constant K ..."                            #line 531
#  at interpretation time: 123 is on the Stack, we have consumed "constant" from BUFF, BUFF now contains "K ..." #line 532
#  invoke 'word' which parses "K" and pushed it. The stack becomes [... 123 "K"] #line 533
#  pop "K", pop 123, create a new word called 'K' with its PFA set to 123 and its CFA set to a subr that⎩534⎭
#     gets 123 from its PFA and pushes it onto the stack #line 535

def xconst ():
    global State                                       #line 536
    #  get next word - the name - from BUFF            #line 537#line 538
    State.S.push (( 32))                               #line 539
    xword()                                            #line 540
    #  stack is now: ( NNNN name -- )                  #line 541

    name = State.S.pop ()                              #line 542

    value = State.S.pop ()                             #line 543#line 544

    fobj =  code( name,( 0), doconst)                  #line 545

    State.RAM.append ( value)                          #line 546#line 547#line 548
code("const",0,  xconst)


def xcomma ():
    global State                                       #line 549
    comma(State.S.pop ())                              #line 550#line 551#line 552
code(",",0,  xcomma)


def xvar ():
    global State                                       #line 553#line 554
    State.S.push (( 32))                               #line 555
    xword()                                            #line 556

    name = State.S.pop ()                              #line 557

    value = State.S.pop ()                             #line 558
    fvar( name, value)                                 #line 559#line 560#line 561
code("variable",0,  xvar)


def xdump ():
    global State                                       #line 562

    n = int (State.S.pop ())                           #line 563

    start = int (State.S.pop ())                       #line 564
    print ( "----------------------------------------------------------------", end="")#line 565

    a =  start                                         #line 566
    while ( a <  start+( min( n,( len( State.RAM)- start)))):#line 567
        print ( a, end="")                             #line 568
        print ( ": ", end="")                          #line 569
        print ( State.RAM [ a], end="")                #line 570
        print ()                                       #line 571

        a =  a+ 1                                      #line 572#line 573#line 574#line 575
code("dump",0,  xdump)


def xstore ():
    global State                                       #line 576

    b = State.S.pop ()                                 #line 577

    a = State.S.pop ()                                 #line 578
    State.RAM [ b] =  a                                #line 579#line 580#line 581
code("!",0,  xstore)


def xbye ():
    global State
    # ( --) Leave interpreter

    raise SystemExit                                   #line 582#line 583
code("bye",0,  xbye)
                                                       #line 584

def xfind ():
    global State                                       #line 585
    # "( name | -- (name 0)|(xt 1)|(xt -1)) Search for word name." #line 586
    # 3 possible results: 1. (name 0) if not found, 2. (xt 1) if found and word is immediate, 3. (xt -1) if found and word is normal #line 587
    State.S.push ( 32)                                 #line 588
    xword()                                            #line 589

    found =  _find(State.S[-1])                        #line 590
    if ( 0 ==  found):                                 #line 591
        State.S.push ( 0)                              #line 592
    else:                                              #line 593
        State.S.pop ()
        # # Get rid of name on stack.                  #line 594
        State.S.push ( found)                          #line 595

        immediate =  -1                                #line 596
        if ( State.RAM [State.S[-1]- 1] &  1):
            immediate =  1                             #line 597
        State.S.push ( immediate)                      #line 598#line 599#line 600#line 601
code("find",0,  xfind)


def xtick ():
    global State                                       #line 602
    # "( name -- xt|-1) Search for execution token of word name." #line 603
    State.S.push ( 32)                                 #line 604
    xword()                                            #line 605

    name = State.S.pop ()                              #line 606

    found =  _find( name)                              #line 607
    State.S.push ( found)                              #line 608#line 609#line 610
code("'",0,  xtick)


def xnone ():
    global State                                       #line 611

    State.S.append (None)                              #line 612#line 613#line 614
code("None",0,  xnone)


def xwords ():
    global State                                       #line 615
    # print words in dictionary                        #line 616

    x =  State.LAST                                    #line 617
    while ( x >  -1):                                  #line 618
        print ( State.RAM [ x+ 1], end="")             #line 619
        print ( " ", end="")                           #line 620#line 621
    print ()                                           #line 622#line 623#line 624
code("words",0,  xwords)
                                                       #line 625

def xexecute ():
    global State                                       #line 626
    # invoke given word                                #line 627

    wordAddress = State.S.pop ()                       #line 628
    wordAddress()                                      #line 629#line 630#line 631
code("execute",0,  xexecute)
                                                       #line 632

def xcolon ():
    global State                                       #line 633
    # ( name | --) Start compilation.                  #line 634#line 635
    State.S.push (( 32))                               #line 636
    xword()                                            #line 637

    name = State.S.pop ()                              #line 638
    code( name, 0, doword)                             #line 639
    State.compiling = True                             #line 640#line 641#line 642
code(":",0,  xcolon)


def xsemi ():
    global State                                       #line 643
    # ( --) Finish definition.                         #line 644#line 645

    State.RAM.append ( -1)
    # Marker for end of definition.                    #line 646
    State.compiling = False                            #line 647#line 648#line 649
code(";", 1, xsemi)


def xinterpret ():
    global State                                       #line 650
    # ( string --) Execute word.                       #line 651#line 652
    xfind()                                            #line 653
    # 3 possible results from xfind:⎩654⎭
    #        1. (name 0) if not found,⎩655⎭
    #	2. (xt 1) if found and word is immediate,⎩656⎭
    #	3. (xt -1) if found and word is normal           #line 657

    result = State.S.pop ()                            #line 658

    item = State.S.pop ()                              #line 659#line 660#line 661#line 662
    if ((((( result == ( 1))) or ((( result == ( -1))))))):#line 663
        if (State.compiling):                          #line 664
            if ((( result == ( 1)))):                  #line 665
                exec( item)                            #line 666
            else:                                      #line 667
                compileword( item)                     #line 668#line 669#line 670
        else:                                          #line 671
            exec( item)                                #line 672#line 673#line 674
    else:                                              #line 675
        if (State.compiling):                          #line 676
            if (re.match(r"^-?\d*$",  item)):          #line 677
                compileinteger( item)                  #line 678
            else:                                      #line 679
                if (re.match(r"^-?d*\.?\d*$",  item)): #line 680
                    compilefloat( item)                #line 681
                else:                                  #line 682
                    returnFalse()                      #line 683#line 684#line 685#line 686#line 687
        else:                                          #line 688
            if (re.match(r"^-?\d*$",  item)):          #line 689
                pushasinteger( item)                   #line 690
            else:                                      #line 691
                if (re.match(r"^-?d*\.?\d*$",  item)): #line 692
                    pushasfloat( item)                 #line 693
                else:                                  #line 694
                    returnFalse()                      #line 695#line 696#line 697#line 698#line 699#line 700#line 701#line 702#line 703
    return  True                                       #line 704#line 705#line 706
code("interpret",0,  xinterpret)
                                                       #line 707#line 708
ok()                                                   #line 709#line 710