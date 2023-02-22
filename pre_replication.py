# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 13:48:02 2023

@author: GESSLOCAL
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


#%% Creating a fake dataset
stereotype_factor = 2 # how the beliefs diverge from the actual performance difference, 100% correspnds to 2
Demographics=['Race','Age','Gender','State','Education']

listOfQuestions=[
    'NV_task',
    'Maze_task',
    'Count_letters_task',
    'Word_puzzle_task',
    'Word_order_task',
    'Count_numbers_task',
    'Ball_bucket_task',
    'Word_in_word_task',
    'Numbers_in_numbers_task',
    'MRT_task'    
    ]

true_difference_list={
    'NV_task': 0.05,
    'Maze_task': 0.11,
    'Count_letters_task': -0.07,
    'Word_puzzle_task':0,
    'Word_order_task':0.12,
    'Count_numbers_task':0,
    'Ball_bucket_task':0,
    'Word_in_word_task':0,
    'Numbers_in_numbers_task':0,
    'MRT_task':0.15
}

df=pd.DataFrame(index=range(500),columns=range(15))
df.columns = Demographics+listOfQuestions

for task in true_difference_list:
    df[task]= np.random.normal(stereotype_factor*true_difference_list[task], 1, 500) 
    
df['Age'] = np.random.normal(50, 6, 500)
df['Gender'] = np.random.binomial(1,0.5, 500)
df['State'] = np.random.uniform(1, 50, 500).round()
df['Race'] = np.random.uniform(1, 5, 500).round()
df['Education'] = np.random.uniform(1, 50, 500).round()


margun_beliefs={
    'NV_task': 0.30,
    'Maze_task': 0.28,
    'Count_letters_task': 0,
    'Word_puzzle_task':-.11,
    'Word_order_task':-0.075,
    'Count_numbers_task':0,
    'Ball_bucket_task':0.25,
    'Word_in_word_task':-0.20,
    'Numbers_in_numbers_task':0.32,
    'MRT_task':0.45
}

df_margun=df


for task in margun_beliefs:
    df_margun[task]= np.random.normal(margun_beliefs[task], 1, 500) 
    


#%% Data analysis (incomplete)

competition_gap_values={
    'NV_task': 0.38 ,
    'Maze_task': 0.126 ,
    'Count_letters_task': 0.127,
    'Word_puzzle_task':0.058,
    'Word_order_task':0.094,
    'Count_numbers_task':0.14,
    'Ball_bucket_task':0.36,
    'Word_in_word_task':0.09,
    'Numbers_in_numbers_task':0.25,
    'MRT_task':0.115   
    }

x = df.mean()[5:].tolist()
y = list(competition_gap_values.values())

fig, ax = plt.subplots()
ax.plot(x, y, 'bo')
plt.show()

x_1=np.array(x).reshape((-1, 1))
y=np.array(y)
model = LinearRegression().fit(x_1, y)

r_sq = model.score(x_1, y)
print(f"coefficient of determination: {r_sq}")
r = np.corrcoef(x, y)
print(r)

