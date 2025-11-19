# Disease Signature Atlas

## Multi-Tissue Disease Signature Discovery Using Single-Cell RNA-seq

This project discovers disease-specific gene signatures across multiple tissues using Scanpy and the CELLxGENE Census dataset.

## Overview

**Goal**: Identify disease-specific gene expression signatures across tissues (blood, lung, heart) for COVID-19 and other diseases.

**Approach**:
1. Load single-cell RNA-seq data from CELLxGENE Census
2. Quality control and preprocessing with Scanpy
3. Differential expression analysis (disease vs healthy)
4. Cross-tissue comparison
5. Machine learning validation
6. Interactive visualization dashboard

## Quick Start

```bash
cd "/Users/sakeeb/Code repositories/vcp dataset exploration"
```bash
cd "/Users/sakeeb/Code repositories/vcp dataset exploration"
# Use the Scanpy-compatible environment (Python 3.11)
source venv-scanpy/bin/activate
cd projects/02_disease_signature_atlas

# Test imports
python test_pipeline.py

# Run signature discovery pipeline (Phases 1-3)
python scripts/run_signature_discovery.py

# Run multi-tissue analysis (Phase 4)
python scripts/run_multi_tissue_analysis.py

# Run ML validation (Phase 5)
python scripts/run_ml_validation.py

# Launch interactive dashboard (Phase 6)
streamlit run app/app.py

# Or test data loading only
python scripts/download_data.py
```

## Status

**✅ Phases Complete**: 1-4 (Foundation, Scanpy, Signatures, Multi-Tissue)  
**🚧 In Progress**: Phase 5 (ML Validation)  
**📋 Planned**: Phase 6 (Dashboard), Phase 7 (Documentation)

## Project Structure

```
02_disease_signature_atlas/
├── README.md                    # This file
├── config.yaml                  # Project configuration
├── src/                         # Source code
│   ├── data/                    # Data loading & preprocessing
│   ├── analysis/                # Disease signature discovery
│   ├── models/                  # ML models
│   └── visualization/           # Plotting functions
├── notebooks/                   # Jupyter notebooks
├── results/                     # Outputs
│   ├── figures/                 # Plots
│   ├── signatures/              # Gene lists (CSV/JSON)
│   ├── models/                  # Trained models
│   └── reports/                 # Analysis summaries
├── scripts/                     # Executable scripts
└── app/                         # Streamlit dashboard
```

## Results Summary

### Disease Signatures Discovered

**Cross-tissue COVID-19 Signatures**:
- [ ] XX genes upregulated across all tissues
- [ ] YY genes tissue-specific 
- [ ] ZZ immune pathways enriched

### Classification Performance

| Tissue | Accuracy | F1-Score | Genes Used |
|--------|----------|----------|------------|
| Blood  | TBD      | TBD      | TBD        |
| Lung   | TBD      | TBD      | TBD        |
| Heart  | TBD      | TBD      | TBD        |

### Key Findings

_To be completed after analysis_

## Dependencies

See main repository `venv-benchmarks` environment:
- scanpy
- cellxgene-census
- scikit-learn
- streamlit
- plotly
- seaborn

## Configuration

Edit `config.yaml` to customize:
- Tissues to analyze
- Disease conditions
- Cell count limits
- Scanpy parameters

## Documentation

See [PROJECT_02_DISEASE_ATLAS_PLAN.md](../../docs/PROJECT_02_DISEASE_ATLAS_PLAN.md) for full implementation plan.

## Contact

Part of the VCP Dataset Exploration repository by Sakeeb Rahman
