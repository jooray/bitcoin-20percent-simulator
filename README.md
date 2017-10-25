Motivation
==========

This software was simulation of a strategy I talked about in my talk
[Using Bitcoin as a store of
value](https://juraj.bednar.io/talk/2017/03/18/bitcoin-as-a-store-of-value/).
There is also a [version in
Slovak](https://juraj.bednar.io/talk/2017/04/12/bitcoin-ako-ulozisko-hodnoty/)
and the [more recent slides from my HCPP17 talk are available as well](http://bit.ly/cryptos-store),
although the recording is not out yet.

I don't think these scripts are of any use if you have not seen the
talk, so before you ask and try to play with it, go and see the full
video recording, so you understand what is happening here.

20 percent portfolio simulation
===============================

This software makes simulates the following strategy:

Invest 100 USD in BTC every month. When the price of the portfolio
increases by 20% (*payout_percentage*), withdraw the 20% to USD and
continue with the strategy. This condition is checked daily.

The software simulates the outcome of this strategy (red lines)
vs. pure buying of Bitcoin (blue line).

Blue lines represent the USD value of the portfolio after the
investment window (default 24 months, *investment_window*).

Red line contains the USD value of bitcoin portfolio at the end
of the investment window plus all the USD withdrawals (green line)
in the withdrawal strategy.

Yellow line is the amount invested (it is always *investment_window* *
100).

If the blue or red lines are below the yellow line, the strategy was
a net loss.

Each x represents the state of the investment strategies **at the end
of the investment period that started at that day**. The graph does
not represent the change in values in that portfolio, it represents
multiple portfolios depending on when the investor started.

Simplifications: For simplicity, "a month" is defined as 28 days

Results:
 * the longer the portfolio duration, the safer at least on historical
   data both strategies are. Invest long term, buy every month, if
   historical data are good enough.
 * for shorter periods, if Bitcoin goes down, the 20 percent strategy
   slightly outperforms the pure buying strategy
 * with 20 percent strategy, you can use the withdrawals to power your
   business or other investments, so that's an advantage
 * investing more often (even if the same monthly amount) resulted in
   higher returns in both strategies. Maybe even investing very small
   amounts daily is better than one transaction per month or weekly
   transactions.

Technical details
=================

*get_daily_data.py* converts [bitstampUSD.csv BitcoinCharts.com](http://api.bitcoincharts.com/v1/csv/bitstampUSD.csv.gz)
to a JSON representation of prices with daily bitcoin price (no
averaging, first price of that day). You have to download it manually.

*bitcoin-fund.py* simulates the investment strategies over all possible
start days to see the difference between good days and bad days, the
colors are described above

*bitcoin-fund-one-run.py* runs the strategy at *start_day* in the script
and displays the investment strategy as follows:

 * blue - value in fiat if you are just buying BTC
 * red - value in fiat (dividends and btc value) of the strategy
 * green - dividend payout of the strategy
 * yellow - value of bitcoin portfolio in fiat
 * gray - invested fiat


Installation
============

This requires Python3 and matplotlib.

```bash
pip3 install -r requirements.txt # or maybe pip, depending on your setup
wget -O - http://api.bitcoincharts.com/v1/csv/bitstampUSD.csv.gz | gzip -dc > bitstampUSD.csv
python3 ./get_daily_data.py
```


