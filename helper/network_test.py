import requests

url = "https://justizonline.gv.at/jop/api/at.gv.justiz.fbw/ws/fbw.wsdl"
response = requests.get(url, timeout=10)
print(response.status_code)
print(response.text[:500])  # print first 500 characters
