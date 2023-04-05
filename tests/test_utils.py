import unittest
import pandas as pd
from utils.data_preprocessing import preprocess_data
from utils.feature_engineering import add_bollinger_bands

class TestDataPreprocessing(unittest.TestCase):
    def test_preprocess_data(self):
        # create example dataframe
        df = pd.DataFrame({'open': [100, 200, 300],
                           'high': [150, 250, 350],
                           'low': [50, 150, 250],
                           'close': [120, 220, 320],
                           'volume': [1000, 2000, 3000]},
                          index=['2020-01-01', '2020-01-02', '2020-01-03'])
        # preprocess the data
        processed_df = preprocess_data(df)
        # check if the shape of the data is the same
        self.assertEqual(df.shape, processed_df.shape)
        # check if the processed data is sorted by date
        self.assertEqual(processed_df.index.is_monotonic_increasing, True)

class TestFeatureEngineering(unittest.TestCase):
    def test_add_bollinger_bands(self):
        # create example dataframe
        df = pd.DataFrame({'open': [100, 200, 300],
                           'high': [150, 250, 350],
                           'low': [50, 150, 250],
                           'close': [120, 220, 320],
                           'volume': [1000, 2000, 3000]},
                          index=['2020-01-01', '2020-01-02', '2020-01-03'])
        # add bollinger bands
        bb_df = add_bollinger_bands(df)
        # check if the shape of the data is the same
        self.assertEqual(df.shape, bb_df.shape)
        # check if the bollinger bands columns were added
        self.assertEqual(list(bb_df.columns), ['open', 'high', 'low', 'close', 'volume', 'bb_middle_band', 'bb_upper_band', 'bb_lower_band'])
