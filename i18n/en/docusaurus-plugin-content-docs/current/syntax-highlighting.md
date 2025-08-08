---
id: syntax-highlighting
title: Syntax Highlighting
---

# Syntax Highlighting

Syntax highlighting in editors and other environments is achieved through quite specific means, for which, unfortunately, there is no common solution. And since there is no common solution, difficulties arise with maintaining code for each individual solution.

<!-- todo: write about QGen -->

## Highlighting in VS Code

VS Code has two highlighting methods:

* TextMate format
* Semantic highlighting

<!-- todo: describe working principle -->

### Ready-made Solutions {#vscode-text-solutions}

* TextMate format
  * `glife/tools/syntax/VSCode/qsrc/syntaxes/QSP.tmLanguage.json`
  * [LangQSP by someone called Xorgroth](https://gitlab.com/kevinsmartstfg/girl-life/-/raw/master/tools/syntax/VSCode/qsrc/syntaxes/QSP.tmLanguage.json)

* Semantic highlighting
  * Combination of `Qsp.FSharp.Parser`, `Qsp.FSharp.ServerLanguage` and `Qsp.FSharp.VsCode`

## Highlighting in Sublime Text

### Ready-made Solutions {#sublime-text-solutions}

* [JAD_for_QSP](https://github.com/AleksVersus/JAD_for_QSP/blob/master/QSP.sublime-package/qsp.sublime-syntax)

## Highlighting in Other Environments

* [highlighting on wiki.qsp.org](https://wiki.qsp.org/lib/plugins/syntaxhighlighter3/sxh3/scripts/shBrushQsp.js)
* highlighting in [howdo_faq](https://github.com/AleksVersus/howdo_faq) by Aleks Versus

  The function that converts QSP code is [here](https://github.com/AleksVersus/howdo_faq/blob/7aea086c17ac34171f785f2ef3fc500dc132af6b/res/%5Bconverters%5D/nodes.py#L1204-L1271)