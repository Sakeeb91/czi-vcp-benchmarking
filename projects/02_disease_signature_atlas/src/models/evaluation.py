"""
Evaluation metrics and visualization for disease classifiers.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve, auc, confusion_matrix, precision_recall_curve
from typing import Dict, List, Optional, Tuple
import os

class ModelEvaluator:
    """Evaluator for disease classification models."""
    
    def __init__(self, output_dir: str = "results/models"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def plot_roc_curve(
        self,
        model,
        X_test,
        y_test,
        save_name: str = "roc_curve.png"
    ):
        """Plot ROC curve."""
        if hasattr(model, "predict_proba"):
            y_score = model.predict_proba(X_test)[:, 1]
        else:
            print("Model does not support predict_proba")
            return
            
        fpr, tpr, _ = roc_curve(y_test, y_score)
        roc_auc = auc(fpr, tpr)
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic')
        plt.legend(loc="lower right")
        plt.grid(True, alpha=0.3)
        
        plt.savefig(os.path.join(self.output_dir, save_name), dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Saved ROC curve to {save_name}")
        
    def plot_confusion_matrix(
        self,
        y_true,
        y_pred,
        classes: List[str],
        save_name: str = "confusion_matrix.png"
    ):
        """Plot confusion matrix."""
        cm = confusion_matrix(y_true, y_pred)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=classes, yticklabels=classes)
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        
        plt.savefig(os.path.join(self.output_dir, save_name), dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Saved confusion matrix to {save_name}")
        
    def evaluate_cross_tissue(
        self,
        model,
        tissue_datasets: Dict[str, object],
        target_col: str = 'condition'
    ) -> pd.DataFrame:
        """
        Evaluate model performance across multiple tissues.
        
        Parameters
        ----------
        model : DiseaseClassifier
            Trained model
        tissue_datasets : dict
            Dict of {tissue_name: adata}
        target_col : str
            Target column name
            
        Returns
        -------
        results : pd.DataFrame
            Performance metrics per tissue
        """
        results = []
        
        for tissue, adata in tissue_datasets.items():
            print(f"Evaluating on {tissue}...")
            try:
                y_pred, acc = model.predict(adata, target_col=target_col)
                
                if acc is not None:
                    results.append({
                        'tissue': tissue,
                        'accuracy': acc,
                        'n_samples': adata.n_obs
                    })
            except Exception as e:
                print(f"Error evaluating on {tissue}: {e}")
                
        return pd.DataFrame(results)

if __name__ == "__main__":
    print("Evaluation module loaded successfully")
