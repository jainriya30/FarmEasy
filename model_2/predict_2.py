from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
import pandas as pd

from os import path
from glob import glob

# The directory at which all the crop datasets are present
PRICE_DATASETS_DIR = 'crop_price_data'

# A class that represents a crop price prediction model
class CropPricePredictor:
    def __init__(self, csv_file_path):
        ## Load the dataset
        dataset = pd.read_csv(csv_file_path)

        ## Separate the columns of the dataset into X (params) and Y (result)

        # Get all the columns accept the result WPI
        self.X = dataset.iloc[:, :-1].values

        # Only get the last column
        self.Y = dataset.iloc[:, 3].values

        ## Split the dataset into train and test dataset
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(self.X, self.Y, test_size=0.1, random_state=0)

        ## Perform the required training using decision tree regressor
        self.regressor = DecisionTreeRegressor(max_depth=10, random_state=0)
        self.regressor.fit(self.X, self.Y)

# A dictionary that stores all the trained prediction models by their name
crop_price_predictors = {}

## Load the datasets

for dataset_path in glob(path.join(PRICE_DATASETS_DIR, '*')):
    crop_name = ''.join(path.basename(dataset_path).split('.')[:-1])
    try:
        crop_price_predictor = CropPricePredictor(dataset_path)
        crop_price_predictors[crop_name] = crop_price_predictor
    except BaseException as e:
        print(f"Unable to load dataset {dataset_path}...")
        print(e)

#print(crop_price_predictors)

for crop in crop_price_predictors:

    # Get the crop predictor
    crop_price_predictor = crop_price_predictors[crop]

    index = 0

    # Pick the first record/row from the test dataset as params
    record = crop_price_predictor.X_test[index]

    prediction = crop_price_predictor.regressor.predict([record])
    actual_value = crop_price_predictor.Y_test[index]
    
    print(f"Crop Name: {crop}")
    print(f"Test record: {record}")
    print(f"Prediction: {prediction}")
    print(f"Actual value: {actual_value}")
    print()
