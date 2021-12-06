'''
Research Question: 
How do various quantitative pieces of financial data affect and correlate with 
 their company’s current share price?

We are interested in the intersection of data science and finance and hope to 
 analyze any possible correlations between financial data and closing stock
 price. We became interested in this topic after watching an interview with Jim
 Simons. He tracked the correlation between an uncountable amount of variables
 and stock prices. It is commonly said that they tracked this correlation
 between stock price and almost every possible variable that could be tracked
 over time.

---
Our Data:
Our data consists of Compustat and Yahoo Finance exported csv files for our two
  companies, Apple and Google.
We collected the quarterly data from Jan 2000 - Jan 2021 for all major
 collected financial data on Compustat, and the monthly close price data
 on Yahoo Finance.

We have over 600 variables for the 84 quarters in our time range, with an
  entry representing an equivalent value on the 10-Q or 10-K. An empty space
 represents 0 or N/A, as provided by Compustat.
Relevant variables will be taken when needed using the following key:
 https://www.crsp.org/products/documentation/quarterly-data-industrial
 Stock price data was taken from one csv and imported into the df.

---
Data Analysis:
We are working with dataframes using pandas to simplify how we worked with the
 data.
Our functions either calculate a ratio and add it to our dataframe, or graph
 the ratio against the stock price.
For each function, we calculated the correlation betweeen stock price and the
 associated ratio and reported this.

---
Data Interpretation:
After analyzing the 8 apple and 7 google graphs, it is clear that certain
 metrics and relationships are hard to predict, even across companies in the
 same industry.
For example, in the case of apple and google's current ratios, it is extremely
 unexpected for apple's to be very close to 1 in comparison to google's 3.
Our graphs are extremely easy to follow by being labeled and titled. We also
 graphed the linear regression for the information.
Our next steps include analyzing more companies in the tech industry and
 possibly branching off into other industries.
We also hope to analyze the most 5 or 10 years instead of just the last
 20 years, since the tech industry is constantly innovating.

'''

import matplotlib.pyplot as plt
import pandas as pd  # useful library to handle dataframe
import numpy as np  # useful library to handle array and computation

APPLE_FILE = "apple_ds.csv"
APPLE_PRICE_FILE = "AAPL_Project.csv"
GOOGLE_FILE = "googl_ds.csv"
GOOGLE_PRICE_FILE = "GOOGL_Project.csv"

def read_csv(infile):
    '''
    Function will read in our csv file 
    
    Function will take a infile

    Function will return a dataframe
    '''
    
    # Creates a dataframe with the data from the file
    df = pd.read_csv(infile)
        
    return df

def df_slice(df, periods):
    '''
    Function will slice a df into a new df based on the parameters
    
    Function will take in a df, an int that represents the num of periods
    
    Function will return a new df
    '''
    # for example, 40 quarters = 10 years
    # so we must slice up to 84-40 or 44
    slice_int = 84 - periods
    df2 = df.drop(df.index[:slice_int])
    # Fixing indexing after slicing
    df2 = df2.reset_index()
    
    return df2

def get_colors(df):
    '''
    Function will add a color to each row depending on if the row is a 10-K
    or a 10-Q
    
    Function will take a dataframe

    Function will return nothing but update data to contain a color based on
    the report
    '''
    # Creates a new element in the header and sets all values to NaN
    df["clean_color"] = np.nan
    
    # If it's the 4th quarter, red will be appended to the corresponding row.
    for i in range(0, df.shape[0]):
        if 'Q4' in df.loc[i, 'datacqtr']:
            df.loc[i, 'clean_color'] = 'red'
        else:
            df.loc[i, 'clean_color'] = 'blue'
            
        
def get_stats(desired_stat, df):
    '''
    Function will focus on one stat in the entire dataset 

    Function will take a string, desired_stat, and the dataframe

    Function will return the information as a list containing a number for
    every quarter in our 21 year period
    '''
    stat_list = []
    
    # Appends our desired stat to the stat_list for each corresponding period
    for i in range (0, df.shape[0]):
        stat_list.append(df.loc[i, desired_stat])
        
    return stat_list

def get_stock_price(df, price_df):
    '''
    Function will get the stock price at the end of each quarter 
    and add it to a column in the dataframe
    
    Function will take our main dataframe and the dataframe containing our
    price information

    Function will return nothing, just add a column to the main dataframe
    '''
    
    # Creates a new column in the main dataframe and sets all the values to NaN
    df["stock_price"] = np.nan
    for i in range(0, df.shape[0]):
        # Appends every Adj Price to its corresponding row in the main dataframe
        df.loc[i, "stock_price"] = price_df.loc[i, "Adj Close"]  
        
def calc_cur_ratio(df):
    '''
    Function will calculate the current ratio (Current assets/current
                                               liabilities)
    
    Function will take in a dataframe
    
    Function will return northing and just add a column to the dataframe
    '''
    # Creats a new column in the dataframe
    df['cur_ratio'] = np.nan
    
    # Calculates the current ratio and sets it to its corresponding location
    # in the dataframe
    for i in range(0, df.shape[0]):
        df.loc[i, 'cur_ratio'] = df.loc[i, 'actq'] / df.loc[i, 'lctq']

def calc_corr(df1, df2):
    '''
    Function will calculate the correlation between two columns in a dataframe

    Function will take in a dataframe

    Function will return a float that represents the correlation between -1.0
    and 1.0

    '''
    
    # Calculates correlation
    correlation = df1.corr(df2)
    
    return correlation

def graph_cur_ratio_to_stock(df, company):
    '''
    Function will graph the stock price against the current ratio
    
    Function will take in the main dataframe, company as a string
    
    Function will return nothing, just creates a plot
    '''
    
    # Makes the plot bigger
    plt.figure(figsize= (16,12))
    
    # Plots the points as a scatter plot
    plt.scatter(df['stock_price'], df['cur_ratio'])
    
    # Calculaates the slope and y-intercept of the line of best fit
    m, b = np.polyfit(df['stock_price'], df['cur_ratio'], 1)
    
    # Plots the line of best fit
    plt.plot(df['stock_price'], m*df['stock_price'] + b, "--", color = "Red",
             label = "Line-of-Best-Fit")
    
    # Calculates the correlation of these two points
    cur_ratio_to_stock_corr = calc_corr(df['stock_price'], df['cur_ratio'])
    
    # Important graphing functions
    fig_title = company + " Share Price vs. Current Ratio"
    plt.title(fig_title)
    x_label = "Share Price \n Correlation: " + \
        str(round(cur_ratio_to_stock_corr, 5))
    plt.xlabel(x_label)
    plt.ylabel("Current Ratio")
    plt.legend()
    
    # different fig name based on the company
    fig_name = company + "_SharePrice_to_CurrentRatio.png"
    plt.savefig(fig_name)
    
    plt.show()
    print("Current Ratio Correlation: ",cur_ratio_to_stock_corr)

def calc_roa_ratio(df):
    '''
    Function will calculate the return on assets (net income / average total
                                                  assets)
    
    Function will take in a dataframe
    
    Function will return nothing and just add a column to the dataframe
    '''
    # Creats a new column in the dataframe
    df['roa_ratio'] = np.nan
    
    # Calculates the roa and sets it to its corresponding location in the
    # dataframe
    
    # Our denominator is usually an average with the previous quarter
    # So for the first quarter we are not taking an average
    df.loc[0, 'roa_ratio'] = df.loc[0, 'niq'] / df.loc[0, 'atq']
    for i in range(1, df.shape[0]):
        average_atq = (df.loc[i, 'atq'] + df.loc[i-1, 'atq']) / 2
        df.loc[i, 'roa_ratio'] = df.loc[i, 'niq'] / average_atq

def graph_roa_ratio_to_stock(df, company):
    '''
    Function will graph the stock price against the roa ratio
    
    Function will take in the main dataframe, company as a string
    
    Function will return nothing, just creates a plot
    '''
    
    # Makes the plot bigger
    plt.figure(figsize= (16,12))
    
    # Plots the points as a scatter plot
    plt.scatter(df['stock_price'], df['roa_ratio'])
    
    # Calculates the slope and y-intercept of the line of best fit
    m, b = np.polyfit(df['stock_price'], df['roa_ratio'], 1)
    
    # Plots the line of best fit
    plt.plot(df['stock_price'], m*df['stock_price'] + b, "--", color = "Red",
             label = "Line-of-Best-Fit")
    
    # Calculates the correlation of these two points
    roa_ratio_to_stock_corr = calc_corr(df['stock_price'], df['roa_ratio'])

    fig_title = company + " Share Price vs. Return on Assets"
    plt.title(fig_title)
    x_label = "Share Price \n Correlation: " + \
        str(round(roa_ratio_to_stock_corr, 5))
    plt.xlabel(x_label)
    plt.ylabel("Return on Assets")
    plt.legend()
    
    # different fig name based on the company
    fig_name = company + "_SharePrice_to_ReturnOnAssets.png"
    plt.savefig(fig_name)
    
    plt.show()
    print("ROA Correlation: ",roa_ratio_to_stock_corr)

def calc_roe_ratio(df):
    '''
    Function will calculate the return on equity (net income / average
                                                  shareholder equity)
    
    Function will take in a dataframe
    
    Function will return nothing and just add a column to the dataframe
    '''
    # Creats a new column in the dataframe
    df['roe_ratio'] = np.nan
    
    # Calculates the roe and sets it to its corresponding location in the
    # dataframe
    
    # Our denominator is usually an average with the previous quarter
    # So for the first quarter we are not taking an average
    df.loc[0, 'roe_ratio'] = df.loc[0, 'niq'] / df.loc[0, 'seqq']
    for i in range(1, df.shape[0]):
        average_seqq = (df.loc[i, 'seqq'] + df.loc[i-1, 'seqq']) / 2
        df.loc[i, 'roe_ratio'] = df.loc[i, 'niq'] / average_seqq

def graph_roe_ratio_to_stock(df, company):
    '''
    Function will graph the stock price against the roe ratio
    
    Function will take in the main dataframe, company as a string
    
    Function will return nothing, just creates a plot
    '''
    
    # Makes the plot bigger
    plt.figure(figsize= (16,12))
    
    # Plots the points as a scatter plot
    plt.scatter(df['stock_price'], df['roe_ratio'])
    
    # Calculates the slope and y-intercept of the line of best fit
    m, b = np.polyfit(df['stock_price'], df['roe_ratio'], 1)
    
    # Plots the line of best fit
    plt.plot(df['stock_price'], m*df['stock_price'] + b, "--", color = "Red",
             label = "Line-of-Best-Fit")
    
    # Calculates the correlation of these two points
    roe_ratio_to_stock_corr = calc_corr(df['stock_price'], df['roe_ratio'])
    
    fig_title = company + " Share Price vs. Return on Equity"
    plt.title(fig_title)
    x_label = "Share Price \n Correlation: " + \
        str(round(roe_ratio_to_stock_corr, 5))
    plt.xlabel(x_label)
    plt.ylabel("Return on Equity")
    plt.legend()
    
    fig_name = company + "_SharePrice_to_ReturnOnEquity.png"
    plt.savefig(fig_name)
    
    plt.show()
    print("ROE Correlation: ",roe_ratio_to_stock_corr)      

def calc_profit_margin(df):
    '''
    Function will calculate the net profit margin (net income / net sales
                                                   revenue)
    
    Function will take in a dataframe
    
    Function will return nothing and just add a column to the dataframe
    '''
    # Creats a new column in the dataframe
    df['profit_margin'] = np.nan
    
    # Calculates the net profit margin and sets it to its corresponding
    # location in the dataframe
    
    for i in range(0, df.shape[0]):
        df.loc[i, 'profit_margin'] = df.loc[i, 'niq'] / df.loc[i, 'saleq']
    
def graph_profit_margin_to_stock(df, company):
    '''
    Function will graph the stock price against the net profit margin
    
    Function will take in the main dataframe, company as a string
    
    Function will return nothing, just creates a plot
    '''
    
    # Makes the plot bigger
    plt.figure(figsize= (16,12))
    
    # Plots the points as a scatter plot
    plt.scatter(df['stock_price'], df['profit_margin'])
    
    # Calculates the slope and y-intercept of the line of best fit
    m, b = np.polyfit(df['stock_price'], df['profit_margin'], 1)
    
    # Plots the line of best fit
    plt.plot(df['stock_price'], m*df['stock_price'] + b, "--", color = "Red",
             label = "Line-of-Best-Fit")
    
    # Calculates the correlation of these two points
    profit_margin_to_stock_corr = calc_corr(df['stock_price'],
                                            df['profit_margin'])

    fig_title = company + " Share Price vs. Net Profit Margin"
    plt.title(fig_title)
    x_label = "Share Price \n Correlation: " + \
        str(round(profit_margin_to_stock_corr, 5))
    plt.xlabel(x_label)
    plt.ylabel("Net Profit Margin")
    plt.legend()
    
    fig_name = company + "_SharePrice_to_NetProfitMargin.png"
    plt.savefig(fig_name)
    
    plt.show()
    print("Profit Margin Stock Correlation: ",profit_margin_to_stock_corr)

def calc_inventory_turnover(df):
    '''
    Function will calculate the inventory turnover (cost of goods sold / 
                                                    average inventory)
    
    Function will take in a dataframe
    
    Function will return nothing and just add a column to the dataframe
    '''
    # Creats a new column in the dataframe
    df['inventory_turnover'] = np.nan
    
    # Calculates the inventory turnover and sets it to its corresponding
    # location in the dataframe
    
    # Our denominator is usually an average with the previous quarter
    # So for the first quarter we are not taking an average
    df.loc[0, 'inventory_turnover'] = df.loc[0, 'cogsq'] / df.loc[0, 'invtq']
    for i in range(1, df.shape[0]):
        average_atq = (df.loc[i, 'invtq'] + df.loc[i-1, 'invtq']) / 2
        df.loc[i, 'inventory_turnover'] = df.loc[i, 'cogsq'] / average_atq
        
def graph_inventory_turnover_to_stock(df, company):
    '''
    Function will graph the stock price against inventory turnover
    
    Function will take in the main dataframe, company as a string
    
    Function will return nothing, just creates a plot
    '''
    
    # Makes the plot bigger
    plt.figure(figsize= (16,12))
    
    # Plots the points as a scatter plot
    plt.scatter(df['stock_price'], df['inventory_turnover'])
    
    # Calculates the slope and y-intercept of the line of best fit
    m, b = np.polyfit(df['stock_price'], df['inventory_turnover'], 1)
    
    # Plots the line of best fit
    plt.plot(df['stock_price'], m*df['stock_price'] + b, "--", color = "Red",
             label = "Line-of-Best-Fit")
    
    # Calculates the correlation of these two points
    inventory_turnover_to_stock_corr = calc_corr(df['stock_price'],
                                                 df['inventory_turnover'])

    fig_title = company + " Share Price vs. Inventory Turnover Ratio"
    plt.title(fig_title)
    x_label = "Share Price \n Correlation: " + \
        str(round(inventory_turnover_to_stock_corr, 5))
    plt.xlabel(x_label)
    plt.ylabel("Inventory Turnover")
    plt.legend()
    
    fig_name = company + "_SharePrice_to_InventoryTurnover.png"
    plt.savefig(fig_name)
    
    plt.show()
    print("Inventory Turnover Stock Correlation: ",
          inventory_turnover_to_stock_corr)



def calc_debt_to_equity(df):
    '''
    Function will calculate the debt to equity ratio (total liabilities /
                                                      shareholder equity)
    
    Function will take in a dataframe
    
    Function will return northing and just add a column to the dataframe
    '''
    # Creats a new column in the dataframe
    df['debt_to_equity'] = np.nan
    
    # Calculates the debt to equity ratio and sets it to its corresponding
    # location in the dataframe
    for i in range(0, df.shape[0]):
        df.loc[i, 'debt_to_equity'] = df.loc[i, 'ltq'] / df.loc[i, 'seqq']

def graph_debt_to_equity_to_stock(df, company):
    '''
    Function will graph the stock price against the debt to equity ratio
    
    Function will take in the main dataframe, company as a string
    
    Function will return nothing, just creates a plot
    '''
    
    # Makes the plot bigger
    plt.figure(figsize= (16,12))
    
    # Plots the points as a scatter plot
    plt.scatter(df['stock_price'], df['debt_to_equity'])
    
    # Calculaates the slope and y-intercept of the line of best fit
    m, b = np.polyfit(df['stock_price'], df['debt_to_equity'], 1)
    
    # Plots the line of best fit
    plt.plot(df['stock_price'], m*df['stock_price'] + b, "--", color = "Red",
             label = "Line-of-Best-Fit")
    
    # Calculates the correlation of these two points
    debt_to_equity_to_stock_corr = calc_corr(df['stock_price'],
                                             df['debt_to_equity'])
    
    fig_title = company + " Share Price vs. Debt to Equity Ratio"
    plt.title(fig_title)
    x_label = "Share Price \n Correlation: " + \
        str(round(debt_to_equity_to_stock_corr, 5))
    plt.xlabel(x_label)
    plt.ylabel("Debt to Equity Ratio")
    plt.legend()
    
    fig_name = company + "_SharePrice_to_DebtToEquity.png"
    plt.savefig(fig_name)
    
    plt.show()
    print("Debt to Equity Stock Correlation: ",debt_to_equity_to_stock_corr)
    
def calc_cf_capex(df):
    '''
    Function will calculate the cash flow to capital expenditure ratio
    (cf/capex)
    
    Function will take in a dataframe
    
    Function will return northing and just add a column to the dataframe
    '''
    # Creats a new column in the dataframe
    df['cf_capex'] = np.nan
    
    # Calculates the debt to equity ratio and sets it to its corresponding
    # location in the dataframe
    for i in range(0, df.shape[0]):
        cashflow_total = df.loc[i, 'oancfy'] + df.loc[i, 'ivncfy'] + \
            df.loc[i, 'fincfy']
        df.loc[i, 'cf_capex'] = cashflow_total / df.loc[i, 'capxy']
        
def graph_cf_capex_to_stock(df, company):
    '''
    Function will graph the stock price against the cf to capex ratio
    
    Function will take in the main dataframe, company as a string
    
    Function will return nothing, just creates a plot
    '''
    
    # Makes the plot bigger
    plt.figure(figsize= (16,12))
    
    # Plots the points as a scatter plot
    plt.scatter(df['stock_price'], df['cf_capex'])
    
    # Calculaates the slope and y-intercept of the line of best fit
    m, b = np.polyfit(df['stock_price'], df['cf_capex'], 1)
    
    # Plots the line of best fit
    plt.plot(df['stock_price'], m*df['stock_price'] + b, "--", color = "Red",
             label = "Line-of-Best-Fit")
    
    # Calculates the correlation of these two points
    cf_capex_to_stock_corr = calc_corr(df['stock_price'], df['cf_capex'])

    fig_title = company + " Share Price vs. Cash Flow to Capital Expenditures"
    plt.title(fig_title)
    x_label = "Share Price \n Correlation: " + \
        str(round(cf_capex_to_stock_corr, 5))
    plt.xlabel(x_label)
    plt.ylabel("Cash Flow to Capital Expenditures")
    plt.legend()
    
    fig_name = company + "_SharePrice_to_CFCapEX.png"
    plt.savefig(fig_name)
    
    plt.show()
    print("CF to CapEX Stock Correlation: ",cf_capex_to_stock_corr)
    
def graph_rnd_to_stock(df, company):
    '''
    Function will graph the stock price against the rnd expense
    
    Function will take in the main dataframe, company as a string
    
    Function will return nothing, just creates a plot
    '''
    
    # Makes the plot bigger
    plt.figure(figsize= (16,12))
    
    # Plots the points as a scatter plot
    plt.scatter(df['stock_price'], df['xrdq'])
    
    # Calculaates the slope and y-intercept of the line of best fit
    m, b = np.polyfit(df['stock_price'], df['xrdq'], 1)
    
    # Plots the line of best fit
    plt.plot(df['stock_price'], m*df['stock_price'] + b, "--", color = "Red",
             label = "Line-of-Best-Fit")
    
    # Calculates the correlation of these two points
    r_and_d_to_stock_corr = calc_corr(df['stock_price'], df['xrdq'])

    fig_title = company + " Share Price vs. Research and Development Expense"
    plt.title(fig_title)
    x_label = "Share Price \n Correlation: " + \
        str(round(r_and_d_to_stock_corr, 5))
    plt.xlabel(x_label)
    plt.ylabel("Research and Development Expense")
    plt.legend()
    
    fig_name = company + "_SharePrice_to_RND.png"
    
    plt.savefig(fig_name)
    
    plt.show()
    print("R&D Stock Correlation: ",r_and_d_to_stock_corr)
    
if __name__ == "__main__":
    
    # Creates our main dataframe
    aapl = read_csv(APPLE_FILE)
    googl = read_csv(GOOGLE_FILE)
    
    # Creates the stock price dataframe
    aapl_price_df = read_csv(APPLE_PRICE_FILE)
    googl_price_df = read_csv(GOOGLE_PRICE_FILE)
    
    
    # Converts the date and time from string to date types for Pandas to read
    aapl['datadate'] = pd.to_datetime(aapl['datadate'])
    googl['datadate'] = pd.to_datetime(googl['datadate'])
    # df for the last x quarters
    aapl_20 = df_slice(aapl, 20)
    googl_20 = df_slice(googl, 20)
    
    # Gets the colors based on quarter and adds it to the company specific
    # dataframe
    get_colors(aapl)
    get_colors(googl)
    
    # Gets the stock price at the end of each quarter and adds it to the
    # company specific dataframe
    get_stock_price(aapl, aapl_price_df)
    get_stock_price(googl, googl_price_df)
    # Calculates the current ratio and adds it to the respective dataframe
    calc_cur_ratio(aapl)
    calc_cur_ratio(googl)
    
    # Graphs the current ratio against the stock price and its line of best fit
    # Also prints the correlation between the data points
    graph_cur_ratio_to_stock(aapl, "Apple")
    graph_cur_ratio_to_stock(googl, "Google")

    # Calculates the roa ratio and adds it to the company's respective
    # dataframe
    calc_roa_ratio(aapl)
    calc_roa_ratio(googl)

    # Graphs the roa ratio against the stock price and its line of best fit
    # Also prints the correlation between the data points
    graph_roa_ratio_to_stock(aapl, "Apple")
    graph_roa_ratio_to_stock(googl, "Google")

    # Calculates the roe ratio and adds it to the company's respective
    # dataframe
    calc_roe_ratio(aapl)
    calc_roe_ratio(googl)
    
    # Graphs the roe ratio against the stock price and its line of best fit
    # Also prints the correlation between the data points
    graph_roe_ratio_to_stock(aapl, "Apple")
    graph_roe_ratio_to_stock(googl, "Google")

    # Calculates the net profit margin and adds it to the company's
    # respective dataframe
    calc_profit_margin(aapl)
    calc_profit_margin(googl)
    
    # Graphs the net profit margin against the stock price and its line of
    # best fit
    # Also prints the correlation between the data points
    graph_profit_margin_to_stock(aapl, "Apple")
    graph_profit_margin_to_stock(googl, "Google")

    # Calculates the inventory turnover and adds it to the respective dataframe
    calc_inventory_turnover(aapl)
    # Google has a 0 inventory during certain quarters so we're unable to
    # calculate the ratio because inventory is the denominator
    # calc_inventory_turnover(googl)
    
    
    # Graphs the inventory turnover against the stock price and its line of
    # best fit
    # Also prints the correlation between the data points
    graph_inventory_turnover_to_stock(aapl, "Apple")
    # graph_inventory_turnover_to_stock(googl, "Google")
    
    # Calculates the debt to equity ratio and adds it to the company's
    # respective dataframe
    calc_debt_to_equity(aapl)
    calc_debt_to_equity(googl)
    
    # Graphs the debt to equity ratio against the stock price and its line
    # of best fit
    # Also prints the correlation between the data points
    graph_debt_to_equity_to_stock(aapl, "Apple")
    graph_debt_to_equity_to_stock(googl, "Google")
    
    # Calculates the cf/capex ratio and adds it to the company's respective 
    # dataframe
    calc_cf_capex(aapl)
    calc_cf_capex(googl)
    
    # Graphs the cf to capex against the stock price and its line of best fit
    # Also prints the correlation between the data points
    graph_cf_capex_to_stock(aapl, "Apple")
    graph_cf_capex_to_stock(googl, "Google")
    
    # Graphs the r&d expense against the stock price and its line of best fit
    # Also prints the correlation between the data points
    graph_rnd_to_stock(aapl, "Apple")
    graph_rnd_to_stock(googl, "Google")