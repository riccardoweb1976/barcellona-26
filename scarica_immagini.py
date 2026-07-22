#!/usr/bin/env python3
"""
Scarica automaticamente un'immagine libera da Wikimedia Commons per ogni
attrazione dell'itinerario di Barcellona.

- Cerca su Commons con una parola chiave (non serve conoscere il nome esatto
  del file), prende il primo risultato immagine valido e lo scarica.
- Salva i file in ./immagini/ come sagrada-familia.jpg, park-guell.jpg, ecc.
- Crea immagini/CREDITI.txt con autore, licenza e link fonte di ogni immagine
  (serve per rispettare le licenze Creative Commons: cita sempre l'autore).

Uso:   python3 scarica_immagini.py
Solo libreria standard di Python 3, nessuna installazione necessaria.
"""
import json, os, re, urllib.request, urllib.parse

# nome-file-locale : termine di ricerca su Wikimedia Commons
ATTRAZIONI = {
    "sagrada-familia":   "Sagrada Familia Barcelona exterior",
    "park-guell":        "Park Güell Barcelona",
    "casa-batllo":       "Casa Batlló Barcelona facade",
    "casa-mila":         "Casa Milà La Pedrera Barcelona",
    "mnac":              "Palau Nacional MNAC Barcelona",
    "museo-picasso":     "Museu Picasso Barcelona",
    "castell-montjuic":  "Castell de Montjuïc Barcelona",
    "la-boqueria":       "Mercat de la Boqueria Barcelona",
    "hospital-sant-pau": "Hospital de Sant Pau Barcelona",
    "font-magica":       "Font màgica Montjuïc Barcelona",
    "cattedrale":        "Barcelona Cathedral facade",
    "port-olimpic":      "Port Olímpic Barcelona",
}

API = "https://commons.wikimedia.org/w/api.php"
UA  = "BarcellonaSitoScript/1.0 (progetto personale; contatto: uso-privato)"

def api(params):
    params["format"] = "json"
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def cerca_file(termine):
    """Restituisce il titolo del primo file immagine trovato per il termine."""
    d = api({
        "action": "query", "list": "search", "srsearch": termine,
        "srnamespace": "6", "srlimit": "10",   # namespace 6 = File
    })
    for hit in d["query"]["search"]:
        t = hit["title"]
        if re.search(r"\.(jpe?g|png)$", t, re.I):
            return t
    return None

os.makedirs("immagini", exist_ok=True)
crediti = []

for nome, termine in ATTRAZIONI.items():
    try:
        titolo = cerca_file(termine)
        if not titolo:
            print(f"NESSUN RISULTATO per {nome} ({termine})"); continue
        d = api({
            "action": "query", "titles": titolo, "prop": "imageinfo",
            "iiprop": "url|extmetadata", "iiurlwidth": "1600",
        })
        info = next(iter(d["query"]["pages"].values()))["imageinfo"][0]
        src = info.get("thumburl") or info["url"]
        meta = info.get("extmetadata", {})
        autore = re.sub("<[^>]+>", "", meta.get("Artist", {}).get("value", "Sconosciuto")).strip()
        licenza = meta.get("LicenseShortName", {}).get("value", "?")
        ext = ".jpg" if re.search(r"jpe?g", src, re.I) else ".png"
        dest = f"immagini/{nome}{ext}"
        req = urllib.request.Request(src, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as r, open(dest, "wb") as f:
            f.write(r.read())
        crediti.append(f"{dest}\n  Attrazione: {nome}\n  Fonte: {info['descriptionurl']}\n  Autore: {autore}\n  Licenza: {licenza}\n")
        print(f"OK  {dest}  <- {titolo}")
    except Exception as e:
        print(f"ERRORE su {nome}: {e}")

with open("immagini/CREDITI.txt", "w", encoding="utf-8") as f:
    f.write("CREDITI IMMAGINI — Wikimedia Commons\n")
    f.write("Cita sempre autore e licenza come indicato qui sotto.\n")
    f.write("=" * 45 + "\n\n" + "\n".join(crediti))

print("\nFatto. Guarda la cartella immagini/ e il file CREDITI.txt")
