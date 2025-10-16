import streamlit as st
import random

# ====== DATA PEMAIN ======
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

# ====== FUNGSI MATCH ======
def simulate_match(team_rating, opponent_rating):
    diff = team_rating - opponent_rating
    prob_win = 0.5 + (diff / 50)
    result = random.random()

    if result < prob_win:
        score_team = random.randint(1, 4)
        score_opponent = random.randint(0, score_team)
    elif result < 0.95:
        score_team = score_opponent = random.randint(0, 2)
    else:
        score_team = random.randint(0, 2)
        score_opponent = random.randint(score_team, 4)
    return score_team, score_opponent


# ====== STREAMLIT ======
st.set_page_config(page_title="Football Manager Mini: Arsenal Edition", layout="wide")
st.title("Football Manager Mini: Arsenal Edition")

# ====== SESSION STATE ======
if "money" not in st.session_state:
    st.session_state.money = 200
if "squad" not in st.session_state:
    st.session_state.squad = arsenal_players.copy()
if "stats" not in st.session_state:
    st.session_state.stats = {"W": 0, "D": 0, "L": 0}

# ====== MENU ======
tabs = st.tabs(["Squad", "Transfer Market", "Match", "Club Info"])

# ====== SQUAD ======
with tabs[0]:
    st.header("Daftar Pemain Arsenal")
    for p in st.session_state.squad:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"{p['name']}")
        with col2:
            st.write(p["pos"])
        with col3:
            st.write(f"Rating {p['rating']}")

    avg_rating = sum(p["rating"] for p in st.session_state.squad) / len(st.session_state.squad)
    st.info(f"Rata-rata rating tim: {avg_rating:.1f}")

# ====== TRANSFER MARKET ======
with tabs[1]:
    st.header("Bursa Transfer Pemain")
    for player in transfer_market:
        col1, col2, col3, col4 = st.columns([3, 1, 1, 2])
        with col1:
            st.write(f"{player['name']}")
        with col2:
            st.write(player["pos"])
        with col3:
            st.write(f"Rating {player['rating']}")
        with col4:
            if st.button(f"Beli £{player['price']}M", key=player["name"]):
                if st.session_state.money >= player["price"]:
                    st.session_state.money -= player["price"]
                    st.session_state.squad.append(player)
                    st.success(f"{player['name']} berhasil dibeli.")
                else:
                    st.error("Uang tidak cukup.")

# ====== MATCH ======
with tabs[2]:
    st.header("Simulasi Pertandingan")

    selected_players = st.multiselect(
        "Pilih 11 pemain untuk starting lineup:",
        [p["name"] for p in st.session_state.squad],
    )

    opponent = st.selectbox("Pilih lawan:", [o["name"] for o in opponents])
    opponent_data = next(o for o in opponents if o["name"] == opponent)

    if "last_match" not in st.session_state:
        st.session_state.last_match = None
        
    if st.button("Mulai Pertandingan"):
        if len(selected_players) != 11:
            st.warning("Pilih tepat 11 pemain untuk memulai pertandingan.")
        else:
            lineup = [p for p in st.session_state.squad if p["name"] in selected_players]
            avg_rating = sum(p["rating"] for p in lineup) / len(lineup)

            score_team, score_opponent = simulate_match(avg_rating, opponent_data["rating"])

            st.session_state.last_match = {
                "opponent": opponent_data["name"],
                "opponent_logo": opponent_data.get("logo", None),
                "score_team": score_team,
                "score_opponent": score_opponent
            }

            if score_team > score_opponent:
                st.session_state.stats["W"] += 1
                st.session_state.money += 20
                st.balloons()
            elif score_team == score_opponent:
                st.session_state.stats["D"] += 1
            else:
                st.session_state.stats["L"] += 1

    if st.session_state.last_match:
        lm = st.session_state.last_match
        # layout dua kolom
        col1, col2, col3 = st.columns([2, 1, 2])
        with col1:
            try:
                st.image("logos/arsenal.png", width=120)
            except Exception:
                st.write("Arsenal")
        with col2:
            st.markdown(f"<h3 style='text-align: center;'>{lm['score_team']} - {lm['score_opponent']}</h3>", unsafe_allow_html=True)
        with col3:
            if lm["opponent_logo"]:
                try:
                    st.image(lm["opponent_logo"], width=120)
                except Exception:
                    st.write(lm["opponent"])
            else:
                st.write(lm["opponent"])

        st.markdown("---")

# ====== CLUB INFO ======
with tabs[3]:
    st.image("logos/arsenal.png", width=150)
    st.header("Informasi Klub")
    team_rating = sum(p["rating"] for p in st.session_state.squad) / len(st.session_state.squad)
    st.metric("Total Pemain", len(st.session_state.squad))
    st.metric("Rata-Rata Rating", f"{team_rating:.1f}")
    st.metric("Uang Klub", f"£{st.session_state.money} juta")

    st.subheader("Statistik Musim Ini")
    w, d, l = st.session_state.stats.values()
    st.write(f"Menang: {w} | Seri: {d} | Kalah: {l}")

    if st.button("Reset Game"):
        st.session_state.clear()
        st.rerun()

st.markdown("---")
st.caption("Created by Khai | Football Manager Mini")