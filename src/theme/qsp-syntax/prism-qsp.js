
let kw_operators = '\\b(act|addobj|cla|close|all|cls|cmdclear|copyarr|delact|delobj|dynamic|exit|gosub|goto|if|else|elseif|inclib|jump|killall|killobj|freelib|killvar|let|local|loop|menu|msg|opengame|openqst|play|refint|savegame|scanstr|set|settimer|showacts|showinput|showobjs|showstat|sortarr|unselect|view|wait|xgoto|addqst|killqst|unsel|cmdclr|gt|xgt|gs|exec)\\b'
let kw_controls = '\\b(act|if|elseif|else|loop|while|step|end)\\b'
let kw_text_operators = '\\*?\\b(pl?|nl|clr|clear)\\b'

let functions_string = '\\$(desc|user_text|usrtxt|maintxt|stattxt|curloc|selobj|selact|mid|(u|l)case|trim|replace|str|strfind|input|qspver|curacts|getobj|iif|dyneval|func|max|min|arritem)\\b'
let functions_num = '\\b(loc|obj|isnum|isplay|len|val|instr|strcomp|strpos|arrsize|arrpos|arrcomp|msecscount|rgb|countobj|ra?nd|iif|dyneval|func|max|min|arritem)\\b'

let system_vars_string = '\\$(counter|ongload|ongsave|onnewloc|onactsel|onobjsel|onobjadd|onobjdel|usercom|fname|backimage|args|result)\\b'
let system_vars_num = '\\b(nosave|disablescroll|disablesubex|debug|usehtml|(b|f|l)color|fsize|args|result)\\b'

Prism.languages.qsp = {
	'comment': {
		pattern: /((^\s*?)|(\&\s*?)|(\:\s*?))(![^\n{'"]*$)/m,
		lookbehind: true,
		greedy: true,
	},
	'braced-comment': {
		pattern: /((^\s*?)|(\&\s*?)|(\:\s*?))(![^\n{'"]*\{[^\}]*\}.*?$)/m,
		alias: 'comment',
		lookbehind: true,
		greedy: true,
	},
	'quoted-comment': {
		pattern: /((^\s*?)|(\&\s*?)|(\:\s*?))((![^\n{'"]*"[^"]*".*?$)|(![^'\n\r]*'[^']*?'.*?$))/m,
		alias: 'comment',
		lookbehind: true,
		greedy: true,
	},
	'string': {
		pattern: /("|')(?:[\s\S]*?)\1/im,
		lookbehind: false,
		greedy: true
	},
	'function': {
		pattern: /\@[\w\.а-я]+(?=\s*\()/i,
	},
	'start-location': /^\#\s*\S+.*$/im,
	'end-location': /^\-.*$/im,
	'label': {
		pattern: /^\s*:[^&\n]*(?=\&|$)/im,
		lookbehind: true,
		greedy: true,
	},
	'sys-variable': RegExp(`(?:${system_vars_string}|${system_vars_num})`, 'i'),
	'builtin': RegExp(`(?:(${functions_string}|${functions_num}))`, 'i'),
	'number': /\b\d+\b/,
	'keyword': RegExp(`(?:${kw_text_operators}|${kw_operators}|${kw_controls})`, 'i'),
	'declarator': /(?:\b(local|set|let)\b)/i,
	'operator': /[<>\+\-\*\/]=|<>|\+|\&|-|<|>|=|\/|\*|!|\b(and|or|mod|no)\b/i,
	'sign-punctuation': /[{}[\];(),:]/,
	'user-variable': /[\$\%][\wа-я]+|[\wа-я]+/i,
};