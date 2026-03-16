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
    fs.appendFileSync('/tmp/@pbplog.md', `resetlog` + '\n');    
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
