# Disease Signature Finder with Multi-Tissue Analysis

## Project Overview

Create a comprehensive systems biology project that discovers disease-specific gene signatures across multiple tissues using Scanpy and CELLxGENE Census data. This project will combine biological discovery, machine learning, and interactive visualization to create a portfolio showcase piece.

## Repository Strategy

### Recommended Approach: Same Repository, New Project Directory

**Location**: `/Users/sakeeb/Code repositories/vcp dataset exploration/projects/02_disease_signature_atlas/`

### Why This Approach?

1. **Code Reuse**: Leverage existing data loading utilities from `01_cell_type_classifier`
2. **Unified Portfolio**: One repository showcasing progressive complexity
3. **Shared Infrastructure**: Use existing virtual environment and dependencies
4. **Professional Narrative**: Shows project evolution and systems thinking

---

## Proposed Repository Structure

```
vcp-dataset-exploration/
├── projects/
│   ├── 01_cell_type_classifier/          # Existing project
│   │   ├── data_loader.py
│   │   ├── model.py
│   │   └── main.py
│   │
│   └── 02_disease_signature_atlas/       # NEW PROJECT
│       ├── README.md                     # Project overview & results
│       ├── config.yaml                   # Configuration file
│       │
│       ├── src/
│       │   ├── __init__.py
│       │   ├── data/
│       │   │   ├── __init__.py
│       │   │   ├── data_loader.py       # Multi-tissue data loading
│       │   │   └── preprocessing.py     # Scanpy preprocessing pipeline
│       │   │
│       │   ├── analysis/
│       │   │   ├── __init__.py
│       │   │   ├── differential_expression.py  # DE analysis
│       │   │   ├── signature_discovery.py      # Disease signatures
│       │   │   ├── pathway_enrichment.py       # GO/KEGG enrichment
│       │   │   └── cross_tissue_analysis.py    # Multi-tissue comparison
│       │   │
│       │   ├── models/
│       │   │   ├── __init__.py
│       │   │   ├── classifiers.py       # ML models using signatures
│       │   │   └── evaluation.py        # Model evaluation
│       │   │
│       │   └── visualization/
│       │       ├── __init__.py
│       │       ├── scanpy_plots.py      # Scanpy visualizations
│       │       ├── custom_plots.py      # Custom multi-tissue plots
│       │       └── dashboard.py         # Streamlit dashboard
│       │
│       ├── notebooks/
│       │   ├── 01_data_exploration.ipynb
│       │   ├── 02_quality_control.ipynb
│       │   ├── 03_disease_signature_discovery.ipynb
│       │   ├── 04_multi_tissue_comparison.ipynb
│       │   └── 05_ml_validation.ipynb
│       │
│       ├── results/
│       │   ├── figures/                  # Publication-quality plots
│       │   ├── signatures/               # Discovered gene signatures (CSV/JSON)
│       │   ├── models/                   # Trained models
│       │   └── reports/                  # Analysis summaries
│       │
│       ├── scripts/
│       │   ├── run_full_pipeline.py     # End-to-end pipeline
│       │   ├── download_data.py         # Data acquisition
│       │   └── generate_report.py       # Auto-generate report
│       │
│       ├── tests/
│       │   └── test_analysis.py         # Unit tests
│       │
│       └── app/
│           └── streamlit_app.py         # Interactive dashboard
│
├── shared/                               # NEW: Shared utilities
│   ├── __init__.py
│   ├── census_utils.py                  # Common Census functions
│   ├── plotting_utils.py                # Shared plotting functions
│   └── config.py                        # Global configuration
│
└── docs/
    ├── README_MAIN.md                   # Main repo README
    └── PROJECT_02_GUIDE.md              # NEW: Disease atlas guide
```

---

## Implementation Phases

### Phase 1: Foundation (Week 1)
**Goal**: Set up project structure and data pipeline

- [ ] Create `projects/02_disease_signature_atlas/` directory structure
- [ ] Create `shared/` directory for reusable code
- [ ] Refactor `data_loader.py` from project 01 into `shared/census_utils.py`
- [ ] Write `config.yaml` with tissue/disease parameters
- [ ] Set up data loading for multiple tissues

### Phase 2: Scanpy Integration (Week 2)
**Goal**: Implement Scanpy preprocessing pipeline

- [ ] Create `preprocessing.py` with Scanpy QC pipeline
- [ ] Implement normalization, scaling, HVG selection
- [ ] Add dimensionality reduction (PCA, UMAP)
- [ ] Create quality control visualizations
- [ ] Test on single tissue first

### Phase 3: Disease Signature Discovery (Week 2-3)
**Goal**: Find disease-specific gene signatures

- [ ] Implement differential expression analysis (`differential_expression.py`)
- [ ] Compare disease vs healthy across tissues
- [ ] Identify cross-tissue signatures (`cross_tissue_analysis.py`)
- [ ] Validate with pathway enrichment
- [ ] Export signature gene lists

### Phase 4: Multi-Tissue Analysis (Week 3-4)
**Goal**: Compare disease responses across tissues

- [ ] Integrate data from 3-5 tissues
- [ ] Identify shared vs tissue-specific signatures
- [ ] Create comparative visualizations
- [ ] Build cross-tissue correlation analysis
- [ ] Generate heatmaps and network plots

### Phase 5: Machine Learning Validation (Week 4-5)
**Goal**: Build predictive models using discovered signatures

- [ ] Create classifiers using signature genes
- [ ] Test cross-tissue generalization
- [ ] Compare to using all genes
- [ ] Evaluate model interpretability
- [ ] Benchmark against literature

### Phase 6: Visualization & Dashboard (Week 5-6)
**Goal**: Create interactive exploration tools

- [ ] Build Streamlit dashboard
- [ ] Add interactive UMAP explorer
- [ ] Create signature comparison tool
- [ ] Add gene expression browser
- [ ] Deploy locally (document deployment)

### Phase 7: Documentation & Polish (Week 6)
**Goal**: Make portfolio-ready

- [ ] Write comprehensive README with results
- [ ] Create project walkthrough notebook
- [ ] Generate publication-quality figures
- [ ] Write analysis report
- [ ] Update main repo README

---

## Key Design Decisions

### 1. **Shared Code Strategy**

**Extract common utilities to `shared/`**:
- Avoids code duplication between projects
- Shows software engineering best practices
- Makes future projects easier

**Example Migration**:
```python
# Before: projects/01_cell_type_classifier/data_loader.py
def load_census_data(...):
    # specific implementation

# After: shared/census_utils.py (generalized)
def load_census_data(...):
    # flexible implementation for multiple use cases

# projects/02_disease_signature_atlas/src/data/data_loader.py
from shared.census_utils import load_census_data
```

### 2. **Configuration Management**

Use `config.yaml` for all parameters:
```yaml
data:
  tissues: ["blood", "lung", "heart", "brain", "liver"]
  organism: "homo_sapiens"
  max_cells_per_tissue: 10000
  
diseases:
  covid19:
    disease_filter: "disease == 'COVID-19'"
    control_filter: "disease == 'normal'"
  
scanpy:
  min_genes: 200
  min_cells: 3
  mt_percent_threshold: 20
  n_hvgs: 2000
  n_pcs: 50
```

### 3. **Modular Analysis Pipeline**

Each analysis step is independent:
- Can run individually for testing
- Easy to swap methods
- Clear dependencies

---

## Target Diseases & Tissues

### Recommended Starting Point

**Disease**: COVID-19 (well-studied, good data availability)

**Tissues** (in order of priority):
1. **Blood** - Immune response, most cells available
2. **Lung** - Primary infection site
3. **Heart** - Known complications
4. **Brain** - Neurological effects (optional)
5. **Liver** - Systemic effects (optional)

**Why COVID-19?**:
- ✅ Large datasets available
- ✅ Multi-tissue effects documented
- ✅ Clear disease vs control
- ✅ Literature for validation
- ✅ Clinically relevant

### Alternative Diseases
- **Cancer** (multiple types)
- **Alzheimer's** (brain-focused)
- **Inflammatory bowel disease** (gut-focused)
- **Type 2 diabetes** (pancreas, blood)

---

## Dependencies to Add

Update your `venv-benchmarks` environment:

```bash
pip install scanpy
pip install scvelo  # For trajectory analysis (optional)
pip install gprofiler-official  # For pathway enrichment
pip install streamlit  # For dashboard
pip install plotly  # For interactive plots
pip install seaborn  # For better heatmaps
pip install statannot  # For statistical annotations
pip install adjustText  # For better plot labels
```

---

## Success Metrics

### Technical Metrics
- [ ] Process 50,000+ cells across 3+ tissues
- [ ] Identify 100+ differentially expressed genes
- [ ] Achieve >85% classification accuracy using signatures
- [ ] Generate 15+ publication-quality figures

### Portfolio Metrics
- [ ] Comprehensive README with clear results
- [ ] Working Streamlit dashboard
- [ ] Clean, documented code
- [ ] Reproducible pipeline
- [ ] Biological insights documented

### Biological Metrics
- [ ] Discovery of cross-tissue disease signatures
- [ ] Validation against published literature
- [ ] Pathway enrichment showing relevant biology
- [ ] Novel observations or hypotheses

---

## Timeline

**Fast Track (4 weeks)**:
- Focus on 2 tissues (blood, lung)
- Basic ML validation
- Essential visualizations

**Standard (6 weeks)**:
- 3-4 tissues
- Full ML pipeline
- Streamlit dashboard

**Portfolio Showcase (8-10 weeks)**:
- 5 tissues
- Advanced trajectory analysis
- Publication-quality everything
- Potential manuscript

---

## Next Steps

1. **Review this plan** - Adjust based on your timeline
2. **Choose disease & tissues** - Start with COVID-19 + blood/lung
3. **Create project structure** - Set up directories
4. **Migrate shared code** - Extract from project 01
5. **Start Phase 1** - Data loading and exploration

---

## Additional Considerations

### When to Split Into Separate Repo

**Consider separate repo if**:
- Project becomes publication-quality (create `disease-atlas-paper` repo)
- You want to showcase JUST this project
- Repository becomes too large (>1GB)
- Different collaborators/audience

**Best of both worlds**:
- Keep development in this repo
- Create showcase repo later with just the polished project
- Link between repos in READMEs

### Future Extensions

Once complete, this project can spawn:
- Individual disease-specific deep dives
- Method comparison papers
- Web application deployment
- Integration with external databases
- Collaboration opportunities
