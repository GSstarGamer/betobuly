import requests
import pprint
headers = {
    'Accept': 'application/vnd.github+json',
}
response = requests.get('https://api.github.com/repos/GSstarGamer/betobuly/releases/tags/v1-updater', headers=headers)

pprint.pprint(response.json())