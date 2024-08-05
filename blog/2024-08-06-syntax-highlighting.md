---
authors:
  - alex
tags:
  - документация
  - docusaurus
  - highlighting
---
# Подсветка синтаксиса QSP в Docusaurus

Добавил в документацию Docusaurus подсветку синтаксиса для кода QSP. Она весьма проста, и умеет подсвечивать синтаксис на самом примитивном уровне. Тем не менее работает уже довольно сносно, не считая некоторых артефактов.

Например:

```qsp title="Действие по условию"
if ваза_на_столе=1:
  ! если переменная-маркер ваза_на_столе равна 1

  ! создаём действие
  act "Взять вазу со стола":
    ! в действии изменяем значение переменной-маркера
    ваза_на_столе=0
    addobj "Ваза"
    goto $curloc
  end
end
```

Другой пример:

```qsp title="Код в формате qsps с двумя локациями"
# start
result = 123  & ! записываем число в переменную result
N=24
*pl func('square')  & ! выведет на экран 576
*pl result  & ! выведет на экран 123
- start -

vase_on_desk = 0

# square
result = N * N
- square -
```

И ещё пример:

```qsp
# em.summ
local $_, $res
if $args[0]='': exit  & !@ если не указано имя массива. Защита от дурака
if $args[1]='':
  !@ если аргумент не указан, в качестве разделителя используется пробел
  $args[1]=' '
elseif $args[1]='/se':
  !@ если аргументом указан ключ, разделитель не используется
  $args[1]=''
end
!@ если указан текстовый массив, помечаем в переменной-маркере
if instr($args[0],'$')=1: $_='$'
loop local i,size=0,arrsize($args[0]) while i<size step i+=1:
  if $_='$':
    !@ для текстовых массивов раюотает конкатенация
    $res+=$dyneval("$result=<<$args[0]>>[<<i>>]")+$args[1]
  else
    !@ для числовых суммирование
    res+=dyneval("result=<<$args[0]>>[<<i>>]")
  end
end
!@ возвращение результата
if $_='$':
  $result=$res
else
  result=res
end
--- em.summ ---------------------------------
```

:::warning[Проверяйте окончания строк]
LineEndings при использовании подсветки в markdown-файлах для Docusaurus должны быть строго `LF`! Не `CRLF`, иначе вылезают артефакты в виде лишних отступов.
:::

Установка подсветки в ваш Docusaurus весьма проста:
1. Используйте swizzle для того, чтобы добавить неподдерживаемые языки, введя команду в терминале:
  ```bash
  npm run swizzle @docusaurus/theme-classic prism-include-languages
  ```
  При этом будет создан файл "`src/theme/prism-include-languages.ts`" (или `.js`).
2. В папке "`src/theme"` создайте папку `qsp-syntax` и скопируйте в неё файл "`prism-qsp.js`", например, [отсюда](). <!-- TODO: не забыть добавить ссылку -->
3. В файле "`src/theme/prism-include-languages.ts`" отредактируйте функцию `prismIncludeLanguages`:
  ```ts
  export default function prismIncludeLanguages(PrismObject: typeof PrismNamespace,): void {
    // ...
    additionalLanguages.forEach((lang) => {
      // ...
      require(`prismjs/components/prism-${lang}`);
    });
    require('./qsp-syntax/prism-qsp.js');
    // ..
  }
  ```

После сохранения и перезапуска сервера, или при сборке проекта, подсветка QSP-кода подхватится.

Больше примеров работы подсветки можно посмотреть в **[онлайн-версии справочника](https://aleksversus.github.io/howdo_faq/)** по самым часто задаваемым вопросам о QSP, на котором собственно и производились опыты.

:::tip
Параллельно была написана подсветка для Obsidian: **[qsp-syntax-obsidian](https://github.com/AleksVersus/qsp-syntax-obsidian)**.
::