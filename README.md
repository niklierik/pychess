# PyChess

Sakk Pythonban

## Követelmények:

- Python 3.10.6
- pipenv (ajánlott, de nem szükséges)
- Stockfish

## Gép, amin készült:

- OS: KDE Neon (Ubuntu alapú)
- Screen: 1920 x 1080
- CPU: AMD 64x (AMD Ryzen 5 3500x)
- RAM: 16 GB
- GPU: NVIDIA RTX 3600

## Telepítés

Van lehetőségünk pipenv-vel telepíteni a

`pipenv install`

paranccsal, vagy pedig a requirements.txt használatával

`pip install -r requirements.txt`

### Stockfish telepítése:

A projekt többféle Stockfish-sel jön (ezeket a stockfish_versions mappában találod). Manuálisan válasszuk ki, hogy melyik változatot szeretnénk használni. Ezt a main.py fájl mellé másoljuk be `stockfish` néven (kiterjesztés nélkül).
Ajánlott változatok:

- Windowshoz: `stockfish-windows-2022-x86-64-modern.exe`
- Ubuntuhoz: `stockfish-ubuntu-20.04-x86-64-modern`
- MacOS: Látogassunk el a [stockfish](https://stockfishchess.org/download/) oldalára

További Stockfish változatok innen tölthetőek le: [stockfish](https://stockfishchess.org/download/)

Ha szükséges, módosíthatjuk a Stockfish elérhetőségét a settings.json fájlban.

## Indítás

Indíthatjuk a

`pipenv run start`

ha pipenvvel telepítettük, vagy pedig a

`python3 main.py`

paranccsal, ha a requirements.txt fájlt használtuk.
