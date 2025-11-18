# ✅ cz-benchmarks Successfully Installed!

## What You Now Have

### Python Versions
- **Global Python**: Python 3.14.0 (latest, at `/opt/homebrew/bin/python3`)
- **Benchmarks Python**: Python 3.13.9 (in virtual environment)

### Virtual Environment
- **Location**: `/Users/sakeeb/Code repositories/vcp dataset exploration/venv-benchmarks`
- **Python**: 3.13.9
- **cz-benchmarks**: 0.15.0 (latest from GitHub)
- **Status**: ✅ Fully functional!

## How to Use

### Activate the Virtual Environment

Every time you want to use cz-benchmarks:

```bash
cd "/Users/sakeeb/Code repositories/vcp dataset exploration"
source venv-benchmarks/bin/activate
```

You'll see `(venv-benchmarks)` in your prompt.

### Verify Installation

```bash
python -c "import czbenchmarks; print('✓ cz-benchmarks is installed and working!')"
```

Expected output: `✓ cz-benchmarks is installed and working!`

**Note**: Import as `czbenchmarks` (no underscore), not `cz_benchmarks`

### Deactivate When Done

```bash
deactivate
```

## Quick Start with cz-benchmarks

### Example: Cell Type Classification Benchmark

```python
import czbenchmarks
# Note: The package name is czbenchmarks (no underscore)
import cellxgene_census

# Activate the environment first!
# cd "/Users/sakeeb/Code repositories/vcp dataset exploration"
# source venv-benchmarks/bin/activate

# Your model code here
class MyModel:
    def fit(self, X, y):
        # Training logic
        pass

    def predict(self, X):
        # Prediction logic
        return predictions

# Run benchmark
task = CellTypeClassification()
results = task.evaluate(
    model=MyModel(),
    dataset="standard",  # Use cz-benchmarks standard dataset
    metrics=["accuracy", "f1_macro", "precision", "recall"]
)

print(results)
```

## Project Structure

```
vcp dataset exploration/
├── venv-benchmarks/              # Python 3.13 environment (cz-benchmarks)
├── venv-python314/               # Python 3.14 environment (for other uses)
├── model-benchmarking/           # Your manual benchmarking project (Python 3.9 compatible)
├── starter-project/              # Cell type analysis project
└── (documentation files)
```

## What's Installed in venv-benchmarks

All official dependencies:
- ✅ cz-benchmarks 0.15.0
- ✅ cellxgene-census (if needed, install with: `pip install cellxgene-census`)
- ✅ scanpy 1.11.5
- ✅ anndata 0.12.6
- ✅ scikit-learn 1.7.2
- ✅ numpy 2.3.4
- ✅ pandas 2.3.3
- ✅ And all other dependencies

## Available Benchmark Tasks

When using cz-benchmarks, you have access to **6 standardized tasks**:

1. **Cell Type Classification**
   ```python
   from cz_benchmarks.tasks import CellTypeClassification
   ```

2. **Cell Clustering**
   ```python
   from cz_benchmarks.tasks import CellClustering
   ```

3. **Cross-Species Integration**
   ```python
   from cz_benchmarks.tasks import CrossSpeciesIntegration
   ```

4. **Perturbation Prediction**
   ```python
   from cz_benchmarks.tasks import PerturbationPrediction
   ```

5. **Sequential Ordering**
   ```python
   from cz_benchmarks.tasks import SequentialOrdering
   ```

6. **Cross-Species Disease Transfer**
   ```python
   from cz_benchmarks.tasks import DiseaseTransfer
   ```

## Example Workflow

```bash
# 1. Activate environment
cd "/Users/sakeeb/Code repositories/vcp dataset exploration"
source venv-benchmarks/bin/activate

# 2. Create a benchmark script
cat > test_benchmark.py << 'EOF'
import cz_benchmarks
print(f"cz-benchmarks version: {cz_benchmarks.__version__}")
print("Available tasks:")
# List available tasks
EOF

# 3. Run it
python test_benchmark.py

# 4. Deactivate when done
deactivate
```

## Comparison: Two Options Now Available

### Option 1: Manual Benchmarking (Works with any Python)
**Location**: `model-benchmarking/`
- ✅ Works with Python 3.9 (your system Python)
- ✅ Manual metric implementation
- ✅ Flexible and customizable
- ✅ No virtual environment needed
- ❌ Not standardized with community

```bash
cd model-benchmarking
python benchmarks/cell_type_classification.py
```

### Option 2: Official cz-benchmarks (NEW!)
**Location**: `venv-benchmarks/`
- ✅ Requires Python 3.13 (in virtual environment)
- ✅ Official CZI + NVIDIA package
- ✅ Standardized tasks and metrics
- ✅ Community baselines
- ✅ Regular updates
- ⚠️ Requires activation of virtual environment

```bash
source venv-benchmarks/bin/activate
python your_benchmark_script.py
```

## Next Steps

### 1. Read the Official Documentation
```bash
# Open in browser
open https://chanzuckerberg.github.io/cz-benchmarks/
```

### 2. Check Available Examples
```bash
# Explore example notebooks on GitHub
open https://github.com/chanzuckerberg/cz-benchmarks
```

### 3. Try Your First Benchmark
Create a simple test script following the examples in the documentation.

### 4. Integrate with CELLxGENE Census
```bash
# Install census in the benchmark environment
source venv-benchmarks/bin/activate
pip install cellxgene-census
```

## Troubleshooting

### Environment Not Found
```bash
# Make sure you're in the right directory
cd "/Users/sakeeb/Code repositories/vcp dataset exploration"

# Verify the environment exists
ls -la venv-benchmarks/
```

### Import Errors
```bash
# Make sure environment is activated
source venv-benchmarks/bin/activate

# Verify Python version
python --version  # Should be 3.13.9

# Verify cz-benchmarks is installed
pip list | grep cz-benchmarks

# Test import (use czbenchmarks, not cz_benchmarks!)
python -c "import czbenchmarks; print('Success!')"
```

**Important**: The package imports as `czbenchmarks` (no underscore), not `cz_benchmarks`

### Need Different Python for Other Projects
Use the Python 3.14 environment:
```bash
source venv-python314/bin/activate
# This has Python 3.14 but NOT cz-benchmarks (dependency issues)
```

Or use system Python 3.9:
```bash
# No activation needed - just use python3 directly
python3 --version  # Will show system Python
```

## Resources

- **Documentation**: [BENCHMARKING_GUIDE.md](BENCHMARKING_GUIDE.md)
- **Quick Start**: [QUICK_START_BENCHMARKING.md](QUICK_START_BENCHMARKING.md)
- **Summary**: [BENCHMARKING_SUMMARY.md](BENCHMARKING_SUMMARY.md)
- **Official Docs**: https://chanzuckerberg.github.io/cz-benchmarks/
- **GitHub**: https://github.com/chanzuckerberg/cz-benchmarks

---

**You're ready to use official cz-benchmarks! 🚀**

**Remember**: Always activate the virtual environment first!
```bash
source venv-benchmarks/bin/activate
```
