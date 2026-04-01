# Pension Processing Tools (Python)

## 📌 Overview

This repository contains two Python tools designed to automate pension-related data processing:

1. **`pension_tool.py`**
   Combines multiple CSV files and aggregates pension data for monthly processing.

2. **`dedupe_tool.py`**
   Deduplicates CSV records based on SSN (身分證字號) and aggregates duplicated entries.

---

## ⚙️ Requirements

* Python 3.x
* Required packages:

  ```bash
  pip install pandas chardet
  ```

---

## 📁 Project Structure

```
.
├── pension_tool.py
├── dedupe_tool.py
├── pension_resources/     # Input folder for pension tool
├── pension_output/        # Output folder for pension tool
├── dedupe_output/         # Deduplicated output files
├── dupes_output/          # Files containing duplicated records
```

---

## 🧾 pension_tool.py

### 🎯 Purpose

Automates the process of combining multiple pension CSV files and generating aggregated outputs for:

* 自提退休金 (Self-contribution)
* 公提退休金 (Government contribution)

---

### ⚠️ Important Notes

* Only **CSV files** are supported
* All files must use the **same encoding** (default: Big5)
* Remove any **summary or total rows** at the bottom of Excel files
* Ensure required columns exist:

  * 姓名
  * 身分證字號
  * (代扣)自提退休金金額
  * 單位負擔退休金金額 (optional in some files)

---

### ▶️ How to Use

1. Place all relevant CSV files into:

   ```
   pension_resources/
   ```

2. Run the script:

   ```bash
   python pension_tool.py
   ```

3. Output will be generated in:

   ```
   pension_output/
   ```

---

### 📤 Output Files

* `output_自提.csv` → Self-contribution records
* `output_公提.csv` → Government contribution records

---

### 🧠 What It Does

* Validates file encoding consistency
* Extracts relevant columns
* Handles missing columns automatically
* Merges all files into one dataset
* Aggregates data by SSN (身分證字號)
* Filters out zero-value records
* Outputs two categorized CSV files

---

## 🧾 dedupe_tool.py

### 🎯 Purpose

Removes duplicate records from a CSV file based on SSN and provides both:

* Deduplicated dataset
* Original duplicated records (for auditing)

---

### ▶️ How to Use

Run the script with the input file:

```bash
python dedupe_tool.py <path_to_csv_file>
```

Example:

```bash
python dedupe_tool.py resources/sample.csv
```

---

### 📤 Output

* `dedupe_output/<filename>_deduplicated.csv`

  * Clean dataset with duplicates merged

* `dupes_output/<filename>_duplicated.csv`

  * All duplicated rows before aggregation

---

### 🧠 What It Does

* Detects file encoding automatically
* Identifies duplicated SSNs
* Outputs duplicated rows separately
* Aggregates numeric columns for duplicate entries
* Keeps first occurrence of non-numeric fields

---

## 🔧 Notes & Best Practices

* Always verify encoding before processing
* Avoid modifying column names in source files
* Ensure consistent formatting across CSV files
* Keep backups of original data before running scripts

---

## 👤 Author

* 蔡易儒
* 梯次: 271

---

## 📅 Dates

* `pension_tool.py`: 2026-02-09
* `dedupe_tool.py`: 2026-02-06

---

## 🚀 Future Improvements (Optional Ideas)

* Add support for Excel (.xlsx)
* Add logging instead of print statements
* Add validation reports for missing/invalid data
* Build a simple UI for non-technical users

---
