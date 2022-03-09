htmlGrammar = {
    "<start>":
        ["<htmlDocument>"],

    "<htmlDocument>":
        ["<doctype><scriptletOrSeaWses><scriptletOrSeaWses><scriptletOrSeaWses><htmlElementses>",
         "<doctype><scriptletOrSeaWses><XML><scriptletOrSeaWses><scriptletOrSeaWses><htmlElementses>",
         "<doctype><scriptletOrSeaWses><scriptletOrSeaWses><DTD><scriptletOrSeaWses><htmlElementses>",
         "<doctype><scriptletOrSeaWses><XML><scriptletOrSeaWses><DTD><scriptletOrSeaWses><htmlElementses>"],        
    
    "<doctype>":
        ["<LGUI>!DOCTYPE html<RGUI> "],

    "<scriptletOrSeaWses>":
        ["", "<scriptletOrSeaWs><scriptletOrSeaWses>"],

    "<htmlElementses>":
        ["", "<htmlElements><htmlElementses>"],

    "<scriptletOrSeaWs>":
        ["<SCRIPTLET>", "<SEA_WS>"],

    "<htmlElements>":
        ["<htmlMiscs><htmlElement><htmlMiscs>"],
    
    "<htmlMiscs>":
        ["", "<htmlMisc><htmlMiscs>"],

    "<htmlElement>":
        ["<LGUI><TAG_NAME><htmlAttributes><TAG_SLASH_CLOSE>",
         "<LGUI><TAG_NAME><htmlAttributes><RGUI>",
         "<LGUI><TAG_NAME><htmlAttributes><RGUI><htmlContent><LGUI><TAG_SLASH><TAG_NAME><RGUI>",
         "<SCRIPTLET>", "<script>", "<style>"],

    "<htmlAttributes>":
        ["", "<htmlAttribute><htmlAttributes>"],

    "<htmlContent>":
        ["<htmlChardata><consecHtmlChardatas>", "<consecHtmlChardatas>"],
    
    "<consecHtmlChardatas>":
        ["", "<consecHtmlChardata><consecHtmlChardatas>"],
    
    "<consecHtmlChardata>":
        ["<htmlElement><htmlChardata>", "<htmlElement>",
         "<CDATA><htmlChardata>", "<CDATA>",
         "<htmlComment><htmlChardata>", "<htmlComment>"],

    "<htmlAttribute>":
        ["<TAG_NAME>", "<TAG_NAME><TAG_EQUALS><ATTVALUE_VALUE>"],

    "<htmlChardata>":
        ["<HTML_TEXT>", "<SEA_WS>"],

    "<htmlMisc>":
        ["<htmlComment>", "<SEA_WS>"],

    "<htmlComment>":
        ["<HTML_COMMENT>", "<HTML_CONDITIONAL_COMMENT>"],

    "<script>":
        ["<SCRIPT_OPEN><SCRIPT_BODY>", "<SCRIPT_OPEN><SCRIPT_SHORT_BODY>"],

    "<style>":
        ["<STYLE_OPEN><STYLE_BODY>", "<STYLE_OPEN><STYLE_SHORT_BODY>"],

    "<HTML_COMMENT>": ["<LGUI>!-- <STRING> --<RGUI>"],
    "<HTML_CONDITIONAL_COMMENT>":  ["<LGUI>![ <STRING> ]<RGUI>"],
    "<XML>":    ["<LGUI>?xml <STRING><RGUI>"],
    "<CDATA>":  ["<LGUI>![CDATA[ <STRING> ]]<RGUI>"],
    "<DTD>":    ["<LGUI>! <STRING> <RGUI>"],

    "<SCRIPTLET>":
        ["<LGUI>? <STRING> ?<RGUI>", "<LGUI>% <STRING> %<RGUI>"],

    "<SEA_WS>":
        ["<sea_ws>", "<sea_ws><SEA_WS>"],
        
    "<sea_ws>":
        [" ", "\t", "\n", "\r\n"],

    "<SCRIPT_OPEN>":
        ["<LGUI>script <STRING><RGUI>"],

    "<STYLE_OPEN>":
        ["<LGUI>style <STRING><RGUI>"],

    "<HTML_TEXT>":
        ["<textChar>", "<textChar><HTML_TEXT>"],

    "<textChar>":
        [chr(order) for order in range(32, 60)] + [chr(order) for order in range(61, 127)],


    # tag declarations

    "<TAG_SLASH_CLOSE>": ["/>"],

    "<TAG_SLASH>":  ["/"],


    # lexing mode for attribute values

    "<TAG_EQUALS>": ["="],

    "<TAG_NAME>":
        ["<TAG_NameStartChar><TAG_NameChars>", "a"],
    "<TAG_NameChars>":
        ["", "<TAG_NameChar><TAG_NameChars>"],
    # "<TAG_WHITESPACE>":
    #     ["\t", "\r", "\n"],

    "<TAG_NameChar>":
        ["<TAG_NameStartChar>", '-', '_', '.', "<digit>"]
         + [chr(ord('\u00B7'))]
         + [chr(order) for order in range(ord('\u0300'), ord('\u036F'))]
         + [chr(order) for order in range(ord('\u203F'), ord('\u2040'))],

    "<TAG_NameStartChar>":
        [chr(order) for order in range(ord('A'), ord('Z')+1)] 
        + [chr(order) for order in range(ord('a'), ord('z')+1)]
        + [chr(order) for order in range(ord('\u2070'), ord('\u218F'))]
        + [chr(order) for order in range(ord('\u2C00'), ord('\u2FEF'))]
        + [chr(order) for order in range(ord('\u3001'), ord('\uD7FF'))]
        + [chr(order) for order in range(ord('\uF900'), ord('\uFDCF'))]
        + [chr(order) for order in range(ord('\uFDF0'), ord('\uFFFD'))],

    # <scripts>
    "<SCRIPT_BODY>":
        ["<STRING> <LGUI>/script<RGUI>"],

    "<SCRIPT_SHORT_BODY>":
        ["<STRING> <LGUI>/<RGUI>"],

    "<STYLE_BODY>":
        ["<STRING> <LGUI>/style<RGUI>"],

    "<STYLE_SHORT_BODY>":
        ["<STRING> <LGUI>/<RGUI>"],

    "<STRING>":
        ["\"<string>\""],
    
    "<string>":
        ["<char>", "<char><string>"],
    
    "<char>":
        [chr(32), chr(33)] + [chr(order) for order in range(35, 92)] + [chr(order) for order in range(93, 127)],


    # an attribute value may have spaces b/t the '=' and the value
    "<ATTVALUE_VALUE>":
        ["<spaces><ATTRIBUTE>"],
        
    "<spaces>":
        ["", "<space><spaces>"],
    
    "<space>":
        [" "],

    "<ATTRIBUTE>":
        ["<DOUBLE_QUOTE_STRING>", "<SINGLE_QUOTE_STRING>", 
         "<ATTCHARS>", "<HEXCHARS>", "<DECCHARS>"],

    "<ATTCHARS>":
        ["<ATTCHAR>", "<ATTCHAR> ", "<ATTCHAR><ATTCHARS>"],

    "<ATTCHAR>":
        ["-", "_", ".", "/", "+", ",", "?", '=', ':', ';', '#', "<attchar>"],
    
    "<attchar>":
        [str(i) for i in range(0, 10)] + [chr(order) for order in range(ord('A'), ord('Z')+1)] + [chr(order) for order in range(ord('a'), ord('z')+1)],

    "<HEXCHARS>":
        ["#<hexChars>"],
    "<hexChars>":
        ["<hexChar>", "<hexChar><hexChars>"],
    "<hexChar>":
        ["<lowercaseHexChar>", "<uppercaseHexChar>", "<digit>"],
    "<uppercaseHexChar>":
        [chr(order) for order in range(ord('A'), ord('F')+1)],
    "<lowercaseHexChar>":
        [chr(order) for order in range(ord('a'), ord('f')+1)],  


    "<DECCHARS>":
        ["<digits>", "<digits>%"],   
    "<digits>":  # digits string，不管有无前导零
        ["<digit>", "<digit><digits>"], 
    "<digit>":
        [str(i) for i in range(0, 10)],

    "<SINGLE_QUOTE_STRING>":
        ["\'<singleString>\'"],
    "<singleString>":
        ["<singleChar>", "<singleChar><singleString>"],
    "<singleChar>":
        [chr(order) for order in range(32, 39)] + [chr(order) for order in range(40, 127)],
    "<DOUBLE_QUOTE_STRING>":
        ["\"<doubleString>\""],
    "<doubleString>":
        ["<doubleChar>", "<doubleChar><doubleString>"],
    "<doubleChar>":
        [chr(order) for order in range(32, 34)] + [chr(order) for order in range(35, 127)],

    "<LGUI>": ["<"],
    "<RGUI>": [">"],

}