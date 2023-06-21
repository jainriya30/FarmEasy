from os import path
from threading import Thread
import pandas as pd
from time import sleep
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from .constants import DATASETS_DIR_PATH

class CropRecommendationModel:    

    CROP_DATASET_FILE = 'crop_recommendation.csv'
    CROP_DATASET_PATH = path.join(DATASETS_DIR_PATH, CROP_DATASET_FILE)

    ENSURE_TRAINED_CHECK_INTERVAL = 1

    TOP_N_RESULTS = 3

    def __init__(self, train_parallel=True):
        # A flag that let's the prediction methods know whether the model is trained or not
        self.is_trained = False

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
        ## Load the dataset
        df = pd.read_csv(self.CROP_DATASET_PATH)

        ## Clean dataset

        # Replacing missing N, P, K values with 0
        df.N = df.N.fillna(value = 0)
        df.P = df.P.fillna(value = 0)
        df.K = df.K.fillna(value = 0)

        # Replacing missing temperature, humidity, ph and rainfall values with the mean
        df.temperature = df.temperature.fillna(value = df.temperature.mean())
        df.humidity = df.humidity.fillna(value = df.humidity.mean())
        df.ph = df.ph.fillna(value = df.ph.mean())
        df.rainfall = df.rainfall.fillna(value = df.rainfall.mean())

        # Replacing missing labels with the most repeated label
        df.label = df.label.fillna(value = df.label.mode()[0])

        ## Splitting the dataset into testing and training data

        # Obtaining an instance of the dataset without the label
        x = df.drop('label', axis = 1)

        self.df_columns = x.columns

        # Obtaining just the label column
        y = df['label']

        # Actually splitting the dataset
        x_train , x_test , y_train , y_test = train_test_split(x, y, test_size = 0.30, random_state = 10)

        ## Training the model using random forest classifier
        predictor = RandomForestClassifier(n_estimators = 500, criterion = "entropy")
        predictor.fit(x_train, y_train)

        # Setting the predictor as the recommender's main predictor
        self.predictor = predictor

        # Setting the flag to indicate that the model has been trained
        self.is_trained = True

    # def recommend_for_location(self, lat, lng, n, p, k):
    #     pass

    def recommend(self, n, p, k, temperature, humidity, ph, rainfall):
        self.ensure_trained()
        probs = self.predictor.predict_proba(pd.DataFrame([[n, p, k, temperature, humidity, ph, rainfall]], columns=self.df_columns))[0]
        return list(map(lambda x: x[0], sorted(zip(self.predictor.classes_, probs), key=lambda x: x[1], reverse=True)))[:CropRecommendationModel.TOP_N_RESULTS]

# Test Driver (crop )
def main():
    crop_recommender = CropRecommendationModel()
    print(crop_recommender.recommend(49, 69, 82, 18.3, 15.3, 7.3, 81.78))
    print(crop_recommender.recommend(123, 123, 82, 123.3, 333.3, 123.3, 22.78))
    print(crop_recommender.recommend(1231, 11, 82, 1128.3, 22.3, 123.3, 44.78))

if __name__ == "__main__":
    main()