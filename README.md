# AI4MH Phase 2: Governance Logic Layer

This repository contains the prototype implementation of the Governance Logic Layer proposed for Phase 2 of the AI4MH GSoC project. 

Because the Phase 1 machine learning outputs (BERT/VADER) operate on a post-by-post basis, this pipeline demonstrates how to aggregate those raw probabilities into reliable, bias-mitigated, and auditable public health alerts using time-series data engineering.

## How to Run

1. **Install Dependencies:**
   Ensure you have Python 3.10+ installed.
   bash
   pip install -r requirements.txt
   
Execute the Pipeline:
Run the orchestrator script. This will generate a synthetic Phase 1 dataset, pass it through the governance filters, and output the final alerts.


python main.py
🏗️ Pipeline Architecture
The system is broken down into four distinct processing modules:

**generate_mock_data.py** (Data Ingestion Simulation)

Procedurally generates 6,000+ rows of simulated social media data.

Note: This script intentionally injects "poison" into the dataset (e.g., a single bot posting 300 times, and an artificial media spike) to verify that the downstream risk filters function correctly.

**risk_filters.py** (Reliability & Noise Reduction)

Implements an Information Entropy filter to cap single-user volume contributions at 10% per county.

Suppresses artificial volume spikes driven by media entities rather than organic local distress.

**crisis_engine.py** (Time-Series Aggregation)

Converts static data into dynamic signals using Pandas df.rolling('72h').

Calculates the sustained high-risk volume and average sentiment intensity over continuous 72-hour sliding windows.

**geo_bias_logic.py** (Bias Mitigation)

Addresses rural/urban data disparities.

Applies the dynamic population threshold formula: max(25, county_population * 0.0001) to ensure equitable crisis detection regardless of geographic sparsity.

**📂 Outputs**
After running main.py, the system will generate an outputs/ directory containing final_audit_log.csv. This represents the Immutable Audit Log that would be escalated to the Human-in-the-Loop (HITL) dashboard for final review by a state health official.