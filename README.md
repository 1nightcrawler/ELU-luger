# Lugemisseade

Funktsionaalse lugemisoskuse arengut toetava seadme prototüüp hariduslike
erivajadustega õpilastele. Õpilane loeb oma tasemele vastavaid tekste
ja vastab loetu mõistmise küsimustele; õpetaja saab jälgida tema edenemist.

Tallinna Ülikooli ELU projekt.
**Staatus:** varajane prototüüp, arenduses.

## Tekstide import

Planeeritud sisendvormingud on `.json`, `.txt`, `.epub` ja `.docx`; importimise ja teisendamise töövoog ei ole praeguses prototüübis veel valmis. PDF-tugi ei ole esialgu plaanis. Eesmärk on teisendada tekst ühtsesse JSON-kujusse, et seda oleks lihtsam küsimuste ja lugemisfunktsioonidega kasutada.

## Tehnoloogiad

Python + Flask (backend), HTML/CSS/JS (frontend), SQLite (andmebaas).
Sihtriistvara: Raspberry Pi 400 koos puuteekraaniga.

## Dokumentatsioon

Dokumentatsioon on hetkel kirjutatud inglise keeles.

- [Töökeskkonna seadistamine ja käivitamine](docs/getting-started.md)
- [Andmebaasi mudel](docs/database.md)

Käivitamise, migreerimise ja arenduse töövoo juhised asuvad getting-started juhendis.

## Projekti struktuur

- `app/` – Flaski rakendus, mudelid ja mallid
- `migrations/` – andmebaasi migratsioonid
- `docs/` – arendus- ja andmebaasidokumentatsioon
- `content/texts/` – planeeritud asukoht lugemistekstidele; pole veel prototüübis loodud
