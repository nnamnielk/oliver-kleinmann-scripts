import unittest
import pandas as pd
import os
from datetime import datetime
import shutil
from sttMerge import merge_time_records, process_directory

class TestMergeRecords(unittest.TestCase):
    def setUp(self):
        # Create a temporary test directory
        self.test_dir = "test_data"
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)

        # Create test CSV files
        self.create_test_files()

    def tearDown(self):
        # Clean up the test directory
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def create_test_files(self):
        # Test file 1: stt_records_20240101_120000.csv
        df1 = pd.DataFrame({
            'time started': ['2024-01-01 10:00:00', '2024-01-01 11:00:00'],
            'time ended': ['2024-01-01 10:30:00', '2024-01-01 11:30:00'],
            'activity name': ['Reading', 'Writing'],
            'comment': ['Short comment', 'Another comment'],
            'categories': ['Education', 'Work'],
            'record tags': ['book', 'document'],
            'duration': ['30m', '30m'],
            'duration minutes': [30, 30]
        })
        df1.to_csv(os.path.join(self.test_dir, 'stt_records_20240101_120000.csv'), index=False)

        # Test file 2: stt_records_20240102_120000.csv (with conflicts)
        df2 = pd.DataFrame({
            'time started': ['2024-01-01 10:00:00', '2024-01-01 12:00:00'],
            'time ended': ['2024-01-01 10:30:00', '2024-01-01 12:30:00'],
            'activity name': ['Reading Updated', 'Coding'],
            'comment': ['A much longer comment about reading', ''],
            'categories': ['Education, Learning', 'Programming'],
            'record tags': ['book, study', 'python'],
            'duration': ['30m', '30m'],
            'duration minutes': [30, 30]
        })
        df2.to_csv(os.path.join(self.test_dir, 'stt_records_20240102_120000.csv'), index=False)

        # Test file 3: stt_records_20240103_120000.csv (with missing values)
        df3 = pd.DataFrame({
            'time started': ['2024-01-01 10:00:00', '2024-01-01 13:00:00'],
            'time ended': ['2024-01-01 10:30:00', '2024-01-01 13:30:00'],
            'activity name': ['Reading Final', 'Meeting'],
            'comment': [None, 'Team meeting'],
            'categories': ['', 'Work'],
            'record tags': ['book, study, notes', ''],
            'duration': ['30m', '30m'],
            'duration minutes': [30, 30]
        })
        df3.to_csv(os.path.join(self.test_dir, 'stt_records_20240103_120000.csv'), index=False)

    def test_activity_name_from_latest_file(self):
        merged_df = merge_time_records(self.test_dir)
        # Check if the activity name from the latest file is used
        first_record = merged_df[merged_df['time started'] == '2024-01-01 10:00:00'].iloc[0]
        self.assertEqual(first_record['activity name'], 'Reading Final')

    def test_longest_comment_preserved(self):
        merged_df = merge_time_records(self.test_dir)
        first_record = merged_df[merged_df['time started'] == '2024-01-01 10:00:00'].iloc[0]
        self.assertEqual(first_record['comment'], 'A much longer comment about reading')

    def test_longest_categories_preserved(self):
        merged_df = merge_time_records(self.test_dir)
        first_record = merged_df[merged_df['time started'] == '2024-01-01 10:00:00'].iloc[0]
        self.assertEqual(first_record['categories'], 'Education, Learning')

    def test_longest_record_tags_preserved(self):
        merged_df = merge_time_records(self.test_dir)
        first_record = merged_df[merged_df['time started'] == '2024-01-01 10:00:00'].iloc[0]
        self.assertEqual(first_record['record tags'], 'book, study, notes')

    def test_no_duplicate_entries(self):
        merged_df = merge_time_records(self.test_dir)
        # Count occurrences of each time started/ended pair
        counts = merged_df.groupby(['time started', 'time ended']).size()
        self.assertTrue(all(count == 1 for count in counts))

    def test_chronological_order(self):
        merged_df = merge_time_records(self.test_dir)
        # Check if records are sorted by time started
        self.assertTrue(merged_df['time started'].equals(merged_df['time started'].sort_values()))

    def test_process_directory(self):
        process_directory(self.test_dir)
        # Check if output file was created
        output_files = [f for f in os.listdir(self.test_dir) if f.startswith('merged_records_')]
        self.assertEqual(len(output_files), 1)

    def test_empty_values_handling(self):
        merged_df = merge_time_records(self.test_dir)
        # Check if empty values are handled properly
        self.assertTrue(all(merged_df['comment'].notna()))
        self.assertTrue(all(merged_df['categories'].notna()))
        self.assertTrue(all(merged_df['record tags'].notna()))

    def test_total_record_count(self):
        merged_df = merge_time_records(self.test_dir)
        # Should have 4 unique records (1 overlapping, 3 unique times)
        self.assertEqual(len(merged_df), 4)

if __name__ == '__main__':
    unittest.main(verbosity=2)