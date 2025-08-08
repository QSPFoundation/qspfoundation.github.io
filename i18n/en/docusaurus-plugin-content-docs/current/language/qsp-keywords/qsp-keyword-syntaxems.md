---
id: qsp-keyword-syntaxems
title: Syntax Elements and Special Symbols
sidebar_position: 5
---

# Syntax Elements and Special Symbols

:::tips[Definition]

In the context of programming, a syntax element can be considered as a **minimal unit of syntax** that defines the structure and rules for writing code.

Thus, a syntax element can be a variable, operator, function, declaration keyword, or special symbols used to structure code.

:::

Here are syntax elements/special symbols not included in other sections with keywords and system variables.

## END

Keyword (operator) marking the end of a multi-line construct. Actions, conditional constructs, and loops can be multi-line. Examples:

```qsp
! open condition
if obj "Jug":
    *pl "You have a jug."
! close condition
end

! open action
act "Take apple":
    apple += 1
    addobj "Apple"
! close action
end

loop local i = 0 while i < 10 step i += 1:
    *pl "Pass <<i+1>>: i=<<i>>"
end
```

Each multi-line construct must end with the `end` keyword. However, the same rules apply here as for HTML tags or brackets: if we nest one construct inside another, we must first close the last opened construct:

```qsp
! open condition
if obj "Empty jug":
    ! code related to the condition
    *pl "You have an empty jug."
    ! open action
    act "Fill jug":
        ! code related to the action
        delobj "Empty jug"
        addobj "Full jug"
    ! close ACTION
    end
    *pl "The jug can be filled from the well."
! close CONDITION
end
```

You can use not just `end`, but `end if`, `end act` and `end loop`:

```qsp
! open action
act "Buy 10 arrows at 5 rubles each":
    ! open condition level 1
    if money >= 10 * 5:
        arrow += 10
        money -= 10 * 5
        ! open condition level 2
        if no (obj "Arrows"):
            addobj "Arrows"
        ! close condition level 2
        end if
    else
        *pl "You don't have enough money."
    ! close condition level 1
    end if
! close action
end act
```

Generally, any text is allowed after the `end` keyword, but not approved. All text until the next command is ignored. If a command is written on the same line as `end`, this command must come after an ampersand (`&`):

```qsp
! open action
act "Take apple":
    apple += 1
    addobj "Apple"
! close action
end the presence of this text after end is not approved & *pl "New command"
```

## Labels `:`

Labels are special syntactic constructs (or rather less than constructs — syntax elements) that mark the specified code line and serve for quick movement to such lines using the [`JUMP`](qsp-keyword-operators.md#jump) operator. General syntax:

```qsp
:[label_name]
```

, where `[label_name]` — theoretically any combination of symbols, but in practice it's desirable to use only letters, numbers, underscores, and spaces. Spaces and tabs can precede the colon in any amount. Adjacent spaces and tabs around the label name are also ignored (but not recommended for code readability).

```qsp
! recommended label usage
jump 'label'
! ...
:label
```

```qsp
! working variant with ignored adjacent spaces in label
jump "label with adjacent spaces"
! ...
: label with adjacent spaces
```

```qsp
! working variant with ignored adjacent spaces in jump
jump "  label with adjacent spaces  "
! ...
:label with adjacent spaces
```

Any other commands can follow directly after the label on the same line through an ampersand (`&`), but this is not recommended.

```qsp
! label with commands after it
jump 'markdown'
! ...
:markdown & *pl "output text" & ! comment
```

Labels are case-insensitive:

```qsp
jump "FoR"
! ...
:for
```

The `jump` operator "sees" labels only within the current code block. In other words, labels are local.

Labels with identical names can be located on different locations (in different code blocks).

If labels with identical names are located in one code block, all duplicate labels except the first one are ignored by the player.

Separate code blocks for labels are considered:

* "Execute on visit" code of a specific location (each location is a separate code block),
* action code even if the action is added programmatically,
* code in hyperlinks,
* code passed to `DYNAMIC`/`DYNEVAL`.

Labels inside loops belong to the same code block where the loop is located.

If an action is added programmatically, labels placed in this action become available from the code block where this action was created. However, from the action it's impossible to jump to a label located outside the action.

Random labels, i.e., labels that have no jump to them with `jump` in the current code block, are simply ignored by the interpreter.

## Ampersand `&`

`&` — the ampersand symbol serves to list commands on one line. General syntax:

```qsp
[command 1] & [command 2] & ...
```

This symbol should not be confused with the [string concatenation operation](qsp-keyword-operacion.md#-concatenation), and should be used carefully.

Examples:

```qsp
*pl "I picked an apple from the branch." & addobj "Apple" & apple+=1

a = 3 & b = 7 & g = rand(1, 6) & ("26" & "27") & ! in parentheses — concatenation
```

## Comma `,`

The comma `,` in QSP is used to list arguments passed to various operators and functions:

```qsp
rgb(25, 67, 250)

max(12, 45, 67, 89, 90, 122, 135, 168, 90)

addobj "Screwdriver", "img/screwdriver.png"

gosub "add_object", "Orange", 2, "Food", 37
```

The comma is also used to list values in a tuple:

```qsp
%personage = [26, 192, 85, 'Peter', 'boxer']
```

## Round Brackets `()`

Round brackets `()` in QSP are used in three cases:

1. In various expressions, brackets increase operation priority (operations in brackets are executed first):

    ```qsp
    ! increasing priority of arithmetic operations
    (256 + 789) * (789 - 256)
    ! increasing priority of comparison operations
    if A = (A <> B): ...
    ```

2. If you need to pass more than one argument to a function, you should place the entire group of arguments in brackets:

    ```qsp
    rgb(25, 67, 250)
    max(12, 45, 67, 89, 90, 122, 135, 168, 90)
    rand(1, 1000)
    ```

    It's good practice to place even one function argument in brackets:

    ```qsp
    rand(999)
    ```

    It won't be criticized, though it's not usually done, to place argument groups for operators in brackets:

    ```qsp
    showinput(0)

    addobj("Screwdriver", "img/screwdriver.png")

    gosub("add_object", "Orange", 2, "Food", 37)
    gosub("add_object", "Rec", rand(23, 45), "Artifact", max(36, 67, 90, a))
    ```

3. If you need to organize a tuple of values:

    ```qsp
    %tuple = (123, 234, 'string')
    %mass[23] = ('Petrov', 'Peter', 'Petrovich')
    ```

:::warning[Recommendation!]
For organizing tuples, it's recommended to use square brackets.

```qsp
%tuple = [123, 234, 'string']
%mass[23] = ['Petrov', 'Peter', 'Petrovich']
```

:::

## Square Brackets `[]`

Square brackets `[]` in QSP are used to specify the index of an array cell:

```qsp
! assign value to the seventh cell of array $mass
$mass[7] = "textstring"
```

You can use string values for array cell indexing:

```qsp
$mass["x:4,y:6"] = "map-dot"
```

You can also use tuples for array cell indexing. Duplicating brackets is not necessary:

```qsp
$mass[4, 6] = "map_cell"
! equivalent to
$mass[[4, 6]] = "map_cell"
```

If square brackets don't follow the array name, work is done with the zero cell of the array:

```qsp
$mass = "text"
! equivalent to
$mass[0] = "text"
```

If the index in square brackets is not specified, we work with the last cell of the array:

```qsp
! create new cell at the end of array and assign value to it
$mass[] = "last_cell"

! get value from the last array cell:
$mass[]
```

Square brackets are also used to create tuples:

```qsp
%tuple = [123, 234, 'string']
%mass[23] = ['Petrov', 'Peter', 'Petrovich']
```

## Curly Brackets `{}`

Curly brackets `{}` in QSP act as special symbols marking the beginning and end of string values. In other words, by the presence of such brackets, the player can understand where a string value begins and ends:

```qsp
*pl {Text that will be output to the screen.}
```

The feature of specifying text value using curly brackets is that sub-expressions are not expanded in such strings:

```qsp
health = 150
*pl {Health: <<health>>}
! the text 'Health: <<health>>' will be output to the screen
*pl "Health: <<health>>"
! the text 'Health: 150' will be output to the screen
```

For better compatibility with various player versions, and for reading convenience, curly brackets should mainly be used for writing code intended for the `dynamic` operator or `dyneval` function:

```qsp
*pl $dyneval({$result = $mid("abcd", 2, 1) + "qwerty"})
dynamic {
    $args[0]
    addobj $args[1]
}, 'Text', 'Fork'
```

Curly brackets can also be used for writing multi-line comments:

```qsp
! {
    multi-line
    comment
}
```

Any number of curly brackets can be nested within each other.

## Quote `"`

Quotes `"` (double apostrophe) in QSP act as a special symbol marking the beginning and end of string values. In other words, by the presence of quotes, the player can understand where a string value begins and ends:

```qsp
*pl "Text that will be output to the screen."
```

The feature of specifying text value using quotes is that sub-expressions are expanded in such strings:

```qsp
health = 150
*pl "Health: <<health>>"
! the text 'Health: 150' will be output to the screen
```

Quotes inside a string can be escaped by doubling:

```qsp
*pl "At the tavern ""At Mo's"" it's cheerful and noisy today."
```

Quotes can also be used for writing multi-line comments:

```qsp
! "
    multi-line
    comment
"
```

## Apostrophe `'`

Apostrophe `'` in QSP acts as a special symbol marking the beginning and end of string values. In other words, by the presence of apostrophes, the player can understand where a string value begins and ends:

```qsp
*pl 'Text that will be output to the screen.'
```

The feature of specifying text value using apostrophes is that sub-expressions are expanded in such strings:

```qsp
health = 150
*pl 'Health: <<health>>'
! the text 'Health: 150' will be output to the screen
```

Apostrophes inside a string can be escaped by doubling:

```qsp
*pl 'Rug''Sta''Rag said: — What do you want, mora? Want a fly agaric?'
```

Apostrophes can also be used for writing multi-line comments:

```qsp
! '
    multi-line
    comment
'
```

## "At" Symbol `@`

The "at" symbol `@` is used to organize implicit function-location calls, simplifying notation and replacing the `gosub` operator or `func` function. General syntax:

```qsp
@[$location]([argument 0], [argument 1], ... , [argument 18])
```

, where `[$location]` — the name of the location whose code we want to execute without direct transition to it. Arguments `[argument 0]`, `[argument 1]`, etc. can be used at this location, their values are automatically placed in variables `args[0]`, `args[1]`, etc. respectively. After processing the location, previous `args` values are restored. Using arguments is not mandatory; in this case, brackets can be omitted.

When calling a location using `@`, the base description of the location is added to the current description, base actions are added to current actions, and operators in the "Execute on visit" field are executed, then return to the original line (continue code execution after the command with `@`).

The location name in implicit calls must not contain special characters, otherwise this may lead to non-working code. You can use letters, numbers, underscores, and dots.

Examples:

```qsp
!processing location "move". The args[] array is empty.
@move()

!processing location "move" with 3 parameters passed.
! $args[0] = $var (value), args[1] = 2,
! $args[2] = "data". Note the ' symbols.
@move($var, 2, 'data')
```

```qsp
! this is code calling location "transition"
@transition('location')

! and this is code of the "transition" location itself
# transition
*pl $args[0]  & ! the text 'location' will be output to the screen
! a new action will appear in the actions window:
act 'go':
    goto "street"
end
- transition
```

```qsp
! location code for function getting sum of series of numbers from one to specified value
# summ
! args[0] will contain the number we specify as [argument 0]
loop while args[0] > 0 step args[0] -= 1:
    result += args[0]
end
- summ

! example of calling location "summ" as function
*pl @summ(19) & ! will output 190 to screen
```

:::warning[Pay attention!]
Implicit function-location call replaces both `gosub` and `func`, therefore:

1. if your function-location returns a result, implicit call of such location will work exactly like explicit call through `func`;
2. if the function-location does not return a result, then when using it with the **[implicit operator](qsp-keyword-operators.md#implicit-operator)** it will work like explicit call through `gosub`.

:::

## Dollar Sign `---
sidebar_position: 5
---

# Syntax Elements and Special Symbols

:::tips[Definition]

In the context of programming, a syntax element can be considered as a **minimal unit of syntax** that defines the structure and rules for writing code.

Thus, a syntax element can be a variable, operator, function, declaration keyword, or special symbols used to structure code.

:::

Here are syntax elements/special symbols not included in other sections with keywords and system variables.

## END

Keyword (operator) marking the end of a multi-line construct. Actions, conditional constructs, and loops can be multi-line. Examples:

```qsp
! open condition
if obj "Jug":
    *pl "You have a jug."
! close condition
end

! open action
act "Take apple":
    apple += 1
    addobj "Apple"
! close action
end

loop local i = 0 while i < 10 step i += 1:
    *pl "Pass <<i+1>>: i=<<i>>"
end
```

Each multi-line construct must end with the `end` keyword. However, the same rules apply here as for HTML tags or brackets: if we nest one construct inside another, we must first close the last opened construct:

```qsp
! open condition
if obj "Empty jug":
    ! code related to the condition
    *pl "You have an empty jug."
    ! open action
    act "Fill jug":
        ! code related to the action
        delobj "Empty jug"
        addobj "Full jug"
    ! close ACTION
    end
    *pl "The jug can be filled from the well."
! close CONDITION
end
```

You can use not just `end`, but `end if`, `end act` and `end loop`:

```qsp
! open action
act "Buy 10 arrows at 5 rubles each":
    ! open condition level 1
    if money >= 10 * 5:
        arrow += 10
        money -= 10 * 5
        ! open condition level 2
        if no (obj "Arrows"):
            addobj "Arrows"
        ! close condition level 2
        end if
    else
        *pl "You don't have enough money."
    ! close condition level 1
    end if
! close action
end act
```

Generally, any text is allowed after the `end` keyword, but not approved. All text until the next command is ignored. If a command is written on the same line as `end`, this command must come after an ampersand (`&`):

```qsp
! open action
act "Take apple":
    apple += 1
    addobj "Apple"
! close action
end the presence of this text after end is not approved & *pl "New command"
```

## Labels `:`

Labels are special syntactic constructs (or rather less than constructs — syntax elements) that mark the specified code line and serve for quick movement to such lines using the [`JUMP`](qsp-keyword-operators.md#jump) operator. General syntax:

```qsp
:[label_name]
```

, where `[label_name]` — theoretically any combination of symbols, but in practice it's desirable to use only letters, numbers, underscores, and spaces. Spaces and tabs can precede the colon in any amount. Adjacent spaces and tabs around the label name are also ignored (but not recommended for code readability).

```qsp
! recommended label usage
jump 'label'
! ...
:label
```

```qsp
! working variant with ignored adjacent spaces in label
jump "label with adjacent spaces"
! ...
: label with adjacent spaces
```

```qsp
! working variant with ignored adjacent spaces in jump
jump "  label with adjacent spaces  "
! ...
:label with adjacent spaces
```

Any other commands can follow directly after the label on the same line through an ampersand (`&`), but this is not recommended.

```qsp
! label with commands after it
jump 'markdown'
! ...
:markdown & *pl "output text" & ! comment
```

Labels are case-insensitive:

```qsp
jump "FoR"
! ...
:for
```



Acts as a type prefix for naming variables and functions of string type. It must be specified if you want to assign a string value to a variable:

```qsp
$string = 'This is so long string. Very very long string'
```

If you don't specify the dollar sign before the string type variable name during assignment, this will cause error #101: "Data type mismatch":

```qsp title="Don't do this!"
string = 'Short string'
```

If you assigned a value of another type to a variable and try to get a string, this won't cause a data type mismatch error, but the variable will return a value corresponding to the default value for string values, i.e., an empty string (`''`).

```qsp
number = 123
*pl 'Number ' + $number + '.'
! we'll see 'Number .' on screen because $number will return an empty string.
```

## Percent Sign `%`

Acts as a type prefix for naming variables and functions containing or returning tuples. It must be specified if you want to assign a tuple to a variable:

```qsp
%tuple = [13, 37, 'string']
```

If you don't specify the percent sign before the tuple type variable name during assignment, this will cause error #101: "Data type mismatch":

```qsp title="Don't do this!"
tuple = [13, 37, 'string']
```

If you assigned a value of another type to a variable and try to get a tuple, this won't cause a data type mismatch error, but the variable will return a value corresponding to the default value, i.e., empty strings (`''`) if a text value is extracted, or zeros (`0`) if a numeric value is extracted.

```qsp
number = 123
$var[0], $var[1] = %number
*pl '[<<$var[0]>>,<<$var[1]>>]'
! We'll see '[,]' on screen
```