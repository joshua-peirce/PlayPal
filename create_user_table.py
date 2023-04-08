# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 16:46:47 2023

@author: tijana
"""

# imports the necessary libraries/packages
import pandas as pd
import random
import string

# creates a new df with the UserID and Password columns - sets the IDs to
# be numbered in ascending order from 1 to len(df_users); initially sets the
# Password column to 'password' in order to create the 1000 rows
df_users = pd.DataFrame({'user_id': range(1, 1001),
                         'password': ['password'] * 1000})
      
# loops through all of the rows in the df and generates a random, unique,
# 8-character password that we replace the 'password' string placeholder
# with
for index, row in df_users.iterrows():
    if row['password'] == 'password':
        password = ''.join(random.choices(string.ascii_letters + string.digits,
                                          k = 8))
        df_users.at[index, 'password'] = password

# saves the df to a CSV file
df_users.to_csv('user_table.csv', index=False)
