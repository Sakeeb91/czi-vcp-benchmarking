#!/usr/bin/env python3
"""
Run complete disease signature discovery pipeline.

This script:
1. Loads disease and control data from multiple tissues
2. Preprocesses with Scanpy
3. Runs differential expression analysis
4. Identifies cross-tissue and tissue-specific signatures
5. Saves results
"""

import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))
sys.path.insert(0, str(project_root.parent.parent / "shared"))

from data.data_loader import DiseaseDataLoader
from data.preprocessing import ScancpyPreprocessor
from analysis.differential_expression import DifferentialExpressionAnalyzer, run_single_tissue_de
from analysis.signature_discovery import SignatureDiscovery


def main():
    print("="*80)
    print("DISEASE SIGNATURE DISCOVERY PIPELINE")
    print("="*80)
    
    # Configuration
    disease_key = "covid19"
    tissues = ["blood", "lung"]  # Start with 2 tissues
    max_cells = 2000  # Small for testing
    
    print(f"\nConfiguration:")
    print(f"  Disease: {disease_key}")
    print(f"  Tissues: {', '.join(tissues)}")
    print(f"  Max cells per tissue: {max_cells:,}")
    
    # Initialize
    loader = DiseaseDataLoader()
    preprocessor = ScancpyPreprocessor()
    analyzer = DifferentialExpressionAnalyzer()
    discoverer = SignatureDiscovery()
    
    # Storage for results
    tissue_de_results = {}
    
    # Process each tissue
    for tissue in tissues:
        print(f"\n\n{'='*80}")
        print(f"PROCESSING TISSUE: {tissue.upper()}")
        print(f"{'='*80}")
        
        # Step 1: Load data
        print(f"\n[1/4] Loading {tissue} data...")
        disease_data, control_data, meta = loader.load_single_tissue(
            tissue=tissue,
            disease_key=disease_key,
            max_cells=max_cells,
            verbose=True
        )
        
        # Step 2: Preprocess
        print(f"\n[2/4] Preprocessing with Scanpy...")
        disease_processed = preprocessor.preprocess(disease_data, verbose=True)
        control_processed = preprocessor.preprocess(control_data, verbose=True)
        
        # Step 3: Differential expression
        print(f"\n[3/4] Running differential expression analysis...")
        combined = analyzer.prepare_for_de(
            disease_processed,
            control_processed,
            tissue_label=tissue
        )
        
        de_results = analyzer.run_de_analysis(combined)
        sig_genes = analyzer.filter_significant_genes(de_results)
        
        # Store results
        tissue_de_results[tissue] = sig_genes
        
        # Step 4: Save individual tissue results
        print(f"\n[4/4] Saving {tissue} results...")
        output_dir = project_root / "results" / "differential_expression"
        analyzer.save_results(sig_genes, str(output_dir / f"de_{tissue}.csv"))
        
        print(f"\n✓ {tissue} analysis complete!")
        print(f"  Significant genes: {len(sig_genes)}")
        if len(sig_genes) > 0:
            print(f"  Top 5 upregulated genes:")
            top_up = sig_genes[sig_genes['direction'] == 'up'].head(5)
            for _, row in top_up.iterrows():
                print(f"    - {row['gene']}: log2FC={row['logfoldchanges']:.2f}, p={row['pvals_adj']:.2e}")
    
    # Multi-tissue signature discovery
    print(f"\n\n{'='*80}")
    print("MULTI-TISSUE SIGNATURE DISCOVERY")
    print(f"{'='*80}")
    
    # Identify cross-tissue signatures
    cross_tissue_sigs = discoverer.identify_cross_tissue_signatures(
        tissue_de_results,
        min_tissues=2,
        direction_consistent=True
    )
    
    # Identify tissue-specific signatures
    tissue_specific_sigs = discoverer.identify_tissue_specific_signatures(
        tissue_de_results,
        cross_tissue_genes=cross_tissue_sigs['gene'].tolist() if len(cross_tissue_sigs) > 0 else []
    )
    
    # Save all signatures
    output_dir = project_root / "results" / "signatures"
    discoverer.save_signatures(cross_tissue_sigs, tissue_specific_sigs, str(output_dir))
    
    # Print summary
    print(f"\n\n{'='*80}")
    print("DISCOVERY SUMMARY")
    print(f"{'='*80}")
    
    print(f"\nCross-Tissue Signatures:")
    print(f"  Total: {len(cross_tissue_sigs)}")
    if len(cross_tissue_sigs) > 0:
        print(f"  Upregulated: {(cross_tissue_sigs['direction'] == 'up').sum()}")
        print(f"  Downregulated: {(cross_tissue_sigs['direction'] == 'down').sum()}")
        print(f"\n  Top 10 cross-tissue genes:")
        for i, row in cross_tissue_sigs.head(10).iterrows():
            print(f"    {i+1}. {row['gene']}")
            print(f"       - Tissues: {row['tissues']}")
            print(f"       - Avg log2FC: {row['avg_log2fc']:.2f}")
            print(f"       - Direction: {row['direction']}")
    
    print(f"\nTissue-Specific Signatures:")
    for tissue, sig_df in tissue_specific_sigs.items():
        print(f"  {tissue}: {len(sig_df)} genes")
    
    print(f"\n{'='*80}")
    print("✅ PIPELINE COMPLETE!")
    print(f"{'='*80}")
    print(f"\nResults saved to:")
    print(f"  - {project_root / 'results' / 'differential_expression'}")
    print(f"  - {project_root / 'results' / 'signatures'}")
    print()


if __name__ == "__main__":
    main()
