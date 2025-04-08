import pandas as pd
from dateutil import parser

data = {
    "customer_id": [101, 102, 103, 101, 104, 105, 102],
    "amount": [200, None, 300, 200, None, 150, 500],
    "date": ["01/03/2024", "2024-02-10", "03-15-2024", "01/03/2024", "2024-01-29", None, "10-05-2023"]
}

df = pd.DataFrame(data)

print(df)

"""Challenge clean DF with
    -no duplicate rows
    -missing amount value filled with median
    -dates standardize to YYYY-MM-DD
"""
df = df.drop_duplicates()
print("Dropped Duplicates:\n",df)

#median = df["amount"].median()
#print("Amount median:",median)

df["amount"] = df["amount"].fillna(df["amount"].median())
print("missing amount value filled with median:\n",df)


print(df.dtypes)

#1. Convert object to datetime: pd.to_datetime()
#2. Format date: .dt.strftime()

# Function to parse mixed date formats
def parse_date(date):
    try:
        return parser.parse(date).strftime("%Y-%m-%d")  # Standardize format
    except (TypeError, ValueError):
        return None  # Return None for invalid/missing dates

# Apply function to the "date" column
df["date"] = df["date"].apply(parse_date)

print("Dates standardized to YYYY-MM-DD:\n", df)
