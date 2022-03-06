

Identifier_Grammar = {
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

String_Grammar = {
    # string
    "<STRING>":
        ["\"<string>\""],
    
    "<string>":
        ["<char>", "<char><string>"],
    
    "<char>":
        [chr(32), chr(33)] + [chr(order) for order in range(35, 92)] + [chr(order) for order in range(93, 127)],

}

VARNAME_GRAMMAR = {
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
#VARNAME_GRAMMAR.update(Identifier_Grammar)

RULESET_GRAMMAR = {
    "<start>": 
        ["<ruleset>"],

    "<ruleset>":
        ["<selectors> <block>"],

    "<block>":
        ["<BlockStart> <properties_> <BlockEnd>",
         "<BlockStart> <properties_> <lastProperty> <BlockEnd>",
         "<BlockStart> <ruleset> <BlockEnd>",
         "<BlockStart> <ruleset> <lastProperty> <BlockEnd>"],
    
    # selectors
    "<selectors>":
        ["<selector> <consecSelectors>"],

    "<consecSelectors>":
        ["", "<consecSelector><consecSelectors>"],

    "<consecSelector>":
        ["<COMMA> <selector>"], 

    "<selector>":
        ["<Identifier>", "<HASH><Identifier>", "<DOT><Identifier>"],

    # properties
    "<properties_>":
        ["", "<property_><properties_>"],
    
    "<property_>":
        ["<Identifier><COLON> <propertyValue> <SEMI>",
         "<Identifier><COLON> <propertyValue> <IMPORTANT> <SEMI>"],

    "<lastProperty>":
        ["<Identifier><COLON> <propertyValue>",
         "<Identifier><COLON> <propertyValue> <IMPORTANT>"],

    "<propertyValue>":
        ["<expression>"],

    # expression
    "<expression>":
        ["<measurement>", "<Color>",
         "<StringLiteral>", "<NULL_>"],

    # measurement
    "<measurement>":
        ["<Number>", "<Number> <Unit>"],

    # unit
    "<Unit>":
        ["px", "cm", "mm", "in", "pt",
         "pc", "em", "ex", "deg", "rad", "grad",
         "ms", "s", "hz", "khz"],
    
    # string literals
    "<StringLiteral>": ["<STRING>"],

    # null
    "<NULL_>":
        ["null"],

    # number
    "<Number>":
        ["<integer>", "-<integer>", "<integer>.<digits>", "-<integer>.<digits>"],


    "<integer>": # number语法，不允许前导零
        ["<leadingdigit><digits>"],
    
    "<leadingdigit>":
        [str(i) for i in range(1, 10)],

    "<digits>":  # digits string，不管有无前导零
        ["<digit>", "<digit><digits>"],

    # COLOR:
    "<Color>":
        ["#<digit><hexChar><hexChar>"],

    "<hexChar>":
        ["<lowercaseHexChar>", "<uppercaseHexChar>"],
    
    
    "<uppercaseHexChar>":
        [chr(order) for order in range(ord('A'), ord('F')+1)],

    "<lowercaseHexChar>":
        [chr(order) for order in range(ord('a'), ord('f')+1)],   

    "<DOT>": ["."],
    "<COMMA>":  [","],
    "<HASH>":  ["#"],

    "<BlockStart>": ["{"],
    "<BlockEnd>"  : ["}"],
    "<SEMI>"      : [";"],
    "<COLON>"     : [":"],
    "<IMPORTANT>" : ["!important"],

}

# RULESET_GRAMMAR.update(Identifier_Grammar)
# RULESET_GRAMMAR.update(String_Grammar)
USE_GRAMMAR = RULESET_GRAMMAR
USE_GRAMMAR.update(Identifier_Grammar)
USE_GRAMMAR.update(String_Grammar)

VARIABLE_DECLARE_GRAMMAR = {

    
}