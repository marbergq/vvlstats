import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import os
from tqdm import tqdm


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
mapping = {
    'högsta_punkten': 'https://results.vasaloppet.se/2024/index.php?event=VL_HCH8NDMR2400&num_results=100&pid=list&ranking=time_04&search%5Bsex%5D={sex}&search%5Bage_class%5D=%25&search%5Bnation%5D=%25',
    'smågan': 'https://results.vasaloppet.se/2024/index.php?event=VL_HCH8NDMR2400&num_results=100&pid=list&ranking=time_01&search%5Bsex%5D={sex}&search%5Bage_class%5D=%25&search%5Bnation%5D=%25',
    'mångsbodarna': 'https://results.vasaloppet.se/2024/index.php?event=VL_HCH8NDMR2400&num_results=100&pid=list&ranking=time_05&search%5Bsex%5D={sex}&search%5Bage_class%5D=%25&search%5Bnation%5D=%25',
    'evertsberg': 'https://results.vasaloppet.se/2024/index.php?event=VL_HCH8NDMR2400&num_results=100&pid=list&ranking=time_15&search%5Bsex%5D={sex}&search%5Bage_class%5D=%25&search%5Bnation%5D=%25',
    'oxberg': 'https://results.vasaloppet.se/2024/index.php?event=VL_HCH8NDMR2400&num_results=100&pid=list&ranking=time_20&search%5Bsex%5D={sex}&search%5Bage_class%5D=%25&search%5Bnation%5D=%25',
    'hökberg': 'https://results.vasaloppet.se/2024/index.php?event=VL_HCH8NDMR2400&num_results=100&pid=list&ranking=time_25&search%5Bsex%5D={sex}&search%5Bage_class%5D=%25&search%5Bnation%5D=%25',
    'eldris': 'https://results.vasaloppet.se/2024/index.php?event=VL_HCH8NDMR2400&num_results=100&pid=list&ranking=time_30&search%5Bsex%5D={sex}&search%5Bage_class%5D=%25&search%5Bnation%5D=%25',
}
sexes = {'M':'men', 'W':'wmn'}
for gender_key, folder in tqdm(sexes.items(), 'genders'):
    for checkpoint, url in tqdm(mapping.items(), f'{gender_key}/checkpoints'):
        foldr = f'{folder}/checkpoints/{checkpoint}'
        isExist = os.path.exists(foldr)
        if not isExist:
            os.makedirs(foldr)
        
        if os.path.exists(f"{foldr}/results.csv"):
            continue
        base_url = url.format(sex=gender_key)
        # print(base_url)
        first = requests.get(base_url + '&page=1')

        soup = BeautifulSoup(first.text, 'html.parser')
        pagination = soup.find('ul', {'class': 'pagination'})
        last_page = int(pagination.find_all('li')[-2].text)


        for i in tqdm(range(1, last_page+1),f'{checkpoint}/pages'):
            text = ''
            if os.path.exists(f"{foldr}/response_page_{i}.html"):
                with open(f"{foldr}/response_page_{i}.html", "r") as f:
                    text = f.read()
            else:
            # with open(f"response.html", "r") as f:
                res = requests.get(base_url + "&page="+ str(i))
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