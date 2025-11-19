from data_loader import load_census_data

import matplotlib.pyplot as plt
import os

from model import preprocess_data, train_model, evaluate_model
from sklearn.model_selection import train_test_split

def main():
    print("Starting Cell Type Classifier Project...")
    
    # 1. Load Data
    try:
        # Fetch a larger sample for training
        print("Loading data from Census...")
        adata, total_cells = load_census_data(
            tissue="blood",
            max_cells=500  # Production-scale run
        )
        
        print("\n" + "="*50)
        print(f"DATASET REPORT")
        print("="*50)
        print(f"Total available cells in Census (blood): {total_cells:,}")
        print(f"Cells loaded for analysis: {adata.n_obs:,}")
        print(f"Genes loaded: {adata.n_vars:,}")
        print("="*50 + "\n")
        
        # 2. Preprocess Data
        X, y, label_encoder = preprocess_data(adata)
        
        # 3. Split Data
        print("Splitting data into train/test sets...")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42  # No stratify for small samples
        )
        print(f"Training set: {X_train.shape[0]} cells")
        print(f"Test set: {X_test.shape[0]} cells")
        
        # 4. Train Model
        clf = train_model(X_train, y_train)
        
        # 5. Evaluate Model
        output_dir = os.path.join("projects", "01_cell_type_classifier", "plots")
        evaluate_model(clf, X_test, y_test, label_encoder, output_dir)
        
    except Exception as e:
        print(f"Error in pipeline: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
