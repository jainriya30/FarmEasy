import pandas as pd

state_wise_data = pd.read_csv('state_wise_crop_production.csv')

ll_data = state_wise_data[state_wise_data["District_Name"] == "leh ladakh"]
ll_free_data = state_wise_data[state_wise_data["District_Name"] != "leh ladakh"]

ll_data["State_Name"] = "ladakh"

state_wise_data = pd.concat([ll_free_data, ll_data])

state_wise_data.to_csv("test.csv")

# print(state_wise_data[state_wise_data["District_Name"] == "leh ladakh"])

# state_wise_data = state_wise_data.applymap(lambda x: "uttaranchal" if x == "uttarakhand" else x)

# state_wise_data.to_csv("state_wise_crop_production.csv")