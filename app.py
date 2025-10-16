import streamlit as st
import random
import os
import base64

st.set_page_config(page_title="Mini Football Manager", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_DIR = os.path.join(BASE_DIR, "logos")

os.makedirs(LOGO_DIR, exist_ok=True)

def get_base64_image(image_path):
    """Return data URI for an image; auto fallback ke default jika tidak ada."""
    if not os.path.exists(image_path):
        default_path = os.path.join(LOGO_DIR, "default.png")
 
        if not os.path.exists(default_path):
            import PIL.Image, PIL.ImageDraw
            img = PIL.Image.new("RGB", (200, 200), color=(220, 220, 220))
            d = PIL.ImageDraw.Draw(img)
            d.text((60, 90), "No Logo", fill=(0, 0, 0))
            img.save(default_path)
        image_path = default_path

    try:
        with open(image_path, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode()
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
        ],
    },
}

for name, data in clubs.items():
    players = data["players"]
    avg = sum(p["rating"] for p in players) / len(players)
    data["avg_rating"] = avg
    data["logo"] = get_base64_image(data.get("logo_path", os.path.join(LOGO_DIR, "default.png")))

transfer_market = [
    {"name": "Kylian Mbappe", "pos": "ST", "rating": 92, "price": 180},
    {"name": "Jude Bellingham", "pos": "CM", "rating": 90, "price": 150},
    {"name": "Vinicius Jr", "pos": "LW", "rating": 89, "price": 130},
    {"name": "Pedri", "pos": "CM", "rating": 86, "price": 100},
    {"name": "Erling Haaland", "pos": "ST", "rating": 93, "price": 200},
]

if "money" not in st.session_state:
    st.session_state.money = 200
if "managed_club" not in st.session_state:
    st.session_state.managed_club = "Arsenal"
if "stats" not in st.session_state:
    st.session_state.stats = {"W": 0, "D": 0, "L": 0}
if "last_match" not in st.session_state:
    st.session_state.last_match = None

# ======= Sidebar =======
with st.sidebar:
    st.header("Manager Controls")
    club_keys = list(clubs.keys())

    default_index = 0
    if st.session_state.get("managed_club") in club_keys:
        default_index = club_keys.index(st.session_state["managed_club"])
    managed = st.selectbox("Pilih klub yang dikelola:", club_keys, index=default_index)
    st.session_state.managed_club = managed

    st.markdown("---")
    st.markdown(f"**Dana klub:** £{st.session_state.money}M")
    st.markdown(f"**Statistik:** W {st.session_state.stats['W']} | D {st.session_state.stats['D']} | L {st.session_state.stats['L']}")
    if st.button("Reset Progress"):
        st.session_state.money = 200
        st.session_state.stats = {"W": 0, "D": 0, "L": 0}
        st.session_state.last_match = None

tabs = st.tabs(["Club", "Match", "Transfer", "Stats"])

# ==== TAB 1: CLUB ====
with tabs[0]:
    club = st.session_state.managed_club
    data = clubs[club]
    st.markdown(f"### {club}")
    if data["logo"]:
        st.image(data["logo"], width=120)
    st.write(f"**Rata-rata Rating:** {data['avg_rating']:.1f}")

    st.subheader("Daftar Pemain")
    for p in data["players"]:
        st.markdown(f"**{p['name']}** — {p['pos']} | Rating {p['rating']} | £{p['price']}M")

# ==== TAB 2: MATCH ====
with tabs[1]:
    st.header("Simulasi Pertandingan")
    managed = clubs[st.session_state.managed_club]
    names = [p["name"] for p in managed["players"]]
    selected = st.multiselect("Pilih 11 pemain:", names)

    opponent_name = st.selectbox("Pilih lawan:", [c for c in clubs.keys() if c != st.session_state.managed_club])
    opponent = clubs[opponent_name]

    if st.button("Mulai Pertandingan"):
        if len(selected) != 11:
            st.warning("Pilih tepat 11 pemain dulu!")
        else:
            team_rating = sum(p["rating"] for p in managed["players"] if p["name"] in selected) / 11
            opp_rating = opponent["avg_rating"]

            score_team = int(random.gauss(team_rating / 10, 1))
            score_opp = int(random.gauss(opp_rating / 10, 1))
            score_team = max(0, score_team)
            score_opp = max(0, score_opp)

            st.session_state.last_match = {
                "team": st.session_state.managed_club,
                "opponent": opponent_name,
                "score_team": score_team,
                "score_opponent": score_opp,
                "team_logo": managed["logo"],
                "opponent_logo": opponent["logo"],
            }

            if score_team > score_opp:
                st.session_state.stats["W"] += 1
                st.session_state.money += 20
                st.success(f"Kemenangan {score_team}-{score_opp}!")
            elif score_team == score_opp:
                st.session_state.stats["D"] += 1
                st.info(f"Seri {score_team}-{score_opp}.")
            else:
                st.session_state.stats["L"] += 1
                st.error(f"Kalah {score_team}-{score_opp}.")

    if st.session_state.last_match:
        lm = st.session_state.last_match
        st.markdown(
            f"""
            <div style="display:flex;align-items:center;justify-content:center;gap:16px;margin-top:12px;">
                <div style="text-align:center;">
                    <img src="{lm['team_logo']}" width="80"><br><b>{lm['team']}</b>
                </div>
                <div style="font-size:28px;"><b>{lm['score_team']} - {lm['score_opponent']}</b></div>
                <div style="text-align:center;">
                    <img src="{lm['opponent_logo']}" width="80"><br><b>{lm['opponent']}</b>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ==== TAB 3: TRANSFER ====
with tabs[2]:
    st.header("Bursa Transfer")
    st.write(f"Anggaran: **£{st.session_state.money}M**")

    for p in transfer_market:
        cols = st.columns([3, 1, 1, 1])
        cols[0].write(p["name"])
        cols[1].write(p["pos"])
        cols[2].write(f"Rating {p['rating']}")
        if cols[3].button(f"Beli £{p['price']}M", key=p["name"]):
            if st.session_state.money >= p["price"]:
                clubs[st.session_state.managed_club]["players"].append(p.copy())
                st.session_state.money -= p["price"]
                st.success(f"{p['name']} bergabung ke {st.session_state.managed_club}!")
            else:
                st.error("Dana tidak cukup.")

# ==== TAB 4: STATS ====
with tabs[3]:
    st.header("Statistik Klub")
    st.metric("Dana Klub", f"£{st.session_state.money}M")
    st.write(f"Menang: {st.session_state.stats['W']} | Seri: {st.session_state.stats['D']} | Kalah: {st.session_state.stats['L']}")
    if st.session_state.last_match:
        lm = st.session_state.last_match
        st.write(f"Pertandingan terakhir: {lm['team']} {lm['score_team']} - {lm['score_opponent']} {lm['opponent']}")
    else:
        st.write("_Belum ada pertandingan_")

st.markdown("---")
st.caption("iseng @khaissaint")