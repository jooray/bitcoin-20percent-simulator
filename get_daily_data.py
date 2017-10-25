import json

last_day_start=0
day_length=3600*24
prices = []

with open("bitstampUSD.csv", "r") as f:
 for line in f:
     timestamp,price,amount = line.rstrip().split(",")
     if (last_day_start == 0):
         last_day_start=int(timestamp)
     if int(timestamp) > (last_day_start+day_length):
         prices.append(float(price))
         last_day_start = last_day_start+day_length

with open('bitcoin-price-data.json', 'w') as outfile:
    json.dump(prices, outfile)