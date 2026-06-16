import requests

usuario = "isairey"
token = ""

headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.star+json"
} if token else {
    "Accept": "application/vnd.github.star+json"
}

# =========================
# 🔥 1. Obtener repos
# =========================
# =========================
# 🔥 1. Obtener TODOS los repos (PAGINACIÓN REAL)
# =========================
repos = []
page = 1

while True:
    repos_url = f"https://api.github.com/user/repos?per_page=100&page={page}"

    response = requests.get(repos_url, headers=headers, timeout=20)

    if response.status_code != 200:
        print("Error API:", response.json())
        break

    data = response.json()

    if not data:
        break

    repos.extend(data)
    page += 1

repos_con_estrellas = []
ultimas_estrellas = []

# =========================
# 🔁 2. Analizar repos (SOLO CON ESTRELLAS)
# =========================
for repo in repos:
    nombre = repo["name"]
    stars = repo["stargazers_count"]

    if stars <= 0:
        continue  # ❌ IGNORA repos sin estrellas

    repos_con_estrellas.append({
        "name": nombre,
        "stars": stars
    })

    # =========================
    # ⭐ Obtener stargazers (fecha)
    # =========================
    stars_url = f"https://api.github.com/repos/{usuario}/{nombre}/stargazers"
    stargazers = requests.get(stars_url, headers=headers).json()

    if isinstance(stargazers, list):
        for s in stargazers:
            if "starred_at" in s:
                ultimas_estrellas.append({
                    "repo": nombre,
                    "user": s["user"]["login"],
                    "date": s["starred_at"]
                })

# =========================
# 📌 3. SOLO REPOS CON ESTRELLAS
# =========================
print("\n⭐ Repos con estrellas:")

if not repos_con_estrellas:
    print("No tienes repos con estrellas 😢")
else:
    for r in repos_con_estrellas:
        print(f"- {r['name']} → {r['stars']} ⭐")

# =========================
# 🔝 4. TOP 3
# =========================
top3 = sorted(repos_con_estrellas, key=lambda x: x["stars"], reverse=True)[:3]

print("\n🔥 Top 3 repos con más estrellas:")
for i, r in enumerate(top3, 1):
    print(f"{i}. {r['name']} → {r['stars']} ⭐")

# =========================
# ⏱ 5. ÚLTIMA ESTRELLA
# =========================
if ultimas_estrellas:
    ultima = sorted(ultimas_estrellas, key=lambda x: x["date"], reverse=True)[0]

    print("\n🚀 Última estrella recibida:")
    print(f"Repo: {ultima['repo']}")
    print(f"Usuario: {ultima['user']}")
    print(f"Fecha: {ultima['date']}")
else:
    print("\n⚠️ No se pudieron obtener eventos de estrellas recientes")