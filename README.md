# Detecting Model Smells in UML Diagrams Using Large Language Models

This repository contains the source code, test data, and results for Bachelor's thesis:<br/>
**"Detecting Model Smells in UML Diagrams Using Large Language Models"**.<br/>

### 📄 Project Overview

The goal of this project is to test and evaluate the capability of Large Language Models to detect quality issues, commonly known as "model smells," in Unified Modeling Language (UML) diagrams provided in PDF format.

- **Input:** UML diagrams (PDF) + Prompts (TXT).
- **Engine:** Large Language Models (LLMs).
- **Output:** JSON-structured analysis including empirical testing of identifying smells like _Redundancy_, _Inconsistencies_, etc.
- **Results:** Individual JSON response files for each LLM are stored in the `Results/` directory.
- **Analysis:** Detailed results and comparisons are processed via the **Jupyter Notebook** (`Results.ipynb`).

### 🛠️ Tech Stack

- **Language:** Python
- **Models:** Gemini 3 Pro / ChatGPT 5.1 / Claude Opus 4.5
- **Format:** JSON (ISO 8601 Timestamps)

---

### 🎓 Acknowledgements

This project uses a **condensed selection** of model smell rules adapted from the [Catalog of Model Smells](https://github.com/erki77/model-smells), based on the paper **"On Finding Model Smells Based on Code Smells"** (Eessaar & Käosaar, 2018).

---

### ⚖️ Licensing

This project is licensed under multiple licenses:

- **Source Code**: The source code is licensed under the **MIT License**.
- **Data**: The datasets found in the `Data/` directory and **its** sub-directories are licensed under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license.

See the `LICENSE` file in each respective directory for full details.

---

_Created by Tarmo Ploom for TalTech - Tallinn University of Technology, 2025._
