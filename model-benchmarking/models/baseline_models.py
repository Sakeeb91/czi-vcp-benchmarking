"""
Baseline machine learning models for cell type classification.
"""

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from xgboost import XGBClassifier
from typing import Dict, Any


class ModelRegistry:
    """Registry of available baseline models."""

    @staticmethod
    def get_models(include_slow=False) -> Dict[str, Any]:
        """
        Get dictionary of model name to model instance.

        Parameters:
        -----------
        include_slow : bool
            Whether to include slow models like SVM

        Returns:
        --------
        Dict[str, model]
            Dictionary mapping model names to model instances
        """
        models = {
            "Random Forest": RandomForestClassifier(
                n_estimators=100,
                max_depth=20,
                min_samples_split=5,
                random_state=42,
                n_jobs=-1
            ),
            "XGBoost": XGBClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42,
                n_jobs=-1,
                tree_method='hist'  # Faster training
            ),
            "Logistic Regression": LogisticRegression(
                max_iter=1000,
                random_state=42,
                n_jobs=-1,
                solver='saga'  # Faster for large datasets
            ),
            "Gradient Boosting": GradientBoostingClassifier(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                random_state=42
            ),
            "Naive Bayes": GaussianNB()
        }

        if include_slow:
            models["SVM (RBF)"] = SVC(
                kernel='rbf',
                random_state=42,
                probability=True
            )
            models["SVM (Linear)"] = SVC(
                kernel='linear',
                random_state=42,
                probability=True
            )

        return models

    @staticmethod
    def get_model(name: str, **kwargs) -> Any:
        """
        Get a specific model by name with optional parameters.

        Parameters:
        -----------
        name : str
            Model name
        **kwargs
            Additional parameters to pass to model

        Returns:
        --------
        model
            Model instance
        """
        model_map = {
            "random_forest": RandomForestClassifier,
            "xgboost": XGBClassifier,
            "logistic": LogisticRegression,
            "gradient_boosting": GradientBoostingClassifier,
            "naive_bayes": GaussianNB,
            "svm_rbf": lambda **kw: SVC(kernel='rbf', **kw),
            "svm_linear": lambda **kw: SVC(kernel='linear', **kw)
        }

        if name.lower() not in model_map:
            raise ValueError(f"Unknown model: {name}. Available: {list(model_map.keys())}")

        return model_map[name.lower()](**kwargs)


def get_default_params(model_name: str) -> Dict[str, Any]:
    """
    Get default hyperparameters for a model.

    Parameters:
    -----------
    model_name : str
        Name of the model

    Returns:
    --------
    Dict[str, Any]
        Default hyperparameters
    """
    params = {
        "random_forest": {
            "n_estimators": 100,
            "max_depth": 20,
            "min_samples_split": 5,
            "random_state": 42,
            "n_jobs": -1
        },
        "xgboost": {
            "n_estimators": 100,
            "max_depth": 6,
            "learning_rate": 0.1,
            "random_state": 42,
            "n_jobs": -1,
            "tree_method": 'hist'
        },
        "logistic": {
            "max_iter": 1000,
            "random_state": 42,
            "n_jobs": -1,
            "solver": 'saga'
        },
        "gradient_boosting": {
            "n_estimators": 100,
            "max_depth": 5,
            "learning_rate": 0.1,
            "random_state": 42
        },
        "naive_bayes": {},
        "svm_rbf": {
            "kernel": 'rbf',
            "random_state": 42,
            "probability": True
        },
        "svm_linear": {
            "kernel": 'linear',
            "random_state": 42,
            "probability": True
        }
    }

    return params.get(model_name.lower(), {})
