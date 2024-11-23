import requests

headers = {}

# json_data = {
#     'keyword': '三体',
#     'page': 1,
#     'sensitive': False,
# }
# response = requests.post('https://api.ylibrary.org/api/search/', headers=headers, json=json_data)


json_data = {
    'id': 2817721,
    'source': 'zlibrary',
}

response = requests.post('https://api.ylibrary.org/api/detail/', headers=headers, json=json_data)

print(f"接受到的数据：{response.json()}")