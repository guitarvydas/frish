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
def fvget (name):
    global State                                       #line 7


    fobjaddress =  _find(State.S.pop ())               #line 8

    return  State.RAM [ fobjaddress+ 1]                #line 9

                                                       #line 10
                                                       #line 11

def fvset (name,v):
    global State                                       #line 12


    fobjaddress =  _find(State.S.pop ())               #line 13


    namefieldaddress =  fobjaddress+ 1                 #line 14

    State.RAM [ namefieldaddress] =  v                 #line 15

                                                       #line 16
                                                       #line 17
                                                       #line 18

def doword ():
    global State                                       #line 19
    #⎩20⎭
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

    State.R.append ( State.IP)                         #line 63

    State.IP =  State.W+ 1                             #line 64

    while ( -1!= State.RAM [ State.IP]):
                                                       #line 65

        State.W =  State.RAM [ State.IP]               #line 66

        State.IP =  State.IP+ 1                        #line 67

        State.RAM [ State.W]()                         #line 68

                                                       #line 69


    State.IP = State.R.pop ()                          #line 70

                                                       #line 71
                                                       #line 72
                                                       #line 73

def notfound (word):
    global State                                       #line 74


    State.S.clear()                                    #line 75


    State.R.clear()                                    #line 76

    print ( word, end="")                              #line 77

    print ( "?", end="")                               #line 78

    print ()                                           #line 79

                                                       #line 80
                                                       #line 81

def exec (xt):
    global State                                       #line 82
    # found and compiling and immediate                #line 83

    State.W =  xt                                      #line 84

    State.IP =  -1# Dummy to hold place in return stack. 	#line 85

    State.RAM [ xt]()  # Execute code.                 #line 86

                                                       #line 87
                                                       #line 88

def compile_word (xt):
    global State                                       #line 89
    # found and not compiling                          #line 90

    State.W =  xt                                      #line 91

    State.IP =  -1# Dummy to hold place in return stack. 	#line 92

    State.RAM [ xt]()  # Execute code.                 #line 93

                                                       #line 94
                                                       #line 95

def pushasinteger (word):
    global State                                       #line 96

    State.S.push (int ( word))                         #line 97

                                                       #line 98
                                                       #line 99

def pushasfloat (word):
    global State                                       #line 100

    State.S.push (float ( word))                       #line 101

                                                       #line 102
                                                       #line 103

def compileinteger (word):
    global State                                       #line 104

    pushasinteger( word)                               #line 105

    literalize()                                       #line 106

                                                       #line 107
                                                       #line 108

def compilefloat (word):
    global State                                       #line 109

    pushasfloat( word)                                 #line 110

    literalize()                                       #line 111

                                                       #line 112
                                                       #line 113

def code (name,flags,does):
    global State                                       #line 114
    # Add new word to RAM dictionary. We create a word (Forth "object") in RAM with 5 fields and extend the⎩115⎭
    #	the dictionary by linking back to the head of the dictionary list #line 116

    x =  len( State.RAM)                               #line 117
                                                       #line 118


    State.RAM.append ( State.LAST) # (LFA) link to previous word in dictionary list #line 119


    State.RAM.append ( name)       # (NFA) name of word #line 120


    State.RAM.append ( flags)      #       0 = normal word, 1 = immediate word #line 121


    State.RAM.append ( does)       # (CFA) function pointer that points to code that executes the word #line 122
                                                       #line 123

    State.LAST =  x                # LAST is the pointer to the head of the dictionary list, set it to point to⎩124⎭
    #					this new word                                #line 125

                                                       #line 126
                                                       #line 127

def literalize ():
    global State                                       #line 128
    # Compile literal into definition.                 #line 129


    State.RAM.append ( _find( "(literal)"))  ## Compile address of doliteral. #line 130


    State.RAM.append (State.S.pop ())             # # Compile literal value. #line 131

                                                       #line 132
                                                       #line 133

def xinterpret ():
    global State                                       #line 134

    State.R.append ( "interpret")                      #line 135

    _walk()                                            #line 136

    return State.S.pop ()                              #line 137

                                                       #line 138
                                                       #line 139

def ok ():
    global State                                       #line 140
    # ( --) Interaction loop -- REPL                   #line 141


    blank =  32                                        #line 142

    while  True:
                                                       #line 143


        State.BUFF = input("OK ")
        State.BUFP = 0
                                                       #line 144

        while not (State.BUFP >= len(State.BUFF)) :
                                                       #line 145

            xinterpret()                               #line 146

                                                       #line 147


                                                       #line 148


                                                       #line 149
                                                       #line 150

def doconst ():
    global State# method for const                     #line 151


    parameter =  State.RAM [ State.W+ 1]               #line 152

    State.S.push ( parameter)                          #line 153

                                                       #line 154
                                                       #line 155
                                                       #line 156

def docreate ():
    global State                                       #line 157


    parameterAddress =  len( State.RAM) + 4            #line 158

    State.S.push ( parameterAddress)                   #line 159

                                                       #line 160

def create (name):
    global State                                       #line 161


    normal =  0                                        #line 162

    code( name,  normal,  docreate)                    #line 163

                                                       #line 164

def comma (value):
    global State                                       #line 165


    State.RAM.append ( value)                          #line 166

                                                       #line 167
                                                       #line 168

def fvar (name,value):
    global State                                       #line 169

    create( name)                                      #line 170

    comma( value)                                      #line 171

                                                       #line 172
                                                       #line 173

def _find (name):
    global State                                       #line 174
    # "( name -- cfa|0) Find CFA of word name."        #line 175


    x =  State.LAST                                    #line 176

    while ( x >=  0):
                                                       #line 177
        # ## print(f"-- {x} : {RAM[x]}, {RAM[x + 1]}")  # Debug. #line 178

        if ( name ==  State.RAM [ x+ 1]):
            # # Match!                                 #line 179

            return  x+ 3                               #line 180



        else:
                                                       #line 181

            x =  State.RAM [ x]  # # Get next link.    #line 182

                                                       #line 183


                                                       #line 184


    return  0  # # Nothing found.                      #line 185

                                                       #line 186
                                                       #line 187

def debugok ():
    global State                                       #line 188
    # ( --) Interaction loop -- REPL                   #line 189


    blank =  32                                        #line 190


    State.BUFF = "7 ."
    State.BUFP = 0
                                                       #line 191

    while not (State.BUFP >= len(State.BUFF)) :
                                                       #line 192

        if ( interpret()):
                                                       #line 193

            print ( " ok", end="")                     #line 194

            print ()                                   #line 195

                                                       #line 196


        print ( State.BUFP, end="")
        print ( " -- ", end="")
        print ( State.BUFF, end="")
        print ()                                       #line 197

        xdots()                                        #line 198

                                                       #line 199


    print ( State.BUFP, end="")
    print ( " == ", end="")
    print ( State.BUFF, end="")
    print ()                                           #line 200

    xdot()                                             #line 201

    xdots()                                            #line 202

                                                       #line 203

                                                       #line 204
                                                       #line 205

def _walk ():
    global State
    opcode = State.R.pop ()
    match opcode:
        case "create":                                 #line 208


            blank =  32                                #line 209

            State.S.push ( blank)                      #line 210

            xword()                                    #line 211


            name = State.S.pop ()                      #line 212

            create( name)                              #line 213

                                                       #line 214
                                                       #line 215


        case "drop":                                   #line 216
            # ( a -- )                                 #line 217

            State.S.pop ()                             #line 218

                                                       #line 219
                                                       #line 220


        case "dup":                                    #line 221
            # ( a -- a a )                             #line 222


            A = State.S.pop ()                         #line 223

            State.S.push ( A)                          #line 224

            State.S.push ( A)                          #line 225

                                                       #line 226
                                                       #line 227


        case "negate":                                 #line 228
            # ( n -- (-n) )                            #line 229


            n = State.S.pop ()                         #line 230

            State.S.push ( -n)                         #line 231

                                                       #line 232
                                                       #line 233


        case "emit":                                   #line 234
            # ( c -- ) emit specified character        #line 235


            c = State.S.pop ()                         #line 236

            print (chr (int ( c)), end="")             #line 237

                                                       #line 238
                                                       #line 239


        case "cr":
            print ()
                                                       #line 240


        case ".":# ( n --) Print TOS
            print (State.S.pop (), end="")
            print ()
                                                       #line 241


        case ".s":# ( --) Print stack contents
            print (State.S, end="")
            print ()
                                                       #line 242
                                                       #line 243


        case "+":                                      #line 244
            # ( a b -- sum)                            #line 245


            B = State.S.pop ()                         #line 246


            A = State.S.pop ()                         #line 247

            State.S.push ( A+ B)                       #line 248

                                                       #line 249
                                                       #line 250


        case "*":                                      #line 251
            # ( a b -- product )                       #line 252


            B = State.S.pop ()                         #line 253


            A = State.S.pop ()                         #line 254

            State.S.push ( A* B)                       #line 255

                                                       #line 256
                                                       #line 257


        case "=":                                      #line 258
            # ( a b -- bool )                          #line 259


            B = State.S.pop ()                         #line 260


            A = State.S.pop ()                         #line 261

            State.S.push ( A ==  B)                    #line 262

                                                       #line 263
                                                       #line 264


        case "<":                                      #line 265
            # ( a b -- bool )                          #line 266


            B = State.S.pop ()                         #line 267


            A = State.S.pop ()                         #line 268

            State.S.push ( A <  B)                     #line 269

                                                       #line 270
                                                       #line 271


        case ">":                                      #line 272
            # ( a b -- bool )                          #line 273


            B = State.S.pop ()                         #line 274


            A = State.S.pop ()                         #line 275

            State.S.push ( A >  B)                     #line 276

                                                       #line 277
                                                       #line 278


        case "0=":                                     #line 279
            # ( a -- bool )                            #line 280


            a = State.S.pop ()                         #line 281

            State.S.push ( a ==  0)                    #line 282

                                                       #line 283
                                                       #line 284


        case "0<":                                     #line 285
            # ( a -- bool )                            #line 286


            a = State.S.pop ()                         #line 287

            State.S.push ( 0 <  a)                     #line 288

                                                       #line 289
                                                       #line 290


        case "0>":                                     #line 291
            # ( a -- bool )                            #line 292


            a = State.S.pop ()                         #line 293

            State.S.push ( 0 >  a)                     #line 294

                                                       #line 295
                                                       #line 296


        case "not":                                    #line 297
            # ( a -- bool )                            #line 298


            a = State.S.pop ()                         #line 299

            State.S.push (not  a)                      #line 300

                                                       #line 301
                                                       #line 302


        case "and":                                    #line 303
            # ( a b -- bool )                          #line 304


            b = State.S.pop ()                         #line 305


            a = State.S.pop ()                         #line 306

            State.S.push ( a and  b)                   #line 307

                                                       #line 308
                                                       #line 309


        case "or":                                     #line 310
            # ( a b -- bool )                          #line 311


            b = State.S.pop ()                         #line 312


            a = State.S.pop ()                         #line 313

            State.S.push ( a or  b)                    #line 314

                                                       #line 315
                                                       #line 316


        case ">r":                                     #line 317
            # ( a --  )                                #line 318


            a = State.S.pop ()                         #line 319

            State.R.append ( a)                        #line 320

                                                       #line 321
                                                       #line 322


        case "r>":                                     #line 323
            # ( -- x )                                 #line 324


            x = State.R.pop ()                         #line 325

            State.S.push ( x)                          #line 326

                                                       #line 327
                                                       #line 328


        case "i":                                      #line 329
            # ( -- i ) get current loop index from R stack #line 330


            i = State.R [-1]                           #line 331

            State.S.push ( i)                          #line 332

                                                       #line 333
                                                       #line 334


        case "i'":                                     #line 335
            # ( -- i ) get outer loop limit from R stack #line 336


            i = State.R [-2]                           #line 337

            State.S.push ( i)                          #line 338

                                                       #line 339
                                                       #line 340


        case "j":                                      #line 341
            # ( -- j ) get outer loop index from R stack #line 342


            j = State.R [-3]                           #line 343

            State.S.push ( j)                          #line 344

                                                       #line 345
                                                       #line 346


        case "swap":                                   #line 347
            # ( a b -- b a)                            #line 348


            B = State.S.pop ()                         #line 349


            A = State.S.pop ()                         #line 350

            State.S.push ( B)                          #line 351

            State.S.push ( A)                          #line 352

                                                       #line 353


        case "-":                                      #line 354
            # ( a b -- diff)                           #line 355


            B = State.S.pop ()                         #line 356


            A = State.S.pop ()                         #line 357

            State.S.push ( A- B)                       #line 358

                                                       #line 359


        case "/":                                      #line 360
            # ( a b -- div)                            #line 361

            xswap()                                    #line 362


            B = State.S.pop ()                         #line 363


            A = State.S.pop ()                         #line 364

            State.S.push ( B [A])                      #line 365

                                                       #line 366
                                                       #line 367


        case "word":                                   #line 368
            # (char -- string) Read in string delimited by char #line 369


            wanted = chr(State.S.pop ())               #line 370


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
                                                       #line 371

                                                       #line 372
                                                       #line 373
            # Example of state-smart word, which Brodie sez not to do. Sorry, Leo... #line 374
            # This sin allows it to be used the same way compiling or interactive. #line 375


        case "'":                                      #line 376
            # ( -- string) Read up to closing dquote, push to stack #line 377
            # A string in Forth begins with the word " (followed by a space) then all characters up to the next " #line 378
            # E.G. " abc"                              #line 379


            DQ =  34                                   #line 380

            State.S.push ( DQ)                         #line 381

            xword()                                    #line 382

            if State.compiling [-1] :
                                                       #line 383

                literalize()                           #line 384

                                                       #line 385


                                                       #line 386
                                                       #line 387


        case ".'":                                     #line 388
            # ( --) Print string.                      #line 389

            xquote()                                   #line 390

            print (State.S.pop (), end="")             #line 391

                                                       #line 392
                                                       #line 393
                                                       #line 394
                                                       #line 395


        case "(literal)":                              #line 396
            #⎩397⎭
            #   Inside definitions only, pushes compiled literal to stack ⎩398⎭
            #⎩399⎭
            #       Certain Forth words are only applicable inside compiled sequences of subroutines ⎩400⎭
            #       Literals are handled in different ways when interpreted when in the REPL vs⎩401⎭
            #       compiled into sequences of subrs ⎩402⎭
            #       In the REPL, when we encounter a literal, we simply push it onto the stack ⎩403⎭
            #       In the compiler, though, we have to create an instruction that pushes ⎩404⎭
            #	 the literal onto the stack. ⎩405⎭
            #	 Compiled code doesn't do what the REPL does, we have to hard-wire and ⎩406⎭
            #	 bake in code that pushes the literal when the time comes to run the sequence. ⎩407⎭
            #⎩408⎭
            #       This word - "(literal)" - is a simple case and one could actually type this ⎩409⎭
            #	 instruction into the REPL, but, that would be redundant.  Other kinds of words, ⎩410⎭
            #	 e.g. some control-flow words, tend to be messier and the code below only handles ⎩411⎭
            #	 the compiled aspects and ignores the REPL aspects ⎩412⎭
            #⎩413⎭
            #       "IP" is the current word index in a sequence of words being compiled. ⎩414⎭
            #                                          #line 415


            lit =  State.RAM [ State.IP]               #line 416

            State.S.push ( lit)                        #line 417

            State.IP =  State.IP+ 1 # move past this item (the literal) - we're done with it #line 418

                                                       #line 419
                                                       #line 420


        case "branch":                                 #line 421
            # This instruction appears only inside subroutine sequences, jump to address in next cell #line 422
            # This instruction is inserted into a subr sequence when compiling control-flow words, like "else" see below) #line 423

            State.IP =  State.RAM [ State.IP]          #line 424
            # normally, we just execute an instruction then move the IP sequentially forward by 1 unit, i.e. IP ⇐ IP + 1 #line 425
            #   in this case, though, we explicitly change the IP to some other value and don't just increment it #line 426

                                                       #line 427
                                                       #line 428


        case "0branch":                                #line 429
            # This instruction appears only inside subroutine sequences, jump on false to address in next cell #line 430


            test = bool (State.S.pop ())               #line 431

            if ( test):
                                                       #line 432

                State.IP =  State.IP+ 1                #line 433



            else:
                                                       #line 434

                State.IP =  State.RAM [ State.IP]      #line 435

                                                       #line 436


                                                       #line 437
                                                       #line 438
                                                       #line 439
            # "immediate" words are fully operational even when in compile mode. Some (not all) of these words are meant to⎩440⎭
            #      work /only/ in compile mode. At the REPL prompt ("interpret" mode), they produce unwanted results.⎩441⎭
            #    immediate words: xif, xelse, xthen, xquote, xcomment, xsemi⎩442⎭
            #    immediate words that only have meaning in compile mode: xif, xelse, xthen, xsemi⎩443⎭
            #                                          #line 444
                                                       #line 445
                                                       #line 446
            # IF, ELSE and THEN are "immediate" words - they should only be used inside of ":" (colon compiler) #line 447
                                                       #line 448
            # see diagram compiling-IF-THEN.drawio.png #line 449

        case "if":
            State.compiling.push (False)
            State.compiling = False                    #line 450
            # This instruction appears only inside subroutine sequences, ( f -- ) compile if test and branchFalse  #line 451
            # Step. 1: generate conditional branch to yet-unknown target1  #line 452


            branchFalseAddress =  _find( "0branch")    #line 453


            State.RAM.append ( branchFalseAddress) # insert branch-if-false opcode (word)  #line 454

            State.R.append (len (Stack.RAM)) # target1 onto r-stack as memo for later fixup  #line 455


            target1 =  -1                              #line 456


            State.RAM.append ( target1) # branch target will be fixed up later  #line 457
            # Step. 2: generate code for true branch - return to compiler which will compile the following words  #line 458
            # THEN or ELSE will do the fixup of target1  #line 459

                                                       #line 460
                                                       #line 461
            # see diagram compiling-IF-ELSE-THEN.drawio.png #line 462

            State.compiling = State.compiling.pop ()
        case "else":
            State.compiling.push (False)
            State.compiling = False                    #line 463
            # Step. 1: fixup target1 from IF-true, retrieving memo from R-stack #line 464


            target1 = State.R.pop ()                   #line 465

            State.RAM [ target1] = len (Stack.RAM)     #line 466
            # Step. 2: generate unconditional branch for preceding IF, creating new memo for target2 on R-stack #line 467


            brAddress =  _find( "branch")              #line 468

            State.R.append (len (Stack.RAM)) # target2 address on R-stack as memo for later fixup #line 469


            target2 =  -1                              #line 470


            State.RAM.append ( target2) # branch target will be fixed up later #line 471
            # Step. 3: generate code for false branch - return to compiler which will compile the following words #line 472
            # THEN will do the fixup of target2        #line 473

                                                       #line 474
                                                       #line 475
            # see diagrams compiling-IF-THEN.drawio.png and compiling-IF-ELSE-THEN.drawio.png #line 476

            State.compiling = State.compiling.pop ()
        case "then":
            State.compiling.push (False)
            State.compiling = False                    #line 477
            # Step. 1: fixup target (from IF or from ELSE, above), retrieving memo from R-stack #line 478


            target = State.R.pop ()                    #line 479

            State.RAM [ target] = len (Stack.RAM)      #line 480

                                                       #line 481
                                                       #line 482

            State.compiling = State.compiling.pop ()

        case "(do)":                                   #line 483
            # ( limit index --) Puts limit and index on return stack. #line 484

            xswap()                                    #line 485


            index = State.S.pop ()                     #line 486


            limit = State.S.pop ()                     #line 487

            State.R.append ( index)                    #line 488

            State.R.append ( limit)                    #line 489

                                                       #line 490
                                                       #line 491

        case "do":
            State.compiling.push (False)
            State.compiling = False                    #line 492
            # (  limit index --) Begin counted loop.   #line 493


            State.RAM.append ( _find( "(do)"))  # Push do loop handler. #line 494

            State.R.append (len (Stack.RAM))           # Push address to jump back to. #line 495

                                                       #line 496
                                                       #line 497

            State.compiling = State.compiling.pop ()

        case "(loop)":                                 #line 498
            # (  -- f) Determine if loop is done.      #line 499


            index = State.R.pop ()                     #line 500


            limit = State.R.pop ()                     #line 501


            cond = ( index >=  limit)                  #line 502

            State.S.push ( cond)                       #line 503

            if ( cond):
                # clean up rstack if index >= limit    #line 504

                State.R.pop ()                         #line 505

                State.R.pop ()                         #line 506

                                                       #line 507


                                                       #line 508
                                                       #line 509

        case "+loop":
            State.compiling.push (False)
            State.compiling = False                    #line 510
            # ( --) Close counted loop.                #line 511


            State.RAM.append ( _find( "(loop)"))   # Compile in loop test. #line 512


            State.RAM.append ( _find( "0branch"))  # Compile in branch check. #line 513


            State.RAM.append (State.R.pop ())           # Address to jump back to. #line 514

                                                       #line 515
                                                       #line 516

            State.compiling = State.compiling.pop ()
        case "loop":
            State.compiling.push (False)
            State.compiling = False                    #line 517
            # (  --) Close counted loop.               #line 518

            State.S.push ( 1)                          #line 519

            literalize()# Default loop increment for x_loop. #line 520


            State.RAM.append ( _find( "(loop)"))   # Compile in loop test. #line 521


            State.RAM.append ( _find( "0branch"))  # Compile in branch check. #line 522


            State.RAM.append (State.R.pop ())           # Address to jump back to. #line 523

                                                       #line 524
                                                       #line 525

            State.compiling = State.compiling.pop ()
        case "begin":
            State.compiling.push (False)
            State.compiling = False                    #line 526

            State.R.append (len (Stack.RAM))  # ( --) Start indefinite loop. #line 527

                                                       #line 528
                                                       #line 529

            State.compiling = State.compiling.pop ()
        case "until":
            State.compiling.push (False)
            State.compiling = False                    #line 530
            # (  f --) Close indefinite loop with test. #line 531


            State.RAM.append ( _find( "0branch"))  # Expects result of test on stack. #line 532


            State.RAM.append (State.R.pop ())           # Address to jump back to. #line 533

                                                       #line 534
                                                       #line 535
                                                       #line 536
                                                       #line 537
            #  "... 123 constant K ..."                #line 538
            #  at interpretation time: 123 is on the Stack, we have consumed "constant" from BUFF, BUFF now contains "K ..." #line 539
            #  invoke 'word' which parses "K" and pushed it. The stack becomes [... 123 "K"] #line 540
            #  pop "K", pop 123, create a new word called 'K' with its PFA set to 123 and its CFA set to a subr that⎩541⎭
            #       gets 123 from its PFA and pushes it onto the stack #line 542

            State.compiling = State.compiling.pop ()

        case "const":                                  #line 543
            #  get next word - the name - from BUFF    #line 544


            blank =  32                                #line 545

            State.S.push ( blank)                      #line 546

            xword()                                    #line 547
            #  stack is now: ( NNNN name -- )          #line 548


            name = State.S.pop ()                      #line 549


            value = State.S.pop ()                     #line 550


            normal =  0                                #line 551


            fobj =  code( name,  normal,  doconst)     #line 552


            State.RAM.append ( value)                  #line 553

                                                       #line 554
                                                       #line 555


        case ",":                                      #line 556

            comma(State.S.pop ())                      #line 557

                                                       #line 558
                                                       #line 559


        case "variable":                               #line 560


            blank =  32                                #line 561

            State.S.push ( blank)                      #line 562

            xword()                                    #line 563


            name = State.S.pop ()                      #line 564


            value = State.S.pop ()                     #line 565

            fvar( name,  value)                        #line 566

                                                       #line 567
                                                       #line 568


        case "dump":                                   #line 569


            n = int (State.S.pop ())                   #line 570


            start = int (State.S.pop ())               #line 571

            print ( "----------------------------------------------------------------", end="")#line 572


            a =  start                                 #line 573

            while ( a <  start+( min( n, ( len( State.RAM) - start)))):
                                                       #line 574

                print ( a, end="")                     #line 575

                print ( ": ", end="")                  #line 576

                print ( State.RAM [ a], end="")        #line 577

                print ()                               #line 578


                a =  a+ 1                              #line 579

                                                       #line 580


                                                       #line 581
                                                       #line 582


        case "!":                                      #line 583


            b = State.S.pop ()                         #line 584


            a = State.S.pop ()                         #line 585

            State.RAM [ b] =  a                        #line 586

                                                       #line 587
                                                       #line 588


        case "bye":# ( --) Leave interpreter

            raise SystemExit
                                                       #line 589
                                                       #line 590
                                                       #line 591


        case "find":                                   #line 592
            # "( name | -- (name 0)|(xt 1)|(xt -1)) Search for word name." #line 593
            # 3 possible results: 1. (name 0) if not found, 2. (xt 1) if found and word is immediate, 3. (xt -1) if found and word is normal #line 594

            State.S.push ( 32)                         #line 595

            xword()                                    #line 596


            found =  _find(State.S[-1])                #line 597

            if ( 0 ==  found):
                                                       #line 598

                State.S.push ( 0)                      #line 599



            else:
                                                       #line 600

                State.S.pop ()  # # Get rid of name on stack. #line 601

                State.S.push ( found)                  #line 602


                immediate =  -1                        #line 603

                if ( State.RAM [State.S[-1] - 1] &  1):

                    immediate =  1
                                                       #line 604


                State.S.push ( immediate)              #line 605

                                                       #line 606


                                                       #line 607
                                                       #line 608


        case "'":                                      #line 609
            # "( name -- xt|-1) Search for execution token of word name." #line 610

            State.S.push ( 32)                         #line 611

            xword()                                    #line 612


            name = State.S.pop ()                      #line 613


            found =  _find( name)                      #line 614

            State.S.push ( found)                      #line 615

                                                       #line 616
                                                       #line 617


        case "None":                                   #line 618


            State.S.append (None)                      #line 619

                                                       #line 620
                                                       #line 621


        case "words":                                  #line 622
            # print words in dictionary                #line 623


            x =  State.LAST                            #line 624

            while ( x >  -1):
                                                       #line 625

                print ( State.RAM [ x+ 1], end="")     #line 626

                print ( " ", end="")                   #line 627

                                                       #line 628


            print ()                                   #line 629

                                                       #line 630
                                                       #line 631
                                                       #line 632


        case "execute":                                #line 633
            # invoke given word                        #line 634


            wordAddress = State.S.pop ()               #line 635

            wordAddress()                              #line 636

                                                       #line 637
                                                       #line 638
                                                       #line 639


        case ":":                                      #line 640
            # ( name | --) Start compilation.          #line 641


            blank =  32                                #line 642

            State.S.push ( blank)                      #line 643

            xword()                                    #line 644


            name = State.S.pop ()                      #line 645

            code( name,  0,  doword)                   #line 646

            State.compiling [-1] = True                #line 647

                                                       #line 648
                                                       #line 649

        case ";":
            State.compiling.push (False)
            State.compiling = False                    #line 650
            # ( --) Finish definition.                 #line 651
                                                       #line 652


            State.RAM.append ( -1)  # Marker for end of definition. #line 653

            State.compiling [-1] = False               #line 654

                                                       #line 655
                                                       #line 656

            State.compiling = State.compiling.pop ()

        case "interpret":                              #line 657
            # ( string --) Execute word.               #line 658
                                                       #line 659

            find()                                     #line 660
            # 3 possible results from find:⎩661⎭
            #	  1. (name 0) if not found,⎩662⎭
            #	  2. (xt 1) if found and word is immediate,⎩663⎭
            #	  3. (xt -1) if found and word is normal #line 664


            result = State.S.pop ()

            foundimmediate = ( result ==  1)           #line 665


            item = State.S.pop ()

            foundnormal = ( result ==  -1)             #line 666


            notfound = ( result ==  0)                 #line 667


            found = ( foundimmediate or  foundnormal)  #line 668
                                                       #line 669

            if ( found):
                                                       #line 670

                if (State.compiling [-1]):
                                                       #line 671

                    if ( foundimmediate):
                                                       #line 672

                        exec( item)                    #line 673



                    else:
                                                       #line 674

                        compileword( item)             #line 675

                                                       #line 676
                                                       #line 677




                else:
                                                       #line 678

                    exec( item)                        #line 679

                                                       #line 680
                                                       #line 681




            else:
                                                       #line 682

                if (State.compiling [-1]):
                                                       #line 683

                    if (re.match(r"^-?\d*$",  item)):
                                                       #line 684

                        compileinteger( item)          #line 685



                    else:
                                                       #line 686

                        if (re.match(r"^-?d*\.?\d*$",  item)):
                                                       #line 687

                            compilefloat( item)        #line 688



                        else:
                                                       #line 689

                            returnFalse()              #line 690

                                                       #line 691
                                                       #line 692


                                                       #line 693
                                                       #line 694




                else:
                                                       #line 695

                    if (re.match(r"^-?\d*$",  item)):
                                                       #line 696

                        pushasinteger( item)           #line 697



                    else:
                                                       #line 698

                        if (re.match(r"^-?d*\.?\d*$",  item)):
                                                       #line 699

                            pushasfloat( item)         #line 700



                        else:
                                                       #line 701

                            returnFalse()              #line 702

                                                       #line 703
                                                       #line 704


                                                       #line 705
                                                       #line 706


                                                       #line 707
                                                       #line 708


                                                       #line 709
                                                       #line 710


            return  True                               #line 711

                                                       #line 712

                                                       #line 713
                                                       #line 714


                                                       #line 715
ok ()                                                  #line 716
                                                       #line 717