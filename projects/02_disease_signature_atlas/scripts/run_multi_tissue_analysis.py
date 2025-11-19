#!/usr/bin/env python3
"""
Run multi-tissue analysis pipeline.

This script:
1. Loads data for multiple tissues
2. Runs differential expression analysis
3. Performs cross-tissue correlation analysis
4. Generates comparative visualizations
"""

import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))
sys.path.insert(0, str(project_root.parent.parent / "shared"))

from data.data_loader import DiseaseDataLoader
from data.preprocessing import ScancpyPreprocessor
from analysis.differential_expression import DifferentialExpressionAnalyzer
from analysis.cross_tissue_analysis import CrossTissueAnalyzer
from visualization.multi_tissue_plots import MultiTissueVisualizer


def main():
    print("="*80)
    print("MULTI-TISSUE ANALYSIS PIPELINE")
    print("="*80)
    
    # Configuration
    disease_key = "covid19"
    tissues = ["blood", "lung", "heart"]
    max_cells = 1500  # Small for testing
    
    print(f"\nConfiguration:")
    print(f"  Disease: {disease_key}")
    print(f"  Tissues: {', '.join(tissues)}")
    
    # Initialize tools
    loader = DiseaseDataLoader()
    preprocessor = ScancpyPreprocessor()
    de_analyzer = DifferentialExpressionAnalyzer()
    cross_analyzer = CrossTissueAnalyzer()
    visualizer = MultiTissueVisualizer()
    
    # Storage
    tissue_data = {}
    de_results = {}
    
    # 1. Process each tissue
    for tissue in tissues:
        print(f"\nProcessing {tissue}...")
        
        # Load
        try:
            disease, control, meta = loader.load_disease_data(
                disease_key=disease_key,
                tissues=[tissue],
                max_cells_per_tissue=max_cells,
                verbose=False
            )
        except Exception as e:
            print(f"  Skipping {tissue}: {e}")
            continue
            
        # Preprocess
        disease_proc = preprocessor.preprocess(disease, verbose=False)
        control_proc = preprocessor.preprocess(control, verbose=False)
        
        # Store processed disease data for correlation
        tissue_data[tissue] = disease_proc
        
        # Run DE
        combined = de_analyzer.prepare_for_de(disease_proc, control_proc, tissue)
        results = de_analyzer.run_de_analysis(combined)
        sig_genes = de_analyzer.filter_significant_genes(results)
        
        de_results[tissue] = sig_genes
        print(f"  Found {len(sig_genes)} significant genes")
        
    # 2. Cross-Tissue Correlation
    print(f"\n{'='*80}")
    print("CROSS-TISSUE CORRELATION")
    print(f"{'='*80}")
    
    # Compute correlation of expression profiles (using HVGs)
    corr_matrix = cross_analyzer.compute_expression_correlation(tissue_data)
    print("\nExpression Correlation Matrix:")
    print(corr_matrix)
    
    # Plot correlation
    output_dir = project_root / "results" / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    visualizer.plot_correlation_heatmap(
        corr_matrix,
        title=f"Cross-Tissue Expression Correlation ({disease_key})",
        save_path=str(output_dir / "expression_correlation.png")
    )
    
    # 3. Signature Overlap
    print(f"\n{'='*80}")
    print("SIGNATURE OVERLAP")
    print(f"{'='*80}")
    
    # Compute Jaccard overlap
    overlap_matrix = cross_analyzer.compute_signature_overlap(de_results, metric='jaccard')
    print("\nSignature Overlap (Jaccard):")
    print(overlap_matrix)
    
    visualizer.plot_signature_overlap(
        overlap_matrix,
        save_path=str(output_dir / "signature_overlap.png")
    )
    
    visualizer.plot_upset_like_bar(
        de_results,
        save_path=str(output_dir / "signature_counts.png")
    )
    
    # 4. Cross-Tissue Heatmap of Top Genes
    print(f"\n{'='*80}")
    print("CROSS-TISSUE HEATMAP")
    print(f"{'='*80}")
    
    # Find top shared genes
    all_sig_genes = set()
    for df in de_results.values():
        all_sig_genes.update(df['gene'])
        
    # Count occurrence
    gene_counts = {}
    for gene in all_sig_genes:
        count = sum(1 for df in de_results.values() if gene in df['gene'].values)
        gene_counts[gene] = count
        
    # Select genes present in at least 2 tissues
    shared_genes = [g for g, c in gene_counts.items() if c >= 2]
    print(f"Found {len(shared_genes)} genes shared across at least 2 tissues")
    
    if len(shared_genes) > 0:
        # Get fold changes
        fc_matrix = cross_analyzer.compare_fold_changes(de_results, shared_genes)
        
        # Plot
        visualizer.plot_cross_tissue_heatmap(
            fc_matrix,
            title="Shared Disease Signatures (log2FC)",
            save_path=str(output_dir / "shared_signatures_heatmap.png")
        )
    else:
        print("Not enough shared genes for heatmap.")

    print(f"\n{'='*80}")
    print("✅ ANALYSIS COMPLETE!")
    print(f"Results saved to: {output_dir}")

if __name__ == "__main__":
    main()
