# Disease Signature Atlas - Dashboard

## Running the Dashboard

### Prerequisites
```bash
# Activate the environment
source venv-scanpy/bin/activate

# Install dashboard dependencies (if not already installed)
pip install streamlit plotly matplotlib-venn
```

### Launch
```bash
cd projects/02_disease_signature_atlas
streamlit run app/app.py
```

The dashboard will open in your browser at `http://localhost:8501`

## Dashboard Pages

1. **Home** - Project overview and key findings
2. **🤖 ML Predictor** - Explore the trained Random Forest model
3. **🧬 Gene Browser** - Search and visualize gene expression
4. **🔬 Signatures** - View cross-tissue disease signatures

## Features

- Interactive visualizations with Plotly
- Feature importance analysis
- Cross-tissue performance metrics
- Biological interpretation of results

## Data Requirements

For full functionality, ensure you have run:
```bash
python scripts/run_ml_validation.py
python scripts/run_multi_tissue_analysis.py
```

This will generate:
- `results/models/disease_classifier_rf.joblib`
- `results/figures/*.png`
