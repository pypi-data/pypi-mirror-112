# Setup

```
pip3 install colorifix
```

# Requirements
* Python 3.6+

# Usage
It's very simple to use, just remember three symbols:
* `#` to set a **color**
* `@` to set a **style**
* `!` to set a **background**
```python
from colorifix.colorifix import paint

paint("[#red]String to color in red [#blue]and in blue")
paint("[#yellow !green]One color and background at a time,[#red #cyan] last set win")
paint("[@bold @underline]Many styles in one [@dim]string")
paint("[#44 !123]You can use int bash colors")
```
![Examples](images/examples.png)
### Remove styles
You can **remove** every part of a style with the symbol `/` followed by the symbol of the style you want to remove. You can use it alone to remove every styles, it will remove every styles anyway at the end of the string.
```python
paint("[#yellow @underline]This is a yellow underline string[/@], now only yellow[/].")
```
![Remove example](images/remove.png)
### Print or not print
You can choose to **print** the string or just save in a variable [default is a `print`].
```python
paint("[!black @dim]Hello Color![/]") # it prints
colored_str = paint("[!42]Again![/]", False)
```

# Colors
To disaply all different colors, you can use the function `sample`
```python
from colorifix.colorifix import sample

sample()  # base colors
sample(complete=True)  # to display all bash int colors
```
![Base colors](images/colors.png)