import pandas as pd

df = pd.read_csv("crop_production.csv")

states = set(df["State_Name"])
print(states)
print(len(states))