---
id: qsp-keyword-operacion
sidebar_position: 1
---

# Operations

List of operations for player version 5.8.0 in ascending order of priority:

- `OR`
- `AND`
- `NO`
- `=`, `<`, `>`, `!`, `<>`, `<=`, `>=`, `=<`, `=>` (comparison operations)
- `OBJ`, `LOC`
- `&` (concatenation)
- `+`, `-` (addition, subtraction)
- `MOD`
- `*`, `/` (multiplication, division)
- `-` (unary minus)
- `([expr])` - expressions in brackets

Operations written on one line have equal priority and are executed in order from left to right if present at the same level in an expression.

Operations in brackets have priority over other operations.

Function value calculation has priority over all operations.

A numeric expression whose value is not `0` is considered true. When the value is `0`, the expression is considered false. For the "true" value, it's strongly recommended to use `1` for compatibility with logical operations and functions returning logical values.

:::note[5.7.0]
In older player versions, the priority order was different.

- `&`
- `OR`
- `AND`
- `OBJ`, `LOC`, `NO`
- `=`, `<`, `>`, `!`, `<>`, `<=`, `>=`, `=<`, `=>`
- `+`, `-`
- `MOD`
- `*`, `/`
- `+`, `-` (unary)

:::

**Some features of comparison operations:**

- Comparison operations return `1` (true) or `0` (false) depending on the comparison result.
- When comparing numbers, everything is simple:
  - of two positive numbers, the positive number with greater magnitude will be considered greater;
  - a negative number is always less than a non-negative (positive and zero);
  - a positive number is always greater than a non-positive (negative and zero);
  - of two negative numbers, the negative number with greater magnitude will be considered smaller.
- When comparing strings, character-by-character comparison occurs from left to right:
  - the character that comes later in the character table is considered greater. You can rely on alphabetical sequence of characters to understand which string will be greater. Then character '`z`' will be greater than character '`a`'. Examples:

  ```qsp
  'z' > 'a' & ! returns 1
  'z' > 'az' & ! returns 1
  'akz' > 'akk' & ! returns 1
  ```

  - when comparing any non-empty string with an empty string, the empty string will be considered smaller:

  ```qsp
  ' ' > '' & ! returns 1
  'a' > '' & ! returns 1
  'z' > '' & ! returns 1
  'akzakz' > 'akzak' & ! returns 1
  ```

  :::tip[You can consider]
  that missing characters in a string are empty characters (empty strings), which when compared with any other character turn out to be smaller.
  :::

  - when comparing a string with a number, the player will try to convert both values to numbers. If successful, numbers will be compared. If unsuccessful — the number will be converted to a string, and strings will be compared.

  ```qsp
  'zzz' > 123 & ! returns 1
  '123' > 92 & ! returns 1
  '123' > '92' & ! returns 0
  ```

- When comparing tuples, element-by-element comparison occurs from left to right:
  - the tuple whose element turned out to be greater will be considered greater:

  ```qsp
  [1, 2, 3] > [1, 2, 2] & ! returns 1
  [2, 2, 3] > [1, 2, 3] & ! returns 1
  ```

  - when comparing any non-empty tuple with an empty tuple, the empty tuple will be considered smaller:

  ```qsp
  [1] > [] & ! returns 1
  [''] > [] & ! returns 1
  [0] > [] & ! returns 1
  [1, 2] > [1] & ! returns 1
  [1, 2] < [9] & ! returns 1
  ```

  :::tip[You can consider]
  that missing elements in a tuple are empty elements, which when compared with any other element turn out to be smaller.
  :::

  - when comparing tuples with numbers or strings, the number or string will be compared as a tuple of one element. For easier understanding, you can consider that the number or string is converted to a tuple when compared:

  ```qsp
  [8] < 9 & ! returns 1
  [9, 8] > 9 & ! returns 1
  [0, 0] > 9 & ! returns 0

  [8, 9] > '8,9' & ! returns 0
  ['a', 'z'] < 'az' & ! returns 1
  ['a', 'z'] > 'a' & ! returns 1
  (['az'] = "az") & ! returns 1
  ```

:::warning[We recommend:]
Not to compare values of different types to avoid confusion.
:::

## `*` (multiplication)

`*` — arithmetic operation "MULTIPLICATION". Multiplies two numbers. General syntax:

```qsp
[#expression 1] * [#expression 2]
```

, where `[#expression 1]` and `[#expression 2]` — any two numeric values or expressions. The operation result is the product of two numbers.

Examples:

```qsp
2 * 2 & ! returns 4
4 * 2 & ! returns 8
17 * 5 & ! returns 85
37 * 100 & ! returns 3700
```

Can be used with tuples whose values are numbers and/or other tuples containing numbers. General syntax:

```qsp
[%tuple] * [#number]
```

In this case, each tuple element will be multiplied by the specified number. Examples:

```qsp
%tuple = [4, 10, 16]
%a = %tuple * 2
! %a will equal [8, 20, 32]

[4, 10] * 'b' & ! data type mismatch error
```

Note the last example. A data type mismatch error occurs because it's impossible to apply multiplication to a string value. The same error will occur if the tuple contains string values. However, you can multiply tuples containing only numeric values:

```qsp
*pl [2, 3] * [4, 5]
! [2 * [4,5], 3 * [4,5]]
! [[8,10],[12,15]]
```

In this case, each element of the first tuple is multiplied by the second tuple. This gives us a new tuple of two tuples as a result.

## `*=` (multiplication-assignment)

`*=` — "MULTIPLICATION-ASSIGNMENT" operation. Combines assignment and multiplication operations. Multiplies the specified variable value by a certain number and returns the result to the same variable. General syntax:

```qsp
ARRAY_NAME *= [#expression 1]
```

, where `ARRAY_NAME` — variable name (without quotes) or array name with cell specification, and `[#expression 1]` — any numeric value or expression.

Analogous to:

```qsp
ARRAY_NAME = ARRAY_NAME*[#expression 1]
```

Example:

```qsp
! we replace two operations: assignment and multiplication
warrior = warrior * 2
! with multiplication-assignment (identical action)
warrior *= 2
```

If the `ARRAY_NAME` variable value is a tuple, each tuple element will be multiplied by the specified number, and the resulting tuple will be assigned to the variable. Example:

```qsp
%tuple = [4, 10, 16]
%tuple *= 2
! %tuple will equal [8, 20, 32]
```

You cannot multiply by a string type value; this will lead to a data type mismatch error. Also, tuple values (and all nested tuples) should not contain string values when performing this operation. However, you can perform multiplication-assignment with another tuple:

```qsp
%tuple = [2, 3]
%tuple *= [4, 5]
! %tuple will equal [[8,10],[12,15]]
```

:::warning[Note]
Multiplication-assignment with a tuple will cause a data type mismatch error if the variable type is not a tuple:

```qsp
number = 4
number *= [4,5] & ! data type mismatch error
! this way there will be no error, but the variable will contain an empty tuple:
%number *= [4,5]
```

:::

## `+` (addition)

`+` — arithmetic operation "ADDITION". Adds two numbers. General syntax:

```qsp
[expression 1]+[expression 2]
```

, where `[expression 1]` and `[expression 2]` — any two values or expressions. The operation result is the sum of two values.

Examples:

```qsp
2+2 & ! returns 4
4+2 & ! returns 6
17+5 & ! returns 22
37+100 & ! returns 137
```

When "adding" string values, [concatenation](qsp-keyword-operacion.md#-concatenation) is performed, i.e., "gluing" strings together:

```qsp
! the string "2627" will be output to screen
"26"+"27"
```

If values are "added" to a tuple, each tuple element is summed with the specified value:

```qsp
%tuple = [4, 10, 16]
%a = %tuple + 2
! %a will equal [6, 12, 18]
```

If two tuples are added, the second tuple is added to the values of each element of the first tuple:

```qsp
[4, 10] + ['b', 'x']
! [4 + ['b', 'x'], 10 + ['b', 'x']]
! [['4b','4x'], ['10b','10x']]
```

## `+=` (addition-assignment)

`+=`, `(increment)` — "INCREMENT" operation, combining assignment and addition operations. Adds the specified value to the current variable value. General syntax:

```qsp
ARRAY_NAME += [expression 1]
```

, where `ARRAY_NAME` — variable name (without quotes) or array name with cell specification, and `[expression 1]` — any value or expression.

Analogous to:

```qsp
ARRAY_NAME = ARRAY_NAME + [expression 1]
```

Example:

```qsp
! we replace two operations: assignment and addition
warrior = warrior + 15
! with increment (identical action)
warrior += 15
```

It's also possible to perform increment with string values, works like [concatenation](qsp-keyword-operacion.md#-concatenation):

```qsp
$text += " (maybe something is written here)"
```

If the `ARRAY_NAME` variable value is a tuple, each tuple element will be summed with the specified value, and the resulting tuple will be assigned to the variable. Example:

```qsp
%tuple = [4, 10, 16]
%tuple += 2
! %tuple will equal [6, 12, 18]
```

You can perform addition-assignment with another tuple:

```qsp
%tuple = [2, 3]
%tuple += [4, 5]
! %tuple will equal [[6,7],[7,8]]
```

:::warning[Note]
Addition-assignment with a tuple will cause a data type mismatch error if the variable type is not a tuple:

```qsp
number = 4
number += [4,5] & ! data type mismatch error
! this way there will be no error, but the variable will contain an empty tuple:
%number += [4,5]
```

:::

:::tip[Note]
Increment — in many programming languages this is an operation that performs variable increase. Most often, increment means increasing a variable by `1`.
:::

## `-` (subtraction)

`-` — arithmetic operation "SUBTRACTION". Subtracts one number from another. General syntax:

```qsp
[#expression 1] - [#expression 2]
```

, where `[#expression 1]` and `[#expression 2]` — two numeric values or expressions. The operation result is the difference of two values.

Examples:

```qsp
2 - 2 & ! returns 0
4 - 2 & ! returns 2
17 - 5 & ! returns 12
37 - 100 & ! returns -63
```

Can be used with tuples whose values are numbers and/or other tuples containing numbers. General syntax:

```qsp
[%tuple] - [#number]
```

In this case, the specified number will be subtracted from each tuple element. Examples:

```qsp
%tuple = [4, 10, 16]
%a = %tuple - 2
! %a will equal [2, 8, 14]

[4, 10] - 'b' & ! data type mismatch error
```

Note the last example. A data type mismatch error occurs because it's impossible to apply subtraction to a string value. The same error will occur if the tuple contains string values. However, you can subtract one tuple from another if both tuples contain only numeric values:

```qsp
*pl [2, 3] - [4, 5]
! [2 - [4,5], 3 - [4,5]]
! [2  + ([4,5] * -1), 3 + ([4,5] * -1)]
! [[-4, -5] + 2, [-4,-5] + 3]
! [[-2,-3],[-1,-2]]
```

In this case, the second tuple is subtracted from each element of the first tuple. If you sequentially expand brackets and perform all necessary mathematical operations, you get a new tuple containing other tuples with results.

## `-=` (subtraction-assignment)

**`-=`, `(decrement)`** — "DECREMENT" operation, combining assignment and subtraction operations. Subtracts the specified value from the current variable value. General syntax:

```qsp
ARRAY_NAME -= [#expression 1]
```

, where `ARRAY_NAME` — variable name (without quotes) or array name with cell specification, and `[#expression 1]` — any numeric value or expression.

Analogous to:

```qsp
ARRAY_NAME = ARRAY_NAME - [#expression 1]
```

Example:

```qsp
! we replace two operations: assignment and subtraction
warrior = warrior - 15
! with decrement (identical action)
warrior -= 15
```

If the `ARRAY_NAME` variable value is a tuple, the specified number will be subtracted from each tuple element, and the resulting tuple will be assigned to the variable. Example:

```qsp
%tuple = [4, 10, 16]
%tuple -= 2
! %tuple will equal [2, 8, 14]
```

You cannot subtract a string type value; this will lead to a data type mismatch error. Also, tuple values (and all nested tuples) should not contain string values when performing this operation. However, you can perform subtraction-assignment with another tuple:

```qsp
%tuple = [2, 3]
%tuple -= [4, 5]
! %tuple will equal [[-2,-3],[-1,-2]]
```

:::warning[Note]
Subtraction-assignment with a tuple will cause a data type mismatch error if the variable type is not a tuple:

```qsp
number = 4
number -= [4,5] & ! data type mismatch error
! this way there will be no error, but the variable will contain an empty tuple:
%number -= [4,5]
```

:::

:::tip[Note]
Decrement — in many programming languages this is an operation that performs variable decrease. Most often, decrement means decreasing a variable by `1`.
:::

## `-` (unary minus)

**unary `-`** — unary operation. General syntax:

```qsp
-[#expression]
```

, where `[#expression]` — any numeric value or expression. The result of this operation is the same value but with opposite sign.

Examples:

```qsp
-2 & ! returns -2
-(3+6) & ! returns -9
-(-27) & ! returns 27
```

Unary minus can be used before a tuple containing only numeric values. This expression will return a new tuple where the sign of each element is changed to opposite:

```qsp
- [2, 3, -1, -17, 5]
! [-2, -3, 1, 17, -5]
```

:::note[5.7.0]

In earlier player versions, there was a "unary plus" operation:

```qsp
+(6+7)
```

Essentially, it did nothing, so it was decided to abandon it.
:::

## `/` (division)

`/` — arithmetic operation "DIVISION". General syntax:

```qsp
[#expression 1] / [#expression 2]
```

, where `[#expression 1]` and `[#expression 2]` — any two numeric values or expressions. The value `[#expression 2]` must not equal zero. The operation result is the quotient of dividing two numbers.

Since QSP supports only integer values, division is also performed as integer division, without rounding, with truncation of the fractional part.

Examples:

```qsp
2 / 2 & ! returns 1
4 / 2 & ! returns 2
17 / 5 & ! returns 3
37 / 100 & ! returns 0
```

Can be used with tuples whose values are numbers and/or other tuples containing numbers. General syntax:

```qsp
[%tuple] / [#number]
```

In this case, each tuple element will be divided by the specified number. Examples:

```qsp
%tuple = [4, 10, 16]
%a = %tuple / 2
! %a will equal [2, 5, 8]

[4, 10] / 'b' & ! data type mismatch error
```

Note the last example. A data type mismatch error occurs because it's impossible to apply division to a string value. The same error will occur if the tuple contains string values. However, you can divide tuples containing only numbers:

```qsp
*pl [30, 60] / [2, 6]
! [30 / [2,6], 60 / [2,6]]
! [[15,5],[30,10]]
```

In this case, each element of the first tuple is "divided" by the second tuple. This gives us a new tuple of two tuples as a result.

## `/=` (division-assignment)

`/=` — "DIVISION-ASSIGNMENT" operation. Combines assignment and division operations. Divides the specified variable value by a certain number and returns the result to the same variable. General syntax:

```qsp
ARRAY_NAME /= [#expression 1]
```

, where `ARRAY_NAME` — variable name (without quotes) or array name with cell specification, and `[#expression 1]` — any numeric value or expression.

Analogous to:

```qsp
ARRAY_NAME = ARRAY_NAME / [#expression 1]
```

Example:

```qsp
! we replace two operations: assignment and division
warrior = warrior / 2
! with division-assignment (identical action)
warrior /= 2
```

If the `ARRAY_NAME` variable value is a tuple, each tuple element will be divided by the specified number, and the resulting tuple will be assigned to the variable. Example:

```qsp
%tuple = [4, 10, 16]
%tuple /= 2
! %tuple will equal [2, 5, 8]
```

You cannot divide by a string type value; this will lead to a data type mismatch error. Also, tuple values (and all nested tuples) should not contain string values when performing this operation. However, you can perform division-assignment with another tuple:

```qsp
%tuple = [10, 30]
%tuple /= [5, 2]
! %tuple will equal [[2,5],[6,15]]
```

:::warning[Note]
Division-assignment with a tuple will cause a data type mismatch error if the variable type is not a tuple:

```qsp
number = 4
number /= [4,5] & ! data type mismatch error
! this way there will be no error, but the variable will contain an empty tuple:
%number /= [4,5]
```

:::

## MOD

`MOD` — operation calculates the remainder from dividing two numbers. General syntax:

```qsp
[#expression 1] MOD [#expression 2]
```

, where `[#expression 1]` — dividend, `[#expression 2]` — divisor.

Examples:

```qsp
! 4 divides by 2 evenly
4 mod 2 & ! returns 0
! 5 doesn't divide by 2 evenly
5 mod 2 & ! returns 1
! 13 doesn't divide by 10 evenly
13 mod 10 & ! returns 3
```

The remainder from dividing a negative number will be a negative number.

## `<` (less than)

`<` — comparison operation "LESS THAN". General syntax:

```qsp
[expression_1] < [expression_2]
```

If the value of expression `[expression_1]` is less than the value of expression `[expression_2]`, the operation returns `1`, otherwise it returns `0`. In other words: true if the first is less than the second.

Examples:

```qsp
! 2 is less than 4 — returns 1
2 < 4
! 5 is not less than 5 — returns 0
5 < 5
! 7 is not less than 3 — returns 0
7 < 3
```

You can compare text values:

```qsp
"a" < "z"      & ! true
"z" < "zz"     & ! true
"aaaaaa" < "z" & ! true
```

And you can compare tuples:

```qsp
[1, 2, 3] < [1, 2, 9] & ! true
[1, 2, 3] < [2, 2, 3] & ! true
[1, 2] < [1, 2, 3] & ! true
```

## `<=` (less than or equal)

`<=` — comparison operation "LESS THAN OR EQUAL". General syntax:

```qsp
[expression_1] <= [expression_2]
```

If the value of expression `[expression_1]` is less than or equal to the value of expression `[expression_2]`, the operation returns `1`, otherwise it returns `0`. In other words: true if the first is less than the second, or equal to it.

Examples:

```qsp
! 2 is less than 4 — returns 1
2 <= 4
! 5 equals 5 — returns 1
5 <= 5
! 7 is not less than three and not equal to it
7 <= 3 & ! returns 0
```

Analogous to "`=<`" and constructs:

```qsp
([expression_1] < [expression_2]) or ([expression_1] = [expression_2])

no [expression_1] > [expression_2]
```

You can also compare text values:

```qsp
"a" <= "z"    & ! true
"z" <= "zz"    & ! true
"aaaaaa" <= "z" & ! true
"z" <= "z" & ! true
```

And tuples:

```qsp
[1, 2, 3] <= [1, 2, 9] & ! true
[1, 2, 3] <= [2, 2, 3] & ! true
[1, 2] <= [1, 2, 3] & ! true
[1, 2, 3] <= [1, 2, 3] & ! true
```

## `<>` (not equal)

`<>` — comparison operation "NOT EQUAL". General syntax:

```qsp
[expression_1] <> [expression_2]
```

If the value of expression `[expression_1]` is not equal to the value of expression `[expression_2]`, the operation returns `1`, otherwise it returns `0`. In other words: true if the expressions are not equal.

Analogous to "`!`", or construct:

```qsp
no [expression_1] = [expression_2]
```

Examples:

```qsp
! 2 is not equal to 4 — returns 1
2 <> 4
! 5 equals 5 — returns 0
5 <> 5
```

You can compare string values:

```qsp
"abc" <> "def" & ! returns 1
"abc" <> "abc" & ! returns 0
```

You can compare tuples:

```qsp
[1, 2, 3] <> [4, 6, 7] & ! returns 1
[1, 2, 3] <> [1, 2, 3] & ! returns 0
```

## `=` (equal)

`=` — comparison operation "EQUAL". General syntax:

```qsp
[expression_1] = [expression_2]
```

If the value of expression `[expression_1]` equals the value of expression `[expression_2]`, the operation returns `1`, otherwise it returns `0`. In other words: true if the expressions are equal.

Analogous to construct:

```qsp
no [expression_1] <> [expression_2]
```

Examples:

```qsp
! 2 is not equal to 4 — returns 0
(2 = 4)
! 5 equals 5 — returns 1
(5 = 5)
```

You can compare string values:

```qsp
("abc" = "def") & ! returns 0
("abc" = "abc") & ! returns 1
```

You can compare tuples:

```qsp
([1, 2, 3] = [4, 6, 7]) & ! returns 0
([1, 2, 3] = [1, 2, 3]) & ! returns 1
```

:::warning[Attention!]
Don't confuse with the [assignment operation](#-assignment).
:::

## `=` (assignment)

`=` — assignment operation. General syntax:

```qsp
ARRAY_NAME = [value]
```

, where `ARRAY_NAME` — variable name (not in quotes) or array name with cell specification (not in quotes), `[value]` — any value or expression.

Examples:

```qsp
! assign value 13 to variable BOX
BOX = 13
! assign value "Text string" to variable $text
$text = "Text string"
! assign value 365 to zero cell of array day
day[0] = 365
! assign tuple [1, 'unit', 3] to variable tuple:
%tuple = [1, 'unit', 3]
```

String variable/array names must start with the `$` symbol.

Variable/array names containing tuples must start with the `%` symbol.

:::warning[Attention!]
The assignment operation should not be confused with the "EQUAL TO" comparison operation, although they look very similar:

```qsp
! assignment operation
alukard = 1000
! comparison operation
(alukard = 1000)
```

In this case, the player understands that inside the brackets is a comparison operation because brackets are used for writing expressions. The notation:

```qsp
"abc" = "abc"
```

is syntactically incorrect. The player will give an error: invalid variable/array name. Since in this case it doesn't understand that this is a comparison operation.

If an operator explicitly precedes the comparison operation, brackets can be omitted:

```qsp
if alukard = 150: *pl "Not enough strength"
*pl "abc" = "abc"
```

:::

### Multiple Assignment

Multiple assignment allows assigning values to several variables or array cells with one `=` command. General syntax:

```qsp
ARRAY_NAME_1, ARRAY_NAME_2, ... , ARRAY_NAME_N = [VALUE_1], [VALUE_2], ... , [VALUE_N]
```

, where variable names (or array names with cell index specification in square brackets) are written to the left of the `=` sign, and values to be assigned to variables or array cells are listed to the right of the `=` sign.

:::warning[Important to remember!]
There must be as many variables to the left of the equals sign as there are values to the right. The number of variables and the number of assigned values must match.

This rule is not followed when unpacking tuples.
:::

Examples:

```qsp
apples_in_pocket, apples_in_basket, apples_at_lyoshka = 58, 11, 19
$string_1, $string_2 = 'Grekha rode across the river', 'Grekha sees a crab in the river'
$name, count = 'Old sword', 2
```

Instead of directly specifying values, you can assign values of other variables, expressions, functions:

```qsp
! three variables = three values
red, green, blue = rand(0,255), rand(0,255), rand(0,255)
! two variables = two values
apples_in_pocket, apples_in_basket = apples_at_lyoshka, apples_on_tree+15
```

Thanks to the ability to simultaneously assign values to several variables, you can swap data in two variables without using a third:

```qsp
! assign variables x and y values 12 and 99
x, y = 12, 99
! swap values. Now x contains number 99, and y — 12
x, y = y, x
```

### Tuple Unpacking

Since tuples contain several values at once, the notation for assigning values to variables from tuples can differ from the usual:

```qsp
! %unit = [187, 94, 'steel', [0, 2]]
height, weight, $material, %coordinates = %unit
```

As you can see, here we have four variable names on the left, but only one tuple variable name on the right. Such assignment is called unpacking — values are extracted from the tuple and placed in the specified variables.

A tuple not placed in a variable is unpacked the same way:

```qsp
height, weight, $material, %coordinates = [187, 94, 'steel', [0, 2]]
```

Such notation differs little from multiple assignment, so external square brackets are not required:

```qsp
height, weight, $material, %coordinates = 187, 94, 'steel', [0, 2]
```

It should be emphasized that **multiple assignment is essentially tuple unpacking**.

Since if there are more variables to the left of the equals sign than values in the tuple, default values for those variables will be written to the "extra" variables, the same will happen with multiple assignment.

```qsp
r, g, b, a = [255, 188, 19]
! r = 255, g = 188, b = 19, a = 0
raz, dva, tri, chetyre = 137, 61
! raz = 137, dva = 61, tri = 0, chetyre = 0
```

At the same time, if there are fewer variables to the left of the equals sign than values to the right in multiple assignment, this will cause a data type mismatch error:

```qsp title="Data type mismatch"
coords = 23, 34
age, weight, material = 27, 94, 'steel', 'biorobot'
```

If the type of the last listed variable is a tuple, such assignment won't cause an error:

```qsp
age, weight, %type = 27, 94, 'steel', 'biorobot'
! age = 27, weight = 94, %type = ['steel', 'biorobot']
```

## `=<` (equal or less)

:::warning[Attention!]
This notation, although acceptable in QSP, is not recommended for use. Use "`<=` (less than or equal)" instead.
:::

`=<` — comparison operation "EQUAL OR LESS". General syntax:

```qsp
[expression_1] =< [expression_2]
```

If the value of expression `[expression_1]` is less than or equal to the value of expression `[expression_2]`, the operation returns `1`, otherwise it returns 0. In other words: true if the first is less than the second, or equal to it.

Examples:

```qsp
! 2 is less than 4 — returns 1
2 =< 4
! 5 equals 5 — returns 1
5 =< 5
! 7 is not less than three and not equal to it
7 =< 3 & ! returns 0
```

Analogous to "`<=`" and constructs:

```qsp
([expression_1] < [expression_2]) or ([expression_1] = [expression_2])

no [expression_1] > [expression_2]
```

## `=>` (equal or greater)

:::warning[Attention!]
This notation, although acceptable in QSP, is not recommended for use. Use "`>=` (greater than or equal)" instead.
:::

`=>` — comparison operation "EQUAL OR GREATER". General syntax:

```qsp
[expression_1] => [expression_2]
```

If the value of expression `[expression_1]` is greater than or equal to the value of expression `[expression_2]`, the operation returns `1`, otherwise it returns 0. In other words: true if the first is greater than the second, or equal to it.

Examples:

```qsp
! 2 is not greater than and not equal to 4 — returns 0
2 => 4
! 5 equals 5 — returns 1
5 => 5
! 7 is greater than 3
7 => 3 & ! returns 1
```

Analogous to "`>=`" and constructs:

```qsp
([expression_1] > [expression_2]) or ([expression_1] = [expression_2])
no [expression_1] < [expression_2]
```

## `>` (greater than)

`>` — comparison operation "GREATER THAN". General syntax:

```qsp
[expression_1] > [expression_2]
```

If the value of expression `[expression_1]` is greater than the value of expression `[expression_2]`, the operation returns `1`, otherwise it returns `0`. In other words: true if the first is greater than the second.

Examples:

```qsp
! 2 is not greater than 4 — returns 0
2 > 4
! 5 is not greater than 5 — returns 0
5 > 5
! 7 is greater than 3 — returns 1
7 > 3
```

You can compare text values, where characters are compared sequentially, and the character closer to the end of the alphabet is considered greater.

```qsp
"z" > "a"         & ! true
"zz" > "z"     & ! true
"z" > "aaaaaa" & ! true
```

And you can compare tuples:

```qsp
[1, 2, 9] > [1, 2, 3] & ! true
[1, 2, 3] > [2, 2, 3] & ! false
[1, 2, 3] > [1, 2] & ! true
```

## `>=` (greater than or equal)

`>=` — comparison operation "GREATER THAN OR EQUAL". General syntax:

```qsp
[expression_1] >= [expression_2]
```

If the value of expression `[expression_1]` is greater than or equal to the value of expression `[expression_2]`, the operation returns `1`, otherwise it returns 0. In other words: true if the first is greater than the second, or equal to it.

Examples:

```qsp
! 2 is not greater than and not equal to 4 — returns 0
2 >= 4
! 5 equals 5 — returns 1
5 >= 5
! 7 is greater than 3
7 >= 3 & ! returns 1
```

Analogous to "`=>`" and constructs:

```qsp
([expression_1] > [expression_2]) or ([expression_1] = [expression_2])
no [expression_1] < [expression_2]
```

You can compare text values, where characters are compared sequentially, and the character closer to the end of the alphabet is considered greater.

```qsp
"z" >= "a"    & ! true
"zz" >= "z"    & ! true
"z" >= "aaaaaa" & ! true
"z" >= "z" & ! true
```

And tuples:

```qsp
[1, 2, 9] >= [1, 2, 3] & ! true
[1, 2, 3] >= [2, 2, 3] & ! false
[1, 2] >= [1, 2, 3] & ! false
[1, 2, 3] >= [1, 2, 3] & ! true
```

## `!` (not equal)

:::warning[Attention!]
Don't confuse with the comment operator.

For better code readability, we recommend using `<>`.
:::

`!` — comparison operation "NOT EQUAL". General syntax:

```qsp
[expression_1]![expression_2]
```

If the value of expression `[expression_1]` is not equal to the value of expression `[expression_2]`, the operation returns `1`, otherwise it returns `0`. In other words: true if the expressions are not equal.

Analogous to "`<>`", or construct:

```qsp
no [expression_1] = [expression_2]
```

Examples:

```qsp
! 2 is not equal to 4 — returns 1
2 ! 4
! 5 equals 5 — returns 0
5 ! 5
```

## `&` (concatenation)

`&` — concatenation, operation for combining string expressions or tuples. General syntax:

```qsp
([$expression 1] & [$expression 2])
([%expression 1] & [%expression 2])
```

:::warning[Attention!]
Concatenation must always be enclosed in brackets!
:::

If you try to combine numeric values, they will be converted to strings, and then the strings will be combined.

Examples:

```qsp
*pl ('hello, ' & 'World!')
! we'll see the string 'hello, World!' on screen
*pl ([1, 2, 3] & [4, 5, 6])
! we'll see the tuple [1, 2, 3, 4, 5, 6] on screen
```

:::warning[Attention!]
Don't confuse with the command enumeration symbol:

```qsp
! in this case, strings "26" and "27" will be
! output to screen sequentially
"26" & "27"
! and here the string "2627" will be output to screen
("26" & "27")
```

:::

:::tip
It's not recommended to use this operation for combining strings, since strings can be combined through [`+`](qsp-keyword-operacion.md#-addition):

```qsp
! the string "2627" will be output to screen
"26"+"27"
```

Such notation creates less confusion when reading code and works similarly.

You can't join two tuples into one using the `+` operation:

```qsp
[2, 5] + [3, 7]
! the tuple [[5,9],[8,12]] will be on screen
```

:::

## AND

`AND` — logical "AND". General syntax:

```qsp
[#expression 1] AND [#expression 2]
```

The entire expression will be true if both `[#expression 1]` and `[#expression 2]` are true.

Examples:

```qsp
! both parts of expression are true, so entire expression is true
(2 = 2) and (3 <> 2) & ! expression returns 1 (true)
! one part of expression is not true, so entire expression is false
(2 <> 2) and (3 <> 2) & ! expression returns 0 (false)
! both parts of expression are not true, so entire expression is not true
(2 <> 2) and (3 = 2) & ! expression returns 0 (false)
```

:::note[5.7.0]
In older player versions, the operation was bitwise.
:::

## LOC

`LOC` — operation checks for location existence and returns `1` if location exists, and `0` if location doesn't exist. General syntax:

```qsp
LOC([$location])
```

, where `[$location]` — location name whose existence needs to be checked in the game. Expression is true if location exists in the game.

Examples:

```qsp
! checks if location "start" exists in game
loc("start") & ! if location exists, returns 1

! if location "street" is not added to game
if loc("street") = 0:
    act "Go outside": *pl "I can't go outside, the door won't open."
end
```

## NO

`NO` — negation operation. General syntax:

```qsp
NO [#expression]
```

If `[#expression]` is true, then the entire expression is false, and vice versa. In other words, returns `0` if the expression value is not zero, and returns `1` if the expression value equals `0`.

Example:

```qsp
! 4 equals 4 is true, so entire expression is false
no (4 = 4) & ! returns 0 (false)
! can be read as question: four does not equal four? No — false.

! that 5 equals 3 is false, so entire expression is true
no (5 = 3) & ! returns 1 (true)
! can be read as question: five does not equal three? Yes — true.
```

:::note[5.7.0]
In older player versions, the operation was bitwise.
:::

## OBJ

`OBJ` — operation checks for item presence in inventory and returns `1` if item exists, and `0` if item doesn't exist. General syntax:

```qsp
OBJ([$name])
```

, where `[$name]` — item name whose presence needs to be checked in the objects window. Expression is true if item is added to the objects window.

Examples:

```qsp
! checks if "Screwdriver" item is added to objects window
obj("Screwdriver") & ! if item exists, returns 1

! depending on presence of this or that item
! this or that action is output
if obj("Full jug") = 1:
    act "Empty jug":
        delobj "Full jug"
        addobj "Empty jug"
        goto $curloc
    end
elseif obj("Empty jug") = 1:
    act "Fill jug":
        addobj "Full jug"
        delobj "Empty jug"
        goto $curloc
    end
end
```

## OR

`OR` — logical "OR". General syntax:

```qsp
[#expression 1] OR [#expression 2]
```

The entire expression will be true if at least one of expressions `[#expression 1]` and `[#expression 2]` is true.

Examples:

```qsp
! both parts of expression are true, so entire expression is true
(2 = 2) or (3 <> 2) & ! expression returns 1 (true)
! one part of expression is true, so entire expression is true
(2 <> 2) or (3 <> 2) & ! expression returns 1 (true)
! both parts of expression are not true, so entire expression is not true
(2 <> 2) or (3 = 2) & ! expression returns 0 (false)
```

:::note[5.7.0]
In older player versions, the operation was bitwise.
:::