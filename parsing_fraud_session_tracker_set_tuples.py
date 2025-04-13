"""
Problem: You're given a list of login events in the form of tuples:

    (user_id: str, ip_address: str, device: str, timestamp: str)

    1. Deduplicate the logs (remove exact duplicates).
    2. For each user, find all (IP, device) pairs they used to log in.
    3. Check for Suspicious Users: If a user logs in from more than 3 unique IPs and/or 
        more than 2 different devices in a 24-hour window, flag them as suspicious.
        (Handle Time Windows: You can use datetime to compute whether the logins occurred within 24 hours of each other.)

Example Input:
logs = [
    ('alice', '192.168.1.2', 'iPhone', '2025-04-11T08:00:00Z'),
    ('alice', '192.168.1.3', 'iPad', '2025-04-11T09:00:00Z'),
    ('alice', '192.168.1.4', 'MacBook', '2025-04-11T10:00:00Z'),
    ('alice', '192.168.1.5', 'iPhone', '2025-04-11T11:00:00Z'),
    ('bob',   '10.0.0.1',    'Windows', '2025-04-10T08:00:00Z'),
    ('bob',   '10.0.0.1',    'Windows', '2025-04-10T08:00:00Z'),  # duplicate
    ('bob',   '10.0.0.2',    'Windows', '2025-04-10T08:30:00Z'),
    ('carol', '172.16.0.3',  'Linux', '2025-04-11T07:59:59Z'),
    ('carol', '172.16.0.4',  'Linux', '2025-04-11T08:00:01Z'),
    ('carol', '172.16.0.5',  'Linux', '2025-04-11T08:01:01Z'),
    ('carol', '172.16.0.6',  'Linux', '2025-04-11T08:03:01Z')
]

Expected output:
    Suspicious users:
    ['alice', 'carol']

    Alice → 4 IPs, 3 devices, within a short span.
    Carol → 4 IPs, 1 device, all within 4 minutes — flagged for IP hopping.
"""

from collections import defaultdict
from datetime import datetime, timedelta

logs = [
    ('alice', '192.168.1.2', 'iPhone', '2025-04-11T08:00:00Z'),
    ('alice', '192.168.1.3', 'iPad', '2025-04-11T09:00:00Z'),
    ('alice', '192.168.1.4', 'MacBook', '2025-04-11T10:00:00Z'),
    ('alice', '192.168.1.5', 'iPhone', '2025-04-11T11:00:00Z'),
    ('bob',   '10.0.0.1',    'Windows', '2025-04-10T08:00:00Z'),
    ('bob',   '10.0.0.1',    'Windows', '2025-04-10T08:00:00Z'),  # duplicate
    ('bob',   '10.0.0.2',    'Windows', '2025-04-10T08:30:00Z'),
    ('carol', '172.16.0.3',  'Linux', '2025-04-11T07:59:59Z'),
    ('carol', '172.16.0.4',  'Linux', '2025-04-11T08:00:01Z'),
    ('carol', '172.16.0.5',  'Linux', '2025-04-11T08:01:01Z'),
    ('carol', '172.16.0.6',  'Linux', '2025-04-11T08:03:01Z')
]
print("="*40)

#Convert list of tuples to set to remove duplicate
logs_set = set(logs)
print("Set of tuples (deduplicated):\n",logs_set)

#Initialize dictionary that holds list
logs_dict_set = defaultdict(list)

#Here I am using "logs_set" i.e. set of tuples hence dict will not have duplicates but if we wanted to keep the duplicates then
#we should use "logs" i.e. list of tuples that contain duplicates
for user,ip,machine,timestamp in logs_set:
    timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    logs_dict_set[user].append((ip,machine,timestamp))

# Convert defaultdict to regular dict (optional)
logs_dict_set = dict(logs_dict_set)

print("="*40)
print("Each user unique IP, device:")
for user,entries in logs_dict_set.items():
    unique_IP_user = set(ip for ip, _,_ in entries) #Note: the "_" position is important here because the tuple is ordered
                                                # and ip comes first then machine in the set
    unique_machine_user = set(machine for _,machine,_ in entries)
    print(f"{user}:{unique_IP_user}:{unique_machine_user}")

print("="*40)
#Check for Suspicious Users:
print("Check for Suspicious Users:")
#print(logs_dict_set.keys(),"\n",logs_dict_set.values())


for user,entries in logs_dict_set.items():

    # Sort user entries by time
    sorted_entries = sorted(entries, key=lambda x: x[2])
    window_start = sorted_entries[0][2]
    window_end = window_start + timedelta(hours=24)

    # Filter entries in 24-hour window
    filtered = [(ip, machine) for ip, machine, timestamp in sorted_entries if window_start <= timestamp < window_end]

    #create unique IP and device set of each user
    unique_IP_user = set(ip for ip, _ in filtered) 
    unique_machine_user = set(machine for _,machine in filtered)
    #print(f"{user}:",unique_IP_user,unique_machine_user,"\n")

    if len(unique_IP_user) > 3 or len(unique_machine_user) > 2:
        print("Supicious User: ",user)

