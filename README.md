# Python Stack 2

Read the Abstract Data Types lecture (Stack section) before you start.

**Rules for this assignment**

- Functions **return** their answer — do not print.
- Use `global Stack, TopOfStack` in every function that changes them.

## Exercise 1

**Problem:**

An "undo" stack for a text editor. Every word you type is pushed onto the
stack. Undo pops the last word off.

Set up the stack:

- `Stack` → a global array of **8** elements, all set to `""` (empty string)
- `TopOfStack` → a global integer, set to `-1`

Then write three functions:

`Push(Word)`

- If the stack is full (`TopOfStack` is 7), return `False`
- Otherwise add 1 to `TopOfStack`, store `Word` at `Stack[TopOfStack]`,
  and return `True`

`Pop()`

- If the stack is empty, return `""` (empty string)
- Otherwise return the word at `Stack[TopOfStack]`, and take 1 off `TopOfStack`

`GetText()`

- Return all the words in the stack, from the **bottom** (`Stack[0]`) up to
  the **top** (`Stack[TopOfStack]`), with **one space** between each word
- Return `""` if the stack is empty
- Do **not** change the stack

**Example:**

    Input:
      Push("I")
      Push("love")
      Push("Python")
      print(GetText())
      print(Pop())
      print(GetText())
      Push("cats")
      print(GetText())

    Output:
      I love Python
      Python
      I love
      I love cats

*Hint:* after `Pop()`, the word `"Python"` is still in the array — only
`TopOfStack` moved. So `GetText()` must stop at `TopOfStack`, not at the end
of the array.

---

## Exercise 2

**Problem:**

`DecimalToBinary(Number)`

`Number` is a whole number from `0` to `255`. Use **your stack** to change it
into a binary string.

1. **Empty the stack first** by setting `TopOfStack` to `-1`.
2. If `Number` is `0`, return `"0"`.
3. While `Number` is more than 0:
    - Push the remainder `Number % 2` onto the stack **as a string**
    - Divide `Number` by 2 with `//`
4. Pop every digit off the stack, joining them into one string, and return it.

Do **not** use `bin()` or `format()`.

**Example:**

    Input:                      Output:
      DecimalToBinary(5)          "101"
      DecimalToBinary(10)         "1010"
      DecimalToBinary(255)        "11111111"
      DecimalToBinary(0)          "0"

How it works for `13`:

    13 % 2 = 1   push "1"     13 // 2 = 6
     6 % 2 = 0   push "0"      6 // 2 = 3
     3 % 2 = 1   push "1"      3 // 2 = 1
     1 % 2 = 1   push "1"      1 // 2 = 0   stop

    Stack (bottom → top):  "1"  "0"  "1"  "1"
    Pop them all:          "1"  "1"  "0"  "1"   →   "1101"

The remainders come out in the **wrong** order, and the stack turns them
around — Last In, First Out.

Why is the stack size 8? The biggest number, 255, is `11111111` — exactly 8 digits.

