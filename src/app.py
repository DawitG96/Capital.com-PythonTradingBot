import os
import sys
import argparse

from database import Database
from dotenv import load_dotenv
from data_fetcher import fetch_trading, fetch_news
from downloaders import CapitalDownloader

# Controllo se le variabili d'ambiente sono state impostate
if not os.getenv("APP_TRADING_BOT"):
    print("Variabili di ambiente non impostate. Caricamento dal file .env...")
    if not load_dotenv():
        print("❌\tFile .env non trovato.\nCopia il file .env.example in .env e imposta le variabili d'ambiente.")
        exit(1)

# Configurazioni iniziali
DB_URL = os.getenv("APP_DB_URL")
NEWS_APIKEY = os.getenv("NEWS_APIKEY")
CAPITAL_APIKEY = os.getenv("CAPITAL_APIKEY")
CAPITAL_EMAIL = os.getenv("CAPITAL_EMAIL")
CAPITAL_PASSWORD = os.getenv("CAPITAL_PASSWORD")


# ======= Main =======
arg = argparse.ArgumentParser(description="Bot di trading")
grp = arg.add_argument_group()
grp.add_argument("-e", "--epics", help="Epic dei dati da scaricare, lasciare vuoto per tutti", nargs="*")
grp.add_argument("-t", "--timeframe", help="Timeframe dei dati da scaricare, lasciare vuoto per DAY", nargs="*", choices=CapitalDownloader.get_timeframe_limit(), default=["DAY"])
arg.add_argument("-n", "--news", help="Scarica le news", action="store_true")
arguments = arg.parse_args()

if not len(sys.argv) > 1:
    print("❌ Nessun comando specificato. Utilizzare -h per visualizzare l'help.")
    exit(1)

try:
    database = Database(DB_URL)
    arguments.epics != None and fetch_trading(database, arguments.epics, arguments.timeframe)
    arguments.news and fetch_news(database)
except KeyboardInterrupt:
    print("\n❌ Operazione annullata dall'utente.")
