# Bryant Men's Basketball – 2026 Recruiting Tracker

A small, single-page website to keep personal tabs on the **2026 recruiting class for Bryant Men's Basketball**. It is built with plain HTML/CSS/JS, so you can easily edit the data and host it anywhere.

---

## What this does

- **Recruits grid**: Cards for 2026 recruits with position, size, status (target/offered/committed), notes, and quick tags.
- **Timeline of updates**: A chronological log you can use for offers, visits, and commitments.
- **Simple filters**: Filter recruits by position and recruiting status.
- **Fully manual control**: All data lives in `app.js`, so you can update it whenever news breaks.

> This project does **not** scrape or automatically pull live data from external sites. You stay in control of what gets logged.

---

## Getting started (static site)

From `/Users/kylerandall/Documents`:

```bash
cd "/Users/kylerandall/Documents"
npm install
npm run start
```

This uses `live-server` to open `index.html` in your default browser and auto‑reload on changes.

If you prefer not to install anything, you can also just open `index.html` directly in your browser (double‑click from Finder).

---

## Getting started (Streamlit app)

If you prefer a Python app with a simple URL to share, you can use the Streamlit version (`streamlit_app.py`).

From `/Users/kylerandall/Documents`:

```bash
cd "/Users/kylerandall/Documents"
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

This will open the Streamlit app in your browser at a local URL (usually `http://localhost:8501`).

- **Edit data** in `streamlit_app.py`:
  - `RECRUITS` – commitments and targets (includes Connor Lyons as a committed 2026 SF).
  - `UPDATES` – timeline of offers/visits/commits.
  - `EXPERT_ANALYSIS` – scouting blurbs like the Prep Hoops evaluation for Connor Lyons.
- **Refresh the page**; Streamlit hot‑reloads when you save the file.

---

## Editing recruits and updates

All of the “content” lives in `app.js`:

- **`recruits` array** – one object per prospect.
- **`updates` array** – one object per timeline event.

Each recruit looks like:

```js
{
  name: 'Sample Guard Prospect',
  classYear: 2026,
  position: 'PG',
  height: "6'2\"",
  weight: '180',
  status: 'target',      // 'target' | 'offered' | 'committed'
  hometown: 'Your City, ST',
  ranking: 'Top-150 watchlist',
  tags: ['High motor', 'Perimeter scoring'],
  notes: 'Short scouting blurb or context.'
}
```

Each timeline update looks like:

```js
{
  date: '2026-01-05',    // YYYY-MM-DD
  type: 'offer',         // any string you like
  title: 'Bryant offers 2026 guard prospect',
  body: 'More detailed context about the news.',
  tag: 'Offer'           // small label chip shown in the UI
}
```

After editing `app.js`, just **refresh the page** in your browser to see changes.

---

## Customization ideas

- **Color & branding**: Tweak colors in `styles.css` (look for `:root` at the top) to lean harder into Bryant branding.
- **Extra fields**: Add things like highlight links, social handles, or composite rankings to the recruit cards.
- **Separate pages**: If you want future classes (2027, etc.), you can copy this setup into `2027/index.html` with its own `app.js`.

