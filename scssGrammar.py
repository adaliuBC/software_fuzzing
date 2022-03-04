SCSS_GRAMMAR = {  # : Grammar = {?
    # Parser
    
    "<start>": 
        ["<scss>"],

    "<scss>":
        ["<statements>"],
    
    "<statements>":
        ["", "<statement><statements>"],
    
    "<statement>":
        [#"<importDeclaration>",   
         "<mediaDeclaration>",
         "<ruleset>",             "<mixinDeclaration>", 
         #"<contentDeclaration>",  "<functionDeclaration>",
         "<functionDeclaration>",
         "<variableDeclaration>", #"<includeDeclaration>",
         "<ifDeclaration>",       "<forDeclaration>",
         "<whileDeclaration>",    "<eachDeclaration>"],

    # Params declared by rules such as @mixin and @function.
    "<declaredParams>":
        ["<declaredParam> <consecDeclaredParams> <Ellipsis>", 
         "<declaredParam> <consecDeclaredParams>"],

    "<consecDeclaredParams>":
        ["", "<consecDeclaredParam><consecDeclaredParams>"],

    "<consecDeclaredParam>":
        ["<COMMA> <declaredParam>"],
    
    "<declaredParam>":
        ["<variableName> <paramOptionalValue>",
         "<variableName>"],


    "<variableName>":
        ["<DOLLAR><Identifier>",
         "<MINUS_DOLLAR><Identifier>",
         "<PLUS_DOLLAR><Identifier>",
         "<namespaces><DOLLAR><Identifier>",
         "<namespaces><MINUS_DOLLAR><Identifier>",
         "<namespaces><PLUS_DOLLAR><Identifier>"],

    "<paramOptionalValue>":
        ["<COLON> <expressions>"],

    "<expressions>":
        ["<expression>", "<expression><expressions>"],

    # Params passed to rules such as @include and @content.
    "<passedParams>":
        ["<passedParam> <consecPassedParams>",
         "<passedParam> <consecPassedParams> <COMMA>",
         "<passedParam> <consecPassedParams>",
         "<passedParam> <consecPassedParams> <Ellipsis>"],

    "<consecPassedParams>":
        ["", "<consecPassedParam><consecPassedParams>"],

    "<consecPassedParam>":
        ["<COMMA> <passedParam>"],

    "<passedParam>":
        ["<params> <commandStatement>",
         "<params> <listSpaceSeparated>",
         "<params> <listBracketed>",
         "<params> <map_>"],
    
    "<params>":
        ["", "<param>"],

    "<param>":
        ["<variableName> <COLON>"],

    # MIXINS and related rules
    "<mixinDeclaration>":
        ["<MIXIN> <FunctionIdentifier> <RPAREN> <block>",
         "<MIXIN> <FunctionIdentifier> <declaredParams> <RPAREN> <block>",
         "<MIXIN> <Identifier> <block>",
         "<MIXIN> <Identifier> <LPAREN> <contentDeclaration> <RPAREN> <block>",
         "<MIXIN> <Identifier> <LPAREN> <declaredParams> <RPAREN> <block>"],
    # TODO: be careful about what you put here, and how we are parsing 正则表达式？

    "<contentDeclaration>":
        ["<CONTENT> <SEMI>",
         "<CONTENT> <LPAREN> <RPAREN> <SEMI>",
         "<CONTENT> <LPAREN> <passedParams> <RPAREN> <SEMI>"],
    
    # "<includeDeclaration>":
    #     ["<INCLUDE> <Identifier>",
    #         "<INCLUDE> <Identifier> <SEMI>",
    #         "<INCLUDE> <Identifier>",
    #         "<INCLUDE> <Identifier> <block>",
    #         "<INCLUDE> <Identifier> <USING> <LPAREN> <declaredParams> <RPAREN> <block>",
    #         "<INCLUDE> <functionCall>",
    #         "<INCLUDE> <functionCall> <SEMI>",
    #         "<INCLUDE> <functionCall>",
    #         "<INCLUDE> <functionCall> <block>",
    #         "<INCLUDE> <functionCall> <USING> <LPAREN> <declaredParams> <RPAREN> <block>"],
    # 

    # FUNCTIONS
    "<functionDeclaration>":
        ["<FUNCTION> <FunctionIdentifier> <RPAREN> <BlockStart> <BlockEnd>",
         "<FUNCTION> <FunctionIdentifier> <declaredParams> <RPAREN> <BlockStart> <BlockEnd>",
         "<FUNCTION> <FunctionIdentifier> <RPAREN> <BlockStart> <functionBody> <BlockEnd>",
         "<FUNCTION> <FunctionIdentifier> <declaredParams> <RPAREN> <BlockStart> <functionBody> <BlockEnd>",
         "<FUNCTION> <Identifier> <LPAREN> <RPAREN> <BlockStart> <BlockEnd>",
         "<FUNCTION> <Identifier> <LPAREN> <declaredParams> <RPAREN> <BlockStart> <BlockEnd>",
         "<FUNCTION> <Identifier> <LPAREN> <RPAREN> <BlockStart> <functionBody> <BlockEnd>",
         "<FUNCTION> <Identifier> <LPAREN> <declaredParams> <RPAREN> <BlockStart> <functionBody> <BlockEnd>"], 
    # TODO: 这里上面好像只有右括号没有左括号，查一下


    "<functionBody>":
        ["<functionStatements> <functionReturn>"],

    "<functionReturn>":
        ["<RETURN> <commandStatement> <SEMI>"],
    
    "<functionStatements>":
        ["", "<functionStatement><functionStatements>"],

    "<functionStatement>":
        ["<commandStatement> <SEMI>", "<statement>"],

    "<commandStatement>":
        ["<expression> <mathStatements>", 
         "<LPAREN> <commandStatement> <RPAREN> <mathStatements>",
         "<MINUS_LPAREN> <commandStatement> <RPAREN> <mathStatements>",
         "<PLUS_LPAREN> <commandStatement> <RPAREN> <mathStatements>"],

    "<mathStatements>":
        ["", "<mathStatement>"],

    # "<mathCharacter>":
    #     ["<TIMES>", "<PLUS>", "<DIV>", "<MINUS>", "<PERC>"],
    
    "<expression>":
        ["<measurement>", "<identifier>", "<Color>",
         "<StringLiteral>", "<NULL_>", "<url>", 
         "<variableName>", "<functionCall>"],

    "<mathStatement>":
        # ["<mathCharacter> <commandStatement>"],
        ["<expTerm> <PLUS> <expression>", "<expTerm> <MINUS> <expression>", "<expTerm>"],

    "<expTerm>":
        ["<expFactor> <TIMES> <expTerm>", "<expFactor> <DIV> <expTerm>", 
         "<expFactor> <PERC> <expTerm>", "<expFactor>"],

    "<expFactor>":
        ["<PLUS><expFactor>",
         "<MINUS><expFactor>",
         "(<expression>)",
         "<Number>"],

    # "<integer>":
    #     ["<digit><integer>", "<digit>"],


    # If statement
    "<ifDeclaration>":
        ["<AT_IF> <conditions> <block> <elseIfStatements>",
         "<AT_IF> <conditions> <block> <elseIfStatements> <elseStatement>"],

    "<elseIfStatements>":
        ["", "<elseIfStatement><elseIfStatements>"],

    "<elseIfStatement>":
        ["<AT_ELSE> <IF> <conditions> <block>"],

    "<elseStatement>":
        ["<AT_ELSE> <block>"],

    "<conditions>":
        ["<condition>",
         "<condition> <COMBINE_COMPARE> <conditions>",
         "<NULL_>"],

    "<condition>":
        ["<commandStatement>",
         "<commandStatement> <EQEQ> <conditions>",
         "<commandStatement> <LT> <conditions>",
         "<commandStatement> <GT> <conditions>",
         "<commandStatement> <NOTEQ> <conditions>",
         "<LPAREN> <conditions> <RPAREN>"],
    # TODO: here should I change "==" to <EQ>, "!=" to <NE>? or can I use the '' to mark them as string?

    "<variableDeclaration>":
        ["<variableName> <COLON> <propertyValue> <POUND_DEFAULT> <SEMI>",
         "<variableName> <COLON> <propertyValue> <SEMI>",
         "<variableName> <COLON> <listBracketed> <POUND_DEFAULT> <SEMI>",
         "<variableName> <COLON> <listBracketed> <SEMI>",
         "<variableName> <COLON> <map_> <POUND_DEFAULT> <SEMI>",
         "<variableName> <COLON> <map_> <SEMI>"],


    # for
    "<forDeclaration>":
        ["<AT_FOR> <variableName> <FROM> <fromNumber> <TO> <throughNumber> <block>",
         "<AT_FOR> <variableName> <FROM> <fromNumber> <THROUGH> <throughNumber> <block>"],

    "<fromNumber>":
        ["<Number>"],
    
    "<throughNumber>":
        ["<Number>", "<functionCall>"],

    
    # while
    "<whileDeclaration>":
        ["<AT_WHILE> <conditions> <block>"],

    
    # EACH
    "<eachDeclaration>":
        ["<AT_EACH> <variableName> <consecVariableNames> <IN> <eachValueList> <block>"],
    
    "<consecVariableNames>":
        ["", "<consecVariableName><consecVariableNames>"],

    "<consecVariableName>":
        ["<COMMA> <variableName>"],

    "<eachValueList>":
        ["<commandStatement>", "<list_>", "<map_>"],
        

    # Imports
    # "<importDeclaration>":
    #     ["<IMPORT> <referenceUrl> <SEMI>",
    #      "<USE> <referenceUrl> <SEMI>",
    #      "<USE> <referenceUrl> <asClause> <SEMI>",
    #      "<USE> <referenceUrl> <withClause> <SEMI>",
    #      "<USE> <referenceUrl> <asClause> <withClause> <SEMI>"],

    # "<referenceUrl>":
    #     ["<StringLiteral>", "<UrlStart> <Url> <UrlEnd>"],

    # "<asClause>":
    #     ["<AS> <TIMES>", "<AS> <identifier>"],

    # "<withClause>":
    #     ["<WITH> <LPAREN> <keywordArgument> <consecKeywordArguments> <RPAREN>",
    #      "<WITH> <LPAREN> <keywordArgument> <consecKeywordArguments> <COMMA> <RPAREN>"],
        
    # "<consecKeywordArguments>":
    #     ["", "<consecKeywordArgument><consecKeywordArguments>"],

    # "<consecKeywordArgument>":
    #     ["<COMMA> <keywordArgument>"],
        
    # "<keywordArgument>":
    #     ["<identifierVariableName> : <expression>"],
    

    # MEDIA
    "<mediaDeclaration>":
        ["<MEDIA> <mediaQueryList> <block>"],

    "<mediaQueryList>":
        ["", "<mediaQuery> <consecMediaQueries>"],

    "<consecMediaQueries>":
        ["", "<consecMediaQuery><consecMediaQueries>"],

    "<consecMediaQuery>":
        ["<COMMA> <mediaQuery>"],


    "<mediaQuery>":
        ["<mediaType> <consecMediaExpressions>",
         "<ONLY> <mediaType> <consecMediaExpressions>",
         "<NOT> <mediaType> <consecMediaExpressions>",
         "<mediaExpression> <consecMediaExpressions>"],

    "<consecMediaExpressions>":
        ["", "<consecMediaExpression><consecMediaExpressions>"],

    "<consecMediaExpression>":
        ["<AND_WORD> <mediaExpression>"],

    # Typically only 'all', 'print', 'screen', and 'speech', but there are some
    # deprecated values too.
    "<mediaType>":
        ["<Identifier>"],

    "<mediaExpression>":
        ["( <mediaFeature> )",
         "( <mediaFeature> : <commandStatement> )"],

    # Typically 'max-width', 'hover', 'orientation', etc. Many possible values.
    "<mediaFeature>":
        ["<Identifier>"],


    # Rules
    "<ruleset>":
        ["<selectors> <block>"],

    "<block>":
        ["<BlockStart> <properties_> <BlockEnd>",
         "<BlockStart> <properties_> <lastProperty> <BlockEnd>",
         "<BlockStart> <statements> <BlockEnd>",
         "<BlockStart> <statements> <lastProperty> <BlockEnd>"],
    
    "<properties_>":
        ["", "<property_><properties_>"],

    "<selectors>":
        ["<selector> <consecSelectors>"],

    "<consecSelectors>":
        ["", "<consecSelector><consecSelectors>"],

    "<consecSelector>":
        ["<COMMA> <selector>"], 

    "<selector>":
        ["<elements>"],

    "<elements>":
        ["<element>", "<element><elements>"],

    "<element>":
        ["<identifier>", "<HASH><identifier>", "<DOT><identifier>", 
         "<AND>", "<TIMES>", "<combinator>", "<attrib>", "<pseudo>"],

    "<combinator>":
        ["<GT>", "<PLUS>", "<TIL>"],

    "<pseudo>":
        ["<pseudoIdentifier>",
         "<pseudoIdentifier> <LPAREN> <selector> <RPAREN>", 
         "<pseudoIdentifier> <LPAREN> <commandStatement> <RPAREN>"],

    "<attrib>":
        ["<LBRACK> <Identifier> <RBRACK>", 
         "<LBRACK> <Identifier> <attribRelate> <StringLiteral> <RBRACK>",
         "<LBRACK> <Identifier> <attribRelate> <Identifier> <RBRACK>"],

    "<attribRelate>":
        ["<EQ>", "<PIPE_EQ>", "<TILD_EQ>"],

    "<identifier>":
        ["<Identifier><identifierParts>",
         "<InterpolationStart> <identifierVariableName> <BlockEnd> <identifierParts>"],
         # These are keywords in some contexts, but can be used as identifiers too.
         #"<AND_WORD>", "<FROM>", "<NOT>", "<ONLY>", 
         #"<THROUGH>", "<TO>", "<USING>"],
        # TODO: see later!
    "<pseudoIdentifier>":
        ["<PseudoIdentifier> <identifierParts>"],

    "<identifierParts>":
        ["", "<identifierPart><identifierParts>"],

    "<identifierPart>":
        ["<InterpolationStartAfter> <identifierVariableName> <BlockEnd>",
         "<IdentifierAfter>"],
         
    "<identifierVariableName>":
        ["<DOLLAR><Identifier>",
         "<DOLLAR><IdentifierAfter>"],

    "<property_>":
        ["<identifier><COLON> <propertyValue> <SEMI>",
         "<identifier><COLON> <propertyValue> <IMPORTANT> <SEMI>"],
         #"<identifier><COLON> <block>",
         #"<identifier><COLON> <propertyValue> <block>",
         #"<identifier><COLON> <propertyValue> <IMPORTANT> <block>"],
        # TODO: see later!
        
    "<lastProperty>":
        ["<identifier><COLON> <propertyValue>",
         "<identifier><COLON> <propertyValue> <IMPORTANT>"],

    "<propertyValue>":
        ["<commandStatement> <consecCommandStatements>",
         "<commandStatement> <consecCommandStatements>"],
    
    "<consecCommandStatements>":
        ["", "<consecCommandStatement><consecCommandStatements>"],

    "<consecCommandStatement>":
        ["<commandStatement>", "<COMMA> <commandStatement>"],

    "<url>":
        ["<LPAREN> <Url> <RPAREN>"],

    "<measurement>":
        ["<Number>", "<Number> <Unit>"],


    "<functionCall>":
        [" <FunctionIdentifier> <RPAREN>",
         "<namespaces> <FunctionIdentifier> <RPAREN>",
         "<FunctionIdentifier> <passedParams> <RPAREN>",
         "<namespaces> <FunctionIdentifier> <passedParams> <RPAREN>"],
    # TODO：这个也是，左括号呢？

    "<namespaces>":
        ["<namespace>", "<namespace><namespaces>"],
    
    "<namespace>":
        ["<Identifier><DOT>"],

    "<list_>":
        ["<listCommaSeparated>", "<listSpaceSeparated>", "<listBracketed>"],

    "<listCommaSeparated>":
        ["<listElement> <consecListElements>",
         "<listElement> <consecListElements> <COMMA>"],
    
    "<consecListElements>":
        ["<consecListElement>", "<consecListElement><consecListElements>"],

    "<consecListElement>":
        ["<COMMA> <listElement>"], 

    "<listSpaceSeparated>":
        ["<listElement> <listElements>"],

    "<listElements>":
        ["<listElement>", "<listElement><listElements>"],

    "<listBracketed>":
        ["<LBRACK> <listCommaSeparated> <RBRACK>",
         "<LBRACK> <listSpaceSeparated> <RBRACK>"],

    "<listElement>":
        ["<commandStatement>",
         "<LPAREN> <list_> <RPAREN>"],

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


    
    # Lexer
    "<NULL_>":
        ["null"],

    "<IN>":
        ["in"],

    "<Unit>":
        ["%", "px", "cm", "mm", "in", "pt",
         "pc", "em", "ex", "deg", "rad", "grad",
         "ms", "s", "hz", "khz"],

    "<COMBINE_COMPARE>": 
        ["&&", "||"],

    "<Ellipsis>":
        ["..."],

    # TODO ?????
    "<InterpolationStart>":
        ["<HASH> <BlockStart>"], # -> pushMode(IDENTIFY)

    #Separators
    "<LPAREN>"          : ["("],
    "<RPAREN>"          : [")"],
    "<BlockStart>"      : ["{"],
    "<BlockEnd>"        : ["}"],
    "<LBRACK>"          : ["["],
    "<RBRACK>"          : ["]"],
    "<GT>"              : [">"],
    "<TIL>"             : ["~"],

    "<LT>"              : ["<"],
    "<COLON>"           : [":"],
    "<SEMI>"            : [";"],
    "<COMMA>"           : [","],
    "<DOT>"             : ["."],
    "<DOLLAR>"          : ["$"],
    #"<AT>"              : ["@"],
    "<AND>"             : ["&"],
    "<HASH>"            : ["#"],
    "<PLUS>"            : ["+"],
    "<TIMES>"           : ["*"],
    "<DIV>"             : ["/"],
    "<MINUS>"           : ["-"],
    "<PERC>"            : ["%"],

    # When a variable or parenthesized statement is negated, there cannot be a
    # space after the - or +.
    # ?????
    "<MINUS_DOLLAR>"    : ["<MINUS> <DOLLAR>"],
    "<PLUS_DOLLAR>"     : ["<PLUS> <DOLLAR>"],
    "<MINUS_LPAREN>"    : ["<MINUS> <LPAREN>"],
    "<PLUS_LPAREN>"     : ["<PLUS> <LPAREN>"],


    #"<UrlStart>":
    #    ["<url> <LPAREN>"],  #-> pushMode(URL_STARTED)

    "<EQEQ>"            : ["=="],
    "<NOTEQ>"           : ["!="],

    "<EQ>"              : ["="],
    "<PIPE_EQ>"         : ["|="],
    "<TILD_EQ>"         : ["~="],

    "<MIXIN>"           : ["@mixin"],
    "<FUNCTION>"        : ["@function"],
    "<AT_ELSE>"         : ["@else"],
    "<IF>"              : ["if"],
    "<AT_IF>"           : ["@if"],
    "<AT_FOR>"          : ["@for"],
    "<AT_WHILE>"        : ["@while"],
    "<AT_EACH>"         : ["@each"],
    #"<INCLUDE>"         : ["@include"],
    # "<IMPORT>"          : ["@import"],
    # "<USE>"             : ["@use"],
    "<RETURN>"          : ["@return"],
    "<MEDIA>"           : ["@media"],
    "<CONTENT>"         : ["@content"],

    "<FROM>"            : ["from"],
    "<TO>"              : ["to"],
    "<THROUGH>"         : ["through"],
    "<POUND_DEFAULT>"   : ["!default"],
    "<IMPORTANT>"       : ["!important"],
    "<ONLY>"            : ["only"],
    "<NOT>"             : ["not"],
    "<AND_WORD>"        : ["and"],
    #"<USING>"           : ["using"],
    # "<AS>"              : ["as"],
    # "<WITH>"            : ["with"],


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

    
    "<PseudoIdentifier>":
        ["<COLON> <COLON> <Identifier>", "<COLON> <Identifier>"],  ##??? -> pushMode(IDENTIFY)

    
    "<FunctionIdentifier>": 
        ["<Identifier> <LPAREN>"],


    # string
    "<STRING>":
        ["\"<string>\""],
    
    "<string>":
        ["<char>", "<char><string>"],
    
    "<char>":
        [chr(32), chr(33)] + [chr(order) for order in range(35, 92)] + [chr(order) for order in range(93, 127)],
    # no ", no \
    # TODO: check this string

    # string literals
    "<StringLiteral>": ["<STRING>"],

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
    
    
    #??? color -> '#' ('0'..'9'|'a'..'f'|'A'..'F')+ 这个+是怎么回事？
    


    # Whitespace -- ignored
    #"<WS>":
    #    ["<wsChar>", "<wsChar><WS>"],

    #"<wsChar>":
    #    [" ", "\t", "\n", "\r", "\r\n"],

    # TODO: single-line comments
    #SL_COMMENT: '//'(~('\n'|'\r'))* ('\n'|'\r'('\n')?) -> skip;

    # TODO:multiple-line comments
    #COMMENT: '/*' .*? '*/' -> skip;
    
    "<InterpolationStartAfter>"  : ["<InterpolationStart>"],
    #"<InterpolationEnd_ID>"    : ["<BlockEnd>"],  # -> type(BlockEnd);
    "<IdentifierAfter>"        : ["<Identifier>"],

    #"<UrlEnd>"                 : ["<RPAREN>"], #-> popMode;
    # "<Url>"                    : ["<STRING>",  "<urlChars>"],  # loop here!!!
    
    # "<urlChars>"               : ["<urlChar>", "<urlChar><urlChars>"],
    # "<urlChar>"                : 
    #     [chr(order) for order in range(32, 41)] 
    #     + [chr(order) for order in range(42, 59)]
    #     + [chr(order) for order in range(60, 92)]
    #     + [chr(order) for order in range(93, 127)],
    # # no 41, no 59, no 92
    # #(~(')' | '\n' | '\r' | ';'))+;

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
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
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
        ["<id>=<id>", "<id>=<nat>"]


}

'''
    #"<BlockStart_ID>"          : ["<BlockStart>"], #-> popMode, type(BlockStart);
    #"<SPACE>"                  : ["<WS>"], #-> popMode, skip;
    #"<DOLLAR_ID>"              : ["<DOLLAR>"], # -> type(DOLLAR);

    "<InterpolationStartAfter>"  : ["<InterpolationStart>"],
    #"<InterpolationEnd_ID>"    : ["<BlockEnd>"],  # -> type(BlockEnd);
    "<IdentifierAfter>"        : ["<Identifier>"],

    # All tokens that can signal the end of identifiers
    #"<Ellipsis_ID>"               : ["<Ellipsis>"],   #-> popMode, type(Ellipsis);
    #"<DOT_ID>"                    : ["<DOT>"],        #-> popMode, type(DOT);
    #"<LBRACK_ID>"                 : ["<LBRACK>"],     #-> popMode, type(LBRACK);
    #"<RBRACK_ID>"                 : ["<RBRACK>"],     #-> popMode, type(RBRACK);
    #"<LPAREN_ID>"                 : ["<LPAREN>"],     #-> popMode, type(LPAREN);
    #"<RPAREN_ID>"                 : ["<RPAREN>"],     #-> popMode, type(RPAREN);
    #"<COLON_ID>"                  : ["<COLON>"],      #-> popMode, type(COLON);
    #"<COMMA_ID>"                  : ["<COMMA>"],      #-> popMode, type(COMMA);
    #"<SEMI_ID>"                   : ["<SEMI>"],       #-> popMode, type(SEMI);
    #"<EQ_ID>"                     : ["<EQ>"],         #-> popMode, type(EQ);
    #"<PIPE_EQ_ID>"                : ["<PIPE_EQ>"],    #-> popMode, type(PIPE_EQ);
    #"<TILD_EQ_ID>"                : ["<TILD_EQ>"],    #-> popMode, type(TILD_EQ);
    #"<PseudoIdentifier_ID>"       : ["<PseudoIdentifier>"],   #-> popMode, type(PseudoIdentifier);
'''
'''
fragment STRING
    : '"' (~('"'|'\n'|'\r'))* '"'
    | '\'' (~('\''|'\n'|'\r'))* '\''
    ;
'''

'''
mode URL_STARTED;
UrlEnd                 : RPAREN -> popMode;
Url                    :  STRING | (~(')' | '\n' | '\r' | ';'))+;

mode IDENTIFY;
BlockStart_ID          : BlockStart -> popMode, type(BlockStart);
SPACE                  : WS -> popMode, skip;
DOLLAR_ID              : DOLLAR -> type(DOLLAR);
'''
