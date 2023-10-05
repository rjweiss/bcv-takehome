import csv
import json
import os
import requests
import time
import uuid


def main():
  
  writer = csv.writer(open('investors-not-found.csv', 'w'))
  writer.writerow(['id', 'name', 'link'])

  #url = 'https://api.crunchbase.com/api/v4/entities/organizations/'
  #url = 'https://api.crunchbase.com/api/v4/entities/people/'
  headers={
    "accept": "application/json",
    "x-cb-user-key": os.environ['CBASE_API_KEY']
  }
  params={
    #"card_ids": "categories"
  }

  reader = open('notfound.txt')
  for line in reader:
    u = uuid.UUID(line.strip())

    r = requests.get(f"{url}/{str(u)}", params=params, headers=headers)
    
    delay = 1
    while r.status_code == 429:
      delay = delay * 2
      print("wait", delay)
      time.sleep(delay)
      r = requests.get(f"{url}/{str(u)}", params=params, headers=headers)
    if r.status_code == 404:
      print(u, "not found")
      continue
    else:
      r.raise_for_status()
    
    j = r.json()
    print(r)
    if "properties" in j:
      print(u, "ok")
      i = j["properties"]["identifier"]
      writer.writerow([i["uuid"], i["value"], i["permalink"]])
    else:
      print(u, "error")
    time.sleep(1)


if __name__ == "__main__":
  main()
