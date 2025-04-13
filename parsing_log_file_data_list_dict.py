"""
Problem: You're given a simplified version of a server log file as a list of strings. Each log line follows this format:
        
        <timestamp> <log_level> <user_id> <action>

        logs = [
    "2025-04-11T12:00:00Z INFO user123 login",
    "2025-04-11T12:01:05Z INFO user123 view_page",
    "2025-04-11T12:03:45Z ERROR user123 crash",
    "2025-04-11T12:04:00Z INFO user456 login",
    "2025-04-11T12:06:00Z INFO user456 logout",
    "2025-04-11T12:07:00Z INFO user123 logout"
]

    1. Parse the log lines into structured data (dicts or objects).
    2. Write a function to return:
        A dictionary mapping user_id to their actions in order.
        A count of how many ERROR logs occurred overall.
    3. (Bonus) Return the total session duration per user (from login to logout).

Sample Output:

    {
    'user123': ['login', 'view_page', 'crash', 'logout'],
    'user456': ['login', 'logout']
    }, 
    1, 
    {
    'user123': 420,   # in seconds (from login to logout)
    'user456': 120
    }

    
"""

import pandas as pd
from datetime import datetime, timedelta

logs = [
    "2025-04-11T08:00:00Z INFO user001 login",
    "2025-04-11T08:01:00Z INFO user002 login",
    "2025-04-11T08:01:30Z INFO user001 view_page",
    "2025-04-11T08:02:00Z ERROR user001 crash",
    "2025-04-11T08:02:30Z INFO user003 login",
    "2025-04-11T08:03:00Z INFO user002 view_page",
    "2025-04-11T08:04:00Z INFO user001 logout",
    "2025-04-11T08:05:00Z INFO user003 view_page",
    "2025-04-11T08:05:30Z ERROR user003 crash",
    "2025-04-11T08:06:00Z INFO user002 logout",
    "2025-04-11T08:10:00Z INFO user001 login",
    "2025-04-11T08:12:00Z INFO user001 logout",
    "2025-04-11T08:20:00Z INFO user003 logout"
]

columns = ['user','action','type','timestamp']

#Initialize empty dataframe that will hold log data
df_log_table = pd.DataFrame(columns=columns)

for index,row in enumerate(logs):
    df_log_table.loc[index,'user'] = row.split(" ")[2]
    df_log_table.loc[index,'action'] = row.split(" ")[3]
    df_log_table.loc[index,'type'] = row.split(" ")[1]
    df_log_table.loc[index,'timestamp'] = row.split(" ")[0]

#print(df_log_table.shape, df_log_table.dtypes)
print(df_log_table)

count_errors = (df_log_table['type'].str.lower() == 'error').sum()
print("A count of how many ERROR logs occurred overall")
print(count_errors)

count_errors_by_user = df_log_table[df_log_table['type'].str.lower() == 'error'].groupby('user').size().reset_index(name='error_count')
#print(count_errors_by_user)

#what is session duration = time difference between logout and login
#   1. group by user,action by timestamp in ascending
#   2. split the data by user then find each login/logout part and calculate it's duration
#   3. append to the final dictionary

display_user_order = df_log_table[['user','action','timestamp']].sort_values(by=['user','timestamp'],ascending=True).reset_index(drop=True)
#print(display_user_order)

dict_user = {}
dict_total_user_sessions = {}
dict_total_user_sessions_tot = {}

display_user_order["timestamp"] = pd.to_datetime(display_user_order["timestamp"])

#let's split the data by user first
for user, user_df in display_user_order.groupby("user"):
    #print(user)
    #print(user_df)

    actions = []
    session_times = []
    login_time = None
    duration = 0
    duration_tot = 0

    for _, row in user_df.iterrows():
        action = row["action"]
        actions.append(action)

        if action == 'login':
            login_time = row["timestamp"]
        elif action == 'logout' and login_time:
            duration = (row["timestamp"] - login_time).total_seconds()
            session_times.append(duration)
            duration_tot += duration
            login_time = None
    
    dict_user[user] = actions
    dict_total_user_sessions[user] = session_times
    dict_total_user_sessions_tot[user] = duration_tot

print("==========")
print("A dictionary mapping user_id to their actions in order.")
print(dict_user)
print("Total session duration per user (from login to logout).")
print(dict_total_user_sessions)
print(dict_total_user_sessions_tot)