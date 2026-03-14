import pandas as pd
import numpy as np

def apply_dynamic_thresholds(signals_df):
    print("Applying dynamic population thresholds for Rural/Urban bias mitigation...")
    
    population_map = {
        "Urban_County_A": 1000000,
        "Urban_County_B": 850000,
        "Rural_County_X": 15000,
        "Rural_County_Y": 8000
    }
    
    signals_df['population'] = signals_df['county_id'].map(population_map)
    
    # Calculate the dynamic threshold: max(25, pop * 0.0001)
    signals_df['dynamic_threshold'] = np.maximum(25, signals_df['population'] * 0.0001)
    
    # Trigger an alert 
    signals_df['alert_triggered'] = signals_df['72h_high_risk_volume'] >= signals_df['dynamic_threshold']
    
    alerts_df = signals_df[signals_df['alert_triggered']].copy()
    
    print(f"Bias Mitigation Complete. Identified {len(alerts_df)} critical escalation points.")
    
    return alerts_df