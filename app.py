import streamlit as st
import random
import base64
import os

# ===== Fungsi untuk load logo club =====
def get_base64_image(image_path):
    if not os.path.exists(image_path):
        return None
    with open(image_path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()

# ===== Path direktori logo =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_DIR = os.path.join(BASE_DIR, "logos")

# ===== Daftar klub dan logo =====
clubs = {
    "Arsenal": {"rating": 85, "logo": get_base64_image(os.path.join(LOGO_DIR, "arsenal.png"))},
    "Chelsea": {"rating": 83, "logo": get_base64_image(os.path.join(LOGO_DIR, "chelsea.png"))},
    "Liverpool": {"rating": 86, "logo": get_base64_image(os.path.join(LOGO_DIR, "liverpool.png"))},
    "Manchester City": {"rating": 89, "logo": get_base64_image(os.path.join(LOGO_DIR, "mancity.png"))},
    "Manchester United": {"rating": 84, "logo": get_base64_image(os.path.join(LOGO_DIR, "manunited.png"))},
    "Newcastle United": {"rating": 82, "logo": get_base64_image(os.path.join(LOGO_DIR, "newcastleunited.png"))},
}

# ===== Daftar pemain Arsenal (contoh) =====
arsenal_players = [
    "David Raya (GK)", "Ben White (DF)", "William Saliba (DF)", "Gabriel Magalhães (DF)", "Kieran Tierney (DF)",
    "Martin Ødegaard (MF)", "Declan Rice (MF)", "Thomas Partey (MF)",
    "Bukayo Saka (FW)", "Gabriel Jesus (FW)", "Leandro Trossard (FW)"
]

# ===== Fungsi simulasi pertandingan =====
def simulate_match(team_rating, opponent_rating):
    luck_team = random.uniform(-5, 5)
    luck_opponent = random.uniform(-5, 5)
    score_team = max(0, int((team_rating + luck_team) / 20))
    score_opponent = max(0, int((opponent_rating + luck_opponent) / 20))
    return score_team, score_opponent

# ===== Inisialisasi state =====
if "money" not in st.session_state:
    st.session_state.money = 200
if "squad" not in st.session_state:
    st.session_state.squad = arsenal_players.copy()
if "stats" not in st.session_state:
    st.session_state.stats = {"W": 0, "D": 0, "L": 0}
if "last_match" not in st.session_state:
    st.session_state.last_match = None

# ===== CSS =====
st.markdown("""
<style>
body {
    background-color: #fafafa;
}
h1, h2, h3 {
    text-align: center;
    font-family: 'Poppins', sans-serif;
}
.team-card {
    text-align: center;
    border-radius: 15px;
    background: white;
    padding: 15px;
    margin: 10px;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.1);
}
img {
    max-width: 90px;
    height: auto;
}
@media (max-width: 768px) {
    img { max-width: 60px; }
    h1 { font-size: 22px; }
}
</style>
""", unsafe_allow_html=True)

# ===== Judul =====
st.markdown("<h1>Mini Football Manager</h1>", unsafe_allow_html=True)

# ===== Sidebar klub pilihan =====
team_name = st.sidebar.selectbox("Pilih Klub Anda:", list(clubs.keys()))
team_info = clubs[team_name]

# ===== Tampilkan logo klub =====
if team_info["logo"]:
    st.markdown(f"<div style='text-align:center'><img src='{team_info['logo']}'></div>", unsafe_allow_html=True)

# ===== Daftar pemain =====
st.subheader(f"Daftar Pemain {team_name}")
if team_name == "Arsenal":
    for player in arsenal_players:
        st.markdown(f"- {player}")
else:
    st.markdown("_Daftar pemain belum tersedia untuk klub ini._")

# ===== Simulasi pertandingan =====
st.divider()
st.subheader("Simulasi Pertandingan")

opponent_name = st.selectbox("Pilih Lawan:", [club for club in clubs.keys() if club != team_name])

if st.button("Mulai Pertandingan 🎮"):
    team_rating = clubs[team_name]["rating"]
    opponent_rating = clubs[opponent_name]["rating"]

    score_team, score_opponent = simulate_match(team_rating, opponent_rating)
    st.session_state.last_match = (team_name, opponent_name, score_team, score_opponent)

    if score_team > score_opponent:
        st.session_state.stats["W"] += 1
        result = "Menang "
    elif score_team < score_opponent:
        st.session_state.stats["L"] += 1
        result = "Kalah "
    else:
        st.session_state.stats["D"] += 1
        result = "Seri "

    st.success(f"Hasil: {team_name} {score_team} - {score_opponent} {opponent_name}")
    st.info(f"Hasil pertandingan: {result}")

# ===== Statistik =====
st.divider()
st.subheader("Statistik Musim Ini")
stats = st.session_state.stats
st.markdown(f"**Menang:** {stats['W']} | **Seri:** {stats['D']} | **Kalah:** {stats['L']}")

# ===== Informasi terakhir =====
if st.session_state.last_match:
    team, opponent, s1, s2 = st.session_state.last_match
    st.caption(f"Pertandingan terakhir: {team} {s1}-{s2} {opponent}")