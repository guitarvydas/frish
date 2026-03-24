//fs.writeFileSync('/tmp/@pbplog.md', new Date().toISOString() + '\n');

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
