
# coding: utf-8

# In[8]:


## Import useful libraries

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as plt


# In[19]:


## Read in Data

blueDF = pd.read_csv('BlueBloodTiming.csv')
blueDF = blueDF.replace(np.nan, 0, regex=True)

blueDF.head()


# In[45]:


## Fix the ranking (0.0 means unranked)

blueDF['temp'] = blueDF['Rank'] + blueDF['Rank2']
blueDF['RANK'] = np.where(blueDF['temp'] > 0, blueDF['temp'], 0)
blueDF.head()


# In[63]:


## Get all the losses to unranked team

losses = blueDF[(blueDF['RANK'] < 1) & (blueDF['WL'] == 'L')]
losses.head()


# In[149]:


## Number of losses by game number to unranked teams

ax = sns.distplot(losses['Week'], hist=False);
ax.set_title('Distribution of Losses to Unranked Teams by Game Number')
ax.set_xlabel('Game Number')


# In[128]:


## Get the win percentage by game number

wins = [0] * 50
games = [0] * 50

for index, row in blueDF.iterrows():
    week = int(row['Week'])
    win = (row['WL'] == 'W')
    ind = week
    
    games[ind] += 1
    
    if win == True: 
        wins[ind] += 1

def getWeekWinPct(week):
    totalWins = wins[week]
    totalGames = games[week]
    
    return round(totalWins / totalGames, 2)


# In[155]:


## Plot win % by game number

weekWinPcts = []
week = []
for i in range(1, 32):
    if games[i] != 0:
        weekWinPcts.append(getWeekWinPct(i))
    else:
        weekWinPcts.append(0)
    
    week.append(i)
    
ax = sns.regplot(x=week, y=weekWinPcts);
ax.set_title('Distribution of Win % by Game Number')
ax.set_xlabel('Game Number')


# In[154]:


## Plot win % by game number specifically against unranked teams

wins = [0] * 50
games = [0] * 50

for index, row in blueDF.iterrows():
    week = int(row['Week'])
    win = (row['WL'] == 'W')
    ind = week
    unranked = (row['RANK'] == 0.0)
    
    if unranked: 
        games[ind] += 1
    
    if win & unranked: 
        wins[ind] += 1

def getWeekWinPct(week):
    totalWins = wins[week]
    totalGames = games[week]
    
    return round(totalWins / totalGames, 2)

weekWinPcts = []
week = []
for i in range(1, 32):
    if games[i] != 0:
        weekWinPcts.append(getWeekWinPct(i))
    else:
        weekWinPcts.append(0)
    
    week.append(i)
    
ax = sns.regplot(x=week, y=weekWinPcts);
ax.set_title('Distribution of Win % by Game Number - Unranked Opponents')
ax.set_xlabel('Game Number')


# In[147]:


## Find the difference in winning percentage against unranked teams early in season vs late in season

numGamesEarly = blueDF[(blueDF['Week'] <= 5) & blueDF['RANK'] == 0.0]
restOfGames = blueDF[(blueDF['Week'] > 5) & (blueDF['Week'] < 25) & (blueDF['RANK'] == 0.0)]

earlyLosses = numGamesEarly[(numGamesEarly['WL'] == 'L')]
otherLosses = restOfGames[(restOfGames['WL'] == 'L')]

earlyLosePct = round(len(earlyLosses) / len(numGamesEarly) * 100, 2)
print('Loss % in first 5 games: ', earlyLosePct, '%')

otherLosePct = round(len(otherLosses) / len(restOfGames) * 100, 2)
print('Loss % in rest of games: ', otherLosePct, '%')


# In[162]:


## Showing statistic significant of winning percentage difference using t-test

t1 = []
for each in restOfGames['WL']:
    if each == "W":
        t1.append(1)
    else:
        t1.append(0)

t2 = []
for EACH in numGamesEarly['WL']:
    if EACH == "W":
        t2.append(1)
    else:
        t2.append(0)
        
import scipy
from scipy.stats import ttest_ind, ttest_ind_from_stats
from scipy.special import stdtr

t, p = ttest_ind(t1, t2, equal_var=False)
round(p, 10)

