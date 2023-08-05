import numpy as np
import pandas as pd
from sklearn.metrics import (
    explained_variance_score,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    accuracy_score,
    precision_score,
    recall_score,
)


def _explained_variance_score(y_true: pd.Series, y_pred: pd.Series) -> float:
    return explained_variance_score(y_true, y_pred)


def _mean_absolute_error(y_true: pd.Series, y_pred: pd.Series) -> float:
    return mean_absolute_error(y_true, y_pred)


def _mean_squared_error(y_true: pd.Series, y_pred: pd.Series) -> float:
    return mean_squared_error(y_true, y_pred)


def _median_absolute_error(y_true: pd.Series, y_pred: pd.Series) -> float:
    return float(np.median(np.abs(y_pred - y_true)))


def _r2_score(y_true: pd.Series, y_pred: pd.Series) -> float:
    if y_true.shape[0] >= 2:
        return r2_score(y_true, y_pred)
    else:
        return np.nan


def _mean_absolute_percentage_error(y_true: pd.Series, y_pred: pd.Series) -> float:
    return float(np.mean(np.abs((y_true - y_pred) / y_true)))


def _median_absolute_percentage_error(y_true: pd.Series, y_pred: pd.Series) -> float:
    return float(np.median(np.abs((y_true - y_pred) / y_true)))


def _accuracy(y_true: pd.Series, y_pred: pd.Series) -> float:
    try:
        return accuracy_score(y_true=y_true, y_pred=y_pred, normalize=True)
    except ValueError:
        return np.nan


def _precision(y_true: pd.Series, y_pred: pd.Series) -> float:
    try:
        return precision_score(y_true=y_true, y_pred=y_pred, zero_division=0)
    except ValueError:
        return np.nan


def _recall(y_true: pd.Series, y_pred: pd.Series) -> float:
    try:
        return recall_score(y_true=y_true, y_pred=y_pred, zero_division=0)
    except ValueError:
        return np.nan


regression_quality_metrics = {
    "explained_variance_score": _explained_variance_score,
    "mean_absolute_error": _mean_absolute_error,
    "mean_squared_error": _mean_squared_error,
    "median_absolute_error": _median_absolute_error,
    "r2_score": _r2_score,
    "mean_absolute_percentage_error": _mean_absolute_percentage_error,
    "median_absolute_percentage_error": _median_absolute_percentage_error,
}

classification_quality_metrics = {"accuracy": _accuracy, "precision": _precision, "recall": _recall}


all_quality_metrics = {**regression_quality_metrics, **classification_quality_metrics}
