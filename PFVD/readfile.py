import pandas as pd
from pandas import read_csv
import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
import plotly.express as px

# Read the CSV file
paris_men_attackers = pd.read_csv("datasets/Olympics-paris-men/olympics_paris_men_attackers.txt")
# Get a list of all CSV files in a directory
csv_files = glob.glob('datasets/Olympics-paris-men/*.txt')

# Create an empty dataframe to store the combined data
df_paris_men = paris_men_attackers[["Player-Name","Team"]].copy()

# Loop through each CSV file and append its contents to the combined dataframe
for csv_file in csv_files:
    df = pd.read_csv(csv_file)
    df = df.drop(columns=['Team']) # For error prevention in merge
    df_paris_men = pd.merge(df, df_paris_men, on='Player-Name', suffixes=("","")).fillna(0)

# Create the teams_men DataFrame with total matches
df_temp = df_paris_men.drop_duplicates(['Team'])
teams_men = pd.DataFrame({
    "Team": df_temp["Team"],
    "total-matches": [4, 6, 6, 4, 6, 6, 4, 3, 4, 3, 3, 3]  # datas from https://en.volleyballworld.com/volleyball/competitions/volleyball-olympic-games-paris-2024/schedule/#fromDate=2024-08-10
})

# Merge df_paris_men with teams_men to add total-matches
df_paris_men = pd.merge(df_paris_men, teams_men, on='Team', suffixes=("", "")).fillna(0)

# Normalize the data per total-match from each player
df_paris_men[['Rank-setter', 'Successful-setter', 'Errors-setter',
       'Attempts-setter', 'Total-setter', 'Rank-server', 'serve-points', 'Errors-serve',
       'Attemps-serve', 'Total-serve', 'Rank-scores', 'Points', 'Attack-Points', 'Block-Points',
       'Serve-Points', 'Rank-receiver', 'Succesful-receive', 'Errors-receive',
       'Attemps-receive', 'Total-receive', 'Rank-digger',
       'Successful-dig', 'Errors-dig', 'Receptions-dig',
       'Total-dig', 'Rank-blocker', 'Succesful-blocks', 'Errors-block', 'Rebounds-block',
       'Total-block','Rank-attacker', 'Points-attacks', 'Errors-attack',
       'Attempts-shots-attack', 'Total-attack']] = df_paris_men[['Rank-setter', 'Successful-setter', 'Errors-setter',
       'Attempts-setter', 'Total-setter', 'Rank-server', 'serve-points', 'Errors-serve',
       'Attemps-serve', 'Total-serve', 'Rank-scores', 'Points', 'Attack-Points', 'Block-Points',
       'Serve-Points', 'Rank-receiver', 'Succesful-receive', 'Errors-receive',
       'Attemps-receive', 'Total-receive', 'Rank-digger',
       'Successful-dig', 'Errors-dig', 'Receptions-dig',
       'Total-dig', 'Rank-blocker', 'Succesful-blocks', 'Errors-block', 'Rebounds-block',
       'Total-block','Rank-attacker', 'Points-attacks', 'Errors-attack',
       'Attempts-shots-attack', 'Total-attack']].div(df_paris_men["total-matches"], axis=0)

# Read the CSV file
paris_women_attackers = pd.read_csv("datasets/Olympics-paris-women/olympics_paris_women_attackers.txt")
# Get a list of all CSV files in a directory
csv_files = glob.glob('datasets/Olympics-paris-women/*.txt')

# Create an empty dataframe to store the combined data
df_paris_women = paris_women_attackers[["Player-Name","Team"]].copy()

# Loop through each CSV file and append its contents to the combined dataframe
for csv_file in csv_files:
    df = pd.read_csv(csv_file)
    df = df.drop(columns=['Team']) # For error prevention in merge
    df_paris_women = pd.merge(df, df_paris_women, on='Player-Name', suffixes=("","")).fillna(0)

# Create the teams_men DataFrame with total matches
df_temp = df_paris_women.drop_duplicates(['Team'])

teams_women = pd.DataFrame({
    "Team": df_temp["Team"],
    "total-matches": [6, 4, 6, 6, 6, 4, 4, 4, 5, 3, 3, 3]  # datas from https://en.volleyballworld.com/volleyball/competitions/volleyball-olympic-games-paris-2024/schedule/#fromDate=2024-08-10
})

# Merge df_paris_women with teams_women to add total-matches
df_paris_women = pd.merge(df_paris_women, teams_women, on='Team', suffixes=("", "")).fillna(0)

# Normalize the data per total-match from each player
df_paris_women[['Rank-setter', 'Successful-setter', 'Errors-setter',
       'Attempts-setter', 'Total-setter', 'Rank-server', 'serve-points', 'Errors-serve',
       'Attemps-serve', 'Total-serve', 'Rank-scores', 'Points', 'Attack-Points', 'Block-Points',
       'Serve-Points', 'Rank-receiver', 'Succesful-receive', 'Errors-receive',
       'Attemps-receive', 'Total-receive', 'Rank-digger',
       'Successful-dig', 'Errors-dig', 'Receptions-dig',
       'Total-dig', 'Rank-blocker', 'Succesful-blocks', 'Errors-block', 'Rebounds-block',
       'Total-block','Rank-attacker', 'Points-attacks', 'Errors-attack',
       'Attempts-shots-attack', 'Total-attack']] = df_paris_women[['Rank-setter', 'Successful-setter', 'Errors-setter',
       'Attempts-setter', 'Total-setter', 'Rank-server', 'serve-points', 'Errors-serve',
       'Attemps-serve', 'Total-serve', 'Rank-scores', 'Points', 'Attack-Points', 'Block-Points',
       'Serve-Points', 'Rank-receiver', 'Succesful-receive', 'Errors-receive',
       'Attemps-receive', 'Total-receive', 'Rank-digger',
       'Successful-dig', 'Errors-dig', 'Receptions-dig',
       'Total-dig', 'Rank-blocker', 'Succesful-blocks', 'Errors-block', 'Rebounds-block',
       'Total-block','Rank-attacker', 'Points-attacks', 'Errors-attack',
       'Attempts-shots-attack', 'Total-attack']].div(df_paris_women["total-matches"], axis=0)

# Concatenating the dataframes
df_paris_geral = pd.concat([df_paris_men, df_paris_women], ignore_index=True)
