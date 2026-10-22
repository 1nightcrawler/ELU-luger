# Lugemisseade

Funktsionaalse lugemisoskuse arengut toetava seadme prototüüp hariduslike
erivajadustega õpilastele. Õpilane loeb oma tasemele vastavaid tekste
ja vastab loetu mõistmise küsimustele; õpetaja saab jälgida tema edenemist.

Tallinna Ülikooli ELU projekt.
**Staatus:** varajane prototüüp, arenduses.

## Tehnoloogiad

Python + Flask (backend), HTML/CSS/JS (frontend), SQLite (andmebaas).
Sihtriistvara: Raspberry Pi 400 koos puuteekraaniga.

## Käivitamine

```bash
git clone <repo-url>
cd ELU-luger
python3 -m venv venv
source venv/bin/activate      # Windowsis: venv\Scripts\activate
pip install -r requirements.txt
flask --app app/app.py run
```

Seejärel ava brauseris [http://localhost:5000]

## Projekti struktuur

- `app/` – Flaski rakendus (marsruudid, andmebaas, esirakendus)
- `content/texts/` – lugemistekstid või raamatud
