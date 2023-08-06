Beatnik
===========
This python package contains functions for stack-based esoteric programming language: Beatnik
---

Description
-----------
[Beatink] is a stack-based esoteric programming language created by Cliff L. Biffle.
This package contains each ACTION functions by the rules of beatnik, and build a stack to calculate the resulted output from the given text.

<pre>
Scrabble letter values
--- ABCDEFGHIJKLMNOPQRSTUVWXYZ ---
 1: A---E---I--L-NO--RSTU-----
 2: ---D--G-------------------
 3: -BC---------M--P----------
 4: -----F-H-------------VW-Y-
 5: ----------K---------------
 6: --------------------------
 7: --------------------------
 8: ---------J-------------X--
 9: --------------------------
10: ----------------Q--------Z
--- ABCDEFGHIJKLMNOPQRSTUVWXYZ ---
</pre>
---

**Action list**

The following table describes the meaning of the ACTIONS (see above).
| Score | Pseudo-Code | Description|
|-------|----------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| <5| NOOP| Does nothing. The Beatnik Interpreter may mock you for your poor scoring, at its discretion.|
| 5 n| push(n)| Finds the score of the next word and push it onto the stack. <br>the actual word with 5 is then skipped. |
| 6     | pop(n)                                 | Pops the top number off the stack and discards it. |
| 7     | push(pop()+pop())                      | Adds the top two values on the stack together|
| 8     | push(input())                          | Input a character from the user and push its value on the stack. Waits for a keypress. |
| 9     | print(pop())                           | Pop a number off the stack and output the corresponding ASCII character to the screen.|
| 10    | push(pop()-pop())                      | Pop two numbers from the stack, subtract the first one popped from the second one popped, and push the result. |
| 11    | a = pop(); b = pop(); push(a); push(b) | Swap the top two values on the stack. |
| 12    | a = pop(); push(a); push(a)            | Duplicate the top value and pushes the value on top of the stack. |
| 13 n  | if(top()==0) jump(+n)                  | Pop a number from the stack, and figure out the score of the next word. <br>If the number from the stack is zero, skip ahead by n words, where n is the score of the next word. <br>(The skipping is actually n+1 words, because the word scored to give us n is also skipped.) |
| 14 n   | if(top()!=0) jump(+n)                  | Same as above, except skip if the value on the stack isn't zero.|
| 15    | if(top()==0) jump(-n)                  | Skip back n words, if the value on the stack is zero. |
| 16    | if(top()!=0) jump(-n)                  | Skip back if it's not zero.     |
| 17    | exit()                                 | Stop the program.|
| 18-23 | NOOP                                   | Does nothing. However, the score is high enough that the Beatnik Interpreter will not mock you, unless it's had a really bad day.|
| >23   |                                        | Generates "Beatnik applause" for the programmer.  

---
## Installation
------------

The Blend Modes package can be installed through pip:
```sh
pip install beatnik
```


Import
-----

```python
from beatnik import beatnik_simple
from beatnik import beatnik_stack
```


Usage
------------
Use the library directly on Jupyter lab
-----
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/experimental-informatics/beatnik/HEAD)

Use the example file beatnik_interact
-----
Simple usage of this library
```python
text = "this is a line of text"
beatnik.beatnik_simple(text,debug=True)
```
---

Step-by-step

preprocess text
```python
text = "this is a line of text"
words = beatnik.preprocess(text)
```


scrabbling word
------------
```python
beatnik.scrabble(words)
```
`words` are list of words that before scrabble


running stack machine
------------
```python
beatnik.stack(words,VALUE,debug=False)
```


License
-------------
The Beatnik package is distributed under the [MIT License (MIT)](https://github.com/experimental-informatics/beatnik/blob/master/LICENSE.txt). Please also take note of the licenses of the dependencies.

   [Beatink]: <https://esolangs.org/wiki/Beatnik>
