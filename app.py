import streamlit as st
import random
import os
import base64

st.set_page_config(page_title="Mini Football Manager", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_DIR = os.path.join(BASE_DIR, "logos")

def get_base64_image(image_path):
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
        "logo": "arsenal.png",
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
        "logo": "chelsea.png",
        "players": [
            {"name": "Kepa", "pos": "GK", "rating": 80, "price": 25},
            {"name": "Reece James", "pos": "RB", "rating": 84, "price": 55},
            {"name": "Thiago Silva", "pos": "CB", "rating": 83, "price": 40},
            {"name": "Ben Chilwell", "pos": "LB", "rating": 81, "price": 30},
            {"name": "Enzo Fernandez", "pos": "CM", "rating": 84, "price": 70},
            {"name": "Raheem Sterling", "pos": "LW", "rating": 85, "price": 80},
            {"name": "Nicolas Jackson", "pos": "ST", "rating": 80, "price": 35},
        ],
    },
    "Liverpool": {
        "logo": "liverpool.png",
        "players": [
            {"name": "Alisson", "pos": "GK", "rating": 89, "price": 90},
            {"name": "Virgil van Dijk", "pos": "CB", "rating": 90, "price": 100},
            {"name": "Trent Alexander-Arnold", "pos": "RB", "rating": 88, "price": 95},
            {"name": "Mohamed Salah", "pos": "RW", "rating": 91, "price": 120},
            {"name": "Luis Díaz", "pos": "LW", "rating": 86, "price": 85},
            {"name": "Diogo Jota", "pos": "ST", "rating": 85, "price": 75},
        ],
    },
    "Manchester City": {
        "logo": "mancity.png",
        "players": [
            {"name": "Ederson", "pos": "GK", "rating": 88, "price": 95},
            {"name": "Ruben Dias", "pos": "CB", "rating": 89, "price": 95},
            {"name": "Kevin De Bruyne", "pos": "CM", "rating": 92, "price": 150},
            {"name": "Phil Foden", "pos": "CAM", "rating": 88, "price": 120},
            {"name": "Erling Haaland", "pos": "ST", "rating": 93, "price": 200},
        ],
    },
    "Manchester United": {
        "logo": "manunited.png",
        "players": [
            {"name": "David De Gea", "pos": "GK", "rating": 82, "price": 30},
            {"name": "Raphaël Varane", "pos": "CB", "rating": 86, "price": 70},
            {"name": "Casemiro", "pos": "CDM", "rating": 87, "price": 80},
            {"name": "Bruno Fernandes", "pos": "CAM", "rating": 89, "price": 110},
            {"name": "Marcus Rashford", "pos": "LW", "rating": 88, "price": 100},
        ],
    },
    "Newcastle": {
        "logo": "newcastleunited.png",
        "players": [
            {"name": "Nick Pope", "pos": "GK", "rating": 84, "price": 50},
            {"name": "Kieran Trippier", "pos": "RB", "rating": 84, "price": 65},
            {"name": "Bruno Guimarães", "pos": "CM", "rating": 88, "price": 95},
            {"name": "Miguel Almirón", "pos": "RW", "rating": 78, "price": 30},
            {"name": "Alexander Isak", "pos": "ST", "rating": 84, "price": 75},
        ],
    },
}

for club, data in clubs.items():
    data["avg_rating"] = sum(p["rating"] for p in data["players"]) / len(data["players"])

if "managed_club" not in st.session_state:
    st.session_state.managed_club = None
if "points" not in st.session_state:
    st.session_state.points = {c: 0 for c in clubs}

st.sidebar.title("Mini Football Manager")

if st.session_state.managed_club is None:
    club_choice = st.sidebar.selectbox("Pilih klub yang ingin kamu kelola:", list(clubs.keys()))
    if st.sidebar.button("Mulai Kelola Klub"):
        st.session_state.managed_club = club_choice
        st.rerun()
else:
    st.sidebar.success(f"Kamu sekarang mengelola {st.session_state.managed_club}")
    if st.sidebar.button("Ganti Klub"):
        st.session_state.managed_club = None
        st.rerun()

# ===== TAB =====
tabs = st.tabs(["Club", "Match", "Transfer", "Stats"])

# ===== CLUB TAB =====
with tabs[0]:
    club = st.session_state.managed_club
    if club:
        st.image(f"logos/{clubs[club]['logo']}", width=150)
        st.markdown(f"## {club}")
        st.write(f"Average Rating: {clubs[club]['avg_rating']:.1f}")

        st.subheader("Daftar Pemain")
        for p in clubs[club]["players"]:
            st.write(f"{p['name']} ({p['pos']}) — Rating {p['rating']} — £{p['price']}M")
    else:
        st.info("Pilih klub dulu di sidebar.")

# ===== MATCH TAB =====
with tabs[1]:
    club = st.session_state.managed_club
    if club:
        st.subheader("Simulasi Pertandingan")
        opponent = st.selectbox("Pilih lawan:", [c for c in clubs.keys() if c != club])
        if st.button("Mainkan Pertandingan"):
            team_rating = clubs[club]["avg_rating"]
            opponent_rating = clubs[opponent]["avg_rating"]
            score_team = random.randint(0, 4)
            score_opp = random.randint(0, 4)

            if team_rating > opponent_rating:
                score_team += random.choice([0, 1])
            elif opponent_rating > team_rating:
                score_opp += random.choice([0, 1])

            st.markdown(f"### {club} {score_team} - {score_opp} {opponent}")

            if score_team > score_opp:
                st.success(f"{club} MENANG!")
                st.session_state.points[club] += 3
            elif score_team == score_opp:
                st.info("Seri!")
                st.session_state.points[club] += 1
                st.session_state.points[opponent] += 1
            else:
                st.error(f"{opponent} menang kali ini.")
                st.session_state.points[opponent] += 3
    else:
        st.info("Pilih klub dulu di sidebar.")

# ===== TRANSFER TAB =====
with tabs[2]:
    club = st.session_state.managed_club
    if club:
        st.subheader("Transfer Market")
        all_players = []
        for cname, cdata in clubs.items():
            if cname != club:
                for p in cdata["players"]:
                    all_players.append((cname, p))
        player = st.selectbox("Pilih pemain untuk dibeli:", [f"{p['name']} ({c})" for c, p in all_players])
        if st.button("Beli Pemain"):
            pname, from_club = player.split("(")[0].strip(), player.split("(")[1][:-1]
            target = next(p for p in clubs[from_club]["players"] if p["name"] == pname)
            clubs[club]["players"].append(target)
            clubs[from_club]["players"].remove(target)
            st.success(f"{pname} berhasil dibeli dari {from_club}!")
    else:
        st.info("Pilih klub dulu di sidebar.")

# ===== STATS TAB =====
with tabs[3]:
    st.subheader("Klasemen Sementara")
    sorted_points = sorted(st.session_state.points.items(), key=lambda x: x[1], reverse=True)
    for i, (team, pts) in enumerate(sorted_points, start=1):
        st.markdown(f"**{i}. {team}** — {pts} pts")

    st.divider()
    st.caption("iseng @khaissaint")