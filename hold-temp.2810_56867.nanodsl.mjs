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
pretransmogrifier {
  code = item+
  item =
    | applySyntactic<ScopedSubr> -- scopedsubr
    | any -- other
    
  ScopedSubr = "defsubr" subrname str "{" #subrinnards "}"
  subrinnards =
    | "{" subrinnards "}" subrinnards?     -- rec
    | applySyntactic<Pattern> subrinnards? -- pattern
    | ~"}" any  subrinnards?            -- other

  Pattern =
    | "defsynonym" name "≡" PureExpression -- memomacro
    
  exprCh = ~"{" any
  bodyCh =
    | "{" bodyCh+ "}" -- recursive
    | ~"}" item     -- flat

  PureExpression =
    | "(" PureExpression ")" -- parenthesized
    | primary "[" PureExpression "]" -- indexed
    | primary op PureExpression -- op
    | primary -- primary
  
  primary = int | "State.RAM" | "State.IP" | "State.W" | "State.LAST" | "State.BUFFP" | "State.BUFF" |  name
  op = "+" | "-" | "*" | "/" | ">=" | "<=" | "<" | ">" | "and" | "or" | "="
  int = "-"? digit+
  subrname = id
  name = id
  id = (letter | "_") (alnum | "_")*
  str = "\"" (~"\"" any)* "\""
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

function resetmacros () {
    macros = {};
}   
 
function memomacro (name, s) {
    fs.appendFileSync('/tmp/@pbplog.md', `memomacro ${name} == /${s}/` + '\n');    
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

code : function (item,) {
enter_rule ("code");
    set_return (`${item.rwr ().join ('')}`);
return exit_rule ("code");
},
item_scopedsubr : function (s,) {
enter_rule ("item_scopedsubr");
    set_return (`${s.rwr ()}`);
return exit_rule ("item_scopedsubr");
},
item_other : function (c,) {
enter_rule ("item_other");
    set_return (`${c.rwr ()}`);
return exit_rule ("item_other");
},
ScopedSubr : function (_def,name,str,lb,innards,rb,) {
enter_rule ("ScopedSubr");
    resetmacros ();
    
    set_return (`\ndefsubr ${name.rwr ()} ${str.rwr ()} { ${innards.rwr ()} } `);

return exit_rule ("ScopedSubr");
},
subrinnards_rec : function (lb,innards,rb,rec,) {
enter_rule ("subrinnards_rec");
    set_return (`{${innards.rwr ().join ('')}}${rec.rwr ().join ('')}`);
return exit_rule ("subrinnards_rec");
},
subrinnards_pattern : function (p,rec,) {
enter_rule ("subrinnards_pattern");
    set_return (`${p.rwr ()}${rec.rwr ().join ('')}`);
return exit_rule ("subrinnards_pattern");
},
subrinnards_other : function (c,rec,) {
enter_rule ("subrinnards_other");
    set_return (`${c.rwr ()}${rec.rwr ().join ('')}`);
return exit_rule ("subrinnards_other");
},
Pattern_memomacro : function (_defsyn,name,_def,e,) {
enter_rule ("Pattern_memomacro");
    memomacro (`${name.rwr ()}`,`${e.rwr ()}`,);
    
    set_return (` ${xcontinue ()}`);

return exit_rule ("Pattern_memomacro");
},
exprCh : function (c,) {
enter_rule ("exprCh");
    set_return (`${c.rwr ()}`);
return exit_rule ("exprCh");
},
bodyCh_recursive : function (_lb,cs,_rb,) {
enter_rule ("bodyCh_recursive");
    set_return (`${_lb.rwr ()}${cs.rwr ().join ('')}${_rb.rwr ()}`);
return exit_rule ("bodyCh_recursive");
},
bodyCh_flat : function (c,) {
enter_rule ("bodyCh_flat");
    set_return (`${c.rwr ()}`);
return exit_rule ("bodyCh_flat");
},
PureExpression_parenthesized : function (lp,e,rp,) {
enter_rule ("PureExpression_parenthesized");
    set_return (`(${e.rwr ()})`);
return exit_rule ("PureExpression_parenthesized");
},
PureExpression_indexed : function (p,lb,e,rb,) {
enter_rule ("PureExpression_indexed");
    set_return (`${p.rwr ()}[${e.rwr ()}]`);
return exit_rule ("PureExpression_indexed");
},
PureExpression_op : function (prim,op,e,) {
enter_rule ("PureExpression_op");
    set_return (`(${prim.rwr ()}${op.rwr ()}${e.rwr ()})`);
return exit_rule ("PureExpression_op");
},
PureExpression_primary : function (prim,) {
enter_rule ("PureExpression_primary");
    set_return (`(${prim.rwr ()})`);
return exit_rule ("PureExpression_primary");
},
primary : function (p,) {
enter_rule ("primary");
    set_return (`${p.rwr ()}`);
return exit_rule ("primary");
},
op : function (x,) {
enter_rule ("op");
    set_return (`${x.rwr ()}`);
return exit_rule ("op");
},
int : function (sign,ds,) {
enter_rule ("int");
    set_return (`${sign.rwr ().join ('')}${ds.rwr ().join ('')}`);
return exit_rule ("int");
},
subrname : function (s,) {
enter_rule ("subrname");
    set_return (`${s.rwr ()}`);
return exit_rule ("subrname");
},
name : function (s,) {
enter_rule ("name");
    set_return (`${macrolookup (`${s.rwr ()}`,)}`);
return exit_rule ("name");
},
id : function (c,cs,) {
enter_rule ("id");
    set_return (`${c.rwr ()}${cs.rwr ().join ('')}`);
return exit_rule ("id");
},
str : function (lq,cs,rq,) {
enter_rule ("str");
    set_return (`"${cs.rwr ().join ('')}"`);
return exit_rule ("str");
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

