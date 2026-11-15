import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def preprocess_dataset(filename="sample_dataset.csv", output="processed_dataset.csv"):
    # Step 1: Load CSV
    df = pd.read_csv(filename)
    
    # Step 2: Identify columns for each type
    max_cols = [col for col in df.columns if col.startswith("Max_R")]
    alloc_cols = [col for col in df.columns if col.startswith("Alloc_R")]
    need_cols = [col for col in df.columns if col.startswith("Need_R")]
    
    # Columns to scale (Available and Total remain unchanged)
    cols_to_scale = max_cols + alloc_cols + need_cols

    # Step 3: Apply Min-Max scaling
    scaler = MinMaxScaler()
    df[cols_to_scale] = scaler.fit_transform(df[cols_to_scale])

    # Step 4: Save preprocessed dataset
    df.to_csv(output, index=False)
    print(f"Preprocessed dataset saved to {output}")

if __name__ == "__main__":
    preprocess_dataset()