import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
 
from tqdm import tqdm

url = "https://results.vasaloppet.se/2024/index.php?event=VL_HCH8NDMR2400&num_results=100&pid=list&ranking=time_finish_brutto&search%5Bsex%5D=W&search%5Bage_class%5D=%25&search%5Bnation%5D=%25&page="

lookup = {
    # 'gender-place': {'type': 'div','class': 'type-row_num'},
    'gender-place': {'class':'place-primary', 'type':'div'},
    'name': {'class': 'type-fullname', 'type':'h4'},
    'time': {'class': 'type-time', 'type':'div', 'index': 0, 'apply': lambda x: x.replace('Finish', '')},
    'diff': {'class': 'type-time', 'type':'div', 'index': 1, 'apply': lambda x: x.replace('Diff', '')},
}

# Create a DataFrame from the extracted data
df = pd.DataFrame([], columns=[
    'total-place', 'gender-place', 'name', 'time', 'diff'
])

foldr = 'wmn/checkpoints/finish'

for i in tqdm(range(1, 25)):
    # with open(f"response.html", "r") as f:
    res = requests.get(url + str(i))
    text = res.text
    with open(f"{foldr}/response_page_{i}.html", "w") as f:
        f.write(text)
    soup = BeautifulSoup(text, 'html.parser')
    results = soup.find_all('li', {"class": "list-group-item"})
    for idx in results[2:]:
        result = {}
        for k,v in lookup.items():
            all_res = idx.find_all(v['type'], {'class':v['class']})
            res = ''
            if v.get('index'):
                res = all_res[v['index']].text
            else:
                res = all_res[0].text
            if v.get('apply'):
                res = v['apply'](res)
            result[k] = res
        df = df._append(result, ignore_index=True)
df.to_csv(f'{foldr}/results.csv', index=False)