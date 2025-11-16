"""
Utility functions for model training and evaluation.
"""

from sklearn.model_selection import cross_val_score, cross_validate
from sklearn.metrics import (
    accuracy_score, f1_score, precision_score, recall_score,
    classification_report, confusion_matrix
)
import numpy as np
import pandas as pd
from typing import Dict, Any, List
import time


def evaluate_model(model, X_train, X_test, y_train, y_test, model_name="Model") -> Dict[str, Any]:
    """
    Train and evaluate a model.

    Parameters:
    -----------
    model : sklearn model
        Model to evaluate
    X_train, X_test : array-like
        Training and test features
    y_train, y_test : array-like
        Training and test labels
    model_name : str
        Name of the model for reporting

    Returns:
    --------
    Dict[str, Any]
        Evaluation metrics
    """
    # Train
    start_time = time.time()
    model.fit(X_train, y_train)
    training_time = time.time() - start_time

    # Predict
    start_time = time.time()
    y_pred = model.predict(X_test)
    inference_time = time.time() - start_time

    # Compute metrics
    results = {
        "model": model_name,
        "accuracy": accuracy_score(y_test, y_pred),
        "f1_macro": f1_score(y_test, y_pred, average='macro', zero_division=0),
        "f1_weighted": f1_score(y_test, y_pred, average='weighted', zero_division=0),
        "precision_macro": precision_score(y_test, y_pred, average='macro', zero_division=0),
        "recall_macro": recall_score(y_test, y_pred, average='macro', zero_division=0),
        "training_time": training_time,
        "inference_time": inference_time,
        "n_train": len(X_train),
        "n_test": len(X_test)
    }

    return results


def cross_validate_model(model, X, y, cv=5, model_name="Model") -> Dict[str, Any]:
    """
    Perform cross-validation on a model.

    Parameters:
    -----------
    model : sklearn model
        Model to evaluate
    X, y : array-like
        Features and labels
    cv : int
        Number of cross-validation folds
    model_name : str
        Name of the model

    Returns:
    --------
    Dict[str, Any]
        Cross-validation results
    """
    scoring = ['accuracy', 'f1_macro', 'precision_macro', 'recall_macro']

    start_time = time.time()
    cv_results = cross_validate(
        model, X, y,
        cv=cv,
        scoring=scoring,
        return_train_score=True,
        n_jobs=-1
    )
    cv_time = time.time() - start_time

    results = {
        "model": model_name,
        "cv_folds": cv,
        "accuracy_mean": cv_results['test_accuracy'].mean(),
        "accuracy_std": cv_results['test_accuracy'].std(),
        "f1_macro_mean": cv_results['test_f1_macro'].mean(),
        "f1_macro_std": cv_results['test_f1_macro'].std(),
        "precision_mean": cv_results['test_precision_macro'].mean(),
        "recall_mean": cv_results['test_recall_macro'].mean(),
        "cv_time": cv_time
    }

    return results


def get_classification_report(y_true, y_pred, target_names=None) -> pd.DataFrame:
    """
    Generate detailed classification report.

    Parameters:
    -----------
    y_true : array-like
        True labels
    y_pred : array-like
        Predicted labels
    target_names : list, optional
        Class names

    Returns:
    --------
    pd.DataFrame
        Classification report as DataFrame
    """
    report = classification_report(
        y_true, y_pred,
        target_names=target_names,
        output_dict=True,
        zero_division=0
    )

    return pd.DataFrame(report).transpose()


def compare_models(
    models: Dict[str, Any],
    X_train, X_test, y_train, y_test,
    use_cv=False,
    cv=5
) -> pd.DataFrame:
    """
    Compare multiple models.

    Parameters:
    -----------
    models : Dict[str, model]
        Dictionary of model name to model instance
    X_train, X_test : array-like
        Training and test features
    y_train, y_test : array-like
        Training and test labels
    use_cv : bool
        Whether to use cross-validation instead of train/test split
    cv : int
        Number of CV folds if use_cv=True

    Returns:
    --------
    pd.DataFrame
        Comparison results
    """
    results = []

    for name, model in models.items():
        print(f"Evaluating {name}...")

        try:
            if use_cv:
                # Combine train and test for CV
                X = np.vstack([X_train, X_test])
                y = np.concatenate([y_train, y_test])
                result = cross_validate_model(model, X, y, cv=cv, model_name=name)
            else:
                result = evaluate_model(
                    model, X_train, X_test, y_train, y_test, model_name=name
                )

            results.append(result)
            print(f"  ✓ {name} completed")

        except Exception as e:
            print(f"  ✗ {name} failed: {e}")
            results.append({
                "model": name,
                "error": str(e)
            })

    return pd.DataFrame(results)


def test_sample_efficiency(
    model_class,
    X, y,
    sample_sizes: List[int],
    test_size=0.2,
    n_repeats=3
) -> pd.DataFrame:
    """
    Test model performance with varying training set sizes.

    Parameters:
    -----------
    model_class : class
        Model class to instantiate
    X, y : array-like
        Full dataset
    sample_sizes : List[int]
        List of training set sizes to test
    test_size : float
        Fraction of data to use for testing
    n_repeats : int
        Number of times to repeat each experiment

    Returns:
    --------
    pd.DataFrame
        Results for each sample size
    """
    from sklearn.model_selection import train_test_split

    results = []

    for size in sample_sizes:
        for repeat in range(n_repeats):
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, train_size=size, test_size=test_size, random_state=repeat
            )

            # Train and evaluate
            model = model_class()
            start = time.time()
            model.fit(X_train, y_train)
            train_time = time.time() - start

            y_pred = model.predict(X_test)
            acc = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred, average='macro', zero_division=0)

            results.append({
                "sample_size": size,
                "repeat": repeat,
                "accuracy": acc,
                "f1_macro": f1,
                "training_time": train_time
            })

    return pd.DataFrame(results)
