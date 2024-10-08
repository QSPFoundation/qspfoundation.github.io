---
authors:
  - alex
tags:
  - документация
  - syntax
  - синтаксис
  - язык QSP
---
# Ключевые слова, системные переменные и спецсимволы QSP

Поскольку этот раздел был практически полностью написан мной в другом проекте, я решил слегка его отредактировать и перенести сюда.

[Это раздел](../../../../docs/language/qsp-keywords/), в котором собраны все операторы, функции, системные переменные, а так же спецсимволы и синтаксемы языка QSP.

:::warning[Важно помнить:]
Раздел охватывает полностью ключевые слова и т.д. для версий плееров 5.8.0, и частично затрагивает плееры версии 5.9.0. А значит, в будущем требует дополнения.
:::

В процессе работы над разделом, я выяснил, что редактировать документацию удобнее всего, используя Обсидиан, благодаря тому, что обсидиан сам следит за правильностью всех созданных в проекте ссылок при перемещении или переименовании статей и разделов.

Чтобы комфотно работать в Обсидиане и не терять функциональность ссылок в Докузаурус, необходимо следовать некоторым правилам:

- Имена файлов должны начинаться с буквы, но ни в коем случае не с цифры.
    :::note[Потому что:]
    Докузаурус опускает числа в начале имён файлов. Из-за этого ссылки валидные в Обсидиане не будут работать в Докузаурусе. (Соответственно порядок размещения статей должен определяться через поле `sidebar_position` в yml-заголовке документа).
    :::
- Необходимо смириться с тем, что ссылки на `index.md` раздела не будут работать в докузаурусе, либо, если их "обрезать" для докузауруса, не будут работать в обсидиане. Лучше избегать создания разделов `index.md` для комфортной работы и там и там.
- Ссылки на файлы статей должны быть относительными (чтобы работать и там и там), и включать так же расширение файлов (`.md`).
    `../language/qsp-keywords/qsp-keywords-functions.md`
    :::note[Потому что:]
    Докузаурус опускает расширение `.md` в ссылках и таким образом в процессе работы ссылки поддерживаются и в обсидиане и в докузаурусе. После сборки ссылки во всех статьях приобретают вид валидный для докузауруса, но невалидный для Обсидиана.
    `https://dev.qsp.org/docs/language/qsp-keywords/qsp-keyword-operators`
    :::
- Необходимо смириться с тем, что обсидиан не поддерживает те же якоря заголовков, что и докузаурус, из-за чего сослаться на заголовок в обсидиане так же как в докузаурусе невозможно. Это не мешает обсидиану поддерживать такие ссылки при изменении местоположения статей и разделов.
