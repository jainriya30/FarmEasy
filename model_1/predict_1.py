from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd

## Load the dataset
df = pd.read_csv('crop_recommendation.csv')

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

# Obtaining just the label column
y = df['label']

# Actually splitting the dataset
x_train , x_test , y_train , y_test = train_test_split(x, y, test_size = 0.30, random_state = 10)

## Training the model using random forest classifier
rfc = RandomForestClassifier(n_estimators = 500, criterion = "entropy")
rfc.fit(x_train, y_train) 

res = 1

## Testing the trained model
predict_r = rfc.predict_proba(x_test[:1])[0]

print(len(predict_r))
print("===")
print(len(rfc.classes_))



## Displaying the result

print(predict_r)