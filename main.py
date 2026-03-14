import pandas as pd
import os
from pipeline.mock_data import generate_mock_data
from pipeline.risk_filters import apply_bot_filter
from pipeline.crisis import calculate_72h_signals
from pipeline.geo_logic import apply_dynamic_thresholds

def run_governance_pipeline():
    print("--- STARTING AI4MH GOVERNANCE PIPELINE ---")
    
    # 1. Generate the raw mock data
    generate_mock_data(num_rows=6000)
    raw_df = pd.read_csv("data/raw/mock_social_data.csv", parse_dates=['timestamp'])
    
    clean_df = apply_bot_filter(raw_df, max_user_contribution=0.10)
    
    signals_df = calculate_72h_signals(clean_df)
    
    # 2. Apply Bias Mitigation 
    final_alerts = apply_dynamic_thresholds(signals_df)
    
    # 3.Save the final Human-in-the-Loop Audit Log
    os.makedirs("data/outputs", exist_ok=True)
    final_alerts.to_csv("data/outputs/final_audit_log.csv", index=False)
    
    print("--- PIPELINE COMPLETE ---")
    print(f"Check data/outputs/final_audit_log.csv for the {len(final_alerts)} escalated alerts.")

if __name__ == "__main__":
    run_governance_pipeline()