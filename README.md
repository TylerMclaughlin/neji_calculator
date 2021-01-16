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


