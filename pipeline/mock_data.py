import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

"""
Rather than fetching the real world data here we using Synthetic data the data 
which was generated through our systems cpu using the random module by specifying the 
range for each values and generate lines-and-lines of data in seconds, i prefer this 
method because i cant get access to real world social media posts which has high 
privacy breakdown, so for a logic layer i think this suits better.
"""


def generate_mock_data(num_rows=5000):
    print("Generating mock AI4MH Phase 1 output data...")
    
    start_date = datetime(2026, 5, 1, 0, 0)
    counties = ["Urban_County_A", "Urban_County_B", "Rural_County_X", "Rural_County_Y"]
    
    data = []
    
    for i in range(num_rows):
        # Generate a random timestamp within a 7-day window
        random_minutes = random.randint(0, 7 * 24 * 60)
        timestamp = start_date + timedelta(minutes=random_minutes)
        
        county = random.choices(counties, weights=[40, 40, 10, 10])[0]
        
        user_id = f"User_{random.randint(1, 1000)}"
        
        prob_suicide = round(random.uniform(0.0, 1.0), 4) # BERT output
        vader_score = round(random.uniform(-1.0, 1.0), 4) # VADER sentiment
        
        entities = ""
        
        data.append([f"Post_{i}", timestamp, county, user_id, prob_suicide, vader_score, entities])

    # Convert to Pandas DataFrame
    df = pd.DataFrame(data, columns=[
        "post_id", "timestamp", "county_id", "user_id", 
        "prob_suicide", "vader_compound", "entities"
    ])

    
    # 1: The Spam Bot Amplification
    # We force User_999 to post 300 times, our 10% cap filter will catch and drop this later.
    bot_data = []
    for i in range(300):
        bot_data.append({
            "post_id": f"BotPost_{i}",
            "timestamp": start_date + timedelta(days=2, minutes=i*5), # Rapid fire posting
            "county_id": "Urban_County_A",
            "user_id": "User_999", # The Bot
            "prob_suicide": 0.85,  # High risk
            "vader_compound": -0.8,
            "entities": ""
        })
    df = pd.concat([df, pd.DataFrame(bot_data)], ignore_index=True)

    #2: The Media-Driven Spike
    
    media_spike_indices = df[(df['timestamp'] > '2026-05-04') & (df['timestamp'] < '2026-05-05')].sample(frac=0.3).index
    df.loc[media_spike_indices, 'entities'] = "Celebrity_X"
    df.loc[media_spike_indices, 'prob_suicide'] = np.clip(df.loc[media_spike_indices, 'prob_suicide'] + 0.3, 0, 1.0)

    df = df.sort_values(by="timestamp").reset_index(drop=True)
    
    # Ensure the directory exists
    os.makedirs("data/raw", exist_ok=True)
    file_path = "data/raw/mock_social_data.csv"
    df.to_csv(file_path, index=False)
    
    print(f"Success! Mock dataset saved to {file_path}")
    print(f"Total rows generated: {len(df)}")
    print(df.head())

if __name__ == "__main__":
    generate_mock_data()