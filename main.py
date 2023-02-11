import datetime
import requests
import time

now = datetime.datetime.now()
start_date = datetime.date(now.year - 5, 1, 1)
end_date = datetime.date(now.year, now.month, now.day)
period = end_date - start_date
period = int(period.days)
day_list = []

for d in range(period):
    day = start_date + datetime.timedelta(days=d)
    day_list.append(day)

day_list.append(end_date)

# 取得したい企業
specific_company = input()

doc_id_list = []
for day in day_list:
    url = "https://disclosure.edinet-fsa.go.jp/api/v1/documents.json"
    params = {"date": day, "type": 2}
    res = requests.get(url, params=params)
    json_data = res.json()
    time.sleep(2)

    for num in range(len(json_data["results"])):
        company_name = json_data["results"][num]["filerName"]
        if company_name == specific_company:
            doc_id_list.append(json_data["results"][num]["docID"])
    print(day)

for doc_id in doc_id_list:
    url = "https://disclosure.edinet-fsa.go.jp/api/v1/documents/" + doc_id
    params = {"type": 2}
    filename = doc_id + ".pdf"
    res = requests.get(url, params=params, verify=False)
    if res.status_code == 200:
        with open(filename, "wb") as f:
            for chunk in res.iter_content(chunk_size=1024):
                f.write(chunk)
