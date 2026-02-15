import os
import pandas as pd
from sqlalchemy import create_engine, text

# Configuration
DB_NAME = "strathmore_analytics.db"
DATA_DIR = "data/raw"

def migrate_to_sql():
    # 1. Create the SQL Engine (SQLite is easy for local dev)
    engine = create_engine(f'sqlite:///{DB_NAME}')
    
    print(f"--- Starting Migration to {DB_NAME} ---")

    # 2. Iterate through your 'data/raw' folder
    for file in os.listdir(DATA_DIR):
        if file.endswith(".csv"):
            table_name = file.replace(".csv", "")
            file_path = os.path.join(DATA_DIR, file)
            
            print(f"Loading {file} into SQL table '{table_name}'...")
            
            # Read CSV
            df = pd.read_csv(file_path)
            
            # 3. Use SQL to write the data
            # 'replace' drops the table if it exists and recreates it
            df.to_sql(table_name, engine, if_exists='replace', index=False)
            
            # Optional: Verify with a SQL Query
            with engine.connect() as conn:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                count = result.scalar()
                print(f"Successfully inserted {count} rows.")

    print("\n--- All files migrated to SQL successfully ---")

if __name__ == "__main__":
    migrate_to_sql()