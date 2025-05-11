import urllib.request
import json
import os

# attention, ce code ne fournit pas de clé d'accès sur le répèrtoire Github, les requêtes sont donc limité en h, si trop de demande, ce code ne fonctionnera plus

OWNER = "argentrocher"
REPO = "calculatrice-windows.exe"
API_URL = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/"
COMMITS_URL = f"https://api.github.com/repos/{OWNER}/{REPO}/commits?path="
COMMITS_URL1 = f"https://api.github.com/repos/{OWNER}/{REPO}/commits"

def github_api_request(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())

def get_last_modified_global():
    commits = github_api_request(COMMITS_URL1)
    if commits:
        latest_commit = commits[0]
        return latest_commit['commit']['committer']['date']
    return "Inconnu"

def get_last_modified(filename):
    url = COMMITS_URL + filename
    commits = github_api_request(url)
    if commits:
        return commits[0]['commit']['committer']['date']
    return "Inconnu"

def get_github_files():
    return github_api_request(API_URL)

def download_file(file_info):
    download_url = file_info['download_url']
    filename = file_info['name']

    print(f"Téléchargement de {filename}...")
    req = urllib.request.Request(download_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        content = response.read()

    with open(filename, 'wb') as f:
        f.write(content)
    print(f"✅ Fichier '{filename}' téléchargé avec succès.")

def main():
    print(f"📦 Informations sur le dépôt GitHub {REPO}:")
    last_global = get_last_modified_global()
    print(f"📅 Dernière modification globale du dépôt : {last_global}\n")
    
    files = get_github_files()
    print("📁 Fichiers dans le dépôt :")
    for file in files:
        modified = get_last_modified(file['name'])
        print(f" - {file['name']} | Dernière modification : {modified}")

    while True:
        cmd = input("\nTapez 'save nom_du_fichier' pour télécharger, ou 'exit' pour quitter : ").strip()
        if cmd == "exit":
            print("👋 Fin du programme.")
            break
        if cmd == "version" or cmd == "v":
            print("version 0.1, tout droit réservé à argentropcher, assigné au compte Google argentropcher,\nmodification autorisé (se code s'adapte à tout les dépots Github facilement et peut être modifier librement)")
            continue
        if cmd.startswith("save "):
            filename = cmd[5:]
            found = False
            for file in files:
                if file['name'] == filename:
                    download_file(file)
                    found = True
                    break
            if not found:
                print("❌ Fichier non trouvé.")
        else:
            print("❗ Commande invalide. Utilisez : save nom_du_fichier ou exit.")


main()
