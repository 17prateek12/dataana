# -*- coding: utf-8 -*-
"""task1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12bHfhJFIhxlx9dKCgDj8QByqMLMAR7QU
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from google.colab import files
uploaded = files.upload()

df=pd.read_csv('tradelog.csv')

df.head

initial_portfolio_value = 6500
risk_free_rate = 0.05

total_trades = len(df)
print(total_trades)

profitable_trades = len(df[df['Exit Price'] > df['Entry Price']])
print(profitable_trades)

loss_trade=total_trades-profitable_trades
print(loss_trade)

win_rate = profitable_trades / total_trades
print(win_rate)

df['Trade Profit'] = df['Exit Price'] - df['Entry Price']
average_profit_per_trade = df[df['Trade Profit'] > 0]['Trade Profit'].mean()
print(average_profit_per_trade)

average_loss_per_trade = df[df['Trade Profit'] < 0]['Trade Profit'].mean()
print(average_loss_per_trade)

risk_reward_ratio = average_profit_per_trade / abs(average_loss_per_trade)
print(risk_reward_ratio)

loss_rate = 1 - win_rate
expectancy = (win_rate * average_profit_per_trade) - (loss_rate * abs(average_loss_per_trade))
print(expectancy)

average_ror_per_trade = (expectancy / initial_portfolio_value) / (df['Exit Price'] - df['Entry Price']).std()
print(average_ror_per_trade)

sharpe_ratio = ((average_ror_per_trade - risk_free_rate) / df['Exit Price'].std())
print(sharpe_ratio)

cumulative_returns = (df['Exit Price'] - df['Entry Price']).cumsum()
max_drawdown = (cumulative_returns - cumulative_returns.expanding().max()).min()
print(max_drawdown)

max_drawdown_percentage = (max_drawdown / initial_portfolio_value) * 100
print(max_drawdown_percentage)

ending_portfolio_value = initial_portfolio_value + cumulative_returns.iloc[-1]
cagr = (ending_portfolio_value / initial_portfolio_value) ** (1 / (total_trades / 252)) - 1
print(cagr)

calmar_ratio = cagr / max_drawdown
print(calmar_ratio)

results = pd.DataFrame({
    'Parameter': ['Total Trades', 'Profitable Trades', 'Loss-Making Trades', 'Win Rate',
                  'Average Profit per trade', 'Average Loss per trade', 'Risk Reward Ratio',
                  'Expectancy', 'Average ROR per trade', 'Sharpe Ratio', 'Max Drawdown',
                  'Max Drawdown Percentage', 'CAGR', 'Calmar Ratio'],
    'Value': [total_trades, profitable_trades, loss_trade, win_rate,
              average_profit_per_trade, average_loss_per_trade, risk_reward_ratio,
              expectancy, average_ror_per_trade, sharpe_ratio, max_drawdown, max_drawdown_percentage,
              cagr, calmar_ratio]
})

results.head()

print(results)

results.to_csv('trading_results.csv', index=False)