import json
from datetime import datetime
import pandas as pd

def extract_timestamps_json(json_filepath, output_csv_filepath="activity_timestamps.csv"):
    timestamps = []
    try:
        with open(json_filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for record in data:
            if 'time' in record:
                # The 'time' field is typically in ISO 8601 format
                # The 'Z' indicates UTC, so we parse it as UTC and convert to aware datetime
                try:
                    dt_object = datetime.fromisoformat(record['time'].replace('Z', '+00:00'))
                    timestamps.append(dt_object)
                except ValueError:
                    print(f"Warning: Could not parse time format for record: {record['time']}")
                    continue

        df = pd.DataFrame(timestamps, columns=['timestamp'])
        # Sort timestamps for a cleaner timeline
        df = df.sort_values(by='timestamp').reset_index(drop=True)
        df.to_csv(output_csv_filepath, index=False)
        print(f"Successfully extracted {len(timestamps)} timestamps to {output_csv_filepath}")

    except FileNotFoundError:
        print(f"Error: File not found at {json_filepath}")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_filepath}. Make sure it's a valid JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # --- IMPORTANT: REPLACE THIS WITH THE ACTUAL PATH TO YOUR FILE ---
    # Example: 'C:/Users/YourName/Downloads/Takeout/My Activity/Web & App Activity/Web & App Activity.json'
    # Or on Linux/macOS: '/home/YourName/Downloads/Takeout/My Activity/Web & App Activity/Web & App Activity.json'
    your_json_file = 'path/to/your/Web & App Activity.json'

    extract_timestamps_json(your_json_file)
    print("\nExtraction complete. You can now use 'activity_timestamps.csv' for visualization.")
    print("Remember to install pandas if you haven't already: pip install pandas")
