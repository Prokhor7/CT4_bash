import urllib.parse
import json
import requests
import csv
from dynamodb_json import json_util as ujson
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

main_part = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchangenew?json&'


date = '20210001'

data = []
exchange_list = []
n = 12
for i in range(n):


  date = str(int(date)+100)
  url = main_part + urllib.parse.urlencode({'date':date})


  response = requests.get(url)
  json_list = response.json()


  data.append(json_list)

  for i in range(len(json_list)):
    if(json_list[i]["cc"] in ("USD", "EUR")):

      record = {
        "PutRequest": {
            "Item": json.loads(ujson.dumps(json_list[i]))
        }
      }
      exchange_list.append(record)

exchange = {"ExchangeRatesCLI" : exchange_list}

with open('exchange.json', 'w') as json_file:
  json_file.write(json.dumps(exchange, ensure_ascii=False, indent = 4))


for i in range(n):
  with open(f'exchange{i+1}.csv', 'w') as f:
    writer = csv. DictWriter(f, data[0][0].keys())
    writer.writeheader()

    for currency in data[i]:
      writer.writerow(currency)

usd = []
eur = []
for i in range(n):
  df = pd.read_csv(f'exchange{i+1}.csv', index_col = 'r030') 
  dollar = df[df['cc'] == 'USD']['rate']
  usd.append(dollar.values[0])
  euro = df[df['cc'] == 'EUR']['rate']
  eur.append(euro.values[0])

print(usd)
print(eur)


x = [i+1 for i in range(n)]
y = np.array(usd)
plt.plot(x, y, label='USD', color="green")

x = [i+1 for i in range(n)]
z = np.array(eur)
plt.plot(x, z, label='EUR', color="blue")

plt.title("Hrivnya exchange rates")
plt.legend()
plt.xticks(np.arange(min(x), max(x)+1, 1.0))
plt.yticks(np.arange(round(min(y)), round(max(z))+1, 1.0))
plt.savefig('exchange_rates.png')
plt.show()
