
let kw_operators = 'inclib|freelib|addqst|killqst|openqst|opengame|savegame|addobj|delobj|killobj|unsel|unselect|cls|cla|delact|cmdclr|cmdclear|play|close|all|jump|dynamic|goto|gt|xgoto|xgt|gosub|gs|menu|exit|showobjs|showstat|showacts|showinput|refint|copyarr|killvar|killall|view|msg|settimer|wait|exec'
let kw_controls = 'act|if|elseif|else|loop|while|step|end'
let kw_text_operators = '\\*(pl?|nl|clr|clear)|(pl?|nl|clr|clear)'

let functions_string = '\\$(desc|user_text|usrtxt|maintxt|stattxt|curloc|selobj|selact|mid|(u|l)case|trim|replace|str|strfind|input|qspver|curacts|getobj|iif|dyneval|func|max|min|arritem)\\b'
let functions_num = '\\b(loc|obj|isnum|isplay|len|val|instr|strcomp|strpos|arrsize|arrpos|arrcomp|msecscount|rgb|countobj|ra?nd|iif|dyneval|func|max|min|arritem)\\b'

let system_vars_string = '\\$(counter|ongload|ongsave|onnewloc|onactsel|onobjsel|onobjadd|onobjdel|usercom|fname|backimage|args|result)\b'
let system_vars_num = '\\b(nosave|disablescroll|disablesubex|debug|usehtml|(b|f|l)color|fsize|args|result)\\b'

Prism.languages.qsp = {
	'comment': {
		pattern: /((^\s*?)|(\&\s*?))(!.*$)/m,
		lookbehind: false,
		greedy: true
	},
	'string': {
		pattern: /("|')(?:[\s\S]*?)\1/i,
		lookbehind: false,
		greedy: true
	},
	'sys-variable': RegExp(`(?:${system_vars_string}|${system_vars_num})`, 'i'),
	'builtin': RegExp(`(?:(${functions_string}|${functions_num}))`, 'i'),
	'number': /\d+/,
	'keyword': RegExp(`(?:((${kw_text_operators})\b)|${kw_operators}|${kw_controls})`, 'i'),
	'start-location': /^\#\s*\S+.*$/im,
	'end-location': /^\-.*$/im,
	'operator': /[<>\+\-\*\/]=|<>|\+|-|<|>|=|\/|\*|!|and|or|mod/i,
	'punctuation': /[{}[\];(),:]/,
	'user-variable': /[\$\%][\wа-я]+|[\wа-я]+/i,
};
