import streamlit as st
import random
import os
import base64
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="Mini Football Manager v2", layout="wide")

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


def update_avg_rating(club_name):
    players = clubs[club_name]["players"]
    if not players:
        clubs[club_name]["avg_rating"] = 0
    else:
        clubs[club_name]["avg_rating"] = sum(p["rating"] for p in players) / len(players)


def ensure_player_stats_for(club, player_name):
    if player_name not in st.session_state.player_stats.get(club, {}):
        st.session_state.player_stats.setdefault(club, {})
        st.session_state.player_stats[club][player_name] = {"goals": 0, "assists": 0, "matches": 0}


# ---------- Data ----------
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

# Pre-calc avg ratings
for club_name in clubs:
    update_avg_rating(club_name)

# ---------- Session State Init ----------
if "managed_club" not in st.session_state:
    st.session_state.managed_club = None
if "points" not in st.session_state:
    st.session_state.points = {c: 0 for c in clubs}
if "money" not in st.session_state:
    st.session_state.money = {c: 200 for c in clubs}  # starting budget (in millions)
if "player_stats" not in st.session_state:
    st.session_state.player_stats = {c: {p["name"]: {"goals": 0, "assists": 0, "matches": 0} for p in clubs[c]["players"]} for c in clubs}
if "formation" not in st.session_state:
    st.session_state.formation = {c: "4-3-3" for c in clubs}
if "lineup" not in st.session_state:
    st.session_state.lineup = {c: {} for c in clubs}  # mapping pos -> player
if "matches" not in st.session_state:
    st.session_state.matches = []  # history of matches

# ---------- UI: Sidebar ----------
st.sidebar.title("Mini Football Manager v2")
if st.session_state.managed_club is None:
    club_choice = st.sidebar.selectbox("Pilih klub yang ingin kamu kelola:", list(clubs.keys()))
    if st.sidebar.button("Mulai Kelola Klub"):
        st.session_state.managed_club = club_choice
        # experimentally rerun once to show managed state
        st.experimental_rerun()
else:
    st.sidebar.success(f"Kamu sekarang mengelola {st.session_state.managed_club}")
    if st.sidebar.button("Ganti Klub"):
        st.session_state.managed_club = None
        st.experimental_rerun()

st.sidebar.divider()
st.sidebar.markdown("**Budget klub saat ini:**")
if st.session_state.managed_club:
    st.sidebar.write(f"£{st.session_state.money[st.session_state.managed_club]}M")

# ---------- Tabs ----------
tabs = st.tabs(["Club", "Match", "Transfer", "Stats", "Tactics", "Dashboard"])

# ---------- Tab: Club ----------
with tabs[0]:
    club = st.session_state.managed_club
    if club:
        logo_data = get_base64_image(os.path.join(LOGO_DIR, clubs[club]["logo"]))
        if logo_data:
            st.markdown(f"<img src='{logo_data}' width='150'>", unsafe_allow_html=True)
        st.markdown(f"## {club}")
        st.write(f"Average Rating: {clubs[club]['avg_rating']:.1f}")

        st.subheader("Daftar Pemain")
        for p in clubs[club]["players"]:
            stats = st.session_state.player_stats[club].get(p["name"], {"goals":0, "assists":0, "matches":0})
            st.write(f"{p['name']} ({p['pos']}) — Rating {p['rating']} — £{p['price']}M — G:{stats['goals']} A:{stats['assists']} M:{stats['matches']}")
    else:
        st.info("Pilih klub dulu di sidebar.")

# ---------- Tab: Match ----------
with tabs[1]:
    club = st.session_state.managed_club
    if club:
        st.subheader("Simulasi Pertandingan")
        opponent = st.selectbox("Pilih lawan:", [c for c in clubs.keys() if c != club])
        form = st.selectbox("Pilih formasi untuk pertandingan:", ["4-3-3", "4-2-3-1", "3-5-2", "4-4-2"], index=["4-3-3","4-2-3-1","3-5-2","4-4-2"].index(st.session_state.formation.get(club, "4-3-3")))
        st.session_state.formation[club] = form

        st.write("**Pilih lineup (opsional):**")
        # Rough position templates per formation
        formation_positions = {
            "4-3-3": ["GK", "RB", "CB1", "CB2", "LB", "CM1", "CM2", "CM3", "RW", "ST", "LW"],
            "4-2-3-1": ["GK", "RB", "CB1", "CB2", "LB", "CDM1", "CDM2", "RM", "CAM", "LM", "ST"],
            "3-5-2": ["GK", "CB1", "CB2", "CB3", "RM", "CM1", "CM2", "CM3", "LM", "ST1", "ST2"],
            "4-4-2": ["GK", "RB", "CB1", "CB2", "LB", "RM", "CM1", "CM2", "LM", "ST1", "ST2"],
        }
        pos_list = formation_positions.get(form, formation_positions["4-3-3"])
        lineup = {}
        for pos in pos_list:
            choices = [p["name"] for p in clubs[club]["players"]]
            sel = st.selectbox(f"{pos}", choices, key=f"lineup_{club}_{pos}")
            lineup[pos] = sel
        st.session_state.lineup[club] = lineup

        if st.button("Mainkan Pertandingan"):
            team_rating = clubs[club]["avg_rating"]
            opponent_rating = clubs[opponent]["avg_rating"]
            # base random scores influenced by rating difference
            score_team = random.randint(0, 3)
            score_opp = random.randint(0, 3)

            # small bonus based on rating
            if team_rating > opponent_rating:
                score_team += random.choice([0, 0, 1])
            elif opponent_rating > team_rating:
                score_opp += random.choice([0, 0, 1])

            # determine scorers and assist makers
            def pick_scorers(sc, club_name):
                scorers = []
                if sc <= 0:
                    return scorers
                available = [p["name"] for p in clubs[club_name]["players"]]
                # prefer forwards & wingers
                forwards = [p["name"] for p in clubs[club_name]["players"] if p["pos"] in ("ST", "LW", "RW", "CAM")]
                for _ in range(sc):
                    if forwards and random.random() < 0.7:
                        s = random.choice(forwards)
                    else:
                        s = random.choice(available)
                    scorers.append(s)
                return scorers

            team_scorers = pick_scorers(score_team, club)
            opp_scorers = pick_scorers(score_opp, opponent)

            # update session points
            if score_team > score_opp:
                st.session_state.points[club] += 3
                match_result = f"{club} MENANG!"
            elif score_team == score_opp:
                st.session_state.points[club] += 1
                st.session_state.points[opponent] += 1
                match_result = "Seri!"
            else:
                st.session_state.points[opponent] += 3
                match_result = f"{opponent} menang kali ini."

            # update player stats & matches played
            for s in team_scorers:
                ensure_player_stats_for(club, s)
                st.session_state.player_stats[club][s]["goals"] += 1
            for s in opp_scorers:
                ensure_player_stats_for(opponent, s)
                st.session_state.player_stats[opponent][s]["goals"] += 1

            # random assists assignment (if there is at least 1 goal)
            def assign_assists(scorers, club_name):
                for s in scorers:
                    if random.random() < 0.6:  # 60% chance a goal had an assist
                        potential = [p["name"] for p in clubs[club_name]["players"] if p["name"] != s]
                        if potential:
                            a = random.choice(potential)
                            ensure_player_stats_for(club_name, a)
                            st.session_state.player_stats[club_name][a]["assists"] += 1

            assign_assists(team_scorers, club)
            assign_assists(opp_scorers, opponent)

            # increment matches played for all players in lineup
            for p in clubs[club]["players"]:
                ensure_player_stats_for(club, p["name"])
                st.session_state.player_stats[club][p["name"]]["matches"] += 1
            for p in clubs[opponent]["players"]:
                ensure_player_stats_for(opponent, p["name"])
                st.session_state.player_stats[opponent][p["name"]]["matches"] += 1

            # record match
            st.session_state.matches.append({
                "date": datetime.utcnow().isoformat(),
                "home": club,
                "away": opponent,
                "score_home": score_team,
                "score_away": score_opp,
                "scorers_home": team_scorers,
                "scorers_away": opp_scorers,
                "formation_home": form,
            })

            st.markdown(f"### {club} {score_team} - {score_opp} {opponent}")
            if score_team > score_opp:
                st.success(match_result)
            elif score_team == score_opp:
                st.info(match_result)
            else:
                st.error(match_result)

    else:
        st.info("Pilih klub dulu di sidebar.")

# ---------- Tab: Transfer ----------
with tabs[2]:
    club = st.session_state.managed_club
    if club:
        st.subheader("Transfer Market")
        all_players = []
        for cname, cdata in clubs.items():
            if cname != club:
                for p in cdata["players"]:
                    all_players.append((cname, p))
        player_options = [f"{p['name']} ({c}) — £{p['price']}M" for c, p in all_players]
        if player_options:
            player_choice = st.selectbox("Pilih pemain untuk dibeli:", player_options)
            if st.button("Beli Pemain"):

                chosen = player_choice.split(" — ")[0]
                pname = chosen.split("(")[0].strip()
                from_club = chosen.split("(")[1][:-1]
                target = next(p for p in clubs[from_club]["players"] if p["name"] == pname)
                price = target["price"]
                if st.session_state.money[club] >= price:
                   
                    st.session_state.money[club] -= price
                    st.session_state.money[from_club] += price
                   
                    clubs[club]["players"].append(target)
                    clubs[from_club]["players"].remove(target)
                   
                    ensure_player_stats_for(club, pname)
                    if pname in st.session_state.player_stats.get(from_club, {}):
                       
                        st.session_state.player_stats[club][pname] = st.session_state.player_stats[from_club].pop(pname)
                    st.success(f"{pname} berhasil dibeli dari {from_club} seharga £{price}M!")
                    update_avg_rating(club)
                    update_avg_rating(from_club)
                else:
                    st.error("Uang klubmu tidak cukup untuk membeli pemain ini!")
        else:
            st.info("Tidak ada pemain yang tersedia di pasar.")
    else:
        st.info("Pilih klub dulu di sidebar.")

# ---------- Tab: Stats ----------
with tabs[3]:
    st.subheader("Klasemen Sementara")
    sorted_points = sorted(st.session_state.points.items(), key=lambda x: x[1], reverse=True)
    for i, (team, pts) in enumerate(sorted_points, start=1):
        st.markdown(f"**{i}. {team}** — {pts} pts")

    st.divider()
    st.subheader("Top Scorer & Assist")
    all_stats = []
    for club_name, pdata in st.session_state.player_stats.items():
        for name, stat in pdata.items():
            all_stats.append({"club": club_name, "name": name, "goals": stat["goals"], "assists": stat["assists"], "matches": stat["matches"]})

    top_scorers = sorted(all_stats, key=lambda x: x["goals"], reverse=True)[:10]
    st.write("**Top Scorers**")
    for i, s in enumerate(top_scorers, start=1):
        st.write(f"{i}. {s['name']} ({s['club']}) — {s['goals']} gol, {s['assists']} assist, {s['matches']} match")

    st.divider()
    st.write("**Top Assists**")
    top_assists = sorted(all_stats, key=lambda x: x["assists"], reverse=True)[:10]
    for i, s in enumerate(top_assists, start=1):
        st.write(f"{i}. {s['name']} ({s['club']}) — {s['assists']} assist, {s['goals']} gol")

    st.divider()
    st.subheader("Riwayat Pertandingan (5 terbaru)")
    for m in st.session_state.matches[-5:][::-1]:
        st.write(f"{m['date']} — {m['home']} {m['score_home']}-{m['score_away']} {m['away']}")

# ---------- Tab: Tactics ----------
with tabs[4]:
    club = st.session_state.managed_club
    if club:
        st.subheader("Taktik & Formasi Tim")
        form = st.selectbox("Pilih Formasi:", ["4-3-3", "4-2-3-1", "3-5-2", "4-4-2"], index=["4-3-3","4-2-3-1","3-5-2","4-4-2"].index(st.session_state.formation.get(club, "4-3-3")))
        st.session_state.formation[club] = form
        st.success(f"Formasi {form} diterapkan untuk {club}")

        st.write("**Lineup Saat Ini**")
        lineup = st.session_state.lineup.get(club, {})
        if lineup:
            for pos, player in lineup.items():
                st.write(f"{pos}: {player}")
        else:
            st.info("Belum ada lineup yang disimpan — atur lineup lewat tab 'Match'.")

        st.divider()
        st.write("**Formasi visual (sederhana)**")
        st.markdown("_(Ini hanya representasi teks, untuk visual lebih bagus kita bisa menambahkan gambar/plot)_")
        pos_map = {
            "4-3-3": "GK\nLB CB CB RB\nCM CM CM\nLW ST RW",
            "4-2-3-1": "GK\nLB CB CB RB\nCDM CDM\nLM CAM RM\nST",
            "3-5-2": "GK\nCB CB CB\nLM CM CM RM\nST ST",
            "4-4-2": "GK\nLB CB CB RB\nLM CM CM RM\nST ST",
        }
        st.text(pos_map.get(form, pos_map["4-3-3"]))
    else:
        st.info("Pilih klub dulu di sidebar.")

# ---------- Tab: Dashboard ----------
with tabs[5]:
    st.subheader("Dashboard Klub & Pemain")

    df_points = pd.DataFrame(sorted(st.session_state.points.items(), key=lambda x: x[1], reverse=True), columns=["Club", "Points"]) 
    st.markdown("**Poin Klub Saat Ini**")
    st.bar_chart(df_points.set_index("Club"))

    st.divider()

    df_scorer = pd.DataFrame(all_stats).sort_values("goals", ascending=False).head(10)
    if not df_scorer.empty:
        fig, ax = plt.subplots()
        ax.barh(df_scorer["name"], df_scorer["goals"])
        ax.invert_yaxis()
        ax.set_xlabel("Goals")
        ax.set_title("Top 10 Scorers")
        st.pyplot(fig)

    st.divider()
    st.subheader("Distribusi Rating Pemain")
    rating_rows = []
    for c, cdata in clubs.items():
        for p in cdata["players"]:
            rating_rows.append({"club": c, "player": p["name"], "rating": p["rating"]})
    df_rating = pd.DataFrame(rating_rows)
    if not df_rating.empty:
        # simple boxplot per club
        fig2, ax2 = plt.subplots()
        df_rating.boxplot(by="club", column=["rating"], ax=ax2)
        ax2.set_title("")
        ax2.set_ylabel("Rating")
        st.pyplot(fig2)

    st.divider()
    st.caption("iseng @khaissaint")
