# Hierarchical Entity Resolution Engine (Intra-Cluster Matching)

A specialized data cleaning framework designed for high-precision entity resolution. This tool follows a **Two-Step "Split-Apply-Combine"** methodology to resolve textual variations within parent-child data relationships (e.g., resolving product name variations within specific brand clusters).

## 🧩 The Two-Step Logic
1.  **Step 1: Parent Clustering:** We need to first perform fuzzy matching using Brand Name and Brand Code.
2.  **Step 2: Intra-Cluster Resolution:** We need to copy the Traceback(Brand_Code) column and paste it in the IBV Extract. We need to use that extract to in the modified fuzzy matching script which is executed *exclusively within each cluster*. This identifies precise variations (typos, formatting shifts) among similar groups while ensuring that names from different clusters never accidentally merge.

---

## 🚀 Key Features

* **Intra-Cluster Matching:** Performs `RapidFuzz` / `Levenshtein` analysis within specific data silos to increase accuracy.
* **Alphabetical Chunking:** Includes an "Alphabet Filter" (e.g., processing only names starting with 'A-F') to handle massive datasets without memory overflow.
* **One-Row-Per-Cluster Reporting:** Consolidates all identified variations into a single audit row for streamlined review.
* **Automated EDA:** Generates a `Sweetviz` HTML dashboard to profile data health before and after processing.
* **Interactive UI:** A Tkinter-based configuration window for selecting target columns and matching thresholds.

---

## 🛠️ Project Structure

* `main.py`: The orchestrator—manages the UI flow and coordinates the loading and processing steps.
* `data_loader.py`: Handles OCP-compliant file ingestion (CSV/Excel) and the configuration GUI.
* `results.py`: The core logic engine containing the Intra-Cluster fuzzy matching algorithm and report generation.
* `requirements.txt`: Necessary libraries (Pandas, RapidFuzz, Sweetviz, Matplotlib).

---

## ⚙️ Installation & Usage

### 1. Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name

# Install dependencies
pip install -r requirements.txt
```

### 2. Execution
Run the main script to launch the interface:
```bash
python main.py
```

### 3. Workflow
1.  **Select File:** Choose your source CSV or Excel file.
2.  **Configure:**  Select the **Target Column** = IBV Name.
    * Select the **Traceback Column** = Traceback(Brand Code)

3.  **Review:** Check the `Intra_Cluster_Analysis.csv` for results and `Sweetviz_Report.html` for data insights.

---

## 📊 Output Artifacts

* **`Intra_Cluster_Analysis.csv`**: A detailed report showing the Traceback Cluster, all variations found within that cluster, the total rows affected, and the specific Excel row numbers for manual auditing.
* **`Fuzzy_Impact_Histogram.png`**: A visualization showing the reduction in data "noise" achieved by the engine.
* **`Sweetviz_Report.html`**: A comprehensive exploratory data analysis of your dataset.
