---
id: qsp-keyword-sys-var
title: System Variables
sidebar_position: 4
---

# System Variables

## $BACKIMAGE

`$BACKIMAGE` — contains the path to the background image file for the main description window. The background in the main description window is displayed if the value of this variable is not `''` (i.e., not an empty string) and the image file was successfully loaded.

Example:

```qsp
$backimage = "img/bg.png" & ! set background image located in "img" folder.
```

```qsp
$backimage = "" & ! remove image from main description window background.
```

## $COUNTER

`$COUNTER` — contains the name of the counter location. The counter location can be used for real-time events (i.e., events occurring in real time); for example, smooth background color change, gradual text output to screen, playlist for continuous music playback, and others.

The counter location is called at equal time intervals, by default every 500 ms, i.e., 2 times per second. Automatic interface updates trigger at the same frequency. Intervals are set by the `settimer` operator in milliseconds.

If your counter location is called "Counter", you need to write on the very first location in the game:

```qsp
$counter = 'Counter'
```

As a rule, to avoid confusion, the location is named the same as the service variable — "Counter":

```qsp
$counter = 'Counter'
```

To disable counter location execution, you need to set an empty value for the `$COUNTER` variable:

```qsp
$counter = ""
```

:::note[&lt; 5.7.0]

In older player versions, the counter location was used to automate everything possible, but now we recommend using it only where interface work is required or actions requiring some reaction speed from the player.

You shouldn't tie health restoration algorithms or checks for whether the character died to the counter location, and especially shouldn't do object or action selection checks through the counter location. QSP provides several handler locations that more than cover most code automation needs.

:::

## $FNAME

`$FNAME` — contains the name of the currently used font. If equal to `''` (empty string), then the font specified in the program settings is used.

Example:

```qsp
! set Courier New font for entire game
$fname = "Courier New"
```

## $ONACTSEL

`$ONACTSEL` — contains the name of the "action selection" event handler location (hereinafter "*action selection handler*"). In other words, this variable specifies the name of the location whose code triggers when one of the actions displayed on screen is selected.

Remember that action selection occurs when hovering the mouse pointer over it, not when directly clicking.

Assign the "on_mouse" location as *action selection handler*:

```qsp
$onactsel = "on_mouse"
```

This location is useful, for example, for displaying images or playing sounds when selecting actions. You can get the selected action name through the `$selact` function.

```qsp
if instr($selact, 'go', 1): play 'sounds\walk.mp3'
```

To disable the *action selection handler*, you need to set the `$onactsel` variable to an empty value:

```qsp
$onactsel = ""
```

## $ONGLOAD

`$ONGLOAD` — contains the name of the "*game state loading*" event handler location (hereinafter "*load state handler*"). In other words, this variable contains the name of the location whose code will be executed every time after a game state save file ("save file") is loaded using the `opengame` command.

Assign the "on_game_load" location as load state handler:

```qsp
$ongload = "on_game_load"
```

To disable the load state handler, you need to set the `$ongload` variable to an empty value:

```qsp
$ongload = ""
```

## $ONGSAVE

`$ONGSAVE` - contains the name of the "*game state saving*" event handler location (hereinafter "*save state handler*"). In other words, this variable contains the name of the location whose code will be executed every time before the game state is written to a new or existing game state save file ("save file") using the `savegame` command.

Assign the "on_game_save" location as *save state handler*:

```qsp
$ongsave = "on_game_save"
```

To disable the *save state handler*, you need to set the `$ongsave` variable to an empty value:

```qsp
$ongsave=""
```

## $ONNEWLOC

`$ONNEWLOC` — contains the name of the new location transition handler (analog of "common" location in URQ; hereinafter "*new location transition handler*"). In other words, this variable contains the name of the location whose code is executed every time after executing the code of the location that was transitioned to using `goto` or `xgoto` operators. Game control is passed to the player only after executing code at this handler location.

Assign the "on_goto_newloc" location as new location transition handler:

```qsp
$onnewloc = "on_goto_newloc"
```

You can get the name of the location that was transitioned to using the `$curloc` function.

```qsp
if $curloc = 'house': cat = 1
```

To disable the new location transition handler location, you need to set the `$onnewloc` variable to an empty value:

```qsp
$onnewloc = ""
```

## $ONOBJADD

`$ONOBJADD` — contains the name of the "*item addition*" event handler location (hereinafter "*item addition handler*"). In other words, this variable contains the name of the location whose code is executed every time after adding an item to the objects window using the `addobj` command.

When adding an item, two arguments are passed to this handler location, whose values can be obtained from `$args[0]` and `$args[1]` respectively:

* `$ARGS[0]` - name of the added item
* `$ARGS[1]` - path to the image of the added item

This location is useful, for example, for limiting backpack capacity.

Assign the "on_object_add" location as *item addition handler*:

```qsp
$onobjadd = "on_object_add"
```

To disable the *item addition handler*, you need to set the `$onobjadd` variable to an empty value:

```qsp
$onobjadd = ""
```

## $ONOBJDEL

`$ONOBJDEL` — contains the name of the "*item removal*" event handler location (hereinafter "*item removal handler*"). In other words, this variable contains the name of the location whose code is executed every time when removing an item using the `delobj` command. If you use the `killobj` command, this will be equivalent to a series of `delobj` commands, so the handler location will be called as many times as items are removed with `killobj`.

When using the `killall` command, the item removal handler location is not called since the `$onobjdel` system variable is destroyed before item removal.

When removing an item, an argument is passed to this handler location, whose value can be obtained from `$args[0]`:

* `$ARGS[0]` - name of the removed item

Assign the "on_object_del" location as *item removal handler*:

```qsp
$onobjdel = "on_object_del"
```

This location is useful, for example, for checking the possibility of item removal:

```qsp
! for example there's an item we'll need for the plot
if $args[0] = "Important artifact":
    ! restore the item
    addobj $args[0]
end
```

To disable the *item removal handler*, you need to set the `$onobjdel` variable to an empty value:

```qsp
$onobjdel = ""
```

## $ONOBJSEL

`$ONOBJSEL` — contains the name of the "*item selection*" event handler location (hereinafter "*item selection handler*"). In other words, this variable specifies the name of the location whose code is executed every time when selecting an item. Item selection occurs directly when "clicking" on an item (mouse click on item).

Assign the "on_object_select" location as *item selection handler*:

```qsp
$onobjsel = "on_object_select"
```

This location is useful, for example, for displaying item information or item menu. You can get the selected item name through the `$selobj` function.

```qsp
if $selobj = 'teapot':
    p 'The most ordinary cast iron teapot.'
end
```

When a player selects any item, it remains selected. You can remove selection with the `unselect` command.

To disable the *item selection handler*, you need to set the `$onobjsel` variable to an empty value:

```qsp
$onobjsel = ""
```

## $USERCOM

`$USERCOM` — contains the name of the input line (input field) handler location (hereinafter "*input line handler*"). The code of this handler location is executed if the cursor is in the input line when the "Enter" key is pressed.

Assign the "user_command_line" location as *input line handler*:

```qsp
$usercom = "user_command_line"
```

Useful for organizing a parser (game control through input line) or for organizing a debugger. Example code for handler location:

```qsp
! if entered text corresponds to existing location name
if loc($user_text):
    ! transition to this location
    goto $user_text
end
```

To disable the *input line handler*, you need to set the `$usercom` variable to an empty value:

```qsp
$usercom = ""
```

## ARGS

`ARGS` — specific system array in which argument values passed by the user when calling a location or code written as text are placed.

Example:

```qsp
gosub "em.arr.sort", "$mass", "rug", "$time_ar"
```

Here, three arguments will be passed to the "`em.arr.sort`" location, which will be placed in the first three cells of the `$args` array respectively. I.e., at the moment of starting code execution at the "`em.arr.sort`" location, `$args[0]` will already contain the value "`$mass`", `$args[1]` — the value "`rug`", `$args[2]` — the value "`$time_ar`".

When using `gosub`, `goto`, `xgoto`, `dynamic` operators and `dyneval`, `func` functions, you can specify up to nineteen such arguments, and they will all be placed in `args` array cells from zero to eighteenth. However, since `args` is still an array, you can work with it like a regular array, i.e., use more than nineteen cells, assign text indices, etc.

A distinctive feature of the `args` array is that a separate `args` array is created for each separate code block. I.e., if you call location "2" from location "1", then location "1" has its own `args` array, and location "2" has its own, and values in these arrays don't intersect.

Example:

```qsp
# location_1
args[0]=23
gosub "location_2", 34
*pl args[0]
-

# location_2
*pl args[0]
-
```

Running this code, you'll see that first the number `34` will be output, and only then `23`.

Moreover, if you make a recursive call of a location from itself, a separate array will be created for each location call. Thus, the `args` array is local for each separate code block call by default.

Separate code blocks in QSP are considered:

* location code
* code passed to `dynamic`/`dyneval`
* code in hyperlinks
* loop code
* action code

In the first three cases, the player will create a separate `args` array for each separate session of such code blocks.

**However:**

* loops will use the `args` array created in the code block from which the loop was called.
* actions will use the `args` array created at the location that was transitioned to using `goto` or `xgoto` operators.

## BCOLOR

`BCOLOR` — contains the current background color. If equal to `0`, then the color specified in the program settings is used. Examples:

```qsp
! black background color
bcolor = -16777216
! red background color
bcolor = -16776961
! white background color
bcolor = -1
```

Since background color is encoded by a special number, and calculating this number manually is inconvenient, you should use the `rgb` function, which takes three color components as arguments:

```qsp
! set background color through rgb(red,green,blue) function
! blue background
bcolor = rgb(0, 0, 255)
! yellow background
bcolor = rgb(255, 255, 0)
! orange background
bcolor = rgb(255, 130, 0)
! cyan background
bcolor = rgb(0, 255, 255)
! magenta background
bcolor = rgb(255, 0, 255)
```

## DEBUG

`DEBUG` — if the variable value is not zero, game identifier checking is disabled when loading state. Otherwise, every time the game file changes, you won't be able to use save files made before changing the game.

:::tip[Tip:]
during game development and testing, the `debug` variable value should always be non-zero, and when you release the final game version (release), you need to set the `debug` variable to `0` so players can't load save files from other games.
:::

## DISABLESCROLL

`DISABLESCROLL` — if the variable value is not zero, auto-scrolling of text in main and additional description windows is disabled.

:::note[**What this means**]
Suppose we output a large amount of text to the screen, and then when clicking an `action` we output another text fragment. If `DISABLESCROLL = 0`, this text fragment will force the screen to scroll down when output. If we don't want the screen to scroll down in this case, we assign `1` to the `DISABLESCROLL` variable.
:::

Quite murky behavior in the classic player — under some circumstances, text doesn't scroll anyway.

:::note[**Note from Byte:**]

Supposedly `disablescroll` is used when updating the window. if at the moment of update the value is 0 and there was no transition to a new location (`GT/XGT`), then the description scrolls to the end of the text

Window update occurs in different cases - for example, after the player performed some action (selected action / object), or the game called `refint` or some modal window (`input` / `msg` / `menu` - what I can remember off the top of my head)

I.e., imho, there are 2 conditions for text scrolling that must be met. if at least one is not fulfilled, then there will be no scrolling regardless of disablescroll value
:::

## DISABLESUBEX

:::warning[Be careful!]
In players version 5.8.0 and higher, this variable is no longer used.
:::

`DISABLESUBEX` — if the variable value is not zero, sub-expression calculation in strings is disabled. Example:

```qsp
var = 123
$text = '<<var>>'    & ! variable $text will be assigned string '123'
*pl 'string <<var>>'    & ! string 'string 123' will be output to screen
*pl '<<5+6>>'        & ! string '11' will be output to screen

disablesubex = 1    & ! disable sub-expression calculation
$text = '<<var>>'    & ! variable $text will be assigned string '<<var>>'
*pl 'string <<var>>'    & ! string 'string <<var>>' will be output to screen
*pl '<<5+6>>'        & ! string '<<5+6>>' will be output to screen
```

## FCOLOR

`FCOLOR` — contains the color of the currently used font. If equal to `0`, then the color specified in the program settings is used. Changing the variable value changes the color of all game text except hyperlinks and text whose color is reassigned through HTML. Example:

```qsp
! black text color
fcolor = -16777216
! red text color
fcolor = -16776961
! white text color
fcolor = -1
```

Since font color is encoded by a special number, and calculating this number manually is inconvenient, you should use the `rgb` function, which takes three color components as arguments:

```qsp
! set text color through rgb(red,green,blue) function
! black text
fcolor = rgb(0, 0, 0)
! white text
fcolor = rgb(255, 255, 255)
! red text
fcolor = rgb(255, 0, 0)
! green text
fcolor = rgb(0, 255, 0)
```

## FSIZE

`FSIZE` — contains the size of the currently used font. If equal to `0`, then the size specified in the program settings is used. Font sizes of the HTML `<font>` tag are calculated relative to this value in HTML mode. Example:

```qsp
fsize = 18
```

Font size is set for all text in the game except text whose size is reassigned through HTML.

## LCOLOR

`LCOLOR` — contains the current hyperlink font color. If equal to `0`, then the color specified in the program settings is used. Changing the variable value changes the text color of all hyperlinks except those whose color is reassigned through HTML. Example:

```qsp
! black hyperlink color
lcolor = -16777216
! red hyperlink color
lcolor = -16776961
! white hyperlink color
lcolor = -1
```

Since color in QSP is encoded by a special number, and calculating this number manually is inconvenient, you should use the `rgb` function, which takes three color components as arguments:

```qsp
! set hyperlink color through rgb(red,green,blue) function
! blue hyperlinks
lcolor = rgb(0, 0, 255)
! yellow hyperlinks
lcolor = rgb(255, 255, 0)
! orange hyperlinks
lcolor = rgb(255, 130, 0)
! cyan hyperlinks
lcolor = rgb(0, 255, 255)
! magenta hyperlinks
lcolor = rgb(255, 0, 255)
```

## NOSAVE

`NOSAVE` — if the value of this variable is not `0`, the player menu item "Save game state" becomes unavailable to the player, i.e., the player cannot save the game independently. At the same time, the `savegame` operator continues to work at the QSP code level. Example:

```qsp
! disable game saving possibility
nosave = 1
act "Roll dice":
    cubes = rand(1, 6)
    ! enable saving possibility back
    nosave = 0
    delact $selact
end
```

## RESULT

`RESULT` — specific system variable intended for getting a value in the current code block and passing this value to the `func` or `dyneval` function. In other words, for `func` or `dyneval` functions to return some value, you need to assign a value to the `result` variable in the code block they call.

For example:

```qsp
$dyneval {
  if args[0] mod 2 = 0:
    $result = 'even number'
  else
    $result = 'odd number'
  end
}, 279
```

A separate `result` variable is created for each separate code block by the player. I.e., if you call location "2" from location "1", then location "1" creates its own `result` variable, and location "2" creates its own, and values in these variables don't intersect. Thus, the `result` variable is local for each separate code block call.

If both `result`, `$result`, and `%result` were set during code block processing, the value written to the variable last will be returned as the result.

:::note
In players version 5.7.0, a small problem with value intersection in `result` on different locations may be observed. It's recommended to use the `result` variable only at the end of location code.

In newer player versions, this problem was fixed and `result` can be used alongside `args`.
:::

## USEHTML

`USEHTML` — if the value of this variable is not zero, HTML recognition mode is enabled. In this case, HTML markup can be used in action names, object names, in text output to main and additional description windows, as well as in dialog boxes called by the `msg` operator and `$input` function.

```qsp
! enable HTML
usehtml = 1
! output text with HTML markup
*pl "<font color=#ff8888>Red text.</font>"
```

:::note[qSpider]
In **qSpider**, recognition is always enabled and is not disabled by changing the `usehtml` variable value.
:::

## Notes for the Curious

1. It's possible to define any system variable as local for a separate code block, and then this system variable can be used as a regular local variable, i.e., it won't affect player operation. However, it's **strongly** not recommended to do this to avoid possible errors.
2. Like all other variables in QSP, system variables are also arrays.
    * Interface setting variables allow using any cells except zero without consequences; this won't affect player operation, but it's still not recommended unless it's some necessary technical solution.
    * But system variables that specify event handler location names give a very peculiar effect when filling cells sequentially. If you write location names in several cells in a row, each location entered in the array will be called sequentially. This way you can unload code from event handler locations. For example, the counter location:

        ```qsp
        $counter[] = 'playlist'
        $counter[] = 'animation'
        $counter[] = 'time.acts'
        ```

        It's very important that location names are listed consecutively in the array. If there are empty cells between location names, only those locations that are in the array before the first encountered empty cell will be executed:

        ```qsp
        ! only 'playlist' and 'animation' locations will be executed
        $counter[] = 'playlist'
        $counter[] = 'animation'
        $counter[] = ''
        $counter[] = 'time.acts'
        ```