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

def ok ():
    global State                                       #line 134
    # ( --) Interaction loop -- REPL                   #line 135


    blank =  32                                        #line 136

    while  True:
                                                       #line 137


        State.BUFF = input("OK ")
        State.BUFP = 0
                                                       #line 138

        while not (State.BUFP >= len(State.BUFF)) :
                                                       #line 139


            State.R.push ("interpret")
            _walk ()                                   #line 140

                                                       #line 141


                                                       #line 142


                                                       #line 143
                                                       #line 144

def doconst ():
    global State# method for const                     #line 145


    parameter =  State.RAM [ State.W+ 1]               #line 146

    State.S.push ( parameter)                          #line 147

                                                       #line 148
                                                       #line 149
                                                       #line 150

def docreate ():
    global State                                       #line 151


    parameterAddress =  len( State.RAM) + 4            #line 152

    State.S.push ( parameterAddress)                   #line 153

                                                       #line 154

def create (name):
    global State                                       #line 155


    normal =  0                                        #line 156

    code( name,  normal,  docreate)                    #line 157

                                                       #line 158

def comma (value):
    global State                                       #line 159


    State.RAM.append ( value)                          #line 160

                                                       #line 161
                                                       #line 162

def fvar (name,value):
    global State                                       #line 163

    create( name)                                      #line 164

    comma( value)                                      #line 165

                                                       #line 166
                                                       #line 167

def _find (name):
    global State                                       #line 168
    # "( name -- cfa|0) Find CFA of word name."        #line 169


    x =  State.LAST                                    #line 170

    while ( x >=  0):
                                                       #line 171
        # ## print(f"-- {x} : {RAM[x]}, {RAM[x + 1]}")  # Debug. #line 172

        if ( name ==  State.RAM [ x+ 1]):
            # # Match!                                 #line 173

            return  x+ 3                               #line 174



        else:
                                                       #line 175

            x =  State.RAM [ x]  # # Get next link.    #line 176

                                                       #line 177


                                                       #line 178


    return  0  # # Nothing found.                      #line 179

                                                       #line 180
                                                       #line 181

def debugok ():
    global State                                       #line 182
    # ( --) Interaction loop -- REPL                   #line 183


    blank =  32                                        #line 184


    State.BUFF = "7 ."
    State.BUFP = 0
                                                       #line 185

    while not (State.BUFP >= len(State.BUFF)) :
                                                       #line 186

        if (
        State.R.push ("interpret")
        _walk ()):
                                                       #line 187

            print ( " ok", end="")                     #line 188

            print ()                                   #line 189

                                                       #line 190


        print ( State.BUFP, end="")
        print ( " -- ", end="")
        print ( State.BUFF, end="")
        print ()                                       #line 191

        xdots()                                        #line 192

                                                       #line 193


    print ( State.BUFP, end="")
    print ( " == ", end="")
    print ( State.BUFF, end="")
    print ()                                           #line 194

    xdot()                                             #line 195

    xdots()                                            #line 196

                                                       #line 197

                                                       #line 198
                                                       #line 199

def _walk ():
    global State
    opcode = State.R.pop ()
    match opcode:
        case "create":                                 #line 202


            blank =  32                                #line 203

            State.S.push ( blank)                      #line 204

            xword()                                    #line 205


            name = State.S.pop ()                      #line 206

            create( name)                              #line 207

                                                       #line 208
                                                       #line 209


        case "drop":                                   #line 210
            # ( a -- )                                 #line 211

            State.S.pop ()                             #line 212

                                                       #line 213
                                                       #line 214


        case "dup":                                    #line 215
            # ( a -- a a )                             #line 216


            A = State.S.pop ()                         #line 217

            State.S.push ( A)                          #line 218

            State.S.push ( A)                          #line 219

                                                       #line 220
                                                       #line 221


        case "negate":                                 #line 222
            # ( n -- (-n) )                            #line 223


            n = State.S.pop ()                         #line 224

            State.S.push ( -n)                         #line 225

                                                       #line 226
                                                       #line 227


        case "emit":                                   #line 228
            # ( c -- ) emit specified character        #line 229


            c = State.S.pop ()                         #line 230

            print (chr (int ( c)), end="")             #line 231

                                                       #line 232
                                                       #line 233


        case "cr":
            print ()
                                                       #line 234


        case ".":# ( n --) Print TOS
            print (State.S.pop (), end="")
            print ()
                                                       #line 235


        case ".s":# ( --) Print stack contents
            print (State.S, end="")
            print ()
                                                       #line 236
                                                       #line 237


        case "+":                                      #line 238
            # ( a b -- sum)                            #line 239


            B = State.S.pop ()                         #line 240


            A = State.S.pop ()                         #line 241

            State.S.push ( A+ B)                       #line 242

                                                       #line 243
                                                       #line 244


        case "*":                                      #line 245
            # ( a b -- product )                       #line 246


            B = State.S.pop ()                         #line 247


            A = State.S.pop ()                         #line 248

            State.S.push ( A* B)                       #line 249

                                                       #line 250
                                                       #line 251


        case "=":                                      #line 252
            # ( a b -- bool )                          #line 253


            B = State.S.pop ()                         #line 254


            A = State.S.pop ()                         #line 255

            State.S.push ( A ==  B)                    #line 256

                                                       #line 257
                                                       #line 258


        case "<":                                      #line 259
            # ( a b -- bool )                          #line 260


            B = State.S.pop ()                         #line 261


            A = State.S.pop ()                         #line 262

            State.S.push ( A <  B)                     #line 263

                                                       #line 264
                                                       #line 265


        case ">":                                      #line 266
            # ( a b -- bool )                          #line 267


            B = State.S.pop ()                         #line 268


            A = State.S.pop ()                         #line 269

            State.S.push ( A >  B)                     #line 270

                                                       #line 271
                                                       #line 272


        case "0=":                                     #line 273
            # ( a -- bool )                            #line 274


            a = State.S.pop ()                         #line 275

            State.S.push ( a ==  0)                    #line 276

                                                       #line 277
                                                       #line 278


        case "0<":                                     #line 279
            # ( a -- bool )                            #line 280


            a = State.S.pop ()                         #line 281

            State.S.push ( 0 <  a)                     #line 282

                                                       #line 283
                                                       #line 284


        case "0>":                                     #line 285
            # ( a -- bool )                            #line 286


            a = State.S.pop ()                         #line 287

            State.S.push ( 0 >  a)                     #line 288

                                                       #line 289
                                                       #line 290


        case "not":                                    #line 291
            # ( a -- bool )                            #line 292


            a = State.S.pop ()                         #line 293

            State.S.push (not  a)                      #line 294

                                                       #line 295
                                                       #line 296


        case "and":                                    #line 297
            # ( a b -- bool )                          #line 298


            b = State.S.pop ()                         #line 299


            a = State.S.pop ()                         #line 300

            State.S.push ( a and  b)                   #line 301

                                                       #line 302
                                                       #line 303


        case "or":                                     #line 304
            # ( a b -- bool )                          #line 305


            b = State.S.pop ()                         #line 306


            a = State.S.pop ()                         #line 307

            State.S.push ( a or  b)                    #line 308

                                                       #line 309
                                                       #line 310


        case ">r":                                     #line 311
            # ( a --  )                                #line 312


            a = State.S.pop ()                         #line 313

            State.R.append ( a)                        #line 314

                                                       #line 315
                                                       #line 316


        case "r>":                                     #line 317
            # ( -- x )                                 #line 318


            x = State.R.pop ()                         #line 319

            State.S.push ( x)                          #line 320

                                                       #line 321
                                                       #line 322


        case "i":                                      #line 323
            # ( -- i ) get current loop index from R stack #line 324


            i = State.R [-1]                           #line 325

            State.S.push ( i)                          #line 326

                                                       #line 327
                                                       #line 328


        case "i'":                                     #line 329
            # ( -- i ) get outer loop limit from R stack #line 330


            i = State.R [-2]                           #line 331

            State.S.push ( i)                          #line 332

                                                       #line 333
                                                       #line 334


        case "j":                                      #line 335
            # ( -- j ) get outer loop index from R stack #line 336


            j = State.R [-3]                           #line 337

            State.S.push ( j)                          #line 338

                                                       #line 339
                                                       #line 340


        case "swap":                                   #line 341
            # ( a b -- b a)                            #line 342
            x = Stack [-1]
            Stack [-1] = Stack [-2]
            Stack [-2] = x                             #line 343#line 347


        case "-":                                      #line 348
            # ( a b -- diff)                           #line 349


            B = State.S.pop ()                         #line 350


            A = State.S.pop ()                         #line 351

            State.S.push ( A- B)                       #line 352

                                                       #line 353


        case "/":                                      #line 354
            # ( a b -- div)                            #line 355

            xswap()                                    #line 356


            B = State.S.pop ()                         #line 357


            A = State.S.pop ()                         #line 358

            State.S.push ( B [A])                      #line 359

                                                       #line 360
                                                       #line 361


        case "word":                                   #line 362
            # (char -- string) Read in string delimited by char #line 363


            wanted = chr(State.S.pop ())               #line 364


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
                                                       #line 365

                                                       #line 366
                                                       #line 367
            # Example of state-smart word, which Brodie sez not to do. Sorry, Leo... #line 368
            # This sin allows it to be used the same way compiling or interactive. #line 369


        case "'":                                      #line 370
            # ( -- string) Read up to closing dquote, push to stack #line 371
            # A string in Forth begins with the word " (followed by a space) then all characters up to the next " #line 372
            # E.G. " abc"                              #line 373


            DQ =  34                                   #line 374

            State.S.push ( DQ)                         #line 375

            xword()                                    #line 376

            if State.compiling [-1] :
                                                       #line 377

                literalize()                           #line 378

                                                       #line 379


                                                       #line 380
                                                       #line 381


        case ".'":                                     #line 382
            # ( --) Print string.                      #line 383

            xquote()                                   #line 384

            print (State.S.pop (), end="")             #line 385

                                                       #line 386
                                                       #line 387
                                                       #line 388
                                                       #line 389


        case "(literal)":                              #line 390
            #⎩391⎭
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
            #                                          #line 409


            lit =  State.RAM [ State.IP]               #line 410

            State.S.push ( lit)                        #line 411

            State.IP =  State.IP+ 1 # move past this item (the literal) - we're done with it #line 412

                                                       #line 413
                                                       #line 414


        case "branch":                                 #line 415
            # This instruction appears only inside subroutine sequences, jump to address in next cell #line 416
            # This instruction is inserted into a subr sequence when compiling control-flow words, like "else" see below) #line 417

            State.IP =  State.RAM [ State.IP]          #line 418
            # normally, we just execute an instruction then move the IP sequentially forward by 1 unit, i.e. IP ⇐ IP + 1 #line 419
            #   in this case, though, we explicitly change the IP to some other value and don't just increment it #line 420

                                                       #line 421
                                                       #line 422


        case "0branch":                                #line 423
            # This instruction appears only inside subroutine sequences, jump on false to address in next cell #line 424


            test = bool (State.S.pop ())               #line 425

            if ( test):
                                                       #line 426

                State.IP =  State.IP+ 1                #line 427



            else:
                                                       #line 428

                State.IP =  State.RAM [ State.IP]      #line 429

                                                       #line 430


                                                       #line 431
                                                       #line 432
                                                       #line 433
            # "immediate" words are fully operational even when in compile mode. Some (not all) of these words are meant to⎩434⎭
            #      work /only/ in compile mode. At the REPL prompt ("interpret" mode), they produce unwanted results.⎩435⎭
            #    immediate words: xif, xelse, xthen, xquote, xcomment, xsemi⎩436⎭
            #    immediate words that only have meaning in compile mode: xif, xelse, xthen, xsemi⎩437⎭
            #                                          #line 438
                                                       #line 439
                                                       #line 440
            # IF, ELSE and THEN are "immediate" words - they should only be used inside of ":" (colon compiler) #line 441
                                                       #line 442
            # see diagram compiling-IF-THEN.drawio.png #line 443

        case "if":
            State.compiling.push (False)
            State.compiling = False                    #line 444
            # This instruction appears only inside subroutine sequences, ( f -- ) compile if test and branchFalse  #line 445
            # Step. 1: generate conditional branch to yet-unknown target1  #line 446


            branchFalseAddress =  _find( "0branch")    #line 447


            State.RAM.append ( branchFalseAddress) # insert branch-if-false opcode (word)  #line 448

            State.R.append (len (Stack.RAM)) # target1 onto r-stack as memo for later fixup  #line 449


            target1 =  -1                              #line 450


            State.RAM.append ( target1) # branch target will be fixed up later  #line 451
            # Step. 2: generate code for true branch - return to compiler which will compile the following words  #line 452
            # THEN or ELSE will do the fixup of target1  #line 453

                                                       #line 454
                                                       #line 455
            # see diagram compiling-IF-ELSE-THEN.drawio.png #line 456

            State.compiling = State.compiling.pop ()
        case "else":
            State.compiling.push (False)
            State.compiling = False                    #line 457
            # Step. 1: fixup target1 from IF-true, retrieving memo from R-stack #line 458


            target1 = State.R.pop ()                   #line 459

            State.RAM [ target1] = len (Stack.RAM)     #line 460
            # Step. 2: generate unconditional branch for preceding IF, creating new memo for target2 on R-stack #line 461


            brAddress =  _find( "branch")              #line 462

            State.R.append (len (Stack.RAM)) # target2 address on R-stack as memo for later fixup #line 463


            target2 =  -1                              #line 464


            State.RAM.append ( target2) # branch target will be fixed up later #line 465
            # Step. 3: generate code for false branch - return to compiler which will compile the following words #line 466
            # THEN will do the fixup of target2        #line 467

                                                       #line 468
                                                       #line 469
            # see diagrams compiling-IF-THEN.drawio.png and compiling-IF-ELSE-THEN.drawio.png #line 470

            State.compiling = State.compiling.pop ()
        case "then":
            State.compiling.push (False)
            State.compiling = False                    #line 471
            # Step. 1: fixup target (from IF or from ELSE, above), retrieving memo from R-stack #line 472


            target = State.R.pop ()                    #line 473

            State.RAM [ target] = len (Stack.RAM)      #line 474

                                                       #line 475
                                                       #line 476

            State.compiling = State.compiling.pop ()

        case "(do)":                                   #line 477
            # ( limit index --) Puts limit and index on return stack. #line 478

            xswap()                                    #line 479


            index = State.S.pop ()                     #line 480


            limit = State.S.pop ()                     #line 481

            State.R.append ( index)                    #line 482

            State.R.append ( limit)                    #line 483

                                                       #line 484
                                                       #line 485

        case "do":
            State.compiling.push (False)
            State.compiling = False                    #line 486
            # (  limit index --) Begin counted loop.   #line 487


            State.RAM.append ( _find( "(do)"))  # Push do loop handler. #line 488

            State.R.append (len (Stack.RAM))           # Push address to jump back to. #line 489

                                                       #line 490
                                                       #line 491

            State.compiling = State.compiling.pop ()

        case "(loop)":                                 #line 492
            # (  -- f) Determine if loop is done.      #line 493


            index = State.R.pop ()                     #line 494


            limit = State.R.pop ()                     #line 495


            cond = ( index >=  limit)                  #line 496

            State.S.push ( cond)                       #line 497

            if ( cond):
                # clean up rstack if index >= limit    #line 498

                State.R.pop ()                         #line 499

                State.R.pop ()                         #line 500

                                                       #line 501


                                                       #line 502
                                                       #line 503

        case "+loop":
            State.compiling.push (False)
            State.compiling = False                    #line 504
            # ( --) Close counted loop.                #line 505


            State.RAM.append ( _find( "(loop)"))   # Compile in loop test. #line 506


            State.RAM.append ( _find( "0branch"))  # Compile in branch check. #line 507


            State.RAM.append (State.R.pop ())           # Address to jump back to. #line 508

                                                       #line 509
                                                       #line 510

            State.compiling = State.compiling.pop ()
        case "loop":
            State.compiling.push (False)
            State.compiling = False                    #line 511
            # (  --) Close counted loop.               #line 512

            State.S.push ( 1)                          #line 513

            literalize()# Default loop increment for x_loop. #line 514


            State.RAM.append ( _find( "(loop)"))   # Compile in loop test. #line 515


            State.RAM.append ( _find( "0branch"))  # Compile in branch check. #line 516


            State.RAM.append (State.R.pop ())           # Address to jump back to. #line 517

                                                       #line 518
                                                       #line 519

            State.compiling = State.compiling.pop ()
        case "begin":
            State.compiling.push (False)
            State.compiling = False                    #line 520

            State.R.append (len (Stack.RAM))  # ( --) Start indefinite loop. #line 521

                                                       #line 522
                                                       #line 523

            State.compiling = State.compiling.pop ()
        case "until":
            State.compiling.push (False)
            State.compiling = False                    #line 524
            # (  f --) Close indefinite loop with test. #line 525


            State.RAM.append ( _find( "0branch"))  # Expects result of test on stack. #line 526


            State.RAM.append (State.R.pop ())           # Address to jump back to. #line 527

                                                       #line 528
                                                       #line 529
                                                       #line 530
                                                       #line 531
            #  "... 123 constant K ..."                #line 532
            #  at interpretation time: 123 is on the Stack, we have consumed "constant" from BUFF, BUFF now contains "K ..." #line 533
            #  invoke 'word' which parses "K" and pushed it. The stack becomes [... 123 "K"] #line 534
            #  pop "K", pop 123, create a new word called 'K' with its PFA set to 123 and its CFA set to a subr that⎩535⎭
            #       gets 123 from its PFA and pushes it onto the stack #line 536

            State.compiling = State.compiling.pop ()

        case "const":                                  #line 537
            #  get next word - the name - from BUFF    #line 538


            blank =  32                                #line 539

            State.S.push ( blank)                      #line 540

            xword()                                    #line 541
            #  stack is now: ( NNNN name -- )          #line 542


            name = State.S.pop ()                      #line 543


            value = State.S.pop ()                     #line 544


            normal =  0                                #line 545


            fobj =  code( name,  normal,  doconst)     #line 546


            State.RAM.append ( value)                  #line 547

                                                       #line 548
                                                       #line 549


        case ",":                                      #line 550

            comma(State.S.pop ())                      #line 551

                                                       #line 552
                                                       #line 553


        case "variable":                               #line 554


            blank =  32                                #line 555

            State.S.push ( blank)                      #line 556

            xword()                                    #line 557


            name = State.S.pop ()                      #line 558


            value = State.S.pop ()                     #line 559

            fvar( name,  value)                        #line 560

                                                       #line 561
                                                       #line 562


        case "dump":                                   #line 563


            n = int (State.S.pop ())                   #line 564


            start = int (State.S.pop ())               #line 565

            print ( "----------------------------------------------------------------", end="")#line 566


            a =  start                                 #line 567

            while ( a <  start+( min( n, ( len( State.RAM) - start)))):
                                                       #line 568

                print ( a, end="")                     #line 569

                print ( ": ", end="")                  #line 570

                print ( State.RAM [ a], end="")        #line 571

                print ()                               #line 572


                a =  a+ 1                              #line 573

                                                       #line 574


                                                       #line 575
                                                       #line 576


        case "!":                                      #line 577


            b = State.S.pop ()                         #line 578


            a = State.S.pop ()                         #line 579

            State.RAM [ b] =  a                        #line 580

                                                       #line 581
                                                       #line 582


        case "bye":# ( --) Leave interpreter

            raise SystemExit
                                                       #line 583
                                                       #line 584
                                                       #line 585


        case "find":                                   #line 586
            # "( name | -- (name 0)|(xt 1)|(xt -1)) Search for word name." #line 587
            # 3 possible results: 1. (name 0) if not found, 2. (xt 1) if found and word is immediate, 3. (xt -1) if found and word is normal #line 588

            State.S.push ( 32)                         #line 589

            xword()                                    #line 590


            found =  _find(State.S[-1])                #line 591

            if ( 0 ==  found):
                                                       #line 592

                State.S.push ( 0)                      #line 593



            else:
                                                       #line 594

                State.S.pop ()  # # Get rid of name on stack. #line 595

                State.S.push ( found)                  #line 596


                immediate =  -1                        #line 597

                if ( State.RAM [State.S[-1] - 1] &  1):

                    immediate =  1
                                                       #line 598


                State.S.push ( immediate)              #line 599

                                                       #line 600


                                                       #line 601
                                                       #line 602


        case "'":                                      #line 603
            # "( name -- xt|-1) Search for execution token of word name." #line 604

            State.S.push ( 32)                         #line 605

            xword()                                    #line 606


            name = State.S.pop ()                      #line 607


            found =  _find( name)                      #line 608

            State.S.push ( found)                      #line 609

                                                       #line 610
                                                       #line 611


        case "None":                                   #line 612


            State.S.append (None)                      #line 613

                                                       #line 614
                                                       #line 615


        case "words":                                  #line 616
            # print words in dictionary                #line 617


            x =  State.LAST                            #line 618

            while ( x >  -1):
                                                       #line 619

                print ( State.RAM [ x+ 1], end="")     #line 620

                print ( " ", end="")                   #line 621

                                                       #line 622


            print ()                                   #line 623

                                                       #line 624
                                                       #line 625
                                                       #line 626


        case "execute":                                #line 627
            # invoke given word                        #line 628


            wordAddress = State.S.pop ()               #line 629

            wordAddress()                              #line 630

                                                       #line 631
                                                       #line 632
                                                       #line 633


        case ":":                                      #line 634
            # ( name | --) Start compilation.          #line 635


            blank =  32                                #line 636

            State.S.push ( blank)                      #line 637

            xword()                                    #line 638


            name = State.S.pop ()                      #line 639

            code( name,  0,  doword)                   #line 640

            State.compiling [-1] = True                #line 641

                                                       #line 642
                                                       #line 643

        case ";":
            State.compiling.push (False)
            State.compiling = False                    #line 644
            # ( --) Finish definition.                 #line 645
                                                       #line 646


            State.RAM.append ( -1)  # Marker for end of definition. #line 647

            State.compiling [-1] = False               #line 648

                                                       #line 649
                                                       #line 650

            State.compiling = State.compiling.pop ()

        case "interpret":                              #line 651
            # ( string --) Execute word.               #line 652
                                                       #line 653

            find()                                     #line 654
            # 3 possible results from find:⎩655⎭
            #	  1. (name 0) if not found,⎩656⎭
            #	  2. (xt 1) if found and word is immediate,⎩657⎭
            #	  3. (xt -1) if found and word is normal #line 658


            result = State.S.pop ()

            foundimmediate = ( result ==  1)           #line 659


            item = State.S.pop ()

            foundnormal = ( result ==  -1)             #line 660


            notfound = ( result ==  0)                 #line 661


            found = ( foundimmediate or  foundnormal)  #line 662
                                                       #line 663

            if ( found):
                                                       #line 664

                if (State.compiling [-1]):
                                                       #line 665

                    if ( foundimmediate):
                                                       #line 666

                        exec( item)                    #line 667



                    else:
                                                       #line 668

                        compileword( item)             #line 669

                                                       #line 670
                                                       #line 671




                else:
                                                       #line 672

                    exec( item)                        #line 673

                                                       #line 674
                                                       #line 675




            else:
                                                       #line 676

                if (State.compiling [-1]):
                                                       #line 677

                    if (re.match(r"^-?\d*$",  item)):
                                                       #line 678

                        compileinteger( item)          #line 679



                    else:
                                                       #line 680

                        if (re.match(r"^-?d*\.?\d*$",  item)):
                                                       #line 681

                            compilefloat( item)        #line 682



                        else:
                                                       #line 683

                            returnFalse()              #line 684

                                                       #line 685
                                                       #line 686


                                                       #line 687
                                                       #line 688




                else:
                                                       #line 689

                    if (re.match(r"^-?\d*$",  item)):
                                                       #line 690

                        pushasinteger( item)           #line 691



                    else:
                                                       #line 692

                        if (re.match(r"^-?d*\.?\d*$",  item)):
                                                       #line 693

                            pushasfloat( item)         #line 694



                        else:
                                                       #line 695

                            returnFalse()              #line 696

                                                       #line 697
                                                       #line 698


                                                       #line 699
                                                       #line 700


                                                       #line 701
                                                       #line 702


                                                       #line 703
                                                       #line 704


            return  True                               #line 705

                                                       #line 706

                                                       #line 707
                                                       #line 708


                                                       #line 709
ok ()                                                  #line 710
                                                       #line 711