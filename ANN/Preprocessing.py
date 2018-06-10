import csv, sys
from sys import argv
import pandas as pd
import numpy as np
#loading data
df = pd.read_csv(argv[1],header= None,sep='\s+|,\s+|,',engine='python')
length = len(df.columns) -1
#null values
df = df.dropna()

#drop duplicates
df = df.drop_duplicates()

#suffling data
df =  df.iloc[np.random.permutation(len(df))]

#removing rows which has impurities
for column in range(0,len(df.columns) - 1):
    if(df[column].dtype =='object'):
        to_drop = ['?']
        df_replaced = df[~df[column].isin(to_drop)]
        df1 = df_replaced

#Renaming output column label
df.rename(columns={length: 'Output'}, inplace=True)
OutputSet =  df.Output.unique()
#print len(OutputSet)

if (df['Output'].dtype != 'object'):
    #print "Yes"
    df['Output'] = np.where(df['Output'] > df['Output'].mean(), 1, 0)
#finding numerical columns
numeric_list = []
for column in range(0,len(df.columns) - 1):
    if(df[column].dtype != 'object'):
        numeric_list.append(column)

#normalising numeric columns
df[numeric_list] = df[numeric_list].apply(lambda x: (x - x.mean()) / (x.std()))

#converting categorical data into numeric
dfdum =  pd.get_dummies(df)

dataf = pd.DataFrame(data=dfdum)
#print dataf.describe()
dataf.to_csv(argv[2], sep=',',index= None)

#
#df1_suffled.to_csv('output.csv', sep=',')
