import plotly.graph_objects as go
import pandas as pd

# Sample loading of your data - replace this with your actual data loading code
df = pd.read_csv('final_with_both_led_diffs.csv')
# df = data_with_both_led_diffs  # Use your actual dataframe variable here

# Convert 'time' to datetime for easier manipulation and create a 'time_seconds' column for easier calculations
df['time_dt'] = pd.to_timedelta(df['time'])
df['time_seconds'] = df['time_dt'].dt.total_seconds()

# Define time windows in seconds
time_windows = [5*60, 10*60, 20*60]  # 5 minutes, 10 minutes, 20 minutes in seconds

# Initial histogram for the first time window
fig = go.Figure(data=[
    go.Histogram(x=df['time_seconds'], xbins=dict(start=0, end=time_windows[0], size=time_windows[0]))
])

# Update layout and add sliders
fig.update_layout(
    sliders=[
        {
            'steps': [
                {
                    'method': 'restyle',
                    'label': f'{int(window/60)}m',
                    'args': [
                        {'xbins': dict(start=0, end=window, size=window)}
                    ]
                } for window in time_windows
            ]
        }
    ],
    title='Number of Participants Finishing Within Time Frames',
    xaxis_title='Finish Time (Seconds)',
    yaxis_title='Number of Participants'
)

# Show the figure
fig.show()