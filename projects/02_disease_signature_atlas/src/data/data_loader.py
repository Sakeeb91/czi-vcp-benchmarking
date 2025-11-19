"""
Multi-tissue data loader for Disease Signature Atlas.

This module loads data for disease signature discovery across multiple tissues.
"""

import sys
import os
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import anndata as ad
import pandas as pd

# Add shared utilities to path
sys.path.insert(0, str(Path(__file__).parents[3] / "shared"))

from census_utils import load_census_data, load_multi_tissue_data, get_disease_info


class DiseaseDataLoader:
    """Loads disease and control data from CELLxGENE Census."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize loader with configuration.
        
        Parameters
        ----------
        config_path : str, optional
            Path to config.yaml. If None, uses default project config.
        """
        if config_path is None:
            config_path = Path(__file__).parents[2] / "config.yaml"
        
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.data_config = self.config['data']
        self.disease_config = self.config['diseases']
    
    def load_disease_data(
        self,
        disease_key: str = "covid19",
        tissues: Optional[List[str]] = None,
        max_cells_per_tissue: Optional[int] = None,
        verbose: bool = True
    ) -> Tuple[ad.AnnData, ad.AnnData, Dict]:
        """
        Load disease and control data for specified disease.
        """
        if disease_key not in self.disease_config:
            raise ValueError(f"Disease '{disease_key}' not found in config")
        
        disease_info = self.disease_config[disease_key]
        
        if tissues is None:
            tissues = disease_info.get('tissues', self.data_config['tissues'])
        
        if max_cells_per_tissue is None:
            max_cells_per_tissue = self.data_config['max_cells_per_tissue']
        
        organism = self.data_config['organism']
        census_version = self.data_config['census_version']
        
        # Build filters
        disease_filter_template = disease_info['disease_filter'] + " and tissue == '{tissue}' and is_primary_data == True"
        control_filter_template = disease_info['control_filter'] + " and tissue == '{tissue}' and is_primary_data == True"
        
        if verbose:
            print(f"\nLoading {disease_info['name']} data")
            print(f"Tissues: {', '.join(tissues)}")
        
        # Load disease data
        disease_data, disease_meta = load_multi_tissue_data(
            tissues=tissues,
            organism=organism,
            census_version=census_version,
            max_cells_per_tissue=max_cells_per_tissue,
            value_filter_template=disease_filter_template,
            verbose=verbose
        )
        
        # Load control data
        control_data, control_meta = load_multi_tissue_data(
            tissues=tissues,
            organism=organism,
            census_version=census_version,
            max_cells_per_tissue=max_cells_per_tissue,
            value_filter_template=control_filter_template,
            verbose=verbose
        )
        
        metadata = {
            'disease_key': disease_key,
            'disease_name': disease_info['name'],
            'tissues': tissues,
            'disease_cells': disease_data.n_obs,
            'control_cells': control_data.n_obs,
        }
        
        return disease_data, control_data, metadata


if __name__ == "__main__":
    loader = DiseaseDataLoader()
    disease_data, control_data, meta = loader.load_disease_data(
        tissues=["blood"],
        max_cells_per_tissue=1000
    )
    print(f"Disease data: {disease_data}")
    print(f"Control data: {control_data}")
