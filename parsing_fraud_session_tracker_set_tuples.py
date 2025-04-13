"""
Problem: You're given a list of login events in the form of tuples:

    (user_id: str, ip_address: str, device: str, timestamp: str)

    1. Deduplicate the logs (remove exact duplicates).
    2. For each user, find all (IP, device) pairs they used to log in.
    3. Identify suspicious users who have logged in from more than:
        -3 unique IPs
        -2 different devices
        -within a 24-hour window

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

#Convert list of tuples to set to remove duplicate
logs_set = set(logs)
print("Set of tuples:\n",logs_set)

#Initialize dictionary that holds list
logs_dict_set = defaultdict(list)

#Here I am using "logs_set" i.e. set of tuples hence dict will not have duplicates but if we wanted to keep the duplicates then
#we should use "logs" i.e. list of tuples that contain duplicates
for user,ip,machine,timestamp in logs_set:
    logs_dict_set[user].append((ip,machine))

logs_dict_set = dict(logs_dict_set)

for user,entries in logs_dict_set.items():
    print(f"{user}:{entries}")


