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
splitter {

  main = subrOrFunction+ initializeSection

  subrOrFunction = subroutineDefinition | functionDefinition
  initializeSection (initializeSection) = noise "initialize" noise "{" noise "λ" ident noise "(" noise ")" noise "}" noise

  functionDefinition (functionDefinition) = noise "function" noise token noise formals noise statementBlock noise
  subroutineDefinition (subroutineDefinition) =
    | noise "subr" noise "%immediate" noise token noise statementBlock noise -- immediate
    | noise "subr"                    noise token noise statementBlock noise -- normal

  statementBlock = noise "{" blockInnard+ "}" noise
  blockInnard =
    | "{" blockInnard+ "}" blockInnard+ -- rec
    | ~"}" any -- other

  formals (formals) = "(" (~")" any)* ")"
  token = spaces (~space any)+
  ident  = idchar+
  idchar =
    | "❲" idchar+ "❳" -- rec
    | ~"❲" ~"❳" idch -- other

  idch = letter | digit | "_" | "-"

  comment = "⌈" commentchar* "⌉"
  commentchar = 
    | "⌈" commentchar* "⌉" -- rec
    | ~"⌈" ~"⌉" any -- other

  line = "⎩" (~"⎩" ~"⎭" any)* "⎭"

  noise = spaces line* spaces noi* spaces noi* spaces
  noi = line | comment | space
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

//fs.writeFileSync('/tmp/@pbplog.md', new Date().toISOString() + '\n');

let linenumber = 0;
function getlineinc () {
    linenumber += 1;
    return `${linenumber}`;
}

function pynlcomments (s) {
    return s.replace (/\n/g, '\n#')
}

class DictStack {
  constructor() {
    this.stack = [];
  }

  push(dict) {
    this.stack.push(dict);
  }

  pop() {
    return this.stack.pop();
  }

  // Search from top of stack downward; return value if found, else return the key itself
  lookup(key) {
    for (let i = this.stack.length - 1; i >= 0; i--) {
      if (Object.hasOwn(this.stack[i], key)) {
        return this.stack[i][key];
      }
    }
    return key; // not found anywhere — return the key itself
  }
}

let macros = new DictStack ();

function pushnewmacroscope () {
    macros.push ({});
    return "";
}
function popmacroscope () {
    macros.pop ();
    return "";
}
 
function memomacro (name, s) {
    let topmacroscope = macros.pop ();
    topmacroscope [name] = s;
    macros.push (topmacroscope);
    return "";
}

function macrolookup (name) {
    return macros.lookup (name);
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

main : function (SubrOrFunction,InitializeSection,) {
enter_rule ("main");
    set_return (` ${SubrOrFunction.rwr ().join ('')}${InitializeSection.rwr ()}`);
return exit_rule ("main");
},
subrOrFunction : function (sf,) {
enter_rule ("subrOrFunction");
    set_return (`${sf.rwr ()}`);
return exit_rule ("subrOrFunction");
},
initializeSection : function (noise1,_initialize,noise2,lb,noise3,_lambda,ident,noise4,lp,noise5,lr,noise6,rb,noise7,) {
enter_rule ("initializeSection");
    set_return (``);
return exit_rule ("initializeSection");
},
functionDefinition : function (noise1,_function,noise2,token,noise3,formals,noise4,block,noise5,) {
enter_rule ("functionDefinition");
    set_return (`${noise1.rwr ()} ${_function.rwr ()} ${noise2.rwr ()} ${token.rwr ()}${noise3.rwr ()}${formals.rwr ()}${noise4.rwr ()}${block.rwr ()}${noise5.rwr ()}`);
return exit_rule ("functionDefinition");
},
subroutineDefinition_immediate : function (noise1,_subr,noise2,_immediate,noise3,token,noise4,block,noise5,) {
enter_rule ("subroutineDefinition_immediate");
    set_return (``);
return exit_rule ("subroutineDefinition_immediate");
},
subroutineDefinition_normal : function (noise1,_subr,noise2,token,noise3,block,noise4,) {
enter_rule ("subroutineDefinition_normal");
    set_return (``);
return exit_rule ("subroutineDefinition_normal");
},
statementBlock : function (noise1,lb,BlockInnard,rb,noise2,) {
enter_rule ("statementBlock");
    set_return (`${noise1.rwr ()}${lb.rwr ()}${BlockInnard.rwr ().join ('')}${rb.rwr ()}${noise2.rwr ()}`);
return exit_rule ("statementBlock");
},
blockInnard_rec : function (lb,BlockInnard1,rb,BlockInnard2,) {
enter_rule ("blockInnard_rec");
    set_return (`${lb.rwr ()}${BlockInnard1.rwr ().join ('')}${rb.rwr ()}${BlockInnard2.rwr ().join ('')}`);
return exit_rule ("blockInnard_rec");
},
blockInnard_other : function (c,) {
enter_rule ("blockInnard_other");
    set_return (`${c.rwr ()}`);
return exit_rule ("blockInnard_other");
},
formals : function (lp,cs,rp,) {
enter_rule ("formals");
    set_return (`${lp.rwr ()}${cs.rwr ().join ('')}${rp.rwr ()}`);
return exit_rule ("formals");
},
token : function (spaces,cs,) {
enter_rule ("token");
    set_return (`${spaces.rwr ()}${cs.rwr ().join ('')}`);
return exit_rule ("token");
},
ident : function (idchar,) {
enter_rule ("ident");
    set_return (`${idchar.rwr ().join ('')}`);
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
comment : function (lb,commentchar,rb,) {
enter_rule ("comment");
    set_return (`${lb.rwr ()}${commentchar.rwr ().join ('')}${rb.rwr ()}`);
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
line : function (lb,cs,rb,) {
enter_rule ("line");
    set_return (`${lb.rwr ()}${cs.rwr ().join ('')}${rb.rwr ()}`);
return exit_rule ("line");
},
noise : function (ws1,line,ws2,n1,ws3,n2,ws4,) {
enter_rule ("noise");
    set_return (`${ws1.rwr ()}${line.rwr ().join ('')}${ws2.rwr ()}${n1.rwr ().join ('')}${ws3.rwr ()}${n2.rwr ().join ('')}${ws4.rwr ()}`);
return exit_rule ("noise");
},
noi : function (x,) {
enter_rule ("noi");
    set_return (`${x.rwr ()}`);
return exit_rule ("noi");
},
spaces : function (s,) {
enter_rule ("spaces");
    set_return (`${s.rwr ().join ('')}`);
return exit_rule ("spaces");
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

