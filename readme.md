# Serial-Macros (sMacros)

Use your Serial inteface with arduino to execute macro keys

```
Does to need arduino/board with HID 
```

## WORKING
- Arduino prints the button pressed in Serial inteface
- A python script keeps listening for data from Serial, read and execute a action that can be anything

## USAGE
1. Upload the arduino sketch file to your board, you can change the baudrate, buttons and toggle [Port manipulation](https://www.arduino.cc/en/Reference/PortManipulation) if isn't compatible with the board to use commom ```digitalRead() ```

2. [if you changed baudrate] open jmacro.py and change the variable or use [CLI arguments](#cli-arguments)

3. Open jmacro.py and create your own macro actions for the buttons attached to arduino 

4. Run jmacro.py with python 3.7+, selected the port and click Start, keep terminal open



## CLI ARGUMENTS
Provide a way to use without open the select port and start window


### Available arguments:

```py
-h or               show available arguments
--help

-rr                 print raw entries from serial

# -rr also print current window with button press, useful to get exact window title

-sa                 print executed action when a button is pressed            

-da                 enable default actions if any does not match window title

--debug             enable extra debug print

--port <port>       set port to desired one 

--baud <baudrate>   set baudrate to desired one
```

## Helpful links
Send keystrokes with
* [Pynput](https://github.com/moses-palmer/pynput)
* [pynput docs](https://pynput.readthedocs.io/en/latest/keyboard.html)


Port Manipulation, used to get port state without digialRead()

* [Port manipulation](https://www.arduino.cc/en/Reference/PortManipulation)

* [Port Registers](https://forum.arduino.cc/index.php?topic=301832.0)

## LICENSE
MIT, feel free to copy, modify and redistribute
but mention the origin repo if you can :)

<h6>
    Someone probably already used this method to create macro buttons,
    this is just my implementation of it.
    Also, is possible to use Node.js, as i tried first, is easier to create actions and
    process data from serial but slower to execute key presses.
</h6>
