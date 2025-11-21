# 📝 Markdown WYSIWYG Editor

Lokální webová aplikace pro editaci markdown souborů s WYSIWYG editorem, dashboardem a automatickým ukládáním.

## ✨ Současné funkce

### Dashboard
- 📋 Přehled všech markdown souborů ve složce `markdown-files/`
- 🔍 Vyhledávání podle názvu souboru
- 🔄 Třídění souborů:
  - Podle data úpravy (nejnovější/nejstarší)
  - Podle názvu (A-Z, Z-A)
- 📅 Zobrazení data poslední úpravy
- 📦 Zobrazení velikosti souboru

### WYSIWYG Editor
- ✏️ Editace markdown v "hezky" formátovaném režimu
- 💾 **Automatické ukládání** každé 3 sekundy po nečinnosti
- ✓ Indikátor stavu ukládání (Uloženo / Ukládám...)
- 🎨 Podpora všech základních markdown formátů:
  - **Nadpisy** (H1-H6)
  - **Odrážky** a číslované seznamy
  - **Todo checkboxy** ☑️
  - **Linky**
  - **Zvýraznění** (bold, italic, strike)
  - **Citace** (blockquote)
  - **Horizontální oddělovač**
  - **Obrázky** (nahrání i vložení z disku)
  - **Kód** a code bloky
  - **Tabulky**

### Práce s obrázky
- 📷 Nahrání obrázku přímo v editoru (drag & drop nebo tlačítko)
- 🗂️ Automatické uložení do složky `markdown-files/images/`
- 🔗 Relativní cesta v markdown: `![alt](images/obrazek.png)`
- ⏱️ Unikátní názvy s timestamp pro prevenci konfliktů

## 🚀 Instalace a spuštění

### 1. Přejdi do složky projektu

```bash
cd markdown-editor/
```

### 2. Instalace závislostí

```bash
pip3 install -r requirements.txt
```

### 3. Spuštění aplikace

```bash
python3 app.py
```

Aplikace se spustí na: **http://localhost:8000**

### 4. Použití

1. **Nahraj markdown soubory** do složky `markdown-files/`
2. **Otevři prohlížeč** na `http://localhost:8000`
3. **Vyber soubor** z dashboardu, který chceš editovat
4. **Edituj text** v WYSIWYG editoru
5. **Změny se automaticky ukládají** každé 3 sekundy
6. **Zavři stránku** - všechny změny jsou uloženy

## 📁 Struktura projektu

```
markdown-editor/
├── app.py                    # Flask server s API
├── requirements.txt          # Python závislosti
├── README.md                 # Tato dokumentace
├── markdown-files/           # Složka pro tvoje MD soubory
│   └── images/              # Nahrané obrázky
├── static/
│   └── css/
│       └── style.css        # Styling (světle fialový design)
└── templates/
    ├── dashboard.html        # Dashboard s přehledem
    └── editor.html           # WYSIWYG editor
```

## 🎨 Design

Aplikace používá **světle fialovou barvu** (#B19CD9) pro:
- Nadpisy
- Tlačítka
- Interaktivní prvky
- Hover stavy

Design je inspirovaný Notion a Bear - čistý a minimalistický.

## 🔐 Bezpečnost

- ✓ Aplikace běží pouze lokálně (localhost)
- ✓ Žádná data neodcházejí z počítače
- ✓ Bezpečné názvy souborů (sanitizace)
- ✓ Omezení velikosti nahrávaných souborů (16MB)
- ✓ Kontrola povolených formátů obrázků

## ⚠️ Důležité poznámky

### Souběžné editace
Pokud je soubor otevřený v editoru **a zároveň** v jiné aplikaci (např. Obsidian, VS Code), může dojít ke konfliktu při ukládání. Doporučujeme editovat soubor pouze v jedné aplikaci najednou.

### Backup
I když má aplikace auto-save, doporučujeme pravidelně zálohovat složku `markdown-files/` nebo používat git verzování.

## 🐛 Řešení problémů

### Aplikace se nespustí
```bash
# Zkontroluj, zda je nainstalovaný Flask
pip3 list | grep Flask

# Případně reinstaluj závislosti
pip3 install -r requirements.txt --force-reinstall
```

### Soubor se neuloží
- Zkontroluj oprávnění k zápisu do složky `markdown-files/`
- Podívej se do konzole prohlížeče (F12) na chybové hlášky
- Restartuj Flask server

### Obrázek se nenačte
- Ujisti se, že je ve složce `markdown-files/images/`
- Zkontroluj cestu v markdownu: `![alt](images/obrazek.png)`
- Podporované formáty: PNG, JPG, JPEG, GIF, WEBP, SVG

### Port 5000 je obsazený (macOS problém)
Na novějších verzích macOS je port 5000 často obsazený systémovou službou ControlCenter.
**Řešení:** Aplikace proto používá port **8000** místo 5000.

## 📄 Licence

Tento projekt je open source a volně k dispozici pro osobní i komerční použití.

---

**Verze:** 1.0.0  
**Tech stack:** Python Flask, Toast UI Editor, Vanilla JavaScript

