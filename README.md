# Interpreter for a Kotlin Restriction in Python

Authors: Antonio De Candia, Riccardo Fusco

Professor: Floriano Scioscia

The project was carried out for the Formal Languages and Compilers course taught by Professor Floriano Scioscia at the Polytechnic University of Bari. It is an Interpreter able to work with a small restriction of the Kotlin language made entirely in python with the support of the PLY library.

---

## Kotlin Restriction

**Data Types:**

1. Integers (Int)
2. Booleans (Boolean)­­
3. Strings (String)

**Arithmetic Instructions:**

1. Addition (+)
2. Subtraction (-)
3. Multiplication (*)
4. Division (/)­­­

**Comparison Operators:**

1. Equal to (==)
2. Not equal to (!=)
3. Less than (<)
4. Greater than (>)
5. Less than or equal to (<=)
6. Greater than or equal to (>=)

**Functions(*)**

- Definition and calling of methods

**Logical Operators:**

1. Logical **AND** (&&)
2. Logical **OR** (||)
3. Logical **NOT** (!)

**Branching Instructions:**

1. **if** statement for conditional execution.
2. **Else** .

**Loop Instruction:**

1. **while** loop 
2. **for** loop

**Input Instruction:**

1. Reading input from the user using **readLine()**.

**Output Instruction:**

1. Printing output to the console using **println()**.

---

## Usage

Within the project is present a folder containing some test_scripts useful for evaluating the proper functioning of the interpreter. In the ***main.py*** file you just need to change the path indicating the particular script you want to execute and see the result. The output provides the AST representing the program and its interpretation.The first two files(test_1.kt,test_2.kt) are designed to show correct operation, the last 3(test_3.kt,test_4.kt,test_5.kt) the ability to detect errors.

```python
#main.py
with open('test_scripts/test_1.kt', 'r') as file:
    input_sentence = file.read()
```

---

## Resources

<aside>
📄 PLY Documentation : [https://www.dabeaz.com/ply/ply.html](https://www.dabeaz.com/ply/ply.html)

</aside>

<aside>
👨🏻‍💻 Kotlin Grammar : [https://kotlinlang.org/docs/reference/grammar.html](https://kotlinlang.org/docs/reference/grammar.html)

</aside>