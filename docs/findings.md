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

## First reviewer run:
    Claim: underperformance "almost certainly explained by transaction costs"	
    Check: Your Market has no transaction costs	
    Result: False. It invented a cause.

    Claim: "traded in ~140 of 146 weeks"	
    Check: 12 weeks have (no trades), so 134	
    Result: Roughly right

    Claim: best growth (weeks 58–72) had "less frequent repositioning"	
    Check: It traded in 12 of those 15 weeks	
    Result: Mostly false

    Claim: 1-share trades in weeks 34, 50, 55, 137	
    Check: Weeks 34, 50 and 55 are 1–2 share trades. Week 137 is 2–3.	
    Result: True. Real noise trades.

    Claim: week 20 sold A and B to buy C, then reversed in week 21	
    Check: W20: sold 404 A, bought 431 C. W21: sold 150 C, bought 157 A	
    Result: True (a partial reversal)

    Claim: "lock in losses"	
    Check: Value went up, $105,613 → $110,575	
    Result: False

    Claim: week 32 buys 425 B, week 33 sells 200	
    Check: Matches the table	
    Result: True

    Claim: "Week 37 sells STOCK_C, week 38 buys it back"	
    Check: Week 38 is SELL STOCK_A 25, BUY STOCK_B 31	
    Result: False. Made-up evidence.

## Updated prompt and changed model: 
    Reviewer: Haiku, short prompt	
    Quoted Rows Correct: ~50%	
    Invented Causes: Yes (transaction costs)	
    Found the problem period: No

    Reviewer: Sonnet, structured prompt	
    Quoted Rows Correct:11/11	
    Invented Causes: No, but one false supporting claim	
    Found the problem period:Yes (weeks 69–134)

## Initial lessons learned - "Keep holdings near equal-weight" and "don't switch", "don't sit in cash". This almost sounds like it is trending towards a buy and hold strategy... not what we are looking for. 

## First run with reflexion - All three runs with lessons beat every baseline run and buy-and-hold. It lifted the agent from an average of 24.1% to 66.7%. The strategy was very close to just buy-and-hold. It's a momentum rotation: 100% in whichever stock has been strongest recently, with only about 8–10 switches in three years. The agent now behaves like a rule you could write in 10 lines of Python. All three runs acted very similiarly across all three.

## The training returns didn't go up steadily (+62.5% → +70.8% → +52.1%). Round 3 did worst in training, but its lessons did best in testing. So the reviewer's lessons improved in a way the training scores didn't show.

## Trading dropped from ~250 trades to only ~18. There were 0 leaks. Lessons improved the test return from +24.1% to +66.7%, with 0 leaks. A momentum rule chosen on training data got +64.4%, so most of the improvement comes from the strategy the lessons led to. The agent beat the rule mainly on drawdown (-32.7% vs -39.6%) and with far fewer switches. The lessons' effect is visible step by step in the trade counts and concentration. The final all-in behaviour came from the agent's interpretation of the lessons, not from an explicit instruction.

