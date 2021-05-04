"""
This file converts CSV file to JSON file
"""
import pandas as pd
import os
import numpy as np
import csv
import glob
import statsmodels.api as sm

# Input CSV files
path = "C:/Users/timde/Documents/Quantitative Finance/Thesis/rawdatafiles"
mortgage_csv = "C:/Users/timde/Documents/Quantitative Finance/Thesis/controldata/mortgagerate.csv"
unemployment_csv = "C:/Users/timde/Documents/Quantitative Finance/Thesis/controldata/unemployment.csv"
population_csv = "C:/Users/timde/Documents/Quantitative Finance/Thesis/controldata/population_region.csv"
names_csv = "C:/Users/timde/Documents/Quantitative Finance/Thesis/controldata/names.csv"

mortgage_df = pd.read_csv(mortgage_csv, sep=';', usecols=['Periode ', 'Rente'])
unemployment_df = pd.read_csv(unemployment_csv, sep=';')
population_df = pd.read_csv(population_csv, sep=';')
names_df = pd.read_csv(names_csv, sep=',', header=None)
all_files = glob.glob(os.path.join(path, "*.csv"))

# try_csv = "C:/Users/timde/Documents/Quantitative Finance/Thesis/controldata/tryframe.csv"
# try_df = pd.read_csv(try_csv, sep=';')

# Create frame
li = []
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, sep=';', header=[1,2])

    # Append region to dataframe to index on region and quarter
    s1 = str(filename)
    s2 = "C:/Users/timde/Documents/Quantitative Finance/Thesis/rawdatafiles"
    region = s1[s1.index(s2) + len(s2):]
    region = region.replace(".csv","")
    region = region.replace("\\", "")
    df['Region'] = region
    li.append(df)

# Create one dataframe
frame = pd.concat(li, axis=0, ignore_index=False)

# Rename each header
frame.columns = ['Year-Quarter', 'Zuiver kwartaal', 'Voortschrijdend kwartaal', 'Year_Index', 'Zuiver Kwartaal NL', 'Voortschrijdend kwartaal NL', 'Year_Index_NL', 'Region']
names_df.columns = ['Province', 'Region']
frame['Province'] = frame['Region'].map(names_df.set_index('Region')['Province'])
# frame = frame.set_index(['Region', 'Year-Quarter'])
# frame.to_excel("output2.xlsx", sheet_name='df')
# print(frame.loc['Het Gooi'])
# print(frame)

# Mortgage rate
mortgage_df.columns = ['Year-Quarter', 'Rente']
mortgage_df = mortgage_df.set_index('Year-Quarter')
mortgage_df = mortgage_df.groupby(pd.PeriodIndex(mortgage_df.index, freq='Q'), axis=0).mean()
mortgage_df.index = mortgage_df.index.strftime('%y-%q')
# print(mortgage_df)

# Unemployment
unemployment_df.columns = ['Year-Quarter', 'Unemployment']
unemployment_df = unemployment_df.iloc[11:-4]
unemployment_df = unemployment_df.set_index('Year-Quarter')
unemployment_df.index = pd.to_datetime(unemployment_df.index)
unemployment_df.index = unemployment_df.index.to_period("Q")
unemployment_df.index = unemployment_df.index.strftime('%y-%q')
# print(unemployment_df)

# Population
population_df = population_df.rename(columns={'TIME': 'Year-Quarter', 'Friesland (NL)': 'Friesland', 'Limburg (NL)': 'Limburg'})
population_df = population_df.iloc[20:120]
population_df = population_df.set_index(['Year-Quarter'])
population_df.index = pd.to_datetime(population_df.index, format='%Y')
population_df.index = population_df.index.to_period("Q")
population_df.index = population_df.index.strftime('%y-%q')
population_df = population_df.reset_index()
print(population_df)



# frame = frame.merge(unemployment_df, left_index=True, right_index=True, sort=True)
# result = result.sort_index()
# result = result.reset_index()
# result = result.set_index(['Region', 'Year-Quarter'])
# result = result.sort_index()

# result = frame.join(unemployment_df)


# frame['Population'] = frame['Region'].map(population_df[i])



# df['points'] = np.where( ( (df['gender'] == 'male') & (df['pet1'] == df['pet2'] ) ) | ( (df['gender'] == 'female') & (df['pet1'].isin(['cat','dog'] ) ) ), 5, 0)



# for column, row in frame.iteritems():
#     for column_pop, row_pop in population_df.iteritems():
#         if column['Province'] == column_pop & row['Year_Quarter'] == row_pop['Year_Quarter']:
#             frame['Population'] = population_df[column_pop][row_pop]
print(type(frame['Year-Quarter']))
