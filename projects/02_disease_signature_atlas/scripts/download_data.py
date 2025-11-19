#!/usr/bin/env python3
"""
Download and prepare data for disease signature analysis.

This script loads disease and control data, preprocesses with Scanpy,
and saves for further analysis.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from data.data_loader import DiseaseDataLoader
from data.preprocessing import ScancpyPreprocessor


def main():
    print("="*70)
    print("Disease Signature Atlas - Data Download")
    print("="*70)
    
    # Initialize loader and preprocessor
    loader = DiseaseDataLoader()
    preprocessor = ScancpyPreprocessor()
    
    # Load data
    print("\n📥 Loading data from CELLxGENE Census...")
    disease_data, control_data, metadata = loader.load_disease_data(
        disease_key="covid19",
        tissues=["blood"],
        max_cells_per_tissue=5000
    )
    
    print(f"\n✓ Loaded:")
    print(f"  Disease: {disease_data.n_obs:,} cells")
    print(f"  Control: {control_data.n_obs:,} cells")
    
    # Preprocess
    print("\n🔬 Preprocessing with Scanpy...")
    disease_processed = preprocessor.preprocess(disease_data)
    control_processed = preprocessor.preprocess(control_data)
    
    print("\n✓ Data ready for analysis!")
    print(f"  Disease (processed): {disease_processed.n_obs:,} cells")
    print(f"  Control (processed): {control_processed.n_obs:,} cells")
    
    # Save (optional - uncomment if you want to cache)
    # disease_processed.write("results/disease_blood_processed.h5ad")
    # control_processed.write("results/control_blood_processed.h5ad")


if __name__ == "__main__":
    main()
