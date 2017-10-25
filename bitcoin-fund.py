import json
import random
import numpy as np
import matplotlib.pyplot as plt

# parameters
payout_percentage_trigger = 0.15 # trigger for payout
payout_percentage = 0.3 # what percentage is the payout
investment_window = 24 # months
invest_every_days = 7 # 28 = monthly investing, 2 = every other day, 7 = weekly
base_currency_monthly_investments = 100 # all the monthly investments combined


# price functions

# just a sample pricing
def get_linear_price(day):
    return (day + 1) * 2

# real prices
historical_prices = []
start_day = 0

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

# invest sum in base currency (usd)


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

load_historical_prices()

###################################################################################################################
# If you want to zoom in, change the 0 in range to 400 or 500
for i in range(500, len(historical_prices)-(investment_window*28), 1):

    start_day = i
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

    #print_investment_data(investment_window*28)
    g_withdraws.append(withdrew_base)
    g_current_with_withdraws.append(withdrew_base + get_portfolio_current_base_value(investment_window*28))
    ###############################################################################################################
    #print("Investment strategy without any withdrawals (just buying bitcoin)")
    reset_investments()
    for month in range(investment_window):
        for day in range(28):
            if day % invest_every_days == 0:
                invest((base_currency_monthly_investments*invest_every_days/28), day+(month*28))

    #print_investment_data(investment_window*28)
    g_just_invest.append(get_portfolio_current_base_value(investment_window*28))

bad_start_days = 0
for i in g_just_invest:
    if i<invested_base:
        bad_start_days = bad_start_days + 1

print('Percentage of bad days to start the just invest strategy:' + str((bad_start_days*100)/len(g_just_invest)))

plt.plot(g_current_with_withdraws, 'r')
plt.plot(g_withdraws, 'g')
plt.plot(g_just_invest, 'b')
plt.plot((0,len(g_withdraws)), (invested_base, invested_base), 'y')

plt.xlabel('starting day')
plt.ylabel('money (usd)')
plt.show()
