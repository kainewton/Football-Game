import streamlit as st
import random
import os
import base64

st.set_page_config(page_title="Football Manager: Arsenal", layout="centered")

def get_base64_image(image_path):
    if not os.path.exists(image_path):
        image_path = "logos/default.png"
    with open(image_path, "rb") as f:
        data = f.read()
    return "data:image/png;base64," + base64.b64encode(f.read()).decode()

arsenal_players = [
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
]

transfer_market = [
    {"name": "Kylian Mbappe", "pos": "ST", "rating": 92, "price": 180},
    {"name": "Erling Haaland", "pos": "ST", "rating": 93, "price": 200},
    {"name": "Jude Bellingham", "pos": "CM", "rating": 90, "price": 150},
    {"name": "Vinicius Jr", "pos": "LW", "rating": 89, "price": 130},
    {"name": "Pedri", "pos": "CM", "rating": 86, "price": 100},
]

opponents = [
    {"name": "Chelsea", "rating": 83, "logo": "logos/chelsea.png"},
    {"name": "Liverpool", "rating": 86, "logo": "logos/liverpool.png"},
    {"name": "Manchester City", "rating": 90, "logo": "logos/mancity.png"},
    {"name": "Manchester United", "rating": 82, "logo": "logos/manunited.png"},
    {"name": "Newcastle", "rating": 84, "logo": "logos/newcastleunited.png"},
]

def simulate_match(team_rating, opponent_rating):
    luck_team = random.uniform(-5, 5)
    luck_opponent = random.uniform(-5, 5)
    score_team = max(0, int((team_rating + luck_team) / 20))
    score_opponent = max(0, int((opponent_rating + luck_opponent) / 20))
    return score_team, score_opponent

if "money" not in st.session_state:
    st.session_state.money = 200
if "squad" not in st.session_state or len(st.session_state.squad) == 0:
    st.session_state.squad = arsenal_players.copy()
if "stats" not in st.session_state:
    st.session_state.stats = {"W": 0, "D": 0, "L": 0}
if "last_match" not in st.session_state:
    st.session_state.last_match = None

# ====== CSS ======
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #fafafa 40%, #f5f0f0);
}
h1, h2, h3, h4 {
    color: #db0007;
    text-align: center;
    font-family: 'Poppins', sans-serif;
}
.stTabs [data-baseweb="tab-list"] {
    justify-content: center;
}
.stTabs [data-baseweb="tab"] {
    font-weight: 600;
    color: #db0007;
}
.card {
    background-color: #fff;
    border-radius: 15px;
    padding: 1rem;
    margin-bottom: 1rem;
    box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    transition: 0.3s;
}
.card:hover {
    transform: scale(1.02);
    box-shadow: 0 6px 18px rgba(0,0,0,0.15);
}
.player-row {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
}
.player-row p {
    margin: 0.3rem 0;
}
div.stButton > button {
    background-color: #db0007;
    color: white;
    font-weight: 600;
    border-radius: 8px;
}
div.stButton > button:hover {
    transform: scale(1.03);
    background-color: #e01b1b;
}
.scoreboard {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
    background: linear-gradient(135deg, #db0007, #e7c26f);
    color: white;
    padding: 1rem;
    border-radius: 15px;
    backdrop-filter: blur(8px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}
.scoreboard img {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    margin: 0 1rem;
    border: 3px solid white;
}
.scoreboard h3 {
    font-size: 2.5rem;
}
@media (max-width: 768px) {
    .scoreboard h3 { font-size: 2rem; }
    .scoreboard img { width: 65px; height: 65px; }
    .card p { font-size: 0.9rem; }
}
</style>
""", unsafe_allow_html=True)

# ====== Tabs ======
tabs = st.tabs(["Home", "Squad", "Match"])

# --- HOME ---
with tabs[0]:
    arsenal_logo = get_base64_image("logos/arsenal.png")
    st.markdown(f"<div style='text-align:center;'><img src='{arsenal_logo}' width='120'></div>", unsafe_allow_html=True)
    st.markdown("### Football Manager Mini: Arsenal Edition ⚽")
    st.write(f"Dana Klub: **£{st.session_state.money} juta**")
    st.write(f"Statistik: W {st.session_state.stats['W']} | D {st.session_state.stats['D']} | L {st.session_state.stats['L']}")

# --- SQUAD ---
with tabs[1]:
    st.subheader("Daftar Pemain Arsenal")
    for p in st.session_state.squad:
        st.markdown(
            f"""
            <div class="card player-row">
                <p><b>{p['name']}</b> ({p['pos']})</p>
                <p>Rating: {p['rating']}</p>
                <p>Harga: £{p['price']}M</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.subheader("Bursa Transfer")
    with st.expander("Lihat Daftar Pemain di Bursa Transfer"):
        for player in transfer_market:
            col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
            col1.write(player["name"])
            col2.write(player["pos"])
            col3.write(f"Rating {player['rating']}")
            if col4.button(f"Beli (£{player['price']}M)", key=player["name"]):
                if st.session_state.money >= player["price"]:
                    st.session_state.money -= player["price"]
                    st.session_state.squad.append(player)
                    st.success(f"{player['name']} berhasil dibeli!")
                else:
                    st.error("Uang tidak cukup!")

# --- MATCH ---
with tabs[2]:
    st.header("Simulasi Pertandingan")

    selected_players = st.multiselect(
        "Pilih 11 pemain untuk starting lineup:",
        [p["name"] for p in st.session_state.squad],
    )

    opponent = st.selectbox("Pilih lawan:", [o["name"] for o in opponents])
    opponent_data = next(o for o in opponents if o["name"] == opponent)

    if st.button("Mulai Pertandingan"):
        if len(selected_players) != 11:
            st.warning("Pilih tepat 11 pemain untuk memulai pertandingan.")
        else:
            lineup = [p for p in st.session_state.squad if p["name"] in selected_players]
            avg_rating = sum(p["rating"] for p in lineup) / len(lineup)

            score_team, score_opponent = simulate_match(avg_rating, opponent_data["rating"])
            st.session_state.last_match = {
                "opponent": opponent,
                "score_team": score_team,
                "score_opponent": score_opponent,
                "logo": opponent_data["logo"]
            }

            if score_team > score_opponent:
                st.session_state.stats["W"] += 1
                st.session_state.money += 20
                st.success("Kemenangan! Arsenal tampil luar biasa!")
                st.balloons()
            elif score_team == score_opponent:
                st.session_state.stats["D"] += 1
                st.info("Hasil imbang, pertandingan berjalan ketat.")
            else:
                st.session_state.stats["L"] += 1
                st.error("Kekalahan! Arsenal perlu evaluasi.")

    if st.session_state.last_match:
        lm = st.session_state.last_match
        st.markdown(
            f"""
            <div class='scoreboard'>
                <div><img src='{arsenal_logo}'><p><b>Arsenal</b></p></div>
                <h3>{lm['score_team']} - {lm['score_opponent']}</h3>
                <div><img src='{get_base64_image(lm['logo'])}'><p><b>{lm['opponent']}</b></p></div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("---")
st.caption("Created by Khai | iseng")