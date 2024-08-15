import pandas as pd
# This file is here so I can play with trying to save the data I want into columns will complete at home
coins_df = pd.DataFrame(columns=['Coin Id'])
coins_df.to_csv("data-saves/new.csv")
print(coins_df)