import re

class Stack(list):
    def push(my, *items):
        my.extend(items)

class StateClass:
    def __init__ (self):
        self.S = Stack()
        self.R = Stack()
        self.RAM = []
        self.LAST = -1
        self.IP = None
        self.W = None;
        self.BUFF = ""
        self.BUFP = 0
        self.compiling = [False]

State = StateClass ()

                                                       #line 1
# fvget and fvset assume that the forth object (word) is a set of contiguous slots, each 1 machine word wide⎩2⎭
#    these functions use direct integer offsets to access the fields of the fojbect, whereas in higher level languages⎩3⎭
#    we'd use class fields instead - todo: fix this in the future (or not? at what point is customization better than⎩4⎭
#    generalization?)                                  #line 5
def fvget (name):
    global State                                       #line 6

    fobjaddress =  _find(State.S.pop ())               #line 7
    return  State.RAM [ fobjaddress +  1]              #line 8

                                                       #line 9
                                                       #line 10

def fvset (name,v):
    global State                                       #line 11

    fobjaddress =  _find(State.S.pop ())               #line 12 #line 13
    State.RAM [( fobjaddress + ( 1))] =  v             #line 14

                                                       #line 15
                                                       #line 16
                                                       #line 17

def doword ():
    global State                                       #line 18
    #⎩19⎭Executeacolon-definedwordusingindirectthreadedcodeinterpretation.⎩20⎭
    #⎩21⎭Thisfunctionimplementstheinnerinterpreterforthreadedcodeexecution.⎩22⎭Threadedcodewordsstoretheirdefinitionsasarraysofcodefieldaddresses⎩23⎭
    #  (CFAs)intheparameterfieldarea(PFA)immediatelyfollowingthewordheader.⎩24⎭
    #⎩25⎭Theexecutionmodelmaintainstwocriticalregisters:⎩26⎭
    #⎩27⎭
    #  1.IP(InstructionPointer):Referencesthecurrentpositionwithinthe⎩28⎭threadedcodearraybeinginterpreted.Sincethreadedwordsmayinvoke⎩29⎭otherthreadedwords,IPmustbepreservedinareentrantmannervia⎩30⎭thereturnstackoneachinvocation.⎩31⎭
    #⎩32⎭
    #  2.W(WordPointer):ReferencestheCFAofthecurrentlyexecutingprimitive.⎩33⎭Thisglobalregisterservesananalogousfunctionto'self'inobject-oriented⎩34⎭languages,enablingsubroutinestoaccesswordheaderfieldsthroughfixed⎩35⎭offsetsfromtheCFA.⎩36⎭
    #⎩37⎭Optimizationrationale:WispositionedtoreferencetheCFAratherthanthe⎩38⎭wordheaderbase.ThisdesigneliminatesoffsetarithmeticforCFAaccess—the⎩39⎭mostfrequentheaderoperation—atthecostofrequiringoffsetadjustments⎩40⎭forotherheaderfields(NFA:W-2,flags:W-1,PFA:W+1).Thisrepresentsa⎩41⎭deliberatetrade-offfavoringthecommoncase.⎩42⎭
    #⎩43⎭Theinnerinterpreterloopperformsthefollowingoperations:⎩44⎭
    #  -FetchthenextCFAfromRAM[IP]intoW(performingthefirstindirection)⎩45⎭
    #  -IncrementIPtoadvancethroughthethreadedcodearray⎩46⎭
    #  -ExecutetheprimitiveviaRAM[W]() (performingthesecondindirection)⎩47⎭
    #⎩48⎭BycachingthedereferencedCFAinW,weamortizethecostofdouble⎩49⎭indirection:bothprimitiveexecutionandheaderfieldaccesswithin⎩50⎭subroutinesutilizethesamecachedreference,avoidingredundant⎩51⎭dereferences.Thisisfunctionallyequivalenttoparameterpassingin⎩52⎭object-orientedmethodinvocation,buteliminatestheoverheadof⎩53⎭explicitlypassing'self'toeachprimitive.⎩54⎭
    #⎩55⎭Note:Wsstateisonlydefinedduringprimitiveexecution(withinRAM[W]()).⎩56⎭Betweenloopiterations,WmayreferenceastaleCFA,butthisis⎩57⎭architecturallysoundsinceWisunconditionallyupdatedbeforeeach⎩58⎭primitiveinvocation.⎩59⎭
    #                                                  #line 60
                                                       #line 61

    State.R.append ( State.IP)                         #line 62
    State.IP =  State.W +  1                           #line 63
    while ( -1 !=  State.RAM [ State.IP]):
                                                       #line 64
        State.W =  State.RAM [ State.IP]               #line 65
        State.IP =  State.IP +  1                      #line 66

        State.R.push ( State.RAM [ State.W])
        _walk ()                                       #line 67

                                                       #line 68


    State.IP = State.R.pop ()                          #line 69

                                                       #line 70
                                                       #line 71
                                                       #line 72

def notfound (word):
    global State                                       #line 73


    State.S.clear()                                    #line 74


    State.R.clear()                                    #line 75

    print ( word, end="")                              #line 76

    print ( "?", end="")                               #line 77

    print ()                                           #line 78

                                                       #line 79
                                                       #line 80

def exec (xt):
    global State                                       #line 81
    #foundandcompilingandimmediate                     #line 82
    State.W =  xt                                      #line 83
    State.IP =  -1#Dummytoholdplaceinreturnstack. 	    #line 84

    State.R.push ( State.RAM [ xt])
    _walk ()  #Executecode.                            #line 85

                                                       #line 86
                                                       #line 87

def compile_word (xt):
    global State                                       #line 88
    #foundandnotcompiling                              #line 89
    State.W =  xt                                      #line 90
    State.IP =  -1#Dummytoholdplaceinreturnstack. 	    #line 91

    State.R.push ( State.RAM [ xt])
    _walk ()  #Executecode.                            #line 92

                                                       #line 93
                                                       #line 94

def pushasinteger (word):
    global State                                       #line 95

    State.S.push (int ( word))                         #line 96

                                                       #line 97
                                                       #line 98

def pushasfloat (word):
    global State                                       #line 99

    State.S.push (float ( word))                       #line 100

                                                       #line 101
                                                       #line 102

def compileinteger (word):
    global State                                       #line 103

    pushasinteger( word)                               #line 104

    State.R.push ("literalize")
    _walk ()                                           #line 105

                                                       #line 106
                                                       #line 107

def compilefloat (word):
    global State                                       #line 108

    pushasfloat( word)                                 #line 109

    State.R.push ("literalize")
    _walk ()                                           #line 110

                                                       #line 111
                                                       #line 112

def code (name,flags,does):
    global State                                       #line 113
    #AddnewwordtoRAMdictionary.Wecreateaword(Forth"object")inRAMwith5fieldsandextendthe⎩114⎭thedictionarybylinkingbacktotheheadofthedictionarylist#line 115
    x =  len( State.RAM)                               #line 116
                                                       #line 117


    State.RAM.append ( State.LAST) # (LFA)linktopreviouswordindictionarylist#line 118


    State.RAM.append ( name)       # (NFA)nameofword   #line 119


    State.RAM.append ( flags)      #       0 =normalword, 1 =immediateword#line 120


    State.RAM.append ( does)       # (CFA)functionpointerthatpointstocodethatexecutestheword(afunctionpointerisnowjustastring(probablyshouldbeoptimizedtobeabytecode)) #line 121
                                                       #line 122
    State.LAST =  x#LASTisthepointertotheheadofthedictionarylist,setittopointto⎩123⎭thisnewword#line 124

                                                       #line 125
                                                       #line 126

def literalize ():
    global State                                       #line 127
    #Compileliteralintodefinition.                     #line 128


    State.RAM.append ( _find( "(literal)"))  ##Compileaddressofdoliteral. #line 129


    State.RAM.append (State.S.pop ())             # #Compileliteralvalue. #line 130

                                                       #line 131
                                                       #line 132

def xinterpret ():
    global State                                       #line 133

    State.R.push ("interpret")
    _walk ()                                           #line 134
    return State.S.pop ()                              #line 135

                                                       #line 136
                                                       #line 137

def ok ():
    global State                                       #line 138
    # ( --)Interactionloop--REPL                       #line 139 #line 140
    while  True:
                                                       #line 141


        State.BUFF = input("OK ")
        State.BUFP = 0
                                                       #line 142
        while not (State.BUFP >= len(State.BUFF)):
                                                       #line 143

            xinterpret()                               #line 144

                                                       #line 145


                                                       #line 146


                                                       #line 147
                                                       #line 148

def doconst ():
    global State#methodforconst                        #line 149 #line 150

    State.S.push ( State.RAM [( State.W + ( 1))])      #line 151

                                                       #line 152
                                                       #line 153
                                                       #line 154

def docreate ():
    global State                                       #line 155

    parameterAddress =  len( State.RAM)  +  4          #line 156

    State.S.push ( parameterAddress)                   #line 157

                                                       #line 158

def create ():
    global State                                       #line 159 #line 160
    code(( 0))                                         #line 161

                                                       #line 162
                                                       #line 163


def _walk ():
    global State
    opcode = State.R.pop ()
    match opcode:
        case "drop":                                   #line 164
            # (a-- )                                   #line 165

            State.S.pop ()                             #line 166

                                                       #line 167
                                                       #line 168




code( "drop",  0,  "drop")                             #line 169

ok()                                                   #line 170
                                                       #line 171