from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
import joblib
from backend_supabase.fetch_data import fetch_measurements

def train_model():
  df = fetch_measurements()

  X = df[['height','weight','chest','waist','hips','shoulder','sleeve']]
  Y = df['body_type']

  X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

  clf = DecisionTreeClassifier()
  clf.fit(X_train,y_train)

  y_pred = clf.predict(X_test)
  print(f"Classification Report :", classification_report(y_test,y_pred))

  joblib.dump(clf,"body_type_classifier.joblib")
  print("Model saved as body_type_classifier.joblib")

if __name__ == "__main__":
  train_model()