import tushare as ts
prefixes = ['600', '601', '603', '002']

for prefix in prefixes:
	for index in range(1000):
		suffix = str(index).zfill(3)
		stockId = prefix + suffix

		try:	
			stocklist = ts.get_hist_data(stockId)
			print stocklist	
		except Exception, e:
			print stockId + " is not a valid stock.\n"

