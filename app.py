import streamlit as st
import random
import os
import base64

st.set_page_config(page_title="Mini Football Manager", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_DIR = os.path.join(BASE_DIR, "logos")

def get_base64_image(image_path):
    """Return data URI for an image; returns default if not exists."""
    if not os.path.exists(image_path):
        image_path = os.path.join(LOGO_DIR, "default.png")
    try:
        with open(image_path, "rb") as f:
            raw = f.read()
        return "data:image/png;base64," + base64.b64encode(raw).decode()
    except Exception:
        return None

clubs = {
    "Arsenal": {
        "logo_path": os.path.join(LOGO_DIR, "arsenal.png"),
        "players": [
            {"name": "David Raya", "pos": "GK", "rating": 85, "price": 30},
            {"name": "Ben White", "pos": "RB", "rating": 83, "price": 40},
            {"name": "William Saliba", "pos": "CB", "rating": 87, "price": 70},
            {"name": "Gabriel Magalhães", "pos": "CB", "rating": 85, "price": 50},
            {"name": "Oleksandr Zinchenko", "pos": "LB", "rating": 82, "price": 35},
            {"name": "Declan Rice", "pos": "CDM", "rating": 89, "price": 100},
            {"name": "Martin Ødegaard", "pos": "CM", "rating": 88, "price": 90},
            {"name": "Kai Havertz", "pos": "CAM", "rating": 84, "price": 60},
            {"name": "Bukayo Saka", "pos": "RW", "rating": 89, "price": 110},
            {"name": "Gabriel Jesus", "pos": "ST", "rating": 85, "price": 75},
            {"name": "Leandro Trossard", "pos": "LW", "rating": 84, "price": 55},
        ],
    },
    "Chelsea": {
        "logo_path": os.path.join(LOGO_DIR, "chelsea.png"),
        "players": [
            {"name": "Kepa", "pos": "GK", "rating": 80, "price": 25},
            {"name": "Reece James", "pos": "RB", "rating": 84, "price": 55},
            {"name": "Thiago Silva", "pos": "CB", "rating": 83, "price": 40},
            {"name": "Wesley Fofana", "pos": "CB", "rating": 82, "price": 45},
            {"name": "Ben Chilwell", "pos": "LB", "rating": 81, "price": 30},
            {"name": "Enzo Fernandez", "pos": "CM", "rating": 84, "price": 70},
            {"name": "Mason Mount", "pos": "CAM", "rating": 82, "price": 50},
            {"name": "Raheem Sterling", "pos": "LW", "rating": 85, "price": 80},
            {"name": "Nicolas Jackson", "pos": "ST", "rating": 80, "price": 35},
            {"name": "Christian Pulisic", "pos": "RW", "rating": 79, "price": 30},
            {"name": "Callum Hudson-Odoi", "pos": "LM", "rating": 77, "price": 20},
        ],
    },
    "Liverpool": {
        "logo_path": os.path.join(LOGO_DIR, "liverpool.png"),
        "players": [
            {"name": "Alisson", "pos": "GK", "rating": 89, "price": 90},
            {"name": "Trent Alexander-Arnold", "pos": "RB", "rating": 88, "price": 95},
            {"name": "Virgil van Dijk", "pos": "CB", "rating": 90, "price": 100},
            {"name": "Ibrahima Konaté", "pos": "CB", "rating": 84, "price": 60},
            {"name": "Andrew Robertson", "pos": "LB", "rating": 85, "price": 70},
            {"name": "Jordan Henderson", "pos": "CM", "rating": 82, "price": 40},
            {"name": "Luis Díaz", "pos": "LW", "rating": 86, "price": 85},
            {"name": "Mohamed Salah", "pos": "RW", "rating": 91, "price": 120},
            {"name": "Diogo Jota", "pos": "ST", "rating": 85, "price": 75},
            {"name": "Cody Gakpo", "pos": "ST", "rating": 83, "price": 70},
            {"name": "Fabinho", "pos": "CDM", "rating": 84, "price": 65},
        ],
    },
    "Manchester City": {
        "logo_path": os.path.join(LOGO_DIR, "mancity.png"),
        "players": [
            {"name": "Ederson", "pos": "GK", "rating": 88, "price": 95},
            {"name": "Kyle Walker", "pos": "RB", "rating": 83, "price": 40},
            {"name": "Ruben Dias", "pos": "CB", "rating": 89, "price": 95},
            {"name": "Manuel Akanji", "pos": "CB", "rating": 84, "price": 60},
            {"name": "Jack Grealish", "pos": "LW", "rating": 82, "price": 55},
            {"name": "Kevin De Bruyne", "pos": "CM", "rating": 92, "price": 150},
            {"name": "Rodri", "pos": "CDM", "rating": 89, "price": 110},
            {"name": "Phil Foden", "pos": "CAM", "rating": 88, "price": 120},
            {"name": "Erling Haaland", "pos": "ST", "rating": 93, "price": 200},
            {"name": "Jack Grealish", "pos": "LW", "rating": 82, "price": 55},
            {"name": "Riyad Mahrez", "pos": "RW", "rating": 83, "price": 60},
        ],
    },
    "Manchester United": {
        "logo_path": os.path.join(LOGO_DIR, "manutd.png"),
        "players": [
            {"name": "David De Gea", "pos": "GK", "rating": 82, "price": 30},
            {"name": "Diogo Dalot", "pos": "RB", "rating": 80, "price": 35},
            {"name": "Raphaël Varane", "pos": "CB", "rating": 86, "price": 70},
            {"name": "Lisandro Martínez", "pos": "CB", "rating": 83, "price": 60},
            {"name": "Luke Shaw", "pos": "LB", "rating": 82, "price": 50},
            {"name": "Bruno Fernandes", "pos": "CAM", "rating": 89, "price": 110},
            {"name": "Casemiro", "pos": "CDM", "rating": 87, "price": 80},
            {"name": "Marcus Rashford", "pos": "LW", "rating": 88, "price": 100},
            {"name": "Antony", "pos": "RW", "rating": 80, "price": 45},
            {"name": "Anthony Martial", "pos": "ST", "rating": 78, "price": 30},
            {"name": "Mason Greenwood", "pos": "ST", "rating": 79, "price": 35},
        ],
    },
    "Newcastle": {
        "logo_path": os.path.join(LOGO_DIR, "newcastle.png"),
        "players": [
            {"name": "Nick Pope", "pos": "GK", "rating": 84, "price": 50},
            {"name": "Kieran Trippier", "pos": "RB", "rating": 84, "price": 65},
            {"name": "Sven Botman", "pos": "CB", "rating": 80, "price": 45},
            {"name": "Dan Burn", "pos": "CB", "rating": 76, "price": 20},
            {"name": "Matt Targett", "pos": "LB", "rating": 77, "price": 25},
            {"name": "Bruno Guimarães", "pos": "CM", "rating": 88, "price": 95},
            {"name": "Joelinton", "pos": "CM", "rating": 79, "price": 35},
            {"name": "Miguel Almirón", "pos": "RW", "rating": 78, "price": 30},
            {"name": "Callum Wilson", "pos": "ST", "rating": 82, "price": 55},
            {"name": "Alexander Isak", "pos": "ST", "rating": 84, "price": 75},
            {"name": "Allan Saint-Maximin", "pos": "LW", "rating": 80, "price": 40},
        ],
    }
}

for name, data in clubs.items():
    players = data["players"]
    avg = sum(p["rating"] for p in players) / len(players)
    data["avg_rating"] = avg
    data["logo"] = get_base64_image(data.get("logo_path", os.path.join(LOGO_DIR, "default.png")))

transfer_market = [
    {"name": "Kylian Mbappe", "pos": "ST", "rating": 92, "price": 180, "club": None},
    {"name": "Jude Bellingham", "pos": "CM", "rating": 90, "price": 150, "club": None},
    {"name": "Vinicius Jr", "pos": "LW", "rating": 89, "price": 130, "club": None},
    {"name": "Pedri", "pos": "CM", "rating": 86, "price": 100, "club": None},
    {"name": "Erling Haaland", "pos": "ST", "rating": 93, "price": 200, "club": None}
]

if "money" not in st.session_state:
    st.session_state.money = 200  # manager budget (in million)
if "managed_club" not in st.session_state:
    st.session_state.managed_club = "Arsenal"
if "stats" not in st.session_state:
    st.session_state.stats = {"W": 0, "D": 0, "L": 0}
if "last_match" not in st.session_state:
    st.session_state.last_match = None

# ===== CSS =====
st.markdown(
    """
    <style>
    :root {
        --main-red: #c8102e;
        --gold: #e7c26f;
        --card-bg: #ffffff;
    }
    .stApp {
        background: linear-gradient(180deg, #fafafa, #fffdf9);
    }
    .top-row { display:flex; gap:16px; align-items:center; justify-content:space-between; flex-wrap:wrap; }
    .club-card { background: var(--card-bg); padding:12px; border-radius:12px; box-shadow: 0 6px 20px rgba(0,0,0,0.06); }
    .club-name { font-weight:700; color:var(--main-red); margin:0; }
    .muted { color:#666; font-size:0.9rem; }
    .scoreboard { display:flex; align-items:center; justify-content:center; gap:18px; padding:12px; border-radius:12px; background: linear-gradient(135deg, var(--main-red), var(--gold)); color:white; }
    .scoreboard img { width:72px; height:72px; border-radius:50%; border:3px solid rgba(255,255,255,0.6); object-fit:cover; }
    .scoreboard h2 { margin:0; font-size:2rem; }
    @media (max-width: 768px) {
        .scoreboard img { width:56px; height:56px; }
        .scoreboard h2 { font-size:1.5rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Manager Controls")
    managed = st.selectbox("Pilih klub yang dikelola:", list(clubs.keys()), index=list(clubs.keys()).index(st.session_state.managed_club) if st.session_state.managed_club in clubs else 0)
    st.session_state.managed_club = managed
    st.markdown("---")
    st.markdown(f"**Dana klub:** £{st.session_state.money}M")
    st.markdown(f"**Statistik:** W {st.session_state.stats['W']} | D {st.session_state.stats['D']} | L {st.session_state.stats['L']}")
    if st.button("Reset Progress"):
        st.session_state.money = 200
        st.session_state.stats = {"W": 0, "D": 0, "L": 0}
        st.session_state.last_match = None

tabs = st.tabs(["Club", "Match", "Transfer", "Stats"])

with tabs[0]:
    st.markdown("<div class='top-row'>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"<div class='club-card'><h3 class='club-name'>{st.session_state.managed_club}</h3><p class='muted'>Roster & informasi klub</p></div>", unsafe_allow_html=True)
        managed_players = clubs[st.session_state.managed_club]["players"]
        # roster list
        st.subheader("Daftar Pemain")
        for p in managed_players:
            st.markdown(
                f"<div class='club-card' style='margin-top:8px;'><b>{p['name']}</b> — {p['pos']} | Rating: {p['rating']} | Harga: £{p['price']}M</div>",
                unsafe_allow_html=True,
            )
    with col2:
        logo_data = clubs[st.session_state.managed_club]["logo"]
        if logo_data:
            st.markdown(f"<div style='text-align:center'><img src='{logo_data}' width='120'></div>", unsafe_allow_html=True)
        st.markdown(f"Rata-rata rating: **{clubs[st.session_state.managed_club]['avg_rating']:.1f}**")
    st.markdown("</div>", unsafe_allow_html=True)

with tabs[1]:
    st.header("Simulasi Pertandingan")
    managed_players = clubs[st.session_state.managed_club]["players"]
    names = [p["name"] for p in managed_players]
    selected_players = st.multiselect("Pilih 11 pemain untuk starting lineup:", names)

    opponent = st.selectbox("Pilih lawan:", [c for c in clubs.keys() if c != st.session_state.managed_club])
    opponent_data = clubs[opponent]

    # show opponent preview
    colA, colB = st.columns([3, 2])
    with colA:
        st.markdown(f"Anda: **{st.session_state.managed_club}** vs Lawan: **{opponent}**")
    with colB:
        if opponent_data["logo"]:
            st.markdown(f"<div style='text-align:right'><img src='{opponent_data['logo']}' width='80'></div>", unsafe_allow_html=True)

    if st.button("Mulai Pertandingan"):
        if len(selected_players) != 11:
            st.warning("Pilih tepat 11 pemain untuk memulai pertandingan.")
        else:
            lineup = [p for p in managed_players if p["name"] in selected_players]
            team_rating = sum(p["rating"] for p in lineup) / len(lineup)
            opponent_rating = opponent_data["avg_rating"]

            def simulate_match(team_rating, opponent_rating):
                """Simulate a match result based on team ratings."""
                team_chance = team_rating / (team_rating + opponent_rating)
                opponent_chance = opponent_rating / (team_rating + opponent_rating)
                score_team = random.randint(0, 5) if random.random() < team_chance else random.randint(0, 2)
                score_opponent = random.randint(0, 5) if random.random() < opponent_chance else random.randint(0, 2)
                return score_team, score_opponent

            score_team, score_opponent = simulate_match(team_rating, opponent_rating)

            st.session_state.last_match = {
                "team": st.session_state.managed_club,
                "opponent": opponent,
                "score_team": score_team,
                "score_opponent": score_opponent,
                "team_logo": clubs[st.session_state.managed_club]["logo"],
                "opponent_logo": opponent_data["logo"],
            }

            if score_team > score_opponent:
                st.session_state.stats["W"] += 1
                st.session_state.money += 20
                st.success(f"Kemenangan! {st.session_state.managed_club} {score_team} - {score_opponent} {opponent}")
            elif score_team == score_opponent:
                st.session_state.stats["D"] += 1
                st.info(f"Seri: {st.session_state.managed_club} {score_team} - {score_opponent} {opponent}")
            else:
                st.session_state.stats["L"] += 1
                st.error(f"Kekalahan: {st.session_state.managed_club} {score_team} - {score_opponent} {opponent}")

    if st.session_state.last_match:
        lm = st.session_state.last_match
        st.markdown(
            f"""
            <div class="scoreboard" style="margin-top:12px;">
                <div style="text-align:center;">
                    <img src="{lm['team_logo']}" />
                    <div><b>{lm['team']}</b></div>
                </div>
                <div style="text-align:center;"><h2>{lm['score_team']} - {lm['score_opponent']}</h2></div>
                <div style="text-align:center;">
                    <img src="{lm['opponent_logo']}" />
                    <div><b>{lm['opponent']}</b></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

with tabs[2]:
    st.header("Bursa Transfer")
    st.markdown(f"Anggaran saat ini: **£{st.session_state.money}M**")
    for player in transfer_market:
        cols = st.columns([3, 1, 1, 1])
        cols[0].write(player["name"])
        cols[1].write(player["pos"])
        cols[2].write(f"Rating {player['rating']}")
        if cols[3].button(f"Beli £{player['price']}M", key=f"buy_{player['name']}"):
            if st.session_state.money >= player["price"]:
                player_copy = player.copy()
                player_copy.setdefault("price", player_copy.pop("price", 0))
                clubs[st.session_state.managed_club]["players"].append(player_copy)
                players = clubs[st.session_state.managed_club]["players"]
                clubs[st.session_state.managed_club]["avg_rating"] = sum(p["rating"] for p in players) / len(players)
                st.session_state.money -= player["price"]
                st.success(f"{player['name']} dibeli untuk {st.session_state.managed_club}!")
            else:
                st.error("Dana tidak cukup untuk membeli pemain ini.")

with tabs[3]:
    st.header("Statistik")
    st.metric("Dana Klub", f"£{st.session_state.money}M")
    st.write(f"Menang: {st.session_state.stats['W']}  |  Seri: {st.session_state.stats['D']}  |  Kalah: {st.session_state.stats['L']}")
    st.markdown("Riwayat pertandingan terakhir:")
    if st.session_state.last_match:
        lm = st.session_state.last_match
        st.write(f"{lm['team']} {lm['score_team']} - {lm['score_opponent']} {lm['opponent']}")
    else:
        st.write("_Belum ada pertandingan_")

# ===== Footer =====
st.markdown("---")
st.caption("iseng @khaissaint")