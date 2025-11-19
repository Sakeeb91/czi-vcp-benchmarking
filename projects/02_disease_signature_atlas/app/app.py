"""
Disease Signature Atlas - Interactive Dashboard

A Streamlit application for exploring COVID-19 disease signatures across tissues.
"""

import streamlit as st
import sys
from pathlib import Path

# Add project paths
project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root / "src"))
sys.path.append(str(project_root.parents[2] / "shared"))

# Page config
st.set_page_config(
    page_title="Disease Signature Atlas",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Main page
st.markdown('<div class="main-header">🧬 Disease Signature Atlas</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Multi-Tissue COVID-19 Signature Discovery</div>', unsafe_allow_html=True)

# Introduction
st.markdown("""
## Welcome!

This interactive dashboard explores **disease signatures** across multiple tissues using single-cell RNA-seq data 
from the [CELLxGENE Census](https://chanzuckerberg.github.io/cellxgene-census/).

### Project Overview

We analyzed COVID-19 vs Healthy cells across **Blood**, **Lung**, and **Heart** tissues to:
- 🔬 Identify differentially expressed genes
- 🧪 Discover cross-tissue signatures
- 🤖 Build machine learning classifiers
- 📊 Visualize multi-tissue patterns

### Key Findings

""")

# Metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Tissues Analyzed", "3", help="Blood, Lung, Heart")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("ML Model Accuracy", "95.5%", help="Blood tissue classifier")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Top Predictive Gene", "S100A8", help="Immune marker")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Navigation
st.markdown("""
### 📍 Navigation

Use the sidebar to explore different aspects of the analysis:

- **📊 Data Explorer**: Interactive UMAP visualization of cells
- **🧬 Gene Browser**: Search and visualize gene expression
- **🔬 Signatures**: View cross-tissue disease signatures
- **🤖 ML Predictor**: Explore the trained classifier

### 🚀 Getting Started

Click on any page in the sidebar to begin exploring!
""")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888;'>
    Built with Streamlit | Data from CELLxGENE Census | Phase 6 of Disease Signature Atlas Project
</div>
""", unsafe_allow_html=True)
