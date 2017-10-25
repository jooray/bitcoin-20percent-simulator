import json
import random
import numpy as np
import matplotlib.pyplot as plt

# parameters
payout_percentage_trigger = 0.2 # trigger for payout
payout_percentage = 0.2 # what percentage is the payout
investment_window = 48 # months
invest_every_days = 2 # 28 = monthly investing, 2 = every other day, 7 = weekly
base_currency_monthly_investments = 100 # all the monthly investments combined

# which day to start
start_day = 788


# price functions

# just a sample pricing
def get_linear_price(day):
    return (day + 1) * 2

# real prices
historical_prices = []

def load_historical_prices():
    global historical_prices, start_day
    with open('bitcoin-price-data.json') as data_file:    
        historical_prices = json.load(data_file)
    if start_day == -1:
        start_day=random.randint(0,len(historical_prices)-(investment_window*28))
    del historical_prices[:start_day]

def get_historical_price(day):
    global historical_prices
    if len(historical_prices)==0:
        load_historical_prices()
    return historical_prices[day]
    

def get_bitcoin_price(day):
    return get_historical_price(day)


# investment modelling

investments = []
invested_base = 0.0
withdrew_base = 0.0

def reset_investments():
    global investments, invested_base, withdrew_base
    investments = []
    invested_base = 0.0
    withdrew_base = 0.0

# invest sum in base currency (eur)


def invest(base_amount, day, record_base = True):
    global invested_base, investments
    investments.append(
        {"day": day,
         "base_amount": base_amount,
         "bitcoin_amount": base_amount / get_bitcoin_price(day)})
    if (record_base):
        invested_base = invested_base + base_amount


def get_portfolio_invested_base_value(day=0):
    base_value = 0
    for investment in investments:
        if (day == 0) or (investment['day'] <= day):
            base_value = base_value + investment['base_amount']
    return base_value

def get_portfolio_current_base_value(day):
    base_value = 0
    for investment in investments:
        base_value = base_value + (investment['bitcoin_amount'] * get_bitcoin_price(day))
    return base_value

def get_portfolio_bitcoin_value(day=0):
    bitcoin_value = 0
    for investment in investments:
        if (day == 0) or (investment['day'] <= day):
            bitcoin_value = bitcoin_value + investment['bitcoin_amount']
    return bitcoin_value

# lazy man's implementation - all the investments will be replaced by one investment
def withdraw_base(base_amount, day):
    global withdrew_base, investments
    new_base = (get_portfolio_current_base_value(day) - base_amount)
    investments = []
    invest(new_base, day, False)
    withdrew_base = withdrew_base + base_amount

def print_investment_data(day):
    print(" Withdrew: " + str(withdrew_base))
    print(" Current value: " + str(get_portfolio_current_base_value(day)))
    print(" Withdrawals+current value: " + str(withdrew_base + get_portfolio_current_base_value(day)))
    print(" Invested: " + str(invested_base))

g_withdraws = []
g_current_with_withdraws = []
g_just_invest = []

g_btc_in_fiat_values = []
g_dividend_in_fiat_value = []
g_combined_value = []
g_justbuy_fiat_value = []
g_invested_fiat = []

load_historical_prices()

###############################################################################################################
#print("Investment strategy with withdrawals:")

reset_investments()
for month in range(investment_window):
    for day in range(28):
        if day % invest_every_days == 0:
            invest((base_currency_monthly_investments*invest_every_days/28), day+(month*28))
        if (get_portfolio_current_base_value((month*28+day)) >= (get_portfolio_invested_base_value() * (payout_percentage_trigger+1))):
            #withdraw_base(get_portfolio_current_base_value((month*28)+day) * 0.2, (month*28)+day)
            withdraw_base(get_portfolio_current_base_value((month*28)+day) * payout_percentage, (month*28)+day)
        g_btc_in_fiat_values.append(get_portfolio_current_base_value((month*28)+day))
        g_dividend_in_fiat_value.append(withdrew_base)
        g_combined_value.append(get_portfolio_current_base_value((month*28)+day)+withdrew_base)

#print_investment_data(investment_window*28)
###############################################################################################################
#print("Investment strategy without any withdrawals (just buying bitcoin)")
reset_investments()
invested_so_far = 0.0
for month in range(investment_window):
    for day in range(28):
        if day % invest_every_days == 0:
            invest((base_currency_monthly_investments*invest_every_days/28), day+(month*28))
            invested_so_far = invested_so_far + (base_currency_monthly_investments*invest_every_days/28)
        g_justbuy_fiat_value.append(get_portfolio_current_base_value((month*28)+day))
        g_invested_fiat.append(invested_so_far)

plt.plot(g_combined_value, 'r')
plt.plot(g_dividend_in_fiat_value, 'g')
plt.plot(g_justbuy_fiat_value, 'b')
plt.plot(g_btc_in_fiat_values, 'y')
plt.plot(g_invested_fiat, 'gray')

plt.xlabel('day')
plt.ylabel('value in usd')
plt.show()