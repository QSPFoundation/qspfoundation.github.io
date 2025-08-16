---
sidebar_position: 2
---

# Operators

## Implicit operator

The implicit operator is an operator that is not written in QSP code but outputs values to the screen. It is implied wherever an expression without an operator is present in a command. The implicit operator outputs values to the **Main Description Window** in the same way as if you used explicit specification of the `*pl` operator, i.e., it outputs the value and makes a line break. Examples:

```qsp
$AAA + '989'
'You are in the park'
'Preformatted

    string'
$curloc & ! will output the location name to the screen
```

Unlike the `*pl` operator, the implicit operator does not output an empty line with a line break to the screen if no value is passed to it. This means that if a function returns no value, the implicit operator is simply ignored. Example:

```qsp
# start
! this is the code of a location calling a location-function
$curloc
$func('foo')
$func('foo')
$curloc
- start

# foo
! this is the code of the location-function
local i = 0
- foo
```

In this case, the location-function `foo` returns nothing, so we will see two lines with the word "start" on the screen, with no empty lines between them, since the implicit operator in the lines with `$func` at location `start` will be simply ignored. Compare with:

```qsp
# start
! this is the code of a location calling a location-function
*pl $curloc
*pl $func('foo')
*pl $func('foo')
*pl $curloc
- start

# foo
! this is the code of the location-function
local i=0
- foo
```

## `!` (comment)

`!` — comment operator. What is in the line after the comment operator and until the end of the line is ignored by the interpreter. The comment operator allows you to "comment out" (disable) an unnecessary operator/function temporarily during game debugging. In addition, writing comments to program code is one of the signs of good programming style.

It is necessary to clearly understand that this is an operator, so if you are commenting some line of code, then `!` should come after `&`:

```qsp
*pl "Hello, world!" & ! comment
```

Comments can be single-line, i.e., end on the same line where the comment operator is located:

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
can move to other lines " as well as {
you can use other character groups to
continue the multi-line comment
} and the comment won't end until the line ends
```

## `*CLEAR`

`*CLEAR` — clears the main description window. Has a short form `*clr`.

## `*NL`

`*NL` — line break, then text output in the main description window. General syntax:

```qsp
*NL [$text]
```

where `[$text]` is any text string, number, or expression of any type. If `[$text]` is absent, a simple line break occurs. Example:

```qsp
*p "Text without line break."
*nl "Line break + text output."
*p "Text without line break."
```

## `*P`

`*P` — text output to the main description window without line break. Text output by any other operator immediately after `*p` will add new text immediately after the current text. General syntax:

```qsp
*P [$text]
```

where `[$text]` is any text string, number, or expression of any type. `[$text]` can be an empty string `''`, but should not be absent. Example:

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

where `[$text]` is any text string, number, or expression of any type. `[$text]` can be absent, then just a line break. Example:

```qsp
*pl "Text output, then line break."
*pl "Text output, then line break."
*p "Text without line break."
*pl "Text output, then line break."
```

You can output text in the same way by simply writing the needed expression instead of this operator. For example, the lines:

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
ACT [$name], [$path to image file]: [operator] & [operator] & [operator]
```

General syntax in multi-line form:

```qsp
ACT [$name], [$path to image file]:
    [operator]
    [operator]
    [operator]
END
```

A new action with name `[$name]` and image located at `[$path to image file]` is added to the actions list in the actions window. When the action is clicked, the specified operators are executed.

The `[$path to image file]` parameter can be absent, in which case the action is added without an image.

Examples:

```qsp
! action in single-line form
act "Pick apple from birch": apple += 1 & *pl "You picked a ripe white apple."

! action in multi-line form, with image
act "Pick watermelon from bush", "img/watermelon.png":
    watermelon += 1
    *pl "You picked a watermelon from the bush"
end
```

If there is already an action with the specified name in the actions list, no new action is created, and it does not replace the existing one, the player simply ignores the `act` command. Thus, you cannot output actions with identical names. Example:

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

`ADDOBJ` — adding a new object to the objects window. General syntax:

```qsp
ADDOBJ [$name], [$path to image file], [#position]
```

where `[$name]` is the object name, `[$path to image file]` is the path to the object's image file (displayed next to the object name), and `[#position]` is the position in the inventory where the object is added. The `[#position]` parameter can be absent. By default, objects are added to the end of the list. Object numbering in the inventory starts from `1`. The `[$path to image file]` parameter can be absent, default value is `''`, in which case the object is added without an image.

:::note[Allowed but not recommended, deprecated form:]

```qsp
ADD OBJ [$name],[$path to image file],[#index]
```

:::

You can add objects with the same name, but if you plan to add many identical objects, it's better to use an additional variable to count these objects and add one object to the objects window to avoid cluttering the inventory with a list of 137 Ruble / Cartridge objects:

```qsp
if obj('Cartridges'):
! if object "Cartridges" is already added, just increase their number
    cartridges += 10
else
! if object "Cartridges" is not yet added, add it and increase the number
    addobj 'Cartridges'
    cartridges += 10
end
```

You can use arrays indexed by strings to store object counts:

```qsp
objects['money'] = 12
objects['cartridges'] = 137
'Quantity: <<objects[$getobj(countobj)]>>'
```

Example of adding an object to the very top of the list (all other objects will shift down):

```qsp
addobj "Screwdriver", "", 1
```

## CLA

`CLA` - clearing the list of current actions (removing all actions from the actions window).

## CLEAR

`CLEAR` — clears the additional description window. Has a short form `clr`.

## CLOSE

`CLOSE` — stops playing the specified sound file. General syntax:

```qsp
CLOSE [$path to sound file]
```

where `[$path to sound file]` is the path to the sound file relative to the game file. If the `[$path to sound file]` parameter is not specified, all sound files stop playing.

## CLOSE ALL

`CLOSE ALL` — stops playing all active sound files. Has a short form `close`.

## CLS

`CLS` — clears all windows except the objects list. Equivalent to the construction:

```qsp
clear & *clear & cla & cmdclear
```

## CMDCLEAR

`CMDCLEAR` — clearing the input line. Has a short form `cmdclr`.

## COPYARR

`COPYARR` — copying the contents of one array to another. General syntax:

```qsp
COPYARR [$receiver], [$source], [#start], [#count]
```

where: `[$receiver]` is the array to which copying is performed, size and content don't matter; `[$source]` is the array from which copying is performed; `[#start]` is the element number from which to start copying; `[#count]` is how many elements to copy. The `[#count]` parameter is optional; by default — until the end of the source array. The `[#start]` parameter is optional; by default — 0.

Examples:

```qsp
! copy all elements of array '$b' to array '$a'
copyarr '$a', '$b'
! at the same time, all elements of array 'b' were also copied to array 'a'

! copy elements of array 'd' starting from the sixth to array 'c'
copyarr 'c', 'd', 6

! copy the first six elements of array 'd' to array 'c'
copyarr 'c', 'd', 0, 6
```

Due to player peculiarities, when copying, for example, numeric array `mass1` to `mass2`, text array `$mass1` is also copied to `$mass2`.

Other examples:

```qsp
copyarr $arrname1, $arrname2, 10, 5
copyarr 'a<<$arrname1>>', 'a<<$arrname2>>'
```

## DELACT

`DELACT` — removes an action from the actions list (if such action exists). General syntax:

```qsp
DELACT [$name]
```

where `[$name]` is the name of the action we want to remove.

Examples:

```qsp
! remove action with specific name
delact 'Go forward'
! remove selected action
delact $selact
```

:::note[Allowed but not recommended, deprecated form:]

```qsp
DEL ACT [$name]
```

:::

## DELOBJ

`DELOBJ` — removing an object from inventory by name (if such object exists). General syntax:

```qsp
DELOBJ [$name]
```

where `[$name]` is the name of the object we want to remove.

If there are identical objects in the inventory, the command will remove the topmost one with the specified index.

Examples:

```qsp
! remove object with specific name
delobj "Screwdriver"
! remove selected object
delobj $selobj
```

:::note[Allowed but not recommended, deprecated form:]

```qsp
DEL OBJ [$name]
```

:::

## DYNAMIC

`DYNAMIC` — executes code passed as a text string. General syntax:

```qsp
    DYNAMIC([$code], [argument 0], [argument 1], ... , [argument 18])
```

where `[$code]` is regular QSP code written as text. Execution of such code is similar to executing `GOSUB` operator code. Arguments `[argument 0]`, `[argument 1]`, etc. can be used inside `[$code]`, their values are automatically placed in variables `args[0]`, `args[1]`, etc. respectively. After execution, old `args` parameters are restored, then code execution continues from the next command after `dynamic`.

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

The following information is also true for the [`dyneval`](qsp-keyword-functions.md#dyneval) function.

**Important!** If code is specified using apostrophes (`''`) or quotes (`""`), sub-expressions are evaluated in the text:

```qsp
$args[0] = 'qwerty'
$code = '
    *pl "<<$args[0]>>"
    *pl $args[0]
'

dynamic $code, 'asdfg'
```

In this case, when setting the `$code` variable, the sub-expression will be evaluated, so the first line will output 'qwerty', the second line will output 'asdfg'.

Curly braces are the third type of quotes used specifically for writing dynamic code. Here, bracket nesting is supported, and sub-expressions are not evaluated before code execution:

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

`EXIT` — termination of the current code block execution (premature exit from subroutine, function, event handler, etc.).

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
In players version 5.8.0, the `loop` operator appeared.

The loop body is also considered a separate code block, but the `exit` operator interrupts not only the loop itself, but also the code block in which the loop is located.
:::

## FREELIB

`FREELIB` — removes all locations added with the `inclib` operator.

:::note[5.7.0]
In older player versions, the command was called `dellib` and `killqst`.
:::

## GOSUB

`GOSUB` — executing code of the specified location without directly going to it.

General syntax:

```qsp
GOSUB [$location],[argument 0],[argument 1], ... ,[argument 8]
```

where `[$location]` is the name of the location whose code we want to execute without directly going to it. Arguments `[argument 0]`, `[argument 1]`, etc. can be used on this location, their values are automatically placed in variables `args[0]`, `args[1]`, etc. respectively. After processing the location, previous `args` values are restored. Using arguments is not mandatory.

When accessing a location via `gosub`, the base description of the location is added to the current description, base actions are added to current actions, and operators in the "Execute on visit" field are executed, then return to the original line (continuing code execution after `gosub`).

Examples of calling locations via `gosub`:

```qsp
!processing location "move". The args[] array is empty.
gosub 'move'

!processing location with name from variable $location
!One parameter is passed - args[0] equals 1.
gosub $location,1

!processing location "move" with passing 3 parameters.
! $args[0] = $var (value), args[1] = 2,
! $args[2] = "data". Note the '$' symbols.
gosub 'move',$var,2,'data'
```

Another example:

```qsp
! this is the code for calling location "transition"
gosub 'transition', 'location'

! and this is the code of the location "transition" itself
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

where `[$location]` is the name of the location to which the transition should be made. Arguments `[argument 0]`, `[argument 1]`, etc. can be used on this location, their values are automatically placed in variables `args[0]`, `args[1]`, etc. respectively. Using arguments is not mandatory.

When transitioning to a new location using `goto`, the main description window is cleared, as well as the list of current actions, then the base description text is output to the main description window, base actions to the actions window, and code from the "Execute on visit" field of location `[$location]` is executed. Also, when transitioning to a new location, the value returned by the `$curloc` function changes.

Examples:

```qsp
! transition to location "house".
! The args array at location "house" will be empty.
goto 'house'

! transition to location "street" with passing 2 parameters.
! at location "street" args[0] equals 1,
! $args[1] contains string "data".
goto 'street',1,'data'
```

The operator has a short form `gt`:

```qsp
GT [$location],[argument 0],[argument 1], ... ,[argument 8]
```

## IF

`IF` — the main operator for writing conditional constructions. Constructions written using this operator (let's call them "simple conditions") have two forms: single-line and multi-line, and generally look like this:

General form:

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

In this case, if condition `[#expression]` is true, commands `{command 1}`, `{command 2}`, etc. are executed.

- For **single-line form**, these will be only those commands that are on the same line as the `IF` operator until the end of the line;
- and for **multi-line form**, these will be those commands that are in subsequent lines after the colon and until the special keyword `END`.

Comparison operations, logical operations, and other expressions returning numeric values can serve as conditions.

The `END` keyword in multi-line form must be on a separate line.

If condition `[#expression]` is not true, commands will not be executed.

Examples of single-line conditional forms:

```qsp
! if the sum of a and b equals two,
! variable c is assigned value 30
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

In multi-line form, after the colon on the same line where the IF operator is located, there should be no commands, otherwise the player will consider such a conditional operator single-line, and commands in subsequent lines will be executed in any case, regardless of whether the condition turns out to be true or not. Example of such erroneous notation:

```qsp
if library = 0: learned_about_party = 0
  library_returned = 1 &! this line will be executed regardless of the condition's truth
  gt 'library' &! and this one too
end &! the end keyword is simply ignored
```

The exception is the comment operator written after the colon:

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
  learned_about_party = 0 & ! this line will be executed regardless of the condition's truth
  library_returned = 1 & ! and this one
  gt 'library' &! and this one too
end &! the end keyword is simply ignored
```

:::

For multi-line forms, unlimited depth nesting is allowed. Each nesting level must end with its own `end` line.

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
    k2=35 & ! this command will always be executed
    k3=36 & ! this command will always be executed
end & ! this end will be ignored
```

```qsp {3,9}
! this line will output an error unknown action
! since single-line forms should not end with end
if abcd=3: k1=34 else k1=25 end
```

## ELSE

`ELSE` — keyword used together with the `IF` operator, which serves to provide an alternative if the condition is not met. The `ELSE` keyword also has two forms: single-line and multi-line.

- Multi-line form of `ELSE` can only be used in multi-line construction of the `IF` operator,
- single-line form can be used both in single-line and multi-line constructions of the `IF` operator. General form:

```qsp
! single-line form
IF [#expression]: {command y1} & {command y2} & ... ELSE {command n1} & {command n2} & ...

! in multi-line IF:

! multi-line form of ELSE
IF [#expression]:
    {command y1}
    {command y2}
    ...
ELSE
    {command n1}
    {command n2}
    ...
END

! single-line form of ELSE
IF [#expression]:
    {command y1}
    {command y2}
    ...
ELSE {command n1} & {command n2} & ...
    ! commands in following lines
    ! until END are ignored
END
```

Here, if condition `[#expression]` is true, commands from the colon to the `ELSE` keyword are executed, and if condition `[#expression]` is not true, commands from the `ELSE` keyword to the end of the conditional construction are executed.

After `ELSE` you can put or not put a colon.

**For single-line form:**

- both commands and the `ELSE` keyword must be written on one line
- the end of the alternative command list is the end of the line.
- if single-line form of `ELSE` is used in multi-line form of `IF`, all commands that follow in subsequent lines after `ELSE` until `END` are ignored.

Examples of single-line notation:

```qsp
! if the sum of a and b equals two, variable c is assigned value 30
! otherwise (i.e., if the sum of a and b does not equal two)
! variable c is assigned value 10
if a+b=2: c=30 else c=10

! depending on whether there's an orange in inventory
! corresponding text is output
if obj("Orange"): pl "You have an orange." else pl "You don't have an orange."

! single-line form of else inside multi-line if
if $left_hand = 'Great sword':
  gosub 'atack', 300
  gosub 'health.prove'
  gosub 'win.prove'
else gosub 'atack', atack_power
end
```

**For multi-line form:**

- all commands must be in subsequent lines after `ELSE`;

Examples of multi-line notation:

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

- Multi-line form can only be used in multi-line constructions with the `IF` operator,
- single-line form can be used in both multi-line and single-line constructions with the `IF` operator.

General forms:

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

This works as follows. If `[#expression 1]` is true, commands `{command set 1}` are executed. If `[#expression 1]` is false, but `[#expression 2]` is true, commands `{command set 2}` are executed, and so on. And only if all expressions in the current conditional construction are false, commands after `ELSE` will be executed. The truth of expression `[#expression 1]` does not exclude the truth of expression `[#expression 2]`, but the truth of expression `[#expression 2]` excludes the truth of expression `[#expression 1]`.

Features of `ELSEIF` notation:

- The variant `ELSE IF` can be used. Works exactly the same.
- If in multi-line `IF` construction after `ELSEIF` operators are on the same line (single-line form), then all subsequent lines are ignored until the next `ELSEIF`, or until `ELSE` or `END`.
- In `IF` construction with `ELSEIF`, the part with `ELSE` can be either present or absent.

Examples:

```qsp
if obj('Health potion'): health += 100 esleif obj('Apple'): health += 15 else *pl 'Nothing to restore strength!'

IF POINTS>124:
  GOTO 'END3'
ELSEIF POINTS>99:
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
! implementing switch/case in QSP
if r = 0:
  'Option 0'
  elseif r = 1: 'Option 1'
  elseif r = 2: 'Option 2'
  elseif r = 3: 'Option 3'
  else: 'No options'
end
```

:::tip[Note:]

For better code readability, it's recommended to use constructions with `elseif` only in multi-line form of the `if` operator.

:::

## INCLIB

`INCLIB` — from the specified game file, adds all locations whose names are absent among the current game locations. Loaded locations are fully equivalent to locations from the main game file. General syntax:

```qsp
INCLIB [$path to game file]
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

`JUMP` — jump in the current code block to the specified label. General syntax:

```qsp
JUMP [$label]
```

where `[$label]` is a label below or above in the code (see section ["Labels"](qsp-keyword-syntaxems.md#labels-)).

`jump` finds a label only within the current code block, i.e., labels are local.

Separate code blocks in QSP are:

- "Execute on visit" code of a specific location (each location is a separate code block),
- action code even if the action is added programmatically,
- code in a hyperlink,
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

Starting from version 5.8.0, the `loop` operator was introduced for loops.
:::

## KILLALL

`KILLALL` — destroys all variables and removes all objects from the objects window. Equivalent to the construction:

```qsp
killvar & killobj
```

:::warning[Attention!]
Remember that `killall` is not equivalent to the construction:

```qsp
killobj & killvar
```

since in this case variable values are deleted after object deletion, meaning the object deletion handler location code has time to execute (see `$onobjdel`).
:::

Usually `killall` is used at the beginning of the game if there's a "Start over" action at the end of the game.

## KILLOBJ

`KILLOBJ` — removing an object located at the specified position. General syntax:

```qsp
KILLOBJ [#number]
```

where `[#number]` is the object number in the inventory window. Object numbering starts from 1. If the `[#number]` parameter is not specified, all objects are removed. When removing each object using `killobj`, the object deletion handler location code is executed (see `$onobjdel`).

Example:

```qsp
! remove the topmost object in the list
killobj 1
! remove the bottommost object in the list
killobj countobj
! remove all objects
killobj
```

## KILLVAR

`KILLVAR` — removing the specified array element. General syntax:

```qsp
KILLVAR [$array name], [element index]
```

where `[$array name]` is the name of the array from which we want to remove an element, and `[element index]` is the number, text index, or multi-dimensional index of the array element we want to remove. Array element numbering starts from 0.

If the element index is not specified, the entire array is cleared. If the operator is called without arguments, all variables and arrays are deleted.

Examples:

```qsp
killvar 'a', 3 & ! will delete element with index 3 from array 'a'.
killvar 'unit', 'Paratrooper' & ! deletes element with index 'Paratrooper' from array
killvar 'a' & ! deletes array 'a'
killvar & ! deletes all variables, arrays
killvar '$map_cell', (3, 4) & ! deletion by multi-dimensional index
```

When deleting an element, all elements following it shift up one position.

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

`LET` — deprecated operator for setting variables values. General syntax:

```qsp
LET [variable name] = [expression]
LET [variable 1], [variable 2], ... = [value 1], [value 2], ...
```

where `[variable name]` is a valid variable name, `[expression]` is a valid value for this variable.

- Numeric variable names are written without `$` and `%` symbols at the beginning.
- Text variable names are written with `$` symbol at the beginning.
- Variable names containing tuples are written with `%` symbol at the beginning.

Examples:

```qsp
! set text variable
let $text = "text string"
! set numeric variable
let abs = 123
! set tuple
let %tuple = [123, "text string"]
! multiple assignment
let unit_power, $unit_name = 1300, 'DiggerBull'
! unpack the tuple
let $name, age, height = %npc_fields
```

:::tip
This operator is considered deprecated. Use the `set` operator instead, and only in cases when it improves code readability.

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

where `[variable 1]`, `[variable 2]`, etc. are variable/array names written directly (not in quotes), and `[value 1]`, `[value 2]`, etc. are any values, constants, expression values, functions, or other variables.

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

Unlike `set` and `let` operators, you can declare a variable but not assign it a value.

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
- Code executed when clicking on a hyperlink.
- Code of each separate Action ([ACT](qsp-keyword-operators.md#act)).
- Code of each separate Loop ([LOOP](qsp-keyword-operators.md#loop))

:::warning[**Attention!**]
Local variables have one feature that needs to be very clearly understood. The value of a local variable declared in a given code block is translated to all nested or called code blocks from this one. For example, if a local variable is declared on a location, its value is translated to all locations called using `GOSUB` or `FUNC`, to code blocks for `DYNAMIC`/`DYNEVAL`, to loop blocks, and so on. Example:

```qsp
# start
! from this location we will call location foo
i = 99 & ! declare global variable
gosub 'foo'
*nl i & ! we'll see number 99 on screen
--- start ---

# foo
! on this location we declare a local variable
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
*p 'undo:<<i>>, ' & ! numbers 1,3,5,7,9 with prefix undo: will appear on screen
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
*pl x & *pl z   & ! numbers 99 and 549 will be output to screen
--- start ---

# foo
local x & ! declare variable x local for this location
x = 12    & ! change variable x value
z = 549
*pl x & *pl z   & ! numbers 12 and 549 will be output to screen
--- foo ---
```

```qsp title="Example of declaring local variables in DYNEVAL code and in loop"
$chkObjWord = {
    ! this is code written as text in variable $chkObjWord
    ! in local variable $word we write the word
    ! by which we search
    local $word = $args[0]
    loop local i = 1 while no i > countobj step i += 1:
        ! use local variable i inside the loop
        ! loop executes while counter doesn't exceed number of objects
        if instr($getobj(i), $word) <> 0:
            ! as soon as the considered word is found
            ! in the name of the next object
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

`LOOP` — loop operator. Necessary for organizing cyclic calculations. General syntax of single-line form:

```qsp
LOOP {commands before loop start} WHILE [condition] STEP {commands at end of iteration}: {loop body operators}
```

General syntax of multi-line form:

```qsp
LOOP {commands before loop start} WHILE [condition] STEP {commands at end of iteration}:
    {loop body operators}
END
```

where:

- `{commands before loop start}` — these are commands executed before the loop is started. These commands belong to the loop block but don't fall into iterations (passes), i.e., are executed only once. Here you can, for example, declare a loop counter. And here you can write multiple commands, listing them with the `&` (ampersand) separator.
- `[condition]` — this is an expression by whose value the condition is checked. Comparison operations and logical operations in any combinations can be used here. If the value of expression `[condition]` equals zero, the loop is interrupted.
- `{commands at end of iteration}` — these are commands executed at the end of each loop pass. Commands that don't directly relate to the loop body but nevertheless should be executed on each iteration can be placed here. Here you can, for example, change the loop counter value. And here you can actually write multiple commands, listing them with the `&` (ampersand) separator.
- `{loop body operators}` — these are commands that need to be executed on each pass and are the main ones for the loop. I.e., we make the loop specifically for these commands.

The loop in QSP is a separate code block, which means we can declare local variables inside this code block. This is very convenient because we can declare a local variable for the counter, and this won't affect other variables at the location:

```qsp
i = 99
*pl "i before loop <<i>>"
loop local i = 0 & *p "i in loop: " while i < 6 step i += 1:
    *p "<<i>>, "
end
*nl "i after loop <<i>>"
```

Loops are very convenient for iterating through arrays. For example, you can use a loop to add all numbers stored in an array:

```qsp
summ=0 & ! here we'll write the sum of numbers
! our numbers are in array **mass**
loop local i, size = 0, arrsize('mass') while i < size step i += 1:
    summ += mass[i]
end
*pl 'Sum of all elements in array mass: <<summ>>'
```

## MENU

`MENU` — displays a popup menu anywhere in the game, whose items are written in the specified array. General syntax:

```qsp
MENU [$array name]
```

Before using this operator, you need to fill the array based on whose contents the menu items will be formed. Menu items are tuples of three values, sequentially placed in consecutive array cells starting from zero. The contents of each tuple should be approximately like this:

```qsp
["menu item name", "location name", "path to icon file"]
```

Menu item name is what we'll see on screen when the menu is displayed; location name is the name of the location whose code will be executed when clicking on the corresponding menu item; path to icon file is the path to the image file that will be displayed next to the menu item name.

Knowing this, we can fill the array to create our menu items:

```qsp
%stone[0] = ['Take stone', 'takestone']
%stone[1] = ['Throw stone', 'throwstone']
%stone[2] = ['Examine stone', 'lookstone']
```

Here the array name (`%stone`) is the menu name, and the tuples are actions for which item names and handler location names for menu item selection are specified. When selecting the "Take stone" item, the location named "takestone" will be called. Similarly for other items.

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

menu 'usr_menu' &! will show menu of 4 items
```

The menu ends on an array element with an empty tuple, or with a tuple missing a value for the menu item name or item handler location.

Examples where the last two menu items won't be created:

```qsp
%usr_menu[0]=['Take item','take_item'] & ! we'll see this item on screen
$usr_menu[1]=['Examine item','look_item'] & ! and we'll see this item on screen
$usr_menu[2]=[] & ! empty tuple, player will consider menu ended
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

To insert a separator in the menu, use a tuple with "-" values. I.e., if you need to put a separator instead of the 3rd element:

```qsp
%usr_menu[0]=['Take item','take_item']
$usr_menu[1]=['Examine item','look_item']
$usr_menu[2]=['-', '-'] & ! separator instead of menu item
$usr_menu[3]=['Put item','put_item']
```

An argument (`args[0]`) - the position of the selected item - is passed to the menu item selection handler location. Menu item positions are numbered from 1.

:::note[Deprecated array filling variant. Strings]

This variant can be used both in players version 5.9.0 and in earlier versions.

Here menu items are string values of an array with a special format:

```qsp
"menu item name:location name:path to icon file"
```

- Menu item name is what we'll see on screen when the menu is displayed;
- location name is the name of the menu item handler location whose code will be executed when clicking on the corresponding menu item;
- path to icon file is the path to the image file that will be displayed next to the menu item name. If the path to icon file is not specified or the specified file is unavailable, the menu item will be displayed without an icon.

The search for ":" symbols starts from the end of the string, meaning the menu item name can contain colons, but then there must be a colon after the location name, even if you don't use icons for menu items.

```qsp
$stone[0]='Stone: take:takestone:'
$stone[1]='Stone: throw:throwstone:'
$stone[2]='Stone: examine:lookstone:'
```

If the path to icon file is not specified or the specified file is unavailable, the menu item will be displayed without an icon.

Thus we should fill the array to create our menu items:

```qsp
$stone[0]='Take stone:takestone'
$stone[1]='Throw stone:throwstone'
$stone[2]='Examine stone:lookstone'
```

Here the array name (`$stone`) is the menu name, and the text array values are actions for which names and handler location names for menu item selection are specified. When selecting "Take stone", the location named "takestone" will be processed. Similarly for other items.

To call the menu on screen, use the `menu` operator:

```qsp
menu '$stone'
```

Menus can be called anywhere in the game, for example, from hyperlinks:

```qsp
'<a href="EXEC: menu `$stone`">Stone</a>'
```

Example of creating a menu with icons:

```qsp
! no icon
$usr_menu[0] = 'Take item:take_item'
! icon specified by gif file
$usr_menu[1] = 'Put item:put_item:images/put_item.gif'
! icon specified by $icon_file value
$usr_menu[2] = 'Examine item:look_item:<<$icon_file>>'
! menu item specified by 3 variables
$usr_menu[3] = '<<$name>>:<<$location>>:<<$file>>'

menu 'usr_menu' &! will show menu of 4 items
```

The menu ends on an array element with value `''` (empty string). I.e., if the menu array consists of elements 'Take', 'Examine', '', 'Throw', then the last 2 menu items won't be created:

```qsp
$usr_menu[0] = 'Take item:take_item' & ! we'll see this item on screen
$usr_menu[1] = 'Examine item:look_item' & ! and we'll see this item on screen
$usr_menu[2] = '' & ! empty value here, player will consider menu ended
$usr_menu[3] = 'Put item:put_item' & ! we won't see this item
```

To insert a separator in the menu, write `"-:-"` instead of the corresponding array element. I.e., if you need to put a separator instead of the 3rd element:

```qsp
$usr_menu[0] = 'Take item:take_item'
$usr_menu[1] = 'Examine item:look_item'
$usr_menu[2] = '-:-'
$usr_menu[3] = 'Put item:put_item'
```

:::

## MSG

`MSG` — displays the specified message in a dialog box. General syntax:

```qsp
MSG [message]
```

where `[message]` is any text string, number, expression of any type. Examples:

Examples:

```qsp
! simple message output.
msg 'Many ripe pears.'
! we get a window with message 'Many ripe pears'
```

```qsp
! Example of message in ACT action.
act 'Eat pears':
   msg 'Mmm pears are very tasty.'
end
! We get message output when clicking on action "Eat pears"
```

```qsp
!Example with condition.
if breadready = 1:
    msg 'Looks like the bread is ready.'
end
! We get message output when condition breadready = 1
```

## NL

`NL` — line break, then text output in the additional description window. General syntax:

```qsp
NL [$text]
```

where `[$text]` is any text string, number, or expression of any type. If `[$text]` is absent, a simple line break occurs. Example:

```qsp
p "Text without line break."
nl "Line break + text output."
p "Text without line break."
```

## OPENGAME

`OPENGAME` — loading the specified game state file. General syntax:

```qsp
OPENGAME [$path]
```

where `[$path]` is the path to the saved game state file. If the `[$path]` parameter is absent, the game state loading window is called.

Example:

```qsp
! load state from file 1.sav
opengame "1.sav"
! open state loading window
opengame
```

See also the game state loading event handler location ([$ongload](qsp-keyword-sys-var.md#ongload)).

## OPENQST

`OPENQST` — opening and running the specified game file. General syntax:

```qsp
OPENQST [$path]
```

where [$path] is the path to the game file to be run. Example:

```qsp
openqst "gamespool/cubesgame.qsp"
```

When using this operator, variables are not deleted, inventory objects are not removed, the additional description and input line are not cleared, and playing files are not stopped. If you need to clear the screen and all variable values, you can write such commands at the beginning of the loaded game file:

```qsp
killall & cls & close all
```

## P

`P` — text output to the additional description window without line break. Text output by any other operator immediately after p will add new text immediately after the current text. General syntax:

```qsp
P [$text]
```

where `[$text]` is any text string, number, or expression of any type. `[$text]` can be an empty string `''`, but should not be absent. Example:

```qsp
p "Text without line break."
p "Text without line break."
p ""
p "Text without line break."
```

## PL

`PL` — text output to the additional description window, then line break. General syntax:

```qsp
PL [$text]
```

where `[$text]` is any text string, number, or expression of any type. `[$text]` can be absent, then just a line break. Example:

```qsp
pl "Text output, then line break."
pl & ! line break without text output
pl "Text output, then line break."
p "Text without line break."
pl "Text output, then line break."
```

## PLAY

`PLAY` — playing the specified sound file with given volume. General syntax:

```qsp
PLAY [$path to sound file],[#volume]
```

where `[$path to sound file]` is the path to the sound file relative to the game file, `[#volume]` is playback volume as percentage from 0 to 100. The `[#volume]` parameter can be absent, in which case volume is taken as 100%. Examples:

```qsp
!Volume 100%
play 'sound/music.mp3'
!Volume 50%
play 'sound/music.mp3', 50
!Volume 0% (no sound)
play 'sound/music.mp3', 0
```

```qsp
!Playing file by address from variable $file
! with extension 'mid'
! and volume volume
$file = "melody"
play '<<$file>>.mid', volume
! similarly:
$file = "melody.mid"
play $file, volume
```

If the file is already playing, the volume changes without "restarting" it. Multiple audio formats are supported and simultaneous playback of up to 32 compositions.

## REFINT

`REFINT` — forced interface update (including color and font changes assigned using system variables).

By default, interface update occurs 2 times per second (every 500 ms). See also the [`settimer`](#settimer) operator.

## SAVEGAME

`SAVEGAME` — saving game state to the specified file. General syntax:

```qsp
SAVEGAME [$path]
```

where `[$path]` is the path to the created game state save file. If the `[$path]` parameter is absent, the game state save window is called.

Example:

```qsp
! save state to file 1.sav
savegame "1.sav"
! open state save window
savegame
```

See also [game state save event handler location ($ongsave)](qsp-keyword-sys-var.md#ongsave).

## SCANSTR

`SCANSTR` — searching for non-overlapping occurrences in a string that match a pattern, and placing these occurrences in an array. General syntax:

```qsp
SCANSTR [$array_name], [$text_to_parse], [$regexp], [#group_number]
```

where `[$array_name]` is the array where strings matching the regular expression `[$regexp]` are placed. The search is performed on string `[$text_to_parse]`. If parameter `[#group_number]` is specified, not the entire string matching the regular expression will be placed in the array, but only the part corresponding to the specified group in this regular expression.

Examples:

```qsp
! extract all words from string:
$text = 'Sasha walked down the highway, and Greka across the river.'
scanstr '$words', $text, '\b\w+\b'
!The $words array will contain values: 'Sasha', 'walked', 'down', 'highway', 'and', 'Greka', 'across', 'river'

! split string by delimiter:
$text = 'morning|day|evening|night'
scanstr '$words', $text, '[^|]+'
!The $words array will contain values: 'morning', 'day', 'evening', 'night'

! extract all words placed in square brackets from string, but without square brackets:
$text = '[first] ignoredtext [second][third] also ignored'
scanstr '$words', $text, '\[(.*?)\]', 1
!The $words array will contain values: 'first', 'second', 'third'
```

## SET

`SET` — operator for setting variables values. General syntax:

```qsp
SET [variable name] = [expression]
SET [variable 1], [variable 2], ... = [value 1], [value 2], ...
```

where `[variable name]` is a valid variable name, `[expression]` is a valid value for this variable.

Numeric variable names are written without the `$` symbol at the beginning. Text variable names are written with the `$` symbol at the beginning. Examples:

```qsp
! set text variable
set $text = "text string"
! set numeric variable
set abs = 123
! set tuple
set %tuple = [27, 184, 'steel']
! multiple assignment
set unit_power, $unit_name = 1300, 'DiggerBull'
! unpack the tuple
set $name, age, height = %npc_fields
```

:::note[Recommendation:]
Since assignment can be done without the `set` operator, we recommend using this operator only for cases when it improves code readability. For example, with multiple assignment:

```qsp
set apples_in_pocket, apples_in_basket, apples_at_Lyosha = 58, 11, 19
set $string_1, $string_2 = 'Greka Rode Across River', 'Greka Sees Crab In River'
```

:::

## SETTIMER

`SETTIMER` — sets the interval for accessing the counter location. General syntax:

```qsp
SETTIMER [#expression]
```

where `[#expression]` is the period of accessing the counter location in milliseconds. By default, the player accesses the counter location every 500 ms, i.e., 2 times per second.

Setting the counter location access period also affects the frequency of automatic interface settings update.

Examples:

```qsp
! counter location will be launched every 2 seconds:
settimer 2000
```

```qsp
! counter location will be launched 4 times per second:
settimer 250
```

```qsp
! if we set frequency of access (times per second)
frequency=10 & ! ten times per second
settimer 1000/frequency
```

```qsp
! if we set access period (after how many seconds)
period=2 & ! every two seconds
settimer 1000*period
```

The minimum period value can thus be 1 millisecond:

```qsp
settimer 1
```

However, in practice, the minimum value is limited by your computer's power, and it's usually higher than 1 millisecond.

## SETVAR

`SETVAR` — assigns a value to a variable or array cell.

This function allows avoiding the use of `dynamic` in cases where you need to assign a value to a variable whose name is not known in advance.

General syntax:

```qsp
SETVAR [$array_name], [value], [index]
```

where `[$array_name]` is the name of the array or variable to which the value should be assigned; `[value]` is a value of any type: string, number, tuple — however, the type of value that will be placed in the variable is determined by the type prefix before the variable name; `[index]` is if the value is assigned to an array cell, you need to specify the cell index with this parameter (can be of any type).

Examples:

```qsp
SETVAR 'A', 65
SETVAR '$X', 'name', 4
SETVAR '$X', 'name', 'string index'
SETVAR '%Q', ['example', 'tuple'], 3
SETVAR '%Q', ['example', 'tuple'], [x, y]

$arr_pref = '%'
$arr_name = 'tuple'
SETVAR $arr_pref+$arr_name, ['tuple', 1], 3
```

## SHOWACTS

`SHOWACTS` — controls the display of the actions window on screen. General syntax:

```qsp
SHOWACTS [#expression]
```

where `[#expression]` is a number. Usually values `0` and `1` are used. If the value of expression `[#expression]` is not zero, the actions window is displayed. If the value of expression `[#expression]` equals zero, the actions window is hidden. Examples:

```qsp
showacts 1 & ! shows actions list
showacts 0 & ! hides actions list
```

For code readability, you can pre-define `on` and `off` variables and use them:

```qsp
on = 1
off = 0
showacts on & ! shows actions list
showacts off & ! hides actions list
```

## SHOWINPUT

`SHOWINPUT` — controls the display of the input line on screen. General syntax:

```qsp
SHOWINPUT [#expression]
```

where `[#expression]` is a number. Usually values `0` and `1` are used. If the value of expression `[#expression]` is not zero, the input line is displayed. If the value of expression `[#expression]` equals zero, the input line is hidden. Examples:

```qsp
showinput on & ! shows input line
showinput off & ! hides input line
```

## SHOWOBJS

`SHOWOBJS` — controls the display of inventory on screen. General syntax:

```qsp
SHOWOBJS [#expression]
```

where `[#expression]` is a number. Usually values 0 and 1 are used. If the value of expression `[#expression]` is not zero, inventory is displayed. If the value of expression `[#expression]` equals zero, inventory is hidden. Examples:

```qsp
showobjs 1 & ! shows inventory
showobjs 0 & ! hides inventory
```

For code readability, you can pre-define `on` and `off` variables and use them:

```qsp
on = 1
off = 0
showobjs on & ! shows inventory
showobjs off & ! hides inventory
```

## SHOWSTAT

`SHOWSTAT` — controls the display of the additional description window on screen. General syntax:

```qsp
SHOWSTAT [#expression]
```

where `[#expression]` is a number. Usually values `0` and `1` are used. If the value of expression `[#expression]` is not zero, the additional description window is displayed. If the value of expression `[#expression]` equals zero, the additional description window is hidden. Examples:

```qsp
showstat 1 & ! shows additional description window
showstat 0 & ! hides additional description window
```

For code readability, you can pre-define `on` and `off` variables and use them:

```qsp
on = 1
off = 0
showstat on & ! shows additional description window
showstat off & ! hides additional description window
```

## SORTARR

`SORTARR` — sorting the specified array. General syntax:

```qsp
SORTARR [$array_name], [#order]
```

Here `[$array_name]` is the name of the array to be sorted. The `[#order]` parameter can be omitted. If not specified or equals `0`, sorts the array in ascending order (from smaller to larger). If equals `1`, sorts the array in descending order (from larger to smaller).

Can sort arrays of any types (numbers, strings, tuples), but mixing values of different types in one array is not allowed.

To specify the type of sorted values, you need to specify the type prefix as part of the array name (`$`, `%`).

Example of sorting a text array:

```qsp
$a[] = 'nn'
$a[] = 'zz'
$a[] = 'aa'
sortarr '$a'

!check sorting result:
loop local i=0 while i<arrsize('$a') step i+=1:
  *pl $a[i]
end
```

## UNPACKARR

`UNPACKARR` — unpacking a tuple into the specified array. General syntax:

```qsp
UNPACKARR [$array_name], [%tuple], [#start_index], [#count]
```

where `[$array_name]` is the array where we want to place the unpacked values; `[%tuple]` is the tuple we want to unpack; `[#start_index]` is the element number in the tuple from which we want to extract values into the array; `[#count]` is the number of tuple elements we want to place in the array.

Tuple element indexing starts from `0`.

The operator allows making tuple slices, including slices of one element. I.e., using this operator we can extract a separate element from a tuple without using a loop.

Examples:

```qsp
UNPACKARR 'A', ['test','several','values',67, ['nested tuple']]
! $A[0] will contain 'test'
! $A[1] will contain 'several'
! $A[2] will contain 'values'
! A[3] will contain 67
! %A[4] will contain ['nested tuple']

%tpl = ['test','several','values',67, ['nested tuple']]
UNPACKARR 'A', %tpl, 3, 1
! A will contain 67
```

## UNSELECT

`UNSELECT` — canceling object selection. Has a short form `unsel`.

When a player clicks on any object, it remains selected. To remove selection from an object, use this operator. Usually it's placed on the object selection handler location.

```qsp
if $selobj='Orange':
    *P 'Delicious sweet orange. There are many of us, but only one of it.'
end
if $selobj = 'Teapot':
    p 'The most ordinary cast iron teapot.'
end
...
if $selobj='Screwdriver':
    menu '$screwdriver'
end
unsel
```

## VIEW

`VIEW` — displays the specified image on screen. In the classic player, the image is displayed in a separate window (preview window), in qSpider the image is displayed as a layer. General syntax:

```qsp
VIEW [$path to graphics file]
```

where `[$path to graphics file]` is the path to the image file. If the `[$path to graphics file]` parameter is absent, or specified as `''` (empty string), the preview window closes.

Examples:

```qsp
! display image in preview window
view 'content/monster.png'
! close preview window
view ''

! preview window can also be closed like this
view
```

## WAIT

`WAIT` — pausing program code execution for the specified number of milliseconds. General syntax:

```qsp
WAIT [#milliseconds]
```

where `[#milliseconds]` is the time in milliseconds for which program code execution should be stopped.

Example:

```qsp
! stop program execution for 5 seconds
wait 5000
```

:::warning[Caution!]
This operator should be used with caution, since pausing code execution blocks the player's ability to interact with the game.
:::

`WAIT` not only interrupts code execution but also forces the player to output information from the screen buffer. During normal location code execution, all text for operators `*pl`, `*p` `pl`, `nl`, etc. is placed in a special screen buffer, and only after executing all code on the location is it output to the screen. When using `WAIT`, text from the buffer is output immediately at the moment `WAIT` is executed, which is sometimes useful because it allows tracking changes in some values step by step.

In the example below, numbers will first be written to the screen buffer and only then appear on screen:

```qsp
loop i=0 while i<5 step i+=1:
    *p i
end
*pl
```

In the next example, they will be output one after another with an interval of about 100 ms.

```qsp
loop i=0 while i<5 step i+=1:
    wait 100
    *p i
end
*pl
```

## XGOTO

`XGOTO` — transition to the specified location without clearing the main description window. General syntax:

```qsp
XGOTO [$location], [argument 0], [argument 1], ... , [argument 18]
```

where `[$location]` is the name of the location to which the transition should be made. Arguments `[argument 0]`, `[argument 1]`, etc. can be used on this location, their values are automatically placed in variables `args[0]`, `args[1]`, etc. respectively. Using arguments is not mandatory.

When transitioning to a new location using `xgoto`, the main description window is not cleared, and the base description of the new location is added to the existing text in the main description window. The actions list is cleared, then base actions are output to the actions window, and code from the "Execute on visit" field of location `[$location]` is executed. Also, when transitioning to a new location, the value returned by the `$curloc` function changes.

Examples:

```qsp
! transition to location "house".
! The args array at location "house" will be empty.
xgoto 'house'
```

```qsp
! transition to location "street" with passing 2 parameters.
! at location "street" args[0] equals 1,
! $args[1] contains string "data".
xgoto 'street', 1, 'data'
```

The operator has a short form `xgt`:

```qsp
XGT [$location], [argument 0], [argument 1], ... , [argument 18]
```
