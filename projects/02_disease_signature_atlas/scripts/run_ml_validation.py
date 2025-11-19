#!/usr/bin/env python3
"""
Run Machine Learning Validation Pipeline (Phase 5).

This script:
1. Loads data for multiple tissues (Blood, Lung, Heart)
2. Trains classifiers on one tissue (e.g., Blood)
3. Tests performance on held-out tissues (Lung, Heart)
4. Evaluates feature importance (signature genes)
"""

import sys
import os
from pathlib import Path
import yaml
import pandas as pd
import matplotlib.pyplot as plt

# Add src and shared to path
repo_root = Path(__file__).resolve().parents[3]
sys.path.append(str(repo_root / "shared"))
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from data.data_loader import DiseaseDataLoader
from models.classifiers import DiseaseClassifier
from models.evaluation import ModelEvaluator

def main():
    print("="*80)
    print("ML VALIDATION PIPELINE")
    print("="*80)
    
    # Load config
    config_path = Path(__file__).resolve().parents[1] / "config.yaml"
    with open(config_path) as f:
        config = yaml.safe_load(f)
        
    # Setup
    loader = DiseaseDataLoader(config_path)
    evaluator = ModelEvaluator(output_dir="results/models")
    
    # 1. Load Data
    print("\n1. Loading Data...")
    tissues = ["blood", "lung", "heart"]
    disease_key = "covid19"
    
    datasets = {}
    for tissue in tissues:
        print(f"  Loading {tissue}...")
        try:
            disease_data, control_data, _ = loader.load_disease_data(
                disease_key=disease_key,
                tissues=[tissue],
                max_cells_per_tissue=100,  # Minimal for fast testing
                verbose=True
            )
            
            # Combine disease and control for ML
            import anndata as ad
            
            # Add labels
            disease_data.obs['condition'] = 'disease'
            control_data.obs['condition'] = 'healthy'
            
            # Concatenate
            adata = ad.concat([disease_data, control_data], label="batch")
            datasets[tissue] = adata
        except Exception as e:
            print(f"  Failed to load {tissue}: {e}")
            
    if not datasets:
        print("No data loaded. Exiting.")
        return

    # 2. Train on Blood (or first available)
    train_tissue = "blood"
    if train_tissue not in datasets:
        train_tissue = list(datasets.keys())[0]
        
    print(f"\n2. Training Classifier on {train_tissue}...")
    train_data = datasets[train_tissue]
    
    clf = DiseaseClassifier(model_type='rf', n_estimators=100)
    metrics = clf.train(train_data, target_col='condition')
    
    # Save model
    model_save_path = Path(__file__).resolve().parents[1] / "results" / "models" / "disease_classifier_rf.joblib"
    model_save_path.parent.mkdir(parents=True, exist_ok=True)
    clf.save(str(model_save_path))
    print(f"Model saved to {model_save_path}")
    
    # 3. Cross-Tissue Evaluation
    print("\n3. Cross-Tissue Evaluation...")
    results = evaluator.evaluate_cross_tissue(
        clf, 
        datasets, 
        target_col='condition'
    )
    
    print("\nCross-Tissue Performance:")
    print(results)
    
    # Save results
    results_dir = Path(__file__).resolve().parents[1] / "results" / "models"
    results_dir.mkdir(parents=True, exist_ok=True)
    results.to_csv(results_dir / "cross_tissue_performance.csv", index=False)
    
    # 4. Feature Importance
    print("\n4. Feature Importance...")
    importance = clf.get_feature_importance(top_n=20)
    print(importance)
    importance.to_csv(results_dir / "feature_importance.csv", index=False)
    
    # Plot importance
    plt.figure(figsize=(10, 6))
    plt.barh(importance['gene'], importance['importance'])
    plt.xlabel('Importance')
    plt.title(f'Top 20 Predictive Genes (Trained on {train_tissue})')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(results_dir / "feature_importance.png")
    
    print("\nPipeline Complete! Results saved to results/models/")

if __name__ == "__main__":
    main()
