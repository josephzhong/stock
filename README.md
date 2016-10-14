# stock

This is a China's A-Stock Market Recommending tool, implemented in Python.

The decision trees locate in the ~/backup directory. The tree2007.py is suggested to be used, which is trained using the transaction data of more than 2,000 stocks from 2007 to 2015.

A sample output could look like this:

Good stocks:

stock #          threshold(the higher the better)  data due date 

INFO:root:601558		6.0	last day of data on 2015-10-16

INFO:root:601608		6.0	last day of data on 2015-10-16

INFO:root:600109		5.0	last day of data on 2015-10-16

INFO:root:600316		5.0	last day of data on 2015-10-16

INFO:root:600433		5.0	last day of data on 2015-10-16

INFO:root:600485		5.0	last day of data on 2015-10-16

INFO:root:603222		5.0	last day of data on 2015-10-16

Verify:

INFO:root:2015-10-16 TP/FP: 77.78%/22.22% Average Growth: 1.264%

INFO:root:2015-10-15 TP/FP: 100.00%/0.00% Average Growth: 4.697%

INFO:root:2015-10-14 TP/FP: 25.00%/75.00% Average Growth: -1.239%

INFO:root:2015-10-13 TP/FP: 85.71%/14.29% Average Growth: 2.401%

INFO:root:2015-10-12 TP/FP: 100.00%/0.00% Average Growth: 3.826%

INFO:root:2015-10-09 TP/FP: 88.00%/12.00% Average Growth: 3.277%

INFO:root:2015-10-08 TP/FP: 0.00%/0.00% Average Growth: 0.000%

INFO:root:2015-10-07 TP/FP: 0.00%/0.00% Average Growth: 0.000%

INFO:root:2015-10-06 TP/FP: 0.00%/0.00% Average Growth: 0.000%

INFO:root:2015-10-05 TP/FP: 60.00%/40.00% Average Growth: 2.598%

INFO:root:tree7y600prefilter Average TP/FP: 63.45% / 36.55% Average Growth: 1.559%
