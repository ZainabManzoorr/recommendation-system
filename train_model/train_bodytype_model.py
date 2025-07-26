import pandas as pd 
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os

df = pd.read_csv("data/user_measurements.csv")

body_label_encoder = LabelEncoder()
df['body_type_encoded'] = body_label_encoder.fit_transform(df['body_type'])

gender_label_encoder = LabelEncoder()
df['gender_type_encoded']= gender_label_encoder.fit_transform(df['gender'])

X = df[["height", "weight", "chest", "waist", "hips", "shoulder", "sleeve","gender_type_encoded"]]
Y = df["body_type"]

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

model = RandomForestClassifier()

model.fit(X_train, Y_train)

joblib.dump(model, "app/models/bodytype_model.pkl")
joblib.dump(body_label_encoder, "app/models/body_type_label_encoder.pkl")
joblib.dump(gender_label_encoder, "app/models/gender_label_encoder.pkl")

print("✅ Model trained and saved including gender feature!")