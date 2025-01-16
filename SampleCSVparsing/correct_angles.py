# This script was largely generated by ChatGPT

# Usage:
# python correct_angles.py <input directory> [output_directory]
# input directory contains the target csv files
# naming an output directory is optional

# Purpose:
# Retroactively correct bugged data: 
# Ball angles were negative values on Right hand serves
# This corrects all angles to become positive.

import os
import sys
import pandas as pd

def get_files_from_directory(directory):
    return [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith(".csv")]

def read_title_and_dataframe(file_path):
    if not file_path.endswith(".csv"):
        print(f"Skipping {file_path}, not a CSV file.")
        return None, None
    
    with open(file_path, "r", encoding="utf-8") as file:
        header = file.readline().strip()    # first timestamp

    with open(file_path, "rb") as file:
        try:
            file.seek(-2, os.SEEK_END)
            while file.read(1) != b'\n':
                file.seek(-2, os.SEEK_CUR)
        except Exception as e:
            file.seek(0)
        footer = file.readline().decode().strip() # Last timestamp
    
    df = pd.read_csv(file_path, engine="python", skiprows=1, skipfooter=1, dtype=str)

    
    # Convert integer columns back to appropriate types
    for col in df.columns[1:]:  # Ignore column 1 (time)
        try:
            df[col] = pd.to_numeric(df[col])
        except Exception as e:
            print(f"Warning: Could not convert column {col} to numeric - {e}")
    
    return header, df, footer

def process_dataframe(df):
    # Corrects negative angles
    df['ball_angle'] = df['ball_angle'] % 360
    return df

def save_modified_csv(file_path, output_dir, title, df, footer):
    if df is None or title is None:
        return
    
    os.makedirs(output_dir, exist_ok=True)
    output_file_path = os.path.join(output_dir, os.path.basename(file_path))
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(title + "\n")
    df.to_csv(output_file_path, mode="a", index=False)
    with open(output_file_path, "a", encoding="utf-8") as file:
        file.write(footer + "\n")
    print(f"Processed and saved {output_file_path}")

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python script.py <source_directory> [output_directory]")
        return
    
    source_dir = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) == 3 else "output"
    
    if not os.path.isdir(source_dir):
        print("Invalid source directory. Exiting...")
        return
    
    files = get_files_from_directory(source_dir)
    
    for file_path in files:
        title, df, footer = read_title_and_dataframe(file_path)
        if df is not None and title is not None:
            modified_df = process_dataframe(df)
            save_modified_csv(file_path, output_dir, title, modified_df, footer)
    
    print("File processing completed.")

if __name__ == "__main__":
    main()