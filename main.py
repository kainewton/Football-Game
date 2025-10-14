import streamlit as st
import random

# ====== arsenal players ======
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

# ====== bursa Transfer ======
transfer_market = [
    {"name": "Kylian Mbappe", "pos": "ST", "rating": 92, "price": 180},
    {"name": "Erling Haaland", "pos": "ST", "rating": 93, "price": 200},
    {"name": "Jude Bellingham", "pos": "CM", "rating": 90, "price": 150},
    {"name": "Vinicius Jr", "pos": "LW", "rating": 89, "price": 130},
    {"name": "Pedri", "pos": "CM", "rating": 86, "price": 100},
]

# ====== opposing team ======
opponents = [
    {"name": "Chelsea", "rating": 83},
    {"name": "Liverpool", "rating": 86},
    {"name": "Manchester City", "rating": 90},
    {"name": "Manchester United", "rating": 82},
    {"name": "Newcastle", "rating": 84},
]

# ====== match simulation ======
def simulate_match(team_rating, opponent_rating):
    luck_team = random.uniform(-5, 5)
    luck_opponent = random.uniform(-5, 5)
    score_team = max(0, int((team_rating + luck_team) / 20))
    score_opponent = max(0, int((opponent_rating + luck_opponent) / 20))
    return score_team, score_opponent

# ====== streamlit App ======
st.set_page_config(page_title="Football Manager Mini", layout="centered")
st.title("Football Manager Mini: Arsenal Edition (v2.1)")

# session state 
if "money" not in st.session_state:
    st.session_state.money = 200  # juta pound
if "squad" not in st.session_state:
    st.session_state.squad = arsenal_players.copy()

# --- tim info ---
st.subheader("Informasi Klub")
team_rating = sum(p["rating"] for p in st.session_state.squad) / len(st.session_state.squad)
st.write(f"Total Pemain: {len(st.session_state.squad)}")
st.write(f"Rata-rata Rating Tim: {team_rating:.1f}")
st.write(f"Sisa Uang Klub: £{st.session_state.money} juta")

# --- player transfers ---
st.subheader("Bursa Transfer")
with st.expander("Lihat Daftar Pemain di Bursa Transfer"):
    for player in transfer_market:
        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
        with col1:
            st.write(player["name"])
        with col2:
            st.write(player["pos"])
        with col3:
            st.write(f"Rating {player['rating']}")
        with col4:
            price = player["price"]
            if st.button(f"Beli (£{price}M)", key=player["name"]):
                if st.session_state.money >= price:
                    st.session_state.squad.append(player)
                    st.session_state.money -= price
                    st.success(f"{player['name']} berhasil dibeli!")
                else:
                    st.error("Uang klub tidak mencukupi.")

# --- select players ---
st.subheader("Pilih 11 Pemain untuk Starting Lineup")
selected_players = st.multiselect(
    "Pilih pemain:", 
    [p["name"] for p in st.session_state.squad]
)

if len(selected_players) == 11:
    lineup = [p for p in st.session_state.squad if p["name"] in selected_players]
    avg_rating = sum(p["rating"] for p in lineup) / len(lineup)
    opponent = st.selectbox("Pilih lawan:", [o["name"] for o in opponents])
    opponent_data = next(o for o in opponents if o["name"] == opponent)

    if st.button("Mulai Pertandingan"):
        score_team, score_opponent = simulate_match(avg_rating, opponent_data["rating"])
        st.markdown(f"### Hasil: Arsenal {score_team} - {score_opponent} {opponent_data['name']}")
        if score_team > score_opponent:
            st.success("Kemenangan untuk Arsenal!")
        elif score_team == score_opponent:
            st.info("Hasil imbang.")
        else:
            st.error("Kekalahan. Perlu evaluasi taktik.")
else:
    st.info("Pilih tepat 11 pemain untuk memulai pertandingan.")

st.markdown("---")
st.caption("Football Manager Mini | Created by Khai")