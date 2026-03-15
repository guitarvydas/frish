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


def code (name,flags,does):
    global State                                       #line 1
    # Add new word to RAM dictionary. We create a word (Forth "object") in RAM with 5 fields and extend the⎩2⎭
    #      the dictionary by linking back to the head of the dictionary list #line 3
    x =  len( State.RAM)                               #line 4#line 5

    State.RAM.append ( State.LAST)
    # (LFA) link to previous word in dictionary list   #line 6

    State.RAM.append ( name)
    # (NFA) name of word                               #line 7

    State.RAM.append ( flags)
    #       0 = normal word, 1 = immediate word        #line 8

    State.RAM.append ( does)
    # (CFA) function pointer that points to code that executes the word #line 9#line 10
    State.LAST =  x
    # LAST is the pointer to the head of the dictionary list, set it to point to⎩11⎭
    #                                      this new word #line 12#line 13#line 14

def xdrop ():
    global State                                       #line 15
    # ( a -- )                                         #line 16
    State.S.pop ()                                     #line 17#line 18#line 19
code("drop",0,  xdrop)

def xdup ():
    global State                                       #line 20
    # ( a -- a a )                                     #line 21

    A = State.S.pop ()                                 #line 22
    State.S.push ( A)                                  #line 23
    State.S.push ( A)                                  #line 24#line 25#line 26
code("dup",0,  xdup)

def xnegate ():
    global State                                       #line 27
    # ( n -- (-n) )                                    #line 28

    n = State.S.pop ()                                 #line 29
    State.S.push ( -n)                                 #line 30#line 31#line 32
code("negate",0,  xnegate)

def xemit ():
    global State                                       #line 33
    # ( c -- ) emit specified character                #line 34

    c = State.S.pop ()                                 #line 35
    print (chr (int ( c)), end="")                     #line 36#line 37#line 38
code("emit",0,  xemit)

def xcr ():
    global State
    print ()                                           #line 39
code("cr",0,  xcr)

def xdot ():
    global State
    # ( n --) Print TOS
    print (State.S.pop (), end="")
    print ()                                           #line 40
code(".",0,  xdot)

def xdots ():
    global State
    # ( --) Print stack contents
    print (State.S, end="")
    print ()                                           #line 41#line 42
code(".s",0,  xdots)

def xadd ():
    global State                                       #line 43
    # ( a b -- sum)                                    #line 44

    B = State.S.pop ()                                 #line 45

    A = State.S.pop ()                                 #line 46
    State.S.push ( A+ B)                               #line 47#line 48#line 49
code("+",0,  xadd)

def xmul ():
    global State                                       #line 50
    # ( a b -- product )                               #line 51

    B = State.S.pop ()                                 #line 52

    A = State.S.pop ()                                 #line 53
    State.S.push ( A* B)                               #line 54#line 55#line 56
code("*",0,  xmul)

def xeq ():
    global State                                       #line 57
    # ( a b -- bool )                                  #line 58

    B = State.S.pop ()                                 #line 59

    A = State.S.pop ()                                 #line 60
    State.S.push ( A ==  B)                            #line 61#line 62#line 63
code("=",0,  xeq)

def xlt ():
    global State                                       #line 64
    # ( a b -- bool )                                  #line 65

    B = State.S.pop ()                                 #line 66

    A = State.S.pop ()                                 #line 67
    State.S.push ( A <  B)                             #line 68#line 69#line 70
code("<",0,  xlt)

def xgt ():
    global State                                       #line 71
    # ( a b -- bool )                                  #line 72

    B = State.S.pop ()                                 #line 73

    A = State.S.pop ()                                 #line 74
    State.S.push ( A >  B)                             #line 75#line 76#line 77
code(">",0,  xgt)

def xeq0 ():
    global State                                       #line 78
    # ( a -- bool )                                    #line 79

    a = State.S.pop ()                                 #line 80
    State.S.push ( a ==  0)                            #line 81#line 82#line 83
code("0=",0,  xeq0)

def x0lt ():
    global State                                       #line 84
    # ( a -- bool )                                    #line 85

    a = State.S.pop ()                                 #line 86
    State.S.push ( 0 <  a)                             #line 87#line 88#line 89
code("0<",0,  x0lt)

def x0gt ():
    global State                                       #line 90
    # ( a -- bool )                                    #line 91

    a = State.S.pop ()                                 #line 92
    State.S.push ( 0 >  a)                             #line 93#line 94#line 95
code("0>",0,  x0gt)

def xnot ():
    global State                                       #line 96
    # ( a -- bool )                                    #line 97

    a = State.S.pop ()                                 #line 98
    State.S.push (not  a)                              #line 99#line 100#line 101
code("not",0,  xnot)

def xand ():
    global State                                       #line 102
    # ( a b -- bool )                                  #line 103

    b = State.S.pop ()                                 #line 104

    a = State.S.pop ()                                 #line 105
    State.S.push ( a and  b)                           #line 106#line 107#line 108
code("and",0,  xand)

def xor ():
    global State                                       #line 109
    # ( a b -- bool )                                  #line 110

    b = State.S.pop ()                                 #line 111

    a = State.S.pop ()                                 #line 112
    State.S.push ( a or  b)                            #line 113#line 114#line 115
code("or",0,  xor)

def xStoR ():
    global State                                       #line 116
    # ( a --  )                                        #line 117

    a = State.S.pop ()                                 #line 118
    State.R.append ( a)                                #line 119#line 120#line 121
code(">r",0,  xStoR)

def xRtoS ():
    global State                                       #line 122
    # ( -- x )                                         #line 123

    x = State.R.pop ()                                 #line 124
    State.S.push ( x)                                  #line 125#line 126#line 127
code("r>",0,  xRtoS)

def xi ():
    global State                                       #line 128
    # ( -- i ) get current loop index from R stack     #line 129

    i = State.R [-1]                                   #line 130
    State.S.push ( i)                                  #line 131#line 132#line 133
code("i",0,  xi)

def xiquote ():
    global State                                       #line 134
    # ( -- i ) get outer loop limit from R stack       #line 135

    i = State.R [-2]                                   #line 136
    State.S.push ( i)                                  #line 137#line 138#line 139
code("i'",0,  xiquote)

def xj ():
    global State                                       #line 140
    # ( -- j ) get outer loop index from R stack       #line 141

    j = State.R [-3]                                   #line 142
    State.S.push ( j)                                  #line 143#line 144#line 145
code("j",0,  xj)

def xswap ():
    global State                                       #line 146
    # ( a b -- b a)                                    #line 147

    B = State.S.pop ()                                 #line 148

    A = State.S.pop ()                                 #line 149
    State.S.push ( B)                                  #line 150
    State.S.push ( A)                                  #line 151#line 152
code("swap",0,  xswap)

def xsub ():
    global State                                       #line 153
    # ( a b -- diff)                                   #line 154

    B = State.S.pop ()                                 #line 155

    A = State.S.pop ()                                 #line 156
    State.S.push ( A- B)                               #line 157#line 158
code("-",0,  xsub)

def xdiv ():
    global State                                       #line 159
    # ( a b -- div)                                    #line 160
    xswap()                                            #line 161

    B = State.S.pop ()                                 #line 162

    A = State.S.pop ()                                 #line 163
    State.S.push ( B [A])                              #line 164#line 165#line 166
code("/",0,  xdiv)

def xword ():
    global State                                       #line 167
    # (char -- string) Read in string delimited by char #line 168

    wanted = chr(State.S.pop ())                       #line 169

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
                                                       #line 170#line 171#line 172
code("word",0,  xword)

# Example of state-smart word, which Brodie sez not to do. Sorry, Leo... #line 173
# This sin allows it to be used the same way compiling or interactive. #line 174
def xquote ():
    global State                                       #line 175
    # ( -- string) Read up to closing dquote, push to stack #line 176
    # A string in Forth begins with the word " (followed by a space) then all characters up to the next " #line 177
    # E.G. " abc"                                      #line 178

    DQ =  34                                           #line 179
    State.S.push ( DQ)                                 #line 180
    xword()                                            #line 181
    if State.compiling:                                #line 182
        literalize()                                   #line 183#line 184#line 185#line 186
code("'",0,  xquote)

def xdotquote ():
    global State                                       #line 187
    # ( --) Print string.                              #line 188
    xquote()                                           #line 189
    print (State.S.pop (), end="")                     #line 190#line 191#line 192
code(".'",0,  xdotquote)
                                                       #line 193#line 194
def xdoliteral ():
    global State                                       #line 195
    #⎩196⎭
    # Inside definitions only, pushes compiled literal to stack ⎩197⎭
    #    ⎩198⎭
    #     Certain Forth words are only applicable inside compiled sequences of subroutines ⎩199⎭
    #     Literals are handled in different ways when interpreted when in the REPL vs⎩200⎭
    #     compiled into sequences of subrs ⎩201⎭
    #     In the REPL, when we encounter a literal, we simply push it onto the stack ⎩202⎭
    #     In the compiler, though, we have to create an instruction that pushes ⎩203⎭
    #       the literal onto the stack. ⎩204⎭
    #       Compiled code doesn't do what the REPL does, we have to hard-wire and ⎩205⎭
    #       bake in code that pushes the literal when the time comes to run the sequence. ⎩206⎭
    #⎩207⎭
    #     This word - "(literal)" - is a simple case and one could actually type this ⎩208⎭
    #       instruction into the REPL, but, that would be redundant.  Other kinds of words, ⎩209⎭
    #       e.g. some control-flow words, tend to be messier and the code below only handles ⎩210⎭
    #       the compiled aspects and ignores the REPL aspects ⎩211⎭
    #⎩212⎭
    #     "IP" is the current word index in a sequence of words being compiled. ⎩213⎭
    #                                                  #line 214

    lit =  State.RAM [ State.IP]                       #line 215
    State.S.push ( lit)                                #line 216
    State.IP =  State.IP+ 1
    # move past this item (the literal) - we're done with it #line 217#line 218#line 219
code("(literal)",0,  xdoliteral)

def literalize ():
    global State                                       #line 220
    # Compile literal into definition.                 #line 221

    State.RAM.append ( _find( "(literal)"))
    ## Compile address of doliteral.                   #line 222

    State.RAM.append (State.S.pop ())
    # # Compile literal value.                         #line 223#line 224#line 225

def xbranch ():
    global State                                       #line 226
    # This instruction appears only inside subroutine sequences, jump to address in next cell #line 227
    # This instruction is inserted into a subr sequence when compiling control-flow words, like "else" see below) #line 228
    State.IP =  State.RAM [ State.IP]                  #line 229
    # normally, we just execute an instruction then move the IP sequentially forward by 1 unit, i.e. IP ⇐ IP + 1 #line 230
    #   in this case, though, we explicitly change the IP to some other value and don't just increment it #line 231#line 232#line 233
code("branch",0,  xbranch)

def x0branch ():
    global State                                       #line 234
    # This instruction appears only inside subroutine sequences, jump on false to address in next cell #line 235

    test = bool (State.S.pop ())                       #line 236
    if ( test):                                        #line 237
        State.IP =  State.IP+ 1                        #line 238
    else:                                              #line 239
        State.IP =  State.RAM [ State.IP]              #line 240#line 241#line 242#line 243
code("0branch",0,  x0branch)
                                                       #line 244
# "immediate" words are fully operational even when in compile mode. Some (not all) of these words are meant to⎩245⎭
#    work /only/ in compile mode. At the REPL prompt ("interpret" mode), they produce unwanted results.⎩246⎭
#  immediate words: xif, xelse, xthen, xquote, xcomment, xsemi⎩247⎭
#  immediate words that only have meaning in compile mode: xif, xelse, xthen, xsemi⎩248⎭
#                                                      #line 249#line 250#line 251
# IF, ELSE and THEN are "immediate" words - they should only be used inside of ":" (colon compiler) #line 252#line 253
# see diagram compiling-IF-THEN.drawio.png`            #line 254
def xif ():
    global State                                       #line 255
    State.compiling = False
    # This instruction appears only inside subroutine sequences, ( f -- ) compile if test and branchFalse #line 256
    # Step. 1: generate conditional branch to yet-unknown target1 #line 257

    branchFalseAddress =  _find( "0branch")            #line 258

    State.RAM.append ( branchFalseAddress)
    # insert branch-if-false opcode (word)             #line 259
    State.R.append (len (Stack.RAM))
    # target1 onto r-stack as memo for later fixup     #line 260

    target1 =  -1                                      #line 261

    State.RAM.append ( target1)
    # branch target will be fixed up later             #line 262
    # Step. 2: generate code for true branch - return to compiler which will compile the following words #line 263
    # THEN or ELSE will do the fixup of target1        #line 264#line 265#line 266
code("if",0,  xif)

# see diagram `compiling-IF-ELSE-THEN.drawio.png`      #line 267
def xelse ():
    global State                                       #line 268
    # Step. 1: fixup target1 from IF-true, retrieving memo from R-stack #line 269

    target1 = State.R.pop ()                           #line 270
    State.RAM [ target1] = len (Stack.RAM)             #line 271
    # Step. 2: generate unconditional branch for preceding IF, creating new memo for target2 on R-stack #line 272

    brAddress =  _find( "branch")                      #line 273
    State.R.append (len (Stack.RAM))
    # target2 address on R-stack as memo for later fixup #line 274

    target2 =  -1                                      #line 275

    State.RAM.append ( target2)
    # branch target will be fixed up later             #line 276
    # Step. 3: generate code for false branch - return to compiler which will compile the following words #line 277
    # THEN will do the fixup of target2                #line 278#line 279#line 280
code("else", 1, xelse)

# see diagrams `compiling-IF-THEN.drawio.png` and `compiling-IF-ELSE-THEN.drawio.png` #line 281
def xthen ():
    global State                                       #line 282
    # Step. 1: fixup target (from IF or from ELSE, above), retrieving memo from R-stack #line 283

    target = State.R.pop ()                            #line 284
    State.RAM [ target] = len (Stack.RAM)              #line 285#line 286#line 287
code("then", 1, xthen)

def x_do ():
    global State                                       #line 288
    # ( limit index --) Puts limit and index on return stack. #line 289
    xswap()                                            #line 290

    index = State.S.pop ()                             #line 291

    limit = State.S.pop ()                             #line 292
    State.R.append ( index)                            #line 293
    State.R.append ( limit)                            #line 294#line 295#line 296
code("(do)",0,  x_do)

def xdo ():
    global State                                       #line 297
    # (  limit index --) Begin counted loop.           #line 298

    State.RAM.append ( _find( "(do)"))
    # Push do loop handler.                            #line 299
    State.R.append (len (Stack.RAM))
    # Push address to jump back to.                    #line 300#line 301#line 302
code("xdo", 1, xdo)

def x_loop ():
    global State                                       #line 303
    # (  -- f) Determine if loop is done.              #line 304

    index = State.R.pop ()                             #line 305

    limit = State.R.pop ()                             #line 306

    cond = ( index >=  limit)                          #line 307
    State.S.push ( cond)                               #line 308
    if ( cond):
        # clean up rstack if index >= limit            #line 309
        State.R.pop ()                                 #line 310
        State.R.pop ()                                 #line 311#line 312#line 313#line 314
code("(loop)",0,  x_loop)

def xploop ():
    global State                                       #line 315
    # ( --) Close counted loop.                        #line 316

    State.RAM.append ( _find( "(loop)"))
    # Compile in loop test.                            #line 317

    State.RAM.append ( _find( "0branch"))
    # Compile in branch check.                         #line 318

    State.RAM.append (State.R.pop ())
    # Address to jump back to.                         #line 319#line 320#line 321
code("+loop", 1, xploop)

def xloop ():
    global State                                       #line 322
    # (  --) Close counted loop.                       #line 323
    State.S.push ( 1)                                  #line 324
    literalize()
    # Default loop increment for x_loop.               #line 325

    State.RAM.append ( _find( "(loop)"))
    # Compile in loop test.                            #line 326

    State.RAM.append ( _find( "0branch"))
    # Compile in branch check.                         #line 327

    State.RAM.append (State.R.pop ())
    # Address to jump back to.                         #line 328#line 329#line 330
code("xloop", 1, xloop)

def xbegin ():
    global State                                       #line 331
    State.R.append (len (Stack.RAM))
    # ( --) Start indefinite loop.                     #line 332#line 333#line 334
code("begin", 1, xbegin)

def xuntil ():
    global State                                       #line 335
    # (  f --) Close indefinite loop with test.        #line 336

    State.RAM.append ( _find( "0branch"))
    # Expects result of test on stack.                 #line 337

    State.RAM.append (State.R.pop ())
    # Address to jump back to.                         #line 338#line 339#line 340
code("until", 1, xuntil)
                                                       #line 341#line 342
#  "... 123 constant K ..."                            #line 343
#  at interpretation time: 123 is on the Stack, we have consumed "constant" from BUFF, BUFF now contains "K ..." #line 344
#  invoke 'word' which parses "K" and pushed it. The stack becomes [... 123 "K"] #line 345
#  pop "K", pop 123, create a new word called 'K' with its PFA set to 123 and its CFA set to a subr that⎩346⎭
#     gets 123 from its PFA and pushes it onto the stack #line 347
def xconst ():
    global State                                       #line 348
    #  get next word - the name - from BUFF            #line 349

    blank =  32                                        #line 350
    State.S.push ( blank)                              #line 351
    xword()                                            #line 352
    #  stack is now: ( NNNN name -- )                  #line 353

    name = State.S.pop ()                              #line 354

    value = State.S.pop ()                             #line 355

    normal =  0                                        #line 356

    fobj =  code( name, normal, doconst)               #line 357

    State.RAM.append ( value)                          #line 358#line 359#line 360
code("const",0,  xconst)

def doconst ():
    global State
    # method for const                                 #line 361

    parameter =  State.RAM [ State.W+ 1]               #line 362
    State.S.push ( parameter)                          #line 363#line 364#line 365
                                                       #line 366
def docreate ():
    global State                                       #line 367

    parameterAddress =  len( State.RAM)+ 4             #line 368
    State.S.push ( parameterAddress)                   #line 369#line 370

def create (name):
    global State                                       #line 371

    normal =  0                                        #line 372
    code( name, normal, docreate)                      #line 373#line 374

def xcreate ():
    global State                                       #line 375

    blank =  32                                        #line 376
    State.S.push ( blank)                              #line 377
    xword()                                            #line 378

    name = State.S.pop ()                              #line 379
    create( name)                                      #line 380#line 381#line 382
code("create",0,  xcreate)

def comma (value):
    global State                                       #line 383

    State.RAM.append ( value)                          #line 384#line 385#line 386

def xcomma ():
    global State                                       #line 387
    comma(State.S.pop ())                              #line 388#line 389#line 390
code(",",0,  xcomma)

def fvar (name,value):
    global State                                       #line 391
    create( name)                                      #line 392
    comma( value)                                      #line 393#line 394#line 395

def xvar ():
    global State                                       #line 396

    blank =  32                                        #line 397
    State.S.push ( blank)                              #line 398
    xword()                                            #line 399

    name = State.S.pop ()                              #line 400

    value = State.S.pop ()                             #line 401
    fvar( name, value)                                 #line 402#line 403#line 404
code("variable",0,  xvar)

def xdump ():
    global State                                       #line 405

    n = int (State.S.pop ())                           #line 406

    start = int (State.S.pop ())                       #line 407
    print ( "----------------------------------------------------------------", end="")#line 408

    a =  start                                         #line 409
    while ( a <  start+( min( n,( len( State.RAM)- start)))):#line 410
        print ( a, end="")                             #line 411
        print ( ": ", end="")                          #line 412
        print ( State.RAM [ a], end="")                #line 413
        print ()                                       #line 414

        a =  a+ 1                                      #line 415#line 416#line 417#line 418
code("dump",0,  xdump)

def xstore ():
    global State                                       #line 419

    b = State.S.pop ()                                 #line 420

    a = State.S.pop ()                                 #line 421
    State.RAM [ b] =  a                                #line 422#line 423#line 424
code("!",0,  xstore)

def xbye ():
    global State
    # ( --) Leave interpreter

    raise SystemExit                                   #line 425#line 426
code("bye",0,  xbye)
                                                       #line 427
def _find (name):
    global State                                       #line 428
    # "( name -- cfa|0) Find CFA of word name."        #line 429

    x =  State.LAST                                    #line 430
    while ( x >=  0):                                  #line 431
        # ## print(f"-- {x} : {RAM[x]}, {RAM[x + 1]}")  # Debug. #line 432
        if ( name ==  State.RAM [ x+ 1]):
            # # Match!                                 #line 433
            return  x+ 3                               #line 434
        else:                                          #line 435
            x =  State.RAM [ x]
            # # Get next link.                         #line 436#line 437#line 438
    return  0
    # # Nothing found.                                 #line 439#line 440#line 441

def xfind ():
    global State                                       #line 442
    # "( name | -- (name 0)|(xt 1)|(xt -1)) Search for word name." #line 443
    # 3 possible results: 1. (name 0) if not found, 2. (xt 1) if found and word is immediate, 3. (xt -1) if found and word is normal #line 444
    State.S.push ( 32)                                 #line 445
    xword()                                            #line 446

    found =  _find(State.S[-1])                        #line 447
    if ( 0 ==  found):                                 #line 448
        State.S.push ( 0)                              #line 449
    else:                                              #line 450
        State.S.pop ()
        # # Get rid of name on stack.                  #line 451
        State.S.push ( found)                          #line 452

        immediate =  -1                                #line 453
        if ( State.RAM [State.S[-1]- 1] &  1):
            immediate =  1                             #line 454
        State.S.push ( immediate)                      #line 455#line 456#line 457#line 458
code("find",0,  xfind)

def xtick ():
    global State                                       #line 459
    # "( name -- xt|-1) Search for execution token of word name." #line 460
    State.S.push ( 32)                                 #line 461
    xword()                                            #line 462

    name = State.S.pop ()                              #line 463

    found =  _find( name)                              #line 464
    State.S.push ( found)                              #line 465#line 466#line 467
code("'",0,  xtick)

def xnone ():
    global State                                       #line 468

    State.S.append (None)                              #line 469#line 470#line 471
code("None",0,  xnone)

# fvget and fvset assume that the forth object (word) is a set of contiguous slots, each 1 machine word wide⎩472⎭
#  these functions use direct integer offsets to access the fields of the fojbect, whereas in higher level languages⎩473⎭
#  we'd use class fields instead - todo: fix this in the future (or not? at what point is customization better than⎩474⎭
#  generalization?)                                    #line 475
def fvget (name):
    global State                                       #line 476

    fobjaddress =  _find(State.S.pop ())               #line 477
    return  State.RAM [ fobjaddress+ 1]                #line 478#line 479#line 480

def fvset (name,v):
    global State                                       #line 481

    fobjaddress =  _find(State.S.pop ())               #line 482

    namefieldaddress =  fobjaddress+ 1                 #line 483
    State.RAM [ namefieldaddress] =  v                 #line 484#line 485#line 486
                                                       #line 487
def xwords ():
    global State                                       #line 488
    # print words in dictionary                        #line 489

    x =  State.LAST                                    #line 490
    while ( x >  -1):                                  #line 491
        print ( State.RAM [ x+ 1], end="")             #line 492
        print ( " ", end="")                           #line 493#line 494
    print ()                                           #line 495#line 496#line 497
code("words",0,  xwords)
                                                       #line 498
def xexecute ():
    global State                                       #line 499
    # invoke given word                                #line 500

    wordAddress = State.S.pop ()                       #line 501
    wordAddress()                                      #line 502#line 503#line 504
code("execute",0,  xexecute)
                                                       #line 505
def doword ():
    global State                                       #line 506
    #⎩507⎭
    #Execute a colon-defined word using indirect threaded code interpretation.⎩508⎭
    #⎩509⎭
    #This function implements the inner interpreter for threaded code execution.⎩510⎭
    #Threaded code words store their definitions as arrays of code field addresses⎩511⎭
    #(CFAs) in the parameter field area (PFA) immediately following the word header.⎩512⎭
    #⎩513⎭
    #The execution model maintains two critical registers:⎩514⎭
    #⎩515⎭
    #1. IP (Instruction Pointer): References the current position within the⎩516⎭
    #   threaded code array being interpreted. Since threaded words may invoke⎩517⎭
    #   other threaded words, IP must be preserved in a reentrant manner via⎩518⎭
    #   the return stack on each invocation.⎩519⎭
    #⎩520⎭
    #2. W (Word Pointer): References the CFA of the currently executing primitive.⎩521⎭
    #   This global register serves an analogous function to 'self in object-oriented⎩522⎭
    #   languages, enabling subroutines to access word header fields through fixed⎩523⎭
    #   offsets from the CFA.⎩524⎭
    #⎩525⎭
    #Optimization rationale: W is positioned to reference the CFA rather than the⎩526⎭
    #word header base. This design eliminates offset arithmetic for CFA access—the⎩527⎭
    #most frequent header operation—at the cost of requiring offset adjustments⎩528⎭
    #for other header fields (NFA: W-2, flags: W-1, PFA: W+1). This represents a⎩529⎭
    #deliberate trade-off favoring the common case.⎩530⎭
    #⎩531⎭
    #The inner interpreter loop performs the following operations:⎩532⎭
    #- Fetch the next CFA from RAM[IP] into W (performing the first indirection)⎩533⎭
    #- Increment IP to advance through the threaded code array⎩534⎭
    #- Execute the primitive via RAM[W]() (performing the second indirection)⎩535⎭
    #⎩536⎭
    #By caching the dereferenced CFA in W, we amortize the cost of double⎩537⎭
    #indirection: both primitive execution and header field access within⎩538⎭
    #subroutines utilize the same cached reference, avoiding redundant⎩539⎭
    #dereferences. This is functionally equivalent to parameter passing in⎩540⎭
    #object-oriented method invocation, but eliminates the overhead of⎩541⎭
    #explicitly passing 'self' to each primitive.⎩542⎭
    #⎩543⎭
    #Note: W's state is only defined during primitive execution (within RAM[W]()).⎩544⎭
    #Between loop iterations, W may reference a stale CFA, but this is⎩545⎭
    #architecturally sound since W is unconditionally updated before each⎩546⎭
    #primitive invocation.⎩547⎭
    #                                                  #line 548#line 549
    State.R.append ( State.IP)                         #line 550
    State.IP =  State.W+ 1                             #line 551
    while ( -1!= State.RAM [ State.IP]):               #line 552
        State.W =  State.RAM [ State.IP]               #line 553
        State.IP =  State.IP+ 1                        #line 554
        State.RAM [ State.W]()                         #line 555#line 556
    State.IP = State.R.pop ()                          #line 557#line 558#line 559

def xcolon ():
    global State                                       #line 560
    # ( name | --) Start compilation.                  #line 561

    blank =  32                                        #line 562
    State.S.push ( blank)                              #line 563
    xword()                                            #line 564

    name = State.S.pop ()                              #line 565
    code( name, 0, doword)                             #line 566
    State.compiling = True                             #line 567#line 568#line 569
code(":",0,  xcolon)

def xsemi ():
    global State                                       #line 570
    # ( --) Finish definition.                         #line 571#line 572

    State.RAM.append ( -1)
    # Marker for end of definition.                    #line 573
    State.compiling = False                            #line 574#line 575#line 576
code(";", 1, xsemi)

def notfound (word):
    global State                                       #line 577

    State.S.clear()                                    #line 578

    State.R.clear()                                    #line 579
    print ( word, end="")                              #line 580
    print ( "?", end="")                               #line 581
    print ()                                           #line 582#line 583#line 584

def exec (xt):
    global State                                       #line 585
    # found and compiling and immediate                #line 586
    State.W =  xt                                      #line 587
    State.IP =  -1
    # Dummy to hold place in return stack.             #line 588
    State.RAM [ xt]()
    # Execute code.                                    #line 589#line 590#line 591

def compile_word (xt):
    global State                                       #line 592
    # found and not compiling                          #line 593
    State.W =  xt                                      #line 594
    State.IP =  -1
    # Dummy to hold place in return stack.             #line 595
    State.RAM [ xt]()
    # Execute code.                                    #line 596#line 597#line 598

def pushasinteger (word):
    global State                                       #line 599
    State.S.push (int ( word))                         #line 600#line 601#line 602

def pushasfloat (word):
    global State                                       #line 603
    State.S.push (float ( word))                       #line 604#line 605#line 606

def compileinteger (word):
    global State                                       #line 607
    pushasinteger( word)                               #line 608
    literalize()                                       #line 609#line 610#line 611

def compilefloat (word):
    global State                                       #line 612
    pushasfloat( word)                                 #line 613
    literalize()                                       #line 614#line 615#line 616

def xinterpret ():
    global State                                       #line 617
    # ( string --) Execute word.                       #line 618#line 619
    xfind()                                            #line 620
    # 3 possible results from xfind:⎩621⎭
    #        1. (name 0) if not found,⎩622⎭
    #	2. (xt 1) if found and word is immediate,⎩623⎭
    #	3. (xt -1) if found and word is normal           #line 624

    result = State.S.pop ()

    foundimmediate = ( result ==  1)                   #line 625

    item = State.S.pop ()

    foundnormal = ( result ==  -1)                     #line 626

    notfound = ( result ==  0)                         #line 627

    found = ( foundimmediate or  foundnormal)          #line 628#line 629
    if ( found):                                       #line 630
        if (State.compiling):                          #line 631
            if ( foundimmediate):                      #line 632
                exec( item)                            #line 633
            else:                                      #line 634
                compileword( item)                     #line 635#line 636#line 637
        else:                                          #line 638
            exec( item)                                #line 639#line 640#line 641
    else:                                              #line 642
        if (State.compiling):                          #line 643
            if (re.match(r"^-?\d*$",  item)):          #line 644
                compileinteger( item)                  #line 645
            else:                                      #line 646
                if (re.match(r"^-?d*\.?\d*$",  item)): #line 647
                    compilefloat( item)                #line 648
                else:                                  #line 649
                    returnFalse()                      #line 650#line 651#line 652#line 653#line 654
        else:                                          #line 655
            if (re.match(r"^-?\d*$",  item)):          #line 656
                pushasinteger( item)                   #line 657
            else:                                      #line 658
                if (re.match(r"^-?d*\.?\d*$",  item)): #line 659
                    pushasfloat( item)                 #line 660
                else:                                  #line 661
                    returnFalse()                      #line 662#line 663#line 664#line 665#line 666#line 667#line 668#line 669#line 670
    return  True                                       #line 671#line 672#line 673
code("interpret",0,  xinterpret)

def ok ():
    global State                                       #line 674
    # ( --) Interaction loop -- REPL                   #line 675

    blank =  32                                        #line 676
    while  True:                                       #line 677

        State.BUFF = input("OK ")
        State.BUFP = 0
                                                       #line 678
        while not (State.BUFP >= len(State.BUFF)):     #line 679
            xinterpret()                               #line 680#line 681#line 682#line 683#line 684

def debugok ():
    global State                                       #line 685
    # ( --) Interaction loop -- REPL                   #line 686

    blank =  32                                        #line 687

    State.BUFF = "7 ."
    State.BUFP = 0
                                                       #line 688
    while not (State.BUFP >= len(State.BUFF)):         #line 689
        if ( xinterpret()):                            #line 690
            print ( " ok", end="")                     #line 691
            print ()                                   #line 692#line 693
        print ( State.BUFP, end="")
        print ( " -- ", end="")
        print ( State.BUFF, end="")
        print ()                                       #line 694
        xdots()                                        #line 695#line 696
    print ( State.BUFP, end="")
    print ( " == ", end="")
    print ( State.BUFF, end="")
    print ()                                           #line 697
    xdot()                                             #line 698
    xdots()                                            #line 699#line 700#line 701
ok()                                                   #line 702#line 703