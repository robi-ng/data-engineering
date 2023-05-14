"""
This script displays a graph to show the number of cases in Singapore
over time using the APIs from https://covid19api.com
"""

import matplotlib.pyplot as plt
import pandas as pd
import requests
from matplotlib.ticker import StrMethodFormatter

endpoint = "https://api.covid19api.com/country/singapore/status/confirmed"
result = requests.get(endpoint).json()

df = pd.DataFrame(result, columns=["Date", "Cases"])
df.Date = pd.to_datetime(df.Date)
df.set_index("Date", inplace=True)

ax = df.plot(title="Cumulative Confirmed Cases in Singapore")
ax.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
plt.show()
