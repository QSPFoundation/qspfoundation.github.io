Prism.languages.qsp = {
	'comment': {
		pattern: /((^\s*?)|(\&\s*?))(!.*$)/m,
		lookbehind: false, // поиск обратно
		greedy: true // жадный
	},
	// 'string-interpolation': {
	// 	pattern: /(?:f|fr|rf)(?:("""|''')[\s\S]*?\1|("|')(?:\\.|(?!\2)[^\\\r\n])*\2)/i,
	// 	greedy: true,
	// 	inside: {
	// 		'interpolation': {
	// 			// "{" <expression> <optional "!s", "!r", or "!a"> <optional ":" format specifier> "}"
	// 			pattern: /((?:^|[^{])(?:\{\{)*)\{(?!\{)(?:[^{}]|\{(?!\{)(?:[^{}]|\{(?!\{)(?:[^{}])+\})+\})+\}/,
	// 			lookbehind: true,
	// 			inside: {
	// 				'format-spec': {
	// 					pattern: /(:)[^:(){}]+(?=\}$)/,
	// 					lookbehind: true
	// 				},
	// 				'conversion-option': {
	// 					pattern: /![sra](?=[:}]$)/,
	// 					alias: 'punctuation'
	// 				},
	// 				rest: null
	// 			}
	// 		},
	// 		'string': /[\s\S]+/
	// 	}
	// },
	// 'triple-quoted-string': {
	// 	pattern: /(?:[rub]|br|rb)?("""|''')[\s\S]*?\1/i,
	// 	greedy: true,
	// 	alias: 'string'
	// },
	'string': {
		pattern: /("|')(?:\\.|(?!\1)[^\\\r\n])*\1/i,
		greedy: true
	},
	// 'function': {
	// 	pattern: /((?:^|\s)def[ \t]+)[a-zA-Z_]\w*(?=\s*\()/g,
	// 	lookbehind: true
	// },
	// 'class-name': {
	// 	pattern: /(\bclass\s+)\w+/i,
	// 	lookbehind: true
	// },
	// 'decorator': {
	// 	pattern: /(^[\t ]*)@\w+(?:\.\w+)*/m,
	// 	lookbehind: true,
	// 	alias: ['annotation', 'punctuation'],
	// 	inside: {
	// 		'punctuation': /\./
	// 	}
	// },
	'builtin': /\b(?:\$(desc|user_text|usrtxt|maintxt|stattxt|curloc|selobj|selact|mid|(u|l)case|trim|replace|str|strfind|input|qspver|curacts|getobj))\b/i,
	'boolean': /\b(?:False|None|True)\b/,
	'number': /\d+/,
	'operator': /[<>\+\-\*\/]=|<>|\+|-|<|>|=|\/|\*|!|and|or|mod/i,
	'keyword': /(?:(\*(pl?|nl|clr|clear))|(pl?|nl|clr|clear))\b|\b(?:inclib|freelib|addqst|killqst|openqst|opengame|savegame|addobj|delobj|killobj|unsel|unselect|cls|cla|delact|cmdclr|cmdclear|play|close|all|jump|dynamic|goto|gt|xgoto|xgt|gosub|gs|menu|exit|showobjs|showstat|showacts|showinput|refint|copyarr|killvar|killall|view|msg|settimer|wait|exec)\b/i,
	'punctuation': /[{}[\];(),:]/,
	'variable': /[\$\%][\wа-я]+|[\wа-я]+/i,
};

// Prism.languages.qsp['string-interpolation'].inside['interpolation'].inside.rest = Prism.languages.qsp;

// Prism.languages.py = Prism.languages.qsp