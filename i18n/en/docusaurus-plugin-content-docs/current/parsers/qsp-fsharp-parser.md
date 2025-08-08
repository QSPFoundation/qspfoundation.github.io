---
id: qsp-fsharp-parser
title: QSP Fsharp Parser
---

﻿# Qsp.FSharp.Parser

[Qsp.FSharp.Parser](https://github.com/QSPFoundation/Qsp.FSharp/tree/master/src/Qsp.FSharp.Core) is developed for development environments that support LSP (for example, VS Code, for whose [extension](https://github.com/QSPFoundation/Qsp.FSharp.VsCode) all this was started).

Qsp.FSharp.Parser parses the entire source code at once (which differs from the [parser in QSPLib](./qsplib-parser.md)) and simultaneously collects:

* tokens and their locations (it seems this should be done by a *lexical* analyzer, not a syntactic one, but everything is not so simple there)
* semantic meaning of tokens
* builds a syntax tree

The main humor is that the syntax tree is not needed at all for the LSP server, but the parser still stubbornly builds it and then discards it. However, it is used for code formatting (which is called, for example, from the LSP server, so it is still needed!) and other not yet documented things.

Technically, nothing prevents writing an interpreter that could be fed a syntax tree as input, but let QSPLib handle this since it's designed for this purpose.

Qsp.FSharp.Parser tries to honestly follow the specification, but there are also plenty of personal interpretations and shortcomings.

<!-- todo: provide example -->

Written in F#, which, on one hand, ties it to the .Net platform, and on the other hand, allows it to be compiled to JS and other languages using Fable. If there was a desire, as they say.