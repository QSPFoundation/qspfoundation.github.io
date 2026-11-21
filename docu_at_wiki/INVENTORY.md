# Инвентаризация источников и DokuWiki-карты

Статус: инвентаризация выполнена; карта статей и изображений собрана в [`config.toml`](config.toml). Из 64 MDX-источников 62 активны, две страницы-заглушки исключены.

## Источник сопоставлений

Использован файл [`urls_links_to_files.json`](https://github.com/AleksVersus/qsp_wiki_to_help/blob/main/html_src/urls_links_to_files.json), раздел `pages`.

Правило сопоставления: имя исходного `.mdx` переводится в имя `.html`; если оно совпадает с именем HTML-файла, указанного в JSON, целевой идентификатор берётся из URL вида `https://wiki.qsp.org/part:page`. Все 64 файла совпали, ручных сопоставлений страниц на этом этапе нет.

Категорийные файлы `_category.yml` и `_category.json` не считаются статьями и в таблицу не включены.

## Статьи из `docs/qsp_wiki`

| Исходный файл | Идентификатор DokuWiki |
|---|---|
| `docs/qsp_wiki/help_acts.mdx` | `help:acts` |
| `docs/qsp_wiki/help_glossary.mdx` | `help:glossary` |
| `docs/qsp_wiki/help_goto.mdx` | `help:goto` |
| `docs/qsp_wiki/help_limits.mdx` | `help:limits` |
| `docs/qsp_wiki/help_locations.mdx` | `help:locations` |
| `docs/qsp_wiki/help_objs.mdx` | `help:objs` |
| `docs/qsp_wiki/help_qsp.mdx` | `help:qsp` |
| `docs/qsp_wiki/howto_start.mdx` | `howto:start` |
| `docs/qsp_wiki/nyuansy-napisaniya-igr-pod-raznye-pleery/help_classic_qsp.mdx` | `help:classic_qsp` |
| `docs/qsp_wiki/nyuansy-napisaniya-igr-pod-raznye-pleery/help_qspider/help_qspider.mdx` | `help:qspider` |
| `docs/qsp_wiki/nyuansy-napisaniya-igr-pod-raznye-pleery/help_qspider/help_qspider_aeroqsp.mdx` | `help:qspider_aeroqsp` |
| `docs/qsp_wiki/nyuansy-napisaniya-igr-pod-raznye-pleery/help_qspider/help_qspider_gamecfg.mdx` | `help:qspider_gamecfg` |
| `docs/qsp_wiki/nyuansy-napisaniya-igr-pod-raznye-pleery/help_qspider/help_qspider_inclib.mdx` | `help:qspider_inclib` |
| `docs/qsp_wiki/nyuansy-napisaniya-igr-pod-raznye-pleery/help_qspider/help_qspider_interface.mdx` | `help:qspider_interface` |
| `docs/qsp_wiki/nyuansy-napisaniya-igr-pod-raznye-pleery/help_qspider/help_qspider_spectags.mdx` | `help:qspider_spectags` |
| `docs/qsp_wiki/nyuansy-napisaniya-igr-pod-raznye-pleery/help_qspider/help_qspider_standalone.mdx` | `help:qspider_standalone` |
| `docs/qsp_wiki/nyuansy-napisaniya-igr-pod-raznye-pleery/help_qspider/help_qspider_themes.mdx` | `help:qspider_themes` |
| `docs/qsp_wiki/oformlenie/help_graphics.mdx` | `help:graphics` |
| `docs/qsp_wiki/oformlenie/help_html.mdx` | `help:html` |
| `docs/qsp_wiki/oformlenie/help_interface.mdx` | `help:interface` |
| `docs/qsp_wiki/oformlenie/help_menu.mdx` | `help:menu` |
| `docs/qsp_wiki/oformlenie/help_sound.mdx` | `help:sound` |
| `docs/qsp_wiki/programmirovanie/help_arrays.mdx` | `help:arrays` |
| `docs/qsp_wiki/programmirovanie/help_coding.mdx` | `help:coding` |
| `docs/qsp_wiki/programmirovanie/help_conditional.mdx` | `help:conditional` |
| `docs/qsp_wiki/programmirovanie/help_cycle.mdx` | `help:cycle` |
| `docs/qsp_wiki/programmirovanie/help_dynamical.mdx` | `help:dynamical` |
| `docs/qsp_wiki/programmirovanie/help_expressions.mdx` | `help:expressions` |
| `docs/qsp_wiki/programmirovanie/help_jump.mdx` | `help:jump` |
| `docs/qsp_wiki/programmirovanie/help_organizing.mdx` | `help:organizing` |
| `docs/qsp_wiki/programmirovanie/help_principle.mdx` | `help:principle` |
| `docs/qsp_wiki/programmirovanie/help_service_locations.mdx` | `help:service_locations` |
| `docs/qsp_wiki/programmirovanie/help_strings/help_regexp.mdx` | `help:regexp` |
| `docs/qsp_wiki/programmirovanie/help_strings/help_strings.mdx` | `help:strings` |
| `docs/qsp_wiki/programmirovanie/help_tuples.mdx` | `help:tuples` |
| `docs/qsp_wiki/programmirovanie/help_variables.mdx` | `help:variables` |
| `docs/qsp_wiki/rasshirennye-vozmozhnosti/help_inputs.mdx` | `help:inputs` |
| `docs/qsp_wiki/rasshirennye-vozmozhnosti/help_modules.mdx` | `help:modules` |
| `docs/qsp_wiki/rasshirennye-vozmozhnosti/help_realtime.mdx` | `help:realtime` |
| `docs/qsp_wiki/rasshirennye-vozmozhnosti/help_savegame.mdx` | `help:savegame` |
| `docs/qsp_wiki/start.mdx` | `start` |
| `docs/qsp_wiki/utility-i-sredstva-razrabotki/help_analyzer.mdx` | `help:analyzer` |
| `docs/qsp_wiki/utility-i-sredstva-razrabotki/help_debugger.mdx` | `help:debugger` |
| `docs/qsp_wiki/utility-i-sredstva-razrabotki/help_qgen.mdx` | `help:qgen` |
| `docs/qsp_wiki/utility-i-sredstva-razrabotki/help_txt2gam.mdx` | `help:txt2gam` |
| `docs/qsp_wiki/vyvod-teksta/help_main.mdx` | `help:main` |
| `docs/qsp_wiki/vyvod-teksta/help_msgbox.mdx` | `help:msgbox` |
| `docs/qsp_wiki/vyvod-teksta/help_stat.mdx` | `help:stat` |

## Статьи из `docs/help_add`

| Исходный файл | Идентификатор DokuWiki |
|---|---|
| `docs/help_add/glossary_bag.mdx` | `glossary:bag` |
| `docs/help_add/glossary_snippet.mdx` | `glossary:snippet` |
| `docs/help_add/help_classic_standalone.mdx` | `help:classic_standalone` |
| `docs/help_add/help_html_classic.mdx` | `help:html_classic` |
| `docs/help_add/help_keywords.mdx` | `help:keywords` |
| `docs/help_add/help_keywords_operator.mdx` | `help:keywords_operator` |
| `docs/help_add/help_multid_array.mdx` | `help:multid_array` |
| `docs/help_add/help_txt2gam_emeditor.mdx` | `help:txt2gam_emeditor` |
| `docs/help_add/help_txt2gam_linux.mdx` | `help:txt2gam_linux` |
| `docs/help_add/help_txt2gam_manual.mdx` | `help:txt2gam_manual` |
| `docs/help_add/help_txt2gam_preprocessor.mdx` | `help:txt2gam_preprocessor` |
| `docs/help_add/howto_arrays.mdx` | `howto:arrays` |
| `docs/help_add/howto_namedconst.mdx` | `howto:namedconst` |
| `docs/help_add/howto_randomize.mdx` | `howto:randomize` |
| `docs/help_add/howto_vscode_extension.mdx` | `howto:vscode_extension` |
| `docs/help_add/regex_start.mdx` | `regex:start` |

## Активные страницы и исключения

- В `config.toml` активно сопоставлены 62 статьи.
- `docs/help_add/glossary_snippet.mdx` (`glossary:snippet`) и `docs/qsp_wiki/nyuansy-napisaniya-igr-pod-raznye-pleery/help_qspider/help_qspider_standalone.mdx` (`help:qspider_standalone`) содержат заглушку «Эта страница ещё не существует» и исключены из генерации.
- Целевые ID заглушек сохранены в `excluded_pages`, чтобы ссылки из других статей продолжали преобразовываться в ссылки на соответствующие страницы wiki.

## Инвентаризация MDX-разметки

Подсчёты выполнены по всем 64 MDX-файлам, включая две исключённые заглушки:

- Во всех файлах есть front matter с `title` и `sidebar_position`; каждый H1–H4 снабжён Docusaurus-якорем `{#id}`. Найдено 359 заголовков: 60 H1, 183 H2, 110 H3 и 6 H4.
- Найдено 584 закрытых fenced code blocks: 526 `qsp`, 44 `text`, 13 `html` и 1 `js`.
- Найдено 8 Markdown-таблиц в `help_html_classic.mdx`, `help_keywords.mdx` и `regex_start.mdx`.
- 9 Markdown-изображений распределены по 5 страницам.
- 398 относительных ссылок ведут на локальные MDX-файлы, все пути существуют и имеют целевой wiki ID (включая две исключённые страницы). Ещё 167 ссылок ведут на внешние URL.
- Три `DOCLINK::index::<id>` в `help_qspider_interface.mdx` ссылаются на заголовки этой же страницы. По правилу DokuWiki, сообщённому владельцем, их следует преобразовывать в `[[#Полный текст заголовка|текст ссылки]]`, находя заголовок по MDX-якорю `{#id}`.
- Сноски встречаются в `help_qsp.mdx` и `help_html.mdx`. Импорты/экспорты MDX, компоненты JSX и директивы `:::` в статьях не обнаружены; HTML-теги встречаются как примеры в коде/inline-code, а не как компоненты MDX.
- Front matter и Docusaurus-якоря не должны попадать в DokuWiki-разметку. Основной текст заголовка сохраняется. В `docs/qsp_wiki/vyvod-teksta/help_stat.mdx` front matter содержит полное название, но H1 обрезан («Окно дополнительного описан»); это отмечено как контентная аномалия, конвертер не должен молча исправлять текст.

## Изображения

Для восьми из девяти локальных изображений найдены существующие wiki-ресурсы в разделе `images` JSON. Для `qgen.png` владелец подтвердил корневой media ID `:qgen.png`. Девятое изображение не хранится на wiki: по решению владельца оно остаётся внешним ресурсом.

| Локальное изображение | Найденный DokuWiki media ID | Основание |
|---|---|---|
| `docs/qsp_wiki/help_ballad.jpg` | `help:ballad.jpg` | `_detail/help:ballad.jpg` |
| `docs/qsp_wiki/help_input_window.png` | `help:input_window.png` | `_detail/help:input_window.png` |
| `docs/qsp_wiki/help_level13.jpg` | `help:level13.jpg` | `_detail/help:level13.jpg` |
| `docs/qsp_wiki/help_qspblank2.jpg` | `help:qspblank2.jpg` | `_media/help:qspblank2.jpg` |
| `docs/qsp_wiki/help_wiki_logo.png` | `wiki:logo.png` | `_media/wiki:logo.png` |
| `docs/qsp_wiki/help_window_msg.png` | `help:window_msg.png` | `_detail/help:window_msg.png` |
| `docs/qsp_wiki/utility-i-sredstva-razrabotki/qgen.png` | `:qgen.png` | `_media/qgen.png` внутри URL `lib/exe/fetch.php`; root namespace подтверждён владельцем |
| `docs/qsp_wiki/vyvod-teksta/help_msgbox.png` | `help:msgbox.png` | `_detail/help:msgbox.png` |
| `docs/qsp_wiki/nyuansy-napisaniya-igr-pod-raznye-pleery/help_qspider/image.png` | внешняя ссылка `https://i.ibb.co/8z8MHyp/image.png` | Владелец подтвердил, что изображения на wiki нет и его нужно оставить внешним |

Представление внешнего изображения в статье DokuWiki:

```text
[[https://i.ibb.co/8z8MHyp/image.png|{{https://i.ibb.co/8z8MHyp/image.png?500|Ошибка qSpider}}]]
```

Ссылки на игровые файлы вроде `img/watermelon.png`, `image/orange.png` и `<img src="...">` внутри примеров кода не являются вложенными изображениями документа и не включались в эту таблицу.

## Сводка

- Исходные статьи: 64 MDX (48 в `qsp_wiki`, 16 в `help_add`); 62 включены в генерацию, 2 заглушки исключены.
- Найдено 9 локальных изображений (все в `qsp_wiki`): 8 привязаны к существующим wiki media ID, одно оставлено внешней ссылкой по решению владельца.
- Проверено чтение исходного MDX и образца DokuWiki с явной кодировкой UTF-8. Кажущееся mojibake при чтении PowerShell по умолчанию вызвано выбором кодировки чтения, а не содержимым файлов.
- `output/` и `.state/` остаются локальными и исключены из Git; при исчезновении исходника сгенерированная статья сохраняется, а из манифеста удаляется только соответствующая запись.
- В карте есть и другие страницы/изображения, не представленные среди входных файлов этих двух папок; в таблицы они не включены.
