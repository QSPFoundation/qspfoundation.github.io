---
sidebar_position: 5
---

# Syntaxemes and Special Characters

:::tip[Definition]

In the context of programming, a syntaxeme can be considered as a **minimal unit of syntax** that defines the structure and rules for writing code.

A syntaxeme can be a variable, operator, function, declaration keyword, or special symbols used to structure code.

:::

This section presents syntaxemes/special characters not covered in other sections with keywords and system variables.

## END

A keyword (operator) marking the end of a multi-line construct. Multi-line constructs can include actions, conditional statements, and loops. Examples:

```qsp
! open condition
if obj "Pitcher":
    *pl "You have a pitcher."
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
if obj "Empty pitcher":
    ! code that belongs to the condition
    *pl "You have an empty pitcher."
    ! open action
    act "Fill pitcher":
        ! code that belongs to the action
        delobj "Empty pitcher"
        addobj "Full pitcher"
    ! close ACTION
    end
    *pl "The pitcher can be filled from the well."
! close CONDITION
end
```

You can use not just `end`, but also `end if`, `end act`, and `end loop`:

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

Generally, after the `end` keyword, any text is allowed but not recommended. All text until the next command is ignored. If a command is written on the same line as `end`, then this command must come after an ampersand (`&`):

```qsp
! open action
act "Take apple":
    apple += 1
    addobj "Apple"
! close action
end presence of this text after end is not recommended & *pl "New command"
```

## Labels `:`

Labels are special syntactic constructs (or rather, less than constructs — syntaxemes) that mark a specified line of code and serve for quick movement to such lines using the [`JUMP`](qsp-keywords-statements.md#jump) operator. General syntax:

```qsp
:[label name]
```

where `[label name]` is theoretically any combination of characters, but in practice it's advisable to use only letters, numbers, underscores, and spaces. Space and tab characters can precede the colon in any quantity. Adjacent space and tab characters around the label name are also ignored (however, it's not recommended to place them for code readability).

```qsp
! recommended way to use labels
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

Immediately after a label, on the same line, any other commands can follow after an ampersand (`&`), but this is not recommended.

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

Labels with the same names can be located on different locations (in different code blocks).

If labels with the same names are located in the same code block, all duplicate labels except the very first one are ignored by the player.

Separate code blocks for labels are considered:

* "Execute on visit" code of a specific location (each location is a separate code block),
* action code even if the action was added programmatically,
* code in a hyperlink,
* code passed to `DYNAMIC`/`DYNEVAL`.

Labels inside loops belong to the same code block where the loop is located.

If an action is added programmatically, labels placed in this action become available from the code block where this action was created. However, it's impossible to jump from an action to a label located outside the action.

Random labels, i.e., labels that have no jump to them via `jump` in the current code block, are simply ignored by the interpreter.

## Ampersand `&`

`&` — the ampersand symbol serves to enumerate commands on one line. General syntax:

```qsp
[command 1] & [command 2] & ...
```

This symbol should not be confused with the [string concatenation operation](qsp-keywords-operators.md#-concatenation), and should be used carefully.

Examples:

```qsp
*pl "I picked an apple from the branch." & addobj "Apple" & apple+=1

a = 3 & b = 7 & g = rand(1, 6) & ("26" & "27") & ! in parentheses — concatenation
```

## Comma `,`

The comma `,` in QSP is used to enumerate arguments passed to various operators and functions:

```qsp
rgb(25, 67, 250)

max(12, 45, 67, 89, 90, 122, 135, 168, 90)

addobj "Screwdriver", "img/screwdriver.png"

gosub "add_object", "Orange", 2, "Food", 37
```

The comma is also used to enumerate values in a tuple:

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

    It would be good practice to place even a single function argument in brackets:

    ```qsp
    rand(999)
    ```

    It won't be criticized, although it's not usually done, to place groups of arguments to operators in brackets:

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
! assign a value to the seventh cell of the $mass array
$mass[7] = "textstring"
```

String values can be used for array cell indexing:

```qsp
$mass["x:4,y:6"] = "map-dot"
```

Tuples can also be used for array cell indexing. Duplicating brackets is not mandatory:

```qsp
$mass[4, 6] = "map_cell"
! equivalent to
$mass[[4, 6]] = "map_cell"
```

If square brackets don't follow the array name, it means we're working with the zero cell of the array:

```qsp
$mass = "text"
! equivalent to
$mass[0] = "text"
```

If the index in square brackets is not specified, it means we're working with the last cell of the array:

```qsp
! create a new cell at the end of the array and assign it a value
$mass[] = "last_cell"

! get value from the last array cell:
$mass[]
```

Square brackets are also used to create tuples:

```qsp
%tuple = [123, 234, 'string']
%mass[23] = ['Petrov', 'Peter', 'Petrovich']
```

## Curly Braces `{}`

Curly braces `{}` in QSP act as special symbols marking the beginning and end of string values. In other words, by the presence of such braces, the player can understand where a string value begins and ends:

```qsp
*pl {Text that will be displayed on screen.}
```

A special feature of specifying text values using curly braces is that sub-expressions are not expanded in such strings:

```qsp
health = 150
*pl {Health: <<health>>}
! the text 'Health: <<health>>' will be displayed on screen
*pl "Health: <<health>>"
! the text 'Health: 150' will be displayed on screen
```

For better compatibility with different player versions, as well as for reading convenience, curly braces should be used mainly for writing code intended for the `dynamic` operator or `dyneval` function:

```qsp
*pl $dyneval({$result = $mid("abcd", 2, 1) + "qwerty"})
dynamic {
    $args[0]
    addobj $args[1]
}, 'Text', 'Fork'
```

Curly braces can also be used for writing multi-line comments:

```qsp
! {
    multi-line
    comment
}
```

Any number of curly braces can be nested within each other.

## Quote `"`

Quotes `"` (double apostrophe) in QSP act as special symbols marking the beginning and end of string values. In other words, by the presence of quotes, the player can understand where a string value begins and ends:

```qsp
*pl "Text that will be displayed on screen."
```

A special feature of specifying text values using quotes is that sub-expressions are expanded in such strings:

```qsp
health = 150
*pl "Health: <<health>>"
! the text 'Health: 150' will be displayed on screen
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

The apostrophe `'` in QSP acts as a special symbol marking the beginning and end of string values. In other words, by the presence of apostrophes, the player can understand where a string value begins and ends:

```qsp
*pl 'Text that will be displayed on screen.'
```

A special feature of specifying text values using apostrophes is that sub-expressions are expanded in such strings:

```qsp
health = 150
*pl 'Health: <<health>>'
! the text 'Health: 150' will be displayed on screen
```

Apostrophes inside a string can be escaped by doubling:

```qsp
*pl 'Rug''Sta''Rag said: — What do you want, mora? Do you want a fly agaric?'
```

Apostrophes can also be used for writing multi-line comments:

```qsp
! '
    multi-line
    comment
'
```

## Commercial "At" Symbol `@`

The commercial "at" symbol `@` is used to organize implicit calling of location-functions, simplifying syntax and replacing the `gosub` operator or `func` function. General syntax:

```qsp
@[$location]([argument 0], [argument 1], ... , [argument 18])
```

where `[$location]` is the name of the location whose code we want to execute without directly going to it. Arguments `[argument 0]`, `[argument 1]`, etc. can be used on this location, their values are automatically placed in variables `args[0]`, `args[1]`, etc. respectively. After processing the location, previous `args` values are restored. Using arguments is not mandatory; in this case, brackets can be omitted.

When accessing a location using `@`, the base description of the location is added to the current description, base actions are added to current actions, and operators in the "Execute on visit" field are executed, then return to the original line (continuing code execution after the command with `@`).

The location name in implicit calling should not contain special characters, otherwise this may lead to non-functional code. You can use letters, numbers, underscores, and periods.

Examples:

```qsp
!processing location "move". The args[] array is empty.
@move()

!processing location "move" with passing 3 parameters.
! $args[0] = $var (value), args[1] = 2,
! $args[2] = "data". Note the '$' symbols.
@move($var, 2, 'data')
```

```qsp
! this is the code for calling location "transition"
@transition('location')

! and this is the code of the location "transition" itself
# transition
*pl $args[0]  & ! the text 'location' will be displayed on screen
! a new action will appear in the actions window:
act 'go':
    goto "street"
end
- transition
```

```qsp
! location code for a function that gets the sum of a series of numbers from one to the specified value
# summ
! args[0] will contain the number we specify as [argument 0]
loop while args[0] > 0 step args[0] -= 1:
    result += args[0]
end
- summ

! example of calling location "summ" as a function
*pl @summ(19) & ! will display 190 on screen
```

:::warning[Note!]
Implicit location-function calling replaces both `gosub` and `func`, therefore:

1. if your location-function returns a result, implicit calling of such a location will work exactly the same as explicit calling through `func`;
2. if the location-function doesn't return a result, then when using it with the **[implicit operator](qsp-keywords-statements.md#implicit-operator)** it will work like explicit calling through `gosub`.

:::

## Dollar Sign Symbol `$`

Acts as a type prefix for naming variables and functions of string type. It must be specified if you want to assign a string value to a variable:

```qsp
$string = 'This is so long string. Very very long string'
```

If you don't specify the dollar sign before the string type variable name during assignment, this will cause error #101: "Data type mismatch":

```qsp title="Don't do this!"
string = 'Short string'
```

If you assigned a variable a value of another type and try to get a string, this won't cause a data type mismatch error, but the variable will return a value corresponding to the default value for string values, i.e., an empty string (`''`).

```qsp
number = 123
*pl 'Number ' + $number + '.'
! we'll see 'Number .' on screen because $number will return an empty string.
```

## Percent Sign Symbol `%`

Acts as a type prefix for naming variables and functions containing or returning tuples. It must be specified if you want to assign a tuple to a variable:

```qsp
%tuple = [13, 37, 'string']
```

If you don't specify the percent sign before the tuple type variable name during assignment, this will cause error #101: "Data type mismatch":

```qsp title="Don't do this!"
tuple = [13, 37, 'string']
```

If you assigned a variable a value of another type and try to get a tuple, this won't cause a data type mismatch error, but the variable will return a value corresponding to the default value, i.e., empty strings (`''`) if a text value is extracted, or zeros (`0`) if a numeric value is extracted.

```qsp
number = 123
$var[0], $var[1] = %number
*pl '[<<$var[0]>>,<<$var[1]>>]'
! We'll see '[,]' on screen
```
