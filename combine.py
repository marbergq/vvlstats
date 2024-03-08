import pandas as pd
import datetime
wmn = pd.read_csv('wmn/checkpoints/finish/results.csv')  # Use your actual dataframe variable here
men = pd.read_csv('checkpoints/finish/results.csv')  # Use your actual dataframe variable here

# Add a new column 'source' to each dataframe
wmn['source'] = 'wmn'
wmn['time'] = pd.to_datetime(wmn['time'])
men['source'] = 'men'
men['time'] = pd.to_datetime(men['time'])


# merge the two dataframes
combined = pd.concat([wmn, men])

combined = combined.sort_values('time', ascending=True)
combined['total-place'] = combined.reset_index().index + 1
combined['time'] = pd.to_datetime(combined['time'])
combined['all_diff'] = combined['time'] - combined['time'].iloc[0]
combined['all_diff'] = combined['all_diff'].dt.total_seconds()

# Convert total seconds back to time format
combined['all_diff'] = combined['all_diff'].apply(lambda x: str(datetime.timedelta(seconds=x)))

combined['wmn_time_diff'] = (combined['time'] - wmn['time'].iloc[0]).clip(lower=pd.Timedelta(0))

# Convert time delta to total seconds
combined['wmn_time_diff'] = combined['wmn_time_diff'].dt.total_seconds()

# Convert total seconds back to time format
combined['wmn_time_diff'] = combined['wmn_time_diff'].apply(lambda x: str(datetime.timedelta(seconds=x)))
combined['time'] = combined['time'].dt.time

combined.to_csv('combined.csv', index=False)