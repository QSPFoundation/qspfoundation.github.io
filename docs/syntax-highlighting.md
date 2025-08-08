---
id: syntax-highlighting
title: Подсветка синтаксиса
---

# Подсветка синтаксиса

Подсветка синтаксиса в редакторах и в прочих окружениях достигается довольно специфическими средствами, для которых, к сожалению, нет общего решения. А раз нет общего решения, то появляются трудности с сопровождением кода для каждого отдельного решения.

<!-- todo: написать про QGen -->

## Подсветка в VS Code

VS Code есть два способа подсветки:

* TextMate формат
* Семантическая подсветка

<!-- todo: описать принцип работы -->

### Готовые решения {#vscode-text-solutions}

* TextMate Формат
  * `glife/tools/syntax/VSCode/qsrc/syntaxes/QSP.tmLanguage.json`
  * [Формат TextMate от некого Xorgroth](https://gitlab.com/kevinsmartstfg/girl-life/-/raw/master/tools/syntax/VSCode/qsrc/syntaxes/QSP.tmLanguage.json)

* семантическая подсветка
  * Связка `Qsp.FSharp.Parser`, `Qsp.FSharp.ServerLanguage` и `Qsp.FSharp.VsCode`

## Подсветка в Sublime Text

### Готовые решения {#sublime-text-solutions}

* [JAD_for_QSP](https://github.com/AleksVersus/JAD_for_QSP/blob/master/QSP.sublime-package/qsp.sublime-syntax)

## Подсветка в прочих окружениях

* [подсветка на wiki.qsp.org](https://wiki.qsp.org/lib/plugins/syntaxhighlighter3/sxh3/scripts/shBrushQsp.js)
* подсветка в [howdo_faq](https://github.com/AleksVersus/howdo_faq) за авторством Aleks Versus

  Функция, которая преобразовывает код QSP, — [тут](https://github.com/AleksVersus/howdo_faq/blob/7aea086c17ac34171f785f2ef3fc500dc132af6b/res/%5Bconverters%5D/nodes.py#L1204-L1271)
