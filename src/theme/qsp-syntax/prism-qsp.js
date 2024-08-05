
let kw_operators = '\\b(inclib|freelib|addqst|killqst|openqst|opengame|savegame|addobj|delobj|killobj|unsel|unselect|cls|cla|delact|cmdclr|cmdclear|play|close|all|jump|dynamic|goto|gt|xgoto|xgt|gosub|gs|menu|exit|showobjs|showstat|showacts|showinput|refint|copyarr|killvar|killall|view|msg|settimer|wait|exec)\\b'
let kw_controls = '\\b(act|if|elseif|else|loop|while|step|end)\\b'
let kw_text_operators = '\\*?\\b(pl?|nl|clr|clear)\\b'

let functions_string = '\\$(desc|user_text|usrtxt|maintxt|stattxt|curloc|selobj|selact|mid|(u|l)case|trim|replace|str|strfind|input|qspver|curacts|getobj|iif|dyneval|func|max|min|arritem)\\b'
let functions_num = '\\b(loc|obj|isnum|isplay|len|val|instr|strcomp|strpos|arrsize|arrpos|arrcomp|msecscount|rgb|countobj|ra?nd|iif|dyneval|func|max|min|arritem)\\b'

let system_vars_string = '\\$(counter|ongload|ongsave|onnewloc|onactsel|onobjsel|onobjadd|onobjdel|usercom|fname|backimage|args|result)\\b'
let system_vars_num = '\\b(nosave|disablescroll|disablesubex|debug|usehtml|(b|f|l)color|fsize|args|result)\\b'

Prism.languages.qsp = {
	'braced-comment': {
		pattern: /((^\s*?)|(\&\s*?))(![^\{]*\{[^\}]*\}.*?$)/m,
		alias: 'comment',
	},
	'quoted-comment': {
		pattern: /((^\s*?)|(\&\s*?))((![^"\n\r]*"[^"]*".*?$)|(![^'\n\r]*'[^']*?'.*?$))/m,
		alias: 'comment',
	},
	'comment': {
		pattern: /((^\s*?)|(\&\s*?))(!.*$)/m,
		lookbehind: false,
		greedy: true,
	},
	'string': {
		pattern: /("|')(?:[\s\S]*?)\1/im,
		lookbehind: false,
		greedy: true
	},
	'function': {
		pattern: /\@[\w\.\#а-я]+(?=\s*\()/i,
	},
	'start-location': /^\#\s*\S+.*$/im,
	'end-location': /^\-.*$/im,
	'label': /^\s*\:.*?(?=\&|$)/im,
	'sys-variable': RegExp(`(?:${system_vars_string}|${system_vars_num})`, 'i'),
	'builtin': RegExp(`(?:(${functions_string}|${functions_num}))`, 'i'),
	'number': /\b\d+\b/,
	'keyword': RegExp(`(?:${kw_text_operators}|${kw_operators}|${kw_controls})`, 'i'),
	'declarator': /(?:\b(local|set|let)\b)/,
	'operator': /[<>\+\-\*\/]=|<>|\+|\&|-|<|>|=|\/|\*|!|\b(and|or|mod|no)\b/i,
	'sign-punctuation': /[{}[\];(),:]/,
	'user-variable': /[\$\%][\wа-я]+|[\wа-я]+/i,
};