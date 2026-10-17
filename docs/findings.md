                    Return   Max drawdown	
Buy-and-hold	    +37.3%	  -33.9%

Real names, run 1	+63.9%	  -29.8%	
Real names, run 2	+28.1%	  -34.0%	
Real names, run 3	+41.8%	  -34.2%	
Un-anon data ave:   +44.6%.   -32.7%

Anonymised, run 1	+29.7%	  -31.5%
Anonymised, run 2   +11.1%    -39.4%
Anonymised, run 3   +31.6%    -36.2%
Anon data average:  +24.1%.   -35.7%


## First run - The agent said, "Apple is one of the most stable, profitable, and innovation-driven companies." It didn't learn that from your data, which had one price. It's using its training knowledge, and it knows how Apple did after 2020. This is the memorisation issue. Later run an experiment: replace "AAPL" with "Stock A" and see whether the agent trades differently.

## Second run - The agent said, "This looks like market-wide pressure (likely COVID concerns emerging in February 2020)." Confirming that it has knowledge outside of the market history supplied. Likely from the training data. Could hide tickers and dates so it wouldn't have any outside influence.

## Third run - Full 150 week run on baseline agent. The agent beat the baseline, with the final portfolio: cash: 85,261.88, positions: {'MSFT': 280, 'AAPL': 37, 'GOOGL': 100}, total_value: 163,892.99, Return: 63.9%, Max drawdown: -29.8%

## Agent went to cash in 2022 while mentioning the Fed, with dates and quotes. Proving that it is using outside references.

## Fourth run - Full 150 week run on baseline agent. The agent did worse than the baseline, with the final portfolio: cash: 123.23, positions: {'MSFT': 365, 'GOOGL': 135, 'AAPL': 245}, total_value: 128,147.99, Return: 28.1%, Max drawdown: -34.0%

## Fifth run - Full 150 week run on baseline agent. The agent beat the baseline, with the final portfolio cash: 11,855.57, positions: {'MSFT': 147, 'AAPL': 381, 'GOOGL': 539}, total_value: 141,811.80, Return: 41.8%, Max drawdown: -34.2%

## Sixth run (anon data) - Full 150 week run on baseline agent. The agent did worse than the baseline, with the final portfolio: cash: 58,107.78, positions: {'STOCK_A': 154, 'STOCK_C': 289}, total_value: 129,693.39, Return: 29.7%, Max drawdown: -31.5%

## Seventh run (anon data) - Full 150 week run on baseline agent. The agent did worse than the baseline, with the final portfolio: cash: 12,919.07, positions: {'STOCK_B': 100, 'STOCK_C': 440, 'STOCK_A': 100}, total_value: 111,050.26, Return: 11.1%, Max drawdown: -39.4%

## Eigth run (anon data) - Full 150 week run on baseline agent. The agent did worse than the baseline, with the final portfolio: cash: 9,005.39, positions: {'STOCK_A': 201, 'STOCK_C': 567}, total_value: 131,588.06, Return: 31.6%, Max drawdown: -36.2%

# Hiding the names and dates cut the average return by about 20 points, and the anonymised agent lost to buy-and-hold in all three runs. So the agent's apparent edge came mostly from remembering history, not from reading the prices