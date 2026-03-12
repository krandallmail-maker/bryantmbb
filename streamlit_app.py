import streamlit as st
from datetime import datetime

# -----------------------------------------------------------------------------
# Data (edit this just like app.js)
# -----------------------------------------------------------------------------

RECRUITS = [
    {
        "name": "Connor Lyons",
        "class_year": 2026,
        "position": "SF",
        "height": "6'8\"",
        "weight": "—",
        "status": "committed",  # 'target' | 'offered' | 'committed'
        "hometown": "Miller School (VA)",
        "ranking": "2026 SF, Prep Hoops profile",
        "tags": ["Knockdown shooter", "Versatile forward", "Guards 3–5"],
        "notes": (
            "Per Prep Hoops, Lyons is a 6-foot-8 forward, knockdown shooter and "
            "improved facilitator who can defend 3–5. See his Prep Hoops profile "
            "for full context."
        ),
        "profile_url": "https://prephoops.com/player/connor-lyons/",
    },
]

UPDATES = [
    {
        "date": "2026-01-05",
        "type": "offer",
        "title": "Bryant offers 2026 guard prospect (sample)",
        "body": "Use this timeline card to log offers, visits, and commitment announcements as they happen.",
        "tag": "Offer",
    },
    {
        "date": "2025-12-10",
        "type": "visit",
        "title": "Unofficial visit scheduled (sample)",
        "body": "Track unofficial/official visits here so you can see recruiting momentum over time.",
        "tag": "Visit",
    },
    {
        "date": "2025-11-02",
        "type": "commit",
        "title": "First 2026 commit goes public (sample)",
        "body": 'When a prospect commits, add a new entry here and mark their status as "committed" above.',
        "tag": "Commit",
    },
]

EXPERT_ANALYSIS = [
    {
        "player": "Connor Lyons",
        "class_year": 2026,
        "position": "SF",
        "source": "Prep Hoops",
        "source_url": "https://prephoops.com/player/connor-lyons/",
        "author": "Jaylen Fuller",
        "date": "2026-03-10",
        "snippet": (
            "Prep Hoops describes Lyons as a 6-foot-8 forward and knockdown shooter "
            "who can also put the ball on the floor, facilitate, and defend "
            "multiple spots (3–5)."
        ),
        "tags": ["Connor Lyons", "Scouting report", "Prep Hoops"],
    }
]


def parse_date(date_str: str) -> datetime | None:
    try:
        return datetime.fromisoformat(date_str)
    except Exception:
        return None


def format_date(date_str: str) -> str:
    d = parse_date(date_str)
    if not d:
        return date_str
    return d.strftime("%b %-d, %Y") if hasattr(d, "strftime") else date_str


def get_last_updated() -> str:
    dates = [parse_date(u["date"]) for u in UPDATES if u.get("date")]
    dates = [d for d in dates if d]
    if not dates:
        return "No updates logged yet."
    latest = max(dates)
    return f"Last updated: {latest.strftime('%b %-d, %Y')}"


# -----------------------------------------------------------------------------
# Streamlit page config
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="Bryant 2026 Recruiting Tracker",
    layout="wide",
)


# -----------------------------------------------------------------------------
# Sidebar / header
# -----------------------------------------------------------------------------

st.title("Bryant Bulldogs – 2026 Recruiting Class")
st.caption(
    "Personal tracker for Bryant Men's Basketball 2026 recruiting class – commits, targets, "
    "timeline, and expert analysis."
)

with st.container():
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown(
            f"<span style='font-size:0.85rem;color:#9ca3af;'>{get_last_updated()}</span>",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            "<div style='text-align:right;'>"
            "<span style='font-size:0.75rem;padding:4px 10px;border-radius:999px;"
            "border:1px solid rgba(148,163,184,0.6);"
            "background:linear-gradient(to right,rgba(15,23,42,0.9),rgba(15,23,42,0.4));"
            "color:#818cf8;'>Recruiting Tracker</span>"
            "</div>",
            unsafe_allow_html=True,
        )

st.write("---")


# -----------------------------------------------------------------------------
# Filters
# -----------------------------------------------------------------------------

positions = sorted({r["position"] for r in RECRUITS if r.get("position")})
statuses = ["target", "offered", "committed"]

fcol1, fcol2 = st.columns(2)
with fcol1:
    pos_filter = st.selectbox("Filter by position", options=["All positions"] + positions)
with fcol2:
    status_filter = st.selectbox(
        "Filter by status", options=["All statuses"] + statuses, index=3
    )


def passes_filters(r: dict) -> bool:
    if pos_filter != "All positions" and r.get("position") != pos_filter:
        return False
    if status_filter != "All statuses" and r.get("status") != status_filter:
        return False
    return True


# -----------------------------------------------------------------------------
# Layout: left (recruits), right (timeline + expert)
# -----------------------------------------------------------------------------

left_col, right_col = st.columns([1.35, 1])


with left_col:
    st.subheader("2026 Commitments & Targets")
    st.caption(
        "Manually managed list of prospects. Edit the `RECRUITS`, `UPDATES`, and "
        "`EXPERT_ANALYSIS` lists in `streamlit_app.py`."
    )

    filtered_recruits = [r for r in RECRUITS if passes_filters(r)]

    if not filtered_recruits:
        st.info(
            "No recruits match the current filters yet. Try widening them or add new data "
            "in `streamlit_app.py`."
        )
    else:
        for r in filtered_recruits:
            status = r.get("status", "target")
            status_label = (
                "Committed" if status == "committed" else "Offer" if status == "offered" else "Target"
            )
            status_color = (
                "#22c55e" if status == "committed" else "#818cf8" if status == "offered" else "#facc15"
            )

            with st.container():
                st.markdown(
                    f"""
                    <div style="
                        border-radius:16px;
                        padding:10px 12px;
                        margin-bottom:10px;
                        border:1px solid rgba(148,163,184,0.35);
                        background:radial-gradient(circle at top left,rgba(79,70,229,0.28),rgba(15,23,42,0.9));
                    ">
                        <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:8px;">
                            <div>
                                <div style="font-weight:600;font-size:0.95rem;">{r.get("name","")}</div>
                                <div style="font-size:0.78rem;color:#9ca3af;">
                                    {r.get("position","–")} • {r.get("class_year","2026")}
                                    {" • " + r.get("height","") if r.get("height") else ""}
                                </div>
                            </div>
                            <span style="
                                font-size:0.72rem;
                                padding:3px 8px;
                                border-radius:999px;
                                border:1px solid {status_color};
                                color:{status_color};
                            ">{status_label}</span>
                        </div>
                        <div style="margin-top:4px;font-size:0.78rem;color:#9ca3af;">
                            {("<strong>From:</strong> " + r.get("hometown","")) if r.get("hometown") else ""}
                            {" • " if r.get("hometown") and r.get("ranking") else ""}
                            {("<strong>Rank:</strong> " + r.get("ranking","")) if r.get("ranking") else ""}
                        </div>
                    """,
                    unsafe_allow_html=True,
                )

                tags = r.get("tags") or []
                if tags:
                    tag_html = " ".join(
                        f"<span style='font-size:0.7rem;padding:3px 7px;border-radius:999px;"
                        f"border:1px solid rgba(148,163,184,0.45);margin-right:4px;"
                        f"background:rgba(15,23,42,0.9);color:#9ca3af;'>{t}</span>"
                        for t in tags
                    )
                    st.markdown(f"<div style='margin-top:4px;'>{tag_html}</div>", unsafe_allow_html=True)

                if r.get("notes"):
                    st.markdown(
                        f"<div style='margin-top:4px;font-size:0.78rem;color:#9ca3af;'>{r['notes']}</div>",
                        unsafe_allow_html=True,
                    )

                if r.get("profile_url"):
                    st.markdown(
                        f"[Full profile]({r['profile_url']})",
                    )


with right_col:
    # Timeline
    st.subheader("Timeline of Updates")

    if not UPDATES:
        st.info("No timeline events yet. Add your first offer, visit, or commit in `streamlit_app.py`.")
    else:
        sorted_updates = sorted(
            UPDATES,
            key=lambda u: parse_date(u.get("date") or "") or datetime.min,
            reverse=True,
        )
        for u in sorted_updates:
            with st.container():
                st.markdown(
                    f"**{format_date(u.get('date',''))}** – "
                    f"`{u.get('tag','Update')}`  \n"
                    f"**{u.get('title','')}**",
                )
                if u.get("body"):
                    st.caption(u["body"])

    st.write("---")

    # Expert analysis
    st.subheader("Expert Analysis")
    st.caption(
        "Scouting notes from outlets like Prep Hoops for key 2026 targets. "
        "Append new entries to `EXPERT_ANALYSIS`."
    )

    if not EXPERT_ANALYSIS:
        st.info(
            "No expert analysis logged yet. Add scouting blurbs for key targets in the "
            "`EXPERT_ANALYSIS` list in `streamlit_app.py`."
        )
    else:
        sorted_expert = sorted(
            EXPERT_ANALYSIS,
            key=lambda e: parse_date(e.get("date") or "") or datetime.min,
            reverse=True,
        )

        for e in sorted_expert:
            with st.container():
                header = f"{e.get('player','Unnamed prospect')}"
                if e.get("position"):
                    header += f" • {e['position']}"
                if e.get("class_year"):
                    header += f" • {e['class_year']}"

                meta_parts = []
                if e.get("date"):
                    meta_parts.append(format_date(e["date"]))
                author = e.get("author")
                source = e.get("source")
                if author and source:
                    meta_parts.append(f"{author} • {source}")
                elif author:
                    meta_parts.append(author)
                elif source:
                    meta_parts.append(source)

                meta = " | ".join(meta_parts)

                st.markdown(f"**{header}**")
                if meta:
                    st.caption(meta)

                if e.get("snippet"):
                    st.write(e["snippet"])

                if e.get("source_url"):
                    st.markdown(f"[Full profile]({e['source_url']})")

                tags = e.get("tags") or []
                if tags:
                    st.caption(" • ".join(tags))


st.write("---")
st.markdown(
    "Built as a personal fan project. Data is manually maintained and not affiliated with Bryant University.",
    help="All recruiting info is for personal tracking only.",
)

