import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier

IMG_SIZE = 128

# Create model
def create_model():
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    return model

# Train model with dummy data
def train_model(model):
    X = np.random.rand(2, IMG_SIZE * IMG_SIZE * 3)
    y = np.array([0, 1])
    model.fit(X, y)
    return model
        X = np.random.rand(2, IMG_SIZE, IMG_SIZE, 3)
        y = np.array([0, 1])
        model.fit(X, y, epochs=20, verbose=0)
        return model
    else:
        return model

class CovidApp:
    def __init__(self, root):
        self.root = root
        self.root.title("COVID-19 Detection AI")
        self.root.geometry("500x600")
        self.model = None
        self.selected_image_path = None
        
        # Title
        title = tk.Label(root, text="COVID-19 Detection", font=("Arial", 20, "bold"))
        title.pack(pady=20)
        
        # Image display area
        self.image_label = tk.Label(root, bg="gray", width=40, height=15)
        self.image_label.pack(pady=10)
        
        # Buttons frame
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        
        # Load Image button
        load_btn = tk.Button(button_frame, text="Load Image", command=self.load_image, 
                            bg="blue", fg="white", font=("Arial", 12), padx=20)
        load_btn.pack(side=tk.LEFT, padx=5)
        
        # Predict button
        predict_btn = tk.Button(button_frame, text="Predict", command=self.predict, 
                               bg="green", fg="white", font=("Arial", 12), padx=20)
        predict_btn.pack(side=tk.LEFT, padx=5)
        
        # Result label
        self.result_label = tk.Label(root, text="Result: ", font=("Arial", 14, "bold"))
        self.result_label.pack(pady=20)
        
        # Status label
        self.status_label = tk.Label(root, text="Loading model...", font=("Arial", 10))
        self.status_label.pack(pady=10)
        
        # Initialize model in background
        self.init_model()
        
    def init_model(self):
        try:
            self.status_label.config(text="Training model...")
            self.root.update()
            
            self.model = create_model()
            self.model = train_model(self.model)
            
            self.status_label.config(text="Model ready!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to train model: {str(e)}")
    
    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if file_path:
            self.selected_image_path = file_path
            # Display image
            img = Image.open(file_path)
            img.thumbnail((400, 300))
            photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=photo)
            self.image_label.image = photo
            self.result_label.config(text="Result: ")
            self.status_label.config(text=f"Loaded: {os.path.basename(file_path)}")
    
    def predict(self):
        if self.model is None:
            messagebox.showwarning("Warning", "Model is still loading. Please wait.")
            return
        
        if self.selected_image_path is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
        
        try:
            self.status_label.config(text="Analyzing...")
            self.root.update()
            
            # Load and preprocess image
            test_image = Image.open(self.selected_image_path).convert('RGB').resize((IMG_SIZE, IMG_SIZE))
            test_image = np.array(test_image) / 255.0
            test_image = test_image.flatten().reshape(1, -1)
            
            # Make prediction
            prediction = self.model.predict_proba(test_image)
            confidence = prediction[0][1]
            
            # Display result
            if confidence > 0.5:
                result = f"COVID-19 DETECTED\nConfidence: {confidence:.2%}"
                self.result_label.config(text=result, fg="red")
            else:
                result = f"NORMAL (COVID-19 Not Detected)\nConfidence: {(1-confidence):.2%}"
                self.result_label.config(text=result, fg="green")
            
            self.status_label.config(text="Prediction complete!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Prediction failed: {str(e)}")
            self.status_label.config(text="Error during prediction")

if __name__ == "__main__":
    root = tk.Tk()
    app = CovidApp(root)
    root.mainloop()
