headers = {
    'Accept': 'application/vnd.github+json',
}

response = requests.get('https://api.github.com/rate_limit', headers=headers)
response.raise_for_status()  # Raise error for bad responses

print(response.text)