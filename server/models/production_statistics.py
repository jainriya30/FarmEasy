import pandas as pd
from os import path

from threading import Thread
from .constants import DATASETS_DIR_PATH

from time import sleep

class CropNotFoundException(Exception): pass
class StateNotFoundException(Exception): pass

class ProductionStatsModel:

    # Enable to avoid querying the same data multiple times for multiple requests
    # (Could be disabled for data that can be updated live etc.)
    ENABLE_CACHE = True

    # Details to the production dataset
    PRODUCTION_DATASET_FILE = 'state_wise_crop_production.csv'
    PRODUCTION_DATASET_PATH = path.join(DATASETS_DIR_PATH, PRODUCTION_DATASET_FILE)

    # These constants have been calculated from the static dataset
    STATES = ['Andaman And Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Dadra And Nagar Haveli', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu And Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Orissa', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttaranchal', 'West Bengal', 'Ladakh']
    CROPS = ['Apple', 'Arcanut (Processed)', 'Arecanut', 'Arhar/Tur', 'Ash Gourd', 'Atcanut (Raw)', 'Bajra', 'Banana', 'Barley', 'Bean', 'Beans & Mutter(Vegetable)', 'Beet Root', 'Ber', 'Bhindi', 'Bitter Gourd', 'Black Pepper', 'Blackgram', 'Bottle Gourd', 'Brinjal', 'Cabbage', 'Cardamom', 'Carrot', 'Cashewnut', 'Cashewnut Processed', 'Cashewnut Raw', 'Castor Seed', 'Cauliflower', 'Citrus Fruit', 'Coconut', 'Coffee', 'Colocosia', 'Cond-Spcs Other', 'Coriander', 'Cotton(Lint)', 'Cowpea(Lobia)', 'Cucumber', 'Drum Stick', 'Dry Chillies', 'Dry Ginger', 'Garlic', 'Ginger', 'Gram', 'Grapes', 'Groundnut', 'Guar Seed', 'Horse-Gram', 'Jack Fruit', 'Jobster', 'Jowar', 'Jute', 'Jute & Mesta', 'Kapas', 'Khesari', 'Korra', 'Lab-Lab', 'Lemon', 'Lentil', 'Linseed', 'Litchi', 'Maize', 'Mango', 'Masoor', 'Mesta', 'Moong(Green Gram)', 'Moth', 'Niger Seed', 'Oilseeds Total', 'Onion', 'Orange', 'Other  Rabi Pulses', 'Other Cereals & Millets', 'Other Citrus Fruit', 'Other Dry Fruit', 'Other Fibres', 'Other Fresh Fruits', 'Other Kharif Pulses', 'Other Misc. Pulses', 'Other Oilseeds', 'Other Vegetables', 'Paddy', 'Papaya', 'Peach', 'Pear', 'Peas  (Vegetable)', 'Peas & Beans (Pulses)', 'Perilla', 'Pineapple', 'Plums', 'Pome Fruit', 'Pome Granet', 'Potato', 'Pulses Total', 'Pump Kin', 'Ragi', 'Rajmash Kholar', 'Rapeseed &Mustard', 'Redish', 'Ribed Guard', 'Rice', 'Ricebean (Nagadal)', 'Rubber', 'Safflower', 'Samai', 'Sannhamp', 'Sapota', 'Sesamum', 'Small Millets', 'Snak Guard', 'Soyabean', 'Sugarcane', 'Sunflower', 'Sweet Potato', 'Tapioca', 'Tea', 'Tobacco', 'Tomato', 'Total Foodgrain', 'Turmeric', 'Turnip', 'Urad', 'Varagu', 'Water Melon', 'Wheat', 'Yam']

    # A mapping to fix new states that aren't present in the static dataset
    NEW_STATES_MAPPING = {
        "Ladakh": "Jammu and Kashmir",
        "Telangana": "Andhra Pradesh",
    }

    MAX_CROPS_FOR_STATE = 5
    MAX_STATES_FOR_CROP = 5

    # Name of the columns that are being queried from the CSV file as constants
    STATE_COLUMN_NAME = "State_Name"
    CROP_COLUMN_NAME = "Crop"
    YIELD_COLUMN_NAME = "Production"

    def __init__(self) -> None:
        self.dataset = pd.read_csv(self.PRODUCTION_DATASET_PATH)

        # Caching filtered and sorted results for both query functions
        self.TOP_CROPS_FOR_STATE_CACHE = {}
        self.TOP_STATES_FOR_CROP_CACHE = {}

        # Pre-fills cache in background
        self.prefill_cache_in_background()
    
    def prefill_cache_in_background(self):
        Thread(target=self.top_crops_for_all_states).start()
        Thread(target=self.top_states_for_all_crops).start()

    def top_crops_for_all_states(self):
        res = dict()
        for state in ProductionStatsModel.STATES: res[state] = self.top_crops_for_state(state)
        # print(res["Jammu And Kashmir"])
        return res

    def top_states_for_all_crops(self):
        res = dict()
        for crop in ProductionStatsModel.CROPS: res[crop] = self.top_states_for_crop(crop)
        return res

    def top_crops_for_state(self, state):
        if ProductionStatsModel.ENABLE_CACHE:
            try:
                if state not in self.TOP_CROPS_FOR_STATE_CACHE:
                    self.TOP_CROPS_FOR_STATE_CACHE[state] = self._top_crops_for_state(state)
            
                return self.TOP_CROPS_FOR_STATE_CACHE[state]
            except KeyError:
                raise StateNotFoundException

        return self._top_crops_for_state(state)

    # Retrieve top
    def top_states_for_crop(self, crop):
        if ProductionStatsModel.ENABLE_CACHE:
            try:
                if crop not in self.TOP_STATES_FOR_CROP_CACHE:
                    self.TOP_STATES_FOR_CROP_CACHE[crop] = self._top_states_for_crop(crop)

                return self.TOP_STATES_FOR_CROP_CACHE[crop]
            
            except KeyError:
                raise CropNotFoundException

        return self._top_states_for_crop(crop)
    
    @classmethod
    def new_state_names_fix(cls, state):        
        if state in ProductionStatsModel.NEW_STATES_MAPPING:
            return ProductionStatsModel.NEW_STATES_MAPPING[state]
        return state
        

    # Raw functions that do not perform any caching
    def _top_crops_for_state(self, state):
        #state = ProductionStatsModel.new_state_names_fix(state)
        data = self.dataset[self.dataset[ProductionStatsModel.STATE_COLUMN_NAME]==state.lower()].sort_values(by=ProductionStatsModel.YIELD_COLUMN_NAME, ascending=False)
        res = []
        for row in data.iterrows():
            row = row[1]
            dn = row["Crop"]
            if dn not in res:
                res.append(dn)
                if len(res) == ProductionStatsModel.MAX_CROPS_FOR_STATE: break
        
        # Raise not found exception is empty
        if not res: raise StateNotFoundException

        return res

    def _top_states_for_crop(self, crop):
        data = self.dataset[self.dataset[ProductionStatsModel.CROP_COLUMN_NAME]==crop.lower()].sort_values(by=ProductionStatsModel.YIELD_COLUMN_NAME, ascending=False)
        res = []
        for row in data.iterrows():
            row = row[1]
            dn = row["State_Name"]
            if dn not in res:
                res.append(dn)
                if len(res) == ProductionStatsModel.MAX_STATES_FOR_CROP: break
        
        if not res: raise CropNotFoundException

        return res