---
id: qsplib-parser
title: QSPlib Parser
---

﻿# QSPLib Parser

[QSPLib](https://github.com/QSPFoundation/qsp/tree/master/qsp) was parsing source files long before it became fashionable, and continues to do so to this day.

It is the parser closest to the language specification (actually, the specification is written from it), and others align with it with varying degrees of success.

It works on a "lazy" principle: it parses the source line by line and immediately interprets it. Thus, syntax errors are caught only when the parser encounters them.

<!-- todo: add example -->