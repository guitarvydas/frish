if (found_p ()) {
    if (incompilingstate_p ()) {
        if (foundimmediate_p ()) {
            return λexec(item);
        } else {
            return λcompileword(item);
        }
        
    } else {
        return λexec(item);
    }
    
} else {
    if (incompilingstate_p ()) {
        if (isinteger(item)_p ()) {
            return λcompileinteger(item);
        } else {
            if (isfloat(item)_p ()) {
                return λcompilefloat(item);
            } else {
                return returnFalse;
            }
            
        }
        
    } else {
        if (isinteger(item)_p ()) {
            return λpushasinteger(item);
        } else {
            if (isfloat(item)_p ()) {
                return λpushasfloat(item);
            } else {
                return returnFalse;
            }
            
        }
        
    }
    
}