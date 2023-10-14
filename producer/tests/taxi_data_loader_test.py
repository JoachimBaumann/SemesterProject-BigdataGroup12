import unittest
from datetime import datetime
from loaders.taxi_loader import TaxiDataLoader
from models.taxi_data import TaxiData

TEST_BASE_PATH = "../datasets/taxi_dataset/2019/"

class TestTaxiDataLoader(unittest.TestCase):

    def setUp(self):
        # Assuming there's data for March 1-5 in the sqlite DB
        self.start_date = datetime(2019, 3, 1, 12, 20)
        self.end_date = datetime(2019, 3, 1, 12, 30)
        self.batch_size = 1000
        self.loader = TaxiDataLoader(self.start_date, self.end_date, self.batch_size, base_path=TEST_BASE_PATH)

    def test_raises_error_for_invalid_date_range(self):
        # Date range that spans multiple months
        start_date = datetime(2019, 3, 30)
        end_date = datetime(2019, 4, 2)
        with self.assertRaises(AssertionError):
            TaxiDataLoader(start_date, end_date)

    def test_loads_correct_date_range(self):
        # Fetch all the data within the given date range
        entries = list(self.loader.get_entries_in_order())
        
        # Ensuring data isn't empty and falls within date range
        self.assertGreater(len(entries), 0)
        for entry in entries:
            self.assertTrue(self.start_date <= entry.tpep_pickup_datetime <= self.end_date)

    def test_entries_are_ordered(self):
        # Fetch all the data within the given date range
        entries = list(self.loader.get_entries_in_order())
        # Ensuring data is ordered by tpep_pickup_datetime
        for i in range(1, len(entries)):
            self.assertLessEqual(entries[i-1].tpep_pickup_datetime, entries[i].tpep_pickup_datetime)

    def test_correct_batching(self):
        # Let's test with a smaller batch size to simplify
        batches = list(self.loader.get_batches())

        # Ensure batches are not empty
        self.assertGreater(len(batches), 0, "No batches were retrieved")

        # All batches except possibly the last should have 10 items
        for batch in batches[:-1]:
            self.assertEqual(len(batch), self.batch_size)
        
        # The last batch might have fewer, but should not be empty
        self.assertGreater(len(batches[-1]), 0)
        self.assertLessEqual(len(batches[-1]), self.batch_size)


    def test_all_values_parsed_correctly(self):

        count = 0
        for idx, batch in enumerate(self.loader._get_raw_batch()):
            for entry in batch:
                taxi_data = self.loader._from_raw(entry)
                self.assertIsNotNone(taxi_data, f"Value for data entry {idx} is None")
                count = count +1
        
        self.assertGreater(count, 0)

if __name__ == '__main__':
    unittest.main()
