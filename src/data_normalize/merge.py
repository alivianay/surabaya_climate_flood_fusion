import pandas as pd
import glob
import os
from datetime import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data', 'normalize')
output_file = os.path.join(script_dir, '..', '..', 'data','normalize', 'iklim_surabaya_2023.csv')

pattern = os.path.join(data_dir, '*tanjung*.csv')
csv_files = glob.glob(pattern)

print(f"Found {len(csv_files)} files to merge:")
for file in csv_files:
    print(f"  - {os.path.basename(file)}")

if not csv_files:
    print("No CSV files with 'tanjung' found in the directory!")
    exit(1)

dfs = []
for file in csv_files:
    try:
        df = pd.read_csv(file)
        print(f"Read {len(df)} rows from {os.path.basename(file)}")

        if 'Tanggal' in df.columns:
            df['Tanggal'] = pd.to_datetime(df['Tanggal'], errors='coerce', dayfirst=True)

            failed_conversions = df['Tanggal'].isna().sum()
            if failed_conversions > 0:
                print(f"  Warning: {failed_conversions} rows had invalid dates in {os.path.basename(file)}")
            
        dfs.append(df)
    except Exception as e:
        print(f"Error reading {file}: {e}")

if dfs:
    merged_df = pd.concat(dfs, ignore_index=True)

    initial_count = len(merged_df)
    merged_df = merged_df.drop_duplicates()
    final_count = len(merged_df)
    print(f"Removed {initial_count - final_count} duplicate rows")
    
    # # Sort by date if the column exists
    # if 'Tanggal' in merged_df.columns:
    #     # Remove rows with invalid dates before sorting
    #     valid_dates_df = merged_df.dropna(subset=['Tanggal'])
    #     invalid_dates_count = len(merged_df) - len(valid_dates_df)
        
    #     if invalid_dates_count > 0:
    #         print(f"Removed {invalid_dates_count} rows with invalid dates")
    #         merged_df = valid_dates_df
        
    #     # Sort by date
    #     merged_df = merged_df.sort_values('Tanggal')
        
    #     # Verify sorting
    #     dates = merged_df['Tanggal'].tolist()
    #     is_sorted = all(dates[i] <= dates[i+1] for i in range(len(dates)-1))
    #     print(f"Data is {'properly sorted by date' if is_sorted else 'NOT properly sorted'}")
        
    #     # Display date range
    #     print(f"Date range: {merged_df['Tanggal'].min()} to {merged_df['Tanggal'].max()}")
    
    # Save the merged file
    merged_df.to_csv(output_file, index=False)
    print(f"Successfully saved {len(merged_df)} rows to {output_file}")
else:
    print("No valid dataframes to merge!")