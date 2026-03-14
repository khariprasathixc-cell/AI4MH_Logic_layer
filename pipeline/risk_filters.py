
import pandas as pd

def apply_bot_filter(df, max_user_contribution=0.10):
    #Filters out the bot with more that 10 % contribution
    print("Applying Information Entropy Bot Filter...")
    
    initial_rows = len(df)
    
    county_totals = df.groupby('county_id').size().reset_index(name='total_county_posts')
    
    user_totals = df.groupby(['county_id', 'user_id']).size().reset_index(name='user_posts')
    
    #Merge the two dataframes 
    merged_df = pd.merge(user_totals, county_totals, on='county_id')
    
    merged_df['contribution_pct'] = merged_df['user_posts'] / merged_df['total_county_posts']
    
    #Identify the bots 
    bots = merged_df[merged_df['contribution_pct'] > max_user_contribution]
    bot_users = bots['user_id'].unique()
    
    #Filter the original dataframe 
    clean_df = df[~df['user_id'].isin(bot_users)].copy()
    
    final_rows = len(clean_df)
    dropped_rows = initial_rows - final_rows
    
    print(f"Bot Filter Complete. Identified {len(bot_users)} bot(s).")
    print(f"Dropped {dropped_rows} artificial posts.")
    
    return clean_df