import numpy as np
import pandas as pd

def generate_dataset(num_processes=5, num_resources=3, seed=None):
    if seed:
        np.random.seed(seed)

    # Total resources
    total_resources = np.random.randint(7, 15, size=num_resources)

    # Max matrix (each process maximum demand)
    Max = np.random.randint(1, total_resources.max()//2 + 2, size=(num_processes, num_resources))

    # Allocation matrix (cannot exceed Max)
    Allocation = np.zeros((num_processes, num_resources), dtype=int)
    for i in range(num_processes):
        for j in range(num_resources):
            Allocation[i][j] = np.random.randint(0, Max[i][j] + 1)

    # Need matrix = Max - Allocation
    Need = Max - Allocation

    # Available = Total - sum(Allocation)
    allocated_sum = Allocation.sum(axis=0)
    total_resources = np.maximum(total_resources, allocated_sum + 1)   # ensure total resource >= allocated
    Available = total_resources - allocated_sum

    dataset = {
        "Max": Max.tolist(),
        "Allocation": Allocation.tolist(),
        "Need": Need.tolist(),
        "Available": Available.tolist(),
        "Total_Resources": total_resources.tolist()
    }

    return dataset

def save_dataset_csv(dataset, filename="sample_dataset.csv"):
    num_processes = len(dataset["Max"])
    num_resources = len(dataset["Available"])

    # Convert into tabular format
    df_rows = []
    for i in range(num_processes):
        row = {}
        for j in range(num_resources):
            row[f"Max_R{j}"] = dataset["Max"][i][j]
            row[f"Alloc_R{j}"] = dataset["Allocation"][i][j]
            row[f"Need_R{j}"] = dataset["Need"][i][j]
        df_rows.append(row)

    df = pd.DataFrame(df_rows)

    # Save Available and Total_Resources as separate columns
    for j in range(num_resources):
        df[f"Available_R{j}"] = dataset["Available"][j]
        df[f"Total_R{j}"] = dataset["Total_Resources"][j]

    df.to_csv(filename, index=False)
    print(f"Dataset saved to {filename}")

if __name__ == "__main__":
    dataset = generate_dataset(num_processes=5, num_resources=3, seed=42)
    save_dataset_csv(dataset)