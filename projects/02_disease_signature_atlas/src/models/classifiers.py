"""
Machine learning classifiers for disease prediction.

This module implements models to predict disease state based on gene expression
signatures, supporting cross-tissue generalization testing.
"""

import numpy as np
import pandas as pd
import anndata as ad
from typing import Dict, List, Optional, Tuple, Union
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, f1_score, classification_report
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib
from pathlib import Path

class DiseaseClassifier:
    """Classifier for predicting disease state from gene expression."""
    
    def __init__(
        self,
        model_type: str = 'rf',
        n_estimators: int = 100,
        max_depth: Optional[int] = None,
        random_state: int = 42
    ):
        """
        Initialize classifier.
        
        Parameters
        ----------
        model_type : str
            'rf' (Random Forest) or 'lr' (Logistic Regression)
        n_estimators : int
            Number of trees (for RF)
        max_depth : int
            Max depth of trees (for RF)
        random_state : int
            Random seed
        """
        self.model_type = model_type
        self.random_state = random_state
        self.le = LabelEncoder()
        self.scaler = StandardScaler()
        self.genes = None
        
        if model_type == 'rf':
            self.model = RandomForestClassifier(
                n_estimators=n_estimators,
                max_depth=max_depth,
                random_state=random_state,
                n_jobs=-1,
                class_weight='balanced'
            )
        elif model_type == 'lr':
            self.model = LogisticRegression(
                random_state=random_state,
                max_iter=1000,
                class_weight='balanced',
                n_jobs=-1
            )
        else:
            raise ValueError(f"Unknown model type: {model_type}")
            
    def train(
        self,
        adata: ad.AnnData,
        target_col: str = 'condition',
        genes: Optional[List[str]] = None,
        test_size: float = 0.2
    ) -> Dict[str, float]:
        """
        Train the model.
        
        Parameters
        ----------
        adata : anndata.AnnData
            Annotated data matrix
        target_col : str
            Column in obs containing labels
        genes : list, optional
            List of genes to use as features. If None, uses all var_names.
        test_size : float
            Fraction of data to use for testing
            
        Returns
        -------
        metrics : dict
            Training metrics
        """
        print(f"\nTraining {self.model_type.upper()} classifier...")
        
        # Prepare features
        if genes is None:
            self.genes = adata.var_names.tolist()
        else:
            # Ensure genes exist in adata
            valid_genes = [g for g in genes if g in adata.var_names]
            if len(valid_genes) < len(genes):
                print(f"Warning: {len(genes) - len(valid_genes)} genes not found in data")
            self.genes = valid_genes
            
        X = adata[:, self.genes].X
        if hasattr(X, 'toarray'):
            X = X.toarray()
            
        # Prepare labels
        y = adata.obs[target_col].values
        y_encoded = self.le.fit_transform(y)
        
        print(f"Features: {len(self.genes)} genes")
        print(f"Classes: {list(self.le.classes_)}")
        
        # Scale data
        X_scaled = self.scaler.fit_transform(X)
        
        # Split
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y_encoded, test_size=test_size, random_state=self.random_state, stratify=y_encoded
        )
        
        # Train
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        
        print(f"Training complete. Accuracy: {acc:.3f}, F1: {f1:.3f}")
        
        return {
            'accuracy': acc,
            'f1_score': f1,
            'n_train': len(X_train),
            'n_test': len(X_test)
        }
    
    def predict(
        self,
        adata: ad.AnnData,
        target_col: Optional[str] = None
    ) -> Tuple[np.ndarray, Optional[float]]:
        """
        Predict on new data.
        
        Parameters
        ----------
        adata : anndata.AnnData
            New data
        target_col : str, optional
            If provided, calculates accuracy
            
        Returns
        -------
        predictions : np.ndarray
            Predicted labels
        accuracy : float, optional
            Accuracy if target_col provided
        """
        if self.genes is None:
            raise ValueError("Model not trained yet")
            
        # Check for missing genes
        missing = [g for g in self.genes if g not in adata.var_names]
        if missing:
            # Handle missing genes (fill with 0)
            print(f"Warning: {len(missing)} feature genes missing in new data. Filling with 0.")
            # Create DataFrame to handle alignment
            X_df = pd.DataFrame(
                adata.X.toarray() if hasattr(adata.X, 'toarray') else adata.X,
                columns=adata.var_names
            )
            # Add missing columns
            for g in missing:
                X_df[g] = 0.0
            # Select correct order
            X = X_df[self.genes].values
        else:
            X = adata[:, self.genes].X
            if hasattr(X, 'toarray'):
                X = X.toarray()
                
        # Scale
        X_scaled = self.scaler.transform(X)
        
        # Predict
        y_pred_idx = self.model.predict(X_scaled)
        y_pred = self.le.inverse_transform(y_pred_idx)
        
        acc = None
        if target_col and target_col in adata.obs:
            y_true = adata.obs[target_col].values
            acc = accuracy_score(y_true, y_pred)
            print(f"Prediction Accuracy: {acc:.3f}")
            
        return y_pred, acc
    
    def get_feature_importance(self, top_n: int = 20) -> pd.DataFrame:
        """Get top important genes."""
        if self.model_type == 'rf':
            importances = self.model.feature_importances_
        elif self.model_type == 'lr':
            importances = np.abs(self.model.coef_[0])
        else:
            return pd.DataFrame()
            
        df = pd.DataFrame({
            'gene': self.genes,
            'importance': importances
        })
        return df.sort_values('importance', ascending=False).head(top_n)
        
    def save(self, path: str):
        """Save model to disk."""
        joblib.dump(self, path)
        print(f"Model saved to {path}")
        
    @classmethod
    def load(cls, path: str):
        """Load model from disk."""
        return joblib.load(path)

if __name__ == "__main__":
    print("Classifiers module loaded successfully")
