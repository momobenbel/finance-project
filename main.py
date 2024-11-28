import yfinance as yf

novartis = yf.Ticker("NVS")
walmart = yf.Ticker("WMT")
data = yf.download(["NVS", "WMT"], period = "3y", interval = "1d")

# PAGE 2-3

""" 1)
Take the historical stock and bond prices, apply different valuation
methods to assess whether the stock price is fair. If bonds are not
present, try to assess what would be the bond price in any case (looking
at the firm ratings of similar firms), or check whether they have loans
in the balance sheet and try to assess interest rate from the interest
payments (interests/total bank debt)
"""
# STOCK VALUATION BY COMPARABLES
print("Stock valuation by COMPARABLES")

# STOCK VALUATION BY AVERAGE P/E RATIO
print("\nStock valuation by AVERAGE P/E RATIO")
# Define the ticker symbols for the companies
novartis_comparables = ['SNY', 'AZN', 'GSK', 'RHHBY']
# Sanofi, Astrazeneca PLC, GSK PLC, Roche Holding AG

# Initialize a list to store P/E ratios
novartis_pe_ratios = []

for ticker in novartis_comparables:
    stock = yf.Ticker(ticker)
    pe_ratio = stock.info['trailingPE'] 
    print(f"{ticker}: P/E Ratio = {pe_ratio}")
    novartis_pe_ratios.append(pe_ratio)

# Calculate and print the average P/E ratio
novartis_average_pe = sum(novartis_pe_ratios) / len(novartis_pe_ratios)
print(f"Average P/E Ratio = {novartis_average_pe}")

# Now, get Novartis' EPS
novartis_ticker = 'NVS'  
novartis_stock = yf.Ticker(novartis_ticker)
novartis_eps = novartis_stock.info['trailingEps']  # Get trailing EPS

# Print Novartis' EPS
print(f"Novartis' EPS: {novartis_eps}")

# Multiply Novartis' EPS by the average P/E ratio
novartis_estimated_price = novartis_eps * novartis_average_pe
print(f"Stock valuation by comparable based on Average P/E Ratio = {novartis_estimated_price}\n")

# STOCK VALUATION BY AVERAGE P/B RATIO
print("\nStock valuation by AVERAGE P/B RATIO")

# Initialize a list to store P/B ratios
novartis_pb_ratios = []

# Fetch and print P/B ratios for the comparables
for ticker in novartis_comparables:
    stock = yf.Ticker(ticker)
    pb_ratio = stock.info['priceToBook']  # Get price to book value
    print(f"{ticker}: P/B Ratio = {pb_ratio}")
    novartis_pb_ratios.append(pb_ratio)

# Calculate and print the average P/B ratio
novartis_average_pb = sum(novartis_pb_ratios) / len(novartis_pb_ratios)
print(f"Average P/B Ratio = {novartis_average_pb}")
balance_sheet = novartis.balance_sheet

bv = balance_sheet.loc['Total Assets'] - balance_sheet.loc['Total Liabilities Net Minority Interest']
bvps = bv[0]/novartis.info.get('sharesOutstanding')
price_pb = bvps * novartis_average_pb
print(f"Estimated Price Based on Average P/B Ratio = {price_pb}")

"""
novartis_total_assets = novartis_stock.info.get('totalAssets')
novartis_total_liabilities = novartis_stock.info.get('totalLiab')
novartis_shares_outstanding = novartis_stock.info.get('sharesOutstanding',1)  # Prevent division by zero

# Calculate Book Value Per Share without Net Minority Interest (as it might not be directly available)
novartis_bvps = (novartis_total_assets - novartis_total_liabilities) / novartis_shares_outstanding

print(f"Novartis' Approximated Book Value Per Share: {novartis_bvps}")

# Use the previously calculated average P/B ratio (novartis_average_pb) here
estimated_price = novartis_bvps * novartis_average_pb
print(f"Estimated Price Based on Average P/B Ratio = {estimated_price}")
"""

# ----------------------------------------------------------------------------------------------------------------------

# STOCK VALUATION BY P/E RATIO
print("\nStock valuation by AVERAGE P/E RATIO")

# WALMART

# Define the ticker symbols for Walmart's comparables
walmart_comparables = ['TGT', 'COST', 'DG', 'DOL.TO']
# Target Corporation, Costco Wholesale Corporation, Dollar General Corporation, Dollarama Inc.

# Initialize a list to store P/E ratios
walmart_pe_ratios = []

# Fetch and print P/E ratios for the comparables
for ticker in walmart_comparables:
    stock = yf.Ticker(ticker)
    pe_ratio = stock.info['trailingPE']
    print(f"{ticker}: P/E Ratio = {pe_ratio}")
    walmart_pe_ratios.append(pe_ratio)

# Calculate and print the average P/E ratio
walmart_average_pe = sum(walmart_pe_ratios) / len(walmart_pe_ratios)
print(f"Average P/E Ratio for Walmart's Comparables = {walmart_average_pe}")

# Now, get Walmart's EPS
walmart_ticker = 'WMT'  # Walmart's ticker symbol
walmart_stock = yf.Ticker(walmart_ticker)
walmart_eps = walmart_stock.info['trailingEps']  # Get trailing EPS

# Print Walmart's EPS
print(f"Walmart's EPS: {walmart_eps}")

# Multiply Walmart's EPS by the average P/E ratio
estimated_price = walmart_eps * walmart_average_pe
print(f"Estimated Walmart Price Based on Average P/E Ratio = {estimated_price}")

# -----------------------------------------------------------------------------------------------------------------------


"""
CAPM = 0.04351 + uber.info['beta']*0.046
print(CAPM)



# UBER
uber_income_statement = uber.financials
uber_balance_sheet = uber.balance_sheet
uber_cash_flow_statement = uber.cashflow

#uber_total_debt = uber_balance_sheet.loc['Total Debt']
#uber_interest_expense = uber_income_statement.loc['Interest Expense']
#uber_interest_rates = (uber_interest_expense/uber_total_debt)*100
#print("Uber's interest rates are:\n", uber_interest_rates.map("{:.2f}%".format))

# AIRBNB
airbnb_income_statement = airbnb.financials
airbnb_balance_sheet = airbnb.balance_sheet
airbnb_cash_flow_statement = airbnb.cashflow

#airbnb_total_debt = airbnb_balance_sheet.loc['Total Debt']
#airbnb_interest_expense = airbnb_income_statement.loc['Interest Expense']
#airbnb_interest_rates = (airbnb_interest_expense/airbnb_total_debt)*100
#print("Airbnb's interest rates are:\n", airbnb_interest_rates.map("{:.2f}%".format))

 2)
Take the last 5 years balance-sheets to assess the growth and other
parameters to compute the discounting factor model, and then you
compare your computation with the current stock price. For the return
on equity, you can use what is reported from the firm analysts or use
the beta calculation below From week 5-6:


#UBER

#Compound Annual Growth Rate (CAGR), for Total Assets and Shareholder's equity
# Function to calculate CAGR for both total assets and total equity
def calculate_cagr(ending_value, starting_value, number_of_years):
    return (ending_value / starting_value) ** (1 / number_of_years) - 1

starting_assets = 33252000  # Total assets from 2020 (in thousands)
ending_assets = 38699000    # Total assets from 2023 (in thousands)

starting_equity = 13754000  # Total equity from 2020 (in thousands)
ending_equity = 12682000    # Total equity from 2023 (in thousands)

number_of_years = 3

# Calculate CAGR for Total Assets
assets_cagr = calculate_cagr(ending_assets, starting_assets, number_of_years)
# Calculate CAGR for Total Equity
equity_cagr = calculate_cagr(ending_equity, starting_equity, number_of_years)

# Print out the results
print(f"CAGR for Total Assets: {assets_cagr:.4f} or {assets_cagr*100:.2f}%")
# 5.19%. This indicates a moderate growth in assets over the period.
print(f"CAGR for Total Equity: {equity_cagr:.4f} or {equity_cagr*100:.2f}%")
# This negative rate suggests that equity actually decreased on average each year over this period, 
# which could be due to a variety of factors such as share buybacks, dividends, or losses.




 3)
Compute the betas of the firms based on the last 5 years series of
stock prices. You find stock prices on yahoo.finance. Discuss the risk
according to your results.


import pandas as pd
import datetime

# UBER

# Defining stock ticker and index ticker, Uber and S&P 500
uber_stock_ticker = 'UBER'
uber_index_ticker = '^GSPC'

# Define time period for the analysis
uber_end_date = datetime.datetime.now()
uber_start_date = datetime.datetime(2019, 6, 1)


# Fetch historical data from Yahoo Finance
uber_stock_data = yfinance.download(uber_stock_ticker, uber_start_date, uber_end_date, interval = "1mo")
uber_index_data = yfinance.download(uber_index_ticker, uber_start_date, uber_end_date, interval = "1mo")

# Calculate daily returns
uber_stock_returns = uber_stock_data['Adj Close'].pct_change()
uber_index_returns = uber_index_data['Adj Close'].pct_change()

# Calculate covariance between stock and index returns, and variance of index returns
uber_covariance = uber_stock_returns.cov(uber_index_returns)
uber_variance = uber_index_returns.var()

# Calculate beta
uber_beta = uber_covariance / uber_variance
print(f'Beta for {uber_stock_ticker} relative to {uber_index_ticker}: {uber_beta}')

# AIRBNB

# Defining stock ticker and index ticker, Airbnb and Nasdaq Composite
airbnb_stock_ticker = 'ABNB'
airbnb_index_ticker = '^IXIC'

# Define time period for the analysis
airbnb_end_date = datetime.datetime.now()
airbnb_start_date = datetime.datetime(2020, 12, 7)

# Fetch historical data from Yahoo Finance
airbnb_stock_data = yfinance.download(airbnb_stock_ticker, airbnb_start_date, airbnb_end_date, interval = "1mo")
airbnb_index_data = yfinance.download(airbnb_index_ticker, airbnb_start_date, airbnb_end_date, interval = "1mo")

# Calculate daily returns
airbnb_stock_returns = airbnb_stock_data['Adj Close'].pct_change()
airbnb_index_returns = airbnb_index_data['Adj Close'].pct_change()

# Calculate covariance between stock and index returns, and variance of index returns
airbnb_covariance = airbnb_stock_returns.cov(airbnb_index_returns)
airbnb_variance = airbnb_index_returns.var()

# Calculate beta
airbnb_beta = airbnb_covariance / airbnb_variance
print(f'Beta for {airbnb_stock_ticker} relative to {airbnb_index_ticker}: {airbnb_beta}')

"""


