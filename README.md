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
INFO:root:600210		4.0	last day of data on 2015-10-16
INFO:root:600292		4.0	last day of data on 2015-10-16
INFO:root:600360		4.0	last day of data on 2015-10-16
INFO:root:600406		4.0	last day of data on 2015-10-16
INFO:root:600449		4.0	last day of data on 2015-10-16
INFO:root:600562		4.0	last day of data on 2015-10-16
INFO:root:600687		4.0	last day of data on 2015-10-16
INFO:root:600714		4.0	last day of data on 2015-10-16
INFO:root:600768		4.0	last day of data on 2015-10-16
INFO:root:600807		4.0	last day of data on 2015-10-16
INFO:root:603368		4.0	last day of data on 2015-10-16
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
INFO:root:2015-10-02 TP/FP: 60.00%/40.00% Average Growth: 2.598%
INFO:root:2015-10-01 TP/FP: 60.00%/40.00% Average Growth: 2.598%
INFO:root:2015-09-30 TP/FP: 26.32%/73.68% Average Growth: -0.384%
INFO:root:2015-09-29 TP/FP: 40.00%/60.00% Average Growth: -0.206%
INFO:root:2015-09-28 TP/FP: 85.71%/14.29% Average Growth: 2.149%
INFO:root:2015-09-25 TP/FP: 18.18%/81.82% Average Growth: -4.502%
INFO:root:2015-09-24 TP/FP: 80.00%/20.00% Average Growth: 0.783%
INFO:root:2015-09-23 TP/FP: 50.00%/50.00% Average Growth: 1.023%
INFO:root:2015-09-22 TP/FP: 80.56%/19.44% Average Growth: 1.674%
INFO:root:2015-09-21 TP/FP: 100.00%/0.00% Average Growth: 6.021%
INFO:root:2015-09-18 TP/FP: 59.38%/40.62% Average Growth: 0.540%
INFO:root:2015-09-17 TP/FP: 14.63%/85.37% Average Growth: -2.697%
INFO:root:2015-09-16 TP/FP: 100.00%/0.00% Average Growth: 8.668%
INFO:root:2015-09-15 TP/FP: 21.21%/78.79% Average Growth: -2.354%
INFO:root:tree7y600prefilter Average TP/FP: 63.45% / 36.55% Average Growth: 1.559%
