# Model Benchmarking Project

A practical project for comparing different AI/ML models on cell type prediction and other biological tasks using CZI CELLxGENE Census data.

## Current Status

This project works with **Python 3.9** (your current version). When you upgrade to Python 3.10+, you can migrate to use the official `cz-benchmarks` package.

## Project Goal

Compare different machine learning models on biological tasks:
- **Cell Type Classification**: Predict cell types from gene expression
- **Cell Clustering**: Unsupervised grouping of similar cells
- **Anomaly Detection**: Identify unusual cell states
- **Cross-Tissue Generalization**: Test model performance across tissues

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run baseline comparison
python benchmarks/cell_type_classification.py

# View results
open results/comparison_report.html
```

## Project Structure

```
model-benchmarking/
├── README.md                           # This file
├── requirements.txt                    # Dependencies
├── models/
│   ├── baseline_models.py             # Simple ML models (RF, XGB, SVM)
│   ├── neural_networks.py             # PyTorch/TensorFlow models
│   └── utils.py                       # Model utilities
├── benchmarks/
│   ├── cell_type_classification.py    # Main benchmark script
│   ├── clustering_benchmark.py        # Clustering evaluation
│   └── robustness_tests.py           # Test model robustness
├── results/
│   ├── cell_type_results.csv         # Benchmark results
│   └── figures/                      # Visualizations
├── notebooks/
│   └── model_comparison.ipynb        # Interactive analysis
└── configs/
    └── benchmark_config.yaml         # Configuration
```

## Available Models

### Baseline Models (Implemented)
- **Random Forest**: Ensemble tree-based classifier
- **XGBoost**: Gradient boosting classifier
- **Logistic Regression**: Linear classifier
- **Support Vector Machine**: SVM classifier

### Advanced Models (To Implement)
- **Multi-Layer Perceptron**: Simple neural network
- **Autoencoder + Classifier**: Dimensionality reduction + classification
- **Transfer Learning**: Pre-trained embeddings + classifier

## Benchmark Tasks

### 1. Cell Type Classification
- **Dataset**: Human blood cells from Census
- **Task**: Predict cell type from gene expression
- **Metrics**: Accuracy, F1-score, Precision, Recall
- **Cross-validation**: 5-fold CV

### 2. Cross-Tissue Generalization
- **Train**: Blood cells
- **Test**: Lung, brain, heart cells
- **Metrics**: Transfer accuracy, generalization gap

### 3. Robustness Testing
- **Noise**: Add Gaussian noise to expression data
- **Missing Data**: Randomly mask gene values
- **Batch Effects**: Simulate technical variations

### 4. Sample Efficiency
- **Test**: Model performance with varying training sizes
- **Sizes**: 100, 500, 1000, 5000, 10000 cells
- **Metrics**: Learning curves

## Running Benchmarks

### Basic Comparison

```bash
python benchmarks/cell_type_classification.py \
    --max-cells 10000 \
    --tissues blood lung brain \
    --models random_forest xgboost logistic_regression
```

### Robustness Testing

```bash
python benchmarks/robustness_tests.py \
    --model random_forest \
    --noise-levels 0.0 0.1 0.2 0.5
```

### Generate Report

```bash
python benchmarks/generate_report.py \
    --input results/cell_type_results.csv \
    --output results/comparison_report.html
```

## Example Results

```
Model Performance on Cell Type Classification
=============================================
Dataset: Human Blood Cells (10,000 cells, 5,000 genes)

Model                  Accuracy    F1 (macro)   Training Time
-----------------------------------------------------------------
Random Forest          0.87        0.85         12.3s
XGBoost               0.89        0.87         8.7s
Logistic Regression   0.82        0.79         3.2s
SVM                   0.85        0.83         45.6s

Cross-Tissue Generalization:
  Blood → Lung:   0.72 accuracy
  Blood → Brain:  0.65 accuracy
  Blood → Heart:  0.68 accuracy
```

## Migration to cz-benchmarks

When you upgrade to Python 3.10+:

1. **Install cz-benchmarks**
   ```bash
   pip install git+https://github.com/chanzuckerberg/cz-benchmarks.git
   ```

2. **Update benchmark scripts** to use official API
3. **Access standardized datasets** and metrics
4. **Compare with community baselines**

## Dependencies

- cellxgene-census (for data)
- scikit-learn (ML models)
- xgboost (gradient boosting)
- pandas, numpy (data manipulation)
- matplotlib, seaborn (visualization)
- Optional: pytorch, tensorflow (deep learning)

## Next Steps

1. Run the baseline comparison
2. Review results and visualizations
3. Implement additional models
4. Test on different tissues/organisms
5. Add custom evaluation metrics
6. Create interactive dashboard

## Resources

- **Data Source**: CELLxGENE Census
- **Future Benchmarks**: cz-benchmarks (Python 3.10+)
- **Documentation**: See [BENCHMARKING_GUIDE.md](../BENCHMARKING_GUIDE.md)
