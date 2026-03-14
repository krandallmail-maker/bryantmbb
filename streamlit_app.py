import streamlit as st
import pandas as pd


# -----------------------------------------------------------------------------
# Data models
# -----------------------------------------------------------------------------

# NOTE: Fill in real photo URLs and stats from the official Bryant roster page.
BRYANT_PLAYERS = [
    {
        "name": "Example Guard",
        "position": "G",
        "year": "Jr.",
        "height": "6'2\"",
        "weight": "185 lbs",
        "number": 1,
        "description": (
            "Two-way combo guard who can pressure the ball, make plays out of ball screens, "
            "and stretch the floor as a catch-and-shoot threat."
        ),
        "profile_url": "https://bryantbulldogs.com/sports/mens-basketball",
        "photo_url": "https://via.placeholder.com/160x200.png?text=Player+Photo",
        "stats": {
            "PPG": 10.5,
            "RPG": 3.2,
            "APG": 4.1,
            "FG%": 0.43,
            "3P%": 0.36,
        },
    },
    # Add more Bryant players here in the same shape.
]


# 2026 recruiting commits – based on public descriptions and links to Prep Hoops
RECRUITS_2026 = [
    {
        "name": "Connor Lyons",
        "position": "SF",
        "height": "6'8\"",
        "class_year": 2026,
        "status": "Committed to Bryant",
        "school": "Miller School (VA)",
        "club": "Team Loaded VA",
        "prep_hoops_url": "https://prephoops.com/player/connor-lyons/",
        "summary": (
            "6-foot-8 small forward with a reputation as a knockdown shooter. Lyons can also "
            "put the ball on the floor, facilitate in the half court, and defend multiple "
            "frontcourt spots thanks to his length and mobility "
            "(summary based on his Prep Hoops evaluation)."
        ),
        "tags": ["Wing size", "Shooting gravity", "Multi-position defender"],
    },
    {
        "name": "Grady Payton",
        "position": "G",
        "height": "6'4\"",
        "class_year": 2026,
        "status": "Committed to Bryant",
        "school": "High school / prep program",
        "club": "Club / grassroots program",
        "prep_hoops_url": "https://prephoops.com/",
        "summary": (
            "Versatile guard prospect who can score at all three levels and slide between on-ball "
            "and off-ball roles. Payton projects as a tough backcourt piece who can attack "
            "closeouts, create for teammates, and compete defensively on the perimeter "
            "(high-level summary; tailor this once you have his specific Prep Hoops write-up)."
        ),
        "tags": ["Three-level scoring", "Combo guard", "Competitive motor"],
    },
    {
        "name": "Elijah Hayeems",
        "position": "PG",
        "height": "6'6\"",
        "class_year": 2026,
        "status": "Committed to Bryant",
        "school": "Big Tyme Prep Academy (TX)",
        "club": "Prep / grassroots program",
        "prep_hoops_url": "https://prephoops.com/player/elijah-hayeems/",
        "summary": (
            "6-foot-6 point guard with rare positional size. According to Prep Hoops, Hayeems’ "
            "McDonald’s All-American nomination is driven by his blend of size and functional "
            "skill – he sees over defenses, toggles between primary playmaker and scorer based "
            "on game flow, finishes through contact, and guards multiple spots while disrupting "
            "passing lanes."
        ),
        "tags": ["Elite PG size", "Playmaking & scoring", "Defensive versatility"],
    },
]


# Example 2024–25 schedule & results (fill in real data)
TEAM_SCHEDULE = [
    {
        "date": "Nov 5, 2024",
        "opponent": "Non-Conference Opponent",
        "location": "Home",
        "result": "W",
        "score": "78–65",
    },
    {
        "date": "Nov 12, 2024",
        "opponent": "Non-Conference Opponent",
        "location": "Away",
        "result": "L",
        "score": "69–73",
    },
    {
        "date": "Nov 18, 2024",
        "opponent": "Conference Opponent",
        "location": "Home",
        "result": "TBD",
        "score": "-",
    },
]


# -----------------------------------------------------------------------------
# Streamlit page config
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="Bryant MBB – Fan Dashboard",
    layout="wide",
)


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def render_stats_line(stats: dict) -> str:
    """Return a compact text stat line like 'PPG 10.5 · RPG 3.2 · FG% 43.0%'."""
    if not stats:
        return ""
    pieces = []
    for key in ["PPG", "RPG", "APG", "FG%", "3P%"]:
        if key in stats:
            val = stats[key]
            if isinstance(val, float) and "FG" in key:
                pieces.append(f"{key} {val:.1%}")
            else:
                pieces.append(f"{key} {val}")
    return " · ".join(pieces)


def render_header():
    st.title("Bryant Bulldogs Men’s Basketball – Fan Dashboard")
    st.caption(
        "Unofficial fan-built hub for Bryant Men’s Basketball – roster, transfer-portal grades, "
        "2026 recruiting class, schedule, and basic team stats."
    )
    st.write("---")


def section_overview():
    st.subheader("Program Snapshot")
    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        st.markdown(
            """
Bryant has quickly become one of the most entertaining mid-major programs in the country –
playing up-tempo, spacing the floor, and leaning into positionless lineups.

Use the navigation on the left to:

- **Scan the roster** and give your own transfer portal grades.
- **Track the 2026 class** with links out to public scouting reports.
- **Browse the schedule** and keep a quick view of recent results.
- **See simple team charts** built from per-game averages.
"""
        )

    with col_right:
        st.metric("Unofficial Fan Confidence", "87%", "↑ 5% vs. last season")
        st.metric("Estimated Pace Rank", "Top 15%", "Fast tempo")
        st.info(
            "All numbers here are illustrative – plug in real data from Bryant’s official stats page "
            "or KenPom once you have it."
        )


def section_roster_and_portal():
    st.subheader("Bryant Men’s Basketball Players – Transfer Portal Watch")
    st.caption(
        "Pull in players from the official roster with their bios, photos, and stats. "
        "Use the sliders to grade how likely you think each player is to stay at Bryant."
    )

    for player in BRYANT_PLAYERS:
        col_photo, col_info = st.columns([0.4, 1.6])

        with col_photo:
            if player.get("photo_url"):
                st.image(
                    player["photo_url"],
                    width=140,
                    caption=f"#{player.get('number', '')} {player['name']}",
                )
            else:
                st.write(f"#{player.get('number', '')} {player['name']}")

        with col_info:
            header = f"**{player['name']}** – {player['position']} · {player['year']}"
            if player.get("height") or player.get("weight"):
                height_weight = " / ".join(
                    [x for x in [player.get("height"), player.get("weight")] if x]
                )
                header += f" · {height_weight}"
            st.markdown(header)

            if player.get("description"):
                st.write(player["description"])

            stats_line = render_stats_line(player.get("stats", {}))
            if stats_line:
                st.caption(stats_line)

            if player.get("profile_url"):
                st.markdown(f"[Official Bryant profile]({player['profile_url']})")

            slider_key = f"stay_grade_{player['name'].replace(' ', '_')}"
            stay_grade = st.slider(
                "How likely do you think he stays at Bryant?",
                min_value=0,
                max_value=100,
                value=75,
                step=5,
                key=slider_key,
            )
            st.caption(f"Your current grade: **{stay_grade}% chance to stay**")

        st.write("---")


def section_commits_2026():
    st.subheader("2026 Bryant Men’s Basketball Commits")
    st.caption(
        "High-level summaries and links to public scouting info (for example, Prep Hoops profiles). "
        "Update this section as new commits are announced."
    )

    cols = st.columns(3)
    for idx, recruit in enumerate(RECRUITS_2026):
        with cols[idx % 3]:
            st.markdown(f"### {recruit['name']}")
            st.caption(f"{recruit['position']} · Class of {recruit['class_year']}")

            school_line = recruit.get("school", "")
            club_line = recruit.get("club", "")
            if school_line or club_line:
                st.write(
                    " · ".join(
                        [part for part in [school_line, club_line] if part]
                    )
                )

            st.write(recruit["summary"])

            tags = recruit.get("tags", [])
            if tags:
                st.caption(" • ".join(tags))

            if recruit.get("prep_hoops_url"):
                st.markdown(
                    f"[Prep Hoops profile]({recruit['prep_hoops_url']})",
                    help="Opens the public player page on Prep Hoops.",
                )


def section_schedule():
    st.subheader("2024–25 Schedule & Results (Example)")
    st.caption(
        "Swap this placeholder schedule out for the real one from Bryant’s official site. "
        "You can also paste in a CSV and read it with pandas."
    )

    df = pd.DataFrame(TEAM_SCHEDULE)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )

    home_games = df[df["location"] == "Home"].shape[0]
    away_games = df[df["location"] == "Away"].shape[0]
    col1, col2 = st.columns(2)
    col1.metric("Home games", home_games)
    col2.metric("Road games", away_games)


def section_team_stats():
    st.subheader("Team Stats & Simple Visuals")
    st.caption(
        "These charts are built from the `BRYANT_PLAYERS` data structure above. "
        "Once you have full stats, just update that list."
    )

    if not BRYANT_PLAYERS:
        st.info("Add players to `BRYANT_PLAYERS` to see charts here.")
        return

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

    # Build a small DataFrame from the player list
    rows = []
    for p in BRYANT_PLAYERS:
        stats = p.get("stats", {})
        rows.append(
            {
                "Player": p["name"],
                "PPG": stats.get("PPG", 0),
                "RPG": stats.get("RPG", 0),
                "APG": stats.get("APG", 0),
                "FG%": stats.get("FG%", None),
                "3P%": stats.get("3P%", None),
            }
        )

    df_stats = pd.DataFrame(rows)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Points per Game")
        st.bar_chart(df_stats.set_index("Player")["PPG"])

    with col2:
        st.markdown("#### Rebounds per Game")
        st.bar_chart(df_stats.set_index("Player")["RPG"])

    st.markdown("#### Shooting Splits (FG% vs 3P%)")
    splits_df = df_stats[["Player", "FG%", "3P%"]].set_index("Player")
    st.line_chart(splits_df)


def render_footer():
    st.write("---")
    st.markdown(
        "This app is a personal fan project and is **not affiliated with Bryant University, Prep Hoops, "
        "or any official recruiting service**. All descriptions are summaries based on publicly available "
        "information such as Prep Hoops profiles like "
        "[Connor Lyons](https://prephoops.com/player/connor-lyons/) and "
        "[Elijah Hayeems](https://prephoops.com/player/elijah-hayeems/)."
    )


# -----------------------------------------------------------------------------
# Main layout
# -----------------------------------------------------------------------------


def main():
    render_header()

    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        [
            "Team overview",
            "Roster & transfer portal",
            "2026 commits",
            "Schedule & results",
            "Team stats & charts",
        ],
    )

    if page == "Team overview":
        section_overview()
    elif page == "Roster & transfer portal":
        section_roster_and_portal()
    elif page == "2026 commits":
        section_commits_2026()
    elif page == "Schedule & results":
        section_schedule()
    elif page == "Team stats & charts":
        section_team_stats()

    render_footer()


if __name__ == "__main__":
    main()

