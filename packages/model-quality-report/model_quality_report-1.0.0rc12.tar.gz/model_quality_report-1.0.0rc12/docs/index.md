# Model Quality Report

## Metrics

The following metrics are computed as a result of model evaluation:

- Regression metrics:
    - explained_variance_score: [sklearn doc](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.explained_variance_score.html)
    - mean_absolute_error: [sklearn doc](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_absolute_error.html)
    - mean_squared_error: [sklearn doc](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html)
    - r2_score: [sklearn doc](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html)
    - median_absolute_error: $\text{med}\left|y_{true}-y_{pred}\right|$
    - mean_absolute_percentage_error: $\text{mean}\left|\left(y_{true}-y_{pred}\right)/y_{true}\right|$
    - median_absolute_percentage_error: $\text{med}\left|\left(y_{true}-y_{pred}\right)/y_{true}\right|$
    
- Classification metrics:
    - accuracy: [sklearn doc](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html)
    - precision: [sklearn doc](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html)
    - recall: [sklearn doc](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html)
