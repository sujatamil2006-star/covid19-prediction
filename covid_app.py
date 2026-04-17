from sklearn.ensemble import RandomForestClassifier
from PIL import Image
import numpy as np
import os
import joblib

IMG_SIZE = 128

# Load and preprocess image
def load_image(path, label):
    img = Image.open(path).convert('RGB').resize((IMG_SIZE, IMG_SIZE))
    img = np.array(img) / 255.0
    img = img.flatten()
    return img, label

# Load dataset (create dummy data for testing)
normal_img = np.random.rand(IMG_SIZE * IMG_SIZE * 3)
normal_label = 0
covid_img = np.random.rand(IMG_SIZE * IMG_SIZE * 3)
covid_label = 1

X = np.array([normal_img, covid_img])
y = np.array([normal_label, covid_label])

# Random Forest Model
model = RandomForestClassifier(n_estimators=10, random_state=42)

model.fit(X, y)

# Save the model
joblib.dump(model, 'covid_model.pkl')

# Test Prediction
test_image = np.random.rand(IMG_SIZE * IMG_SIZE * 3)
test_image = test_image.reshape(1, -1)

prediction = model.predict_proba(test_image)

if prediction[0][1] > 0.5:
    print("Prediction: COVID")
else:
    print("Prediction: NORMAL")
    


