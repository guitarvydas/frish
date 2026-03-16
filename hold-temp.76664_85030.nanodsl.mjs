'use strict'

import * as ohm from 'ohm-js';

let verbose = false;

function top (stack) { let v = stack.pop (); stack.push (v); return v; }

function set_top (stack, v) { stack.pop (); stack.push (v); return v; }

let return_value_stack = [];
let rule_name_stack = [];
let depth_prefix = ' ';

function enter_rule (name) {
    if (verbose) {
	console.error (depth_prefix, ["enter", name]);
	depth_prefix += ' ';
    }
    return_value_stack.push ("");
    rule_name_stack.push (name);
}

function set_return (v) {
    set_top (return_value_stack, v);
}

function exit_rule (name) {
    if (verbose) {
	depth_prefix = depth_prefix.substr (1);
	console.error (depth_prefix, ["exit", name]);
    }
    rule_name_stack.pop ();
    return return_value_stack.pop ()
}

const grammar = String.raw`
frish {

  Main = TopLevel+
  TopLevel =
    | Defvar -- defvar
    | Defsynonym -- defsynonym
    | Defsubr -- defsubr
    | Defimmediatesubr -- defimmediatesubr
    | Deffunction -- deffunction
    | Defobj -- defobj
    | Builtin -- builtin
    | Call -- call
    | comment line? -- comment
    | line -- line

   Defvar = "defvar" Lval "⇐" Exp line?
   Defsubr = "defsubr" ident string StatementBlock line?
   Defimmediatesubr = "defimmediatesubr" ident string StatementBlock line?
   Deffunction = "deffunction" ident Formals StatementBlock line?
   Defobj = "defobj" ident ObjFormals? line? "{" line? InitStatement+ "}" line?

   StatementBlock = line? "{" line? Rec_Statement line? "}" line?

   Rec_Statement = line? R_Statement line?
   R_Statement =
     | comment Rec_Statement? -- comment
     | Builtin Rec_Statement? -- builtin
     | Deftemp -- deftemp
     | Deftemps  -- deftemps
     | Defsynonym -- defsynonym     
     | IfStatement  -- if
     | "pass" Rec_Statement? -- pass
     | "return" ReturnExp -- return
     | ForStatement -- for
     | WhileStatement  -- while
     | Synonym -- synonym
     | Assignment -- assignment
     | "@@" Lval Rec_Statement? -- callindirect
     | Call -- call
     | spaces #comment? line Rec_Statement? -- line
   CommaIdent = Comma ident

   Call = "@" Lval Rec_Statement?

   Builtin = BuiltinPhrase line?
   BuiltinPhrase =
     | "%popchar" -- popchar
     | "%pop" -- pop
     | "%push" "(" Exp ")" -- push
     | "%stop" -- stop
     | "%scanfor" "(" ident ")" -- scanfor
     | "%assoc" "(" ident "," string "," Subraddress ")" -- assoc
     | "%eol" -- eol
     | "%print" "(" Exp ")" -- print
     | "%printAsCharacter" "(" Exp ")" -- printAsCharacter
     | "%empty-input" -- emptyinput
     | "%empty-string?" "(" Exp ")" -- emptystring
     | "%quit" -- quit
     | "%stack" -- stack
     | "%freshdict" -- freshdict
     | "%digits?" "(" Exp ")" -- isdigits
     | "%toint" "(" Exp ")" -- toint
     | "%tofloat" "(" Exp ")" -- tofloat
     | "%isInteger" "(" Exp ")" -- isInteger
     | "%isinteger" "(" Exp ")" -- isintegerLC
     | "%isFloat" "(" Exp ")" -- isFloat
     | "%isfloat" "(" Exp ")" -- isfloatLC
     | "%input" -- input
     | "%debuginput" -- debuginput
     | "%clearS" -- clearS
     | "%clearR" -- clearR
     | "%pushNone" -- pushNone
     
     | "%rpop" -- rpop
     | "%rpush" "(" Exp ")" -- rpush
     | "%rtop" -- rtop
     | "%rsecond" -- rsecond
     | "%rthird" -- rthird

     | "%toboolean" "(" Exp ")" -- toboolean

     | ("λ" | "%funcall") Primary Actuals -- funcall

     | "%incompilingstate" -- incompilingstate
     | "%setCompilingState" -- setcompilingstate
     | "%setNotCompilingState" -- setnotcompilingstate
     | "%immediate" -- immediate

     | "%RAMnext" -- ramnext
     | "%ram+" "(" Exp ")" -- ramappend
     
     | "%returnFalse" -- returnFalse

     | "%" #ident Args? -- unrecognized

   Args = "(" StuffInsideParentheses* ")"

   Deftemp = "deftemp" Lval "⇐" Exp Rec_Statement?
   Deftemps = "deftemps" LvalComma+ "⇐" Exp Rec_Statement?
   Defsynonym = "defsynonym" Defsyn
   Defsyn =
     | Lval errorMessage "≡" Exp Rec_Statement? -- illegal
     | ident "≡" Exp Rec_Statement? -- legal

   InitStatement = "•" ident "⇐" Exp (comment | line)*

   IfStatement = "if" Exp StatementBlock ElifStatement* ElseStatement? Rec_Statement?
   ElifStatement = "elif" Exp StatementBlock
   ElseStatement = "else" StatementBlock

   ForStatement = "for" ident "in" Exp StatementBlock Rec_Statement?
   WhileStatement = "while" Exp StatementBlock Rec_Statement?

   Synonym = Lval "≡" Exp Rec_Statement?

   Assignment = 
     | "[" LvalComma+ "]" "⇐" Exp Rec_Statement? -- multiple
     | Lval "⇐" Exp Rec_Statement? -- single

   LvalComma = Lval Comma?

    ReturnExp =
      | "[" ExpComma+ "]" Rec_Statement? -- multiple
      | Exp Rec_Statement? -- single

    ExpComma = Exp Comma?
    
    Exp =  BooleanAndOrIn

    BooleanAndOrIn =
      | BooleanAndOrIn andOrIn BooleanExp -- andOrIn
      | BooleanExp -- default
      
    BooleanExp =
      | BooleanExp boolNeq BooleanNot -- boolopneq
      | BooleanExp boolOp BooleanNot -- boolop
      | BooleanNot -- basic

    BooleanNot =
      | "not" BooleanExp -- not
      | AddExp -- basic

    AddExp =
      | AddExp "+" MulExp  -- plus
      | AddExp "-" MulExp  -- minus
      | MulExp -- basic

    MulExp =
      | MulExp "*" ExpExp  -- times
      | MulExp "/" ExpExp  -- divide
      | ExpExp -- basic

    ExpExp =
      | Primary "^" ExpExp  -- power
      | Primary -- basic

    Primary =
      | PrimaryIndexed -- plain

    PrimaryIndexed =
      | PrimaryIndexed "/" ident -- lookupident
      | PrimaryIndexed "/" PrimaryIndexed -- lookup
      | PrimaryIndexed "." ident -- fieldident
      | PrimaryIndexed "." PrimaryIndexed -- field
      | PrimaryIndexed "[" Exp "]" -- index
      | PrimaryIndexed "[" digit+ ":" "]" -- nthslice
      | Atom -- atom

    Atom =
      | Builtin -- builtin
      | Call -- call
      | "[" "]" -- emptylistconst
      | "{" "}" -- emptydict
      | "(" Exp ")" -- paren
      | "[" line? PrimaryComma+ line? "]" -- listconst
      | "{" line? PairComma+ line? "}" -- dict
      | phi -- phi
      | "⊤" -- true
      | "⊥" -- false
      | Subraddress -- subraddress
      | "range" "(" Exp ")" -- range
      | string -- string
      | number -- number
      | ident -- ident


    Subraddress =  "↪︎" ident

    PrimaryComma = Primary Comma? line?
    PairComma = Pair Comma?

    StuffInsideParentheses =
      | "(" StuffInsideParentheses* ")" -- rec
      | ~"(" ~")" any -- default
    
    Lval = Exp

    Formals (Formals) =
      | "(" ")" -- noformals
      | "(" FormalComma* ")" -- withformals
    ObjFormals = Formals

    Formal = 
       | ident -- plain
       
    FormalComma = Formal Comma?
    
    Actuals = 
      | "(" ")" -- noactuals
      | "(" ActualComma* ")" line? -- actuals

   Actual = Exp
   ActualComma = comment? Actual Comma? line?

    number =
      | digit* "." digit+  -- fract
      | digit+             -- whole

    Pair = string ":" Exp Comma?
  

  andOrIn =
    | "and" -- and
    | "or" -- or
    | "in" -- in
    | "&" -- bitwiseand

  boolOp = (boolEq | boolNeq | "<=" | ">=" | ">" | "<")
  boolEq = "="
  boolNeq = "!="

  string = unicodestring | asciistring
  asciistring = "\"" astringchar* "\""
  astringchar = ~"\"" any
  unicodestring = "“" stringchar* "”"
  stringchar = 
    | "“" stringchar* "”" -- rec
    | ~"“" ~"”" any -- other

    keyword = (
        "defsynonym"
      | "deftemp"
      | "defobj"
      | "defvar"
      | "defsubr"
      | "deffunction"
      | "pass"
      | "return"
      | "if"
      | "elif"
      | "else"
      | "and"
      | "or"
      | "in"
      | "not"
      | "range"
      | "while"
      | "as"
      | "pair"
      | "@"
      | phi
      ) ~idchar
      
  phi = ("ϕ" | "%CF%95")

  ident  = ~keyword idchar+
  idchar =
    | "❲" idchar+ "❳" -- rec
    | ~"❲" ~"❳" idch -- other

  idch = letter | digit | "_" | "-"

  comment = "⌈" commentchar* "⌉"
  commentchar = 
    | "⌈" commentchar* "⌉" -- rec
    | ~"⌈" ~"⌉" any -- other

  errorMessage = "⎝" errorchar* "⎠"
  errorchar =  
    | "⎝" errorchar* "⎠" -- rec
    | ~"⎝" ~"⎠" any -- other

  line = "⎩" (~"⎩" ~"⎭" any)* "⎭"

  Comma = line? "," line?
}
`;

let args = {};
function resetArgs () {
    args = {};
}
function memoArg (name, accessorString) {
    args [name] = accessorString;
};
function fetchArg (name) {
    return args [name];
}

fs.writeFileSync('/tmp/@pbplog.md', new Date().toISOString() + '\n');

let linenumber = 0;
function getlineinc () {
    linenumber += 1;
    return `${linenumber}`;
}

function pynlcomments (s) {
    return s.replace (/\n/g, '\n#')
}

let macros = {};

function memomacro (name, s) {
    fs.appendFileSync('/tmp/@pbplog.md', `memomacro ${name}` + '\n');    
    macros [name] = s;
    return "";
}

function macrolookup (name) {
    let s = macros [name];
    fs.appendFileSync('/tmp/@pbplog.md', `macrolookup ${name} -> /${s}/` + '\n');    
    if (s !== undefined) {
	return s;
    } else {
	return name;
    }
}
let parameters = {};
function pushParameter (name, v) {
    if (!parameters [name]) {
        parameters [name] = [];
    }
    parameters [name].push (v);
}
function popParameter (name) {
    parameters [name].pop ();
}
function getParameter (name) {
    let top = parameters [name].pop ();
    parameters [name].push (top);
    return top;
}


let _rewrite = {

Main : function (TopLevel,) {
enter_rule ("Main");
    set_return (`
import re

class Stack(list):⤷
    def push(my, *items):⤷
        my.extend(items)⤶⤶

class StateClass:⤷
    def __init__ (self):⤷
        self.S = Stack() 
        self.R = Stack()
        self.RAM = []
        self.LAST = -1
        self.IP = None
        self.W = None;
        self.BUFF = ""
        self.BUFP = 0
	self.compiling = False⤶⤶

State = StateClass ()

${TopLevel.rwr ().join ('')}`);
return exit_rule ("Main");
},
TopLevel_defvar : function (Defvar,) {
enter_rule ("TopLevel_defvar");
    set_return (`${Defvar.rwr ()}`);
return exit_rule ("TopLevel_defvar");
},
TopLevel_defsynonym : function (Defsynonym,) {
enter_rule ("TopLevel_defsynonym");
    set_return (`${Defsynonym.rwr ()}`);
return exit_rule ("TopLevel_defsynonym");
},
TopLevel_defsubr : function (Defsubr,) {
enter_rule ("TopLevel_defsubr");
    set_return (`${Defsubr.rwr ()}`);
return exit_rule ("TopLevel_defsubr");
},
TopLevel_defimmediatesubr : function (defimmediatesubr,) {
enter_rule ("TopLevel_defimmediatesubr");
    set_return (`${defimmediatesubr.rwr ()}`);
return exit_rule ("TopLevel_defimmediatesubr");
},
TopLevel_deffunction : function (Deffn,) {
enter_rule ("TopLevel_deffunction");
    set_return (`${Deffn.rwr ()}`);
return exit_rule ("TopLevel_deffunction");
},
TopLevel_defobj : function (Defobj,) {
enter_rule ("TopLevel_defobj");
    set_return (`${Defobj.rwr ()}`);
return exit_rule ("TopLevel_defobj");
},
TopLevel_builtin : function (x,) {
enter_rule ("TopLevel_builtin");
    set_return (`${x.rwr ()}`);
return exit_rule ("TopLevel_builtin");
},
TopLevel_call : function (x,) {
enter_rule ("TopLevel_call");
    set_return (`${x.rwr ()}`);
return exit_rule ("TopLevel_call");
},
TopLevel_comment : function (s,line,) {
enter_rule ("TopLevel_comment");
    set_return (`\n${s.rwr ()}${line.rwr ().join ('')}`);
return exit_rule ("TopLevel_comment");
},
TopLevel_line : function (line,) {
enter_rule ("TopLevel_line");
    set_return (`${line.rwr ()}`);
return exit_rule ("TopLevel_line");
},
Defvar : function (__,lval,_eq,e,line,) {
enter_rule ("Defvar");
    set_return (`\n${lval.rwr ()} = ${e.rwr ()}${line.rwr ().join ('')}`);
return exit_rule ("Defvar");
},
Defsubr : function (_4,ident,str,StatementBlock,line,) {
enter_rule ("Defsubr");
    set_return (`\ndef ${ident.rwr ()} ():⤷\nglobal State⤶${StatementBlock.rwr ()}${line.rwr ().join ('')}\ncode(${str.rwr ()},0,  ${ident.rwr ()})\n`);
return exit_rule ("Defsubr");
},
Defimmediatesubr : function (_4,ident,str,StatementBlock,line,) {
enter_rule ("Defimmediatesubr");
    set_return (`\ndef ${ident.rwr ()} ():⤷\nglobal State⤶${StatementBlock.rwr ()}${line.rwr ().join ('')}\ncode(${str.rwr ()}, 1, ${ident.rwr ()})\n`);
return exit_rule ("Defimmediatesubr");
},
Deffunction : function (_4,ident,formals,StatementBlock,line,) {
enter_rule ("Deffunction");
    set_return (`\ndef ${ident.rwr ()} ${formals.rwr ()}:⤷\nglobal State⤶${StatementBlock.rwr ()}${line.rwr ().join ('')}\n`);
return exit_rule ("Deffunction");
},
Defobj : function (_defobj,ident,Formals,line1,lb,line2,init,rb,line3,) {
enter_rule ("Defobj");
    set_return (`\nclass ${ident.rwr ()}:⤷\ndef __init__ (self,${Formals.rwr ()}):${line1.rwr ().join ('')}⤷${line2.rwr ().join ('')}${init.rwr ().join ('')}${line3.rwr ().join ('')}⤶⤶\n`);
return exit_rule ("Defobj");
},
StatementBlock : function (line1,lb,line2,Statement,line3,rb,line4,) {
enter_rule ("StatementBlock");
    set_return (`${line1.rwr ().join ('')}${line2.rwr ().join ('')}⤷${Statement.rwr ()}${line3.rwr ().join ('')}${line4.rwr ().join ('')}⤶`);
return exit_rule ("StatementBlock");
},
Rec_Statement : function (line1,R_Statement,line2,) {
enter_rule ("Rec_Statement");
    set_return (`${line1.rwr ().join ('')}${R_Statement.rwr ()}${line2.rwr ().join ('')}`);
return exit_rule ("Rec_Statement");
},
R_Statement_comment : function (s,rec,) {
enter_rule ("R_Statement_comment");
    set_return (`\n${s.rwr ()}${rec.rwr ().join ('')}`);
return exit_rule ("R_Statement_comment");
},
R_Statement_builtin : function (x,rec,) {
enter_rule ("R_Statement_builtin");
    set_return (`\n${x.rwr ()}${rec.rwr ().join ('')}`);
return exit_rule ("R_Statement_builtin");
},
R_Statement_deftemp : function (x,) {
enter_rule ("R_Statement_deftemp");
    set_return (`\n${x.rwr ()}`);
return exit_rule ("R_Statement_deftemp");
},
R_Statement_deftemps : function (x,) {
enter_rule ("R_Statement_deftemps");
    set_return (`\n${x.rwr ()}`);
return exit_rule ("R_Statement_deftemps");
},
R_Statement_defsynonym : function (x,) {
enter_rule ("R_Statement_defsynonym");
    set_return (`\n${x.rwr ()}`);
return exit_rule ("R_Statement_defsynonym");
},
R_Statement_if : function (IfStatement,) {
enter_rule ("R_Statement_if");
    set_return (`${IfStatement.rwr ()}`);
return exit_rule ("R_Statement_if");
},
R_Statement_pass : function (_27,rec,) {
enter_rule ("R_Statement_pass");
    set_return (`\npass${rec.rwr ().join ('')}`);
return exit_rule ("R_Statement_pass");
},
R_Statement_return : function (_29,ReturnExp,) {
enter_rule ("R_Statement_return");
    set_return (`\nreturn ${ReturnExp.rwr ()}`);
return exit_rule ("R_Statement_return");
},
R_Statement_for : function (ForStatement,) {
enter_rule ("R_Statement_for");
    set_return (`${ForStatement.rwr ()}`);
return exit_rule ("R_Statement_for");
},
R_Statement_while : function (WhileStatement,) {
enter_rule ("R_Statement_while");
    set_return (`${WhileStatement.rwr ()}`);
return exit_rule ("R_Statement_while");
},
R_Statement_assignment : function (Assignment,) {
enter_rule ("R_Statement_assignment");
    set_return (`${Assignment.rwr ()}`);
return exit_rule ("R_Statement_assignment");
},
R_Statement_callindirect : function (_,lval,rec,) {
enter_rule ("R_Statement_callindirect");
    set_return (`\n${lval.rwr ()}()${rec.rwr ().join ('')}`);
return exit_rule ("R_Statement_callindirect");
},
R_Statement_call : function (c,) {
enter_rule ("R_Statement_call");
    set_return (`\n${c.rwr ()}`);
return exit_rule ("R_Statement_call");
},
R_Statement_line : function (ws,comment,line,rec,) {
enter_rule ("R_Statement_line");
    set_return (`${ws.rwr ()}${comment.rwr ().join ('')}${line.rwr ()}${rec.rwr ().join ('')}`);
return exit_rule ("R_Statement_line");
},
CommaIdent : function (_comma,ident,) {
enter_rule ("CommaIdent");
    set_return (`, ${ident.rwr ()}`);
return exit_rule ("CommaIdent");
},
Call : function (_,lval,rec,) {
enter_rule ("Call");
    set_return (`${lval.rwr ()}()${rec.rwr ().join ('')}`);
return exit_rule ("Call");
},
Builtin : function (x,line,) {
enter_rule ("Builtin");
    set_return (`${x.rwr ()}${line.rwr ().join ('')}`);
return exit_rule ("Builtin");
},
BuiltinPhrase_popchar : function (_,) {
enter_rule ("BuiltinPhrase_popchar");
    set_return (`chr(State.S.pop ())`);
return exit_rule ("BuiltinPhrase_popchar");
},
BuiltinPhrase_pop : function (_,) {
enter_rule ("BuiltinPhrase_pop");
    set_return (`State.S.pop ()`);
return exit_rule ("BuiltinPhrase_pop");
},
BuiltinPhrase_push : function (_,lp,exp,rp,) {
enter_rule ("BuiltinPhrase_push");
    set_return (`State.S.push (${exp.rwr ()})`);
return exit_rule ("BuiltinPhrase_push");
},
BuiltinPhrase_stop : function (_,) {
enter_rule ("BuiltinPhrase_stop");
    set_return (`State.S[-1]`);
return exit_rule ("BuiltinPhrase_stop");
},
BuiltinPhrase_scanfor : function (_,lp,want,rp,) {
enter_rule ("BuiltinPhrase_scanfor");
    set_return (`
    found = ""
    while State.BUFP < len(State.BUFF):⤷
        x = State.BUFF[State.BUFP]
        State.BUFP += 1
        if wanted == x:⤷
            if 0 == len(found):⤷
                continue⤶
            else:⤷
                break⤶⤶
        else:⤷
            found += x⤶⤶
    State.S.append(found)
`);
return exit_rule ("BuiltinPhrase_scanfor");
},
BuiltinPhrase_assoc : function (_,lp,dict,_comma1,str,_comma2,addr,rp,) {
enter_rule ("BuiltinPhrase_assoc");
    set_return (`\n${dict.rwr ()} [${str.rwr ()}] = ${addr.rwr ()}`);
return exit_rule ("BuiltinPhrase_assoc");
},
BuiltinPhrase_eol : function (_,) {
enter_rule ("BuiltinPhrase_eol");
    set_return (`print ()`);
return exit_rule ("BuiltinPhrase_eol");
},
BuiltinPhrase_print : function (_,lp,exp,rp,) {
enter_rule ("BuiltinPhrase_print");
    set_return (`print (${exp.rwr ()}, end="")`);
return exit_rule ("BuiltinPhrase_print");
},
BuiltinPhrase_printAsCharacter : function (_,lp,exp,rp,) {
enter_rule ("BuiltinPhrase_printAsCharacter");
    set_return (`print (chr (int (${exp.rwr ()})), end="")`);
return exit_rule ("BuiltinPhrase_printAsCharacter");
},
BuiltinPhrase_emptyinput : function (_,) {
enter_rule ("BuiltinPhrase_emptyinput");
    set_return (`(State.BUFP >= len(State.BUFF))`);
return exit_rule ("BuiltinPhrase_emptyinput");
},
BuiltinPhrase_emptystring : function (_,lp,s,rp,) {
enter_rule ("BuiltinPhrase_emptystring");
    set_return (`(not ${s.rwr ()})`);
return exit_rule ("BuiltinPhrase_emptystring");
},
BuiltinPhrase_quit : function (_,) {
enter_rule ("BuiltinPhrase_quit");
    set_return (`\nraise SystemExit`);
return exit_rule ("BuiltinPhrase_quit");
},
BuiltinPhrase_stack : function (_,) {
enter_rule ("BuiltinPhrase_stack");
    set_return (`State.S`);
return exit_rule ("BuiltinPhrase_stack");
},
BuiltinPhrase_freshdict : function (_,) {
enter_rule ("BuiltinPhrase_freshdict");
    set_return (`{}`);
return exit_rule ("BuiltinPhrase_freshdict");
},
BuiltinPhrase_isdigits : function (_,lp,exp,rp,) {
enter_rule ("BuiltinPhrase_isdigits");
    set_return (`${exp.rwr ()}.isdigit()`);
return exit_rule ("BuiltinPhrase_isdigits");
},
BuiltinPhrase_toint : function (_,lp,exp,rp,) {
enter_rule ("BuiltinPhrase_toint");
    set_return (`int (${exp.rwr ()})`);
return exit_rule ("BuiltinPhrase_toint");
},
BuiltinPhrase_tofloat : function (_,lp,exp,rp,) {
enter_rule ("BuiltinPhrase_tofloat");
    set_return (`float (${exp.rwr ()})`);
return exit_rule ("BuiltinPhrase_tofloat");
},
BuiltinPhrase_isInteger : function (_,lp,exp,rp,) {
enter_rule ("BuiltinPhrase_isInteger");
    set_return (`re.match(r"^-?\\d*$", ${exp.rwr ()})`);
return exit_rule ("BuiltinPhrase_isInteger");
},
BuiltinPhrase_isintegerLC : function (_,lp,exp,rp,) {
enter_rule ("BuiltinPhrase_isintegerLC");
    set_return (`re.match(r"^-?\\d*$", ${exp.rwr ()})`);
return exit_rule ("BuiltinPhrase_isintegerLC");
},
BuiltinPhrase_isFloat : function (_,lp,exp,rp,) {
enter_rule ("BuiltinPhrase_isFloat");
    set_return (`re.match(r"^-?\d*\\.?\\d*$", ${exp.rwr ()})`);
return exit_rule ("BuiltinPhrase_isFloat");
},
BuiltinPhrase_isfloatLC : function (_,lp,exp,rp,) {
enter_rule ("BuiltinPhrase_isfloatLC");
    set_return (`re.match(r"^-?\d*\\.?\\d*$", ${exp.rwr ()})`);
return exit_rule ("BuiltinPhrase_isfloatLC");
},
BuiltinPhrase_input : function (_,) {
enter_rule ("BuiltinPhrase_input");
    set_return (`
State.BUFF = input("OK ")
State.BUFP = 0
`);
return exit_rule ("BuiltinPhrase_input");
},
BuiltinPhrase_debuginput : function (_,) {
enter_rule ("BuiltinPhrase_debuginput");
    set_return (`
State.BUFF = "7 ."
State.BUFP = 0
`);
return exit_rule ("BuiltinPhrase_debuginput");
},
BuiltinPhrase_clearS : function (_,) {
enter_rule ("BuiltinPhrase_clearS");
    set_return (`\nState.S.clear()`);
return exit_rule ("BuiltinPhrase_clearS");
},
BuiltinPhrase_clearR : function (_,) {
enter_rule ("BuiltinPhrase_clearR");
    set_return (`\nState.R.clear()`);
return exit_rule ("BuiltinPhrase_clearR");
},
BuiltinPhrase_pushNone : function (_,) {
enter_rule ("BuiltinPhrase_pushNone");
    set_return (`\nState.S.append (None)`);
return exit_rule ("BuiltinPhrase_pushNone");
},
BuiltinPhrase_rpop : function (_,) {
enter_rule ("BuiltinPhrase_rpop");
    set_return (`State.R.pop ()`);
return exit_rule ("BuiltinPhrase_rpop");
},
BuiltinPhrase_rpush : function (_,lp,exp,rp,) {
enter_rule ("BuiltinPhrase_rpush");
    set_return (`State.R.append (${exp.rwr ()})`);
return exit_rule ("BuiltinPhrase_rpush");
},
BuiltinPhrase_rtop : function (_,) {
enter_rule ("BuiltinPhrase_rtop");
    set_return (`State.R [-1]`);
return exit_rule ("BuiltinPhrase_rtop");
},
BuiltinPhrase_rsecond : function (_,) {
enter_rule ("BuiltinPhrase_rsecond");
    set_return (`State.R [-2]`);
return exit_rule ("BuiltinPhrase_rsecond");
},
BuiltinPhrase_rthird : function (_,) {
enter_rule ("BuiltinPhrase_rthird");
    set_return (`State.R [-3]`);
return exit_rule ("BuiltinPhrase_rthird");
},
BuiltinPhrase_toboolean : function (_,lp,exp,rp,) {
enter_rule ("BuiltinPhrase_toboolean");
    set_return (`bool (${exp.rwr ()})`);
return exit_rule ("BuiltinPhrase_toboolean");
},
BuiltinPhrase_funcall : function (_,f,actuals,) {
enter_rule ("BuiltinPhrase_funcall");
    set_return (`${f.rwr ()}${actuals.rwr ()}`);
return exit_rule ("BuiltinPhrase_funcall");
},
BuiltinPhrase_incompilingstate : function (_,) {
enter_rule ("BuiltinPhrase_incompilingstate");
    set_return (`State.compiling`);
return exit_rule ("BuiltinPhrase_incompilingstate");
},
BuiltinPhrase_setcompilingstate : function (_,) {
enter_rule ("BuiltinPhrase_setcompilingstate");
    set_return (`State.compiling = True`);
return exit_rule ("BuiltinPhrase_setcompilingstate");
},
BuiltinPhrase_setnotcompilingstate : function (_,) {
enter_rule ("BuiltinPhrase_setnotcompilingstate");
    set_return (`State.compiling = False`);
return exit_rule ("BuiltinPhrase_setnotcompilingstate");
},
BuiltinPhrase_immediate : function (_,) {
enter_rule ("BuiltinPhrase_immediate");
    set_return (`State.compiling = False`);
return exit_rule ("BuiltinPhrase_immediate");
},
BuiltinPhrase_ramnext : function (_,) {
enter_rule ("BuiltinPhrase_ramnext");
    set_return (`len (Stack.RAM)`);
return exit_rule ("BuiltinPhrase_ramnext");
},
BuiltinPhrase_ramappend : function (_,lp,exp,rp,) {
enter_rule ("BuiltinPhrase_ramappend");
    set_return (`\nState.RAM.append (${exp.rwr ()})`);
return exit_rule ("BuiltinPhrase_ramappend");
},
BuiltinPhrase_returnFalse : function (_,) {
enter_rule ("BuiltinPhrase_returnFalse");
    set_return (`return False`);
return exit_rule ("BuiltinPhrase_returnFalse");
},
BuiltinPhrase_unrecognized : function (_,ident,args,) {
enter_rule ("BuiltinPhrase_unrecognized");
    set_return (`${_.rwr ()} ⎝ error - unrecognized builtin "${ident.rwr ()}" (with given arguments) ⎠ ${args.rwr ().join ('')} `);
return exit_rule ("BuiltinPhrase_unrecognized");
},
Args : function (lp,stuff,rp,) {
enter_rule ("Args");
    set_return (`${lp.rwr ()}${stuff.rwr ().join ('')}${rp.rwr ()}`);
return exit_rule ("Args");
},
Deftemp : function (_deftemp,lval,_mutate,e,rec,) {
enter_rule ("Deftemp");
    set_return (`\n${lval.rwr ()} = ${e.rwr ()}${rec.rwr ().join ('')}`);
return exit_rule ("Deftemp");
},
Deftemps : function (_deftemp,lvalcomma,_mutate,e,rec,) {
enter_rule ("Deftemps");
    set_return (`\n${lvalcomma.rwr ().join ('')} = ${e.rwr ()}${rec.rwr ().join ('')}`);
return exit_rule ("Deftemps");
},
Defsynonym : function (_,defsyn,) {
enter_rule ("Defsynonym");
    set_return (`${defsyn.rwr ()}`);
return exit_rule ("Defsynonym");
},
Defsyn_illegal : function (lval,err,_eqv,e,rec,) {
enter_rule ("Defsyn_illegal");
    set_return (`\n${lval.rwr ()} ${err.rwr ()} = ${e.rwr ()}${rec.rwr ().join ('')}`);
return exit_rule ("Defsyn_illegal");
},
Defsyn_legal : function (id,_eqv,e,rec,) {
enter_rule ("Defsyn_legal");
    set_return (`\n${id.rwr ()} = ${e.rwr ()}${rec.rwr ().join ('')}`);
return exit_rule ("Defsyn_legal");
},
InitStatement : function (_mark,ident,_33,Exp,fluff,) {
enter_rule ("InitStatement");
    set_return (`\nself.${ident.rwr ()} = ${Exp.rwr ()} ${fluff.rwr ().join ('')}`);
return exit_rule ("InitStatement");
},
IfStatement : function (_35,Exp,StatementBlock,ElifStatement,ElseStatement,rec,) {
enter_rule ("IfStatement");
    set_return (`\nif ${Exp.rwr ()}:${StatementBlock.rwr ()}${ElifStatement.rwr ().join ('')}${ElseStatement.rwr ().join ('')}${rec.rwr ().join ('')}`);
return exit_rule ("IfStatement");
},
ElifStatement : function (_37,Exp,StatementBlock,) {
enter_rule ("ElifStatement");
    set_return (`\nelif ${Exp.rwr ()}:${StatementBlock.rwr ()}`);
return exit_rule ("ElifStatement");
},
ElseStatement : function (_39,StatementBlock,) {
enter_rule ("ElseStatement");
    set_return (`\nelse:${StatementBlock.rwr ()}`);
return exit_rule ("ElseStatement");
},
ForStatement : function (_41,ident,_43,Exp,StatementBlock,rec,) {
enter_rule ("ForStatement");
    set_return (`\nfor ${ident.rwr ()} in ${Exp.rwr ()}:${StatementBlock.rwr ()}${rec.rwr ().join ('')}`);
return exit_rule ("ForStatement");
},
WhileStatement : function (_45,Exp,StatementBlock,rec,) {
enter_rule ("WhileStatement");
    set_return (`\nwhile ${Exp.rwr ()}:${StatementBlock.rwr ()}${rec.rwr ().join ('')}`);
return exit_rule ("WhileStatement");
},
Synonym : function (Lval,_59,Exp,rec,) {
enter_rule ("Synonym");
    set_return (`\n${Lval.rwr ()} = ${Exp.rwr ()}${rec.rwr ().join ('')}`);
return exit_rule ("Synonym");
},
Assignment_multiple : function (_55,Lvals,_57,_58,Exp,rec,) {
enter_rule ("Assignment_multiple");
    set_return (`\n[${Lvals.rwr ().join ('')}] = ${Exp.rwr ()}${rec.rwr ().join ('')}`);
return exit_rule ("Assignment_multiple");
},
Assignment_single : function (Lval,_59,Exp,rec,) {
enter_rule ("Assignment_single");
    set_return (`\n${Lval.rwr ()} = ${Exp.rwr ()}${rec.rwr ().join ('')}`);
return exit_rule ("Assignment_single");
},
LvalComma : function (Lval,Comma,) {
enter_rule ("LvalComma");
    set_return (`${Lval.rwr ()}${Comma.rwr ().join ('')}`);
return exit_rule ("LvalComma");
},
ReturnExp_multiple : function (_60,Exps,_62,rec,) {
enter_rule ("ReturnExp_multiple");
    set_return (`[${Exps.rwr ().join ('')}]${rec.rwr ().join ('')}`);
return exit_rule ("ReturnExp_multiple");
},
ReturnExp_single : function (Exp,rec,) {
enter_rule ("ReturnExp_single");
    set_return (`${Exp.rwr ()}${rec.rwr ().join ('')}`);
return exit_rule ("ReturnExp_single");
},
ExpComma : function (Exp,Comma,) {
enter_rule ("ExpComma");
    set_return (`${Exp.rwr ()}${Comma.rwr ().join ('')}`);
return exit_rule ("ExpComma");
},
Exp : function (e,) {
enter_rule ("Exp");
    set_return (`${e.rwr ()}`);
return exit_rule ("Exp");
},
BooleanAndOrIn_andOrIn : function (e1,op,e2,) {
enter_rule ("BooleanAndOrIn_andOrIn");
    set_return (`${e1.rwr ()}${op.rwr ()}${e2.rwr ()}`);
return exit_rule ("BooleanAndOrIn_andOrIn");
},
BooleanAndOrIn_default : function (e,) {
enter_rule ("BooleanAndOrIn_default");
    set_return (`${e.rwr ()}`);
return exit_rule ("BooleanAndOrIn_default");
},
BooleanExp_boolopneq : function (BooleanExp,boolOp,BooleanNot,) {
enter_rule ("BooleanExp_boolopneq");
    set_return (`${BooleanExp.rwr ()}${boolOp.rwr ()}${BooleanNot.rwr ()}`);
return exit_rule ("BooleanExp_boolopneq");
},
BooleanExp_boolop : function (BooleanExp,boolOp,BooleanNot,) {
enter_rule ("BooleanExp_boolop");
    set_return (`${BooleanExp.rwr ()}${boolOp.rwr ()}${BooleanNot.rwr ()}`);
return exit_rule ("BooleanExp_boolop");
},
BooleanExp_basic : function (BooleanNot,) {
enter_rule ("BooleanExp_basic");
    set_return (`${BooleanNot.rwr ()}`);
return exit_rule ("BooleanExp_basic");
},
BooleanNot_not : function (_64,BooleanExp,) {
enter_rule ("BooleanNot_not");
    set_return (`not ${BooleanExp.rwr ()}`);
return exit_rule ("BooleanNot_not");
},
BooleanNot_basic : function (AddExp,) {
enter_rule ("BooleanNot_basic");
    set_return (`${AddExp.rwr ()}`);
return exit_rule ("BooleanNot_basic");
},
AddExp_plus : function (AddExp,_65,MulExp,) {
enter_rule ("AddExp_plus");
    set_return (`${AddExp.rwr ()}${_65.rwr ()}${MulExp.rwr ()}`);
return exit_rule ("AddExp_plus");
},
AddExp_minus : function (AddExp,_66,MulExp,) {
enter_rule ("AddExp_minus");
    set_return (`${AddExp.rwr ()}${_66.rwr ()}${MulExp.rwr ()}`);
return exit_rule ("AddExp_minus");
},
AddExp_basic : function (MulExp,) {
enter_rule ("AddExp_basic");
    set_return (`${MulExp.rwr ()}`);
return exit_rule ("AddExp_basic");
},
MulExp_times : function (MulExp,_67,ExpExp,) {
enter_rule ("MulExp_times");
    set_return (`${MulExp.rwr ()}${_67.rwr ()}${ExpExp.rwr ()}`);
return exit_rule ("MulExp_times");
},
MulExp_divide : function (MulExp,_68,ExpExp,) {
enter_rule ("MulExp_divide");
    set_return (`${MulExp.rwr ()}${_68.rwr ()}${ExpExp.rwr ()}`);
return exit_rule ("MulExp_divide");
},
MulExp_basic : function (ExpExp,) {
enter_rule ("MulExp_basic");
    set_return (`${ExpExp.rwr ()}`);
return exit_rule ("MulExp_basic");
},
ExpExp_power : function (Primary,_69,ExpExp,) {
enter_rule ("ExpExp_power");
    set_return (`${Primary.rwr ()}${_69.rwr ()}${ExpExp.rwr ()}`);
return exit_rule ("ExpExp_power");
},
ExpExp_basic : function (Primary,) {
enter_rule ("ExpExp_basic");
    set_return (`${Primary.rwr ()}`);
return exit_rule ("ExpExp_basic");
},
Primary_plain : function (p,) {
enter_rule ("Primary_plain");
    set_return (`${p.rwr ()}`);
return exit_rule ("Primary_plain");
},
PrimaryIndexed_lookupident : function (p,_slash,key,) {
enter_rule ("PrimaryIndexed_lookupident");
    set_return (`${p.rwr ()} [${key.rwr ()}]`);
return exit_rule ("PrimaryIndexed_lookupident");
},
PrimaryIndexed_lookup : function (p,_slash,key,) {
enter_rule ("PrimaryIndexed_lookup");
    set_return (`${p.rwr ()} [${key.rwr ()}]`);
return exit_rule ("PrimaryIndexed_lookup");
},
PrimaryIndexed_fieldident : function (p,_dot,key,) {
enter_rule ("PrimaryIndexed_fieldident");
    set_return (`${p.rwr ()}.${key.rwr ()}`);
return exit_rule ("PrimaryIndexed_fieldident");
},
PrimaryIndexed_field : function (p,_dot,key,) {
enter_rule ("PrimaryIndexed_field");
    set_return (`${p.rwr ()}.${key.rwr ()}`);
return exit_rule ("PrimaryIndexed_field");
},
PrimaryIndexed_index : function (p,lb,e,rb,) {
enter_rule ("PrimaryIndexed_index");
    set_return (`${p.rwr ()} [${e.rwr ()}]`);
return exit_rule ("PrimaryIndexed_index");
},
PrimaryIndexed_nthslice : function (p,lb,ds,_colon,rb,) {
enter_rule ("PrimaryIndexed_nthslice");
    set_return (`${p.rwr ()} [${ds.rwr ().join ('')}:]`);
return exit_rule ("PrimaryIndexed_nthslice");
},
PrimaryIndexed_atom : function (a,) {
enter_rule ("PrimaryIndexed_atom");
    set_return (`${a.rwr ()}`);
return exit_rule ("PrimaryIndexed_atom");
},
Atom_builtin : function (x,) {
enter_rule ("Atom_builtin");
    set_return (`${x.rwr ()}`);
return exit_rule ("Atom_builtin");
},
Atom_call : function (c,) {
enter_rule ("Atom_call");
    set_return (`${c.rwr ()}`);
return exit_rule ("Atom_call");
},
Atom_emptylistconst : function (_72,_73,) {
enter_rule ("Atom_emptylistconst");
    set_return (`${_72.rwr ()}${_73.rwr ()}`);
return exit_rule ("Atom_emptylistconst");
},
Atom_emptydict : function (_76,_77,) {
enter_rule ("Atom_emptydict");
    set_return (`${_76.rwr ()}${_77.rwr ()}`);
return exit_rule ("Atom_emptydict");
},
Atom_paren : function (_70,Exp,_71,) {
enter_rule ("Atom_paren");
    set_return (`${_70.rwr ()}${Exp.rwr ()}${_71.rwr ()}`);
return exit_rule ("Atom_paren");
},
Atom_listconst : function (lb,line1,PrimaryComma,line2,rb,) {
enter_rule ("Atom_listconst");
    set_return (`${lb.rwr ()}${PrimaryComma.rwr ().join ('')}${rb.rwr ()}${line2.rwr ().join ('')}`);
return exit_rule ("Atom_listconst");
},
Atom_dict : function (_78,line1,PairComma,line2,_79,) {
enter_rule ("Atom_dict");
    set_return (`${_78.rwr ()}${line1.rwr ().join ('')}${PairComma.rwr ().join ('')}${line2.rwr ().join ('')}${_79.rwr ()}`);
return exit_rule ("Atom_dict");
},
Atom_phi : function (phi,) {
enter_rule ("Atom_phi");
    set_return (` None`);
return exit_rule ("Atom_phi");
},
Atom_true : function (_88,) {
enter_rule ("Atom_true");
    set_return (` True`);
return exit_rule ("Atom_true");
},
Atom_false : function (_89,) {
enter_rule ("Atom_false");
    set_return (` False`);
return exit_rule ("Atom_false");
},
Atom_subraddress : function (x,) {
enter_rule ("Atom_subraddress");
    set_return (`${x.rwr ()}`);
return exit_rule ("Atom_subraddress");
},
Atom_range : function (_91,_92,Exp,_93,) {
enter_rule ("Atom_range");
    set_return (`${_91.rwr ()}${_92.rwr ()}${Exp.rwr ()}${_93.rwr ()}`);
return exit_rule ("Atom_range");
},
Atom_string : function (string,) {
enter_rule ("Atom_string");
    set_return (` ${string.rwr ()}`);
return exit_rule ("Atom_string");
},
Atom_number : function (number,) {
enter_rule ("Atom_number");
    set_return (` ${number.rwr ()}`);
return exit_rule ("Atom_number");
},
Atom_ident : function (ident,) {
enter_rule ("Atom_ident");
    set_return (` ${ident.rwr ()}`);
return exit_rule ("Atom_ident");
},
Subraddress : function (_,ident,) {
enter_rule ("Subraddress");
    set_return (` ${ident.rwr ()}`);
return exit_rule ("Subraddress");
},
PrimaryComma : function (Primary,_94,line,) {
enter_rule ("PrimaryComma");
    set_return (`${Primary.rwr ()}${_94.rwr ().join ('')}${line.rwr ().join ('')}`);
return exit_rule ("PrimaryComma");
},
PairComma : function (Pair,_95,) {
enter_rule ("PairComma");
    set_return (`${Pair.rwr ()}${_95.rwr ().join ('')}`);
return exit_rule ("PairComma");
},
StuffInsideParentheses_rec : function (lp,stuff,rp,) {
enter_rule ("StuffInsideParentheses_rec");
    set_return (`${lp.rwr ()}${stuff.rwr ().join ('')}${rp.rwr ()}`);
return exit_rule ("StuffInsideParentheses_rec");
},
StuffInsideParentheses_default : function (x,) {
enter_rule ("StuffInsideParentheses_default");
    set_return (`${x.rwr ()}`);
return exit_rule ("StuffInsideParentheses_default");
},
Lval : function (Exp,) {
enter_rule ("Lval");
    set_return (`${Exp.rwr ()}`);
return exit_rule ("Lval");
},
Formals_noformals : function (_148,_149,) {
enter_rule ("Formals_noformals");
    set_return (`${_148.rwr ()}${_149.rwr ()}`);
return exit_rule ("Formals_noformals");
},
Formals_withformals : function (_150,FormalComma,_151,) {
enter_rule ("Formals_withformals");
    set_return (`${_150.rwr ()}${FormalComma.rwr ().join ('')}${_151.rwr ()}`);
return exit_rule ("Formals_withformals");
},
ObjFormals : function (x,) {
enter_rule ("ObjFormals");
    set_return (``);
return exit_rule ("ObjFormals");
},
Formal : function (ident,) {
enter_rule ("Formal");
    set_return (`${ident.rwr ()}`);
return exit_rule ("Formal");
},
FormalComma : function (Formal,comma,) {
enter_rule ("FormalComma");
    set_return (`${Formal.rwr ()}${comma.rwr ().join ('')}`);
return exit_rule ("FormalComma");
},
Actuals_noactuals : function (_154,_155,) {
enter_rule ("Actuals_noactuals");
    set_return (`${_154.rwr ()}${_155.rwr ()}`);
return exit_rule ("Actuals_noactuals");
},
Actuals_actuals : function (_156,ActualComma,_157,line,) {
enter_rule ("Actuals_actuals");
    set_return (`${_156.rwr ()}${ActualComma.rwr ().join ('')}${_157.rwr ()}${line.rwr ().join ('')}`);
return exit_rule ("Actuals_actuals");
},
Actual : function (Exp,) {
enter_rule ("Actual");
    set_return (`${Exp.rwr ()}`);
return exit_rule ("Actual");
},
ActualComma : function (comment,Actual,comma,line,) {
enter_rule ("ActualComma");
    set_return (`${Actual.rwr ()}${comma.rwr ().join ('')}${line.rwr ().join ('')}`);
return exit_rule ("ActualComma");
},
number_fract : function (num,_160,den,) {
enter_rule ("number_fract");
    set_return (`${num.rwr ().join ('')}${_160.rwr ()}${den.rwr ().join ('')}`);
return exit_rule ("number_fract");
},
number_whole : function (digit,) {
enter_rule ("number_whole");
    set_return (`${digit.rwr ().join ('')}`);
return exit_rule ("number_whole");
},
Pair : function (string,_161,Exp,_162,) {
enter_rule ("Pair");
    set_return (`${string.rwr ()}${_161.rwr ()}${Exp.rwr ()}${_162.rwr ().join ('')}`);
return exit_rule ("Pair");
},
andOrIn_and : function (op,) {
enter_rule ("andOrIn_and");
    set_return (` and `);
return exit_rule ("andOrIn_and");
},
andOrIn_or : function (op,) {
enter_rule ("andOrIn_or");
    set_return (` or `);
return exit_rule ("andOrIn_or");
},
andOrIn_in : function (op,) {
enter_rule ("andOrIn_in");
    set_return (` in `);
return exit_rule ("andOrIn_in");
},
andOrIn_bitwiseand : function (op,) {
enter_rule ("andOrIn_bitwiseand");
    set_return (` & `);
return exit_rule ("andOrIn_bitwiseand");
},
boolOp : function (_191,) {
enter_rule ("boolOp");
    set_return (` ${_191.rwr ()} `);
return exit_rule ("boolOp");
},
boolEq : function (op,) {
enter_rule ("boolEq");
    set_return (`==`);
return exit_rule ("boolEq");
},
boolNeq : function (op,) {
enter_rule ("boolNeq");
    set_return (`!=`);
return exit_rule ("boolNeq");
},
string : function (x,) {
enter_rule ("string");
    set_return (`${x.rwr ()}`);
return exit_rule ("string");
},
asciistring : function (lq,cs,rq,) {
enter_rule ("asciistring");
    set_return (`"${cs.rwr ().join ('')}"`);
return exit_rule ("asciistring");
},
unicodestring : function (lq,cs,rq,) {
enter_rule ("unicodestring");
    set_return (`"${cs.rwr ().join ('')}"`);
return exit_rule ("unicodestring");
},
stringchar_rec : function (lb,cs,rb,) {
enter_rule ("stringchar_rec");
    set_return (`${lb.rwr ()}${cs.rwr ().join ('')}${rb.rwr ()}`);
return exit_rule ("stringchar_rec");
},
stringchar_other : function (c,) {
enter_rule ("stringchar_other");
    set_return (`${c.rwr ()}`);
return exit_rule ("stringchar_other");
},
keyword : function (w,) {
enter_rule ("keyword");
    set_return (`${w.rwr ()}`);
return exit_rule ("keyword");
},
phi : function (_192,) {
enter_rule ("phi");
    set_return (` None`);
return exit_rule ("phi");
},
ident : function (cs,) {
enter_rule ("ident");
    set_return (`${cs.rwr ().join ('')}`);
return exit_rule ("ident");
},
idchar_rec : function (lb,cs,rb,) {
enter_rule ("idchar_rec");
    set_return (`${lb.rwr ()}${cs.rwr ().join ('')}${rb.rwr ()}`);
return exit_rule ("idchar_rec");
},
idchar_other : function (c,) {
enter_rule ("idchar_other");
    set_return (`${c.rwr ()}`);
return exit_rule ("idchar_other");
},
idch : function (c,) {
enter_rule ("idch");
    set_return (`${c.rwr ()}`);
return exit_rule ("idch");
},
comment : function (lb,cs,rb,) {
enter_rule ("comment");
    set_return (`${lb.rwr ()}${cs.rwr ().join ('')}${rb.rwr ()}`);
return exit_rule ("comment");
},
commentchar_rec : function (lb,cs,rb,) {
enter_rule ("commentchar_rec");
    set_return (`${lb.rwr ()}${cs.rwr ().join ('')}${rb.rwr ()}`);
return exit_rule ("commentchar_rec");
},
commentchar_other : function (c,) {
enter_rule ("commentchar_other");
    set_return (`${c.rwr ()}`);
return exit_rule ("commentchar_other");
},
errorMessage : function (_239,errorchar,_240,) {
enter_rule ("errorMessage");
    set_return (`${_239.rwr ()}${errorchar.rwr ().join ('')}${_240.rwr ()}`);
return exit_rule ("errorMessage");
},
errorchar_rec : function (_241,errorchar,_242,) {
enter_rule ("errorchar_rec");
    set_return (`${_241.rwr ()}${errorchar.rwr ().join ('')}${_242.rwr ()}`);
return exit_rule ("errorchar_rec");
},
errorchar_other : function (any,) {
enter_rule ("errorchar_other");
    set_return (`${any.rwr ()}`);
return exit_rule ("errorchar_other");
},
line : function (lb,cs,rb,) {
enter_rule ("line");
    set_return (`${lb.rwr ()}${cs.rwr ().join ('')}${rb.rwr ()}`);
return exit_rule ("line");
},
Comma : function (line1,_comma,line2,) {
enter_rule ("Comma");
    set_return (`${_comma.rwr ()}`);
return exit_rule ("Comma");
},
_terminal: function () { return this.sourceString; },
_iter: function (...children) { return children.map(c => c.rwr ()); }
}
import * as fs from 'fs';

let terminated = false;

function xbreak () {
    terminated = true;
    return '';
}

function xcontinue () {
    terminated = false;
    return '';
}
    
function is_terminated () {
    return terminated;
}
function expand (src, parser) {
    let cst = parser.match (src);
    if (cst.failed ()) {
	//th  row Error (`${cst.message}\ngrammar=${grammarname (grammar)}\nsrc=\n${src}`);
	throw Error (cst.message);
    }
    let sem = parser.createSemantics ();
    sem.addOperation ('rwr', _rewrite);
    return sem (cst).rwr ();
}

function grammarname (s) {
    let n = s.search (/{/);
    return s.substr (0, n).replaceAll (/\n/g,'').trim ();
}

try {
    const argv = process.argv.slice(2);
    let srcFilename = argv[0];
    if ('-' == srcFilename) { srcFilename = 0 }
    let src = fs.readFileSync(srcFilename, 'utf-8');
    try {
	let parser = ohm.grammar (grammar);
	let s = src;
	xcontinue ();
	while (! is_terminated ()) {
	    xbreak ();
	    s = expand (s, parser);
	}
	console.log (s);
	process.exit (0);
    } catch (e) {
	//console.error (`${e}\nargv=${argv}\ngrammar=${grammarname (grammar)}\src=\n${src}`);
	console.error (`${e}\n\ngrammar = "${grammarname (grammar)}\n"`);
	process.exit (1);
    }
} catch (e) {
    console.error (`${e}\n\ngrammar = "${grammarname (grammar)}"\n`);
    process.exit (1);
}

