---
id: qsp-keyword-operators
title: Operators
sidebar_position: 2
---

# Operators

## Implicit Operator

The implicit operator is an operator that is not written in QSP code but produces output of values to the screen. It is implied everywhere where an expression without an operator is present in a command. The implicit operator outputs values to the **Main Description Window** in the same way as if you used the explicit `*pl` operator, i.e., it outputs the value and makes a line break. Examples:

```qsp
$AAA + '989'
'You are in the park'
'Preformatted

    string'
$curloc & ! will output the location name to the screen
```

Unlike the `*pl` operator, the implicit operator does not output an empty string with a line break to the screen if no value is passed to it. This means that if a function returns no value, the implicit operator is simply ignored. Example:

```qsp
# start
! this is location code calling a function location
$curloc
$func('foo')
$func('foo')
$curloc
- start

# foo
! this is function location code
local i = 0
- foo
```

In this case, the `foo` function location returns nothing, so we will see two lines with the word "start" on the screen, with no empty lines between them, since the implicit operator in the lines with `$func` on the `start` location will simply be ignored. Compare with:

```qsp
# start
! this is location code calling a function location
*pl $curloc
*pl $func('foo')
*pl $func('foo')
*pl $curloc
- start

# foo
! this is function location code
local i=0
- foo
```

## `!` (comment)

`!` — comment operator. What is in the line after the comment operator and until the end of the line is ignored by the interpreter. The comment operator allows you to "comment out" (disable) an unnecessary operator/function temporarily during game debugging. Additionally, writing comments to program code is one of the signs of good programming style.

It's important to clearly understand that this is exactly an operator, so if you're commenting some line of code, the `!` should come after `&`:

```qsp
*pl "Hello, world!" & ! comment
```

Comments can be single-line, i.e., ending on the same line where the comment operator is:

```qsp
! single-line comment
*pl "text string" & ! also a single-line comment
```

:::tip[Exception]
The only exception to this rule is writing a comment after a colon in multi-line operators:

```qsp
act "Multi-line action": ! comment
    *pl "Text on screen"
end
```

:::

Comments can be multi-line. For this, after the comment operator, you need to write quotes, apostrophes, or curly braces. For example:

```qsp
! "this is the first line of the comment
    this is the second line of the comment
    this is the third line of the comment
"
```

Multi-line comments can take various forms:

```qsp
! line before quotes " text inside quotes
can go to other lines " as well as {
you can use other groups of symbols to
continue the multi-line comment
} and the comment won't end until the line ends
```

## `*CLEAR`

`*CLEAR` — clears the main description window. Has the short form `*clr`.

## `*NL`

`*NL` — line break, then text output in the main description window. General syntax:

```qsp
*NL [$text]
```

, where `[$text]` — any text string, number, or expression of any type. If `[$text]` is absent, just a line break occurs. Example:

```qsp
*p "Text without line break."
*nl "Line break + text output."
*p "Text without line break."
```

## `*P`

`*P` — text output to the main description window without line break. Text output by any other operator immediately after `*p` will add new text right after the current one. General syntax:

```qsp
*P [$text]
```

, where `[$text]` — any text string, number, or expression of any type. `[$text]` can be an empty string `''`, but must not be absent. Example:

```qsp
*p "Text without line break."
*p "Text without line break."
*p ""
*p "Text without line break."
```

## `*PL`

`*PL` — text output to the main description window, then line break. General syntax:

```qsp
*PL [$text]
```

where `[$text]` — any text string, number, or expression of any type. `[$text]` can be absent, then just a line break. Example:

```qsp
*pl "Output text, then line break."
*pl "Output text, then line break."
*p "Text without line break."
*pl "Output text, then line break."
```

Similarly, you can output text by simply writing the desired expression instead of this operator. For example, the lines:

```qsp
*pl $AAA + '989'
*pl 'You are in the park'
*pl 'Preformatted

    string'
```

and:

```qsp
$AAA + '989'
'You are in the park'
'Preformatted

    string'
```

will work identically.

## ACT

`ACT` — creates and outputs a new action to the actions window.

General syntax in single-line form:

```qsp
ACT [$name], [$image_path]: [operator] & [operator] & [operator]
```

General syntax in multi-line form:

```qsp
ACT [$name], [$image_path]:
    [operator]
    [operator]
    [operator]
END
```

A new action with the name `[$name]` and image located at `[$image_path]` is added to the actions list in the actions window. When the action is clicked, the specified operators are executed.

The `[$image_path]` parameter can be absent, in which case the action is added without an image.

Examples:

```qsp
! action in single-line form
act "Pick apple from birch": apple += 1 & *pl "You picked an apple, ripe and white."

! action in multi-line form, with image
act "Pick watermelon from bush", "img/watermelon.png":
    watermelon += 1
    *pl "You picked a watermelon from the bush"
end
```

If there is already an action with the specified name in the actions list, no new action is created, and it doesn't replace the existing one; the player simply ignores the `act` command. Thus, you cannot output actions with identical names. Example:

```qsp
act "Action 1": *pl "Old action."
act "Action 1": *pl "New action."
```

However, you can simulate actions with identical names in HTML recognition mode by adding HTML tags to action names:

```qsp
usehtml = 1
act 'Action 1<a data-avs="uid-old"></a>': *pl "Old action."
act 'Action 1<a data-avs="uid-new"></a>': *pl "New action."
```
## ADDOBJ

`ADDOBJ` — adding a new item to the objects window. General syntax:

```qsp
ADDOBJ [$name], [$image_path], [#position]
```

, where `[$name]` — the item name, `[$image_path]` — the path to the item's image file (displayed next to the item name), and `[#position]` — what position in the inventory the item is added to. The `[#position]` parameter can be absent. By default, items are added to the end of the list. Item numbering in the inventory starts from `1`. The `[$image_path]` parameter can be absent, default value is `''`, in which case the item is added without an image.

:::note[Deprecated but acceptable legacy form:]

```qsp
ADD OBJ [$name],[$image_path],[#index]
```

:::

You can add items with the same name, however, if you plan to add many identical items, it's better to use an additional variable to count these items and add one item to the objects window to avoid cluttering the inventory with a list of 137 Ruble / Bullet items:

```qsp
if obj('Bullets'):
! if the "Bullets" item is already added, just increase their number
    bullets += 10
else
! if the "Bullets" item is not yet added, add it and increase the number
    addobj 'Bullets'
    bullets += 10
end
```

For storing the number of items, you can use arrays indexed by strings:

```qsp
objects['money'] = 12
objects['bullets'] = 137
'Quantity: <<objects[$getobj(countobj)]>>'
```

Example of adding an item to the very top of the list (all other items will shift down):

```qsp
addobj "Screwdriver", "", 1
```

## CLA

`CLA` - clears the current actions list (removes all actions from the actions window).

## CLEAR

`CLEAR` — clears the additional description window. Has the short form `clr`.

## CLOSE

`CLOSE` — stops playing the specified sound file. General syntax:

```qsp
CLOSE [$sound_file_path]
```

, where `[$sound_file_path]` — path to the sound file relative to the game file. If the `[$sound_file_path]` parameter is not specified, all sound files stop playing.

## CLOSE ALL

`CLOSE ALL` — stops playing all active sound files. Has the short form `close`.

## CLS

`CLS` — clears all windows except the objects list. Equivalent to:

```qsp
clear & *clear & cla & cmdclear
```

## CMDCLEAR

`CMDCLEAR` — clears the input line. Has the short form `cmdclr`.

## COPYARR

`COPYARR` — copies the contents of one array to another. General syntax:

```qsp
COPYARR [$destination], [$source], [#start], [#count]
```

, where: `[$destination]` — the array to copy to, size and content don't matter; `[$source]` — the array to copy from; `[#start]` — the element number to start copying from; `[#count]` — how many elements to copy. The `[#count]` parameter is optional; default is until the end of the source array. The `[#start]` parameter is optional; default is 0.

Examples:

```qsp
! copy all elements of array '$b' to array '$a'
copyarr '$a', '$b'
! also copied all elements of array 'b' to array 'a'

! copy elements of array 'd' to array 'c', starting from the sixth
copyarr 'c', 'd', 6

! copy the first six elements of array 'd' to array 'c'
copyarr 'c', 'd', 0, 6
```

Due to player specifics, when copying, for example, numeric array `mass1` to `mass2`, the text array `$mass1` is also copied to `$mass2`.

Other examples:

```qsp
copyarr $arrname1, $arrname2, 10, 5
copyarr 'a<<$arrname1>>', 'a<<$arrname2>>'
```

## DELACT

`DELACT` — removes an action from the actions list (if such an action exists). General syntax:

```qsp
DELACT [$name]
```

, where `[$name]` — the name of the action to remove.

Examples:

```qsp
! remove action with specific name
delact 'Go forward'
! remove selected action
delact $selact
```

:::note[Deprecated but acceptable legacy form:]

```qsp
DEL ACT [$name]
```

:::

## DELOBJ

`DELOBJ` — removes an item from inventory by name (if such an item exists). General syntax:

```qsp
DELOBJ [$name]
```

, where `[$name]` — the name of the item to remove.

If there are identical items in the inventory, the command will remove the topmost one with the specified index.

Examples:

```qsp
! remove item with specific name
delobj "Screwdriver"
! remove selected item
delobj $selobj
```

:::note[Deprecated but acceptable legacy form:]

```qsp
DEL OBJ [$name]
```

:::

## DYNAMIC

`DYNAMIC` — executes code passed as a text string. General syntax:

```qsp
    DYNAMIC([$code], [argument 0], [argument 1], ... , [argument 18])
```

, where `[$code]` — regular QSP code written as text. Executing such code is analogous to executing `GOSUB` operator code. Arguments `[argument 0]`, `[argument 1]`, etc. can be used inside `[$code]`, their values are automatically placed in variables `args[0]`, `args[1]`, etc. respectively. After execution, old `args` parameters are restored, then code execution continues from the next command after `dynamic`.

Examples:

```qsp
dynamic '$a = "string<<$b>>"'
dynamic '$a'
dynamic 'if $a = "string": "text!"'
dynamic "
    $args[0]
    addobj $args[1]
", 'Text', 'Fork'
```

The following information is also valid for the [`dyneval`](qsp-keyword-functions.md#dyneval) function.

**Important!** If code is specified using apostrophes (`''`) or quotes (`""`), sub-expressions are calculated in the text:

```qsp
$args[0] = 'qwerty'
$code = '
    *pl "<<$args[0]>>"
    *pl $args[0]
'

dynamic $code, 'asdfg'
```

In this case, when setting the `$code` variable, the sub-expression will be calculated, so 'qwerty' will be output on the first line, and 'asdfg' on the second line.

Curly braces are the third type of quotes used specifically for writing dynamic code. Here, bracket nesting is supported, and sub-expressions are not calculated before code execution:

```qsp
$args[0]='qwerty'
$code = {
    *pl "<<$args[0]>>"
    *pl $args[0]
}

dynamic $code, 'asdfg'
```

In this case, two lines 'asdfg' will be output.

## EXIT

`EXIT` — terminates execution of the current code block (premature exit from a subroutine, function, event handler, etc.).

A code block can be a location, action, code passed to `dynamic` or `dyneval`, or code in a hyperlink.

Example:

```qsp
if args[1] = 0:
    exit
else
    if args[0] mod args[1] = 0:
        result = 1
    else
        result = 0
    end
end
```

:::warning[Attention!!!]
In players version 5.8.0, the `loop` cycle operator appeared.

The loop body is also considered a separate code block, however, the `exit` operator interrupts not only the loop itself but also the code block in which the loop is located.
:::

## FREELIB

`FREELIB` — removes all locations added with the `inclib` operator.

:::note[5.7.0]
In older player versions, the command was called `dellib` and `killqst`.
:::

## GOSUB

`GOSUB` — executes code of the specified location without direct transition to it.

General syntax:

```qsp
GOSUB [$location],[argument 0],[argument 1], ... ,[argument 8]
```

, where `[$location]` — the name of the location whose code we want to execute without direct transition to it. Arguments `[argument 0]`, `[argument 1]`, etc. can be used at this location, their values are automatically placed in variables `args[0]`, `args[1]`, etc. respectively. After processing the location, previous `args` values are restored. Using arguments is not mandatory.

When calling a location via `gosub`, the base description of the location is added to the current description, base actions are added to current actions, and operators in the "Execute on visit" field are executed, then return to the original line (continue code execution after `gosub`).

Examples of calling locations via `gosub`:

```qsp
!processing location "move". The args[] array is empty.
gosub 'move'

!processing location with name from variable $location
!One parameter is passed - args[0] equals 1.
gosub $location,1

!processing location "move" with 3 parameters passed.
! $args[0] = $var (value), args[1] = 2,
! $args[2] = "data". Note the '$' symbols.
gosub 'move',$var,2,'data'
```

Another example:

```qsp
! this is code calling location "transition"
gosub 'transition', 'location'

! and this is code of the "transition" location itself
# transition
*pl $args[0]  & ! the text 'location' will be output to the screen
! a new action will appear in the actions window:
act 'go':
    goto "street"
end
- transition
```

The operator has a short form `gs`:

```qsp
GS [$location], [argument 0], [argument 1], ... , [argument 18]
```

## GOTO

`GOTO` — transition to the specified location. General syntax:

```qsp
GOTO [$location], [argument 0], [argument 1], ... , [argument 18]
```

, where `[$location]` — the name of the location to transition to. Arguments `[argument 0]`, `[argument 1]`, etc. can be used at this location, their values are automatically placed in variables `args[0]`, `args[1]`, etc. respectively. Using arguments is not mandatory.

When transitioning to a new location using `goto`, the main description window is cleared, as well as the current actions list, then the base description text is output to the main description window, base actions to the actions window, and code from the "Execute on visit" field of location `[$location]` is executed. Also, when transitioning to a new location, the value returned by the `$curloc` function changes.

Examples:

```qsp
! transition to location "house".
! The args array at location "house" will be empty.
goto 'house'

! transition to location "street" with 2 parameters passed.
! at location "street" args[0] equals 1,
! $args[1] contains the string "data".
goto 'street',1,'data'
```

The operator has a short form `gt`:

```qsp
GT [$location],[argument 0],[argument 1], ... ,[argument 8]
```

## IF

`IF` — the main operator for writing conditional constructs. Constructs written using this operator (let's call them "simple conditions") have two forms: single-line and multi-line, — and generally look like this:

General syntax:

```qsp
! single-line form
IF [#expression]: {command 1} & {command 2} & ...

! multi-line form
IF [#expression]:
  {command 1}
  {command 2}
  ...
END
```

In this case, if the condition `[#expression]` is true, commands `{command 1}`, `{command 2}`, etc. are executed.

- For **single-line form**, these will only be those commands that are on the same line as the `IF` operator until the end of the line;
- and for **multi-line form**, these will be those commands that are in subsequent lines after the colon and until the special keyword `END`.

Comparison operations, logical operations, and other expressions returning numeric values can serve as conditions.

The `END` keyword in multi-line form must be on a separate line.

If the condition `[#expression]` is not true, the commands will not be executed.

Examples of single-line conditional forms:

```qsp
! if the sum of a and b equals two,
! variable c is assigned the value 30
if a + b = 2: c = 30
! If there's no orange in inventory, text is output
if no obj("Orange"): pl "You don't have an orange."
! this is also a simple single-line form
if ((a+b)/c)=45+54 or (b<5 or c>45) and no obj 'shovel' and $f=$vvv+'RRRRR': p 'OK' & goto 'Next'
```

Examples of multi-line conditional forms:

```qsp
if library = 0:
  learned_about_party = 0
  library_returned = 1
  gt 'library'
end
if a+b=2:
  c=30
end
```

:::warning[Pay attention!!!]

In multi-line form, no commands should follow the colon on the same line as the IF operator, otherwise the player will consider such a conditional operator single-line, and commands in subsequent lines will be executed regardless of whether the condition is true or not. Example of such erroneous notation:

```qsp
if library = 0: learned_about_party = 0
  library_returned = 1 &! this line will execute regardless of condition truth
  gt 'library' &! and this one too
end &! the end keyword is simply ignored
```

The exception is a comment operator written after the colon:

```qsp
if library = 0: ! if haven't visited library
  learned_about_party = 0
  library_returned = 1
  gt 'library'
end
```

But if the comment is separated by an ampersand, the condition will be considered single-line:

```qsp
if library = 0: & ! such a comment makes the condition single-line!
  learned_about_party = 0 & ! this line will execute regardless of condition truth
  library_returned = 1 & ! and this one
  gt 'library' &! and this one too
end &! the end keyword is simply ignored
```

:::

For multi-line forms, unlimited nesting depth is allowed. Each nesting level must end with its own `end` line.

Examples:

```qsp
if a+b<3 or y=8:
    p 'A+B<3 or Y=8'
    nl
    if j=88: nl & p 'NEXT'
    if $h='ooo':
        p 'loo' & jump 'lll'
    end
end
```

```qsp
if a=0:
    'abc1234'
    if b=0: '0' else '1'
    if j=88: nl & p 'NEXT'
    if $h='ooo':
        p 'loo' & jump 'lll'
    else
        p 'sample text'
        v=8
    end
    1234
else
    '01234'
    g=78
end
```

Several examples of incorrect notation:

```qsp {4}
! in this case, if the condition is not met,
! the player will ignore only the command `k1=34`
! since it will consider this a single-line condition
if abcd=3: k1=34
    k2=35 & ! this command will always execute
    k3=36 & ! this command will always execute
end & ! this end will be ignored
```

```qsp {3,9}
! this line will output an error unknown action
! since single-line forms should not end with end
if abcd=3: k1=34 else k1=25 end
```

## ELSE

`ELSE` — keyword used together with the `IF` operator, which serves to provide an alternative if the condition is not met. The `ELSE` keyword also has two forms: single-line and multi-line.

- Multi-line form of `ELSE` can only be used in multi-line `IF` constructs,
- single-line form can be used in both single-line and multi-line `IF` constructs. General syntax:

```qsp
! single-line form
IF [#expression]: {command y1} & {command y2} & ... ELSE {command n1} & {command n2} & ...

! in multi-line IF:

! multi-line ELSE form
IF [#expression]:
    {command y1}
    {command y2}
    ...
ELSE
    {command n1}
    {command n2}
    ...
END

! single-line ELSE form
IF [#expression]:
    {command y1}
    {command y2}
    ...
ELSE {command n1} & {command n2} & ...
    ! commands in subsequent lines
    ! until END are ignored
END
```

Here, if condition `[#expression]` is true, commands from the colon to the `ELSE` keyword are executed, and if condition `[#expression]` is not true, commands from the `ELSE` keyword to the end of the conditional construct are executed.

You can put a colon after `ELSE` or not.

**For single-line form:**

- both commands and the `ELSE` keyword must be written on one line
- the end of the alternative command list is the end of the line.
- if single-line `ELSE` form is used in multi-line `IF` form, all commands in subsequent lines after `ELSE` until `END` are ignored.

Single-line examples:

```qsp
! if the sum of a and b equals two, variable c is assigned value 30
! otherwise (i.e., if the sum of a and b does not equal two)
! variable c is assigned value 10
if a+b=2: c=30 else c=10

! depending on whether there's an orange in inventory
! corresponding text is output
if obj("Orange"): pl "You have an orange." else pl "You don't have an orange."

! single-line else form inside multi-line if
if $left_hand = 'Great sword':
  gosub 'attack', 300
  gosub 'health.prove'
  gosub 'win.prove'
else gosub 'attack', attack_power
end
```

**For multi-line form:**

- all commands must be in subsequent lines after `ELSE`;

Multi-line examples:

```qsp
if a+b=2:
  c=30
else
  c=10
end

if obj("Orange"):
  pl "You have an orange."
else
  pl "You don't have an orange."
end

if len($curtoken) > 0:
  $tokens[curtoken_num] = $curtoken tokens_count = curtoken_num + 1
else
  tokens_count = curtoken_num
end
```

## ELSEIF

`ELSEIF` — keyword used together with the `IF` operator and allows defining sequentially-exclusive conditions at one nesting level. Has single-line and multi-line forms.

- Multi-line form can only be used in multi-line `IF` constructs,
- single-line — in both multi-line and single-line `IF` constructs.

General syntax:

```qsp
! single-line in single-line condition
IF [#expression 1]: {command set 1} ELSEIF [#expression 2]: {command set 2} ELSE {last command set}

! multi-line in multi-line condition
IF [#expression 1]:
  {command set 1}
  ...
ELSEIF [#expression 2]:
  {command set 2}
  ...
ELSEIF ... :
  ...
ELSE
  {last command set}
  ...
END

! single-line in multi-line condition
IF [#expression 1]:
  {command set 1}
  ...
ELSEIF [#expression 2]: {command set 2}
ELSEIF ... : ...
ELSE {last command set}
END
```

This works as follows. If `[#expression 1]` is true, `{command set 1}` is executed. If `[#expression 1]` is false but `[#expression 2]` is true, `{command set 2}` is executed, and so on. Only if all expressions in the current conditional construct are false, the commands after `ELSE` will be executed. The truth of expression `[#expression 1]` does not exclude the truth of expression `[#expression 2]`, but the truth of expression `[#expression 2]` excludes the truth of expression `[#expression 1]`.

`ELSEIF` notation features:

- The variant `ELSE IF` can be used. Works exactly the same.
- If in a multi-line `IF` construct operators follow `ELSEIF` on the same line (single-line form), then all subsequent lines are ignored until the next `ELSEIF`, or until `ELSE` or `END`.
- In an `IF` construct with `ELSEIF`, the `ELSE` part may or may not be present.

Examples:

```qsp
if obj('Health Potion'): health += 100 elseif obj('Apple'): health += 15 else *pl 'Nothing to restore strength with!'

IF SCORE>124:
  GOTO 'END3'
ELSEIF SCORE>99:
  GOTO 'END4'
ELSE
  GOTO 'END5'
END

if money mod 10=1 and money mod 100<>11:
  *pl "You have <<money>> coin."
elseif money mod 10>1 and money mod 10<5 and (money mod 100<5 or money mod 100>20):
  *pl "You have <<money>> coins."
elseif money mod 10=0 or money mod 10>4 or (money mod 100>10 and money mod 100<21):
  *pl "You have <<money>> coins."
end
```

Example of `ELSEIF` notation with operators on the same line:

```qsp
! switch/case implementation in QSP
if r = 0:
  'Option 0'
  elseif r = 1: 'Option 1'
  elseif r = 2: 'Option 2'
  elseif r = 3: 'Option 3'
  else: 'No options'
end
```

:::tip[Note:]

For better code readability, it's recommended to use `elseif` constructs only in multi-line `if` operator form.

:::

## INCLIB

`INCLIB` — from the specified game file, adds all locations whose names are absent among current game locations. Loaded locations are fully equivalent to locations from the main game file. General syntax:

```qsp
INCLIB [$game_file_path]
```

Example:

```qsp
inclib "lib/easy.math.qsp"
inclib "lib/easy.title.qsp"
inclib "res/drive.qsp"
inclib "res/base.qsp"
inclib "res/intro.qsp"
```

:::note[5.7.0]
In older player versions, the command was called `addqst` and `addlib`.
:::

## JUMP

`JUMP` — jump within the current code block to the specified label. General syntax:

```qsp
JUMP [$label]
```

, where `[$label]` — a label below or above in the code (see section ["Labels"](qsp-keyword-syntaxems.md#labels-)).

`jump` finds labels only within the current code block, i.e., labels are local.

Separate code blocks in QSP are:

- "Execute on visit" code of a specific location (each location is a separate code block),
- action code even if the action is added programmatically,
- code in hyperlinks,
- `DYNAMIC`/`DYNEVAL` code

Example:

```qsp
jump 'End'
p 'This message will not be output'
:end
p 'But this message the user will see'
```

:::note[5.7.0]
Using the `jump` operator in older player versions, you could organize loops:

```qsp
:loop
if s<9:
    s=s+1
    pl s
    jump 'loop'
end
p 'Done!'
```

Double loop with one label:

```qsp
:loop
if y<9:
    if x<9:
        *p "<<x>> - "
        x=x+1
        jump 'loop'
    end
    *pl ":<<y>>"
    y=y+1
    x=0
    jump 'loop'
end
```

Starting from version 5.8.0, a dedicated `loop` operator was introduced for loops.
:::

## KILLALL

`KILLALL` — destroys all variables and removes all items from the objects window. Equivalent to:

```qsp
killvar & killobj
```

:::warning[Attention!]
Remember that `killall` is not equivalent to:

```qsp
killobj & killvar
```

since in this case variable values are deleted after item removal, so the item removal handler location code has time to execute (see `$onobjdel`).
:::

Usually `killall` is used at the beginning of the game if a "Start over" action is provided at the end of the game.

## KILLOBJ

`KILLOBJ` — removes an item located at the specified position. General syntax:

```qsp
KILLOBJ [#number]
```

, where `[#number]` — the item number in the inventory window. Item numbering starts from 1. If the `[#number]` parameter is not specified, all items are removed. When removing each item with `killobj`, the item removal handler location code is executed (see `$onobjdel`).

Example:

```qsp
! remove the topmost item in the list
killobj 1
! remove the bottommost item in the list
killobj countobj
! remove all items
killobj
```

## KILLVAR

`KILLVAR` — removes the specified array element. General syntax:

```qsp
KILLVAR [$array_name], [element_index]
```

, where `[$array_name]` — the name of the array from which we want to remove an element, and `[element_index]` — the number, text index, or multi-dimensional index of the array element we want to remove. Array element numbering starts from 0.

If the element index is not specified, the entire array is cleared. If the operator is called without arguments, all variables and arrays are deleted.

Examples:

```qsp
killvar 'a', 3 & ! will remove element with index 3 from array 'a'
killvar 'unit', 'Paratrooper' & ! removes element with index 'Paratrooper' from array
killvar 'a' & ! removes array 'a'
killvar & ! removes all variables, arrays
killvar '$map_cell', (3, 4) & ! removal by multi-dimensional index
```

When removing an element, all following elements shift up one position.

Example:

```qsp
a[0] = 4
a[1] = 3
a[2] = 23
a[3] = 15
KILLVAR 'a', 1
! now the array looks like this:
! a[0] = 4
! a[1] = 23
! a[2] = 15
```

## LET

`LET` — deprecated operator for setting variable values. General syntax:

```qsp
LET [variable_name] = [expression]
```

, where `[variable_name]` — a valid variable name, `[expression]` — a valid value for this variable.

- Numeric variable names are written without `$` and `%` symbols at the beginning.
- Text variable names are written with the `$` symbol at the beginning.
- Variable names containing tuples are written with the `%` symbol at the beginning.

Examples:

```qsp
! set text variable
let $text = "text string"
! set numeric variable
let abs = 123
! set tuple
let %tuple = [123, "text string"]
```

:::tip
This operator is considered deprecated. Use the `set` operator instead, and only in cases where it improves code readability.

```qsp
! assignment can be done without set or let operators:
$text = "text string"
```

:::

## LOCAL

`LOCAL` — declares a local variable (or several variables) in the current code block.

General syntax:

```qsp
LOCAL [variable 1], [variable 2], ...
LOCAL [variable 1], [variable 2], ... = [value 1], [value 2], ...
```

, where `[variable 1]`, `[variable 2]`, etc. — variable/array names written directly (not in quotes), and `[value 1]`, `[value 2]`, etc. — any values, constants, expression values, functions, or other variables.

The number of variables and values must match (except for unpacking cases).

```qsp
! declare one local variable
local tempora = 12
! declare several local variables
local x, y, $item = 11, 19, "Old sword"
! declaration with unpacking
local i, j = %map_cell
local z, $a = [13, '37']
```

Unlike `set` and `let` operators, a variable can be declared without assigning a value.

```qsp
local tempora
local x, y, $item, %map_cell
```

However, despite the variable being created, `arrsize` will return `0` for it. I.e., you cannot check if a variable is declared.

```qsp
local arr
*pl arrsize('arr') & ! will output 0
```

You can create your own local variables in the following code blocks:

- Locations themselves.
- Code passed to the `DYNAMIC` operator or `DYNEVAL` function as text.
- Code executed when clicking a hyperlink.
- Code of each individual Action ([ACT](qsp-keyword-operators.md#act)).
- Code of each individual Loop ([LOOP](qsp-keyword-operators.md#loop))

:::warning[**Attention!**]
Local variables have one feature that needs to be clearly understood. The value of a local variable declared in a given code block is also translated to all nested or called code blocks. For example, if a local variable is declared on a location, its value is translated to all locations called with `GOSUB` or `FUNC`, to `DYNAMIC`/`DYNEVAL` code blocks, to loop blocks, etc. Example:

```qsp
# start
! from this location we will call location foo
i = 99 & ! declare global variable
gosub 'foo'
*nl i & ! we'll see number 99 on screen
--- start ---

# foo
! declare local variable on this location
local i = 0
! local variable is translated to the loop
loop while i < 10 step i += 1:
    ! in the loop we call location undo
    gosub 'undo'
    ! and also in the loop we work with the variable
    ! declared on location foo
end
*nl i & ! we'll see number 10 on screen
--- foo ---

# undo
! to this location from the loop on location foo
! the same local variable declared on location foo is translated
i+=1 & ! increase variable value, affecting the value in foo
*p 'undo:<<i>>, ' & ! numbers 1,3,5,7,9 will appear on screen with undo: prefix
--- undo ---
```

**However!** Local variable values are not translated to actions (unlike `ARGS` array values at the current location):

```qsp
$args[0] = 'current location'
local $var = 'local variable'
*pl $args[0]
*pl $var
act "Output values":
    *pl $args[0]
    *pl $var
end
```

:::

### Examples of local variable assignment

```qsp title="Two locations, each with its own variable i"
# location 1
if i = 0: i = 99 & ! variable i value is set only once
*pl "Global i = <<i>>"
act "To location 2": goto 'location 2'
--- location 1 ---

# location 2
*pl "Global i = <<i>>"
local i = 137 & ! variable i value is set only once
*pl "Local i = <<i>>"
act "To location 1": goto 'location 1'
--- location 2 ---
```

```qsp title="Another example with two locations"
! this code will sequentially output numbers 12, 549 and 99, 549
# start
x = 99
z = 4608
gosub 'foo'
*pl x & *pl z   & ! numbers 99 and 549 will be output
--- start ---

# foo
local x & ! declare variable x local for this location
x = 12    & ! change variable x value
z = 549
*pl x & *pl z   & ! numbers 12 and 549 will be output
--- foo ---
```

```qsp title="Example of declaring local variables in DYNEVAL code and in a loop"
$chkObjWord = {
    ! this is code written as text in variable $chkObjWord
    ! write the search word to local variable $word
    local $word = $args[0]
    loop local i = 1 while no i > countobj step i += 1:
        ! use local variable i inside the loop
        ! loop executes while counter doesn't exceed item count
        if instr($getobj(i), $word) <> 0:
            ! as soon as the considered word is found
            ! in the next item name
            result = i  & ! return position
            exit    & ! close function
        end
    end
}
object_position = dyneval($chkObjWord, 'grenade')
```

```qsp title="Local variables can also be declared inside actions"
i=99
act "Action with local i":
    local i = 449933
    *pl i
end
act "Action with global i":
    *pl i
end
```

## LOOP

`LOOP` — loop operator. Necessary for organizing cyclical calculations. General single-line syntax:

```qsp
LOOP {commands before loop start} WHILE [condition] STEP {commands at end of iteration}: {loop body operators}
```

General multi-line syntax:

```qsp
LOOP {commands before loop start} WHILE [condition] STEP {commands at end of iteration}:
    {loop body operators}
END
```

, where:

- `{commands before loop start}` — commands executed before the loop is started. These commands belong to the loop block but don't fall into iterations (passes), i.e., executed only once. Here you can, for example, declare a loop counter. And here you can write multiple commands, listing them through the separator `&` (ampersand).
- `[condition]` — an expression by whose value the condition is checked. Comparison operations and logical operations in any combinations can be used here. If the `[condition]` expression value equals zero, the loop is interrupted.
- `{commands at end of iteration}` — commands executed at the end of each loop pass. Commands that don't directly relate to the loop body but should be executed on each iteration can be placed here. Here you can, for example, change the loop counter value. And here you can actually write multiple commands, listing them through the separator `&` (ampersand).
- `{loop body operators}` — commands that need to be executed on each pass and are main for the loop. I.e., we make the loop exactly for these commands.

A loop in QSP is a separate code block, which means we can declare local variables inside this code block. This is very convenient because we can declare a local variable for the counter, and this won't affect other variables at the location:

```qsp
i = 99
*pl "i before loop <<i>>"
loop local i = 0 & *p "i in loop: " while i < 6 step i += 1:
    *p "<<i>>, "
end
*nl "i after loop <<i>>"
```

Loops are very convenient for iterating through arrays. For example, you can use a loop to sum all numbers stored in an array:

```qsp
summ=0 & ! here we'll write the sum of numbers
! our numbers are in array **mass**
loop local i, size = 0, arrsize('mass') while i < size step i += 1:
    summ += mass[i]
end
*pl 'Sum of all elements in mass array: <<summ>>'
```

## MENU

`MENU` — displays a popup menu anywhere in the game, whose items are defined in the specified array. General syntax:

```qsp
MENU [$array_name]
```

Before using this operator, you need to fill the array on which the menu items will be based. Menu items are tuples of three values, sequentially placed in consecutive array cells starting from zero. The contents of each tuple should be approximately like this:

```qsp
["menu item name", "location name", "icon file path"]
```

Menu item name is what we'll see on screen when the menu is displayed; location name is the name of the location whose code will be executed when the corresponding menu item is clicked; icon file path is the path to the image file that will be displayed next to the menu item name.

Knowing this, we can fill the array to create our menu items:

```qsp
%stone[0] = ['Take stone', 'takestone']
%stone[1] = ['Throw stone', 'throwstone']
%stone[2] = ['Examine stone', 'lookstone']
```

Here the array name (`%stone`) is the menu name, and the tuples are actions with specified item names and menu item selection handler location names. When selecting "Take stone", the location named "takestone" will be called. The same will happen with other items.

To display the menu on screen, use the `MENU` operator:

```qsp
menu '%stone'
```

Example of creating a menu with icons:

```qsp
! no icon
%usr_menu[0] = ['Take item', 'take_item']
! icon specified by gif file
%usr_menu[1] = ['Put item', 'put_item', 'images/put_item.gif']
! icon specified by $icon_file value
%usr_menu[2] = ['Destroy item','del_item', $icon_file]
! menu item specified by 3 variables
%usr_menu[3] = [$name, $location, $icon_file]

menu 'usr_menu' &! will show menu with 4 items
```

The menu ends at an array element with an empty tuple, or with a tuple missing a value for the menu item name or item handler location.

Examples where the last two menu items won't be created:

```qsp
%usr_menu[0]=['Take item','take_item'] & ! we'll see this item on screen
$usr_menu[1]=['Examine item','look_item'] & ! and we'll see this item on screen
$usr_menu[2]=[] & ! empty tuple, player will consider the menu ended
$usr_menu[3]=['Put item','put_item'] & ! we won't see this item
```

```qsp
%usr_menu[0]=['Take item','take_item'] & ! we'll see this item on screen
$usr_menu[1]=['Examine item','look_item'] & ! and we'll see this item on screen
$usr_menu[2]=['destroy item', ''] & ! no handler location specified, won't see item
$usr_menu[3]=['Put item','put_item'] & ! and we won't see this item
```

```qsp
%usr_menu[0]=['Take item','take_item'] & ! we'll see this item on screen
$usr_menu[1]=['Examine item','look_item'] & ! and we'll see this item on screen
$usr_menu[2]=['', 'del_item'] & ! no name specified, won't see item
$usr_menu[3]=['Put item','put_item'] & ! and we won't see this item
```

To insert a separator in the menu, use a tuple with `-` values. I.e., if you need to put a separator instead of the 3rd element:

```qsp
%usr_menu[0]=['Take item','take_item']
$usr_menu[1]=['Examine item','look_item']
$usr_menu[2]=['-', '-'] & ! separator instead of menu item
$usr_menu[3]=['Put item','put_item']
```

An argument (`args[0]`) - the position of the selected item - is passed to the menu item selection handler location. Menu item positions are numbered from 1.

## MSG

`MSG` — outputs the specified message in a dialog box. General syntax:

```qsp
MSG [message]
```

, where `[message]` — any text string, number, expression of any type. Examples:

```qsp
! simple message output.
msg 'Many ripe pears.'
! we get a window with message 'Many ripe pears'
```

```qsp
! Example message in ACT action.
act 'Eat pears':
   msg 'Mmm pears are very tasty.'
end
! We get message output when clicking "Eat pears" action
```

```qsp
! Example with condition.
if breadready = 1:
    msg 'Looks like the bread is ready.'
end
! We get message output when condition breadready = 1
```

## OPENGAME

`OPENGAME` — loads the specified game state file. General syntax:

```qsp
OPENGAME [$path]
```

, where `[$path]` — path to the saved game state file. If the `[$path]` parameter is absent, the game state loading window is called.

Example:

```qsp
! load state from file 1.sav
opengame "1.sav"
! open state loading window
opengame
```

See also the game state loading event handler location ([$ongload](qsp-keyword-sys-var.md#ongload)).

## OPENQST

`OPENQST` — opens and runs the specified game file. General syntax:

```qsp
OPENQST [$path]
```

, where [$path] — path to the game file to run. Example:

```qsp
openqst "gamespool/cubesgame.qsp"
```

When using this operator, variables are not deleted, inventory items are not removed, additional description and input line are not cleared, and playing files are not stopped. If you need to clear the screen and all variable values, you can write such commands at the beginning of the loaded game file:

```qsp
killall & cls & close all
```

## REFINT

`REFINT` — forced interface update (including color and font changes assigned with system variables).

By default, interface updates occur 2 times per second (every 500 ms). Also see the [`settimer`](#settimer) operator.

## SAVEGAME

`SAVEGAME` — saves game state to the specified file. General syntax:

```qsp
SAVEGAME [$path]
```

, where `[$path]` — path to the created game state save file. If the `[$path]` parameter is absent, the game state save window is called.

Example:

```qsp
! save state to file 1.sav
savegame "1.sav"
! open state save window
savegame
```

See also [game state save event handler location ($ongsave)](qsp-keyword-sys-var.md#ongsave).

## SETTIMER

`SETTIMER` — sets the interval for calling the counter location. General syntax:

```qsp
SETTIMER [#expression]
```

, where `[#expression]` — period for calling the counter location in milliseconds. By default, the player calls the counter location every 500 ms, i.e., 2 times per second.

Setting the counter location call period also affects the frequency of automatic interface settings updates.

Examples:

```qsp
! counter location will run every 2 seconds:
settimer 2000
```

```qsp
! counter location will run 4 times per second:
settimer 250
```

```qsp
! if we set frequency (times per second)
frequency=10 & ! ten times per second
settimer 1000/frequency
```

```qsp
! if we set period (every how many seconds)
period=2 & ! every two seconds
settimer 1000*period
```

The minimum period value can thus be 1 millisecond:

```qsp
settimer 1
```

However, in practice, the minimum value is limited by your computer's power, and it's usually higher than 1 millisecond.

## VIEW

`VIEW` — displays the specified image on screen. In the classic player, the image is displayed in a separate window (preview window), in qSpider the image is displayed as a layer. General syntax:

```qsp
VIEW [$graphics_file_path]
```

, where `[$graphics_file_path]` — path to the image file. If the `[$graphics_file_path]` parameter is absent or set as `''` (empty string), the preview window closes.

Examples:

```qsp
! display image in preview window
view 'content/monster.png'
! close preview window
view ''

! you can also close the preview window like this
view
```

## WAIT

`WAIT` — pauses program code execution for the specified number of milliseconds. General syntax:

```qsp
WAIT [#milliseconds]
```

, where `[#milliseconds]` — time in milliseconds to stop program code execution.

Example:

```qsp
! stop program execution for 5 seconds
wait 5000
```

:::warning[Caution!]
This operator must be used carefully since pausing code execution blocks the player's ability to interact with the game.
:::

`WAIT` not only interrupts code execution but also forces the player to output information from the screen buffer. During normal location code execution, all text for `*pl`, `*p` `pl`, `nl` etc. operators is placed in a special screen buffer and output to screen only after all location code is executed. When using `WAIT`, text from the buffer is output immediately when `WAIT` is executed, which is sometimes useful as it allows tracking value changes step by step.

In the example below, numbers will first be written to the screen buffer and only then appear on screen:

```qsp
loop i=0 while i<5 step i+=1:
    *p i
end
*pl
```

In the next example, they will be output one after another with approximately 100 ms intervals.

```qsp
loop i=0 while i<5 step i+=1:
    wait 100
    *p i
end
*pl
```

