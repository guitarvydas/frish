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
pythontransmogrifier {
  code = item+
  item =
    | applySyntactic<Pattern> -- pattern
    | any -- other
  Pattern =
    | "B" "=" "State.S.pop" "(" ")" line?
      "A" "=" "State.S.pop" "(" ")" line?
      "State.S.push" "(" "B" ")" line?
      "State.S.push" "(" "A" ")" line?     -- swap

  Inits = "subrs" "[" #str "]" "=" #ident #eol Inits?
  str (str) = "\"" (~"\"" any)* "\""

  exprCh (exprCh) =
    | "(" exprCh+ ")" -- recursive
    | ~")" item        -- flat

  eol (eol) = spaces line*
    
  ident (ident) = spaces (letter | "_") (letter | digit | "_")*
  
  line = spaces "⎩" (~"⎩" ~"⎭" any)* "⎭"
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

code : function (item,) {
enter_rule ("code");
    set_return (`${item.rwr ().join ('')}`);
return exit_rule ("code");
},
item_pattern : function (p,) {
enter_rule ("item_pattern");
    set_return (`${p.rwr ()}`);
return exit_rule ("item_pattern");
},
item_other : function (c,) {
enter_rule ("item_other");
    set_return (`${c.rwr ()}`);
return exit_rule ("item_other");
},
Pattern_swap : function (_1,_2,_3,_4,_5,l1,_7,_8,_9,_10,_11,l2,_13,_14,_15,_16,l3,_18,_19,_20,_21,l4,) {
enter_rule ("Pattern_swap");
    set_return (`\nx = Stack [-1]\nStack [-1] = Stack [-2]\nStack [-2] = x ${l1.rwr ().join ('')}`);
return exit_rule ("Pattern_swap");
},
Inits : function (_subrs,_lb,s,_rb,_eq,id,eol,more,) {
enter_rule ("Inits");
    set_return (`\n${s.rwr ()} : ${id.rwr ()},${more.rwr ().join ('')}`);
return exit_rule ("Inits");
},
str : function (_lq,cs,_rq,) {
enter_rule ("str");
    set_return (`${_lq.rwr ()}${cs.rwr ().join ('')}${_rq.rwr ()}`);
return exit_rule ("str");
},
exprCh_recursive : function (_lb,e,_rb,) {
enter_rule ("exprCh_recursive");
    set_return (`${_lb.rwr ()}${e.rwr ().join ('')}undefined`);
return exit_rule ("exprCh_recursive");
},
exprCh_flat : function (c,) {
enter_rule ("exprCh_flat");
    set_return (`${c.rwr ()}`);
return exit_rule ("exprCh_flat");
},
eol : function (ws,line,) {
enter_rule ("eol");
    set_return (`${ws.rwr ()}${line.rwr ().join ('')}`);
return exit_rule ("eol");
},
ident : function (ws,c,cs,) {
enter_rule ("ident");
    set_return (`${c.rwr ()}${cs.rwr ().join ('')}`);
return exit_rule ("ident");
},
line : function (ws,_lb,cs,_rb,) {
enter_rule ("line");
    set_return (`${ws.rwr ()}${_lb.rwr ()}${cs.rwr ().join ('')}${_rb.rwr ()}`);
return exit_rule ("line");
},
spaces : function (cs,) {
enter_rule ("spaces");
    set_return (``);
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

