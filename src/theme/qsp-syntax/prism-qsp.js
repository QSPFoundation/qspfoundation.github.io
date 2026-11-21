const statements = [
    'play', 'close', 'view', 'exit', 'jump',
    'gosub', 'gs', 'goto', 'gt', 'xgoto', 'xgt',
    'pl', 'p', 'nl', 'clear', 'clr',
    '\\*pl', '\\*p', '\\*nl', '\\*clear', '\\*clr',
    'msg', 'wait', 'addobj', 'delobj', 'modobj', 'resetobj', 'killobj',
    'unselect', 'unsel', 'killall', 'cla', 'delact', 'cls',
    'cmdclear', 'cmdclr', 'menu', 'settimer', 'dynamic',
    'setvar', 'insvar', 'killvar', 'copyarr', 'movearr', 'sortarr', 'scanstr', 'unpackarr',
    'opengame', 'savegame', 'openqst', 'inclib', 'freelib', 'refint',
    'showacts', 'showinput', 'showobjs', 'showstat',
].join('|')

const controls = 'act|if|elseif|else|loop|while|step|end'

const functions = [
    'desc', 'max', 'min', 'rand', 'rnd', 'val', 'iif', 'dyneval', 'func',
    'input', 'usrtxt', 'user_text', 'maintxt', 'stattxt',
    'getobj', 'countobj', 'selobj', 'curloc', 'curobjs', 'selact', 'curacts',
    'arrsize', 'arrtype', 'arrkey', 'arritem', 'arrpack', 'arrpos', 'arrcomp',
    'strcomp', 'strfind', 'strpos', 'instr', 'isnum',
    'trim', 'ucase', 'lcase', 'len', 'mid', 'replace', 'str',
    'isplay', 'rgb', 'msecscount', 'qspver',
].join('|')

const system_vars = [
    'counter', 'ongload', 'ongsave', 'onnewloc', 'onactsel', 'onobjsel', 'onobjadd', 'onobjdel',
    'usercom', 'fname', 'backimage', 'args', 'result',
    'nosave', 'disablescroll', 'disablesubex', 'debug', 'usehtml',
    'bcolor', 'fcolor', 'lcolor', 'fsize',
].join('|')

const delimiter_chars = "\\s&'\"(){}\\[\\],:=!<>+\\-/*\\\\;^@?"
const name_char = `[^${delimiter_chars}.]`
const name_start = `[^${delimiter_chars}.0-9#$%]`
const type_prefix = '[#$%]'
const qsp_prism = Prism
const named_token = (pattern) => ({
    pattern: RegExp(`(^|[${delimiter_chars}.])(?:${pattern})(?!${name_char})`, 'i'),
    lookbehind: true,
})

const interpolated_string = (quote) => {
    const inner_quote = quote === '"' ? "'" : '"'
    const literal = `${inner_quote}(?:[^${inner_quote}]|${inner_quote}${inner_quote})*${inner_quote}(?!${inner_quote})`

    return {
        pattern: RegExp(`${quote}(?:[^${quote}]|${quote}${quote})*${quote}`),
        greedy: true,
        inside: {
            interpolation: {
                pattern: RegExp(`<<(?:(?!>>)[^"']|${literal})*>>`),
                greedy: true,
                inside: {
                    'interpolation-punctuation': {
                        pattern: /^<<|>>$/,
                        alias: 'punctuation',
                    },
                },
            },
        },
    }
}

const balanced_pattern = (open, close, atom, depth = 20) => {
    let inner = `(?:${atom})*`
    for (let i = 0; i < depth; i++) {
        inner = `(?:${atom}|\\${open}${inner}\\${close})*`
    }
    return `\\${open}${inner}\\${close}`
}

const string_pattern = `"(?:[^"]|"")*"|'(?:[^']|'')*'`
const end_delimiter = new RegExp(`^[${delimiter_chars}]$`)
let processing_qsp_regions = false

const scan_qsp_regions = (code) => {
    const regions = []
    let regionStart = 0
    let regionType = 'code'
    let textMode = null
    const stack = []
    const textStack = []
    let inString = null
    let inTextString = null
    let lastNonWhitespace = null
    let atLineStart = true

    const pushRegion = (type, start, end) => {
        if (end > start) {
            regions.push({ type, text: code.slice(start, end) })
        }
    }

    const startText = (mode, start) => {
        pushRegion(regionType, regionStart, start)
        regionStart = start
        regionType = mode === 'label' ? 'label' : 'comment'
        textMode = mode
        textStack.length = 0
        inTextString = null
    }

    const finishText = (end) => {
        pushRegion(regionType, regionStart, end)
        regionStart = end
        regionType = 'code'
        textMode = null
    }

    const isInsideRoundOrSquare = () => {
        for (let i = stack.length - 1; i >= 0; i--) {
            if (stack[i] === '(' || stack[i] === '[') return true
            if (stack[i] === '{') return false
        }
        return false
    }

    for (let i = 0; i < code.length; i++) {
        const ch = code[i]
        const startsLine = atLineStart
        atLineStart = ch === '\n' || (atLineStart && (ch === ' ' || ch === '\t'))

        if (textMode === null) {
            if (
                startsLine && inString === null && stack.length === 0 &&
                ((ch === '#' && (code[i + 1] === ' ' || code[i + 1] === '\t')) ||
                    (ch === '-' && code[i + 1] === '-'))
            ) {
                const newline = code.indexOf('\n', i)
                i = newline === -1 ? code.length - 1 : newline - 1
                continue
            }

            if (inString !== null) {
                if (ch === inString) {
                    if (code[i + 1] === inString) {
                        i++
                    } else {
                        inString = null
                    }
                }
            } else {
                const atStatementStart =
                    (lastNonWhitespace === null || lastNonWhitespace === '\n' ||
                        lastNonWhitespace === '&' || lastNonWhitespace === '{' ||
                        lastNonWhitespace === ':') &&
                    !isInsideRoundOrSquare()

                if (ch === ':' && atStatementStart) {
                    startText('label', i + 1)
                    continue
                }

                if (
                    atStatementStart && code.slice(i, i + 3).toLowerCase() === 'end' &&
                    (i + 3 === code.length || end_delimiter.test(code[i + 3]))
                ) {
                    i += 2
                    lastNonWhitespace = code[i]
                    let noteStart = i + 1
                    while (code[noteStart] === ' ' || code[noteStart] === '\t') noteStart++
                    if (noteStart < code.length && !/[\r\n&}]/.test(code[noteStart])) {
                        startText('note', noteStart)
                        i = noteStart - 1
                    }
                    continue
                }

                if (ch === '"' || ch === "'") {
                    inString = ch
                } else if (ch === '{') {
                    stack.push('{')
                } else if (ch === '}') {
                    if (stack[stack.length - 1] === '{') stack.pop()
                } else if (ch === '[') {
                    stack.push('[')
                } else if (ch === ']') {
                    if (stack[stack.length - 1] === '[') stack.pop()
                } else if (ch === '(') {
                    stack.push('(')
                } else if (ch === ')') {
                    if (stack[stack.length - 1] === '(') stack.pop()
                } else if (ch === '!' && atStatementStart) {
                    startText('comment', i)
                }
            }

            if (ch !== ' ' && ch !== '\t') {
                lastNonWhitespace = ch
            }
        } else if (inTextString !== null) {
            if (ch === inTextString) {
                if (code[i + 1] === inTextString) {
                    i++
                } else {
                    inTextString = null
                }
            }
        } else if (ch === '"' || ch === "'") {
            inTextString = ch
        } else if (ch === '{') {
            textStack.push('{')
        } else if (ch === '}') {
            if (textStack[textStack.length - 1] === '{') {
                textStack.pop()
            } else if (stack[stack.length - 1] === '{') {
                finishText(i)
                stack.pop()
                lastNonWhitespace = null
            }
        } else if (ch === '&' && textMode !== 'comment' && textStack.length === 0) {
            finishText(i)
            lastNonWhitespace = '&'
        } else if (ch === '\n' && textStack.length === 0) {
            finishText(textMode === 'label' ? i : i + 1)
            lastNonWhitespace = '\n'
        }
    }

    pushRegion(regionType, regionStart, code.length)
    return regions
}

Prism.languages.qsp = {
    'code-block': {
        pattern: new RegExp(balanced_pattern('{', '}', `[^{}"']|${string_pattern}`)),
        greedy: true,
        alias: 'punctuation',
        inside: {},
    },
    'start-location': /^[ \t]*#[ \t]+\S.*$/m,
    'end-location': /^[ \t]*--.*$/m,
    'string': [interpolated_string('"'), interpolated_string("'")],
    'user-call': {
        pattern: RegExp(`(^|[${delimiter_chars}.])(@@?\\s*[^${delimiter_chars}]+)`, 'i'),
        lookbehind: true,
        greedy: true,
        alias: 'function',
    },
    'sys-variable': named_token(`${type_prefix}?(?:${system_vars})`),
    'builtin': named_token(`${type_prefix}?(?:${functions})`),
    'number': [named_token('\\d+'), /\?/],
    'keyword': [
        named_token('else\\s+if'),
        named_token(`${controls}|${statements}`),
    ],
    'declarator': named_token('alias|local|set|let'),
    'operator': [
        /<=|>=|<>|=<|=>|\+=|-=|\*=|\/=|[+\-*/=<>!&]/,
        named_token('and|or|mod|no|obj|loc'),
    ],
    'sign-punctuation': /[{}[\]();,:.]/,
    'user-variable': named_token(`${type_prefix}?${name_start}${name_char}*`),
};

const nested_tokens = { ...Prism.languages.qsp }
for (const token of ['code-block', 'start-location', 'end-location']) {
    delete nested_tokens[token]
}
for (const string of Prism.languages.qsp.string) {
    string.inside.interpolation.inside.rest = nested_tokens
}
Prism.languages.qsp['code-block'].inside = nested_tokens

Prism.hooks.add('after-tokenize', (env) => {
    if (env.language !== 'qsp' || processing_qsp_regions) return

    const regions = scan_qsp_regions(env.code)
    if (!regions.some((region) => region.type !== 'code')) return

    let normalizedCode = ''
    const replacements = new Map()
    let placeholderIndex = 0
    for (const region of regions) {
        if (region.type === 'code') {
            normalizedCode += region.text
        } else {
            let placeholder
            do {
                placeholder = `qspregionplaceholder${placeholderIndex++}qsp`
            } while (env.code.toLowerCase().includes(placeholder))
            replacements.set(placeholder, region)
            normalizedCode += `(${placeholder})`
        }
    }

    processing_qsp_regions = true
    try {
        env.tokens = qsp_prism.tokenize(normalizedCode, env.grammar)
    } finally {
        processing_qsp_regions = false
    }

    const regionToken = (region) => {
        const type = region.type === 'label' ? 'label' : 'comment'
        return new qsp_prism.Token(type, region.text)
    }

    const restorePlaceholders = (tokens) => {
        const restored = []
        for (let i = 0; i < tokens.length; i++) {
            const token = tokens[i]
            const placeholderToken = tokens[i + 1]
            const closingToken = tokens[i + 2]
            if (
                typeof token !== 'string' && token.content === '(' &&
                typeof placeholderToken !== 'string' &&
                typeof placeholderToken.content === 'string' &&
                replacements.has(placeholderToken.content) &&
                typeof closingToken !== 'string' && closingToken.content === ')'
            ) {
                restored.push(regionToken(replacements.get(placeholderToken.content)))
                i += 2
                continue
            }
            if (typeof token === 'string') {
                restored.push(token)
            } else if (typeof token.content === 'string' && replacements.has(token.content)) {
                restored.push(regionToken(replacements.get(token.content)))
            } else {
                if (Array.isArray(token.content)) {
                    token.content = restorePlaceholders(token.content)
                    token.length = token.content.reduce((length, child) => length + child.length, 0)
                }
                restored.push(token)
            }
        }
        return restored
    }

    env.tokens = restorePlaceholders(env.tokens)
})