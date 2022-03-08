
from cmath import exp


colorGrammar = {
    # COLOR:
    "<start>":
        ["<Color>"],
    "<Color>":
        ["#<digit><hexChar><hexChar>"],
    "<hexChar>":
        ["<lowercaseHexChar>", "<uppercaseHexChar>"],
    "<uppercaseHexChar>":
        [chr(order) for order in range(ord('A'), ord('F')+1)],
    "<lowercaseHexChar>":
        [chr(order) for order in range(ord('a'), ord('f')+1)],  
    "<digit>":
        [str(i) for i in range(0, 10)]
}

NumberGrammar = {
    "<start>":
        ["<Number>"],
    # number
    "<Number>":
        ["<integer>", "-<integer>", "<integer>.<digits>", "-<integer>.<digits>"],
    "<integer>": # number语法，不允许前导零
        ["<leadingdigit><digits>"],
    "<leadingdigit>":
        [str(i) for i in range(1, 10)],
    "<digits>":  # digits string，不管有无前导零
        ["<digit>", "<digit><digits>"], 
    "<digit>":
        [str(i) for i in range(0, 10)]
}

urlGrammar = {

    "<start>":
        ["<url>"],
    
    "<url>":
        ["<LPAREN><Url><RPAREN>"],

    "<Url>":
        ["\"<scheme>://<authority><path><query>\""],

    "<scheme>":
        ["http", "https", "ftp", "ftps"],
    "<authority>":
        ["<host>", "<host>:<port>", "<userinfo>@<host>", "<userinfo>@<host>:<port>"],
    "<host>":  # Just a few
        ["cispa.saarland", "www.google.com", "fuzzingbook.com"],
    "<port>":
        ["80", "8080", "<nat>"],
    "<nat>":
        ["<digit>", "<digit><digit>"],
    "<digit>":
        [str(i) for i in range(0, 10)],
    "<userinfo>":  # Just one
        ["user:password"],
    "<path>":  # Just a few
        ["", "/", "/<id>"],
    "<id>":  # Just a few
        ["abc", "def", "x<digit><digit>"],
    "<query>":
        ["", "?<params>"],
    "<params>":
        ["<param>", "<param>&<params>"],
    "<param>":  # Just a few
        ["<id>=<id>", "<id>=<nat>"],
    
    "<LPAREN>": ["("],
    "<RPAREN>": [")"]

}

stringGrammar = {
    # string
    "<start>":
        ["<STRING>"],
    "<STRING>":
        ["\"<string>\""],
    "<string>":
        ["<char>", "<char><string>"],
    "<char>":
        [chr(32), chr(33)] + [chr(order) for order in range(35, 92)] + [chr(order) for order in range(93, 127)]
}


IdentifierGrammar = {
    # Identifier
    "<Identifier>": 
        ["<idStart><characters>"], ##???, "-<idStart><characters>"],

    "<idStart>":
        ["<uppercaseChar>", "<lowercaseChar>"], #, "_"], ##??? , "-"],
    
    "<characters>":
        ["<character>", "<character><characters>"],
    
    "<character>":
        ["<uppercaseChar>", "<lowercaseChar>", "<digit>"], #, "_"],  ##??? , "-"],

    "<uppercaseChar>":
        [chr(order) for order in range(ord('A'), ord('Z')+1)],

    "<lowercaseChar>":
        [chr(order) for order in range(ord('a'), ord('z')+1)],   

    #"<unicodeChar>":
    #    [chr(order) for order in range(ord('\u0100'), ord('\uffff'))],
    
    "<digit>":
        [str(i) for i in range(0, 10)],
}

stringGrammar = {
    # string
    "<STRING>":
        ["\"<string>\""],
    
    "<string>":
        ["<char>", "<char><string>"],
    
    "<char>":
        [chr(32), chr(33)] + [chr(order) for order in range(35, 92)] + [chr(order) for order in range(93, 127)],

}

variableNameGrammar = {
    "<start>": 
        ["<variableName>"],

    "<variableName>":
        ["<DOLLAR><Identifier>",
         #"<MINUS_DOLLAR><Identifier>",
         #"<PLUS_DOLLAR><Identifier>",
         "<namespaces><MINUS><Identifier>"],
         #"<namespaces><MINUS_DOLLAR><Identifier>",
         #"<namespaces><PLUS_DOLLAR><Identifier>"],

    "<namespaces>":
        ["<namespace>", "<namespace><namespaces>"],
    
    "<namespace>":
        ["<Identifier>"],
    
    "<DOLLAR>": ["$"],
    "<MINUS>":  ["-"]
}
variableNameGrammar.update(IdentifierGrammar)


properties_Grammar = {
    "<start>": 
        ["<properties_>"],
    "<properties_>":
        ["", "<property_><properties_>"],
    
    "<property_>":
        ["<Identifier><COLON> <propertyValue> <SEMI>",
         "<Identifier><COLON> <propertyValue> <IMPORTANT> <SEMI>"],

    "<lastProperty>":
        ["<Identifier><COLON> <propertyValue>",
         "<Identifier><COLON> <propertyValue> <IMPORTANT>"],

    "<propertyValue>":
        ["<commandStatement> <consecCommandStatements>",
         "<commandStatement> <consecCommandStatements>"],

    # "<propertyValue>":
    #     ["<expression>"],
    
    "<SEMI>"      : [";"],
    "<COLON>"     : [":"],
    "<IMPORTANT>" : ["!important"],
}
properties_Grammar.update(IdentifierGrammar)
#properties_Grammar.update(expressionGrammar)

selectorGrammar = {
    "<start>": 
        ["<selectors>"],
    
    "<selectors>":
        ["<selector> <consecSelectors>"],

    "<consecSelectors>":
        ["", "<consecSelector><consecSelectors>"],

    "<consecSelector>":
        ["<COMMA> <selector>"], 

    "<selector>":
        ["<Identifier>", "<HASH><Identifier>", "<DOT><Identifier>"],
    
    "<COMMA>"      : [","],
    "<DOT>"        : ["."],
    "<HASH>"       : ["#"]
}
selectorGrammar.update(IdentifierGrammar)



measurementGrammar = {
    "<start>":
        ["<measurement>"],
    # measurement
    "<measurement>":
        ["<Number>", "<Number> <Unit>"],
    # unit
    "<Unit>":
        ["px"], # "cm", "mm", "in", "pt",
        # "pc", "em", "ex", "deg", "rad", "grad",
        # "ms", "s", "hz", "khz"],
}  # NumberGrammar
measurementGrammar.update(NumberGrammar)

measurementExpressionGrammar = {
    "<start>":
        ["<meaExpression>"],
    "<meaExpression>":
        ["<meaTerm> + <meaExpression>", "<meaTerm> - <meaExpression>", "<meaTerm>"],
    "<meaTerm>":
        ["<meaFactor> * <meaTerm>", "<meaFactor> / <meaTerm>", "<meaFactor> % <meaTerm>", "<meaFactor>"],
    "<meaFactor>":
        ["+<meaFactor>",
         "-<meaFactor>",
         "(<meaExpression>)",
         "<measurement>"]
}
measurementExpressionGrammar.update(measurementGrammar)
# useGrammar = measurementExpressionGrammar
# useGrammar["<start>"] = ["<meaExpression>"]

colorExpressionGrammar = {
    "<start>":
        ["<colorExpression>"], 
    "<colorExpression>":
        ["<colorExpTerm> + <colorExpression>", "<colorExpTerm> - <colorExpression>", "<colorExpTerm>"],
    "<colorExpTerm>":
        ["<colorExpFactor> * <colorExpTerm>", "<colorExpFactor> / <colorExpTerm>", 
         "<colorExpFactor> % <colorExpTerm>", "<colorExpFactor>"],
    "<colorExpFactor>":
        ["+<colorExpFactor>",
         "-<colorExpFactor>",
         "(<colorExpression>)",
         "<Color>"],
}
colorExpressionGrammar.update(colorGrammar)



expressionGrammar = {
    "<start>": 
        ["<expression>"],
    "<expression>":
        ["<measurement>", "<Color>",
         "<STRING>", "<NULL_>"],
    "<NULL_>":
        ["null"]

}
expressionGrammar.update(measurementGrammar)
expressionGrammar.update(colorGrammar)
expressionGrammar.update(stringGrammar)


mathStatementGrammar = {
    "<start>":
        ["<mathStatements>"],   
    "<mathStatements>":
        ["", "<mathStatement>"],
    "<mathStatement>":  # 改这里！！！！把不同类型的expr分开
        ["<meaExpression>", "<colorExpression>", "<STRING>", "<url>"], #, "<NULL_>"],

    # "<NULL_>":
    #     ["null"]
}
mathStatementGrammar.update(measurementExpressionGrammar)
mathStatementGrammar.update(colorExpressionGrammar)
mathStatementGrammar.update(urlGrammar)
mathStatementGrammar.update(stringGrammar)
# useGrammar = mathStatementGrammar
# useGrammar["<start>"] = ["<mathStatements>"]


commandStatementGrammar = {
    "<start>":
        ["<commandStatement>"],
    
    "<commandStatement>":
        ["<mathStatement> <mathStatements>", 
         "<LPAREN> <commandStatement> <RPAREN> <mathStatements>",
         "<MINUS_LPAREN> <commandStatement> <RPAREN> <mathStatements>",
         "<PLUS_LPAREN> <commandStatement> <RPAREN> <mathStatements>"],
    
    "<consecCommandStatements>":
        ["", "<consecCommandStatement><consecCommandStatements>"],

    "<consecCommandStatement>":
        ["<commandStatement>", ", <commandStatement>"],

    # null  
    "<LPAREN>": ["("],
    "<RPAREN>": [")"],
    "<PLUS>"  : ["+"],
    "<MINUS>" : ["-"],
    "<MINUS_LPAREN>"    : ["<MINUS> <LPAREN>"],
    "<PLUS_LPAREN>"     : ["<PLUS> <LPAREN>"]

}  # expressionGrammar
#commandStatementGrammar.update(expressionGrammar)
commandStatementGrammar.update(mathStatementGrammar)
# useGrammar = commandStatementGrammar
# useGrammar["<start>"] = ["<commandStatement>"]


propertyValueGrammar = {
    "<start>":
        ["<propertyValue>"],

    "<propertyValue>":
        ["<commandStatement> <consecCommandStatements>",
         "<commandStatement> <consecCommandStatements>"],
    
    "<consecCommandStatements>":
        ["", "<consecCommandStatement><consecCommandStatements>"],

    "<consecCommandStatement>":
        ["<commandStatement>", "<COMMA> <commandStatement>"],
    "<COMMA>":  [","],
}
propertyValueGrammar.update(commandStatementGrammar)


map_Grammar = {
    "<start>":
        ["<map_>"],
    "<map_>":
        ["<LPAREN> <mapEntry> <consecMapEntries> <RPAREN>",
         "<LPAREN> <mapEntry> <consecMapEntries> <COMMA> <RPAREN>"],
    "<consecMapEntries>":
        ["", "<consecMapEntry><consecMapEntries>"],
    "<consecMapEntry>":
        ["<COMMA> <mapEntry>"],
    "<mapEntry>":
        ["<mapKey> <COLON> <mapValue>"],
    "<mapKey>":
        ["<commandStatement>", "<list_>", "<map_>"],
    "<mapValue>":
        ["<commandStatement>", "<list_>", "<map_>"],
    "<COMMA>":  [","],
    "<COLON>":  [":"],
    
}
map_Grammar.update(commandStatementGrammar)


list_Grammar = {
    "<start>":
        ["<list_>"],
    "<list_>":
        ["<listCommaSeparated>", "<listSpaceSeparated>", "<listBracketed>"],

    "<listBracketed>":
        ["<LBRACK> <listCommaSeparated> <RBRACK>",
         "<LBRACK> <listSpaceSeparated> <RBRACK>"],

    "<listCommaSeparated>":
        ["<listElement><consecListElements>",
         "<listElement><consecListElements>,"],
    "<consecListElements>":
        ["<consecListElement>", "<consecListElement><consecListElements>"],
    "<consecListElement>":
        [", <listElement>"], 

    "<listSpaceSeparated>":
        ["<listElement> <listElements>"],
    "<listElements>":
        ["<listElement>", "<listElement> <listElements>"],    
    "<listElement>":
        ["<commandStatement>",
         "<LPAREN><list_><RPAREN>"],
    
    "<LBRACK>"          : ["["],
    "<RBRACK>"          : ["]"]
}
list_Grammar.update(commandStatementGrammar)



rulesetGrammar = {
    "<start>": 
        ["<ruleset>"],

    "<ruleset>":
        ["<selectors> <block>"],

    "<block>":
        ["<BlockStart> <properties_> <BlockEnd>",
         "<BlockStart> <properties_> <lastProperty> <BlockEnd>",
         "<BlockStart> <ruleset> <BlockEnd>",
         "<BlockStart> <ruleset> <lastProperty> <BlockEnd>"],
    
    # # string literals
    # "<StringLiteral>": ["<STRING>"],

    # null
    # "<NULL_>":
    #     ["null"],

    "<DOT>": ["."],
    "<COMMA>":  [","],
    "<HASH>":  ["#"],

    "<BlockStart>": ["{"],
    "<BlockEnd>"  : ["}"],
    "<SEMI>"      : [";"],
    "<COLON>"     : [":"],
    "<IMPORTANT>" : ["!important"],
}
rulesetGrammar.update(IdentifierGrammar)
rulesetGrammar.update(stringGrammar)
#rulesetGrammar.update(expressionGrammar)
rulesetGrammar.update(measurementGrammar)
rulesetGrammar.update(properties_Grammar)
rulesetGrammar.update(selectorGrammar)
rulesetGrammar.update(colorGrammar)
rulesetGrammar.update(NumberGrammar)


variableDeclarationGrammar = {
    "<variableDeclaration>":
        ["<variableName> <COLON> <propertyValue> <POUND_DEFAULT> <SEMI>",
         "<variableName> <COLON> <propertyValue> <SEMI>",
         "<variableName> <COLON> <listBracketed> <POUND_DEFAULT> <SEMI>",
         "<variableName> <COLON> <listBracketed> <SEMI>",
         "<variableName> <COLON> <map_> <POUND_DEFAULT> <SEMI>",
         "<variableName> <COLON> <map_> <SEMI>"],

    "<POUND_DEFAULT>"   : ["!default"],
    "<COLON>"     : [":"],
    "<SEMI>"      : [";"],
    
}
variableDeclarationGrammar.update(propertyValueGrammar)
variableDeclarationGrammar.update(map_Grammar)
variableDeclarationGrammar.update(list_Grammar)
variableDeclarationGrammar.update(variableNameGrammar)
# useGrammar = variableDeclarationGrammar
# useGrammar["<start>"] = ["<variableDeclaration>"]

forDeclarationGrammar = {
    "<start>": 
        ["<forDeclaration>"],

    "<forDeclaration>":
        ["@for $i from <fromNumber> to <throughNumber> <forBlock>",
         "@for $i from <fromNumber> through <throughNumber> <forBlock>"],

    "<forBlock>":
        ["{<properties_>}",
         "{<properties_> <lastProperty>}",
         "{width\: $i * 2em;}",
         "{width\: $i * 2em; <lastProperty>}"],
    "<fromNumber>":
        ["<Number>"],
    "<throughNumber>":
        ["<Number>"],

    # properties
    "<properties_>":
        ["", "<property_><properties_>"],
    "<property_>":
        ["<Identifier><COLON> <propertyValue> <SEMI>",
         "<Identifier><COLON> <propertyValue> <IMPORTANT> <SEMI>"],
    "<lastProperty>":
        ["<Identifier><COLON> <propertyValue>",
         "<Identifier><COLON> <propertyValue> <IMPORTANT>"],
    # "<propertyValue>":
    #     ["<expression>"],

    
    "<IMPORTANT>"       : ["!important"],
    "<SEMI>"            : [";"],
    "<COLON>"           : [":"],
}
forDeclarationGrammar.update(NumberGrammar)
forDeclarationGrammar.update(properties_Grammar)
forDeclarationGrammar.update(propertyValueGrammar)
forDeclarationGrammar.update(IdentifierGrammar)
# useGrammar = forDeclarationGrammar
# useGrammar["<start>"] = ["<forDeclaration>"]


conditionGrammar = {
    "<start>": 
        ["<conditions>"],

    "<conditions>":
        ["<condition>",
         "(<condition> <COMBINE_COMPARE> <condition>)",
         "<NULL_>"],

    "<condition>":
        ["<commandStatement>",
         "(<commandStatement> <EQEQ> <commandStatement>)",
         "(<commandStatement> <LT> <commandStatement>)",
         "(<commandStatement> <GT> <commandStatement>)",
         "(<commandStatement> <NOTEQ> <commandStatement>)",
         "<LPAREN> <conditions> <RPAREN>"],
    
    "<COMBINE_COMPARE>": 
        ["&&", "||"],
    "<EQEQ>"            : ["=="],
    "<NOTEQ>"           : ["!="],
    "<GT>"              : [">"],
    "<LT>"              : ["<"],
    "<NULL_>"           : ["null"]
}
conditionGrammar.update(commandStatementGrammar)

whileDeclarationGrammar = {
    "<start>": 
        ["<whileDeclaration>"],
    "<whileDeclaration>":
        ["@while <conditions> <whileBlock>"],
    "<whileBlock>":
        ["{<properties_>}",
         "{<properties_> <lastProperty>}",
         "{width\: 2em;}",
         "{width\: 2 * 2em; <lastProperty>}"],
}
whileDeclarationGrammar.update(conditionGrammar)
whileDeclarationGrammar.update(properties_Grammar)
# useGrammar = whileDeclarationGrammar
# useGrammar["<start>"] = ["<whileDeclaration>"]

grammar = {
    "<start>": 
        ["<scss>"],
    "<scss>":
        ["<statement>"],
    "<statement>":
        ["<ruleset>", "<variableDeclaration>", "<forDeclaration>", "<whileDeclaration>"]
}
grammar.update(rulesetGrammar)
grammar.update(commandStatementGrammar)
grammar.update(variableDeclarationGrammar)
grammar.update(forDeclarationGrammar)
grammar.update(whileDeclarationGrammar)
useGrammar = grammar
useGrammar["<start>"] = ["<scss>"]