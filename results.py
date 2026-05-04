import pandas as pd
import sweetviz as sv
from fuzzywuzzy import process, fuzz
import matplotlib.pyplot as plt
import string
import os

def generate_sweetviz_report(df: pd.DataFrame, output_filename: str = "Sweetviz_Report.html"):
    """Generates a general data health report using Sweetviz."""
    print("Generating Sweetviz report...")
    report = sv.analyze(df)
    report.show_html(output_filename, open_browser=False)

def get_valid_letters(alpha_filter: str):
    """Parses 'A' or 'A-F' into a list of valid starting letters."""
    if not alpha_filter:
        return None
    alpha_filter = alpha_filter.upper()
    if '-' in alpha_filter:
        try:
            start, end = alpha_filter.split('-')
            start_idx = string.ascii_uppercase.index(start.strip())
            end_idx = string.ascii_uppercase.index(end.strip())
            return list(string.ascii_uppercase[start_idx:end_idx+1])
        except ValueError:
            return None
    return [alpha_filter.strip()]


def generate_fuzzy_report(df: pd.DataFrame, config: dict, match_threshold: int = 80, output_filename: str = "Intra_Cluster_Analysis.csv"):
    """
    Modified Logic: Ensures each Traceback Cluster appears only ONCE in the report.
    All variations found within that cluster are grouped into a single row.
    """
    print("\n--- Running Single-Row Cluster Analysis ---")
    
    traceback_col = config.get('traceback')
    brand_code_col = "Brand Code"
    target_col = "IBV Name"
    
    if traceback_col not in df.columns or brand_code_col not in df.columns:
        print("Error: Required columns not found.")
        return

    all_reports = []
    unique_clusters = df[traceback_col].dropna().unique()

    for cluster_string in unique_clusters:
        # 1. Get the IDs and search the whole file
        target_ids = [i.strip() for i in str(cluster_string).split(',') if i.strip()]
        cluster_data = df[df[brand_code_col].astype(str).isin(target_ids)]
        
        if cluster_data.empty:
            continue

        # 2. Get all unique names for this cluster
        names_in_cluster = cluster_data[target_col].dropna().astype(str).str.strip().unique().tolist()
        
        if len(names_in_cluster) < 2:
            continue 

        # 3. Identify WHICH names are actually variations/duplicates
        # We look for any name that has a fuzzy match with another name in the same cluster
        detected_variations = set()
        for i, name_a in enumerate(names_in_cluster):
            for j, name_b in enumerate(names_in_cluster):
                if i == j: continue
                
                score = fuzz.token_sort_ratio(name_a, name_b)
                if score >= match_threshold:
                    detected_variations.add(name_a)
                    detected_variations.add(name_b)

        # 4. If variations were found, put them all in ONE row for this cluster
        if detected_variations:
            # Get the row numbers for all detected variations in this cluster
            matching_rows = cluster_data[cluster_data[target_col].isin(detected_variations)]
            
            all_reports.append({
                "Traceback Cluster": cluster_string,
                "Brand Codes": ", ".join(target_ids),
                "All Variations in Cluster": " | ".join(sorted(detected_variations)),
                "Distinct Variation Count": len(detected_variations),
                "Total Rows Affected": len(matching_rows),
                "Excel Row Numbers": ", ".join((matching_rows.index + 2).astype(str))
            })

    if all_reports:
        pd.DataFrame(all_reports).to_csv(output_filename, index=False)
        print(f"Success! Each of the {len(all_reports)} clusters now occupies exactly one row.")
    else:
        print("No variations found.")