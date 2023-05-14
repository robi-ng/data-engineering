"""
This script predicts the car buying price using
machine learning model on the provided car data.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

# Definition
buying_price_map = {
    "low": 0,
    "med": 1,
    "high": 2,
    "vhigh": 3,
}
column_names = [
    "buying_price",
    "maintenance",
    "doors",
    "persons",
    "lug_boot",
    "safety",
    "class_value",
]

# Read and prepare data
df = pd.read_csv("data/car.csv", names=column_names)

data_columns = column_names[1:]
df = pd.get_dummies(df, columns=data_columns)

y = df["buying_price"].apply(lambda x: buying_price_map[x])
X = df.drop("buying_price", axis=1)

# Train the model
X_train, X_test, y_train, y_test = train_test_split(
    X, y, train_size=0.80, random_state=1
)
scaler = StandardScaler()
X_train = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns)
model = SVC()
model.fit(X_train, y_train)

# Predict with parameters
query = pd.DataFrame(
    {
        "maintenance": ["high"],
        "doors": ["4"],
        "lug_boot": ["big"],
        "safety": ["high"],
        "class_value": ["good"],
    }
)
query = pd.get_dummies(query)

full_query_row = X_train[:1].copy()
for column in full_query_row:
    full_query_row[column] = True if column in query else False

predicted_result = model.predict(full_query_row)[0]

for k, v in buying_price_map.items():
    if v == predicted_result:
        print(f"Predicted buying price: {k}")
