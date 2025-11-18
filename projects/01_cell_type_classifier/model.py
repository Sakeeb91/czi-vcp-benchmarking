import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import os

def preprocess_data(adata):
    """
    Preprocesses the AnnData object for training.
    
    Args:
        adata: AnnData object containing expression data and metadata.
        
    Returns:
        tuple: (X, y, label_encoder)
    """
    print("Preprocessing data...")
    
    # 1. Extract Expression Matrix (X)
    # Ensure it's a dense array for scikit-learn
    if hasattr(adata.X, "toarray"):
        X = adata.X.toarray()
    else:
        X = adata.X
        
    # 2. Log-normalize (simple log1p)
    # Note: In a real pipeline, we might want to normalize by library size first
    X = np.log1p(X)
    
    # 3. Extract Labels (y)
    y_raw = adata.obs["cell_type"].values
    
    # 4. Encode Labels
    le = LabelEncoder()
    y = le.fit_transform(y_raw)
    
    print(f"Data shape: {X.shape}")
    print(f"Number of classes: {len(le.classes_)}")
    
    return X, y, le

def train_model(X_train, y_train):
    """
    Trains a Random Forest classifier.
    """
    print("Training Random Forest Classifier...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    clf.fit(X_train, y_train)
    print("Training complete.")
    return clf

def evaluate_model(model, X_test, y_test, label_encoder, output_dir):
    """
    Evaluates the model and saves a confusion matrix plot.
    """
    print("Evaluating model...")
    y_pred = model.predict(X_test)
    
    # Classification Report
    report = classification_report(y_test, y_pred, target_names=label_encoder.classes_)
    print("\nClassification Report:")
    print(report)
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    
    # Plot Confusion Matrix
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=label_encoder.classes_, 
                yticklabels=label_encoder.classes_)
    plt.title("Confusion Matrix")
    plt.ylabel("True Label")
    plt.xlabel("Predicted Label")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    
    save_path = os.path.join(output_dir, "confusion_matrix.png")
    plt.savefig(save_path)
    print(f"Confusion matrix saved to: {save_path}")
    
    return report
