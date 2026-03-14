import pandas as pd
import numpy as np

def calculate_72h_signals(df):
    #Calculates the 72-hour rolling volume
    print("Calculating 72-hour rolling crisis signals...")
    
    df = df.sort_values('timestamp')
    
    # Pandas needs this to understand what 72h, cuz we just gave integer 72 inside .rolling()
    df = df.set_index('timestamp')
    
    #filtering posts where the BERT model was highly confident (prob > 0.75)
    high_risk_df = df[df['prob_suicide'] > 0.75]
    
    results = []
    
    #Group by county because a spike in Urban should not affect Rural
    for county, county_data in high_risk_df.groupby('county_id'):
        
        #.rolling() tells time based window of 72h every post 
        rolling_volume = county_data['prob_suicide'].rolling('72h').count()
        
        # We also want the average VADER sentiment during that same 72-hour window
        rolling_sentiment = county_data['vader_compound'].rolling('72h').mean()
        
        county_signals = pd.DataFrame({
            'county_id': county,
            'timestamp': county_data.index,
            '72h_high_risk_volume': rolling_volume.values,
            '72h_avg_sentiment': rolling_sentiment.values
        })
        
        results.append(county_signals)
        
    final_signals = pd.concat(results).reset_index(drop=True)
    
    print(f"Rolling calculations complete. Processed {len(final_signals)} high-risk time windows.")
    
    return final_signals