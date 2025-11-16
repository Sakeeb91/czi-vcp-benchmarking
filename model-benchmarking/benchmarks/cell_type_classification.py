#!/usr/bin/env python3
"""
Cell Type Classification Benchmark

Compares different ML models on cell type prediction from gene expression data.
"""

import sys
sys.path.append('../models')

import cellxgene_census
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.decomposition import PCA
import argparse
from pathlib import Path
import json

from baseline_models import ModelRegistry
from utils import compare_models, get_classification_report


def load_data(
    organism="homo_sapiens",
    tissue="blood",
    max_cells=10000,
    n_genes=1000,
    census_version="stable"
):
    """
    Load cell type classification data from CELLxGENE Census.

    Parameters:
    -----------
    organism : str
        Organism (homo_sapiens or mus_musculus)
    tissue : str
        Tissue to load
    max_cells : int
        Maximum number of cells to load
    n_genes : int
        Number of highly variable genes to use
    census_version : str
        Census version

    Returns:
    --------
    X : np.ndarray
        Gene expression matrix (cells x genes)
    y : np.ndarray
        Cell type labels
    gene_names : list
        Names of selected genes
    cell_types : list
        Unique cell type names
    """
    print("=" * 80)
    print("Loading Data from CELLxGENE Census")
    print("=" * 80)
    print(f"Organism: {organism}")
    print(f"Tissue: {tissue}")
    print(f"Max cells: {max_cells:,}")
    print()

    with cellxgene_census.open_soma(census_version=census_version) as census:
        # Get organism data
        organism_data = census["census_data"][organism]

        # Load cell metadata
        print("Loading cell metadata...")
        cell_metadata = organism_data["obs"].read(
            column_names=["cell_type", "tissue"],
            value_filter=f"tissue == '{tissue}'"
        ).concat().to_pandas()

        # Sample if needed
        if len(cell_metadata) > max_cells:
            cell_metadata = cell_metadata.sample(n=max_cells, random_state=42)

        print(f"✓ Loaded {len(cell_metadata):,} cells")
        print(f"  Cell types: {cell_metadata['cell_type'].nunique()}")
        print()

        # For this demo, we'll create a simplified dataset
        # In practice, you'd load the actual expression matrix
        # using cellxgene_census.get_anndata() or similar

        print("Creating simplified expression dataset...")
        print("(In production, load actual expression data from Census)")

        # Simulate expression data for demo purposes
        # Replace this with actual Census expression data loading
        np.random.seed(42)
        n_cells = len(cell_metadata)

        # Create synthetic gene expression data
        # (In reality, use census expression matrix)
        X = np.random.randn(n_cells, n_genes) * 2 + 5
        X = np.abs(X)  # Gene expression is non-negative

        # Add cell-type-specific patterns
        le = LabelEncoder()
        y_encoded = le.fit_transform(cell_metadata['cell_type'])

        for i in range(len(le.classes_)):
            cell_mask = y_encoded == i
            # Add specific expression pattern for this cell type
            X[cell_mask, i*10:(i+1)*10] += np.random.randn(cell_mask.sum(), 10) * 3 + 5

        y = cell_metadata['cell_type'].values
        gene_names = [f"Gene_{i}" for i in range(n_genes)]
        cell_types = le.classes_

        print(f"✓ Dataset created: {X.shape}")
        print()

    return X, y, gene_names, cell_types


def preprocess_data(X, y, use_pca=False, n_components=50, scale=True):
    """
    Preprocess expression data.

    Parameters:
    -----------
    X : np.ndarray
        Gene expression matrix
    y : np.ndarray
        Cell type labels
    use_pca : bool
        Whether to apply PCA
    n_components : int
        Number of PCA components
    scale : bool
        Whether to standardize features

    Returns:
    --------
    X_processed : np.ndarray
        Processed features
    y_encoded : np.ndarray
        Encoded labels
    label_encoder : LabelEncoder
        Label encoder object
    """
    print("Preprocessing data...")

    # Encode labels
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    # Standardize features
    if scale:
        scaler = StandardScaler()
        X_processed = scaler.fit_transform(X)
    else:
        X_processed = X.copy()

    # Apply PCA if requested
    if use_pca:
        print(f"  Applying PCA: {X.shape[1]} → {n_components} components")
        pca = PCA(n_components=n_components, random_state=42)
        X_processed = pca.fit_transform(X_processed)
        print(f"  Explained variance: {pca.explained_variance_ratio_.sum():.2%}")

    print(f"✓ Preprocessing complete")
    print(f"  Features shape: {X_processed.shape}")
    print(f"  Number of classes: {len(le.classes_)}")
    print()

    return X_processed, y_encoded, le


def run_benchmark(
    X_train, X_test, y_train, y_test,
    models_to_use=None,
    use_cv=False,
    output_dir="results"
):
    """
    Run the benchmark comparison.

    Parameters:
    -----------
    X_train, X_test : np.ndarray
        Training and test features
    y_train, y_test : np.ndarray
        Training and test labels
    models_to_use : list, optional
        List of model names to use
    use_cv : bool
        Whether to use cross-validation
    output_dir : str
        Directory to save results

    Returns:
    --------
    pd.DataFrame
        Comparison results
    """
    print("=" * 80)
    print("Running Benchmark")
    print("=" * 80)

    # Get models
    registry = ModelRegistry()
    all_models = registry.get_models(include_slow=False)

    # Filter models if specified
    if models_to_use:
        models = {k: v for k, v in all_models.items()
                 if k.lower().replace(" ", "_") in [m.lower() for m in models_to_use]}
    else:
        models = all_models

    print(f"Comparing {len(models)} models:")
    for name in models.keys():
        print(f"  • {name}")
    print()

    # Run comparison
    results = compare_models(
        models=models,
        X_train=X_train,
        X_test=X_test,
        y_train=y_train,
        y_test=y_test,
        use_cv=use_cv
    )

    # Sort by accuracy
    results = results.sort_values('accuracy', ascending=False)

    # Save results
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    csv_path = output_path / "cell_type_classification_results.csv"
    results.to_csv(csv_path, index=False)
    print(f"\n✓ Results saved to {csv_path}")

    return results


def main():
    parser = argparse.ArgumentParser(description="Cell Type Classification Benchmark")
    parser.add_argument("--organism", default="homo_sapiens",
                       help="Organism (homo_sapiens or mus_musculus)")
    parser.add_argument("--tissue", default="blood",
                       help="Tissue to analyze")
    parser.add_argument("--max-cells", type=int, default=5000,
                       help="Maximum number of cells to load")
    parser.add_argument("--n-genes", type=int, default=1000,
                       help="Number of genes to use")
    parser.add_argument("--use-pca", action="store_true",
                       help="Apply PCA for dimensionality reduction")
    parser.add_argument("--pca-components", type=int, default=50,
                       help="Number of PCA components")
    parser.add_argument("--test-size", type=float, default=0.2,
                       help="Test set fraction")
    parser.add_argument("--use-cv", action="store_true",
                       help="Use cross-validation instead of train/test split")
    parser.add_argument("--models", nargs="+",
                       help="Models to use (e.g., random_forest xgboost)")
    parser.add_argument("--output-dir", default="../results",
                       help="Output directory for results")

    args = parser.parse_args()

    print("=" * 80)
    print("CELL TYPE CLASSIFICATION BENCHMARK")
    print("=" * 80)
    print()

    # Load data
    X, y, gene_names, cell_types = load_data(
        organism=args.organism,
        tissue=args.tissue,
        max_cells=args.max_cells,
        n_genes=args.n_genes
    )

    # Preprocess
    X_processed, y_encoded, label_encoder = preprocess_data(
        X, y,
        use_pca=args.use_pca,
        n_components=args.pca_components
    )

    # Split data
    if not args.use_cv:
        X_train, X_test, y_train, y_test = train_test_split(
            X_processed, y_encoded,
            test_size=args.test_size,
            random_state=42,
            stratify=y_encoded
        )
        print(f"Train/test split: {len(X_train)} / {len(X_test)} cells")
        print()
    else:
        X_train, X_test = X_processed, X_processed
        y_train, y_test = y_encoded, y_encoded
        print("Using cross-validation (all data)")
        print()

    # Run benchmark
    results = run_benchmark(
        X_train, X_test, y_train, y_test,
        models_to_use=args.models,
        use_cv=args.use_cv,
        output_dir=args.output_dir
    )

    # Display results
    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)
    print()

    display_cols = ['model', 'accuracy', 'f1_macro', 'training_time']
    available_cols = [col for col in display_cols if col in results.columns]

    print(results[available_cols].to_string(index=False))
    print()

    print("=" * 80)
    print("Benchmark Complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
