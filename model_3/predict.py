import pandas as pd

# TODO: Add some calculated threshold value/percent below which 

# Enable to avoid querying the same data multiple times for multiple requests
# (Could be disabled for data that can be updated live etc.)
ENABLE_CACHE = False

# The path to the dataset this program is considering
STATEWISE_CROP_DATA_CSV_PATH = "test.csv"

# These constants have been calculated from the static dataset
STATES = ['Andaman And Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Dadra And Nagar Haveli', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu And Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']
CROPS = ['Apple', 'Arcanut (Processed)', 'Arecanut', 'Arhar/Tur', 'Ash Gourd', 'Atcanut (Raw)', 'Bajra', 'Banana', 'Barley', 'Bean', 'Beans & Mutter(Vegetable)', 'Beet Root', 'Ber', 'Bhindi', 'Bitter Gourd', 'Black Pepper', 'Blackgram', 'Bottle Gourd', 'Brinjal', 'Cabbage', 'Cardamom', 'Carrot', 'Cashewnut', 'Cashewnut Processed', 'Cashewnut Raw', 'Castor Seed', 'Cauliflower', 'Citrus Fruit', 'Coconut ', 'Coffee', 'Colocosia', 'Cond-Spcs Other', 'Coriander', 'Cotton(Lint)', 'Cowpea(Lobia)', 'Cucumber', 'Drum Stick', 'Dry Chillies', 'Dry Ginger', 'Garlic', 'Ginger', 'Gram', 'Grapes', 'Groundnut', 'Guar Seed', 'Horse-Gram', 'Jack Fruit', 'Jobster', 'Jowar', 'Jute', 'Jute & Mesta', 'Kapas', 'Khesari', 'Korra', 'Lab-Lab', 'Lemon', 'Lentil', 'Linseed', 'Litchi', 'Maize', 'Mango', 'Masoor', 'Mesta', 'Moong(Green Gram)', 'Moth', 'Niger Seed', 'Oilseeds Total', 'Onion', 'Orange', 'Other  Rabi Pulses', 'Other Cereals & Millets', 'Other Citrus Fruit', 'Other Dry Fruit', 'Other Fibres', 'Other Fresh Fruits', 'Other Kharif Pulses', 'Other Misc. Pulses', 'Other Oilseeds', 'Other Vegetables', 'Paddy', 'Papaya', 'Peach', 'Pear', 'Peas  (Vegetable)', 'Peas & Beans (Pulses)', 'Perilla', 'Pineapple', 'Plums', 'Pome Fruit', 'Pome Granet', 'Potato', 'Pulses Total', 'Pump Kin', 'Ragi', 'Rajmash Kholar', 'Rapeseed &Mustard', 'Redish', 'Ribed Guard', 'Rice', 'Ricebean (Nagadal)', 'Rubber', 'Safflower', 'Samai', 'Sannhamp', 'Sapota', 'Sesamum', 'Small Millets', 'Snak Guard', 'Soyabean', 'Sugarcane', 'Sunflower', 'Sweet Potato', 'Tapioca', 'Tea', 'Tobacco', 'Tomato', 'Total Foodgrain', 'Turmeric', 'Turnip', 'Urad', 'Varagu', 'Water Melon', 'Wheat', 'Yam']

# Name of the columns that are being queried from the CSV file as constants
STATE_COLUMN_NAME = "State_Name"
CROP_COLUMN_NAME = "Crop"
YIELD_COLUMN_NAME = "Production"

# Loading the state wise crop dataset
df = pd.read_csv(STATEWISE_CROP_DATA_CSV_PATH)

# Caching filtered and sorted results for both the functions
TOP_CROPS_FOR_STATE_CACHE = {}
TOP_STATES_FOR_CROP_CACHE = {}

class CropNotFoundException(Exception): pass
class StateNotFoundException(Exception): pass

def top_crops_for_state(state):
    if ENABLE_CACHE:
        try:
            if state not in TOP_CROPS_FOR_STATE_CACHE:
                TOP_CROPS_FOR_STATE_CACHE[state] = _top_crops_for_state(state)
        
            return TOP_CROPS_FOR_STATE_CACHE[state]
        except KeyError:
            raise StateNotFoundException

    return _top_crops_for_state(state)

# Retrieve top
def top_states_for_crop(crop):
    if ENABLE_CACHE:
        try:
            if crop not in TOP_STATES_FOR_CROP_CACHE:
                TOP_STATES_FOR_CROP_CACHE[crop] = _top_states_for_crop(crop)

            return TOP_STATES_FOR_CROP_CACHE[crop]
        
        except KeyError:
            raise CropNotFoundException

    return _top_states_for_crop(crop)


# Raw functions that do not perform any caching
def _top_crops_for_state(state):
    data = df[df[STATE_COLUMN_NAME]==state.lower()].sort_values(by=YIELD_COLUMN_NAME, ascending=False)
    res = dict()
    for row in data.iterrows():
        row = row[1]
        dn = row["Crop"]
        if dn not in res:
            res[dn] = row
            if len(res) == 5: break
    
    return pd.DataFrame(res.values())  

def _top_states_for_crop(crop):
    data = df[df[CROP_COLUMN_NAME]==crop.lower()].sort_values(by=YIELD_COLUMN_NAME, ascending=False)    
    res = dict()
    for row in data.iterrows():
        row = row[1]
        dn = row["State_Name"]
        if dn not in res:
            res[dn] = row
            if len(res) == 5: break
    
    return pd.DataFrame(res.values())

# print(len(STATES))

# print(list(sorted(map(lambda x:x.title(), set(df[CROP_COLUMN_NAME])))))

# print(list(sorted(map(lambda s: s.title(), STATES))))

#print(top_crops_for_state('karnatAka'))
# print(top_crops_for_state('Karnataka'))

# for column in ["State_Name","District_Name","Season","Crop"]: df[column] = list(map(lambda x: x.lower(), df[column]))
# df.to_csv("test.csv")

#print(top_states_for_crop('SUGARCANE'))
# print(top_states_for_crop('GRAM'))

# data = df[df[CROP_COLUMN_NAME]==crop].sort_values(by=YIELD_COLUMN_NAME, ascending=False)
# print(123)