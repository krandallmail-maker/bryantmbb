import streamlit as st


st.set_page_config(
    page_title="Bryant MBB – Class of 2026 Commits",
    layout="wide",
)


# -----------------------------------------------------------------------------
# Simple data model – update as new commits are announced
# -----------------------------------------------------------------------------

COMMITS_2026 = [
    {
        "name": "Connor Lyons",
        "position": "SF",
        "height": "6'8\"",
        "class_year": 2026,
        "status": "Committed to Bryant",
        "school": "Miller School (VA)",
        "club": "Team Loaded VA",
        "summary": (
            "Knockdown shooting wing with size. Can space the floor, attack closeouts, and defend "
            "multiple frontcourt spots thanks to his length and mobility."
        ),
    },
    {
        "name": "Grady Payton",
        "position": "G",
        "height": "6'4\"",
        "class_year": 2026,
        "status": "Committed to Bryant",
        "school": "High school / prep program",
        "club": "Club / grassroots program",
        "summary": (
            "Versatile combo guard who can score at all three levels, slide on and off the ball, "
            "and compete defensively on the perimeter."
        ),
    },
    {
        "name": "Elijah Hayeems",
        "position": "PG",
        "height": "6'6\"",
        "class_year": 2026,
        "status": "Committed to Bryant",
        "school": "Big Tyme Prep Academy (TX)",
        "club": "Prep / grassroots program",
        "summary": (
            "Big lead guard with rare positional size. Sees over the defense, toggles between "
            "primary playmaker and scorer, and uses his length to guard multiple spots."
        ),
    },
]


# -----------------------------------------------------------------------------
# Global black & gold theme via CSS
# -----------------------------------------------------------------------------

BLACK = "#050505"
GOLD = "#f4c542"
GOLD_SOFT = "#ffd666"
CARD_BG = "#111111"
BORDER = "#333333"

st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: {BLACK};
            color: white;
        }}

        /* Sidebar */
        section[data-testid="stSidebar"] > div {{
            background: radial-gradient(circle at top left, #222 0, #000 55%);
            border-right: 1px solid {BORDER};
        }}
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] p {{
            color: {GOLD_SOFT} !important;
        }}

        /* Headings */
        h1, h2, h3, h4 {{
            color: {GOLD} !important;
        }}

        /* Horizontal rules */
        hr {{
            border: none;
            border-top: 1px solid {BORDER};
            margin: 0.75rem 0 1.5rem 0;
        }}

        /* Player cards */
        .player-card {{
            background: linear-gradient(135deg, {CARD_BG} 0%, #000 60%);
            border-radius: 14px;
            padding: 1.1rem 1.25rem;
            border: 1px solid {BORDER};
            box-shadow: 0 0 14px rgba(0, 0, 0, 0.8);
            transition: transform 120ms ease-out, box-shadow 120ms ease-out,
                        border-color 120ms ease-out;
        }}
        .player-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 0 22px rgba(0, 0, 0, 0.95);
            border-color: {GOLD};
        }}
        .player-name {{
            font-size: 1.1rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }}
        .player-meta {{
            font-size: 0.9rem;
            opacity: 0.85;
        }}
        .status-pill {{
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.12rem 0.6rem;
            border-radius: 999px;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            background: rgba(244, 197, 66, 0.12);
            border: 1px solid {GOLD};
            color: {GOLD_SOFT};
        }}
        .status-dot {{
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: {GOLD_SOFT};
        }}

        /* Streamlit widgets – buttons, selects, etc. */
        .stButton>button {{
            background: linear-gradient(135deg, {GOLD} 0%, {GOLD_SOFT} 60%);
            color: #000;
            border-radius: 999px;
            border: none;
            padding: 0.45rem 1.2rem;
            font-weight: 600;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }}
        .stButton>button:hover {{
            filter: brightness(1.05);
            box-shadow: 0 0 14px rgba(244, 197, 66, 0.6);
        }}

        /* Remove default table background */
        .stDataFrame, .stTable {{
            background-color: transparent;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# Layout
# -----------------------------------------------------------------------------

st.title("Bryant Bulldogs Men’s Basketball")
st.subheader("Class of 2026 Recruiting Class – Commit List")

st.markdown(
    """
Welcome to the **black & gold** tracker for Bryant's men's basketball **class of 2026 commits**.

This page is meant to be a simple, clean way to see who is in the class at a glance.
Update the list in the code as new commitments are announced.
"""
)

st.write("---")


cols = st.columns(len(COMMITS_2026))

for idx, recruit in enumerate(COMMITS_2026):
    with cols[idx]:
        st.markdown(
            f"""
            <div class="player-card">
                <div class="player-name">{recruit['name']}</div>
                <div class="player-meta">
                    {recruit['position']} &nbsp;·&nbsp; Class of {recruit['class_year']}<br/>
                    {recruit['height']} &nbsp;·&nbsp; {recruit.get('school', '')}
                </div>
                <div style="margin-top: 0.6rem; margin-bottom: 0.6rem;">
                    <span class="status-pill">
                        <span class="status-dot"></span>
                        {recruit['status']}
                    </span>
                </div>
                <div style="font-size: 0.9rem; line-height: 1.35;">
                    {recruit['summary']}
                </div>
                <div style="margin-top: 0.6rem; font-size: 0.8rem; opacity: 0.8;">
                    {recruit.get('club', '')}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


st.write("---")
st.caption(
    "Unofficial fan-built page for Bryant Men’s Basketball recruiting. "
    "Not affiliated with Bryant University or any official recruiting service."
)

