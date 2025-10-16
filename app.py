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
            {"name": "Riyad Mahrez", "pos": "RW", "rating": 83, "price": 60},
        ],
    },
    "Manchester United": {
        "logo_path": os.path.join(LOGO_DIR, "manunited.png"),
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
        "logo_path": os.path.join(LOGO_DIR, "newcastleunited.png"),
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
    },
}

for name, data in clubs.items():
    players = data["players"]
    data["avg_rating"] = sum(p["rating"] for p in players) / len(players)
    data["logo"] = get_base64_image(data.get("logo_path", os.path.join(LOGO_DIR, "default.png")))

st.sidebar.title("Football Manager Mini")

if "managed_club" not in st.session_state:
    st.session_state.managed_club = None
if "points" not in st.session_state:
    st.session_state.points = {c: 0 for c in clubs}

if st.session_state.managed_club is None:
    st.sidebar.subheader("Pilih klub untuk kamu kelola:")
    club_choice = st.sidebar.selectbox("Pilih klub:", list(clubs.keys()))
    if st.sidebar.button("Mulai Kelola Klub"):
        st.session_state.managed_club = club_choice
        st.experimental_rerun()
else:
    st.sidebar.success(f"Kamu mengelola {st.session_state.managed_club}")
    if st.sidebar.button("Ganti Klub"):
        st.session_state.managed_club = None
        st.experimental_rerun()

# ===== Tabs =====
tabs = st.tabs(["Club", "Match", "Transfer", "Stats"])

# ===== CLUB TAB =====
with tabs[0]:
    club = st.session_state.managed_club
    if club:
        data = clubs[club]
        st.markdown(f"<h2>{club}</h2>", unsafe_allow_html=True)
        st.image(data["logo_path"], width=150)
        st.write(f"Average Rating: {data['avg_rating']:.1f}")

        st.subheader("Daftar Pemain")
        for p in data["players"]:
            st.write(f"{p['name']} - {p['pos']} | Rating: {p['rating']} | Harga: £{p['price']}M")
    else:
        st.info("Pilih klub dulu di sidebar.")

# ===== MATCH TAB =====
with tabs[1]:
    club = st.session_state.managed_club
    if club:
        st.subheader("Simulasi Pertandingan")
        opponent = st.selectbox("Pilih lawan:", [c for c in clubs if c != club])
        if st.button("Mainkan Pertandingan"):
            club_rating = clubs[club]["avg_rating"]
            opp_rating = clubs[opponent]["avg_rating"]
            club_score = random.randint(0, 4)
            opp_score = random.randint(0, 4)
            if club_rating > opp_rating + random.uniform(0, 5):
                club_score += 1
            elif opp_rating > club_rating + random.uniform(0, 5):
                opp_score += 1
            st.success(f"Hasil: {club} {club_score} - {opp_score} {opponent}")
            if club_score > opp_score:
                st.session_state.points[club] += 3
            elif club_score == opp_score:
                st.session_state.points[club] += 1
                st.session_state.points[opponent] += 1
            else:
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
            for p in cdata["players"]:
                all_players.append((cname, p))
        player = st.selectbox(
            "Pilih pemain untuk dibeli:", [f"{p['name']} ({club_name})" for club_name, p in all_players]
        )
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
