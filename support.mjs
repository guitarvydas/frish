/////// <pbp logging>
//const fs = require('fs');
//const path = require('path');
import * as path from 'path';

function pbplog(message) {
  const baseDir = process.env.PBPCALLER;
  if (!baseDir) throw new Error('PBPCALLER env var not set');
  
  const logFile = path.join(baseDir, 'pbplog.txt');
  fs.appendFileSync(logFile, `${message}\n`, 'utf8');
}

//fs.writeFileSync('/tmp/@pbplog.txt', new Date().toISOString() + '\n');
/////// </pbp logging>

let linenumber = 0;
function getlineinc () {
    linenumber += 1;
    return `${linenumber}`;
}

function pynlcomments (s) {
    return s.replace (/\n/g, '\n#')
}

let braces = [];
let parens = [];
function incbrace () { braces.push (linenumber); return ""; }
function decbrace () {
    braces.pop ();
    return ""; 
}
function incparen () { parens.push (linenumber); return ""; }
function decparen () { 
    parens.pop ();
    return "";
}
function setline (n) {
    linenumber = n;
    return "";
}
function reportbraces () {return `[${braces}]`;}
function reportparens () {return `[${parens}]`;}

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
    pbplog (`push new macro scope`);
    return "";
}
function popmacroscope () {
    macros.pop ();
    pbplog (`pop macro scope`);
    return "";
}
 
function memomacro (name, s) {
    let topmacroscope = macros.pop ();
    topmacroscope [name] = s;
    macros.push (topmacroscope);
    pbplog (`  memomacro /${name}/<-/${s}/ ${macros}`);
    return "";
}

function macrolookup (name) {
    pbplog (`  macrolookup /${name}/ -> ${macros.lookup (name)}`);
    return macros.lookup (name);
}
