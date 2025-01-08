import pandas as pd
import os
import sys
from datetime import datetime
import re

def get_file_number(filename):
    # Extract the number from filename like "stt_records_20250107_195238.csv"
    date=filename.split('_')[-2]
    time=filename.split('_')[-1].split('.')[0]
    result = date + "." + time
    print(result)
    return result

def merge_time_records(directory):
    # Get all CSV files in the directory
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    
    if not csv_files:
        raise Exception("No CSV files found in the specified directory")
    
    # Read all CSV files into dataframes with their file numbers
    dfs = []
    for file in csv_files:
        file_path = os.path.join(directory, file)
        try:
            df = pd.read_csv(file_path)
            file_number = get_file_number(file)
            # Add file number as a column
            df['file_number'] = file_number
            dfs.append(df)
        except Exception as e:
            print(f"Error reading {file}: {str(e)}")
    
    if not dfs:
        raise Exception("No valid CSV files could be read")
    
    # Concatenate all dataframes
    merged_df = pd.concat(dfs, ignore_index=True)
    
    # Convert time columns to datetime
    merged_df['time started'] = pd.to_datetime(merged_df['time started'])
    merged_df['time ended'] = pd.to_datetime(merged_df['time ended'])
    
    # Function to keep longer string when aggregating
    def keep_longer(series):
        # Convert all values to strings and replace NaN with empty string
        series = series.fillna('')
        series = series.astype(str)
        # Return the string with maximum length, or empty string if all are empty
        return max(series, key=len) if len(series) > 0 else ''
    
    # Function to keep activity name from highest numbered file
    def keep_latest_activity(group):
        # Handle empty group case
        if len(group) == 0:
            return ''
        max_file_idx = group['file_number'].idxmax()
        return group.loc[max_file_idx, 'activity name']
    
    # Process groups to handle the activity name selection
    result_records = []
    
    for (start_time, end_time), group in merged_df.groupby(['time started', 'time ended']):
        record = {
            'time started': start_time,
            'time ended': end_time,
            'activity name': keep_latest_activity(group),
            'comment': keep_longer(group['comment']),
            'categories': keep_longer(group['categories']),
            'record tags': keep_longer(group['record tags']),
            'duration': group['duration'].iloc[0] if len(group) > 0 else '',
            'duration minutes': group['duration minutes'].iloc[0] if len(group) > 0 else 0
        }
        result_records.append(record)
    
    # Create final dataframe
    final_df = pd.DataFrame(result_records)
    
    # Sort by start time
    final_df = final_df.sort_values('time started')
    
    return final_df

def save_merged_records(merged_df, output_file):
    # Format datetime columns back to string
    merged_df['time started'] = merged_df['time started'].dt.strftime('%Y-%m-%d %H:%M:%S')
    merged_df['time ended'] = merged_df['time ended'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Save to CSV
    merged_df.to_csv(output_file, index=False)

def process_directory(directory):
    try:
        # Get current timestamp for the output filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = os.path.join(directory, f"merged_records_{timestamp}.csv")
        
        # Merge the files
        merged_df = merge_time_records(directory)
        
        # Save merged records
        save_merged_records(merged_df, output_file)
        
        print(f"Successfully merged records into: {output_file}")
        print(f"Total records: {len(merged_df)}")
        
    except Exception as e:
        print(f"Error processing directory: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory_path>")
        sys.exit(1)
    
    directory = sys.argv[1]
    
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory")
        sys.exit(1)
    
    process_directory(directory)