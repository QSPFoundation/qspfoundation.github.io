---
sidebar_position: 3
---

# Функции


## `$CURACTS`


`$CURACTS` —  данная функция возвращает выведенные на экран действия в виде кода QSP, как текстовое значение.

Действия сохраняются в виде набора операторов `act` с cответствующими параметрами и операциями.

Записав возвращённое функцией значение в переменную, можно восстановить действия с помощью оператора `dynamic`. Пример:

```qsp
! записываем текущие действия в переменную
$actlist = $curacts
! восстанавливаем действия из переменной
dynamic $actlist
```

## `$CURLOC`


`$CURLOC` —  функция возвращает название текущей локации, т.е. локации, в которой "находится" игрок.

Технически это следует понимать так. В момент запуска игры плеер начинает выполнять код самой первой локации в игре, а когда код выполнен, плеер "останавливается" и ждёт участия игрока. Игрок может нажимать различные кнопки в игре, ссылки и выбирать пункты меню, что приводит к выполнению других блоков кода (например, действий) и переходам на новые локации по `goto` или `xgoto`. При таких переходах плеер вновь выполняет код других локаций и, когда код выполнен, "останавливается".

Так вот, когда на локацию осуществлён непосредственный переход (т.е. по `goto` или `xgoto`, либо это самая первая локация в игре), `$curloc` начинает возвращать название этой локации, — во всё время, пока выполняется код, и когда плеер "останавливается". Если после остановки не происходит переход по `goto`/`xgoto`, значение, которое возвращает `$curloc`, не меняется.

Пример использования:

```qsp
*pl $curloc & ! выводим название текущей локации в Окно основного описания
*pl "Сколько раз перезашли: <<перезашёл>>"
act "Перезайти на текущую локацию":
    перезашёл += 1
    goto $curloc
end
```

## `$DESC`


`$DESC` —  возвращает текст базового описания локации с заданным названием. Общая запись:

```qsp
$DESC([$локация])
```

, где `[$локация]` — это название интересующей нас локации. Например:

```qsp
! возвращаем базовое описание локации "каморка_под_лестницей"
$desc('каморка_под_лестницей')
!возвращаем базовое описание текущей локации
$desc($curloc)
```

Если в базовом описании присутствуют подвыражения, функция автоматически раскрывает их.

:::warning[Обратите внимание!]
Функция возвращает текст, написанный только в поле "Описание" (**Базовое описание**) редактора **Quest Generator**. При работе в текстовом редакторе данное поле вам недоступно и функция будет всегда возвращать пустую строку.
:::

## `$DYNEVAL`


`DYNEVAL` —  выполняет код, переданный в виде строки текста, и возвращает результат, если он есть. Общая запись:

```qsp
$DYNEVAL([$код], [аргумент 0], [аргумент 1], ... , [аргумент 18])
DYNEVAL([$код], [аргумент 0], [аргумент 1], ... , [аргумент 18])
```

, где `[$код]` — это обычный код QSP, записанный в виде текста. Выполнение такого кода аналогично выполнению кода функции `FUNC`. Аргументы `[аргумент 0]`, `[аргумент 1]` и т.д. могут использоваться внутри `[$код]`, их значения автоматически помещаются в переменные `args[0]`, `args[1]`, и т.д. соответственно.

Внутри выполняемого кода `dyneval` используется свой собственный массив `ARGS`, его значения не пересекаются со значениями `ARGS` на локации, из которой `dyneval` была вызвана.

После выполнения кода, переданного функции `dyneval`, продолжается вычисление выражения, в котором расположена функция `dyneval`.

Чтобы `dyneval` возвращала результат, необходимо внутри `[$код]` присвоить этот результат переменной `result`.

Примеры:

```qsp
dyneval('result = 3 + 4')
*pl $dyneval('$result = mid("abcd", 2, 1) + "qwerty"')
проход = dyneval("result = ($args[0] <> 'текст')", 'строка')
```

- Чтобы `DYNEVAL` вернула строковое значение, результат должен быть записан в `$RESULT`.
- Чтобы `DYNEVAL` вернула числовое значение, результат должен быть записан в `RESULT`.
- `$RESULT` и `RESULT` — это одна и та же переменная, но с разными типами данных. Следует помнить, что новая запись значения затирает предыдущее, какого бы типа данных не было это значение.

Если при выполнении `dyneval` она не возвращает значения (`result` не инициализируется), и является единственным элементом выражения, передаваемого неявному оператору, плеер ничего не выведет на экран. Т.е. `dyneval` будет работать, как `DYNAMIC`. Пример:

```qsp
! неявный оператор выведет на экран 123:
123
! код в dyneval выполнится, но на экране
! мы ничего не увидим:
dyneval("code = 123 + 890")
! неявный оператор выведет на экран 1013:
code
```

См. также [оператор `DYNAMIC`](qsp-keyword-operators.md#dynamic).

## `$FUNC`


`FUNC` —  выполнение кода указанной локации без непосредственного перехода на неё с возвращением значения.

Общая запись:

```qsp
FUNC([$локация], [аргумент 0], [аргумент 1], ... , [аргумент 18])
$FUNC([$локация], [аргумент 0], [аргумент 1], ... , [аргумент 18])
```

, где `[$локация]` — это название локации, код которой мы хотим выполнить без непосредственного перехода на неё. Аргументы `[аргумент 0]`, `[аргумент 1]` и т.д. могут использоваться на этой локации, их значения автоматически помещаются в переменные `args[0]`, `args[1]`, и т.д. соответственно. 

Чтобы `FUNC` вернула строковый результат, на указанной локации нужно присвоить этот результат переменной `$RESULT`. Для возвращения числового результата, он должен быть присвоен переменной `RESULT`. Следует помнить, что `$RESULT` и `RESULT` — это одна и та же переменная, но разных типов, поэтому если вы определили на локации и `$RESULT` и `RESULT`, функция вернёт то значение, которое было записано в эту переменную последним.

Если переменной `RESULT` не было присвоено ни строковое, ни числовое значение, функция ничего не вернёт. И тут есть два варианта поведения плеера.
- Если функция `FUNC` стоит в каком либо выражении, вместо функции будет подставлено значение по умолчанию (пустая строка или ноль в зависимости от типа самого выражения).
- Если функция `FUNC` стоит сразу после неявного оператора, такой оператор будет проигнорирован, и на экран ничего выводиться не будет. Пример:
    ```qsp title="локация_Н"
    N = 23 * 13
    ! ни одно значение не присваивается переменной result
    ```
    
    ```qsp title="Другая локация"
    'строка 1'
    func('локация_Н') &! ничего не выведется на экран
    'строка 2'
    56 + func('локация_Н') &! функция стоит в выражении. Её значение = 0
    ```

:::note
Не обязательно, но рекомендуется, записывать ключевое слово `FUNC` с символом `$`, если функция должна вернуть текстовое значение, и без символа `$`, если функция должна вернуть числовое значение:

```qsp
$func('срез_строки', 'Мы вышли из дома, когда во всех окнах погасли огни.', 3, 7)
func('возвести_в_степень', 3, 3)
```
:::

При вызове указанной локации с помощью  `FUNC` происходит следующее:
- Плеер прерывает выполнение текущего кода (например, кода текущей локации), и обращается к указанной локации 
- Базовое описание и список действий указанной локации добавляются к описанию и действиям текущей локации. 
- Выполненяется код из поля **Выполнить при посещении**
- Затем плеер возвращается к выполнению кода, который прервал. То есть к вычислению выражения, в котором стоит данная функция.

На каждой локации автоматически создаются свои собственные уникальные массивы  `ARGS` и  `RESULT`, поэтому значения в этих массивах для каждой локации будут свои собственные. После выполнения кода локации, вызванной по  `FUNC`, массивы  `ARGS` и  `RESULT` этой локации уничтожаются.

Другие примеры:

```qsp
!Обработка локации "функция" как функции. 
!Массив ARGS пуст.
яблоки = FUNC('функция')
 
!обработка локации с названием лежащим в переменной $name как функции. ARGS[0] равен 1.
pl func($name, 1) * 78
 
!обработка локации с названием в $name как функции. 
!$ARGS[0] содержит строку "строка", ARGS[1] равен 2.
msg "text" + func($name, "строка", 2)
```

```qsp
! код локации для функции, получающей сумму ряда чисел от единицы до указанного значения
# summ
! в args[0] будет помещено число, которое мы укажем в качестве [аргумента 0]
loop while args[0]>0 step args[0] -= 1:
    result += args[0]
end
---summ---

! пример вызова локации "summ", как функции
*pl func("summ", 19) & ! выведет на экран 190
! пример вызова с записью названия локации в переменную
$name_loc = "summ"
*pl func($name_loc, 23) & ! выведет на экран 276
```

## `$GETOBJ`


`$GETOBJ` —  возвращает название предмета в *Окне предметов*, расположенного в заданной позиции. Общая запись:

```qsp        
$GETOBJ([#номер предмета])
```

Индексация (нумерация) предметов в *Окне предметов* ведётся с 1. Если предмета с индексом `[#номер предмета]` не существует, возвращается пустая строка (`''`).

Примеры:

```qsp
$getobj(1) & ! вернёт название первого предмета в рюкзаке

$getobj(countobj) & ! вернёт название последнего добавленного предмета
```

Код, подсчитывающий в массиве `OBJECTS` число предметов с одинаковым названием:

```qsp
loop local i = 1 while i <= countobj step i += 1:
    objects[$getobj(i)] += 1
end
```

## `$IIF`


`IIF` —  возвращает значение в зависимости от верности выражения.

Общая запись:

```qsp
IIF([#выражение], [#выражение_да], [#выражение_нет])
$IIF([#выражение], [$выражение_да], [$выражение_нет])
```

Если `[#выражение]` верно, возвращает значение выражения `[выражение_да]`, в противном случае возвращает значение выражения `[выражение_нет]`.

Из выражений `[выраажение_да]` и `[выражение_нет]` будет вычислено только одно, в зависимости от того, будет ли выполнено условие.

Примеры:

```qsp
!Модуль числа
abs_x = iif(x>0, x, -x)

!А следующая конструкция НЕ вызовет ошибку деления на ноль:
x = 0
y  = iif(x = 0, 0, 1/x)

! типичное решение для вывода времени, чтобы не терять ноль на часах:
$iif(hour>9, $str(hour), "0"+$str(hour)) + ":"+$iif(minute>9, $str(minute), "0"+$str(minute))
```

Эквивалентность конструкций условия с оператором `IF` и функции `IIF`:

```qsp
if number mod 2 = 0:
    *pl "Число чётное"
else
    *pl "Число нечётное"
end
! эквивалентно
*pl $iif(number mod 2 = 0,"Число чётное","Число не чётное")
```

## `$INPUT`


`$INPUT` —  возвращает интерпретатору введённый игроком текст, либо `''` (пустая строка), если была нажата кнопка "Отмена". Общая запись:

```qsp
$INPUT([$текст])
```

, где `[$текст]` — это приглашение в диалоговом окне, которое видит игрок. Например:

```qsp
$name = $input('Как звать тебя, герой?')
```

При выполнении данной команды на экране появится диалоговое окно с текстом "Как звать тебя, герой?", а выполнение остального кода приостановится, пока игрок не провзаимодействует с диалоговым окном.

Игрок может ввести или не ввести текст, и нажать кнопку "ОК" или "Отмена". Если игрок ввёл текст и нажал кнопку "ОК", функция `$input` вернёт переменной `$text` введённый игроком текст. Во всех остальных случаях после закрытия диалогового окна функция вернёт пустую строку (`''`).

Другие примеры:

```qsp
! Вопрос с одним правильным ответом. 
if $input('Что приходит после тьмы?') = 'свет':
    msg 'Все верно.'
else
    msg 'Ответ не верный.'
end

! Пример реализации вопроса с несколькими вариантами ответа из которых любой будет правильным.
$answer = $trim($lcase($input('Ответить')))
if instr($answer, 'красный') or instr($answer, 'желтый') or instr($answer, 'зеленый'): gt 'win'
! Введя красный или зеленый ил желтый произойдет переход на локацию 'win'
```

Допустимо, но не одобряется, использовать функцию для возвращения числовых значений:

```qsp
INPUT([$приглашение])
```

Это может привести к различным ошибкам в игре, если игрок введёт в диалоговом окне не только цифры. Например:

```qsp
age = input('Сколько вам лет?')
```

Если игрок введёт вместо числа строку "24 года", плеер выдаст ошибку **101** "Несоответствие типов данных". Подобные ситуации должен предусматривать автор игры, а значит правильно будет озаботиться проверкой введённого значения уже после того, как функция `$input` будет выполнена.

```qsp
loop local $text while 1:
    ! предлагаем игроку ответить на вопрос
    ! и присваиваем введённый текст переменной
    $text = $input('Сколько вам лет?')
    ! если во введённом тексте содержатся не только цифры
    ! либо игрок не ввёл ответ
    if isnum($text) and $text <> "":
        ! игрок ввёл число
        age = val($text) & ! устанавливаем возраст
        jump 'break' & ! прерываем цикл
    else
        ! игрок ничего не ввёл или ввёл некорректное значение
        ! цикл продолжается
    end
end
:break
```

## `$LCASE`


`$LCASE` —  возвращает строку маленьких букв, полученную изменением регистра букв исходной строки. Общая запись:

```qsp
$LCASE([$текст])
```

, где `[$текст]` — любая строка текста.

Примеры:

```qsp
$lcase('TExT#') & ! вернёт 'text#'
$lcase('Привет, Алиса!') & ! вернёт 'привет, алиса!'
$lcase('Я НЕ ХОЧУ НА ВАС ОРАТЬ.') & ! вернёт 'я не хочу на вас орать.'
```

## `$MAINTXT`


`$MAINTXT` —  возвращает текст, выведенный в окно основного описания.

Данная функция может быть полезна для замены части текста в окне основного описания, либо иной обработке текста. Пример:

```qsp
! изначально мы вывели строку
*pl "Мы вывели на экран строку и в этой строке есть кусок, который мы хотим удалить."

! получаем текст из окна основного описания
$text = $maintxt
! вырезаем лишний кусок
$text_new = $replace($text, " и в этой строке есть кусок, который мы хотим удалить")
! очищаем окно основного описания
*clr
! выводим новый текст
*p $text_new
```

## `$MAX`


`MAX` —  возвращает максимальное из значений выражений-аргументов. Можно передавать от одного до двадцати значений/аргументов. Если передан один аргумент, то считается, что указано имя массива. Общая запись:

```qsp
MAX([#выражение 1], [#выражение 2], ... , [#выражение 20])
$MAX([$выражение 1], [$выражение 2], ... , [$выражение 20])

MAX([$название массива])
$MAX([$название массива])
```

Обратите внимание, при передаче одного аргумента поиск максимального элемента происходит среди строковых (если название массива указано со знаком `$`) или среди числовых значений элементов массива. Например:

```qsp
max('a') & ! вернёт максимальное из числовых значений элементов массива "a"
$max('$b') & ! вернёт максимальное из строковых значений элементов массива "b"
```

Нельзя писать так и надеяться, что произойдёт поиск среди значений массива `a`:

```qsp
max(a)
```

Можно так:

```qsp
$b = 'a'
max($b) & ! произойдёт поиск максимального значения среди элементов массива "a"
```

Другие примеры:

```qsp
max(1, 2, 5, 2, 0) &! вернёт 5
max(a, b, c) &! вернёт максимальное из значений переменных a,b,c
$max('aa', 'ab', 'zz') &! вернёт 'zz'
```

## `$MID`


`$MID` —  позволяет вырезать из строки её часть. Общая запись:

```qsp
$MID([$строка], [#начало], [#длина])
```

, где `[$строка]` — это строка текста, именно из неё функция вырезает часть, начиная с символа номер `[#начало]`, и длиной в `[#длина]` символов. Нумерация символов начинается с 1.
- Если отсутствует параметр `[#длина]`, вырезается часть до конца строки.
- Параметр `[#начало]` обязателен, и может в принципе принимать любые значения.
- Если значение `[#начало]` превышает длину строки, возвращается пустая строка.

```qsp
$mid('abcdef', 1, 2)    &    ! 'ab'
$mid('abcdef', 2, 3)    &    ! 'bcd'
$mid('abcdef', 2)    &    ! 'bcdef'
$mid('abcdef')        &    ! 'ошибка [120] — неверное число аргументов оператора/функции'
$mid('abcdef', 0)    &    ! 'abcdef'
$mid('abcdef', 8)    &    ! ''
```

## `$MIN`



`MIN` —  возвращает минимальное из значений выражений-аргументов. Можно передавать от одного до двадцати значений/аргументов. Если передан один аргумент, то считается, что указано имя массива. Общая запись:

```qsp
MIN([#выражение 1], [#выражение 2], ... , [#выражение 20])
$MIN([$выражение 1], [$выражение 2], ... , [$выражение 20])
```
```qsp
MIN([$название массива])
$MIN([$название массива])
```

Обратите внимание, при передаче одного аргумента поиск минимального элемента происходит среди строковых (если название массива указано со знаком `$`) или среди числовых значений элементов массива. Например:

```qsp 
min('a')    & ! вернёт минимальное из числовых значений элементов массива "a"
$min('$b')    & ! вернёт минимальное из строковых значений элементов массива "b"
```

Нельзя писать так:

```qsp
min(a)
```

Можно так:

```qsp
$b = 'a'
min($b) & ! произойдёт поиск максимального значения среди элементов массива "a"
```

Другие примеры:

```qsp
min(1, 2, 5, 2, 0)    &    ! вернёт 0
min(a, b, c)        &    ! вернёт минимальное из значений переменных a,b,c
$min('aa', 'ab', 'zz') & ! вернёт 'aa'
```

## `$QSPVER`


`$QSPVER` - возвращает версию интерпретатора в формате "X.Y.Z Player". Например, классический плеер версии 5.8.0. возвращает значение "5.8.0 (classic)", а qSpider просто "5.8.0". Пример использования:

```qsp
if $qspver < "5.8.0":
    *pl "Ваша версия плеера не подходит для этой игры."
    *pl "Установите плеер версии 5.8.0 или выше."
end
```

Так же данная функция может возвращать платформу, на которой запущена игра, если указать аргументом значение "platform":

```qsp
$qspver('platform')
```

## `$REPLACE`


`$REPLACE` —  общая запись:

```qsp
$REPLACE([$строка], [$поиск], [$замена])
```

Данная функция заменяет в строке `[$строка]` все вхождения строки `[$поиск]` строкой `[$замена]` и возвращает результат. Если `[$замена]` отсутствует или указана пустая строка, то удаляет в исходной строке все вхождения искомой строки. Примеры:

```qsp
$replace('test', '12', '4')    & ! выведет на экран 'test'
$replace('test', 'e', 's')    & ! выведет на экран 'tsst'
$replace('test', 't', '34')    & ! выведет на экран '34es34'
$replace('test', 't')        & ! выведет на экран 'es'
```

```qsp
! можно присвоить значение переменной
$text = "Строка текста с разными буквами."
! а новое значение вписать в другую переменную
$text_new = $replace($text, "ст", "st")
*pl $text
*pl $text_new
```

## `$SELACT`


`$SELACT` —  возвращает название выделенного действия в любом месте игры.

Следует помнить, что выделение действия происходит при наведении на него указателя мыши, а не при непосредственном нажатии.

Наиболее часто эту функцию используют, чтобы удалить текущее действие:

```qsp
act "Съесть яблоко":
    *pl "Это было очень вкусное яблоко. Жаль, что червивое."
    здоровье += 100
    delact $selact
end
```

Так же смотрите примеры использования в разделе [`$onactsel`](qsp-keyword-sys-var.md#onactsel)

## `$SELOBJ`


`$SELOBJ` —  возвращает название выделенного предмета в любом месте игры. Выделение предмета происходит в момент нажатия (щелчка мышью по предмету) и не снимается до применения команды `unselect`.

Пример использования можно посмотреть в разделе [`$onobjsel`](qsp-keyword-sys-var.md#onobjsel)

## `$STATTXT`


`$STATTXT` —  возвращает текст, выведенный в окно дополнительного описания. Может быть полезна для замены части текста в окне дополнительного описания.

Пример:
```qsp
p 'Вёз Корабль Карамель'
nl 'Наскочил Корабль На Мель'
$string = $stattxt
```

## `$STR`


`$STR` —  возвращает строку текста, полученную переводом числа в строку. Общая запись:

```qsp
$STR([#число])
```

Пример:

```qsp
$str(56) & ! превратит число 56 в строку "56" и выведет на экран
```

## `$STRFIND`


`$STRFIND` —  возвращает подстроку, соответствующую регулярному выражению, из указанной строки. Общая запись:

```qsp
$STRFIND([$строка], [$шаблон], [#номер])
```

, где `[$строка]` — исходная строка, в которой производим поиск вхождения, соответствующего регулярному выражению `[$шаблон]`, или группе номер `[#номер]` в регулярном выражении. Если подстрока с указанным номером отсутствует, то возвращается пустая строка. Нумерация групп подстрок начинается с 1. Если параметр `[#номер]` отсутствует, или равен 0, то возвращается подстрока, соответствующая всему регулярному выражению `[$шаблон]`.

Например, возьмём регулярное выражение:

```regex
^(\S+)\s(\S+)\s(\S+)$
```

Метасимвол `\S` означает любой непробельный символ, а квантификатор `+` указывает, что непробельные символы должны присутствовать один или более раз. Таким образом запись `\S+` можно условно сопоставить слову. Каждое слово с помощью скобок `()` выделено в отдельную группу, а между группами присутствуют пробельные символы `\s`. Метасимволы `^` и `$` означают соответственно начало и конец строки. Таким образом наше регулярное выражение соответствует любой строке из трёх слов, разделённых пробелами.

Тогда:

```qsp
! в этом случае строка не соответствует регулярному выражению
! потому что согласно регулярному выражению строка должна начинаться
! с группы непробельных символов. Команда вернёт пустую строку ''
$strfind(' идти к пещере','^(\S+)\s(\S+)\s(\S+)$')
```

```qsp
! в данном случае строка полностью соответствует регулярному выражению
! а значит команда вернёт строку полностью 'идти к пещере'
$strfind('идти к пещере','^(\S+)\s(\S+)\s(\S+)$') = ''
```

```qsp
! в следующих трёх примерах строка соответствует регулярному выражению
! однако третий аргумент указывает, какую именно группу из этого
! регулярного выражения мы хотим получить, поэтому каждая команда вернёт
! соответственно первое, второе и третье слова из строки
$strfind('идти к пещере','^(\S+)\s(\S+)\s(\S+)$', 1) & ! вернёт 'идти'
$strfind('идти к пещере','^(\S+)\s(\S+)\s(\S+)$', 2) & ! вернёт 'к'
$strfind('идти к пещере','^(\S+)\s(\S+)\s(\S+)$', 3) & ! вернёт 'пещере'
```

```qsp
! здесь последняя группа непробельных символов объединена в одну
! группу с последним пробельным символом. Квантификатор "?" указывает,
! что эта группа может как присутствовать в строке, так и отсутствовать:
$strfind('идти к пещере', '^(\S+)\s(\S+)(\s(\S+))?$', 4) & ! вернёт 'пещере'
$strfind('идти к пещере', '^(\S+)\s(\S+)(\s(\S+))?$', 3) & ! вернёт ' пещере'
! этому же регулярному выражению соответствует и такая строка
$strfind('искать ключ', '^(\S+)\s(\S+)(\s(\S+))?$', 1) & ! вернёт 'искать'
! а вот эта строка уже не соответствует регулярному выражению
$strfind('искать', '^(\S+)\s(\S+)(\s(\S+))?$', 1) & ! вернёт ''
```

Следующие примеры показывают, как `$strfind` возвращает часть строки, соответствующую регулярному выражению:

```qsp
$strfind('идти к дому', 'к\s(\S+)') & ! вернёт 'к дому'
$strfind('идти к дому', 'к\s(\S+)', 1) & ! вернёт 'дому'
$strfind('идти к своему дому', 'к\s(\S+)', 1) & ! вернёт 'своему'
```

Другие примеры:

```qsp title="слово из четырёх букв"
$strfind('идти к пещере', '\b\w{4}\b') &! на экране увидим 'идти'
```

```qsp title="Выборка с вложенными группами"
$strfind('+33-671-190-23-999', '\+\d{1,2}-(\d{3})((-\d+)+)', 1) &! на экране увидим '671' 
$strfind('+33-671-190-23-999', '\+\d{1,2}-(\d{3})((-\d+)+)', 2) &! на экране увидим '-190-23-999'
$strfind('+33-671-190-23-999', '\+\d{1,2}-(\d{3})((-\d+)+)', 3) &! на экране увидим '-999'
```

```qsp title="ищем числа в строке без чисел"
$strfind('Восемь зелёных яблок в корзине','\d+') &! на экране будет пустая строка
```

## `$TRIM`


`$TRIM` —  возвращает указанную строку без прилегающих символов табуляции и пробелов. Общая запись:

```qsp
$TRIM([$выражение])
```

Например:

```qsp
$trim('     trim test        ') & ! вернёт 'trim test'
```

## `$UCASE`


`$UCASE` —  возвращает строку больших букв, полученную изменением регистра букв исходной строки. Общая запись:

```qsp
$UCASE([$текст])
```

, где `[$текст]` — любая строка текста.

Примеры:

```qsp
$ucase('TExT#') & ! вернёт 'TEXT#'
$ucase('Привет, Алиса!') & ! вернёт 'ПРИВЕТ, АЛИСА!'
$ucase('Я хочу на вас орать.') & ! вернёт 'Я ХОЧУ НА ВАС ОРАТЬ.'
```

## `$USER_TEXT`


`$USER_TEXT` —  в любом месте игры возвращает текст, который находится в строке ввода (поле ввода). Имеет краткую форму `$usrtxt`.

Пример действия, по нажатию на которое в окно дополнительного описания будет выводиться текст, введённый в строку ввода:

```qsp
act "Что я написал?": pl 'Я написал: "<<$user_text>>".'
```

Более распространённый пример представлен в разделе [`$usercom`](qsp-keyword-sys-var.md#usercom).

## ARRCOMP


`ARRCOMP` —  возвращает индекс элемента массива, соответствующего регулярному выражению. Поиск начинается с элемента с заданным номером; индексация элементов массива ведётся с нуля. Если указанное значение не найдено, функция возвращает -1. Общая запись:

```qsp
ARRCOMP([$имя_массива], [$шаблон], [#начало])
```

, где `[#начало]` — номер элемента массива, с которого следует начать поиск, `[$имя_массива]` — название массива, по которому нужно произвести поиск, `[$шаблон]` — регулярное выражение, с которым будет сравниваться искомый элемент.

- Параметр `[#начало]` может отсутствовать, при этом его значение принимается равным 0.
- Поиск работает только по текстовым массивам (символ `$` в названии массива можно опустить).

Для примера возьмём вот такой массив:

```qsp
$mass[0] = "топаю вперёд"
$mass[1] = " иду в пещеру"
$mass[2] = "не иду в пещеру"
$mass[3] = "топаю к дому"
```

Нам нужно найти элемент, значение которого состоит из трёх слов. В грубом приближении слово — это набор из одного или более непробельных символов `\S+`, по бокам от которого могут стоять или не стоять символы пробела `\s`, отсюда мы можем составить вот такое регулярное выражение:

```regex
\s?\S+\s\S+\s\S+\s?
```

Остаётся только выяснить какой элемент массива соответсвует шаблону:

```qsp
arrcomp('$mass', '\s?\S+\s\S+\s\S+\s?') & ! этому выражению соответствует первый элемент
```

Если мы хотим проигнорировать первый элемент и начать поиск со второго:

```qsp
arrcomp('$mass', '\s?\S+\s\S+\s\S+\s?', 2) & ! этому выражению соответствует третий элемент
```

А вот так мы можем вывести на экран значения всех элементов, содержащих слово "иду":

```qsp
loop local pos, index = 0, 0 while 1:
    index = arrcomp('$mass', '(.*\s|^)иду(\s.*|$)', pos)
    if index <> -1:
        $mass[index]
        pos = index + 1
    else:
        jump 'break'
    end
end
:break
```

Другие примеры:

```qsp
! Поиск строки 'This' среди элементов массива "$A"
arrcomp('$A', 'This', 0)
! Поиск строки, соответствующей регулярному выражению "abc\d+"
! (первые два элемента массива игнорируются)
arrcomp('$A', 'abc\d+', 2)
! аналогично предыдущему примеру,
! но поиск осуществляется по всем элементам массива
arrcomp('$A', '.*string.*', 0) 
 
arrcomp('$A', 'This') & ! эквивалентно 1му варианту
```

:::warning[Внимание!]
Функция возвращает только числовой индекс элемента. Строковый или многомерный индекс с помощью данной функции получить нельзя.
:::

## ARRITEM

`ARRITEM` — возвращает значение элемента массива под указанным индексом. Общая запись:

```qsp
ARRITEM([$имя_массива], [индекс_элемента])
```

, где `[$имя_массива]` — это название массива, элемент которого мы хотим получить, а `[индекс_элемента]` — числовой, текстовый или многомерный индекс.

Иными словами функция извлекает значение из указанной ячейки массива. Примеры:

```qsp
! выводим значение элемента с индексом 3
*pl $arritem('$mass', 3)
! выводим значение элемента с текстовым индексом
*pl $arritem('$mass', 'Петя')
! выводим значение элемента с многомерным индексом
*pl $arritem('$mass', (-2, 9, 0))
```

Эта функция может быть полезна для извлечения значений, если имя массива заранее не известно. Пример:

```qsp title="Выводим содержимое нескольких массивов без использования DYNAMIC"
$array_name[] = 'mass_1'
$array_name[] = 'mass_2'
$array_name[] = 'mass_3'
$array_name[] = 'mass_4'
$array_name[] = 'mass_5'
! внешний цикл перебирает имена массивов
loop local j = 0 while j < arrsize('$array_name') step j += 1:
    ! внутренний цикл выводит содержимое массивов
    loop local i = 0 while i < arrsize($array_name[j]) step i += 1:
        *pl arritem($array_name[j], i)
    end
end
```

## ARRPOS


`ARRPOS` —   возвращает индекс элемента массива, равного указанному значению. Поиск начинается с элемента с заданным номером; индексация элементов массива ведётся с нуля. Если указанное значение не найдено, функция возвращает -1.

Общая запись:

```qsp
ARRPOS([$имя_массива], [значение], [#начало])
```

, где `[#начало]` — номер элемента массива, с которого следует начать поиск, `[$имя_массива]` — название массива, по которому нужно произвести поиск, `[значение]` — число, или строка (в зависимости от типа массива), которое нужно найти в массиве.

Для примера возьмём такой массив:

```qsp
$color[0] = 'красный'
$color[1] = 'жёлтый'
$color[2] = 'зелёный'
$color[3] = 'синий'
$color[4] = 'жёлтый'
```

Нам нужно найти элемент со значением "жёлтый":

```qsp
arrpos('$color', 'жёлтый') & ! вернёт значение 1
```

Если мы хотим проигнорировать первые два элемента:

```qsp
arrpos('$color', 'жёлтый', 2) & ! вернёт значение 4
```

Если мы хотим найти элемент со значением, которого нет в массиве:

```qsp
arrpos('$color','голубой') & ! вернёт значение -1
```

Другие примеры:

```qsp
! поиск строки 'this' в текстовом массиве "$a"
arrpos('$a', 'this', 0)
! поиск числа 65 в массиве "a" (два элемента массива игнорируются)
arrpos('a', 65, 2)
! поиск строки 'test' среди значений массива "$b"
arrpos('$b', 'test')
```

:::warning[Внимание!]
Функция возвращает только числовой индекс элемента. Строковый или многомерный индекс с помощью данной функции получить нельзя.
:::

:::note[5.7.0]
В более старых версиях плеера параметр `[#начало]` указывался первым:

```qsp
ARRPOS([#начало], [$имя_массива], [$шаблон])
```
:::

## ARRSIZE


`ARRSIZE` —  функция возвращает число элементов массива. Общая запись:

```qsp
ARRSIZE([$имя_массива])
```

, где `[$имя_массива]` — название массива, размер которого хотим получить.

Не имеет значения, указываете ли вы **`$`** перед названием массива или нет. Подсчитывается общее число ячеек и со строковыми, и с числовыми значениями. Для примера:

```qsp
n = ARRSIZE('a')
n = ARRSIZE('$a')
! Результат будет одинаковый
```

## COUNTOBJ


`COUNTOBJ` —  возвращает количество предметов в инвентаре.

Номер последнего предмета в списке численно совпадает с количеством предметов, поэтому всегда можно получить название последнего предмета так:

```qsp
$getobj(countobj)
```

## INSTR


`INSTR` —  возвращает номер символа, с которого начинается вхождение подстроки в строку. Общая запись:

```qsp
INSTR([$строка], [$подстрока], [#начало])
```

, где `[#начало]` — это номер символа, с которого нужно начинать поиск, `[$строка]` — это текстовое значение (строка), по которому нужно производить поиск, а `[$подстрока]` — значение, которое мы ищем в указанной строке. Нумерация символов начинается с `1`. Параметр `[#начало]` может отсутствовать, при этом он принимается равным `1`.

Примеры:

```qsp
instr('abcdefabcdef', 'bc', 3)    & ! вернёт число 8
instr('abcdefghijklm', 'abc')    & ! вернёт число 1
```

Если ни одного вхождения указанной подстроки в строке нет, `instr` возвращает `0`.

Пример:

```qsp
instr('Вася вышел из дома.', 'идти') & ! вернёт 0
```

:::note[5.7.0]
В более старых версиях плеера параметр `[#начало]` указывался первым:

```qsp
INSTR([#начало], [$строка], [$подстрока])
```
:::

## ISNUM


`ISNUM` —  функция возвращает `1` (истина), если переданная строка является числом, и  — `0`, если строка не является числом. Общая запись:

```qsp
ISNUM([$строка])
```

, где `[$строка]` — любая строка текста.

При проверке учитываются знак `-` в начале, прилегающие пробелы и символы табуляции, но кроме того, если хотя бы один символ окажется не цифрой, функция вернёт `0` (ложь).

Примеры:

```qsp
isnum(' 9999 ') & ! вернёт 1
isnum(' -888')  & ! вернёт 1
isnum('777a6')  & ! вернёт 0
isnum('')       & ! вернёт 0, т.к. пустая строка не содержит числа
```

## ISPLAY


`ISPLAY` —  функция проверяет, проигрывается ли в данный момент файл с указанным названием, и если проигрывается, возвращает `1`. В противном случае функция возвращает `0`. Общая запись:

```qsp
ISPLAY([$путь_к_файлу])
```

, где `[$путь_к_файлу]` — путь к звуковому файлу относительно файла игры.

Пример:

```qsp
if isplay('music/mountsound.mp3'):
    *pl 'Проигрывается музыка.'
else:
    *pl 'Музыка не проигрывается.'
end
```

## LEN


`LEN` —  возвращает длину указанной строки текста (количество символов). Общая запись:

```qsp
LEN([$текст])
```

, где `[$текст]` — любое текстовое значение.

Примеры:

```qsp
len("abc") & ! вернёт значение 3
len("тысячадевятьсотвосьмидесятидевятимиллиметровый") & ! вернёт значение 46
len("") & ! вернёт значение 0
```

## MSECSCOUNT


`MSECSCOUNT` —  возвращает количество миллисекунд, прошедших с момента начала игры. Данная функция при использовании на локации-счётчике позволяет организовывать различные события, происходящие в реальном времени. Так же, с помощью этой функции можно делать замеры быстродействия различных участков кода в вашей игре:

```qsp        
i = 0
old_time = msecscount
:for
if i < 100000:
    d[i] = i
    i += 1
    jump 'for'
end
new_time = msecscount
pl "Скорость работы старого цикла: " + $str(new_time - old_time)
 
old_time = msecscount
loop i = 0 while i < 100000 step i += 1:
    b[i] = i
end
new_time = msecscount
pl "Скорость работы нового цикла: " + $str(new_time - old_time)
```

:::note
Максимальное число, которое может вернуть данная функция, это `2147483647`. Не трудно посчитать, что этого хватит более, чем на **550** часов игры.
:::

## RAND


`RAND` —  возвращает случайное число между двумя указанными числами. Общая запись:

```qsp
RAND([#выражение 1], [#выражение 2])
```

, где `[#выражение 1]` и `[#выражение 2]` — два любых числа или числовых выражения. Параметр `[#выражение 2]` может отсутствовать, при этом он принимается равным `1`.

:::note[5.7.0]
В более старых версиях плеера, данный параметр по умолчанию равен нулю.
:::

Примеры:

```qsp
rand(1, 4) &! вернёт случайное значение от 1 до 4
rand(4, 1) &! вернёт случайное значение от 1 до 4
rand(1000) &! вернёт случайное значение от 1 до 1000
rand 1000 &! вернёт случайное значение от 1 до 1000
```

## RGB


`RGB` —  возвращает числовой код цвета на основе трёх числовых аргумнтов, каждый из которых соответствует составляющей требуемого цвета. Общая запись:

```qsp
RGB([#красный], [#зелёный], [#синий], [#альфа])
```

, где `[#красный]`,`[#зелёный]` и `[#синий]` — числовое выражение трёх составляющих цвета соответственно красной, зелёной и синей; `[#альфа]` — составляющая прозрачности; должны принимать значения от 0 до 255.

Данная функция обычно используется совместно с системными переменными `bcolor`, `fcolor`, `lcolor`. Пример:

```qsp
! гиперссылки светло-жёлтого цвета
lcolor = rgb(255, 255, 100)
! фон тёмно-серого цвета
bcolor = rgb(25, 25, 25)
! текст светло-зелёного цвета
fcolor = rgb(100, 255, 100)
```

Пример полупрозрачного цвета ссылок:

```qsp
lcolor = rgb(0, 255, 255, 128)
```
## RND


`RND` - возвращает случайное значение от `1` до `1000`. Аналогично команде:

```qsp
rand(1, 1000)
```

## STRCOMP


`STRCOMP` —  проводит сравнение строки с регулярным выражением и, если строка соответствует регулярному выражению, возвращает `1` (истина), а если не соответствует — `0` (ложь). Общая запись:

```qsp
STRCOMP([$строка], [$шаблон])
```

, где `[$строка]` — любое текстовое значение, `[$шаблон]` — регулярное выражение, с которым производится сравнение.

Например, нам нужно проверить, состоит ли указанная строка из трёх слов. Каждое слово, в грубом виде, это набор непробельных символов, значит мы можем воспользоваться метасимволом `\S` и квантификатором `+`. Слова обычно разделены пробельными символами, для чего мы используем метасимвол `\s`. Получается вот такое регулярное выражение:

```regex
\s?\S+\s+\S+\s+\S+\s?
```

Теперь мы можем проверить, какие строки соответствуют этому регулярному выражению:

```qsp
strcomp('иду по дороге', '\s?\S+\s+\S+\s+\S+\s?') & ! вернёт 1
strcomp(' иду домой', '\s?\S+\s+\S+\s+\S+\s?') & ! вернёт 0
strcomp(' иду в лес ', '\s?\S+\s+\S+\s+\S+\s?') & ! вернёт 1
strcomp('однословие', '\s?\S+\s+\S+\s+\S+\s?') & ! вернёт 0
```

## STRPOS


`STRPOS` —  возвращает позицию символа, с которого начинается вхождение подстроки, соответствующей регулярному выражению, в указанную строку. Общая запись:

```qsp
STRPOS([$строка], [$шаблон], [#номер])
```

, где `[$строка]` — исходная строка, в которой производим поиск вхождения, соответствующего регулярному выражению `[$шаблон]`, или группе номер `[#номер]` в регулярном выражении. Нумерация групп в регулярном выражении начинается с 1. Если подстрока с указанным номером отсутствует, то возвращается `0`.

Если параметр `[#номер]` отсутствует или равен `0`, то возвращается позиция символа, с которого начинается вхождение подстроки, соответствующей всему регулярному выражению.

Например, нам нужно выяснить, в какой части текста встречается словосочетание "зелёное яблоко", однако при этом не должно быть важно, в каком падеже записано это прилагательное.

Чтобы написать регулярное выражение для этой задачи, нам нужно предусмотреть все падежи:

```
зелёное яблоко
зелёного яблока
зелёному яблоку
зелёное яблоко
зелёным яблоком
зелёном яблоке
```

Как видим, во всех формах меняются только окончания слов. Поэтому мы можем составить вот такое регулярное выражение:

```regex
зелён(ое|ого|ому|ым|ом)\s+яблок(о|а|у|ом|е)
```

Через прямую черту в скобках перечисленны возможные варианты окончаний. А теперь выясним, с какого символа в строке начинается возможное слвовосочетание "зелёное яблоко":

```qsp
! для удобства регулярное выражение помещаем в переменную
$regexp = "зелён(ое|ого|ому|ым|ом)\s+яблок(о|а|у|ом|е)"
strpos("У меня есть зелёное яблоко", $regexp) & ! вернёт 13
strpos("Ты швырнул в него зелёным яблоком!", $regexp) & ! вернёт 19
strpos("полный ящик зелёных яблок", $regexp) & ! вернёт 0, потому что такую форму мы не учли
```

Если мы не просто хотим узнать, с какого символа начинается вхождение в строку словосочетания, а конкретно где начинается вхождение слова "яблоко" из этого словосочетания, нам нужно выделить слово "яблоко" с вариантами окончаний в отдельную группу и воспользоваться параметром `[#номер]`:

```qsp
$regexp = "зелён(ое|ого|ому|ым|ом)\s+(яблок(о|а|у|ом|е))"
strpos("У меня есть зелёное яблоко", $regexp, 2) & ! вернёт 21
strpos("Ты швырнул в него зелёным яблоком!", $regexp, 2) & ! вернёт 27
strpos("полный ящик зелёных яблок", $regexp, 2) & ! вернёт 0, потому что мы не учли форму
```

Другие примеры:

```qsp title="Работа с группами"
!------'----5--8------15--'
STRPOS('+33-671-190-23-999', '\+\d{1,2}-(\d{3})((-\d+)+)',1) &! на экране увидим 5
STRPOS('+33-671-190-23-999', '\+\d{1,2}-(\d{3})((-\d+)+)',2) &! на экране увидим 8
STRPOS('+33-671-190-23-999', '\+\d{1,2}-(\d{3})((-\d+)+)',3) &! на экране увидим 15
```

```qsp title="Поиск числа в строке без числа"
STRPOS('Восемь зелёных яблок в корзине','\d+') &! на экране будет 0
```

```qsp
STRPOS('идти к пещере', '^(\S+)\s(\S+)\s(\S+)$', 0) &! 1
STRPOS(' идти к пещере', '^(\S+)\s(\S+)\s(\S+)$', 0) &! 0
STRPOS('идти к пещере', '^(\S+)\s(\S+)\s(\S+)$', 1)  &! 1
STRPOS('идти к пещере', '^(\S+)\s(\S+)\s(\S+)$', 2)  &! 6
STRPOS('идти к пещере', '^(\S+)\s(\S+)\s(\S+)$', 3)  &! 8
STRPOS('идти к пещере', '^(\S+)\s(\S+)(\s(\S+))?$', 4) &! 8
STRPOS('идти к дому', 'к\s(\S+)', 0) &! 6
STRPOS('идти к дому', 'к\s(\S+)')    &! 6
STRPOS('идти к дому', 'к\s(\S+)', 1) &! 8
STRPOS('идти к своему дому', 'к\s(\S+)', 1) &! 8
```

## VAL


`VAL` —  переводит указанную строку цифр в соответствующее число. Общая запись:

```qsp
VAL([$выражение])
```

, где `[$выражение]` — любая строка текста.

При проверке учитываются знак `-` в начале, прилегающие пробелы и символы табуляции, но кроме того, если хотя бы один символ окажется не цифрой, функция вернёт `0`. Так же если `[$выражение]` равно `''` (пустая строка), то возвращается `0`.

Примеры:

```qsp
яблоки = val($яблоки)

val('123') & ! увидим 123
val('') & ! увидим 0
val('sand') & ! увидим 0
```