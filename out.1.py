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


    State.R.push ("interpret")
    _walk ()                                           #line 135

    return State.S.pop ()                              #line 136

                                                       #line 137
                                                       #line 138

def ok ():
    global State                                       #line 139
    # ( --) Interaction loop -- REPL                   #line 140


    blank =  32                                        #line 141

    while  True:
                                                       #line 142


        State.BUFF = input("OK ")
        State.BUFP = 0
                                                       #line 143

        while not (State.BUFP >= len(State.BUFF)) :
                                                       #line 144

            xinterpret()                               #line 145

                                                       #line 146


                                                       #line 147


                                                       #line 148
                                                       #line 149

def doconst ():
    global State# method for const                     #line 150


    parameter =  State.RAM [ State.W+ 1]               #line 151

    State.S.push ( parameter)                          #line 152

                                                       #line 153
                                                       #line 154
                                                       #line 155

def docreate ():
    global State                                       #line 156


    parameterAddress =  len( State.RAM) + 4            #line 157

    State.S.push ( parameterAddress)                   #line 158

                                                       #line 159

def create (name):
    global State                                       #line 160


    normal =  0                                        #line 161

    code( name,  normal,  docreate)                    #line 162

                                                       #line 163

def comma (value):
    global State                                       #line 164


    State.RAM.append ( value)                          #line 165

                                                       #line 166
                                                       #line 167

def fvar (name,value):
    global State                                       #line 168

    create( name)                                      #line 169

    comma( value)                                      #line 170

                                                       #line 171
                                                       #line 172

def _find (name):
    global State                                       #line 173
    # "( name -- cfa|0) Find CFA of word name."        #line 174


    x =  State.LAST                                    #line 175

    while ( x >=  0):
                                                       #line 176
        # ## print(f"-- {x} : {RAM[x]}, {RAM[x + 1]}")  # Debug. #line 177

        if ( name ==  State.RAM [ x+ 1]):
            # # Match!                                 #line 178

            return  x+ 3                               #line 179



        else:
                                                       #line 180

            x =  State.RAM [ x]  # # Get next link.    #line 181

                                                       #line 182


                                                       #line 183


    return  0  # # Nothing found.                      #line 184

                                                       #line 185
                                                       #line 186

def debugok ():
    global State                                       #line 187
    # ( --) Interaction loop -- REPL                   #line 188


    blank =  32                                        #line 189


    State.BUFF = "7 ."
    State.BUFP = 0
                                                       #line 190

    while not (State.BUFP >= len(State.BUFF)) :
                                                       #line 191

        if ( interpret()):
                                                       #line 192

            print ( " ok", end="")                     #line 193

            print ()                                   #line 194

                                                       #line 195


        print ( State.BUFP, end="")
        print ( " -- ", end="")
        print ( State.BUFF, end="")
        print ()                                       #line 196

        xdots()                                        #line 197

                                                       #line 198


    print ( State.BUFP, end="")
    print ( " == ", end="")
    print ( State.BUFF, end="")
    print ()                                           #line 199

    xdot()                                             #line 200

    xdots()                                            #line 201

                                                       #line 202

                                                       #line 203
                                                       #line 204

def _walk ():
    global State
    opcode = State.R.pop ()
    match opcode:
        case "create":                                 #line 207


            blank =  32                                #line 208

            State.S.push ( blank)                      #line 209

            xword()                                    #line 210


            name = State.S.pop ()                      #line 211

            create( name)                              #line 212

                                                       #line 213
                                                       #line 214


        case "drop":                                   #line 215
            # ( a -- )                                 #line 216

            State.S.pop ()                             #line 217

                                                       #line 218
                                                       #line 219


        case "dup":                                    #line 220
            # ( a -- a a )                             #line 221


            A = State.S.pop ()                         #line 222

            State.S.push ( A)                          #line 223

            State.S.push ( A)                          #line 224

                                                       #line 225
                                                       #line 226


        case "negate":                                 #line 227
            # ( n -- (-n) )                            #line 228


            n = State.S.pop ()                         #line 229

            State.S.push ( -n)                         #line 230

                                                       #line 231
                                                       #line 232


        case "emit":                                   #line 233
            # ( c -- ) emit specified character        #line 234


            c = State.S.pop ()                         #line 235

            print (chr (int ( c)), end="")             #line 236

                                                       #line 237
                                                       #line 238


        case "cr":
            print ()
                                                       #line 239


        case ".":# ( n --) Print TOS
            print (State.S.pop (), end="")
            print ()
                                                       #line 240


        case ".s":# ( --) Print stack contents
            print (State.S, end="")
            print ()
                                                       #line 241
                                                       #line 242


        case "+":                                      #line 243
            # ( a b -- sum)                            #line 244


            B = State.S.pop ()                         #line 245


            A = State.S.pop ()                         #line 246

            State.S.push ( A+ B)                       #line 247

                                                       #line 248
                                                       #line 249


        case "*":                                      #line 250
            # ( a b -- product )                       #line 251


            B = State.S.pop ()                         #line 252


            A = State.S.pop ()                         #line 253

            State.S.push ( A* B)                       #line 254

                                                       #line 255
                                                       #line 256


        case "=":                                      #line 257
            # ( a b -- bool )                          #line 258


            B = State.S.pop ()                         #line 259


            A = State.S.pop ()                         #line 260

            State.S.push ( A ==  B)                    #line 261

                                                       #line 262
                                                       #line 263


        case "<":                                      #line 264
            # ( a b -- bool )                          #line 265


            B = State.S.pop ()                         #line 266


            A = State.S.pop ()                         #line 267

            State.S.push ( A <  B)                     #line 268

                                                       #line 269
                                                       #line 270


        case ">":                                      #line 271
            # ( a b -- bool )                          #line 272


            B = State.S.pop ()                         #line 273


            A = State.S.pop ()                         #line 274

            State.S.push ( A >  B)                     #line 275

                                                       #line 276
                                                       #line 277


        case "0=":                                     #line 278
            # ( a -- bool )                            #line 279


            a = State.S.pop ()                         #line 280

            State.S.push ( a ==  0)                    #line 281

                                                       #line 282
                                                       #line 283


        case "0<":                                     #line 284
            # ( a -- bool )                            #line 285


            a = State.S.pop ()                         #line 286

            State.S.push ( 0 <  a)                     #line 287

                                                       #line 288
                                                       #line 289


        case "0>":                                     #line 290
            # ( a -- bool )                            #line 291


            a = State.S.pop ()                         #line 292

            State.S.push ( 0 >  a)                     #line 293

                                                       #line 294
                                                       #line 295


        case "not":                                    #line 296
            # ( a -- bool )                            #line 297


            a = State.S.pop ()                         #line 298

            State.S.push (not  a)                      #line 299

                                                       #line 300
                                                       #line 301


        case "and":                                    #line 302
            # ( a b -- bool )                          #line 303


            b = State.S.pop ()                         #line 304


            a = State.S.pop ()                         #line 305

            State.S.push ( a and  b)                   #line 306

                                                       #line 307
                                                       #line 308


        case "or":                                     #line 309
            # ( a b -- bool )                          #line 310


            b = State.S.pop ()                         #line 311


            a = State.S.pop ()                         #line 312

            State.S.push ( a or  b)                    #line 313

                                                       #line 314
                                                       #line 315


        case ">r":                                     #line 316
            # ( a --  )                                #line 317


            a = State.S.pop ()                         #line 318

            State.R.append ( a)                        #line 319

                                                       #line 320
                                                       #line 321


        case "r>":                                     #line 322
            # ( -- x )                                 #line 323


            x = State.R.pop ()                         #line 324

            State.S.push ( x)                          #line 325

                                                       #line 326
                                                       #line 327


        case "i":                                      #line 328
            # ( -- i ) get current loop index from R stack #line 329


            i = State.R [-1]                           #line 330

            State.S.push ( i)                          #line 331

                                                       #line 332
                                                       #line 333


        case "i'":                                     #line 334
            # ( -- i ) get outer loop limit from R stack #line 335


            i = State.R [-2]                           #line 336

            State.S.push ( i)                          #line 337

                                                       #line 338
                                                       #line 339


        case "j":                                      #line 340
            # ( -- j ) get outer loop index from R stack #line 341


            j = State.R [-3]                           #line 342

            State.S.push ( j)                          #line 343

                                                       #line 344
                                                       #line 345


        case "swap":                                   #line 346
            # ( a b -- b a)                            #line 347
            x = Stack [-1]
            Stack [-1] = Stack [-2]
            Stack [-2] = x                             #line 348#line 352


        case "-":                                      #line 353
            # ( a b -- diff)                           #line 354


            B = State.S.pop ()                         #line 355


            A = State.S.pop ()                         #line 356

            State.S.push ( A- B)                       #line 357

                                                       #line 358


        case "/":                                      #line 359
            # ( a b -- div)                            #line 360

            xswap()                                    #line 361


            B = State.S.pop ()                         #line 362


            A = State.S.pop ()                         #line 363

            State.S.push ( B [A])                      #line 364

                                                       #line 365
                                                       #line 366


        case "word":                                   #line 367
            # (char -- string) Read in string delimited by char #line 368


            wanted = chr(State.S.pop ())               #line 369


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
                                                       #line 370

                                                       #line 371
                                                       #line 372
            # Example of state-smart word, which Brodie sez not to do. Sorry, Leo... #line 373
            # This sin allows it to be used the same way compiling or interactive. #line 374


        case "'":                                      #line 375
            # ( -- string) Read up to closing dquote, push to stack #line 376
            # A string in Forth begins with the word " (followed by a space) then all characters up to the next " #line 377
            # E.G. " abc"                              #line 378


            DQ =  34                                   #line 379

            State.S.push ( DQ)                         #line 380

            xword()                                    #line 381

            if State.compiling [-1] :
                                                       #line 382

                literalize()                           #line 383

                                                       #line 384


                                                       #line 385
                                                       #line 386


        case ".'":                                     #line 387
            # ( --) Print string.                      #line 388

            xquote()                                   #line 389

            print (State.S.pop (), end="")             #line 390

                                                       #line 391
                                                       #line 392
                                                       #line 393
                                                       #line 394


        case "(literal)":                              #line 395
            #⎩396⎭
            #   Inside definitions only, pushes compiled literal to stack ⎩397⎭
            #⎩398⎭
            #       Certain Forth words are only applicable inside compiled sequences of subroutines ⎩399⎭
            #       Literals are handled in different ways when interpreted when in the REPL vs⎩400⎭
            #       compiled into sequences of subrs ⎩401⎭
            #       In the REPL, when we encounter a literal, we simply push it onto the stack ⎩402⎭
            #       In the compiler, though, we have to create an instruction that pushes ⎩403⎭
            #	 the literal onto the stack. ⎩404⎭
            #	 Compiled code doesn't do what the REPL does, we have to hard-wire and ⎩405⎭
            #	 bake in code that pushes the literal when the time comes to run the sequence. ⎩406⎭
            #⎩407⎭
            #       This word - "(literal)" - is a simple case and one could actually type this ⎩408⎭
            #	 instruction into the REPL, but, that would be redundant.  Other kinds of words, ⎩409⎭
            #	 e.g. some control-flow words, tend to be messier and the code below only handles ⎩410⎭
            #	 the compiled aspects and ignores the REPL aspects ⎩411⎭
            #⎩412⎭
            #       "IP" is the current word index in a sequence of words being compiled. ⎩413⎭
            #                                          #line 414


            lit =  State.RAM [ State.IP]               #line 415

            State.S.push ( lit)                        #line 416

            State.IP =  State.IP+ 1 # move past this item (the literal) - we're done with it #line 417

                                                       #line 418
                                                       #line 419


        case "branch":                                 #line 420
            # This instruction appears only inside subroutine sequences, jump to address in next cell #line 421
            # This instruction is inserted into a subr sequence when compiling control-flow words, like "else" see below) #line 422

            State.IP =  State.RAM [ State.IP]          #line 423
            # normally, we just execute an instruction then move the IP sequentially forward by 1 unit, i.e. IP ⇐ IP + 1 #line 424
            #   in this case, though, we explicitly change the IP to some other value and don't just increment it #line 425

                                                       #line 426
                                                       #line 427


        case "0branch":                                #line 428
            # This instruction appears only inside subroutine sequences, jump on false to address in next cell #line 429


            test = bool (State.S.pop ())               #line 430

            if ( test):
                                                       #line 431

                State.IP =  State.IP+ 1                #line 432



            else:
                                                       #line 433

                State.IP =  State.RAM [ State.IP]      #line 434

                                                       #line 435


                                                       #line 436
                                                       #line 437
                                                       #line 438
            # "immediate" words are fully operational even when in compile mode. Some (not all) of these words are meant to⎩439⎭
            #      work /only/ in compile mode. At the REPL prompt ("interpret" mode), they produce unwanted results.⎩440⎭
            #    immediate words: xif, xelse, xthen, xquote, xcomment, xsemi⎩441⎭
            #    immediate words that only have meaning in compile mode: xif, xelse, xthen, xsemi⎩442⎭
            #                                          #line 443
                                                       #line 444
                                                       #line 445
            # IF, ELSE and THEN are "immediate" words - they should only be used inside of ":" (colon compiler) #line 446
                                                       #line 447
            # see diagram compiling-IF-THEN.drawio.png #line 448

        case "if":
            State.compiling.push (False)
            State.compiling = False                    #line 449
            # This instruction appears only inside subroutine sequences, ( f -- ) compile if test and branchFalse  #line 450
            # Step. 1: generate conditional branch to yet-unknown target1  #line 451


            branchFalseAddress =  _find( "0branch")    #line 452


            State.RAM.append ( branchFalseAddress) # insert branch-if-false opcode (word)  #line 453

            State.R.append (len (Stack.RAM)) # target1 onto r-stack as memo for later fixup  #line 454


            target1 =  -1                              #line 455


            State.RAM.append ( target1) # branch target will be fixed up later  #line 456
            # Step. 2: generate code for true branch - return to compiler which will compile the following words  #line 457
            # THEN or ELSE will do the fixup of target1  #line 458

                                                       #line 459
                                                       #line 460
            # see diagram compiling-IF-ELSE-THEN.drawio.png #line 461

            State.compiling = State.compiling.pop ()
        case "else":
            State.compiling.push (False)
            State.compiling = False                    #line 462
            # Step. 1: fixup target1 from IF-true, retrieving memo from R-stack #line 463


            target1 = State.R.pop ()                   #line 464

            State.RAM [ target1] = len (Stack.RAM)     #line 465
            # Step. 2: generate unconditional branch for preceding IF, creating new memo for target2 on R-stack #line 466


            brAddress =  _find( "branch")              #line 467

            State.R.append (len (Stack.RAM)) # target2 address on R-stack as memo for later fixup #line 468


            target2 =  -1                              #line 469


            State.RAM.append ( target2) # branch target will be fixed up later #line 470
            # Step. 3: generate code for false branch - return to compiler which will compile the following words #line 471
            # THEN will do the fixup of target2        #line 472

                                                       #line 473
                                                       #line 474
            # see diagrams compiling-IF-THEN.drawio.png and compiling-IF-ELSE-THEN.drawio.png #line 475

            State.compiling = State.compiling.pop ()
        case "then":
            State.compiling.push (False)
            State.compiling = False                    #line 476
            # Step. 1: fixup target (from IF or from ELSE, above), retrieving memo from R-stack #line 477


            target = State.R.pop ()                    #line 478

            State.RAM [ target] = len (Stack.RAM)      #line 479

                                                       #line 480
                                                       #line 481

            State.compiling = State.compiling.pop ()

        case "(do)":                                   #line 482
            # ( limit index --) Puts limit and index on return stack. #line 483

            xswap()                                    #line 484


            index = State.S.pop ()                     #line 485


            limit = State.S.pop ()                     #line 486

            State.R.append ( index)                    #line 487

            State.R.append ( limit)                    #line 488

                                                       #line 489
                                                       #line 490

        case "do":
            State.compiling.push (False)
            State.compiling = False                    #line 491
            # (  limit index --) Begin counted loop.   #line 492


            State.RAM.append ( _find( "(do)"))  # Push do loop handler. #line 493

            State.R.append (len (Stack.RAM))           # Push address to jump back to. #line 494

                                                       #line 495
                                                       #line 496

            State.compiling = State.compiling.pop ()

        case "(loop)":                                 #line 497
            # (  -- f) Determine if loop is done.      #line 498


            index = State.R.pop ()                     #line 499


            limit = State.R.pop ()                     #line 500


            cond = ( index >=  limit)                  #line 501

            State.S.push ( cond)                       #line 502

            if ( cond):
                # clean up rstack if index >= limit    #line 503

                State.R.pop ()                         #line 504

                State.R.pop ()                         #line 505

                                                       #line 506


                                                       #line 507
                                                       #line 508

        case "+loop":
            State.compiling.push (False)
            State.compiling = False                    #line 509
            # ( --) Close counted loop.                #line 510


            State.RAM.append ( _find( "(loop)"))   # Compile in loop test. #line 511


            State.RAM.append ( _find( "0branch"))  # Compile in branch check. #line 512


            State.RAM.append (State.R.pop ())           # Address to jump back to. #line 513

                                                       #line 514
                                                       #line 515

            State.compiling = State.compiling.pop ()
        case "loop":
            State.compiling.push (False)
            State.compiling = False                    #line 516
            # (  --) Close counted loop.               #line 517

            State.S.push ( 1)                          #line 518

            literalize()# Default loop increment for x_loop. #line 519


            State.RAM.append ( _find( "(loop)"))   # Compile in loop test. #line 520


            State.RAM.append ( _find( "0branch"))  # Compile in branch check. #line 521


            State.RAM.append (State.R.pop ())           # Address to jump back to. #line 522

                                                       #line 523
                                                       #line 524

            State.compiling = State.compiling.pop ()
        case "begin":
            State.compiling.push (False)
            State.compiling = False                    #line 525

            State.R.append (len (Stack.RAM))  # ( --) Start indefinite loop. #line 526

                                                       #line 527
                                                       #line 528

            State.compiling = State.compiling.pop ()
        case "until":
            State.compiling.push (False)
            State.compiling = False                    #line 529
            # (  f --) Close indefinite loop with test. #line 530


            State.RAM.append ( _find( "0branch"))  # Expects result of test on stack. #line 531


            State.RAM.append (State.R.pop ())           # Address to jump back to. #line 532

                                                       #line 533
                                                       #line 534
                                                       #line 535
                                                       #line 536
            #  "... 123 constant K ..."                #line 537
            #  at interpretation time: 123 is on the Stack, we have consumed "constant" from BUFF, BUFF now contains "K ..." #line 538
            #  invoke 'word' which parses "K" and pushed it. The stack becomes [... 123 "K"] #line 539
            #  pop "K", pop 123, create a new word called 'K' with its PFA set to 123 and its CFA set to a subr that⎩540⎭
            #       gets 123 from its PFA and pushes it onto the stack #line 541

            State.compiling = State.compiling.pop ()

        case "const":                                  #line 542
            #  get next word - the name - from BUFF    #line 543


            blank =  32                                #line 544

            State.S.push ( blank)                      #line 545

            xword()                                    #line 546
            #  stack is now: ( NNNN name -- )          #line 547


            name = State.S.pop ()                      #line 548


            value = State.S.pop ()                     #line 549


            normal =  0                                #line 550


            fobj =  code( name,  normal,  doconst)     #line 551


            State.RAM.append ( value)                  #line 552

                                                       #line 553
                                                       #line 554


        case ",":                                      #line 555

            comma(State.S.pop ())                      #line 556

                                                       #line 557
                                                       #line 558


        case "variable":                               #line 559


            blank =  32                                #line 560

            State.S.push ( blank)                      #line 561

            xword()                                    #line 562


            name = State.S.pop ()                      #line 563


            value = State.S.pop ()                     #line 564

            fvar( name,  value)                        #line 565

                                                       #line 566
                                                       #line 567


        case "dump":                                   #line 568


            n = int (State.S.pop ())                   #line 569


            start = int (State.S.pop ())               #line 570

            print ( "----------------------------------------------------------------", end="")#line 571


            a =  start                                 #line 572

            while ( a <  start+( min( n, ( len( State.RAM) - start)))):
                                                       #line 573

                print ( a, end="")                     #line 574

                print ( ": ", end="")                  #line 575

                print ( State.RAM [ a], end="")        #line 576

                print ()                               #line 577


                a =  a+ 1                              #line 578

                                                       #line 579


                                                       #line 580
                                                       #line 581


        case "!":                                      #line 582


            b = State.S.pop ()                         #line 583


            a = State.S.pop ()                         #line 584

            State.RAM [ b] =  a                        #line 585

                                                       #line 586
                                                       #line 587


        case "bye":# ( --) Leave interpreter

            raise SystemExit
                                                       #line 588
                                                       #line 589
                                                       #line 590


        case "find":                                   #line 591
            # "( name | -- (name 0)|(xt 1)|(xt -1)) Search for word name." #line 592
            # 3 possible results: 1. (name 0) if not found, 2. (xt 1) if found and word is immediate, 3. (xt -1) if found and word is normal #line 593

            State.S.push ( 32)                         #line 594

            xword()                                    #line 595


            found =  _find(State.S[-1])                #line 596

            if ( 0 ==  found):
                                                       #line 597

                State.S.push ( 0)                      #line 598



            else:
                                                       #line 599

                State.S.pop ()  # # Get rid of name on stack. #line 600

                State.S.push ( found)                  #line 601


                immediate =  -1                        #line 602

                if ( State.RAM [State.S[-1] - 1] &  1):

                    immediate =  1
                                                       #line 603


                State.S.push ( immediate)              #line 604

                                                       #line 605


                                                       #line 606
                                                       #line 607


        case "'":                                      #line 608
            # "( name -- xt|-1) Search for execution token of word name." #line 609

            State.S.push ( 32)                         #line 610

            xword()                                    #line 611


            name = State.S.pop ()                      #line 612


            found =  _find( name)                      #line 613

            State.S.push ( found)                      #line 614

                                                       #line 615
                                                       #line 616


        case "None":                                   #line 617


            State.S.append (None)                      #line 618

                                                       #line 619
                                                       #line 620


        case "words":                                  #line 621
            # print words in dictionary                #line 622


            x =  State.LAST                            #line 623

            while ( x >  -1):
                                                       #line 624

                print ( State.RAM [ x+ 1], end="")     #line 625

                print ( " ", end="")                   #line 626

                                                       #line 627


            print ()                                   #line 628

                                                       #line 629
                                                       #line 630
                                                       #line 631


        case "execute":                                #line 632
            # invoke given word                        #line 633


            wordAddress = State.S.pop ()               #line 634

            wordAddress()                              #line 635

                                                       #line 636
                                                       #line 637
                                                       #line 638


        case ":":                                      #line 639
            # ( name | --) Start compilation.          #line 640


            blank =  32                                #line 641

            State.S.push ( blank)                      #line 642

            xword()                                    #line 643


            name = State.S.pop ()                      #line 644

            code( name,  0,  doword)                   #line 645

            State.compiling [-1] = True                #line 646

                                                       #line 647
                                                       #line 648

        case ";":
            State.compiling.push (False)
            State.compiling = False                    #line 649
            # ( --) Finish definition.                 #line 650
                                                       #line 651


            State.RAM.append ( -1)  # Marker for end of definition. #line 652

            State.compiling [-1] = False               #line 653

                                                       #line 654
                                                       #line 655

            State.compiling = State.compiling.pop ()

        case "interpret":                              #line 656
            # ( string --) Execute word.               #line 657
                                                       #line 658

            find()                                     #line 659
            # 3 possible results from find:⎩660⎭
            #	  1. (name 0) if not found,⎩661⎭
            #	  2. (xt 1) if found and word is immediate,⎩662⎭
            #	  3. (xt -1) if found and word is normal #line 663


            result = State.S.pop ()

            foundimmediate = ( result ==  1)           #line 664


            item = State.S.pop ()

            foundnormal = ( result ==  -1)             #line 665


            notfound = ( result ==  0)                 #line 666


            found = ( foundimmediate or  foundnormal)  #line 667
                                                       #line 668

            if ( found):
                                                       #line 669

                if (State.compiling [-1]):
                                                       #line 670

                    if ( foundimmediate):
                                                       #line 671

                        exec( item)                    #line 672



                    else:
                                                       #line 673

                        compileword( item)             #line 674

                                                       #line 675
                                                       #line 676




                else:
                                                       #line 677

                    exec( item)                        #line 678

                                                       #line 679
                                                       #line 680




            else:
                                                       #line 681

                if (State.compiling [-1]):
                                                       #line 682

                    if (re.match(r"^-?\d*$",  item)):
                                                       #line 683

                        compileinteger( item)          #line 684



                    else:
                                                       #line 685

                        if (re.match(r"^-?d*\.?\d*$",  item)):
                                                       #line 686

                            compilefloat( item)        #line 687



                        else:
                                                       #line 688

                            returnFalse()              #line 689

                                                       #line 690
                                                       #line 691


                                                       #line 692
                                                       #line 693




                else:
                                                       #line 694

                    if (re.match(r"^-?\d*$",  item)):
                                                       #line 695

                        pushasinteger( item)           #line 696



                    else:
                                                       #line 697

                        if (re.match(r"^-?d*\.?\d*$",  item)):
                                                       #line 698

                            pushasfloat( item)         #line 699



                        else:
                                                       #line 700

                            returnFalse()              #line 701

                                                       #line 702
                                                       #line 703


                                                       #line 704
                                                       #line 705


                                                       #line 706
                                                       #line 707


                                                       #line 708
                                                       #line 709


            return  True                               #line 710

                                                       #line 711

                                                       #line 712
                                                       #line 713


                                                       #line 714
ok ()                                                  #line 715
                                                       #line 716