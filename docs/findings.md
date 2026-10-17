## First run - The agent said, "Apple is one of the most stable, profitable, and innovation-driven companies." It didn't learn that from your data, which had one price. It's using its training knowledge, and it knows how Apple did after 2020. This is the memorisation issue. Later run an experiment: replace "AAPL" with "Stock A" and see whether the agent trades differently.

## Second run - The agent said, "This looks like market-wide pressure (likely COVID concerns emerging in February 2020)." Confirming that it has knowledge outside of the market history supplied. Likely from the training data. Could hide tickers and dates so it wouldn't have any outside influence.

## Third run - Full 150 week run on baseline agent. The agent beat the baseline, with the final portfolio: cash: 85,261.88, positions: {'MSFT': 280, 'AAPL': 37, 'GOOGL': 100}, total_value: 163,892.99, Return: 63.9%, Max drawdown: -29.8%

## Agent went to cash in 2022 while mentioning the Fed, with dates and quotes. Proving that it is using outside references.

## Fourth run - Full 150 week run on baseline agent. The agent beat the baseline, with the final portfolio: cash: 123.23, positions: {'MSFT': 365, 'GOOGL': 135, 'AAPL': 245}, total_value: 128,147.99, Return: 28.1%, Max drawdown: -34.0%

## Fifth run - Full 150 week run on baseline agent. The agent beat the baseline, with the final portfolio cash: 11,855.57, positions: {'MSFT': 147, 'AAPL': 381, 'GOOGL': 539}, total_value: 141,811.80, Return: 41.8%, Max drawdown: -34.2%