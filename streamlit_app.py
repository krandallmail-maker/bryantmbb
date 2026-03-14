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

