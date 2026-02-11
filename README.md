# CityBike Analytics Platform (Capstone Project)

A comprehensive Python-based data analysis pipeline for a bike-sharing system. This project demonstrates advanced software engineering concepts including Object-Oriented Programming (OOP), Design Patterns, automated data cleaning, custom algorithm implementation, and data visualization.

---

##  Features & Requirements Met

### 1. Object-Oriented Programming (OOP)
- **Inheritance & Polymorphism:** Implements a class hierarchy with `Bike` as the base class and specialized `ClassicBike` and `ElectricBike` subclasses.
- **Abstract Base Classes:** Uses `ABC` to define consistent interfaces for system entities.
- **Encapsulation:** Properties and methods are logically grouped within classes (`models.py`).

### 2. Design Patterns
- **Factory Pattern:** Implements `BikeFactory` and `UserFactory` to decouple object creation code from logic (`factories.py`).

### 3. Data Analysis & NumPy/Pandas
- **Automated Cleaning:** Automatically processes raw CSV data, handling duplicates, missing values (`fillna`), and type conversions (`datetime`).
- **Numerical Processing:** Utilizes internal logic for statistical analysis of trip data.

### 4. Custom Algorithms
- **Merge Sort:** Implements a custom recursive Merge Sort algorithm to sort trips by distance ($O(n \log n)$), demonstrating algorithmic understanding independent of Python's built-in libraries (`algorithms.py`).

### 5. Visualization & Reporting
- **Business Intelligence:** Generates a text-based summary report of system usage (peak hours, revenue, popular stations).
- **Charts:** Visualizes data distributions using Matplotlib (implied via `visualization.py`).

---

##  Project Structure

```text
cpastone_project/
 main.py             # Entry point: Orchestrates loading, processing, and reporting
 analyzer.py         # Data logic: Loading and cleaning CSVs using Pandas
 models.py           # OOP Definitions: Bike, User, Station classes
 factories.py        # Factory Pattern: Creates objects from data rows
 algorithms.py       # Custom Algorithms: Merge Sort implementation
 visualization.py    # Plotting logic for graphs
 utils.py            # Helper utility functions
 data/               # Input CSV files (stations, trips, maintenance)
 output/             # Generated reports and cleaned data files
```

---

##  Setup & Installation

**Prerequisites:** Python 3.10+

### Option 1: Quick Setup (Recommended)
1.  **Create Virtual Environment:**
    ```powershell
    python -m venv .venv
    ```

2.  **Activate Environment:**
    ```powershell
    .venv\Scripts\Activate.ps1
    # If blocked: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
    ```

3.  **Install Dependencies:**
    ```powershell
    python -m pip install -r requirements.txt
    ```

### Option 2: Run Without Activation
You can run the project directly using the virtual environment's interpreter:
```powershell
.venv\Scripts\python.exe .\main.py
```

---

##  Usage

Run the main application script:

```powershell
python main.py
```

**What happens next?**
1.  **Initialization:** Data is loaded from `data/`.
2.  **Preprocessing:** Data is cleaned (duplicates removed, types fixed).
3.  **Sorting:** A sample of trips is sorted using the custom **Merge Sort**.
4.  **Reporting:** A summary is saved to `output/summary_report.txt`.
5.  **Visualization:** Charts are generated in `output/figures/` (or displayed).

---

##  Sample Output

```text
Step 1: Initializing BikeShare System...
File stations.csv: 15 -> 15 rows (Cleaned).
File trips.csv: 1515 -> 1485 rows (Cleaned).
File maintenance.csv: 200 -> 200 rows (Cleaned).

Step 2: Processing Numerical Data...
Numerical processing engine: READY

Step 3: Running Custom Sorting Algorithms...
Sorted 10 sample trips by distance using Merge Sort.

Step 4: Saving Cleaned Datasets...
Cleaned data saved to D:\learning\HsH\teil2\python2\cpastone_project\output

Step 5: Generating Business Report...
Report generated: output/summary_report.txt

Step 6: Generating Visualizations...
Visualizations saved to: output/figures/

✅ ALL MILESTONES COMPLETE!
```
