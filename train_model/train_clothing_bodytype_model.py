import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import ast
import joblib

# Step 1: Load Data
df = pd.read_csv("clothing_model_b_dataset.csv")

# Step 2: Clean + Parse Multi-labels
df['suitable_body_types'] = df['suitable_body_types'].apply(lambda x: [i.strip() for i in x.split(',')])

# Step 3: Combine Text Columns
df['text'] = df['name'] + ' ' + df['description'] + ' ' + df['category'] + ' ' + \
             df['type'] + ' ' + df['style_tag'] + ' ' + df['cut_type'] + ' ' + \
             df['weather_suitability'] + ' ' + df['gender'] + ' ' + df['color'].astype(str)

# Step 4: Encode Labels
mlb = MultiLabelBinarizer()
Y = mlb.fit_transform(df['suitable_body_types'])

# Step 5: Split Data
X_train, X_test, y_train, y_test = train_test_split(df['text'], Y, test_size=0.2, random_state=42)

# Step 6: Pipeline - TFIDF + Random Forest
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=1000)),
    ('clf', MultiOutputClassifier(RandomForestClassifier(n_estimators=100)))
])

# Step 7: Train
pipeline.fit(X_train, y_train)

# Step 8: Evaluate
y_pred = pipeline.predict(X_test)
print(classification_report(y_test, y_pred, target_names=mlb.classes_))


joblib.dump({
    "model": pipeline,
    "label_binarizer": mlb
}, "app/models/clothing_model.pkl")

