---
sidebar_position: 3
---

# Functions

## `$CURACTS`

`$CURACTS` — this function returns actions displayed on screen as QSP code, as a text value.

Actions are saved as a set of `act` operators with corresponding parameters and operations.

By writing the value returned by the function to a variable, actions can be restored using the `dynamic` operator. Example:

```qsp
! write current actions to variable
$actlist = $curacts
! restore actions from variable
dynamic $actlist
```

## `$CURLOC`

`$CURLOC` — function returns the name of the current location, i.e., the location where the player "is".

Technically, this should be understood as follows. When the game starts, the player begins executing code of the very first location in the game, and when the code is executed, the player "stops" and waits for player participation. The player can press various buttons in the game, links and select menu items, which leads to execution of other code blocks (for example, actions) and transitions to new locations via `goto` or `xgoto`. During such transitions, the player again executes code of other locations and, when code is executed, "stops".

So, when a direct transition to a location is made (i.e., via `goto` or `xgoto`, or it's the very first location in the game), `$curloc` begins returning the name of this location, — throughout the time while code is executing and when the player "stops". If no transition via `goto`/`xgoto` occurs after stopping, the value returned by `$curloc` doesn't change.

Usage example:

```qsp
*pl $curloc & ! output current location name to Main Description Window
*pl "Times re-entered: <<re_entered>>"
act "Re-enter current location":
    re_entered += 1
    goto $curloc
end
```

## `$CUROBJS`

`$CUROBJS` - this function returns the list of objects displayed on screen as QSP code.
Objects are saved as a set of `ADDOBJ` operators with corresponding parameters and operations.

By writing the value returned by the function to a variable, objects can be restored using the `DYNAMIC` operator. Example:

```qsp
! save object list as QSP code:
$old_objects = $CUROBJS
! remove all objects from objects window:
KILLOBJ
! restore all objects in objects window:
DYNAMIC $old_objects
```

## `$DESC`

`$DESC` — returns the base description text of a location with the specified name. General syntax:

```qsp
$DESC([$location])
```

, where `[$location]` — the name of the location we're interested in. For example:

```qsp
! return base description of location "cupboard_under_stairs"
$desc('cupboard_under_stairs')
!return base description of current location
$desc($curloc)
```

If sub-expressions are present in the base description, the function automatically expands them.

:::warning[Pay attention!]
The function returns text written only in the "Description" field (**Base description**) of the **Quest Generator** editor. When working in a text editor, this field is unavailable to you and the function will always return an empty string.
:::

## `$DYNEVAL`

`DYNEVAL` — executes code passed as a text string and returns the result if it exists. General syntax:

```qsp
$DYNEVAL([$code], [argument 0], [argument 1], ... , [argument 18])
DYNEVAL([$code], [argument 0], [argument 1], ... , [argument 18])
```

, where `[$code]` — regular QSP code written as text. Executing such code is analogous to executing `FUNC` function code. Arguments `[argument 0]`, `[argument 1]`, etc. can be used inside `[$code]`, their values are automatically placed in variables `args[0]`, `args[1]`, etc. respectively.

Inside the code executed by `dyneval`, its own `ARGS` array is used, its values don't intersect with `ARGS` values at the location from which `dyneval` was called.

After executing the code passed to the `dyneval` function, calculation of the expression in which `dyneval` is located continues.

For `dyneval` to return a result, you need to assign this result to the `result` variable inside `[$code]`.

Examples:

```qsp
dyneval('result = 3 + 4')
*pl $dyneval('$result = mid("abcd", 2, 1) + "qwerty"')
pass = dyneval("result = ($args[0] <> 'text')", 'string')
```

- For `DYNEVAL` to return multiple values, the result must be written to `%RESULT`.
- For `DYNEVAL` to return a string value, the result must be written to `$RESULT`.
- For `DYNEVAL` to return a numeric value, the result must be written to `RESULT`.
- `%RESULT`, `$RESULT` and `RESULT` are the same variable but with different data types. Remember that a new value assignment overwrites the previous one, regardless of the data type of that value.

If `dyneval` doesn't return values during execution (`result` is not initialized), and is the only element of an expression passed to the implicit operator, the player will output nothing to screen. I.e., `dyneval` will work like `DYNAMIC`. Example:

```qsp
! implicit operator will output 123 to screen:
123
! code in dyneval will execute, but we won't see
! anything on screen:
dyneval("code = 123 + 890")
! implicit operator will output 1013 to screen:
code
```

See also [operator `DYNAMIC`](qsp-keyword-operators.md#dynamic).

## `$FUNC`

`FUNC` — executes code of the specified location without direct transition to it with value return.

General syntax:

```qsp
FUNC([$location], [argument 0], [argument 1], ... , [argument 18])
$FUNC([$location], [argument 0], [argument 1], ... , [argument 18])
```

, where `[$location]` — the name of the location whose code we want to execute without direct transition to it. Arguments `[argument 0]`, `[argument 1]`, etc. can be used at this location, their values are automatically placed in variables `args[0]`, `args[1]`, etc. respectively.

For `FUNC` to return:

- multiple values or a tuple, at the specified location you need to assign the result to variable `%RESULT`;
- a string result, at this location you need to assign this result to variable `$RESULT`;
- for returning a numeric result, it must be assigned to variable `RESULT`.

Remember that `%RESULT`, `$RESULT` and `RESULT` are the same variable but of different types, so if you defined both `%RESULT`, `$RESULT`, and `RESULT` at the location, the function will return the value that was written to this variable last.

If no value was assigned to the `RESULT` variable, the function returns nothing. And here there are two player behavior variants.

- If the `FUNC` function is in some expression, the default value will be substituted instead of the function (empty tuple, empty string, or zero depending on the expression type).
- If the `FUNC` function stands right after the implicit operator, such operator will be ignored, and nothing will be output to screen. Example:

```qsp title="location_N"
N = 23 * 13
! no value is assigned to result variable
```

```qsp title="Other location"
'string 1'
func('location_N') &! nothing will be output to screen
'string 2'
56 + func('location_N') &! function is in expression. Its value = 0
```

:::note[Recommendation:]
It's not mandatory, but recommended, to use the type prefix (`$` or `%`) with the `FUNC` keyword if the function should return a string value or tuple, and — without type prefix if the function should return a numeric value:

```qsp
$func('string_slice', 'We left the house when lights went out in all windows.', 3, 7)
func('raise_to_power', 3, 3)
```

:::

**Order of operation.**

When calling the specified location using `FUNC`, the following happens:

- The player interrupts execution of current code (for example, current location code) and calls the specified location.
- Base description and action list of the specified location are added to the description and actions of the current location.
- Code from the **Execute on visit** field is executed
- Then the player returns to executing the code it interrupted. I.e., to calculating the expression in which this function stands.

Separate unique `ARGS` and `RESULT` arrays are automatically created at each location, so values in these arrays will be separate for each location. After executing the location code called by `FUNC`, the `ARGS` and `RESULT` arrays of this location are destroyed.

Other examples:

```qsp
!Processing location "function" as function.
!ARGS array is empty.
apples = FUNC('function')

!processing location with name in variable $name as function. ARGS[0] equals 1.
pl func($name, 1) * 78

!processing location with name in $name as function.
!$ARGS[0] contains string "string", ARGS[1] equals 2.
msg "text" + func($name, "string", 2)
```

```qsp
! location code for function getting sum of series of numbers from one to specified value
# summ
! args[0] will contain the number we specify as [argument 0]
loop while args[0]>0 step args[0] -= 1:
    result += args[0]
end
---summ---

! example of calling location "summ" as function
*pl func("summ", 19) & ! will output 190 to screen
! example of call with location name written to variable
$name_loc = "summ"
*pl func($name_loc, 23) & ! will output 276 to screen
```

Also see ["Implicit `FUNC` function call"](qsp-keyword-syntaxems#commercial-at-symbol-).

## `$GETOBJ`

`$GETOBJ` — returns the name of an item in the *Objects Window* located at the specified position. General syntax:

```qsp
$GETOBJ([#item_number])
```

Indexing (numbering) of items in the *Objects Window* starts from 1. If an item with index `[#item_number]` doesn't exist, an empty string (`''`) is returned.

Examples:

```qsp
$getobj(1) & ! returns name of first item in backpack

$getobj(countobj) & ! returns name of last added item
```

Code counting the number of items with identical names in the `OBJECTS` array:

```qsp
loop local i = 1 while i <= countobj step i += 1:
    objects[$getobj(i)] += 1
end
```

## `$QSPVER`

`$QSPVER` - returns the interpreter version in the format "X.Y.Z Player". For example, classic player version 5.8.0 returns the value "5.8.0 (classic)", and qSpider simply "5.8.0". Usage example:

```qsp
if $qspver < "5.8.0":
    *pl "Your player version is not suitable for this game."
    *pl "Install player version 5.8.0 or higher."
end
```

This function can also return the platform on which the game is running if you specify "platform" as an argument:

```qsp
$qspver('platform')
```

:::note[5.7.0]

In older player versions, the function returned only the interpreter version (libqsp library).

:::

## `$SELACT`

`$SELACT` — returns the name of the selected action anywhere in the game.

Remember that action selection occurs when hovering the mouse pointer over it, not when directly clicking.

Most often this function is used to remove the current action:

```qsp
act "Eat apple":
    *pl "It was a very tasty apple. Too bad it was wormy."
    health += 100
    delact $selact
end
```

Also see usage examples in the [`$onactsel`](qsp-keyword-sys-var.md#onactsel) section

## `$SELOBJ`

`$SELOBJ` — returns the name of the selected object anywhere in the game. Object selection occurs when clicking (mouse click on object) and is not removed until the `unselect` command is applied.

Usage examples can be found in the [`$onobjsel`](qsp-keyword-sys-var.md#onobjsel) section

## `$STATTXT`

`$STATTXT` — returns text output to the additional description window. Can be useful for replacing part of text in the additional description window.

Example:

```qsp
p 'The Ship Carried Caramel'
nl 'The Ship Hit a Shoal'
$string = $stattxt
```

## `$USER_TEXT`

`$USER_TEXT` — anywhere in the game returns text that is in the input line (input field). Has the short form `$usrtxt`.

Example of an action that will output text entered in the input line to the additional description window when clicked:

```qsp
act "What did I write?": pl 'I wrote: "<<$user_text>>".'
```

A more common example is presented in the [`$usercom`](qsp-keyword-sys-var.md#usercom) section.

## COUNTOBJ

`COUNTOBJ` — returns the number of items in inventory.

The number of the last item in the list numerically matches the number of items, so you can always get the name of the last item like this:

```qsp
$getobj(countobj)
```

## MSECSCOUNT

`MSECSCOUNT` — returns the number of milliseconds elapsed since the game started. This function, when used at the counter location, allows organizing various events occurring in real time. Also, with this function you can measure performance of various code sections in your game:

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
pl "Old loop performance: " + $str(new_time - old_time)

old_time = msecscount
loop i = 0 while i < 100000 step i += 1:
    b[i] = i
end
new_time = msecscount
pl "New loop performance: " + $str(new_time - old_time)
```

:::note
The maximum number this function can return is `2147483647`. It's not hard to calculate that this is enough for more than **550** hours of gameplay.
:::

## RND

`RND` - returns a random value from `1` to `1000`. Analogous to the command:

```qsp
rand(1, 1000)
```

## `$IIF`

`IIF` — returns a value depending on expression truth.

General syntax:

```qsp
IIF([#expression], [#expression_yes], [#expression_no])
$IIF([#expression], [$expression_yes], [$expression_no])
```

If `[#expression]` is true, returns the value of expression `[expression_yes]`, otherwise returns the value of expression `[expression_no]`.

Only one of the expressions `[expression_yes]` and `[expression_no]` will be calculated, depending on whether the condition is met.

Examples:

```qsp
!Absolute value of number
abs_x = iif(x>0, x, -x)

!And the following construct will NOT cause division by zero error:
x = 0
y  = iif(x = 0, 0, 1/x)

! typical solution for outputting time so as not to lose zero on hours:
$iif(hour>9, $str(hour), "0"+$str(hour)) + ":"+$iif(minute>9, $str(minute), "0"+$str(minute))
```

Equivalence of conditional constructs with `IF` operator and `IIF` function:

```qsp
if number mod 2 = 0:
    *pl "Number is even"
else
    *pl "Number is odd"
end
! equivalent to
*pl $iif(number mod 2 = 0,"Number is even","Number is odd")
```

## `$INPUT`

`$INPUT` — returns to the interpreter the text entered by the player, or `''` (empty string) if the "Cancel" button was pressed. General syntax:

```qsp
$INPUT([$text])
```

, where `[$text]` — the prompt in the dialog box that the player sees. For example:

```qsp
$name = $input('What is your name, hero?')
```

When this command is executed, a dialog box with the text "What is your name, hero?" will appear on screen, and execution of the rest of the code will pause until the player interacts with the dialog box.

The player can enter or not enter text, and press the "OK" or "Cancel" button. If the player entered text and pressed the "OK" button, the `$input` function will return the text entered by the player to the `$text` variable. In all other cases, after closing the dialog box, the function will return an empty string (`''`).

Other examples:

```qsp
! Question with one correct answer.
if $input('What comes after darkness?') = 'light':
    msg 'Correct.'
else
    msg 'Wrong answer.'
end

! Example implementation of question with multiple answer variants where any will be correct.
$answer = $trim($lcase($input('Answer')))
if instr($answer, 'red') or instr($answer, 'yellow') or instr($answer, 'green'): gt 'win'
! Entering red or green or yellow will transition to 'win' location
```

:::warning[Be careful!]
It's acceptable but not approved to use the function for returning numeric values:

```qsp
INPUT([$prompt])
```

This can lead to various game errors if the player enters not only digits in the dialog box. For example:

```qsp
age = input('How old are you?')
```

If the player enters the string "24 years old" instead of a number, the player will give error **101** "Data type mismatch".

Such situations should be anticipated by the game author, which means it's correct to check the entered value after the `$input` function is executed.

```qsp
loop local $text while 1:
    ! ask player to answer question
    ! and assign entered text to variable
    $text = $input('How old are you?')
    ! if entered text contains not only digits
    ! or player didn't enter answer
    if isnum($text) and $text <> "":
        ! player entered number
        age = val($text) & ! set age
        jump 'break' & ! break loop
    else
        ! player entered nothing or incorrect value
        ! loop continues
    end
end
:break
```

:::

## `$LCASE`

`$LCASE` — returns a lowercase string obtained by changing the case of letters in the original string. General syntax:

```qsp
$LCASE([$text])
```

, where `[$text]` — any text string.

Examples:

```qsp
$lcase('TExT#') & ! returns 'text#'
$lcase('Hello, Alice!') & ! returns 'hello, alice!'
$lcase('I DON\'T WANT TO SHOUT AT YOU.') & ! returns 'i don\'t want to shout at you.'
```

## `$MAINTXT`

`$MAINTXT` — returns text output to the main description window.

This function can be useful for replacing part of text in the main description window, or other text processing. Example:

```qsp
! initially we output a string
*pl "We output a string to screen and in this string there's a piece we want to remove."

! get text from main description window
$text = $maintxt
! cut out extra piece
$text_new = $replace($text, " and in this string there's a piece we want to remove")
! clear main description window
*clr
! output new text
*p $text_new
```

## `$MID`

`$MID` — allows cutting a part from a string. General syntax:

```qsp
$MID([$string], [#start], [#length])
```

, where `[$string]` — text string from which the function cuts a part, starting from character number `[#start]`, and with length of `[#length]` characters. Character numbering starts from 1.

- If the `[#length]` parameter is absent, the part is cut to the end of the string.
- The `[#start]` parameter is mandatory and can take any values.
- If the `[#start]` value exceeds the string length, an empty string is returned.

```qsp
$mid('abcdef', 1, 2)    &    ! 'ab'
$mid('abcdef', 2, 3)    &    ! 'bcd'
$mid('abcdef', 2)    &    ! 'bcdef'
$mid('abcdef')        &    ! 'error [120] — incorrect number of operator/function arguments'
$mid('abcdef', 0)    &    ! 'abcdef'
$mid('abcdef', 8)    &    ! ''
```

## `$REPLACE`

`$REPLACE` — general syntax:

```qsp
$REPLACE([$string], [$search], [$replacement], [#num_replacements])
```

This function replaces several occurrences of string `[$search]` with string `[$replacement]` in string `[$string]` and returns the result. Replacement is performed left-to-right and only for non-overlapping occurrences. The `[#num_replacements]` parameter shows how many occurrences should be replaced. If the parameter is not specified, all occurrences are replaced. If `[$replacement]` is absent or an empty string is specified, then all occurrences of the searched string are removed from the original string. Examples:

```qsp
$replace('test', '12', '4')    & ! will output 'test' to screen
$replace('test', 'e', 's')    & ! will output 'tsst' to screen
$replace('test', 't', '34')    & ! will output '34es34' to screen
$replace('test', 't')        & ! will output 'es' to screen

$replace('test', 't', 'qu', 1) &! 'quest'
$replace('test my test', 't', 'q', 3) &! 'qesq my qest'
```

```qsp
! you can assign value to variable
$text = "Text string with different letters."
! and write new value to another variable
$text_new = $replace($text, "st", "st")
*pl $text
*pl $text_new
```

## `$STR`

`$STR` — returns a text string obtained by converting a number to string. General syntax:

```qsp
$STR([#number])
```

Example:

```qsp
$str(56) & ! converts number 56 to string "56" and outputs to screen
```

## `$STRFIND`

`$STRFIND` — returns a substring matching a regular expression from the specified string. General syntax:

```qsp
$STRFIND([$string], [$pattern], [#number])
```

, where `[$string]` — source string in which we search for an occurrence matching regular expression `[$pattern]`, or group number `[#number]` in the regular expression. If substring with specified number is absent, an empty string is returned. Group numbering starts from 1. If parameter `[#number]` is absent or equals 0, the substring matching the entire regular expression `[$pattern]` is returned.

For example, let's take the regular expression:

```regex
^(\S+)\s(\S+)\s(\S+)$
```

The `\S` metacharacter means any non-whitespace character, and the `+` quantifier indicates that non-whitespace characters must be present one or more times. Thus the notation `\S+` can be conditionally matched to a word. Each word is enclosed in separate groups using parentheses `()`, and whitespace characters `\s` are present between groups. The `^` and `## `$IIF`

`IIF` — returns a value depending on expression truth.

General syntax:

```qsp
IIF([#expression], [#expression_yes], [#expression_no])
$IIF([#expression], [$expression_yes], [$expression_no])
```

If `[#expression]` is true, returns the value of expression `[expression_yes]`, otherwise returns the value of expression `[expression_no]`.

Only one of the expressions `[expression_yes]` and `[expression_no]` will be calculated, depending on whether the condition is met.

Examples:

```qsp
!Absolute value of number
abs_x = iif(x>0, x, -x)

!And the following construct will NOT cause division by zero error:
x = 0
y  = iif(x = 0, 0, 1/x)

! typical solution for outputting time so as not to lose zero on hours:
$iif(hour>9, $str(hour), "0"+$str(hour)) + ":"+$iif(minute>9, $str(minute), "0"+$str(minute))
```

Equivalence of conditional constructs with `IF` operator and `IIF` function:

```qsp
if number mod 2 = 0:
    *pl "Number is even"
else
    *pl "Number is odd"
end
! equivalent to
*pl $iif(number mod 2 = 0,"Number is even","Number is odd")
```

 metacharacters mean the beginning and end of string respectively. Thus our regular expression matches any string of three words separated by spaces.

Then:

```qsp
! in this case the string doesn't match the regular expression
! because according to the regular expression the string should start
! with a group of non-whitespace characters. The command will return empty string ''
$strfind(' go to cave','^(\S+)\s(\S+)\s(\S+))
```

```qsp
! in this case the string fully matches the regular expression
! so the command will return the string entirely 'go to cave'
$strfind('go to cave','^(\S+)\s(\S+)\s(\S+)) = ''
```

```qsp
! in the next three examples the string matches the regular expression
! but the third argument specifies which group from this
! regular expression we want to get, so each command will return
! the first, second and third words from the string respectively
$strfind('go to cave','^(\S+)\s(\S+)\s(\S+), 1) & ! returns 'go'
$strfind('go to cave','^(\S+)\s(\S+)\s(\S+), 2) & ! returns 'to'
$strfind('go to cave','^(\S+)\s(\S+)\s(\S+), 3) & ! returns 'cave'
```

```qsp
! here the last group of non-whitespace characters is combined into one
! group with the last whitespace character. The "?" quantifier indicates
! that this group may or may not be present in the string:
$strfind('go to cave', '^(\S+)\s(\S+)(\s(\S+))?, 4) & ! returns 'cave'
$strfind('go to cave', '^(\S+)\s(\S+)(\s(\S+))?, 3) & ! returns ' cave'
! this regular expression also matches this string
$strfind('search key', '^(\S+)\s(\S+)(\s(\S+))?, 1) & ! returns 'search'
! but this string no longer matches the regular expression
$strfind('search', '^(\S+)\s(\S+)(\s(\S+))?, 1) & ! returns ''
```

The following examples show how `$strfind` returns part of string matching the regular expression:

```qsp
$strfind('go to house', 'to\s(\S+)') & ! returns 'to house'
$strfind('go to house', 'to\s(\S+)', 1) & ! returns 'house'
$strfind('go to my house', 'to\s(\S+)', 1) & ! returns 'my'
```

Other examples:

```qsp title="four-letter word"
$strfind('go to cave', '\b\w{4}\b') &! we'll see 'cave' on screen
```

```qsp title="Selection with nested groups"
$strfind('+33-671-190-23-999', '\+\d{1,2}-(\d{3})((-\d+)+)', 1) &! we'll see '671' on screen
$strfind('+33-671-190-23-999', '\+\d{1,2}-(\d{3})((-\d+)+)', 2) &! we'll see '-190-23-999' on screen
$strfind('+33-671-190-23-999', '\+\d{1,2}-(\d{3})((-\d+)+)', 3) &! we'll see '-999' on screen
```

```qsp title="searching for numbers in string without numbers"
$strfind('Eight green apples in basket','\d+') &! empty string will be on screen
```

## `$TRIM`

`$TRIM` — returns the specified string without adjacent tab and space characters. General syntax:

```qsp
$TRIM([$expression])
```

For example:

```qsp
$trim('     trim test        ') & ! returns 'trim test'
```

## `$UCASE`

`$UCASE` — returns an uppercase string obtained by changing the case of letters in the original string. General syntax:

```qsp
$UCASE([$text])
```

, where `[$text]` — any text string.

Examples:

```qsp
$ucase('TExT#') & ! returns 'TEXT#'
$ucase('Hello, Alice!') & ! returns 'HELLO, ALICE!'
$ucase('I want to shout at you.') & ! returns 'I WANT TO SHOUT AT YOU.'
```

## INSTR

`INSTR` — returns the character number from which the substring occurrence begins in the string. General syntax:

```qsp
INSTR([$string], [$substring], [#start])
```

, where `[#start]` — the character number from which to start the search, `[$string]` — text value (string) in which to search, and `[$substring]` — value we're looking for in the specified string. Character numbering starts from `1`. The `[#start]` parameter can be absent, in which case it's taken as 1.

Examples:

```qsp
instr('abcdefabcdef', 'bc', 3)    & ! returns number 8
instr('abcdefghijklm', 'abc')    & ! returns number 1
```

If no occurrence of the specified substring is found in the string, `instr` returns `0`.

Example:

```qsp
instr('Vasya left the house.', 'go') & ! returns 0
```

:::note[5.7.0]
In older player versions, the `[#start]` parameter was specified first:

```qsp
INSTR([#start], [$string], [$substring])
```

:::

## ISNUM

`ISNUM` — function returns `1` (true) if the passed string is a number, and `0` if the string is not a number. General syntax:

```qsp
ISNUM([$string])
```

, where `[$string]` — any text string.

The check takes into account the `-` sign at the beginning, adjacent spaces and tab characters, but if at least one character turns out not to be a digit, the function will return `0` (false).

Examples:

```qsp
isnum(' 9999 ') & ! returns 1
isnum(' -888')  & ! returns 1
isnum('777a6')  & ! returns 0
isnum('')       & ! returns 0, since empty string contains no number
```

## ISPLAY

`ISPLAY` — function checks if a file with the specified name is currently playing, and if it is, returns `1`. Otherwise the function returns `0`. General syntax:

```qsp
ISPLAY([$file_path])
```

, where `[$file_path]` — path to sound file relative to game file.

Example:

```qsp
if isplay('music/mountsound.mp3'):
    *pl 'Music is playing.'
else
    *pl 'Music is not playing.'
end
```

## LEN

`LEN` — returns the length of the specified text string (number of characters). General syntax:

```qsp
LEN([$text])
```

, where `[$text]` — any text value.

Examples:

```qsp
len("abc") & ! returns value 3
len("thousand-nine-hundred-eighty-nine-millimeter") & ! returns value 46
len("") & ! returns value 0
```

## STRCOMP

`STRCOMP` — compares a string with a regular expression and, if the string matches the regular expression, returns `1` (true), and if it doesn't match — `0` (false). General syntax:

```qsp
STRCOMP([$string], [$pattern])
```

, where `[$string]` — any text value, `[$pattern]` — regular expression to compare with.

For example, we need to check if the specified string consists of three words. Each word, roughly speaking, is a set of non-whitespace characters, so we can use the `\S` metacharacter with the `+` quantifier. Words are usually separated by whitespace characters, for which we use the `\s` metacharacter. We get this regular expression:

```regex
\s?\S+\s+\S+\s+\S+\s?
```

Now we can check which strings match this regular expression:

```qsp
strcomp('go along road', '\s?\S+\s+\S+\s+\S+\s?') & ! returns 1
strcomp(' go home', '\s?\S+\s+\S+\s+\S+\s?') & ! returns 0
strcomp(' go to forest ', '\s?\S+\s+\S+\s+\S+\s?') & ! returns 1
strcomp('oneword', '\s?\S+\s+\S+\s+\S+\s?') & ! returns 0
```

## STRPOS

`STRPOS` — returns the position of the character from which the substring occurrence matching the regular expression begins in the specified string. General syntax:

```qsp
STRPOS([$string], [$pattern], [#number])
```

, where `[$string]` — source string in which we search for an occurrence matching regular expression `[$pattern]`, or group number `[#number]` in the regular expression. Group numbering in regular expression starts from 1. If substring with specified number is absent, `0` is returned.

If parameter `[#number]` is absent or equals `0`, the position of the character from which the substring occurrence matching the entire regular expression begins is returned.

For example, we need to find out in which part of the text the phrase "green apple" occurs, but the case of this adjective shouldn't matter.

To write a regular expression for this task, we need to account for all cases:

```plain
green apple
green apple
green apple
green apple
green apple
green apple
```

As we can see, only word endings change in all forms. Therefore we can compose this regular expression:

```regex
green(oe|ogo|omu|ym|om)\s+apple(o|a|u|om|e)
```

Possible ending variants are listed through a vertical bar in parentheses. And now let's find out from which character in the string the possible phrase "green apple" begins:

```qsp
! for convenience we put the regular expression in a variable
$regexp = "green(oe|ogo|omu|ym|om)\s+apple(o|a|u|om|e)"
strpos("I have a green apple", $regexp) & ! returns 13
strpos("You threw a green apple at him!", $regexp) & ! returns 19
strpos("full box of green apples", $regexp) & ! returns 0, because we didn't account for this form
```

If we don't just want to know from which character the phrase occurrence begins in the string, but specifically where the word "apple" from this phrase begins, we need to put the word "apple" with ending variants in a separate group and use the `[#number]` parameter:

```qsp
$regexp = "green(oe|ogo|omu|ym|om)\s+(apple(o|a|u|om|e))"
strpos("I have a green apple", $regexp, 2) & ! returns 21
strpos("You threw a green apple at him!", $regexp, 2) & ! returns 27
strpos("full box of green apples", $regexp, 2) & ! returns 0, because we didn't account for the form
```

Other examples:

```qsp title="Working with groups"
!------'----5--8------15--'
STRPOS('+33-671-190-23-999', '\+\d{1,2}-(\d{3})((-\d+)+)',1) &! we'll see 5 on screen
STRPOS('+33-671-190-23-999', '\+\d{1,2}-(\d{3})((-\d+)+)',2) &! we'll see 8 on screen
STRPOS('+33-671-190-23-999', '\+\d{1,2}-(\d{3})((-\d+)+)',3) &! we'll see 15 on screen
```

```qsp title="Searching for number in string without number"
STRPOS('Eight green apples in basket','\d+') &! 0 will be on screen
```

```qsp
STRPOS('go to cave', '^(\S+)\s(\S+)\s(\S+), 0) &! 1
STRPOS(' go to cave', '^(\S+)\s(\S+)\s(\S+), 0) &! 0
STRPOS('go to cave', '^(\S+)\s(\S+)\s(\S+), 1)  &! 1
STRPOS('go to cave', '^(\S+)\s(\S+)\s(\S+), 2)  &! 6
STRPOS('go to cave', '^(\S+)\s(\S+)\s(\S+), 3)  &! 8
STRPOS('go to cave', '^(\S+)\s(\S+)(\s(\S+))?, 4) &! 8
STRPOS('go to house', 'to\s(\S+)', 0) &! 6
STRPOS('go to house', 'to\s(\S+)')    &! 6
STRPOS('go to house', 'to\s(\S+)', 1) &! 8
STRPOS('go to my house', 'to\s(\S+)', 1) &! 8
```

## VAL

`VAL` — converts the specified digit string to corresponding number. General syntax:

```qsp
VAL([$expression])
```

, where `[$expression]` — any text string.

The check takes into account the `-` sign at the beginning, adjacent spaces and tab characters, but if at least one character turns out not to be a digit, the function will return `0`. Also if `[$expression]` equals `''` (empty string), `0` is returned.

Examples:

```qsp
apples = val($apples)

val('123') & ! we'll see 123
val('') & ! we'll see 0
val('sand') & ! we'll see 0
```

## `$MAX`

`MAX` — returns the maximum of expression-argument values. You can pass from one to twenty values/arguments. If one argument is passed, it's considered that an array name is specified. General syntax:

```qsp
MAX([#expression 1], [#expression 2], ... , [#expression 20])
$MAX([$expression 1], [$expression 2], ... , [$expression 20])

MAX([$array_name])
$MAX([$array_name])
```

Note, when passing one argument, the search for maximum element occurs among string (if array name is specified with `$` sign) or among numeric values of array elements. For example:

```qsp
max('a') & ! returns maximum of numeric values of "a" array elements
$max('$b') & ! returns maximum of string values of "b" array elements
```

You can't write like this and expect search among array `a` values:

```qsp
max(a)
```

You can do this:

```qsp
$b = 'a'
max($b) & ! search for maximum value among elements of "a" array will occur
```

Other examples:

```qsp
max(1, 2, 5, 2, 0) &! returns 5
max(a, b, c) &! returns maximum of variable values a,b,c
$max('aa', 'ab', 'zz') &! returns 'zz'
```

## `$MIN`

`MIN` — returns the minimum of expression-argument values. You can pass from one to twenty values/arguments. If one argument is passed, it's considered that an array name is specified. General syntax:

```qsp
MIN([#expression 1], [#expression 2], ... , [#expression 20])
$MIN([$expression 1], [$expression 2], ... , [$expression 20])
```

```qsp
MIN([$array_name])
$MIN([$array_name])
```

Note, when passing one argument, the search for minimum element occurs among string (if array name is specified with `$` sign) or among numeric values of array elements. For example:

```qsp
min('a')    & ! returns minimum of numeric values of "a" array elements
$min('$b')    & ! returns minimum of string values of "b" array elements
```

You can't write like this:

```qsp
min(a)
```

You can do this:

```qsp
$b = 'a'
min($b) & ! search for maximum value among elements of "a" array will occur
```

Other examples:

```qsp
min(1, 2, 5, 2, 0)    &    ! returns 0
min(a, b, c)        &    ! returns minimum of variable values a,b,c
$min('aa', 'ab', 'zz') & ! returns 'aa'
```

## RAND

`RAND` — returns a random number between two specified numbers. General syntax:

```qsp
RAND([#expression 1], [#expression 2], [#mode])
```

, where `[#expression 1]` and `[#expression 2]` — any two numbers or numeric expressions.

The `[#mode]` parameter allows specifying a number that should occur more frequently than others. The frequency distribution will smoothly change for all other numbers, decreasing from mode to the limits of the selected interval. If the 3rd parameter is not specified, the function returns a random number in the specified range with uniform/equiprobable number distribution.

The `[#expression 2]` parameter can be absent, in which case it's taken as `1`.

:::note[5.7.0]
In older player versions, this parameter defaults to zero.
:::

Examples:

```qsp
rand(1, 4) &! returns random value from 1 to 4
rand(4, 1) &! returns random value from 1 to 4
rand(1000) &! returns random value from 1 to 1000
rand 1000 &! returns random value from 1 to 1000

x = RAND(1, 1000, 500) & ! 500 will occur more often
x = RAND(1, 1000, 1) & ! 1 will occur more often
x = RAND(1, 1000, 1000) & ! 1000 will occur more often
x = RAND(-1000, 0, -500) & ! -500 will occur more often
x = RAND(1, 1000, 5000) & ! 1000 will occur more often
x = RAND(-1000, -100, -5000) & ! -1000 will occur more often
```

## RGB

`RGB` — returns the numeric color code based on three numeric arguments, each corresponding to a component of the required color. General syntax:

```qsp
RGB([#red], [#green], [#blue], [#alpha])
```

, where `[#red]`, `[#green]` and `[#blue]` — numeric expression of three color components respectively red, green and blue; `[#alpha]` — transparency component; should take values from 0 to 255.

This function is usually used together with system variables `bcolor`, `fcolor`, `lcolor`. Example:

```qsp
! light yellow hyperlinks
lcolor = rgb(255, 255, 100)
! dark gray background
bcolor = rgb(25, 25, 25)
! light green text
fcolor = rgb(100, 255, 100)
```

Example of semi-transparent link color:

```qsp
lcolor = rgb(0, 255, 255, 128)
```

:::note[Note.]

Don't rely on the `[#alpha]` parameter as many players don't support it.

:::

## ARRCOMP

`ARRCOMP` — returns the index of array element matching a regular expression. Search starts from element with specified number; array element indexing starts from zero. If the specified value is not found, the function returns -1. General syntax:

```qsp
ARRCOMP([$array_name], [$pattern], [#start])
```

, where `[#start]` — array element number from which to start search, `[$array_name]` — array name to search in, `[$pattern]` — regular expression to compare the searched element with.

- The `[#start]` parameter can be absent, in which case its value is taken as 0.
- Search works only on text arrays (the `$` symbol in array name can be omitted).

For example, let's take this array:

```qsp
$mass[0] = "stomp forward"
$mass[1] = " go to cave"
$mass[2] = "don't go to cave"
$mass[3] = "stomp to house"
```

We need to find an element whose value consists of three words. Roughly speaking, a word is a set of one or more non-whitespace characters `\S+`, which can be surrounded by whitespace characters `\s`, so we can compose this regular expression:

```regex
\s?\S+\s\S+\s\S+\s?
```

Now we just need to find out which array element matches the pattern:

```qsp
arrcomp('$mass', '\s?\S+\s\S+\s\S+\s?') & ! the first element matches this expression
```

If we want to ignore the first element and start search from the second:

```qsp
arrcomp('$mass', '\s?\S+\s\S+\s\S+\s?', 2) & ! the third element matches this expression
```

And this is how we can output all element values containing the word "go":

```qsp
loop local pos, index = 0, 0 while 1:
    index = arrcomp('$mass', '(.*\s|^)go(\s.*|$)', pos)
    if index <> -1:
        $mass[index]
        pos = index + 1
    else:
        jump 'break'
    end
end
:break
```

Other examples:

```qsp
! Search for string 'This' among elements of array "$A"
arrcomp('$A', 'This', 0)
! Search for string matching regular expression "abc\d+"
! (first two array elements are ignored)
arrcomp('$A', 'abc\d+', 2)
! similar to previous example,
! but search is performed on all array elements
arrcomp('$A', '.*string.*', 0)

arrcomp('$A', 'This') & ! equivalent to 1st variant
```

:::warning[Attention!]
The function returns only the numeric index of the element. String or multi-dimensional index cannot be obtained with this function.
:::

## ARRITEM

`ARRITEM` — returns the value of array element at specified index. General syntax:

```qsp
ARRITEM([$array_name], [element_index])
```

, where `[$array_name]` — the name of the array whose element we want to get, and `[element_index]` — numeric, text, or multi-dimensional index.

In other words, the function extracts a value from the specified array cell. Examples:

```qsp
! output value of element with index 3
*pl $arritem('$mass', 3)
! output value of element with text index
*pl $arritem('$mass', 'Pete')
! output value of element with multi-dimensional index
*pl $arritem('$mass', [-2, 9, 0])
```

This function can be useful for extracting values when the array name is not known in advance. Example:

```qsp title="Output contents of several arrays without using DYNAMIC"
$array_name[] = 'mass_1'
$array_name[] = 'mass_2'
$array_name[] = 'mass_3'
$array_name[] = 'mass_4'
$array_name[] = 'mass_5'
! outer loop iterates through array names
loop local j = 0 while j < arrsize('$array_name') step j += 1:
    ! inner loop outputs array contents
    loop local i = 0 while i < arrsize($array_name[j]) step i += 1:
        *pl arritem($array_name[j], i)
    end
end
```

## %ARRPACK

`ARRPACK` — returns a tuple into which values from the specified array are packed.

General syntax:

```qsp
%ARRPACK([$array_name], [#start_index], [#count])
```

, where `[#start_index]` - the number of array element `[$array_name]` from which to start selecting elements for packing; `[#count]` — the number of elements to be packed into the tuple.

This function allows shortening the command for extracting arguments from `args`:

```qsp
! instead of:
local type, name = args[0], args[1]
! you can write like this:
local type, name = arrpack('args')
```

It can also be convenient if you need to quickly view array contents or part of it:

```qsp
! view values in array without using loop:
*pl %arrpack('massive', 11, 10) & ! we'll see ten elements starting from 11th, as a tuple on screen
```

## ARRPOS

`ARRPOS` — returns the index of array element equal to specified value. Search starts from element with specified number; array element indexing starts from zero. If the specified value is not found, the function returns -1.

General syntax:

```qsp
ARRPOS([$array_name], [value], [#start])
```

, where `[#start]` — array element number from which to start search, `[$array_name]` — array name to search in, `[value]` — number or string (depending on array type) to find in the array.

For example, let's take this array:

```qsp
$color[0] = 'red'
$color[1] = 'yellow'
$color[2] = 'green'
$color[3] = 'blue'
$color[4] = 'yellow'
```

We need to find element with value "yellow":

```qsp
arrpos('$color', 'yellow') & ! returns value 1
```

If we want to ignore the first two elements:

```qsp
arrpos('$color', 'yellow', 2) & ! returns value 4
```

If we want to find element with value that doesn't exist in the array:

```qsp
arrpos('$color','light blue') & ! returns value -1
```

Other examples:

```qsp
! search for string 'this' in text array "$a"
arrpos('$a', 'this', 0)
! search for number 65 in array "a" (two array elements are ignored)
arrpos('a', 65, 2)
! search for string 'test' among values of array "$b"
arrpos('$b', 'test')
```

:::warning[Attention!]
The function returns only the numeric index of the element. String or multi-dimensional index cannot be obtained with this function.
:::

:::note[5.7.0]
In older player versions, the `[#start]` parameter was specified first:

```qsp
ARRPOS([#start], [$array_name], [$pattern])
```

:::

## ARRTYPE

`ARRTYPE` — returns the type of value stored in a variable or specified array cell. The type is returned as one of the following values:
- `''` (empty string) — value not defined (for example, for uninitialized variables);
- `'#'` — variable contains number;
- `'` — variable contains string;
- `'%'` — variable contains tuple.

General syntax:

```qsp
ARRTYPE([$array_name], [index])
```

, where `[$array_name]` — array name (type prefix doesn't matter, better not to specify); `[index]` — cell index whose value type we want to get.

Examples:

```qsp
$ddd = 'text'
arrtype('ddd') & ! '

$g = 'text' & g = 13
arrtype('g') & ! '#'

%tuple['index'] = [12, 'string']
arrtype('tuple', 'index') & ! '%'

! $empty not exist
arrtype('$empty') & ! ''
```

## ARRSIZE

`ARRSIZE` — function returns the number of array elements. General syntax:

```qsp
ARRSIZE([$array_name])
```

, where `[$array_name]` — the name of the array whose size we want to get.

It doesn't matter whether you specify **`## `$MAX`

`MAX` — returns the maximum of expression-argument values. You can pass from one to twenty values/arguments. If one argument is passed, it's considered that an array name is specified. General syntax:

```qsp
MAX([#expression 1], [#expression 2], ... , [#expression 20])
$MAX([$expression 1], [$expression 2], ... , [$expression 20])

MAX([$array_name])
$MAX([$array_name])
```

Note, when passing one argument, the search for maximum element occurs among string (if array name is specified with `$` sign) or among numeric values of array elements. For example:

```qsp
max('a') & ! returns maximum of numeric values of "a" array elements
$max('$b') & ! returns maximum of string values of "b" array elements
```

You can't write like this and expect search among array `a` values:

```qsp
max(a)
```

You can do this:

```qsp
$b = 'a'
max($b) & ! search for maximum value among elements of "a" array will occur
```

Other examples:

```qsp
max(1, 2, 5, 2, 0) &! returns 5
max(a, b, c) &! returns maximum of variable values a,b,c
$max('aa', 'ab', 'zz') &! returns 'zz'
```

## `$MIN`

`MIN` — returns the minimum of expression-argument values. You can pass from one to twenty values/arguments. If one argument is passed, it's considered that an array name is specified. General syntax:

```qsp
MIN([#expression 1], [#expression 2], ... , [#expression 20])
$MIN([$expression 1], [$expression 2], ... , [$expression 20])
```

```qsp
MIN([$array_name])
$MIN([$array_name])
```

Note, when passing one argument, the search for minimum element occurs among string (if array name is specified with `$` sign) or among numeric values of array elements. For example:

```qsp
min('a')    & ! returns minimum of numeric values of "a" array elements
$min('$b')    & ! returns minimum of string values of "b" array elements
```

You can't write like this:

```qsp
min(a)
```

You can do this:

```qsp
$b = 'a'
min($b) & ! search for maximum value among elements of "a" array will occur
```

Other examples:

```qsp
min(1, 2, 5, 2, 0)    &    ! returns 0
min(a, b, c)        &    ! returns minimum of variable values a,b,c
$min('aa', 'ab', 'zz') & ! returns 'aa'
```

## RAND

`RAND` — returns a random number between two specified numbers. General syntax:

```qsp
RAND([#expression 1], [#expression 2], [#mode])
```

, where `[#expression 1]` and `[#expression 2]` — any two numbers or numeric expressions.

The `[#mode]` parameter allows specifying a number that should occur more frequently than others. The frequency distribution will smoothly change for all other numbers, decreasing from mode to the limits of the selected interval. If the 3rd parameter is not specified, the function returns a random number in the specified range with uniform/equiprobable number distribution.

The `[#expression 2]` parameter can be absent, in which case it's taken as `1`.

:::note[5.7.0]
In older player versions, this parameter defaults to zero.
:::

Examples:

```qsp
rand(1, 4) &! returns random value from 1 to 4
rand(4, 1) &! returns random value from 1 to 4
rand(1000) &! returns random value from 1 to 1000
rand 1000 &! returns random value from 1 to 1000

x = RAND(1, 1000, 500) & ! 500 will occur more often
x = RAND(1, 1000, 1) & ! 1 will occur more often
x = RAND(1, 1000, 1000) & ! 1000 will occur more often
x = RAND(-1000, 0, -500) & ! -500 will occur more often
x = RAND(1, 1000, 5000) & ! 1000 will occur more often
x = RAND(-1000, -100, -5000) & ! -1000 will occur more often
```

## RGB

`RGB` — returns the numeric color code based on three numeric arguments, each corresponding to a component of the required color. General syntax:

```qsp
RGB([#red], [#green], [#blue], [#alpha])
```

, where `[#red]`, `[#green]` and `[#blue]` — numeric expression of three color components respectively red, green and blue; `[#alpha]` — transparency component; should take values from 0 to 255.

This function is usually used together with system variables `bcolor`, `fcolor`, `lcolor`. Example:

```qsp
! light yellow hyperlinks
lcolor = rgb(255, 255, 100)
! dark gray background
bcolor = rgb(25, 25, 25)
! light green text
fcolor = rgb(100, 255, 100)
```

Example of semi-transparent link color:

```qsp
lcolor = rgb(0, 255, 255, 128)
```

:::note[Note.]

Don't rely on the `[#alpha]` parameter as many players don't support it.

:::

## ARRCOMP

`ARRCOMP` — returns the index of array element matching a regular expression. Search starts from element with specified number; array element indexing starts from zero. If the specified value is not found, the function returns -1. General syntax:

```qsp
ARRCOMP([$array_name], [$pattern], [#start])
```

, where `[#start]` — array element number from which to start search, `[$array_name]` — array name to search in, `[$pattern]` — regular expression to compare the searched element with.

- The `[#start]` parameter can be absent, in which case its value is taken as 0.
- Search works only on text arrays (the `$` symbol in array name can be omitted).

For example, let's take this array:

```qsp
$mass[0] = "stomp forward"
$mass[1] = " go to cave"
$mass[2] = "don't go to cave"
$mass[3] = "stomp to house"
```

We need to find an element whose value consists of three words. Roughly speaking, a word is a set of one or more non-whitespace characters `\S+`, which can be surrounded by whitespace characters `\s`, so we can compose this regular expression:

```regex
\s?\S+\s\S+\s\S+\s?
```

Now we just need to find out which array element matches the pattern:

```qsp
arrcomp('$mass', '\s?\S+\s\S+\s\S+\s?') & ! the first element matches this expression
```

If we want to ignore the first element and start search from the second:

```qsp
arrcomp('$mass', '\s?\S+\s\S+\s\S+\s?', 2) & ! the third element matches this expression
```

** before the array name or not. The total number of cells with both string and numeric values is counted. For example:

```qsp
n = ARRSIZE('a')
n = ARRSIZE('$a')
! The result will be the same
```

:::warning[Attention!]

If an array was declared using the `LOCAL` operator, but no value was assigned to any array element, `ARRSIZE` of such array will return `0`.

:::