import re
import requests
import time

# Fichier HTML à modifier
html_file = 'GW2/GW2.html'

# Lire le contenu du fichier HTML
with open(html_file, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Expression régulière pour extraire les IDs des divs
div_regex = re.compile(r'id="(emote-\d+)" class="all" title="([^"]+)" src="#" loading="lazy" alt="[^"]+"')

# Trouver toutes les correspondances
matches = div_regex.findall(html_content)

# Dictionnaire pour stocker les URLs des images
image_urls = {}

# Obtenir les URLs des images depuis l'API
for match in matches:
    skin_id = match[0]
    name = match[1]
    id_number = skin_id.split('-')[1]
    api_url = f'https://api.guildwars2.com/v2/items/{id_number}'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        image_urls[skin_id] = data.get('icon', '')
    time.sleep(0.1)

# Remplacer les divs dans le contenu HTML
def replace_div(match):
    skin_id = match.group(1)
    name = match.group(2)
    img_url = image_urls.get(skin_id, '')
    if img_url:
        img_tag = f'title="{name}" src="{img_url}" loading="lazy" alt="{name}"'
    else:
        img_tag = ''
    return f'id="{skin_id}" class="all" {img_tag}'
    
# Faire le remplacement dans le contenu HTML
new_html_content = div_regex.sub(replace_div, html_content)

# Écrire le nouveau contenu HTML dans le fichier
with open(html_file, 'w', encoding='utf-8') as file:
    file.write(new_html_content)

print("Modification terminée!")
