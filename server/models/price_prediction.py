from os import path
from threading import Thread
import pandas as pd
from time import sleep
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from .weather_data import WeatherForecaster
from dateutil.relativedelta import relativedelta
import datetime
import pickle

from .constants import PRICE_DATASETS_DIR_PATH, PRE_TRAINED_MODELS_DIR_PATH

weather_forecaster = WeatherForecaster()

class PricePredictionModelManager:

    ALL_CROPS = ['arhar', 'bajra', 'barley', 'copra', 'cotton', 'gram', 'groundnut', 'jowar', 'jute', 'maize', 'masoor', 'moong', 'niger', 'paddy', 'ragi', 'safflower', 'sesamum', 'soyabean', 'sugarcane', 'sunflower', 'urad', 'wheat']

    def __init__(self, pretrain=True, pretrain_parallel=True):
        self.prediction_models = {}

        # Prefill the 
        if pretrain:
            if pretrain_parallel:
                Thread(target=self.get_stats_for_current_month).start()
            else:
                self.get_stats_for_current_month()
    
    # Returns the price_data of each crop as a list of tuples [(crop_name, current_month, next_month), ...]
    # sorted by the current month's prices
    def get_stats_for_current_month(self, lat=WeatherForecaster.DEFAULT_LAT, lng=WeatherForecaster.DEFAULT_LNG):

        price_data_list = []

        for crop in PricePredictionModelManager.ALL_CROPS: 
            model = self.get_model_for_crop(crop)
            price_data = model.predict_prices_for_next_n_months(2)
            current_month_price, next_month_price = price_data.values()
            price_data_list.append((crop, current_month_price, next_month_price))

        price_data_list.sort(key= lambda price_data: -price_data[1])

        return price_data_list

    def get_model_for_crop(self, crop):
        if crop in self.prediction_models:
            return self.prediction_models[crop]
        else:
            model = PricePredictonModel(crop)
            self.prediction_models[crop] = model
            return model
    
    def predict_price_for(self, crop, year, month, rainfall):
        model = self.get_model_for_crop(crop)
        return model.predict(year, month, rainfall)
    
    def predict_price_for_current_month(self, crop):
        model = self.get_model_for_crop(crop)
        return model.predict_price_for_current_month()
    
    def predict_price_for_last_month(self, crop):
        model = self.get_model_for_crop(crop)
        return model.predict_price_for_last_month()

    def predict_prices_for_next_n_months(self, crop, n):
        model = self.get_model_for_crop(crop)
        return model.predict_prices_for_next_n_months(n)
    
    def predict_prices_for_next_8_months(self, crop):
        model = self.get_model_for_crop(crop)
        return model.predict_prices_for_next_n_months(8)

# Represent a price prediction model
class PricePredictonModel:

    ENSURE_TRAINED_CHECK_INTERVAL = 1
    PRICE_DATASETS_DIR_PATH = PRICE_DATASETS_DIR_PATH

    def __init__(self, crop, train_parallel=True):
        # A flag that let's the prediction methods know whether the model is trained or not
        self.is_trained = False
        self._crop = crop.strip().lower()

        if train_parallel:
            # Start training the model on a separate thread
            Thread(target=self._train_model).start()            
        else:
            # Train the model on the same thread to avoid delays while calling
            # the recommendation methods
            self._train_model()

    # Waits for the model to be trained
    # (Flask requests are handled in concurrent threads, so it wouldn't block the server
    # as a whole while being trained)
    # self._train_model 
    def ensure_trained(self):
        while not self.is_trained: sleep(self.ENSURE_TRAINED_CHECK_INTERVAL)

    # Trains the model and sets the predictor object on self for the recommendation methods
    def _train_model(self):

        # Path to the cache file model to be created/loaded
        cache_model_path = path.join(PRE_TRAINED_MODELS_DIR_PATH, self._crop)  

        # Load the cached model if it is present
        if path.isfile(cache_model_path):
            with open(cache_model_path, "rb") as cache_model_file:
                model = pickle.load(cache_model_file)
                self.regressor = model.regressor
                self.df_columns = model.df_columns
                self.is_trained = True
                return
        

        crop_dataset_path = path.join(self.PRICE_DATASETS_DIR_PATH, f"{self._crop}.csv")

        if not path.isfile(crop_dataset_path):
            raise PriceDatasetNotFoundException

        ## Load the dataset
        dataset = None

        try:
            dataset = pd.read_csv(crop_dataset_path)
        except:
            raise PriceDatasetFormatInvalidException
        
        ## Separate the columns of the dataset into X (params) and Y (result)

        # Get all the columns except the result WPI
        X = dataset.drop('WPI', axis = 1)

        self.df_columns = X.columns

        # Only get the last column
        Y = dataset['WPI']

        ## Split the dataset into train and test dataset
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1, random_state=0)

        ## Perform the required training using decision tree regressor
        regressor = DecisionTreeRegressor(max_depth=10, random_state=0)
        regressor.fit(X, Y)

        # Setting the predictor as the recommender's main predictor
        self.regressor = regressor

        # Setting the flag to indicate that the model has been trained
        self.is_trained = True

        # Save the trained model in cache
        with open(cache_model_path, "wb") as file:
            pickle.dump(self, file=file, protocol=pickle.HIGHEST_PROTOCOL)

    # Performs an direct prediction query to the ML model
    def raw_predict(self, year, month, rainfall):
        self.ensure_trained()
        return self.regressor.predict(pd.DataFrame([[month, year, rainfall]], columns=self.df_columns))[0]
    
    # Predicts the possible prices for the given year and month based on their location
    def predict_price(self, year, month, lat=WeatherForecaster.DEFAULT_LAT, lng=WeatherForecaster.DEFAULT_LNG):
        self.ensure_trained()
        rainfall = weather_forecaster.get_rainfall_for_month(year, month, lat, lng)
        return self.regressor.predict(pd.DataFrame([[month, year, rainfall]], columns=self.df_columns))[0]
    
    # Predict the prices for the current month
    def predict_price_for_current_month(self, lat=WeatherForecaster.DEFAULT_LAT, lng=WeatherForecaster.DEFAULT_LNG):
        today = datetime.date.today()
        return self.predict_price(today.year, today.month, lat, lng)    

    def predict_price_for_last_month(self, lat=WeatherForecaster.DEFAULT_LAT, lng=WeatherForecaster.DEFAULT_LNG):
        last_month_date = datetime.date.today() - relativedelta(months=1)
        return self.predict_price(last_month_date.year, last_month_date.month, lat, lng)    

    def predict_prices_for_next_n_months(self, n, lat=WeatherForecaster.DEFAULT_LAT, lng=WeatherForecaster.DEFAULT_LNG):
        self.ensure_trained()

        rainfall_data = weather_forecaster.get_rainfall_for_next_n_months(n, lat, lng)

        result = {}

        for year, month in rainfall_data:
            rainfall = rainfall_data[(year, month)]
            result[(year, month)] = self.raw_predict(year, month, rainfall)

        return result

class PriceDatasetNotFoundException(Exception): pass
class PriceDatasetFormatInvalidException(Exception): pass    
