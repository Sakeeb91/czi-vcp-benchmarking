# CZI cz-benchmarks - Model Evaluation Guide

## Overview

**cz-benchmarks** is a Python package from the Chan Zuckerberg Initiative (in collaboration with NVIDIA) for standardized evaluation and comparison of machine learning models for biological applications.

### What it Does

- Provides **standardized benchmark tasks** for single-cell biology
- Enables **fair comparisons** between different AI models
- Includes **multiple metrics** per task (not just single scores)
- Supports **containerized model execution**
- Focuses on **biologically-relevant tasks**

### Initial Release (2025)

The initial release includes **6 benchmark tasks** contributed by CZI, NVIDIA, Allen Institute, and the single-cell community:

1. **Cell Clustering** - Group similar cells together
2. **Cell Type Classification** - Predict cell types from expression data
3. **Cross-Species Integration** - Align data across species
4. **Perturbation Expression Prediction** - Predict gene expression changes
5. **Sequential Ordering Assessment** - Determine cell trajectory order
6. **Cross-Species Disease Label Transfer** - Transfer disease labels across species

## Requirements

### System Requirements
- **Python 3.10 or higher** ⚠️ (Current system: Python 3.9.6)
- Recommended: 16+ GB RAM
- GPU recommended for model training

### Installation

#### Option 1: Upgrade Python (Recommended)

```bash
# Using pyenv
pyenv install 3.10.0
pyenv local 3.10.0

# Or using conda
conda create -n benchmarks python=3.10
conda activate benchmarks
```

#### Option 2: Create Virtual Environment with Python 3.10

```bash
# If you have Python 3.10 installed separately
python3.10 -m venv venv-benchmarks
source venv-benchmarks/bin/activate
```

#### Then Install cz-benchmarks

```bash
# From GitHub (latest development version)
pip install git+https://github.com/chanzuckerberg/cz-benchmarks.git

# Or wait for stable PyPI release
pip install cz-benchmarks  # When officially released
```

## Available Benchmark Tasks

### 1. Cell Type Classification

**Task**: Predict cell types from gene expression data

**Use Cases**:
- Compare different ML architectures (Random Forest, XGBoost, Neural Networks)
- Evaluate deep learning models (scGPT, scVI, scBERT)
- Test robustness across different tissues

**Metrics**:
- Accuracy
- F1 Score (macro, micro, weighted)
- Precision/Recall per cell type
- Confusion matrix

### 2. Cell Clustering

**Task**: Group similar cells without labels

**Use Cases**:
- Evaluate unsupervised learning algorithms
- Compare dimensionality reduction methods
- Test clustering stability

**Metrics**:
- Adjusted Rand Index (ARI)
- Normalized Mutual Information (NMI)
- Silhouette Score
- Davies-Bouldin Index

### 3. Cross-Species Integration

**Task**: Align gene expression data between human and mouse

**Use Cases**:
- Test transfer learning approaches
- Evaluate batch correction methods
- Compare integration algorithms

**Metrics**:
- Integration score
- Batch mixing score
- Cell type purity
- Conservation of biological variance

### 4. Perturbation Prediction

**Task**: Predict gene expression changes after perturbations (drugs, CRISPR, etc.)

**Use Cases**:
- Evaluate generative models
- Test causal inference methods
- Compare perturbation response predictors

**Metrics**:
- Mean Squared Error (MSE)
- Pearson Correlation
- R² Score
- Gene-wise accuracy

### 5. Sequential Ordering

**Task**: Order cells along developmental or disease trajectories

**Use Cases**:
- Evaluate trajectory inference methods
- Compare pseudotime algorithms
- Test temporal ordering models

**Metrics**:
- Kendall Tau correlation
- Spearman correlation
- Ordering accuracy

### 6. Cross-Species Disease Transfer

**Task**: Transfer disease labels between human and mouse models

**Use Cases**:
- Evaluate cross-species learning
- Test disease signature conservation
- Compare transfer learning methods

**Metrics**:
- Transfer accuracy
- Cross-species F1 score
- Label consistency

## Example Usage (Conceptual)

### Basic Workflow

```python
from cz_benchmarks import benchmark
from cz_benchmarks.tasks import CellTypeClassification
from cz_benchmarks.datasets import get_dataset
from cz_benchmarks.metrics import compute_metrics

# 1. Load a benchmark dataset
dataset = get_dataset(
    task="cell_type_classification",
    tissue="blood",
    species="homo_sapiens"
)

# 2. Define your model
class MyModel:
    def fit(self, X, y):
        # Your training code
        pass

    def predict(self, X):
        # Your prediction code
        pass

# 3. Run the benchmark
task = CellTypeClassification()
results = task.evaluate(
    model=MyModel(),
    dataset=dataset,
    metrics=["accuracy", "f1_macro", "f1_per_class"]
)

# 4. View results
print(results)
# {
#     'accuracy': 0.89,
#     'f1_macro': 0.87,
#     'f1_per_class': {...},
#     'confusion_matrix': [...]
# }
```

### Comparing Multiple Models

```python
from cz_benchmarks import compare_models

models = {
    "Random Forest": RandomForestClassifier(),
    "XGBoost": XGBClassifier(),
    "Neural Network": MLPClassifier(),
    "scGPT": scGPTModel()  # Hypothetical
}

# Run all models on the same task
comparison = compare_models(
    models=models,
    task="cell_type_classification",
    dataset=dataset,
    metrics=["accuracy", "f1_macro", "precision", "recall"]
)

# Generate comparison table
comparison.to_dataframe()
#             accuracy  f1_macro  precision  recall
# Random Forest   0.85      0.83       0.84    0.82
# XGBoost         0.88      0.86       0.87    0.85
# Neural Network  0.89      0.87       0.88    0.86
# scGPT          0.92      0.91       0.91    0.90

# Visualize results
comparison.plot()
```

### Robustness Testing

```python
from cz_benchmarks.robustness import test_robustness

# Test model across different conditions
robustness_results = test_robustness(
    model=my_model,
    task="cell_type_classification",
    tests=[
        "tissue_generalization",  # Test on different tissues
        "batch_effects",          # Test with batch variations
        "data_quality",           # Test with noisy data
        "sample_size"             # Test with varying data amounts
    ]
)

# View robustness scores
print(robustness_results.summary())
```

## Integration with CELLxGENE Census

The benchmarks can use data directly from the CELLxGENE Census:

```python
import cellxgene_census
from cz_benchmarks import load_benchmark_data

# Load benchmark data from Census
with cellxgene_census.open_soma(census_version="stable") as census:
    benchmark_data = load_benchmark_data(
        census=census,
        task="cell_type_classification",
        organism="homo_sapiens",
        tissues=["blood", "lung", "brain"]
    )

# Use for benchmarking
results = run_benchmark(
    model=my_model,
    data=benchmark_data
)
```

## Project Structure for Benchmarking

```
model-benchmarking/
├── README.md
├── requirements.txt
├── models/
│   ├── __init__.py
│   ├── baseline_models.py      # Simple baselines (RF, XGB)
│   ├── deep_learning.py        # Neural network models
│   └── foundation_models.py    # Pre-trained models
├── benchmarks/
│   ├── __init__.py
│   ├── run_all_benchmarks.py
│   ├── cell_type_classification.py
│   ├── clustering.py
│   └── perturbation_prediction.py
├── results/
│   ├── cell_type_results.csv
│   ├── clustering_results.csv
│   └── figures/
├── notebooks/
│   ├── 01_baseline_comparison.ipynb
│   ├── 02_robustness_testing.ipynb
│   └── 03_results_visualization.ipynb
└── configs/
    └── benchmark_config.yaml
```

## Resources

### Official Resources
- **Documentation**: https://chanzuckerberg.github.io/cz-benchmarks/
- **GitHub**: https://github.com/chanzuckerberg/cz-benchmarks
- **Virtual Cells Platform**: https://virtualcellmodels.cziscience.com/benchmarks
- **Contact**: virtualcellmodels@chanzuckerberg.com

### Related Tools
- **cellxgene-census**: For accessing training data
- **VCP CLI**: For dataset management (when released)
- **NVIDIA MONAI**: For imaging models
- **CodonFM**: RNA foundation model

### Community
- **CZI Science Slack**: https://czi.co/science-slack
- **GitHub Issues**: https://github.com/chanzuckerberg/cz-benchmarks/issues

## Current Status (November 2025)

- **Version**: 0.15.0 (Alpha)
- **Status**: Active development
- **Python**: Requires 3.10+
- **Focus**: Single-cell transcriptomics (with plans to expand)

## Next Steps

### To Use cz-benchmarks:

1. **Upgrade Python**
   ```bash
   # Check current version
   python3 --version

   # Install Python 3.10+ (using conda, pyenv, or system package manager)
   conda create -n benchmarks python=3.11
   conda activate benchmarks
   ```

2. **Install cz-benchmarks**
   ```bash
   pip install git+https://github.com/chanzuckerberg/cz-benchmarks.git
   ```

3. **Review Documentation**
   - Read the official docs: https://chanzuckerberg.github.io/cz-benchmarks/
   - Check example notebooks in the GitHub repo

4. **Start with Simple Benchmarks**
   - Begin with cell type classification
   - Use baseline models (Random Forest, Logistic Regression)
   - Gradually add more complex models

### Alternative: Use Without cz-benchmarks (For Now)

While waiting to upgrade Python, you can:

1. **Manually implement benchmarks** using scikit-learn metrics
2. **Use cellxgene-census** with current Python (3.9)
3. **Create your own evaluation framework**
4. **Document your approach** for future migration to cz-benchmarks

See the next section for a Python 3.9-compatible alternative.

## Python 3.9 Alternative (Current System)

Since cz-benchmarks requires Python 3.10+, here's how to do model benchmarking with your current setup:

```python
# This works with Python 3.9
import cellxgene_census
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, classification_report
from sklearn.model_selection import train_test_split
import pandas as pd

# Load data from Census
with cellxgene_census.open_soma(census_version="stable") as census:
    human = census["census_data"]["homo_sapiens"]

    # Get cell metadata and expression data
    # (See cellxgene-census docs for full implementation)

# Compare models manually
models = {
    "Random Forest": RandomForestClassifier(),
    "Logistic Regression": LogisticRegression()
}

results = []
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    results.append({
        "Model": name,
        "Accuracy": accuracy_score(y_test, y_pred),
        "F1 (macro)": f1_score(y_test, y_pred, average='macro')
    })

# Display results
results_df = pd.DataFrame(results)
print(results_df)
```

---

**Note**: This guide will be fully functional once Python is upgraded to 3.10 or higher. The conceptual examples show the intended usage patterns.
