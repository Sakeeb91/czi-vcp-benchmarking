# Quick Start: Model Benchmarking

## 🎯 Goal
Compare different AI/ML models on cell type prediction using CZI data.

## ⚡ Fastest Path (2 Minutes)

```bash
cd "/Users/sakeeb/Code repositories/vcp dataset exploration/model-benchmarking"

# Install dependencies
pip install scikit-learn xgboost

# Run benchmark
python benchmarks/cell_type_classification.py --max-cells 1000

# Check results
cat ../results/cell_type_classification_results.csv
```

## 📋 What You Get

- Model comparison (Random Forest, XGBoost, Logistic Regression, etc.)
- Performance metrics (Accuracy, F1-score, Training time)
- Results saved to CSV
- Ready to extend with your own models

## 🔧 Customize

### Different Tissue
```bash
python benchmarks/cell_type_classification.py --tissue lung
```

### More Cells
```bash
python benchmarks/cell_type_classification.py --max-cells 10000
```

### Specific Models Only
```bash
python benchmarks/cell_type_classification.py \
    --models random_forest xgboost
```

### Use PCA (faster)
```bash
python benchmarks/cell_type_classification.py \
    --use-pca --pca-components 50
```

### Cross-Validation
```bash
python benchmarks/cell_type_classification.py --use-cv
```

## 📊 Example Output

```
Model Performance on Cell Type Classification
=============================================
Dataset: Human Blood Cells (5,000 cells, 1,000 genes)

Model                  Accuracy    F1 (macro)   Training Time
-----------------------------------------------------------------
XGBoost               0.89        0.87         8.7s
Random Forest         0.87        0.85         12.3s
Logistic Regression   0.82        0.79         3.2s
Gradient Boosting     0.88        0.86         15.2s
Naive Bayes           0.79        0.76         1.1s
```

## 🚀 Next Steps

### Add Your Own Model

Edit `models/baseline_models.py`:

```python
class MyModel:
    def fit(self, X, y):
        # Your training code
        pass

    def predict(self, X):
        # Your prediction code
        return predictions

# Add to registry
models["My Custom Model"] = MyModel()
```

### Test Robustness

```python
# Test on different tissues
for tissue in ["blood", "lung", "brain"]:
    python benchmarks/cell_type_classification.py --tissue $tissue
```

### Upgrade to Official cz-benchmarks

When you have Python 3.10+:

```bash
conda create -n benchmarks python=3.10
conda activate benchmarks
pip install git+https://github.com/chanzuckerberg/cz-benchmarks.git

# Then use standardized benchmarks with community baselines
```

## 📚 Full Documentation

- **Comprehensive Guide**: [BENCHMARKING_GUIDE.md](BENCHMARKING_GUIDE.md)
- **Project README**: [model-benchmarking/README.md](model-benchmarking/README.md)
- **Summary**: [BENCHMARKING_SUMMARY.md](BENCHMARKING_SUMMARY.md)

## ❓ Common Issues

### Out of Memory
```bash
# Reduce cells and genes
python benchmarks/cell_type_classification.py \
    --max-cells 1000 --n-genes 500
```

### Slow Training
```bash
# Use PCA to reduce dimensions
python benchmarks/cell_type_classification.py --use-pca
```

### Want More Models
```bash
# Install additional packages
pip install lightgbm catboost
# Then add to models/baseline_models.py
```

---

**Start benchmarking in under 2 minutes! ⚡**
