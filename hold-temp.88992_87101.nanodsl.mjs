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
pydecode {
  text = char+
  char =
    | unicode_string  -- unicodestring
    | "⌈" (~"⌈" ~"⌉" any)* "⌉"  -- comment
    | "⎝" (~"⎝" ~"⎠" any)* "⎠"  -- errormessage
    | "⎩" (~"⎩" ~"⎭" any)* "⎭"  -- line
    | historical_edge_case      -- edgecase
    | any                       -- other

  historical_edge_case =
    | "❲"                       -- ulb
    | "%E2%9D%B2"               -- encodedulb
    | "❳"                       -- urb
    | "%E2%9D%B3"               -- encodedurb
    | "%20"                     -- space
    | "%09"                     -- tab
    | "%0A"                     -- newline
    | "¶"                       -- paramark

  unicode_string = "“" ustringchar* "”"
  ustringchar =
    | "“" ustringchar* "”" -- nested
    | ~"“" ~"”" any -- other
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

text : function (chars,) {
enter_rule ("text");
    set_return (`${chars.rwr ().join ('')}`);
return exit_rule ("text");
},
char_unicodestring : function (s,) {
enter_rule ("char_unicodestring");
    set_return (`${s.rwr ()}`);
return exit_rule ("char_unicodestring");
},
char_comment : function (lb,cs,rb,) {
enter_rule ("char_comment");
    set_return (`#${pynlcomments (`${cs.rwr ().join ('')}`,)}`);
return exit_rule ("char_comment");
},
char_errormessage : function (lb,cs,rb,) {
enter_rule ("char_errormessage");
    set_return (` >>> ${cs.rwr ().join ('')} <<< `);
return exit_rule ("char_errormessage");
},
char_line : function (lb,cs,rb,) {
enter_rule ("char_line");
    set_return (`#line ${cs.rwr ().join ('')}`);
return exit_rule ("char_line");
},
char_other : function (c,) {
enter_rule ("char_other");
    set_return (`${c.rwr ()}`);
return exit_rule ("char_other");
},
historical_edge_case_ulb : function (c,) {
enter_rule ("historical_edge_case_ulb");
    set_return (``);
return exit_rule ("historical_edge_case_ulb");
},
historical_edge_case_encodedulb : function (c,) {
enter_rule ("historical_edge_case_encodedulb");
    set_return (`_L`);
return exit_rule ("historical_edge_case_encodedulb");
},
historical_edge_case_urb : function (c,) {
enter_rule ("historical_edge_case_urb");
    set_return (``);
return exit_rule ("historical_edge_case_urb");
},
historical_edge_case_encodedurb : function (c,) {
enter_rule ("historical_edge_case_encodedurb");
    set_return (`R_`);
return exit_rule ("historical_edge_case_encodedurb");
},
historical_edge_case_space : function (c,) {
enter_rule ("historical_edge_case_space");
    set_return (`_`);
return exit_rule ("historical_edge_case_space");
},
historical_edge_case_tab : function (c,) {
enter_rule ("historical_edge_case_tab");
    set_return (`	`);
return exit_rule ("historical_edge_case_tab");
},
historical_edge_case_newline : function (c,) {
enter_rule ("historical_edge_case_newline");
    set_return (`
`);
return exit_rule ("historical_edge_case_newline");
},
historical_edge_case_paramark : function (c,) {
enter_rule ("historical_edge_case_paramark");
    set_return (`¶`);
return exit_rule ("historical_edge_case_paramark");
},
unicode_string : function (lq,cs,rq,) {
enter_rule ("unicode_string");
    set_return (`${lq.rwr ()}${cs.rwr ().join ('')}${rq.rwr ()}`);
return exit_rule ("unicode_string");
},
ustringchar_nested : function (lq,cs,rq,) {
enter_rule ("ustringchar_nested");
    set_return (`${lq.rwr ()}${cs.rwr ().join ('')}${rq.rwr ()}`);
return exit_rule ("ustringchar_nested");
},
ustringchar_other : function (c,) {
enter_rule ("ustringchar_other");
    set_return (`${c.rwr ()}`);
return exit_rule ("ustringchar_other");
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

