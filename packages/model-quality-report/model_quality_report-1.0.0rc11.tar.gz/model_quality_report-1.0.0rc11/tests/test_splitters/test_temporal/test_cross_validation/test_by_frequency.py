import os
import unittest

import pandas as pd
from numpy.random import randint

from model_quality_report.splitters.temporal.cross_validation.by_frequency import (
    ByFrequency,
)


class TestByFrequency(unittest.TestCase):
    def setUp(self):
        __current_dir_path = os.path.dirname(os.path.abspath(__file__))
        test_data = (
            pd.read_pickle(os.path.join(__current_dir_path, "../../../data/date-value_df.pkl"))
            .drop_duplicates(subset=["date"])
            .assign(date=lambda x: pd.to_datetime(x["date"]))
            .sort_values(by="date")
            .reset_index(drop=True)
        )
        self.X = test_data.assign(**{"exog": lambda x: randint(100, size=test_data.shape[0])}).drop(columns=["value"])
        self.y = test_data.set_index("date")["value"]

    def test_correct_number_of_splits(self):
        start_split_date = pd.Timestamp("2017-01-01")
        frequency = "W-FRI"
        splitter = ByFrequency(
            start_split_date=start_split_date,
            frequency=frequency,
            date_column_name="date",
        )

        splits = splitter.split(self.X, self.y)

        self.assertEqual(len(splits), 47)

    def test_split_date_boundaries(self):
        start_split_date = pd.Timestamp("2017-01-01")
        frequency = "W-FRI"
        splitter = ByFrequency(
            start_split_date=start_split_date,
            frequency=frequency,
            date_column_name="date",
        )

        splits = splitter.split(self.X, self.y)

        for X_train, X_test, y_train, y_test in splits:
            self.assertGreaterEqual(X_test["date"].min(), start_split_date)
            self.assertLess(X_train["date"].max(), X_test["date"].min())
            self.assertGreaterEqual(y_test.index.min(), start_split_date)
            self.assertLess(y_train.index.max(), y_test.index.min())

    def test_increment_of_train_data(self):
        start_split_date = pd.Timestamp("2017-01-01")
        frequency = "W-FRI"
        splitter = ByFrequency(
            start_split_date=start_split_date,
            frequency=frequency,
            date_column_name="date",
        )

        splits = splitter.split(self.X, self.y)

        for split, split_next in zip(splits[:-1], splits[1:]):
            X_train, _, y_train, _ = split
            X_train_next, _, y_train_next, _ = split_next
            self.assertLessEqual(X_train.shape[0], X_train_next.shape[0])
            self.assertLessEqual(y_train.shape[0], y_train_next.shape[0])

    def test_returns_error_if_no_datetime_index(self):
        start_split_date = pd.Timestamp("2017-01-01")
        frequency = "W-FRI"
        splitter = ByFrequency(
            start_split_date=start_split_date,
            frequency=frequency,
            date_column_name="date",
        )

        errors = splitter.validate_parameters(self.X, self.y.reset_index(drop=True))

        self.assertTrue(len(errors) > 0)
        self.assertTrue("DatetimeIndex" in errors[0])

    def test_returns_error_if_split_date_too_large(self):
        start_split_date = pd.Timestamp("2100-01-01")
        frequency = "W-FRI"
        splitter = ByFrequency(
            start_split_date=start_split_date,
            frequency=frequency,
            date_column_name="date",
        )

        errors = splitter.validate_parameters(self.X, self.y)

        self.assertTrue(len(errors) > 0)
        self.assertTrue(str(start_split_date) in errors[0])

    def test_returns_error_if_split_date_too_small(self):
        start_split_date = pd.Timestamp("1900-01-01")
        frequency = "W-FRI"
        splitter = ByFrequency(
            start_split_date=start_split_date,
            frequency=frequency,
            date_column_name="date",
        )

        errors = splitter.validate_parameters(self.X, self.y)

        self.assertTrue(len(errors) > 0)
        self.assertTrue(str(start_split_date) in errors[0])

    def test_returns_error_if_wrong_frequency_is_provided(self):
        start_split_date = pd.Timestamp("2017-01-01")
        frequency = "wrong_freq"
        splitter = ByFrequency(
            start_split_date=start_split_date,
            frequency=frequency,
            date_column_name="date",
        )

        errors = splitter.validate_parameters(self.X, self.y)

        self.assertTrue(len(errors) > 0)
        self.assertTrue("wrong_freq" in errors[0])

    def test_returns_error_if_wrong_date_col_is_provided(self):
        start_split_date = pd.Timestamp("2017-01-01")
        frequency = "wrong_freq"
        splitter = ByFrequency(
            start_split_date=start_split_date,
            frequency=frequency,
            date_column_name="exog",
        )

        errors = splitter.validate_parameters(self.X, self.y)

        self.assertTrue(len(errors) > 0)
        self.assertTrue("exog" in errors[0])

    def test_parameters_can_be_accessed_by_get_parameters(self):
        start_split_date = pd.Timestamp("2017-01-01")
        frequency = "W-FRI"
        splitter = ByFrequency(
            start_split_date=start_split_date,
            frequency=frequency,
            date_column_name="date",
        )

        parameters = splitter.get_parameters()

        self.assertIsInstance(parameters, dict)
        self.assertDictEqual(
            {
                ByFrequency.lbl_start_split_date: start_split_date,
                ByFrequency.lbl_frequency: frequency,
                ByFrequency.lbl_date_column_name: "date",
            },
            parameters,
        )
