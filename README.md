# Near-Equal Just Intonation (NEJI) calculator
This is a command-line tool for calculating tuning tables and exporting Scala files of Near-Equal Just Intonation (NEJI) tuning systems

# Requirements
Python 3 (tested on version 3.7.1)

NumPy Python module (tested on version 1.19.4)

# Usage

To calculate a NEJI tuning, you must provide the following three arguments:

* the EDO you wish to approximate or "un-temper" via just intervals,
* a comma-separated list of 'generators':  the integers that can be used for the denominator of the just intervals.  No spaces allowed here!
* a name for the generated .scl file.

For example, to calculate the NEJI that approximates 15-EDO using just intervals and has 2, 31, and product combinations (i.e., 2 x 31 = 62) as the denominator, this is the command to run:

```bash
python neji_calculator.py 15 2,31 31_neji_15
```
The third argument, "31_neji_15", is the file name.  This will export a scala file called "31_neji_15.scl".  
It will also print the following information:
```
N-EDO: 15, Generators: [2, 31], Filename: 31_neji_15.scl

degree, ratio, cents, error (cents from EDO)
 0      1    0.000000    0.000000
 1  65/62   81.805803    1.805803
 2  34/31  159.919837   -0.080163
 3  71/62  234.660971   -5.339029
 4  75/62  329.546856    9.546856
 5  39/31  397.447090   -2.552910
 6  41/31  484.026833    4.026833
 7  43/31  566.482133    6.482133
 8  45/31  645.188143    5.188143
 9  47/31  720.471050    0.471050
10  49/31  792.616240   -7.383760
11 103/62  878.765060   -1.234940
12  54/31  960.829430    0.829430
13 113/62 1039.179182   -0.820818
14  59/31 1114.136087   -5.863913
15      2 1200.000000    0.000000
```
## Nudging a scale degree

Nudging or tweaking a degree in the tuning can be useful for balancing or centering the tuning.  The following example is taken from [Zhea Erose's 'Eurybia'](https://www.youtube.com/watch?v=ubPwKxcp87g),  which uses 12-note undecimal tuning and has a raised fourth.  To nudge, specify the degree you wish to nudge (5 in this example) and by how much.  

```bash
python neji_calculator.py 12 2,11 eurybia --nudge 5 --by 1
```

writes the Scala file **eurybia.scl** and prints the following output:

```
N-EDO: 12, Generators: [2, 11], Filename: eurybia.scl

degree, ratio, cents, error (cents from EDO)
 0     1    0.000000    0.000000
 1 23/22   76.956405  -23.043595
 2 25/22  221.309485   21.309485
 3 13/11  289.209719  -10.790281
 4 14/11  417.507964   17.507964
 5 15/11  536.950772   36.950772 (raised by 1/22)
 6 31/22  593.717630   -6.282370
 7   3/2  701.955001    1.955001
 8 35/22  803.821678    3.821678
 9 37/22  900.026096    0.026096
10 39/22  991.164720   -8.835280
11 21/11 1119.462965   19.462965
12     2 1200.000000    0.000000
```
The '--by' argument may be positive or negative.  It adjusts by increments of 1 divided by the product of all the generators (increments of 1/22 in this example).


## Getting finer control by explicitly constraining or 'limiting' the denominators

In the above example, the output values in the denominators of the just ratios were 2, 11, and 22.  2 and 11 were specified as generators.  22, the product of 2 and 11, was added by default.  This product-taking default setting leads to closer approximations of the EDO scale.  What if we don't want that?  

We can turn off the default product expansion of the denominators by using the `-l` or `--limit` argument. (This has nothing to do with N-limit just intonation.)   Here's an example with 5 different generators:

```bash
python neji_calculator.py -l 12 2,3,5,7,14 
```

```
N-EDO: 12, Generators: [2, 3, 5, 7, 14], Filename: 12_neji_2-3-5-7-14_lim.scl

degree, ratio, cents, error (cents from EDO)
 0     1    0.000000    0.000000
 1 15/14  119.442808   19.442808
 2   8/7  231.174094   31.174094
 3   6/5  315.641287   15.641287
 4   9/7  435.084095   35.084095
 5   4/3  498.044999   -1.955001
 6  10/7  617.487807   17.487807
 7   3/2  701.955001    1.955001
 8   8/5  813.686286   13.686286
 9   5/3  884.358713  -15.641287
10 25/14 1003.801521    3.801521
11  13/7 1071.701755  -28.298245
12     2 1200.000000    0.000000
```

You can see that 2, 3, 5, 7, and 14 all occur on the denominator.  But 6, the product of 2 and 3, is missing, because it was not explicitly passed to the calculator.  Thus, should be able to see what the `-l` argument does -- it just limits the denominators to the ones explicitly passed.

In general, limiting the denominators with the `-l` setting offers an alternative way to explore tunings in the space between JI and EDO.
