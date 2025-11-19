import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import os

def preprocess_data(adata, n_top_genes=500):
    """
    Preprocesses the AnnData object for training with feature selection.
    OPTIMIZED FOR SPEED: Uses fewer genes (500) for faster training.
    
    Args:
        adata: AnnData object containing expression data and metadata.
        n_top_genes: Number of top variable genes to select (default: 500)
        
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
    X = np.log1p(X)
    
    # 3. Extract Labels (y)
    y_raw = adata.obs["cell_type"].values
    
    # 4. Encode Labels
    le = LabelEncoder()
    y = le.fit_transform(y_raw)
    
    print(f"Data shape before feature selection: {X.shape}")
    
    # 5. Feature Selection - Select top variable genes
    # Use variance-based selection (more genes = more noise with small samples)
    n_features = min(n_top_genes, X.shape[1])
    gene_variances = np.var(X, axis=0)
    top_gene_indices = np.argsort(gene_variances)[-n_features:]
    X_selected = X[:, top_gene_indices]
    
    print(f"Data shape after feature selection: {X_selected.shape}")
    print(f"Selected top {n_features} most variable genes")
    print(f"Number of classes: {len(le.classes_)}")
    
    # 6. Standard Scaling for better model performance
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_selected)
    
    return X_scaled, y, le

def train_model(X_train, y_train):
    """
    Trains a speed-optimized Random Forest classifier.
    OPTIMIZED FOR SPEED: Fewer trees, shallower depth.
    """
    print("Training Random Forest Classifier (speed-optimized)...")
    # Speed-optimized parameters:
    # - Only 20 trees (vs 50) for 2.5x faster training
    # - Max depth 8 (vs 10) for faster tree building
    # - Balanced class weights maintained
    clf = RandomForestClassifier(
        n_estimators=20,
        max_depth=8,
        min_samples_split=3,
        min_samples_leaf=2,
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    )
    clf.fit(X_train, y_train)
    print("Training complete.")
    return clf

def evaluate_model(model, X_test, y_test, label_encoder, output_dir):
    """
    Evaluates the model and saves a confusion matrix plot.
    """
    print("Evaluating model...")
    y_pred = model.predict(X_test)
    
    # Classification Report (only for labels present in test set)
    labels_present = np.unique(np.concatenate([y_test, y_pred]))
    target_names_present = [label_encoder.classes_[i] for i in labels_present]
    report = classification_report(y_test, y_pred, labels=labels_present, target_names=target_names_present)
    print("\nClassification Report:")
    print(report)
    
    # Confusion Matrix (only for labels present)
    cm = confusion_matrix(y_test, y_pred, labels=labels_present)
    
    # Plot Confusion Matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=target_names_present, 
                yticklabels=target_names_present)
    plt.title("Confusion Matrix")
    plt.ylabel("True Label")
    plt.xlabel("Predicted Label")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    
    save_path = os.path.join(output_dir, "confusion_matrix.png")
    plt.savefig(save_path)
    print(f"Confusion matrix saved to: {save_path}")
    
    return report
