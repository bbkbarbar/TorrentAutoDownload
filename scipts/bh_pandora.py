import os
import requests
import transmission_rpc

# Transmission kapcsolat
tc = transmission_rpc.Client(
    host="127.0.0.1",     # ha a Transmission ugyanazon a gépen fut egyéb esetben a transmisson-t futtató gép címe
    port=9092,            
    username="<your_transmission_user>",    
    password="<your_transmission_pw>"    
)

# --- CONFIG ---
#SEARCH_URL = "https://bithumen.be/browse.php?search=sorozatnev+1080p"  
BITCOOKIE = "uid=123456; pass=d66xxxxxxxxxxxxxxxxxxxxxxxxxd202" # << your bithumen cookie from chrome

TITLE = "Pandóra szellentése"                              # Barmilyen cim, csak hogy a konzolban latszon, melyiket csinalja, ha tobb is van
SEARCH_URL = "https://bithumen.be/browse.php?c23=1&c7=1&genre=0&search=Pand%F3ra&vxx=3a330"   # rakeresel az oldalon (lehetőleg leszűrve csak arra a ketegóriára ami releváns), majd copy a TELJES url-t
LAST_FILE = "d:\\TorrentLoader\\last_seen_pandora.txt"     # adott sorozathoz tartotó szövegfájl amiben tároljuk, melyiket töltöttük le legutóbb
DOWNLOAD_DIR = r"n:\Media\Sorozatok\Pandóra szelencéje"    # hova töltse a tartalmat (a transmisson-ben használható path)
# --- /CONFIG ---

def get_last_id():
    if os.path.exists(LAST_FILE):
        with open(LAST_FILE, "r") as f:
            return f.read().strip()
    return "0"

def set_last_id(tid):
    with open(LAST_FILE, "w") as f:
        f.write(str(tid))

def download_and_add(torrent_id, download_dir):
    url = f"https://bithumen.be/download.php/{torrent_id}/file.torrent"
    headers = {"Cookie": BITCOOKIE}
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
        torrent_data = resp.content
        # közvetlenül átadjuk Transmission-nek
        tc.add_torrent(torrent_data, download_dir=download_dir)
        print(f"Torrent ID {torrent_id} hozzáadva ({download_dir})")
    else:
        print(f"Hiba a torrent letöltésénél: {resp.status_code}")

def main():
    print(TITLE +" keresése")
    last_id = int(get_last_id())

    url = SEARCH_URL  # vagy saját szűrt link
    headers = {"Cookie": BITCOOKIE}
    resp = requests.get(url, headers=headers)

    if resp.status_code != 200:
        print("Nem tudtam lekérni az RSS-t")
        return

    # parsing: csak torrent ID-kat keres
    ids = []
    for line in resp.text.splitlines():
        if "download.php/" in line:
            try:
                tid = line.split("download.php/")[1].split("/")[0]
                ids.append(int(tid))
            except:
                pass

    new_ids = [tid for tid in ids if tid > last_id]
    if new_ids:
        print("Új torrentek:", new_ids)
        for tid in new_ids:
            try:
                download_and_add(tid, DOWNLOAD_DIR)
                set_last_id(tid)
            except Exception as e:
                print(f"Hiba az ID={tid} feldolgozásánál: {e}")
    else:
        print("Nincs új torrent.")

    print("Kész.")

if __name__ == "__main__":
    main()