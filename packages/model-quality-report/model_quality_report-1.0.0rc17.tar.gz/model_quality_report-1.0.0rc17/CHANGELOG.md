# Changelog

## 1.0.0rc17 (2021-07-10)
### Added
- Run `create_reports()` in parallel Using `joblib` if the argument `n_jobs` in initialization of `ModelComparisonReport` is not `None` (see more in [`joblib.Parallel`](https://joblib.readthedocs.io/en/latest/generated/joblib.Parallel.html) documentation).

## 1.0.0rc16 (2021-07-08)
### Fixed
- Quality metrics with division in the formula now return `np.nan` in case of `ZeroDivisionError`. 

## 1.0.0rc14 (2021-07-07)
### Fixed
- Catch `TypeError` exceptions in metrics.

## 1.0.0rc13 (2021-07-07)
### Added
- New metrics: `mean_error`, `median_error`, `mean_sign_error`, `mean_percentage_error`, `median_percentage_error`, `mean_absolute_cum_error`, `median_absolute_cum_error`, `mean_absolute_percentage_cum_error`, `median_absolute_percentage_cum_error`, `mean_sign_cum_error`.

## 1.0.0rc12 (2021-07-06)
### Added
- Accuracy, precision, recall metrics for classification problems.
### Changed
- Quality metrics callables are organized into the dictionary name/metric `all_quality_metrics` in `model_quality_report.quality_metrics` to make easier looping over all metrics and accessing them by name. Regression metrics are accessible separately from `regression_quality_metrics` dictionary in the same module, while classification metrics are stored in `classification_quality_metrics` dictionary.

## 1.0.0rc10 (2021-06-14)
### Added
- Logging to `model_quality_report.model_comparison_report.ModelComparisonReport` and `model_quality_report.quality_report.base.QualityReportBase`.

## 1.0.0rc9 (2021-05-17)
### Changed
- Method `create_reports` of `model_quality_report.model_comparison_report.ModelComparisonReport` returns a list of dictionaries `ModelComparisonReportType` that contain experiment key, quality report, and errors string.

## 1.0.0rc8 (2021-05-11)
### Added
- Method `get_true_and_predicted_data` in `model_quality_report.model_comparison_report.ModelComparisonReport` which returns a single DataFrame with true and predicted data collected from all quality reports.

## 1.0.0rc7 (2021-05-10)
### Changed
- Refactor `ModelComparisonReport`. It takes four lists of equal size: `QualityReportBase` instances, `X_data_list`, `y_data_list`, and flat dictionaries `experiment_keys`. The class now has only two public methods:
  - `create_reports` that simply returns the list quality reports for each experiment, and
  - `get_metrics` that extracts a single metrics DataFrame from multiple quality reports obtained above. The resulting DataFrame has experiment keys in corresponding columns. 
### Removed
- Methods `set_model`, `get_model`, `set_splitter`, `get_splitter` from quality report classes.

## 1.0.0rc6 (2021-05-05)
### Changed
- Rename `create_quality_report_and_return_dict` method of quality report to `create_quality_report`. Now it still returns a dictionary, but the data and metrics values are pandas `DataFrame` objects.
- Rename `metrics_to_frame` method  of quality report to `get_metrics`.

## 1.0.0rc5 (2021-04-29)
### Changed
- Drop missing observations from either actual or predicted series after merging them and before computing quality metrics in `CrossValidationTimeSeriesQualityReport`. This permits actual and predicted series to be not aligned in case a model produces forecasts of a different length than `y_test`. 

## 1.0.0rc4 (2021-04-28)
### Added
- New metric "median_absolute_percentage_error" in `model_quality_report.quality_metrics.RegressionQualityMetrics`.
### Changed
- Rename "mape" into "mean_absolute_percentage_error" in `model_quality_report.quality_metrics.RegressionQualityMetrics`.

## 1.0.0rc3 (2021-04-27)
### Changed
- Check that predictions and true values have the same index names.

## 1.0.0rc2 (2021-04-26)
### Changed
- Convert model predictions to `pd.Series` only if some other type is returned.

## 1.0.0rc1 (2021-04-23)
### Added
- `ByFrequency` splitter in `model_quality_report.splitters.temporal.cross_validation.by_frequency`.
### Changed
- Major refactoring and renaming of modules and classes.

## 0.2 (2019-08-26)
- New `TimeSeriesCrossValidationDataSplitter` which produces a list of splits of temporal data such that each consecutive train set has one more observation and test set one less. This class can be of use in Time Series analysis, where one wants to produce predictions for several steps ahead starting at different dates, in order to assess predictive power of a model by averaging errors across these dates for each specific horizon.
- New `CrossValidationTimeSeriesQualityReport` for cross-validation time series quality reporting. Collects quality metrics when model predictions are in general non-scalar, e.g. for several time steps ahead.
- New `ModelComparisonReport` takes a splitter, a quality report class, and the list of model/data. It calculates quality metrics for each pair and combines this into one single quality report.
- All splitters return a list of at least one split
- `QualityReportArchetype` calculates quality metrics internally through pandas objects. For that end one needs to implement a new method `_calculate_quality_metrics_as_pandas` for each new quality report that takes true and predicted values as pandas objects and returns pandas objects as well. This allows to add as many dimensions to the report as necessary. For example, one may need to compare several models for several KPI's.

## 0.1 (2019-07-10)
- First release
