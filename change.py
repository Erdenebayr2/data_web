from datetime import date, datetime, timedelta
import aiohttp,asyncio,json
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
from apartment import main
import pandas as pd

asyncio.run(main())
with open("data.json", "r") as json_file:
    data = json.load(json_file)

df = pd.DataFrame.from_dict(data, orient='index')
df.to_csv('data.csv', index_label='ID')

try:
    with open("data.csv", "r", encoding="utf-8") as csv_file:
        data = pd.read_csv(csv_file)
except UnicodeDecodeError:
    with open("data.csv", "r", encoding="latin1") as csv_file:
        data = pd.read_csv(csv_file)

data = data.drop(
    ["ID"], axis=1
)

data["price"] = data["price"].fillna(value=0).astype(int)

data.to_csv("modified_data.csv", index=False, encoding='utf-8')
data = pd.read_csv("modified_data.csv", encoding='utf-8')
data.to_excel("modified_data.xlsx", index=False, engine='openpyxl')