#!/usr/bin/env python3
"""
Main analysis script for cell type distribution analysis.

This script:
1. Loads cell metadata from the CZI CELLxGENE Census
2. Analyzes cell type distributions across tissues
3. Generates visualizations
4. Saves summary statistics
"""

import pandas as pd
from pathlib import Path
import sys

from data_loader import load_cell_metadata, get_available_tissues, get_cell_type_summary
from visualization import (
    plot_cell_type_heatmap,
    plot_top_cell_types,
    plot_tissue_composition,
    plot_tissue_comparison
)


def main():
    """Main analysis pipeline."""

    print("=" * 80)
    print("Cell Type Distribution Analysis")
    print("=" * 80)
    print()

    # Configuration
    ORGANISM = "homo_sapiens"  # or "mus_musculus"
    TARGET_TISSUES = ["blood", "lung", "brain", "heart", "liver"]
    MAX_CELLS_PER_TISSUE = 5000  # Limit to keep analysis manageable

    # Step 1: Get available tissues
    print("Step 1: Exploring available tissues...")
    print("-" * 80)
    tissue_counts = get_available_tissues(organism=ORGANISM)

    print("\nTop 10 tissues by cell count:")
    for tissue, count in tissue_counts.head(10).items():
        print(f"  • {tissue}: {count:,} cells")
    print()

    # Step 2: Load cell metadata for target tissues
    print("Step 2: Loading cell metadata...")
    print("-" * 80)
    cell_data = load_cell_metadata(
        organism=ORGANISM,
        tissues=TARGET_TISSUES,
        max_cells_per_tissue=MAX_CELLS_PER_TISSUE
    )
    print()

    # Step 3: Generate summary statistics
    print("Step 3: Generating summary statistics...")
    print("-" * 80)
    summary = get_cell_type_summary(cell_data)

    print(f"Cell types analyzed: {len(summary)}")
    print(f"Tissues analyzed: {len(summary.columns)}")
    print()

    # Save summary to CSV
    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)

    summary_path = output_dir / "cell_type_summary.csv"
    summary.to_csv(summary_path)
    print(f"✓ Saved summary statistics to {summary_path}")
    print()

    # Step 4: Generate visualizations
    print("Step 4: Generating visualizations...")
    print("-" * 80)

    # 4a. Heatmap of cell types across tissues
    plot_cell_type_heatmap(summary.head(30))  # Top 30 cell types

    # 4b. Bar chart of most abundant cell types
    plot_top_cell_types(cell_data)

    # 4c. Tissue composition pie charts for each tissue
    for tissue in TARGET_TISSUES:
        plot_tissue_composition(cell_data, tissue)

    # 4d. Comparison across tissues
    plot_tissue_comparison(cell_data, TARGET_TISSUES)

    print()

    # Step 5: Print key findings
    print("Step 5: Key Findings")
    print("-" * 80)

    print("\nMost abundant cell types overall:")
    top_types = cell_data['cell_type'].value_counts().head(5)
    for i, (cell_type, count) in enumerate(top_types.items(), 1):
        print(f"  {i}. {cell_type}: {count:,} cells")

    print("\nCell type diversity by tissue:")
    diversity = cell_data.groupby('tissue')['cell_type'].nunique().sort_values(ascending=False)
    for tissue, n_types in diversity.items():
        print(f"  • {tissue}: {n_types} unique cell types")

    print()
    print("=" * 80)
    print("Analysis complete!")
    print("=" * 80)
    print(f"\nResults saved to: {output_dir.absolute()}")
    print(f"  • CSV: {summary_path}")
    print(f"  • Figures: {output_dir / 'figures'}")
    print()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
