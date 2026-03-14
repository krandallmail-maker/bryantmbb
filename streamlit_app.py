"""
grady_payton.py
---------------
Grady Payton recruit profile page for the Bryant MBB Streamlit app.
Scrapes https://prephoops.com/player/grady-payton/ and displays a
clean recruit card. Falls back to cached data if the page is unreachable.

Usage (add to your app's navigation / pages):
    import grady_payton
    grady_payton.show()

Or use directly as a Streamlit page file.
"""

import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# ── Constants ────────────────────────────────────────────────────────────────
PLAYER_URL = "https://prephoops.com/player/grady-payton/"
PLAYER_IMAGE = "https://prephoops.com/wp-content/uploads/sites/2/2025/02/IMG_3083.jpeg"
BRYANT_LOGO = "https://upload.wikimedia.org/wikipedia/en/thumb/d/d0/Bryant_Bulldogs_logo.svg/200px-Bryant_Bulldogs_logo.svg.png"

# Cached / fallback data pulled from Prep Hoops on 2026-03-13
CACHED_DATA = {
    "name": "Grady Payton",
    "position": "Small Forward",
    "class_year": "2026",
    "height": "6'9\"",
    "weight": "195 lbs",
    "high_school": "Capital City",
    "state": "Missouri",
    "club": "PAC Basketball",
    "profile_url": PLAYER_URL,
    "image_url": PLAYER_IMAGE,
    "offer": "Bryant University",
    "news": [
        {
            "title": "Forwards and Posts Who Delivered on Championship Saturday",
            "author": "Earl Austin",
            "date": "March 8, 2026",
            "url": "https://prephoops.com/2026/03/forwards-and-posts-who-delivered-on-championship-saturday/",
        },
        {
            "title": "More Recruiting Tidbits",
            "author": "Earl Austin",
            "date": "January 31, 2026",
            "url": "https://prephoops.com/2026/01/more-recruiting-tidbits-47/",
        },
        {
            "title": "Milestone Monday",
            "author": "Earl Austin",
            "date": "January 26, 2026",
            "url": "https://prephoops.com/2026/01/milestone-monday-20/",
        },
        {
            "title": "Inside the Norm Stewart Classic: What the Event Really Revealed",
            "author": "Daniel Siehndel",
            "date": "December 10, 2025",
            "url": "https://prephoops.com/2025/12/inside-the-norm-stewart-classic-what-the-event-really-revealed/",
        },
    ],
}


# ── Scraper ───────────────────────────────────────────────────────────────────
def scrape_player(url: str) -> dict:
    """Attempt a live scrape of the Prep Hoops player page."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        )
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
    except Exception:
        return {}

    soup = BeautifulSoup(resp.text, "html.parser")
    data = {}

    # Player name
    h3 = soup.find("h3", string=lambda t: t and "Payton" in t)
    if h3:
        data["name"] = h3.get_text(strip=True)

    # Bio paragraph
    about = soup.find("div", class_="player-about") or soup.find("p", string=lambda t: t and "6'9" in str(t))
    if about:
        data["bio"] = about.get_text(" ", strip=True)

    # News items
    news_items = []
    for article in soup.select("a[href*='prephoops.com/202']")[:6]:
        title_tag = article.find("h2") or article.find("h3") or article.find("p")
        if title_tag:
            news_items.append({
                "title": title_tag.get_text(strip=True),
                "url": article["href"],
                "date": "",
                "author": "",
            })
    if news_items:
        data["news"] = news_items

    # Image
    img = soup.find("img", {"src": lambda s: s and "IMG_3083" in str(s)})
    if img:
        data["image_url"] = img["src"].split("?")[0]

    return data


# ── Main display ──────────────────────────────────────────────────────────────
def show():
    st.set_page_config(
        page_title="Grady Payton | Bryant MBB Recruiting",
        page_icon="🏀",
        layout="wide",
    )

    # Try live scrape; merge with cached fallback
    live = scrape_player(PLAYER_URL)
    player = {**CACHED_DATA, **live}  # live data wins if present

    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown(
        """
        <style>
        .recruit-card {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
            border-radius: 16px;
            padding: 2rem;
            color: white;
            margin-bottom: 1.5rem;
        }
        .stat-box {
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 10px;
            padding: 0.75rem 1rem;
            text-align: center;
        }
        .stat-label { font-size: 0.72rem; color: #aab4be; text-transform: uppercase; letter-spacing: 1px; }
        .stat-value { font-size: 1.35rem; font-weight: 700; color: #f5c518; margin-top: 2px; }
        .news-item {
            border-left: 3px solid #f5c518;
            padding: 0.5rem 0.75rem;
            margin-bottom: 0.75rem;
            background: #f9f9f9;
            border-radius: 0 6px 6px 0;
        }
        .news-item a { color: #0f3460; font-weight: 600; text-decoration: none; }
        .news-item a:hover { text-decoration: underline; }
        .news-meta { font-size: 0.78rem; color: #666; margin-top: 2px; }
        .source-badge {
            display: inline-block;
            background: #e8f4f8;
            border: 1px solid #bee3f8;
            color: #2b6cb0;
            font-size: 0.72rem;
            padding: 2px 8px;
            border-radius: 12px;
            margin-top: 0.25rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Bryant header bar
    col_logo, col_title = st.columns([1, 6])
    with col_logo:
        st.image(BRYANT_LOGO, width=70)
    with col_title:
        st.markdown("## 🏀 Bryant Bulldogs — Recruiting Profile")
        st.caption("Class of 2026 Commit")

    st.divider()

    # ── Player card ───────────────────────────────────────────────────────────
    img_col, info_col = st.columns([1, 2], gap="large")

    with img_col:
        st.image(
            player.get("image_url", PLAYER_IMAGE),
            width=280,
            caption="Grady Payton — Prep Hoops",
        )
        st.markdown(
            f'<a href="{PLAYER_URL}" target="_blank" class="source-badge">📄 View Full Profile on Prep Hoops</a>',
            unsafe_allow_html=True,
        )

    with info_col:
        st.markdown(
            f"""
            <div class="recruit-card">
                <div style="font-size:2rem; font-weight:800; letter-spacing:-0.5px;">{player['name']}</div>
                <div style="font-size:1rem; color:#aab4be; margin-bottom:1.2rem;">
                    {player['position']} &nbsp;·&nbsp; Class of {player['class_year']}
                </div>
            """,
            unsafe_allow_html=True,
        )

        s1, s2, s3, s4 = st.columns(4)
        for col, label, val in [
            (s1, "Height", player["height"]),
            (s2, "Weight", player["weight"]),
            (s3, "State", player["state"]),
            (s4, "Class", player["class_year"]),
        ]:
            with col:
                st.markdown(
                    f"""
                    <div class="stat-box">
                        <div class="stat-label">{label}</div>
                        <div class="stat-value">{val}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("#### 🏫 School & Club")
        st.markdown(
            f"**High School:** {player['high_school']} ({player['state']})  \n"
            f"**Club:** {player['club']}  \n"
            f"**Offer / Commit:** {player.get('offer', 'Bryant University')}"
        )

    st.divider()

    # ── Bio ───────────────────────────────────────────────────────────────────
    st.markdown("### 📋 About Grady")
    bio = player.get(
        "bio",
        f"Grady Payton is a **{player['height']} Small Forward** in the **{player['class_year']} class**. "
        f"He attends **{player['high_school']}** in {player['state']} and plays club basketball "
        f"for **{player['club']}**. Payton has drawn interest from Bryant University and is one of "
        f"the top forwards in Missouri.",
    )
    st.write(bio)

    # ── News ──────────────────────────────────────────────────────────────────
    st.markdown("### 📰 Recent News")
    for item in player.get("news", []):
        meta_parts = [p for p in [item.get("author"), item.get("date")] if p]
        meta = " · ".join(meta_parts)
        st.markdown(
            f"""
            <div class="news-item">
                <a href="{item['url']}" target="_blank">{item['title']}</a>
                {"<div class='news-meta'>" + meta + "</div>" if meta else ""}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f'<a href="{PLAYER_URL}" target="_blank" class="source-badge">🔗 See all news on Prep Hoops</a>',
        unsafe_allow_html=True,
    )

    # ── Footer ────────────────────────────────────────────────────────────────
    st.divider()
    st.caption(
        f"Data sourced from [Prep Hoops]({PLAYER_URL}) · "
        f"Last updated: {datetime.today().strftime('%B %d, %Y')}"
    )


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    show()
