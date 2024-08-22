# Cryptocurrency comparison program useage and istalltion guide.
## What is this program for?
My program is created for an coding assement. It saves the top 20 coins and their price data for a year and then plots it so you can see the changes in prices and if other coins crash or fall at the same time.

### How do I run the program?
1. Simply use the below command in your terminal.
```
pip install -r requirements.txt
```
2. Click the run button in your preferred IDE (In App.py) and then give the program a second.
3. Follow the terminal instructions and open the link. (Shown below)
4. The program is running and you can navigate around the GUI. However when plotting the chart Flask can sometimes take up to 20 seconds so be patient and don't assume the program has failed, I know this isn’t ideal but this is to create over 7,300 lines with multiple columns and save them to csv files. (Note if coin gecko isn’t working and the program is using backups it’s generally very fast)
5. Once you are finished click into the terminal and then press Ctr+C at the same time and wait for the errors to stop. Once they finish the locally hosted website has closed. You can then read through the terminal to see your dataframe or go into the static folder to look at your most recent plot.

### Common Errors and Solutions
- Selecting past 364 days will result in an error as the dataset only plots the last year.
   - Solution: Don't type in past the date
- Bad scaling. This isn't really an error more just an oversight as cryptocurrencies are very diverse leading some lines that look like they don't move or that they are on zero in reality their price is just very close to USD
   - Solution: Unfortunately there isn't one if you need more accurate data try plotting the coin by itself.
- Typing a string into the days column causes matplotlib + pandas to have a crisis
    - Solution: Don't type in a string
- I can't see the cryptocurrency  I want to plot?. 
    - Solution: In the getcoins function change the vaule in the params dictionary to create more pages and they should hypothetically work. However most people won't want to plot anymore than the Top 20 coins.