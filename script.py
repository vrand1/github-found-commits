import os
import requests

OWNER = os.getenv("OWNER")
REPO = os.getenv("REPO")
BRANCH = os.getenv("BRANCH")
TOKEN = os.getenv("GITHUB_TOKEN")

headers = {"Accept": "application/vnd.github+json"}
if TOKEN:
    if TOKEN.startswith("ghp_"):
        headers["Authorization"] = f"token {TOKEN}"
    else:
        headers["Authorization"] = f"Bearer {TOKEN}"

needle = "правк"
page = 1
session = requests.Session()

print(f"Ищу коммиты с вхождением '{needle}' в {OWNER}/{REPO}@{BRANCH}\n")

total_found = 0

while True:
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/commits"
    params = {"sha": BRANCH, "per_page": 100, "page": page}

    resp = session.get(url, headers=headers, params=params)
    if resp.status_code != 200:
        print("GitHub вам отказал:", resp.status_code, resp.text)
        break

    commits = resp.json()
    if not commits:
        break

    for c in commits:
        msg = c["commit"]["message"]
        if needle.lower() in msg.lower():
            total_found += 1
            sha = c["sha"][:7]
            date = c["commit"]["author"]["date"]
            print(f"{date} | {sha} | {msg.splitlines()[0]}")
            print(f"→ {c['html_url']}\n")

    page += 1

print(f"\nИтого найдено коммитов с '{needle}': {total_found}")
