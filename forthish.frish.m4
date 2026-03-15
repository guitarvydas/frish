deffunction code (name, flags, does) {
    ⌈ Add new word to RAM dictionary. We create a word (Forth "object") in RAM with 5 fields and extend the
      the dictionary by linking back to the head of the dictionary list ⌉
    x ⇐ %funcall len (State.RAM)

    %ram+ (State.LAST) ⌈ (LFA) link to previous word in dictionary list ⌉
    %ram+ (name)       ⌈ (NFA) name of word ⌉
    %ram+ (flags)      ⌈       0 = normal word, 1 = immediate word ⌉
    %ram+ (does)       ⌈ (CFA) function pointer that points to code that executes the word ⌉

    State.LAST ⇐ x                ⌈ LAST is the pointer to the head of the dictionary list, set it to point to
                                      this new word ⌉
}

defsubr xdrop "drop" {
    ⌈ ( a -- ) ⌉
    %pop
}

defsubr xdup "dup" {
    ⌈ ( a -- a a ) ⌉
    deftemp A ⇐ %pop
    %push (A)
    %push (A)
}

defsubr xnegate "negate" {
    ⌈ ( n -- (-n) ) ⌉
    deftemp n ⇐ %pop
    %push (-n)
}

defsubr xemit "emit" {
    ⌈ ( c -- ) emit specified character ⌉
    deftemp c ⇐ %pop
    %printAsCharacter (c)
}

defsubr xcr "cr" { %eol }
defsubr xdot "." { ⌈ ( n --) Print TOS ⌉ %print (%pop) %eol }
defsubr xdots ".s" { ⌈ ( --) Print stack contents ⌉ %print (%stack) %eol }

defsubr xadd "+" {
    ⌈ ( a b -- sum) ⌉
    deftemp B ⇐ %pop
    deftemp A ⇐ %pop
    %push (A + B)
}

defsubr xmul "*" {
    ⌈ ( a b -- product ) ⌉
    deftemp B ⇐ %pop
    deftemp A ⇐ %pop
    %push (A * B)
}

defsubr xeq "=" {
    ⌈ ( a b -- bool ) ⌉
    deftemp B ⇐ %pop
    deftemp A ⇐ %pop
    %push (A = B)
}

defsubr xlt "<" {
    ⌈ ( a b -- bool ) ⌉
    deftemp B ⇐ %pop
    deftemp A ⇐ %pop
    %push (A < B)
}

defsubr xgt ">" {
    ⌈ ( a b -- bool ) ⌉
    deftemp B ⇐ %pop
    deftemp A ⇐ %pop
    %push (A > B)
}

defsubr xeq0 "0=" {
    ⌈ ( a -- bool ) ⌉
    deftemp a ⇐ %pop
    %push (a = 0)
}

defsubr x0lt "0<"  {
    ⌈ ( a -- bool ) ⌉
    deftemp a ⇐ %pop
    %push (0 < a)
}

defsubr x0gt "0>" {
    ⌈ ( a -- bool ) ⌉
    deftemp a ⇐ %pop
    %push (0 > a)
}

defsubr xnot "not" {
    ⌈ ( a -- bool ) ⌉
    deftemp a ⇐ %pop
    %push (not a)
}

defsubr xand "and" {
    ⌈ ( a b -- bool ) ⌉
    deftemp b ⇐ %pop
    deftemp a ⇐ %pop
    %push (a and b)
}

defsubr xor "or" {
    ⌈ ( a b -- bool ) ⌉
    deftemp b ⇐ %pop
    deftemp a ⇐ %pop
    %push (a or b)
}

defsubr xStoR ">r" {
    ⌈ ( a --  ) ⌉
    deftemp a ⇐ %pop
    %rpush (a)
}

defsubr xRtoS "r>" {
    ⌈ ( -- x ) ⌉
    deftemp x ⇐ %rpop
    %push (x)
}

defsubr xi "i" {
    ⌈ ( -- i ) get current loop index from R stack ⌉
    deftemp i ⇐ %rtop
    %push (i)
}

defsubr xiquote "i'" {
    ⌈ ( -- i ) get outer loop limit from R stack ⌉
    deftemp i ⇐ %rsecond
    %push (i)
}

defsubr xj "j" {
    ⌈ ( -- j ) get outer loop index from R stack ⌉
    deftemp j ⇐ %rthird
    %push (j)
}

defsubr xswap "swap" {
    ⌈ ( a b -- b a) ⌉
    deftemp B ⇐ %pop
    deftemp A ⇐ %pop
    %push (B)
    %push (A)
}
defsubr xsub "-" {
    ⌈ ( a b -- diff) ⌉
    deftemp B ⇐ %pop
    deftemp A ⇐ %pop
    %push (A - B)
}
defsubr xdiv "/" {
    ⌈ ( a b -- div) ⌉
    @xswap
    deftemp B ⇐ %pop
    deftemp A ⇐ %pop
    %push (B / A)
}

defsubr xword "word" {
    ⌈ (char -- string) Read in string delimited by char ⌉
    deftemp wanted ⇐ %popchar
    %scanfor (wanted)
}

⌈ Example of state-smart word, which Brodie sez not to do. Sorry, Leo... ⌉
⌈ This sin allows it to be used the same way compiling or interactive. ⌉
defsubr xquote "'" {
    ⌈ ( -- string) Read up to closing dquote, push to stack ⌉
    ⌈ A string in Forth begins with the word " (followed by a space) then all characters up to the next " ⌉
    ⌈ E.G. " abc" ⌉
    defsynonym DQ ≡ 34
    %push (DQ)
    @xword
    if %incompilingstate {
        %funcall literalize ()
    }
}

defsubr xdotquote ".'" {
    ⌈ ( --) Print string. ⌉
    @xquote
    %print (%pop)
}



defsubr xdoliteral "(literal)" {
    ⌈
 Inside definitions only, pushes compiled literal to stack 
    
     Certain Forth words are only applicable inside compiled sequences of subroutines 
     Literals are handled in different ways when interpreted when in the REPL vs
     compiled into sequences of subrs 
     In the REPL, when we encounter a literal, we simply push it onto the stack 
     In the compiler, though, we have to create an instruction that pushes 
       the literal onto the stack. 
       Compiled code doesn't do what the REPL does, we have to hard-wire and 
       bake in code that pushes the literal when the time comes to run the sequence. 

     This word - "(literal)" - is a simple case and one could actually type this 
       instruction into the REPL, but, that would be redundant.  Other kinds of words, 
       e.g. some control-flow words, tend to be messier and the code below only handles 
       the compiled aspects and ignores the REPL aspects 

     "IP" is the current word index in a sequence of words being compiled. 
⌉
    defsynonym lit ≡ State.RAM [State.IP]
    %push (lit)
    State.IP ⇐ State.IP + 1 ⌈ move past this item (the literal) - we're done with it ⌉
}

deffunction literalize () {
    ⌈ Compile literal into definition. ⌉
    %ram+ (%funcall _find ("(literal)"))  ⌈# Compile address of doliteral. ⌉
    %ram+ (%pop)             ⌈ # Compile literal value. ⌉
}

defsubr xbranch "branch" {
    ⌈ This instruction appears only inside subroutine sequences, jump to address in next cell ⌉
    ⌈ This instruction is inserted into a subr sequence when compiling control-flow words, like "else" see below) ⌉
    State.IP ⇐ State.RAM [State.IP]
    ⌈ normally, we just execute an instruction then move the IP sequentially forward by 1 unit, i.e. IP ⇐ IP + 1 ⌉
    ⌈   in this case, though, we explicitly change the IP to some other value and don't just increment it ⌉
}

defsubr x0branch "0branch" {
    ⌈ This instruction appears only inside subroutine sequences, jump on false to address in next cell ⌉
    deftemp test ⇐ %toboolean (%pop)
    if (test) {
        State.IP ⇐ State.IP + 1
    } else {
       State.IP ⇐ State.RAM [State.IP]
    }
}


⌈ "immediate" words are fully operational even when in compile mode. Some (not all) of these words are meant to
    work /only/ in compile mode. At the REPL prompt ("interpret" mode), they produce unwanted results.
  immediate words: xif, xelse, xthen, xquote, xcomment, xsemi
  immediate words that only have meaning in compile mode: xif, xelse, xthen, xsemi
⌉


⌈ IF, ELSE and THEN are "immediate" words - they should only be used inside of ":" (colon compiler) ⌉

⌈ see diagram `compiling-IF-THEN.drawio.png` ⌉
defsubr xif "if" { 
    %immediate ⌈ This instruction appears only inside subroutine sequences, ( f -- ) compile if test and branchFalse ⌉ 
    ⌈ Step. 1: generate conditional branch to yet-unknown target1 ⌉ 
    deftemp branchFalseAddress ⇐ %funcall _find ("0branch")
    %ram+ (branchFalseAddress) ⌈ insert branch-if-false opcode (word) ⌉ 
    %rpush (%RAMnext) ⌈ target1 onto r-stack as memo for later fixup ⌉ 
    defsynonym target1 ≡ -1 
    %ram+ (target1) ⌈ branch target will be fixed up later ⌉ 
    ⌈ Step. 2: generate code for true branch - return to compiler which will compile the following words ⌉ 
    ⌈ THEN or ELSE will do the fixup of target1 ⌉ 
} 

⌈ see diagram `compiling-IF-ELSE-THEN.drawio.png` ⌉
defimmediatesubr xelse "else" {
    ⌈ Step. 1: fixup target1 from IF-true, retrieving memo from R-stack ⌉
    deftemp target1 ⇐ %rpop
    State.RAM [target1] ⇐ %RAMnext
    ⌈ Step. 2: generate unconditional branch for preceding IF, creating new memo for target2 on R-stack ⌉
    deftemp brAddress ⇐ %funcall _find ("branch")
    %rpush (%RAMnext) ⌈ target2 address on R-stack as memo for later fixup ⌉
    defsynonym target2 ≡ -1
    %ram+ (target2) ⌈ branch target will be fixed up later ⌉
    ⌈ Step. 3: generate code for false branch - return to compiler which will compile the following words ⌉
    ⌈ THEN will do the fixup of target2 ⌉
}

⌈ see diagrams `compiling-IF-THEN.drawio.png` and `compiling-IF-ELSE-THEN.drawio.png` ⌉
defimmediatesubr xthen "then" {
    ⌈ Step. 1: fixup target (from IF or from ELSE, above), retrieving memo from R-stack ⌉
    deftemp target ⇐ %rpop
    State.RAM [target] ⇐ %RAMnext
}

defsubr x_do "(do)" {
    ⌈ ( limit index --) Puts limit and index on return stack. ⌉
    @xswap
    deftemp index ⇐ %pop
    deftemp limit ⇐ %pop
    %rpush (index)
    %rpush (limit)
}

defimmediatesubr xdo "xdo" {
    ⌈ (  limit index --) Begin counted loop. ⌉
    %ram+(%funcall _find("(do)"))  ⌈ Push do loop handler. ⌉
    %rpush(%RAMnext)           ⌈ Push address to jump back to. ⌉
}

defsubr x_loop "(loop)" {
    ⌈ (  -- f) Determine if loop is done. ⌉
    deftemp index ⇐ %rpop
    deftemp limit ⇐ %rpop
    defsynonym cond ≡ (index >= limit)
    %push (cond)
    if (cond) { ⌈ clean up rstack if index >= limit ⌉
        %rpop
        %rpop
    }    
}

defimmediatesubr xploop "+loop" {
    ⌈ ( --) Close counted loop. ⌉
    %ram+(%funcall _find("(loop)"))   ⌈ Compile in loop test. ⌉
    %ram+(%funcall _find("0branch"))  ⌈ Compile in branch check. ⌉
    %ram+(%rpop)           ⌈ Address to jump back to. ⌉
}

defimmediatesubr xloop "xloop" {
    ⌈ (  --) Close counted loop. ⌉
    %push (1)
    @literalize                  ⌈ Default loop increment for x_loop. ⌉
    %ram+(%funcall _find("(loop)"))   ⌈ Compile in loop test. ⌉
    %ram+(%funcall _find("0branch"))  ⌈ Compile in branch check. ⌉
    %ram+(%rpop)           ⌈ Address to jump back to. ⌉
}

defimmediatesubr xbegin "begin" {
    %rpush (%RAMnext)  ⌈ ( --) Start indefinite loop. ⌉
}

defimmediatesubr xuntil "until" {
    ⌈ (  f --) Close indefinite loop with test. ⌉
    %ram+(%funcall _find("0branch"))  ⌈ Expects result of test on stack. ⌉
    %ram+(%rpop)           ⌈ Address to jump back to. ⌉
}



⌈  "... 123 constant K ..." ⌉
⌈  at interpretation time: 123 is on the Stack, we have consumed "constant" from BUFF, BUFF now contains "K ..." ⌉
⌈  invoke 'word' which parses "K" and pushed it. The stack becomes [... 123 "K"] ⌉
⌈  pop "K", pop 123, create a new word called 'K' with its PFA set to 123 and its CFA set to a subr that
     gets 123 from its PFA and pushes it onto the stack ⌉
defsubr xconst "const" {
    ⌈  get next word - the name - from BUFF ⌉
    defsynonym blank ≡ 32
    %push (blank)
    @xword
    ⌈  stack is now: ( NNNN name -- ) ⌉
    deftemp name ⇐ %pop
    deftemp value ⇐ %pop
    defsynonym normal ≡ 0
    deftemp fobj ⇐ %funcall code (name, normal, ↪︎doconst)
    %ram+ (value)
}

deffunction doconst () {  ⌈ method for const ⌉
    defsynonym parameter ≡ State.RAM [State.W + 1]
    %push (parameter)
}


deffunction docreate () {
    defsynonym parameterAddress ≡ %funcall len (State.RAM) + 4
    %push (parameterAddress)
}
deffunction create (name) {
    defsynonym normal ≡ 0
    %funcall code (name, normal, ↪︎docreate)
}
defsubr xcreate "create"{
    defsynonym blank ≡ 32
    %push (blank)
    @xword
    deftemp name ⇐ %pop
    %funcall create (name)
}

deffunction comma (value) {
    %ram+ (value)
}

defsubr xcomma "," {
    %funcall comma (%pop)
}

deffunction fvar (name, value) {
    %funcall create (name)
    %funcall comma (value)
}

defsubr xvar "variable" {
    defsynonym blank ≡ 32
    %push (blank)
    @xword
    deftemp name ⇐ %pop
    deftemp value ⇐ %pop
    %funcall fvar (name, value)    
}

defsubr xdump "dump" {
    deftemp n ⇐ %toint (%pop)
    deftemp start ⇐ %toint (%pop)
    %print ("----------------------------------------------------------------")
    deftemp a ⇐ start
    while (a < start + (%funcall min (n, (%funcall len (State.RAM) - start)))) {
        %print (a)
	%print (": ")
	%print (State.RAM [a])
	%eol
        deftemp a ⇐ a + 1
    }
}

defsubr xstore"!" {
    deftemp b ⇐ %pop
    deftemp a ⇐ %pop
    State.RAM [b] ⇐ a
}

defsubr xbye "bye" { ⌈ ( --) Leave interpreter ⌉ %quit }


deffunction _find (name) {
    ⌈ "( name -- cfa|0) Find CFA of word name." ⌉
    deftemp x ⇐ State.LAST
    while (x >= 0) {
        ⌈ ## print(f"-- {x} : {RAM[x]}, {RAM[x + 1]}")  # Debug. ⌉
        if (name = State.RAM[x + 1]) {  ⌈ # Match! ⌉
            return x + 3
        } else {
            x ⇐ State.RAM[x]  ⌈ # Get next link. ⌉
	}
    }
    return 0  ⌈ # Nothing found. ⌉
}

defsubr xfind "find" {
    ⌈ "( name | -- (name 0)|(xt 1)|(xt -1)) Search for word name." ⌉
    ⌈ 3 possible results: 1. (name 0) if not found, 2. (xt 1) if found and word is immediate, 3. (xt -1) if found and word is normal ⌉
    %push (32)
    @xword
    deftemp found ⇐ %funcall _find(%stop)
    if (0 = found) {
        %push (0)
    } else {
        %pop  ⌈ # Get rid of name on stack. ⌉
        %push(found)
        deftemp immediate ⇐ -1
        if (State.RAM[%stop - 1] & 1) { immediate ⇐ 1 }
        %push(immediate)
    }
}

defsubr xtick "'"  {
    ⌈ "( name -- xt|-1) Search for execution token of word name." ⌉
    %push (32)
    @xword
    deftemp name ⇐ %pop
    deftemp found ⇐ %funcall _find(name)
    %push (found)
}

defsubr xnone "None" {
    %pushNone
}

⌈ fvget and fvset assume that the forth object (word) is a set of contiguous slots, each 1 machine word wide
  these functions use direct integer offsets to access the fields of the fojbect, whereas in higher level languages
  we'd use class fields instead - todo: fix this in the future (or not? at what point is customization better than
  generalization?) ⌉
deffunction fvget (name) {
    deftemp fobjaddress ⇐ %funcall _find(%pop)
    return State.RAM [fobjaddress + 1]
}

deffunction fvset (name, v) {
    deftemp fobjaddress ⇐ %funcall _find(%pop)
    defsynonym namefieldaddress ≡ fobjaddress + 1
    State.RAM [namefieldaddress] ⇐ v
}


defsubr xwords "words" {
    ⌈ print words in dictionary ⌉
    deftemp x ⇐ State.LAST
    while (x > -1) {
        %print (State.RAM [x+ 1])
	%print (" ")
    }
    %eol
}


defsubr xexecute "execute" {
    ⌈ invoke given word ⌉
    deftemp wordAddress ⇐ %pop
    @@wordAddress
}


deffunction doword () {
⌈
Execute a colon-defined word using indirect threaded code interpretation.

This function implements the inner interpreter for threaded code execution.
Threaded code words store their definitions as arrays of code field addresses
(CFAs) in the parameter field area (PFA) immediately following the word header.

The execution model maintains two critical registers:

1. IP (Instruction Pointer): References the current position within the
   threaded code array being interpreted. Since threaded words may invoke
   other threaded words, IP must be preserved in a reentrant manner via
   the return stack on each invocation.

2. W (Word Pointer): References the CFA of the currently executing primitive.
   This global register serves an analogous function to 'self' in object-oriented
   languages, enabling subroutines to access word header fields through fixed
   offsets from the CFA.

Optimization rationale: W is positioned to reference the CFA rather than the
word header base. This design eliminates offset arithmetic for CFA access—the
most frequent header operation—at the cost of requiring offset adjustments
for other header fields (NFA: W-2, flags: W-1, PFA: W+1). This represents a
deliberate trade-off favoring the common case.

The inner interpreter loop performs the following operations:
- Fetch the next CFA from RAM[IP] into W (performing the first indirection)
- Increment IP to advance through the threaded code array
- Execute the primitive via RAM[W]() (performing the second indirection)

By caching the dereferenced CFA in W, we amortize the cost of double
indirection: both primitive execution and header field access within
subroutines utilize the same cached reference, avoiding redundant
dereferences. This is functionally equivalent to parameter passing in
object-oriented method invocation, but eliminates the overhead of
explicitly passing 'self' to each primitive.

Note: W's state is only defined during primitive execution (within RAM[W]()).
Between loop iterations, W may reference a stale CFA, but this is
architecturally sound since W is unconditionally updated before each
primitive invocation.
⌉

    %rpush (State.IP)
    State.IP ⇐ State.W + 1
    while (-1 != State.RAM[State.IP]) {
        State.W ⇐ State.RAM[State.IP]
	State.IP ⇐ State.IP + 1
	@State.RAM[State.W]
    }
    State.IP ⇐ %rpop
}

defsubr xcolon ":" {
    ⌈ ( name | --) Start compilation. ⌉
    defsynonym blank ≡ 32
    %push (blank)
    @xword
    deftemp name ⇐ %pop
    %funcall code(name, 0, doword)
    %setCompilingState
}

defimmediatesubr xsemi ";"{
    ⌈ ( --) Finish definition. ⌉

    %ram+(-1)  ⌈ Marker for end of definition. ⌉
    %setNotCompilingState
}

deffunction notfound (word) {
    %clearS
    %clearR
    %print (word)
    %print ("?")
    %eol
}

deffunction exec (xt) {
    ⌈ found and compiling and immediate ⌉
    State.W ⇐ xt
    State.IP ⇐ -1  ⌈ Dummy to hold place in return stack. ⌉	
    @State.RAM[xt]  ⌈ Execute code. ⌉
}

deffunction compile_word (xt) {
    ⌈ found and not compiling ⌉
    State.W ⇐ xt
    State.IP ⇐ -1  ⌈ Dummy to hold place in return stack. ⌉	
    @State.RAM[xt]  ⌈ Execute code. ⌉
}

deffunction pushasinteger (word) {
    %push (%toint (word))
}

deffunction pushasfloat (word) {
    %push (%tofloat (word))
}

deffunction compileinteger (word) {
    %funcall pushasinteger(word)
    @literalize
}

deffunction compilefloat (word) {
    %funcall pushasfloat(word)
    @literalize
}

defsubr xinterpret "interpret" {
    ⌈ ( string --) Execute word. ⌉

    @xfind
    ⌈ 3 possible results from xfind:
        1. (name 0) if not found,
	2. (xt 1) if found and word is immediate,
	3. (xt -1) if found and word is normal ⌉
    deftemp result ⇐ %pop					    defsynonym foundimmediate ≡ (result = 1)
    deftemp item ⇐ %pop						    defsynonym foundnormal ≡ (result = -1)
    	    	   						    defsynonym notfound ≡ (result = 0)
    	    	   						    defsynonym found ≡ (foundimmediate or foundnormal)

include(`xinterpret.frish')

    return True
}

deffunction ok () {
    ⌈ ( --) Interaction loop -- REPL ⌉
    defsynonym blank ≡ 32
    while ⊤ {
        %input
        while not %empty-input {
           @xinterpret
        }
    }
}

deffunction debugok () {
    ⌈ ( --) Interaction loop -- REPL ⌉
    defsynonym blank ≡ 32
        %debuginput
        while not %empty-input {
           if (@xinterpret) {
	           %print (" ok")
		   %eol
	   }
	   %print (State.BUFP) %print (" -- ") %print (State.BUFF) %eol
	   @xdots
        }
	   %print (State.BUFP) %print (" == ") %print (State.BUFF) %eol
	   @xdot
	   @xdots
}

@ok
    
