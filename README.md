# Near-Equal Just Intonation (NEJI) calculator
This is a command-line tool for calculating tuning tables and exporting Scala files of Near-Equal Just Intonation (NEJI) tuning systems

# Requirements
Python 3 (tested on version 3.7.1)
NumPy Python module (tested on version 1.19.4)

# Usage

To calculate a NEJI tuning, you must provide the following three arguments:

* the EDO you wish to approximate or "un-temper" with just intervals,
* a comma-separated list of 'generators':  the integers that can be used for the denominator of the just intervals.  No spaces allowed here!
* a name for the generated .scl file.

For example, to calculate the NEJI that approximates 15-EDO using just intervals and has 2, 31, and product combinations (i.e., 2*31 = 62) as the denominator, this is the command to run:

```bash
python neji_calculator.py 15 2,31 31_neji_15
```
The third argument, "31_neji_15", is the file name.  This will export a scala file called "31_neji_15.scl".  
It will also print the following information:
```
N-EDO: 15, Generators: [2, 31], Filename: 31_neji_15.scl

degree, ratio, cents, error (cents from EDO)
0 1 0.000000 0.000000
1 65/62 81.805803 1.805803
2 34/31 159.919837 -0.080163
3 71/62 234.660971 -5.339029
4 75/62 329.546856 9.546856
5 39/31 397.447090 -2.552910
6 41/31 484.026833 4.026833
7 43/31 566.482133 6.482133
8 45/31 645.188143 5.188143
9 47/31 720.471050 0.471050
10 49/31 792.616240 -7.383760
11 103/62 878.765060 -1.234940
12 54/31 960.829430 0.829430
13 113/62 1039.179182 -0.820818
14 59/31 1114.136087 -5.863913
15 2 1200.000000 0.000000
```


