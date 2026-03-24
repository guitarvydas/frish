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
# fvget and fvset assume that the forth object (word) is a set of contiguous slots, each 1 machine word wide⎩2⎭
#    these functions use direct integer offsets to access the fields of the fojbect, whereas in higher level languages⎩3⎭
#    we'd use class fields instead - todo: fix this in the future (or not? at what point is customization better than⎩4⎭
#    generalization?)                                  #line 5
def fvget (name):
    global State                                       #line 6


    fobjaddress =  _find(State.S.pop ())               #line 7

    return  State.RAM [ fobjaddress+ 1]                #line 8

                                                       #line 9
                                                       #line 10

def fvset (name,v):
    global State                                       #line 11


    fobjaddress =  _find(State.S.pop ())               #line 12


    namefieldaddress =  fobjaddress+ 1                 #line 13

    State.RAM [ namefieldaddress] =  v                 #line 14

                                                       #line 15
                                                       #line 16
                                                       #line 17

def doword ():
    global State                                       #line 18
    #⎩19⎭
    #  Execute a colon-defined word using indirect threaded code interpretation.⎩20⎭
    #⎩21⎭
    #  This function implements the inner interpreter for threaded code execution.⎩22⎭
    #  Threaded code words store their definitions as arrays of code field addresses⎩23⎭
    #  (CFAs) in the parameter field area (PFA) immediately following the word header.⎩24⎭
    #⎩25⎭
    #  The execution model maintains two critical registers:⎩26⎭
    #⎩27⎭
    #  1. IP (Instruction Pointer): References the current position within the⎩28⎭
    #     threaded code array being interpreted. Since threaded words may invoke⎩29⎭
    #     other threaded words, IP must be preserved in a reentrant manner via⎩30⎭
    #     the return stack on each invocation.⎩31⎭
    #⎩32⎭
    #  2. W (Word Pointer): References the CFA of the currently executing primitive.⎩33⎭
    #     This global register serves an analogous function to 'self' in object-oriented⎩34⎭
    #     languages, enabling subroutines to access word header fields through fixed⎩35⎭
    #     offsets from the CFA.⎩36⎭
    #⎩37⎭
    #  Optimization rationale: W is positioned to reference the CFA rather than the⎩38⎭
    #  word header base. This design eliminates offset arithmetic for CFA access—the⎩39⎭
    #  most frequent header operation—at the cost of requiring offset adjustments⎩40⎭
    #  for other header fields (NFA: W-2, flags: W-1, PFA: W+1). This represents a⎩41⎭
    #  deliberate trade-off favoring the common case.⎩42⎭
    #⎩43⎭
    #  The inner interpreter loop performs the following operations:⎩44⎭
    #  - Fetch the next CFA from RAM[IP] into W (performing the first indirection)⎩45⎭
    #  - Increment IP to advance through the threaded code array⎩46⎭
    #  - Execute the primitive via RAM[W]() (performing the second indirection)⎩47⎭
    #⎩48⎭
    #  By caching the dereferenced CFA in W, we amortize the cost of double⎩49⎭
    #  indirection: both primitive execution and header field access within⎩50⎭
    #  subroutines utilize the same cached reference, avoiding redundant⎩51⎭
    #  dereferences. This is functionally equivalent to parameter passing in⎩52⎭
    #  object-oriented method invocation, but eliminates the overhead of⎩53⎭
    #  explicitly passing 'self' to each primitive.⎩54⎭
    #⎩55⎭
    #  Note: Ws state is only defined during primitive execution (within RAM[W]()).⎩56⎭
    #  Between loop iterations, W may reference a stale CFA, but this is⎩57⎭
    #  architecturally sound since W is unconditionally updated before each⎩58⎭
    #  primitive invocation.⎩59⎭
    #                                                  #line 60
                                                       #line 61

    State.R.append ( State.IP)                         #line 62

    State.IP =  State.W+ 1                             #line 63

    while ( -1!= State.RAM [ State.IP]):
                                                       #line 64

        State.W =  State.RAM [ State.IP]               #line 65

        State.IP =  State.IP+ 1                        #line 66

        State.R.push ( State.RAM [ State.W])
        _walk ()                                       #line 67

                                                       #line 68


    State.IP = State.R.pop ()                          #line 69

                                                       #line 70
                                                       #line 71
                                                       #line 72

def notfound (word):
    global State                                       #line 73


    State.S.clear()                                    #line 74


    State.R.clear()                                    #line 75

    print ( word, end="")                              #line 76

    print ( "?", end="")                               #line 77

    print ()                                           #line 78

                                                       #line 79
                                                       #line 80

def exec (xt):
    global State                                       #line 81
    # found and compiling and immediate                #line 82

    State.W =  xt                                      #line 83

    State.IP =  -1# Dummy to hold place in return stack. 	#line 84

    State.R.push ( State.RAM [ xt])
    _walk ()  # Execute code.                          #line 85

                                                       #line 86
                                                       #line 87

def compile_word (xt):
    global State                                       #line 88
    # found and not compiling                          #line 89

    State.W =  xt                                      #line 90

    State.IP =  -1# Dummy to hold place in return stack. 	#line 91

    State.R.push ( State.RAM [ xt])
    _walk ()  # Execute code.                          #line 92

                                                       #line 93
                                                       #line 94

def pushasinteger (word):
    global State                                       #line 95

    State.S.push (int ( word))                         #line 96

                                                       #line 97
                                                       #line 98

def pushasfloat (word):
    global State                                       #line 99

    State.S.push (float ( word))                       #line 100

                                                       #line 101
                                                       #line 102

def compileinteger (word):
    global State                                       #line 103

    pushasinteger( word)                               #line 104

    State.R.push ("literalize")
    _walk ()                                           #line 105

                                                       #line 106
                                                       #line 107

def compilefloat (word):
    global State                                       #line 108

    pushasfloat( word)                                 #line 109

    State.R.push ("literalize")
    _walk ()                                           #line 110

                                                       #line 111
                                                       #line 112

def code (name,flags,does):
    global State                                       #line 113
    # Add new word to RAM dictionary. We create a word (Forth "object") in RAM with 5 fields and extend the⎩114⎭
    #	the dictionary by linking back to the head of the dictionary list #line 115

    x =  len( State.RAM)                               #line 116
                                                       #line 117


    State.RAM.append ( State.LAST) # (LFA) link to previous word in dictionary list #line 118


    State.RAM.append ( name)       # (NFA) name of word #line 119


    State.RAM.append ( flags)      #       0 = normal word, 1 = immediate word #line 120


    State.RAM.append ( does)       # (CFA) function pointer that points to code that executes the word (a function pointer is now just a string (probably should be optimized to be a bytecode)) #line 121
                                                       #line 122

    State.LAST =  x                # LAST is the pointer to the head of the dictionary list, set it to point to⎩123⎭
    #					this new word                                #line 124

                                                       #line 125
                                                       #line 126

def literalize ():
    global State                                       #line 127
    # Compile literal into definition.                 #line 128


    State.RAM.append ( _find( "(literal)"))  ## Compile address of doliteral. #line 129


    State.RAM.append (State.S.pop ())             # # Compile literal value. #line 130

                                                       #line 131
                                                       #line 132

def xinterpret ():
    global State                                       #line 133

    State.R.push ("interpret")
    _walk ()                                           #line 134

    return State.S.pop ()                              #line 135

                                                       #line 136
                                                       #line 137

def ok ():
    global State                                       #line 138
    # ( --) Interaction loop -- REPL                   #line 139


    blank =  32                                        #line 140

    while  True:
                                                       #line 141


        State.BUFF = input("OK ")
        State.BUFP = 0
                                                       #line 142

        while not (State.BUFP >= len(State.BUFF)) :
                                                       #line 143

            xinterpret()                               #line 144

                                                       #line 145


                                                       #line 146


                                                       #line 147
                                                       #line 148

def doconst ():
    global State# method for const                     #line 149


    parameter =  State.RAM [ State.W+ 1]               #line 150

    State.S.push ( parameter)                          #line 151

                                                       #line 152
                                                       #line 153
                                                       #line 154

def docreate ():
    global State                                       #line 155


    parameterAddress =  len( State.RAM) + 4            #line 156

    State.S.push ( parameterAddress)                   #line 157

                                                       #line 158

def create (name):
    global State                                       #line 159


    normal =  0                                        #line 160

    code( name,  normal,  docreate)                    #line 161

                                                       #line 162

def comma (value):
    global State                                       #line 163


    State.RAM.append ( value)                          #line 164

                                                       #line 165
                                                       #line 166

def fvar (name,value):
    global State                                       #line 167

    create( name)                                      #line 168

    comma( value)                                      #line 169

                                                       #line 170
                                                       #line 171

def _find (name):
    global State                                       #line 172
    # "( name -- cfa|0) Find CFA of word name."        #line 173


    x =  State.LAST                                    #line 174

    while ( x >=  0):
                                                       #line 175
        # ## print(f"-- {x} : {RAM[x]}, {RAM[x + 1]}")  # Debug. #line 176

        if ( name ==  State.RAM [ x+ 1]):
            # # Match!                                 #line 177

            return  x+ 3                               #line 178



        else:
                                                       #line 179

            x =  State.RAM [ x]  # # Get next link.    #line 180

                                                       #line 181


                                                       #line 182


    return  0  # # Nothing found.                      #line 183

                                                       #line 184
                                                       #line 185

def debugok ():
    global State                                       #line 186
    # ( --) Interaction loop -- REPL                   #line 187


    blank =  32                                        #line 188


    State.BUFF = "7 ."
    State.BUFP = 0
                                                       #line 189

    while not (State.BUFP >= len(State.BUFF)) :
                                                       #line 190

        if ( interpret()):
                                                       #line 191

            print ( " ok", end="")                     #line 192

            print ()                                   #line 193

                                                       #line 194


        print ( State.BUFP, end="")
        print ( " -- ", end="")
        print ( State.BUFF, end="")
        print ()                                       #line 195

        State.R.push ("dots")
        _walk ()                                       #line 196

                                                       #line 197


    print ( State.BUFP, end="")
    print ( " == ", end="")
    print ( State.BUFF, end="")
    print ()                                           #line 198

    State.R.push ("dot")
    _walk ()                                           #line 199

    State.R.push ("dots")
    _walk ()                                           #line 200

                                                       #line 201
                                                       #line 202


def _walk ():
    global State
    opcode = State.R.pop ()
    match opcode:
        case "create":                                 #line 203


            blank =  32                                #line 204

            State.S.push ( blank)                      #line 205

            State.R.push ("word")
            _walk ()                                   #line 206


            name = State.S.pop ()                      #line 207

            create( name)                              #line 208

                                                       #line 209
                                                       #line 210


        case "drop":                                   #line 211
            # ( a -- )                                 #line 212

            State.S.pop ()                             #line 213

                                                       #line 214
                                                       #line 215


        case "dup":                                    #line 216
            # ( a -- a a )                             #line 217


            A = State.S.pop ()                         #line 218

            State.S.push ( A)                          #line 219

            State.S.push ( A)                          #line 220

                                                       #line 221
                                                       #line 222


        case "negate":                                 #line 223
            # ( n -- (-n) )                            #line 224


            n = State.S.pop ()                         #line 225

            State.S.push ( -n)                         #line 226

                                                       #line 227
                                                       #line 228


        case "emit":                                   #line 229
            # ( c -- ) emit specified character        #line 230


            c = State.S.pop ()                         #line 231

            print (chr (int ( c)), end="")             #line 232

                                                       #line 233
                                                       #line 234


        case "cr":
            print ()
                                                       #line 235


        case ".":# ( n --) Print TOS
            print (State.S.pop (), end="")
            print ()
                                                       #line 236


        case ".s":# ( --) Print stack contents
            print (State.S, end="")
            print ()
                                                       #line 237
                                                       #line 238


        case "+":                                      #line 239
            # ( a b -- sum)                            #line 240


            B = State.S.pop ()                         #line 241


            A = State.S.pop ()                         #line 242

            State.S.push ( A+ B)                       #line 243

                                                       #line 244
                                                       #line 245


        case "*":                                      #line 246
            # ( a b -- product )                       #line 247


            B = State.S.pop ()                         #line 248


            A = State.S.pop ()                         #line 249

            State.S.push ( A* B)                       #line 250

                                                       #line 251
                                                       #line 252


        case "=":                                      #line 253
            # ( a b -- bool )                          #line 254


            B = State.S.pop ()                         #line 255


            A = State.S.pop ()                         #line 256

            State.S.push ( A ==  B)                    #line 257

                                                       #line 258
                                                       #line 259


        case "<":                                      #line 260
            # ( a b -- bool )                          #line 261


            B = State.S.pop ()                         #line 262


            A = State.S.pop ()                         #line 263

            State.S.push ( A <  B)                     #line 264

                                                       #line 265
                                                       #line 266


        case ">":                                      #line 267
            # ( a b -- bool )                          #line 268


            B = State.S.pop ()                         #line 269


            A = State.S.pop ()                         #line 270

            State.S.push ( A >  B)                     #line 271

                                                       #line 272
                                                       #line 273


        case "0=":                                     #line 274
            # ( a -- bool )                            #line 275


            a = State.S.pop ()                         #line 276

            State.S.push ( a ==  0)                    #line 277

                                                       #line 278
                                                       #line 279


        case "0<":                                     #line 280
            # ( a -- bool )                            #line 281


            a = State.S.pop ()                         #line 282

            State.S.push ( 0 <  a)                     #line 283

                                                       #line 284
                                                       #line 285


        case "0>":                                     #line 286
            # ( a -- bool )                            #line 287


            a = State.S.pop ()                         #line 288

            State.S.push ( 0 >  a)                     #line 289

                                                       #line 290
                                                       #line 291


        case "not":                                    #line 292
            # ( a -- bool )                            #line 293


            a = State.S.pop ()                         #line 294

            State.S.push (not  a)                      #line 295

                                                       #line 296
                                                       #line 297


        case "and":                                    #line 298
            # ( a b -- bool )                          #line 299


            b = State.S.pop ()                         #line 300


            a = State.S.pop ()                         #line 301

            State.S.push ( a and  b)                   #line 302

                                                       #line 303
                                                       #line 304


        case "or":                                     #line 305
            # ( a b -- bool )                          #line 306


            b = State.S.pop ()                         #line 307


            a = State.S.pop ()                         #line 308

            State.S.push ( a or  b)                    #line 309

                                                       #line 310
                                                       #line 311


        case ">r":                                     #line 312
            # ( a --  )                                #line 313


            a = State.S.pop ()                         #line 314

            State.R.append ( a)                        #line 315

                                                       #line 316
                                                       #line 317


        case "r>":                                     #line 318
            # ( -- x )                                 #line 319


            x = State.R.pop ()                         #line 320

            State.S.push ( x)                          #line 321

                                                       #line 322
                                                       #line 323


        case "i":                                      #line 324
            # ( -- i ) get current loop index from R stack #line 325


            i = State.R [-1]                           #line 326

            State.S.push ( i)                          #line 327

                                                       #line 328
                                                       #line 329


        case "i'":                                     #line 330
            # ( -- i ) get outer loop limit from R stack #line 331


            i = State.R [-2]                           #line 332

            State.S.push ( i)                          #line 333

                                                       #line 334
                                                       #line 335


        case "j":                                      #line 336
            # ( -- j ) get outer loop index from R stack #line 337


            j = State.R [-3]                           #line 338

            State.S.push ( j)                          #line 339

                                                       #line 340
                                                       #line 341


        case "swap":                                   #line 342
            # ( a b -- b a)                            #line 343


            B = State.S.pop ()                         #line 344


            A = State.S.pop ()                         #line 345

            State.S.push ( B)                          #line 346

            State.S.push ( A)                          #line 347

                                                       #line 348


        case "-":                                      #line 349
            # ( a b -- diff)                           #line 350


            B = State.S.pop ()                         #line 351


            A = State.S.pop ()                         #line 352

            State.S.push ( A- B)                       #line 353

                                                       #line 354


        case "/":                                      #line 355
            # ( a b -- div)                            #line 356

            State.R.push ("swap")
            _walk ()                                   #line 357


            B = State.S.pop ()                         #line 358


            A = State.S.pop ()                         #line 359

            State.S.push ( B [A])                      #line 360

                                                       #line 361
                                                       #line 362


        case "word":                                   #line 363
            # (char -- string) Read in string delimited by char #line 364


            wanted = chr(State.S.pop ())               #line 365


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
                                                       #line 366

                                                       #line 367
                                                       #line 368
            # Example of state-smart word, which Brodie sez not to do. Sorry, Leo... #line 369
            # This sin allows it to be used the same way compiling or interactive. #line 370


        case "'":                                      #line 371
            # ( -- string) Read up to closing dquote, push to stack #line 372
            # A string in Forth begins with the word " (followed by a space) then all characters up to the next " #line 373
            # E.G. " abc"                              #line 374


            DQ =  34                                   #line 375

            State.S.push ( DQ)                         #line 376

            State.R.push ("word")
            _walk ()                                   #line 377

            if State.compiling [-1] :
                                                       #line 378

                literalize()                           #line 379

                                                       #line 380


                                                       #line 381
                                                       #line 382


        case ".'":                                     #line 383
            # ( --) Print string.                      #line 384

            State.R.push ("quote")
            _walk ()                                   #line 385

            print (State.S.pop (), end="")             #line 386

                                                       #line 387
                                                       #line 388
                                                       #line 389
                                                       #line 390


        case "(literal)":                              #line 391
            #⎩392⎭
            #   Inside definitions only, pushes compiled literal to stack ⎩393⎭
            #⎩394⎭
            #       Certain Forth words are only applicable inside compiled sequences of subroutines ⎩395⎭
            #       Literals are handled in different ways when interpreted when in the REPL vs⎩396⎭
            #       compiled into sequences of subrs ⎩397⎭
            #       In the REPL, when we encounter a literal, we simply push it onto the stack ⎩398⎭
            #       In the compiler, though, we have to create an instruction that pushes ⎩399⎭
            #	 the literal onto the stack. ⎩400⎭
            #	 Compiled code doesn't do what the REPL does, we have to hard-wire and ⎩401⎭
            #	 bake in code that pushes the literal when the time comes to run the sequence. ⎩402⎭
            #⎩403⎭
            #       This word - "(literal)" - is a simple case and one could actually type this ⎩404⎭
            #	 instruction into the REPL, but, that would be redundant.  Other kinds of words, ⎩405⎭
            #	 e.g. some control-flow words, tend to be messier and the code below only handles ⎩406⎭
            #	 the compiled aspects and ignores the REPL aspects ⎩407⎭
            #⎩408⎭
            #       "IP" is the current word index in a sequence of words being compiled. ⎩409⎭
            #                                          #line 410


            lit =  State.RAM [ State.IP]               #line 411

            State.S.push ( lit)                        #line 412

            State.IP =  State.IP+ 1 # move past this item (the literal) - we're done with it #line 413

                                                       #line 414
                                                       #line 415


        case "branch":                                 #line 416
            # This instruction appears only inside subroutine sequences, jump to address in next cell #line 417
            # This instruction is inserted into a subr sequence when compiling control-flow words, like "else" see below) #line 418

            State.IP =  State.RAM [ State.IP]          #line 419
            # normally, we just execute an instruction then move the IP sequentially forward by 1 unit, i.e. IP ⇐ IP + 1 #line 420
            #   in this case, though, we explicitly change the IP to some other value and don't just increment it #line 421

                                                       #line 422
                                                       #line 423


        case "0branch":                                #line 424
            # This instruction appears only inside subroutine sequences, jump on false to address in next cell #line 425


            test = bool (State.S.pop ())               #line 426

            if ( test):
                                                       #line 427

                State.IP =  State.IP+ 1                #line 428



            else:
                                                       #line 429

                State.IP =  State.RAM [ State.IP]      #line 430

                                                       #line 431


                                                       #line 432
                                                       #line 433
                                                       #line 434
            # "immediate" words are fully operational even when in compile mode. Some (not all) of these words are meant to⎩435⎭
            #      work /only/ in compile mode. At the REPL prompt ("interpret" mode), they produce unwanted results.⎩436⎭
            #    immediate words: xif, xelse, xthen, xquote, xcomment, xsemi⎩437⎭
            #    immediate words that only have meaning in compile mode: xif, xelse, xthen, xsemi⎩438⎭
            #                                          #line 439
                                                       #line 440
                                                       #line 441
            # IF, ELSE and THEN are "immediate" words - they should only be used inside of ":" (colon compiler) #line 442
                                                       #line 443
            # see diagram compiling-IF-THEN.drawio.png #line 444

        case "if":
            State.compiling.push (False)
            State.compiling = False                    #line 445
            # This instruction appears only inside subroutine sequences, ( f -- ) compile if test and branchFalse  #line 446
            # Step. 1: generate conditional branch to yet-unknown target1  #line 447


            branchFalseAddress =  _find( "0branch")    #line 448


            State.RAM.append ( branchFalseAddress) # insert branch-if-false opcode (word)  #line 449

            State.R.append (len (Stack.RAM)) # target1 onto r-stack as memo for later fixup  #line 450


            target1 =  -1                              #line 451


            State.RAM.append ( target1) # branch target will be fixed up later  #line 452
            # Step. 2: generate code for true branch - return to compiler which will compile the following words  #line 453
            # THEN or ELSE will do the fixup of target1  #line 454

                                                       #line 455
                                                       #line 456
            # see diagram compiling-IF-ELSE-THEN.drawio.png #line 457

            State.compiling = State.compiling.pop ()
        case "else":
            State.compiling.push (False)
            State.compiling = False                    #line 458
            # Step. 1: fixup target1 from IF-true, retrieving memo from R-stack #line 459


            target1 = State.R.pop ()                   #line 460

            State.RAM [ target1] = len (Stack.RAM)     #line 461
            # Step. 2: generate unconditional branch for preceding IF, creating new memo for target2 on R-stack #line 462


            brAddress =  _find( "branch")              #line 463

            State.R.append (len (Stack.RAM)) # target2 address on R-stack as memo for later fixup #line 464


            target2 =  -1                              #line 465


            State.RAM.append ( target2) # branch target will be fixed up later #line 466
            # Step. 3: generate code for false branch - return to compiler which will compile the following words #line 467
            # THEN will do the fixup of target2        #line 468

                                                       #line 469
                                                       #line 470
            # see diagrams compiling-IF-THEN.drawio.png and compiling-IF-ELSE-THEN.drawio.png #line 471

            State.compiling = State.compiling.pop ()
        case "then":
            State.compiling.push (False)
            State.compiling = False                    #line 472
            # Step. 1: fixup target (from IF or from ELSE, above), retrieving memo from R-stack #line 473


            target = State.R.pop ()                    #line 474

            State.RAM [ target] = len (Stack.RAM)      #line 475

                                                       #line 476
                                                       #line 477

            State.compiling = State.compiling.pop ()

        case "(do)":                                   #line 478
            # ( limit index --) Puts limit and index on return stack. #line 479

            State.R.push ("swap")
            _walk ()                                   #line 480


            index = State.S.pop ()                     #line 481


            limit = State.S.pop ()                     #line 482

            State.R.append ( index)                    #line 483

            State.R.append ( limit)                    #line 484

                                                       #line 485
                                                       #line 486

        case "do":
            State.compiling.push (False)
            State.compiling = False                    #line 487
            # (  limit index --) Begin counted loop.   #line 488


            State.RAM.append ( _find( "(do)"))  # Push do loop handler. #line 489

            State.R.append (len (Stack.RAM))           # Push address to jump back to. #line 490

                                                       #line 491
                                                       #line 492

            State.compiling = State.compiling.pop ()

        case "(loop)":                                 #line 493
            # (  -- f) Determine if loop is done.      #line 494


            index = State.R.pop ()                     #line 495


            limit = State.R.pop ()                     #line 496


            cond = ( index >=  limit)                  #line 497

            State.S.push ( cond)                       #line 498

            if ( cond):
                # clean up rstack if index >= limit    #line 499

                State.R.pop ()                         #line 500

                State.R.pop ()                         #line 501

                                                       #line 502


                                                       #line 503
                                                       #line 504

        case "+loop":
            State.compiling.push (False)
            State.compiling = False                    #line 505
            # ( --) Close counted loop.                #line 506


            State.RAM.append ( _find( "(loop)"))   # Compile in loop test. #line 507


            State.RAM.append ( _find( "0branch"))  # Compile in branch check. #line 508


            State.RAM.append (State.R.pop ())           # Address to jump back to. #line 509

                                                       #line 510
                                                       #line 511

            State.compiling = State.compiling.pop ()
        case "loop":
            State.compiling.push (False)
            State.compiling = False                    #line 512
            # (  --) Close counted loop.               #line 513

            State.S.push ( 1)                          #line 514

            State.R.push ("literalize")
            _walk ()# Default loop increment for x_loop. #line 515


            State.RAM.append ( _find( "(loop)"))   # Compile in loop test. #line 516


            State.RAM.append ( _find( "0branch"))  # Compile in branch check. #line 517


            State.RAM.append (State.R.pop ())           # Address to jump back to. #line 518

                                                       #line 519
                                                       #line 520

            State.compiling = State.compiling.pop ()
        case "begin":
            State.compiling.push (False)
            State.compiling = False                    #line 521

            State.R.append (len (Stack.RAM))  # ( --) Start indefinite loop. #line 522

                                                       #line 523
                                                       #line 524

            State.compiling = State.compiling.pop ()
        case "until":
            State.compiling.push (False)
            State.compiling = False                    #line 525
            # (  f --) Close indefinite loop with test. #line 526


            State.RAM.append ( _find( "0branch"))  # Expects result of test on stack. #line 527


            State.RAM.append (State.R.pop ())           # Address to jump back to. #line 528

                                                       #line 529
                                                       #line 530
                                                       #line 531
                                                       #line 532
            #  "... 123 constant K ..."                #line 533
            #  at interpretation time: 123 is on the Stack, we have consumed "constant" from BUFF, BUFF now contains "K ..." #line 534
            #  invoke 'word' which parses "K" and pushed it. The stack becomes [... 123 "K"] #line 535
            #  pop "K", pop 123, create a new word called 'K' with its PFA set to 123 and its CFA set to a subr that⎩536⎭
            #       gets 123 from its PFA and pushes it onto the stack #line 537

            State.compiling = State.compiling.pop ()

        case "const":                                  #line 538
            #  get next word - the name - from BUFF    #line 539


            blank =  32                                #line 540

            State.S.push ( blank)                      #line 541

            State.R.push ("word")
            _walk ()                                   #line 542
            #  stack is now: ( NNNN name -- )          #line 543


            name = State.S.pop ()                      #line 544


            value = State.S.pop ()                     #line 545


            normal =  0                                #line 546


            fobj =  code( name,  normal,  doconst)     #line 547


            State.RAM.append ( value)                  #line 548

                                                       #line 549
                                                       #line 550


        case ",":                                      #line 551

            comma(State.S.pop ())                      #line 552

                                                       #line 553
                                                       #line 554


        case "variable":                               #line 555


            blank =  32                                #line 556

            State.S.push ( blank)                      #line 557

            State.R.push ("word")
            _walk ()                                   #line 558


            name = State.S.pop ()                      #line 559


            value = State.S.pop ()                     #line 560

            fvar( name,  value)                        #line 561

                                                       #line 562
                                                       #line 563


        case "dump":                                   #line 564


            n = int (State.S.pop ())                   #line 565


            start = int (State.S.pop ())               #line 566

            print ( "----------------------------------------------------------------", end="")#line 567


            a =  start                                 #line 568

            while ( a <  start+( min( n, ( len( State.RAM) - start)))):
                                                       #line 569

                print ( a, end="")                     #line 570

                print ( ": ", end="")                  #line 571

                print ( State.RAM [ a], end="")        #line 572

                print ()                               #line 573


                a =  a+ 1                              #line 574

                                                       #line 575


                                                       #line 576
                                                       #line 577


        case "!":                                      #line 578


            b = State.S.pop ()                         #line 579


            a = State.S.pop ()                         #line 580

            State.RAM [ b] =  a                        #line 581

                                                       #line 582
                                                       #line 583


        case "bye":# ( --) Leave interpreter

            raise SystemExit
                                                       #line 584
                                                       #line 585
                                                       #line 586


        case "find":                                   #line 587
            # "( name | -- (name 0)|(xt 1)|(xt -1)) Search for word name." #line 588
            # 3 possible results: 1. (name 0) if not found, 2. (xt 1) if found and word is immediate, 3. (xt -1) if found and word is normal #line 589

            State.S.push ( 32)                         #line 590

            State.R.push ("word")
            _walk ()                                   #line 591


            found =  _find(State.S[-1])                #line 592

            if ( 0 ==  found):
                                                       #line 593

                State.S.push ( 0)                      #line 594



            else:
                                                       #line 595

                State.S.pop ()  # # Get rid of name on stack. #line 596

                State.S.push ( found)                  #line 597


                immediate =  -1                        #line 598

                if ( State.RAM [State.S[-1] - 1] &  1):

                    immediate =  1
                                                       #line 599


                State.S.push ( immediate)              #line 600

                                                       #line 601


                                                       #line 602
                                                       #line 603


        case "'":                                      #line 604
            # "( name -- xt|-1) Search for execution token of word name." #line 605

            State.S.push ( 32)                         #line 606

            State.R.push ("word")
            _walk ()                                   #line 607


            name = State.S.pop ()                      #line 608


            found =  _find( name)                      #line 609

            State.S.push ( found)                      #line 610

                                                       #line 611
                                                       #line 612


        case "None":                                   #line 613


            State.S.append (None)                      #line 614

                                                       #line 615
                                                       #line 616


        case "words":                                  #line 617
            # print words in dictionary                #line 618


            x =  State.LAST                            #line 619

            while ( x >  -1):
                                                       #line 620

                print ( State.RAM [ x+ 1], end="")     #line 621

                print ( " ", end="")                   #line 622

                                                       #line 623


            print ()                                   #line 624

                                                       #line 625
                                                       #line 626
                                                       #line 627


        case "execute":                                #line 628
            # invoke given word                        #line 629


            wordAddress = State.S.pop ()               #line 630

            State.R.push ( wordAddress)
            _walk ()                                   #line 631

                                                       #line 632
                                                       #line 633
                                                       #line 634


        case ":":                                      #line 635
            # ( name | --) Start compilation.          #line 636


            blank =  32                                #line 637

            State.S.push ( blank)                      #line 638

            State.R.push ("word")
            _walk ()                                   #line 639


            name = State.S.pop ()                      #line 640

            code( name,  0,  doword)                   #line 641

            State.compiling [-1] = True                #line 642

                                                       #line 643
                                                       #line 644

        case ";":
            State.compiling.push (False)
            State.compiling = False                    #line 645
            # ( --) Finish definition.                 #line 646
                                                       #line 647


            State.RAM.append ( -1)  # Marker for end of definition. #line 648

            State.compiling [-1] = False               #line 649

                                                       #line 650
                                                       #line 651

            State.compiling = State.compiling.pop ()

        case "interpret":                              #line 652
            # ( string --) Execute word.               #line 653
                                                       #line 654

            State.R.push ("find")
            _walk ()                                   #line 655
            # 3 possible results from find:⎩656⎭
            #	  1. (name 0) if not found,⎩657⎭
            #	  2. (xt 1) if found and word is immediate,⎩658⎭
            #	  3. (xt -1) if found and word is normal #line 659


            result = State.S.pop ()

            foundimmediate = ( result ==  1)           #line 660


            item = State.S.pop ()

            foundnormal = ( result ==  -1)             #line 661


            notfound = ( result ==  0)                 #line 662


            found = ( foundimmediate or  foundnormal)  #line 663
                                                       #line 664

            if ( found):
                                                       #line 665

                if (State.compiling [-1]):
                                                       #line 666

                    if ( foundimmediate):
                                                       #line 667

                        exec( item)                    #line 668



                    else:
                                                       #line 669

                        compileword( item)             #line 670

                                                       #line 671
                                                       #line 672




                else:
                                                       #line 673

                    exec( item)                        #line 674

                                                       #line 675
                                                       #line 676




            else:
                                                       #line 677

                if (State.compiling [-1]):
                                                       #line 678

                    if (re.match(r"^-?\d*$",  item)):
                                                       #line 679

                        compileinteger( item)          #line 680



                    else:
                                                       #line 681

                        if (re.match(r"^-?d*\.?\d*$",  item)):
                                                       #line 682

                            compilefloat( item)        #line 683



                        else:
                                                       #line 684

                            State.S.append (False)     #line 685

                                                       #line 686
                                                       #line 687


                                                       #line 688
                                                       #line 689




                else:
                                                       #line 690

                    if (re.match(r"^-?\d*$",  item)):
                                                       #line 691

                        pushasinteger( item)           #line 692



                    else:
                                                       #line 693

                        if (re.match(r"^-?d*\.?\d*$",  item)):
                                                       #line 694

                            pushasfloat( item)         #line 695



                        else:
                                                       #line 696

                            State.S.append (False)     #line 697

                                                       #line 698
                                                       #line 699


                                                       #line 700
                                                       #line 701


                                                       #line 702
                                                       #line 703


                                                       #line 704
                                                       #line 705


            State.S.append (True)                      #line 706
                                                       #line 707

                                                       #line 708
                                                       #line 709
                                                       #line 710




code( "create",  0,  "create")

code( "drop",  0,  "drop")

code( "dup",  0,  "dup")

code( "negate",  0,  "negate")

code( "emit",  0,  "emit")

code( "cr",  0,  "cr")

code( ".",  0,  ".")

code( ".s",  0,  ".s")

code( "+",  0,  "+")

code( "*",  0,  "*")

code( "=",  0,  "=")

code( "<",  0,  "<")

code( ">",  0,  ">")

code( "0=",  0,  "0=")

code( "0<",  0,  "0<")

code( "0>",  0,  "0>")

code( "not",  0,  "not")

code( "and",  0,  "and")

code( "or",  0,  "or")

code( ">r",  0,  ">r")

code( "r>",  0,  "r>")

code( "i",  0,  "i")

code( "i'",  0,  "i'")

code( "j",  0,  "j")

code( "swap",  0,  "swap")

code( "-",  0,  "-")

code( "/",  0,  "/")

code( "word",  0,  "word")

code( "'",  0,  "'")

code( ".'",  0,  ".'")

code( "(literal)",  0,  "(literal)")

code( "branch",  0,  "branch")

code( "0branch",  0,  "0branch")

code( "if",  1,  "if")

code( "else",  1,  "else")

code( "then",  1,  "then")

code( "(do)",  0,  "(do)")

code( "do",  1,  "do")

code( "(loop)",  0,  "(loop)")

code( "+loop",  1,  "+loop")

code( "loop",  1,  "loop")

code( "begin",  1,  "begin")

code( "until",  1,  "until")

code( "const",  0,  "const")

code( ",",  0,  ",")

code( "variable",  0,  "variable")

code( "dump",  0,  "dump")

code( "!",  0,  "!")

code( "bye",  0,  "bye")

code( "find",  0,  "find")

code( "'",  0,  "'")

code( "None",  0,  "None")

code( "words",  0,  "words")

code( "execute",  0,  "execute")

code( ":",  0,  ":")

code( ";",  1,  ";")

code( "interpret",  0,  "interpret")                   #line 711

ok()                                                   #line 712
                                                       #line 713