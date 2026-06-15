
import os
import requests

usuario = "isairey"
token = ""  # o deja None si no tienes



headers = {"Authorization": f"token {token}"} if token else {}

total_stars = 0
page = 1

while True:
    repos_url = f"https://api.github.com/users/{usuario}/repos?per_page=100&page={page}"
    repos = requests.get(repos_url, headers=headers).json()

    if not repos or "message" in repos:  # si ya no hay más páginas
        break

    for repo in repos:
        nombre = repo["name"]
        stars = repo["stargazers_count"]
        total_stars += stars
        if stars > 0:
            print(f"⭐ Repo: {nombre} → {stars} estrellas")

    page += 1

print(f"\n🌟 Total de estrellas en tu cuenta: {total_stars}")



# Endpoint de eventos del usuario
url = f"https://api.github.com/users/{usuario}/events"
eventos = requests.get(url, headers=headers).json()

for ev in eventos:
    if ev["type"] == "WatchEvent":  # WatchEvent = alguien dio estrella
        repo = ev["repo"]["name"]
        quien = ev["actor"]["login"]
        fecha = ev["created_at"]
        print(f"⭐ Última estrella: {quien} → {repo} en {fecha}")
        break
