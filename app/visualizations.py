import pandas as pd
from matplotlib import pyplot as plt


plt.style.use("dark_background")

# CREATE PLOTS ##################################
def energy_vs_loudness_tempo(db):
    db.execute("SELECT * FROM track_features")
    df = pd.DataFrame(db.result())
    df.columns = ["track_id", "danceability", "energy", "instrumentalness", "liveness", "loudness", "speechiness", "tempo", "type", "valence", "song_uri"]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
    make_energy_axes(ax1, df, "loudness", "loudness (lufs)")
    make_energy_axes(ax2, df, "tempo", "tempo (bpm)")

    plt.tight_layout()
    plt.savefig("app/images/energy-vs-loudness-tempo.png", bbox_inches='tight', pad_inches=.8)

def loudness_vs_danceability(db):
    db.execute("SELECT * FROM track_features")
    df = pd.DataFrame(db.result())
    df.columns = ["track_id", "danceability", "energy", "instrumentalness", "liveness", "loudness", "speechiness", "tempo", "type", "valence", "song_uri"]

    plt.clf()

    plt.scatter(df["danceability"], df["loudness"], c=df["energy"], cmap="Greens")
    cbar = plt.colorbar()
    cbar.set_label("energy", fontname="monospace")
    plt.title("loudness vs danceability", fontname="monospace", backgroundcolor="#1DB954", fontsize=18, y=1.05)
    plt.xlabel("danceability", fontname="monospace")
    plt.ylabel("loudness", fontname="monospace")
    plt.grid(color="#FFFFFF", linestyle="--", alpha=.3)

    plt.tight_layout()
    plt.savefig("app/images/loudness-vs-danceability.png", bbox_inches='tight', pad_inches=.6)

def genre_style_comparison(db):
    # GET DATA
    db.execute("SELECT * FROM V_genre_features")
    df = pd.DataFrame(db.result())
    df.columns = ["genre", "danceability", "energy", "instrumentalness", "liveness", "loudness", "speechiness", "tempo", "valence"]
    df.sort_values("loudness", ascending=True, inplace=True)

    # GROUP DATA
    metal_filter = df["genre"].isin(["djent", "alternative metal", "deathcore"])
    elec_filter = df["genre"].isin(["dubstep", "brostep", "deathstep", "canadian electronic"])

    avg_loudness_metal, avg_loudness_elec = df[metal_filter]["loudness"].mean(), df[elec_filter]["loudness"].mean()
    avg_danceability_metal, avg_danceability_elec = df[metal_filter]["danceability"].mean(), df[elec_filter]["danceability"].mean()
    avg_valence_metal, avg_valence_elec = df[metal_filter]["valence"].mean(), df[elec_filter]["valence"].mean()
    avg_tempo_metal, avg_tempo_elec = df[metal_filter]["tempo"].mean(), df[elec_filter]["tempo"].mean()

    # PLOT DATA
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(10, 6))
    fig.suptitle('genre style comparisons', fontsize=18, fontname="monospace", y=1.01, backgroundcolor="#FFFFFF", color="#191414")
    fig.text(0.5, -0.02, 'genre', ha='center', fontsize=14, fontname="monospace")
    make_genres_axes(ax1, avg_danceability_elec, avg_danceability_metal, "danceability", "avg danceability score")
    make_genres_axes(ax2, avg_loudness_elec, avg_loudness_metal, "loudness", "avg loudness (lufs)")
    make_genres_axes(ax3, avg_valence_elec, avg_valence_metal, "valence", "avg valence score")
    make_genres_axes(ax4, avg_tempo_elec, avg_tempo_metal, "tempo", "avg tempo (bpm)")

    plt.tight_layout()
    plt.savefig("app/images/genre-style-comparison.png", bbox_inches='tight', pad_inches=.8)

def subgenre_style_comparison(db):
    # GET DATA
    db.execute("SELECT * FROM V_genre_features")
    df = pd.DataFrame(db.result())
    df.columns = ["genre", "danceability", "energy", "instrumentalness", "liveness", "loudness", "speechiness", "tempo", "valence"]
    df.sort_values("loudness", ascending=True, inplace=True)

    # GROUP DATA
    metal_filter = df["genre"].isin(["djent", "alternative metal", "deathcore"])
    elec_filter = df["genre"].isin(["dubstep", "brostep", "deathstep", "canadian electronic"])

    # PLOT DATA
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 6))
    fig.suptitle('sub-genre style comparisons', fontsize=18, fontname="monospace", y=1.02, backgroundcolor="#FFFFFF", color="#191414")
    makes_subgenres_axes(ax1, df, metal_filter, elec_filter, "danceability", "danceability score")
    makes_subgenres_axes(ax2, df, metal_filter, elec_filter, "loudness", "avg loudness (lufs)")
    makes_subgenres_axes(ax3, df, metal_filter, elec_filter, "tempo", "tempo (bpm)")
    makes_subgenres_axes(ax4, df, metal_filter, elec_filter, "valence", "valence score")

    plt.figlegend(["metal", "heavy electronic"], loc='lower center', bbox_to_anchor=(0.5, -0.1))
    plt.tight_layout()
    plt.savefig("app/images/sub-genre-style-comparison.png", bbox_inches='tight', pad_inches=.6)
    

# HELPERS #######################################
def make_energy_axes(ax, df, metric, ylabel):
    ax.scatter(df["energy"], df[metric], c="#FFFFFF" if metric == "tempo" else "#1DB954")
    ax.set_title(f"energy level vs. {metric}", fontname="monospace", fontsize=18, backgroundcolor="#FFFFFF", color="black")
    ax.set_ylabel(ylabel, fontname="monospace")
    ax.grid(color="#FFFFFF", linestyle='--', alpha=.3)

def make_genres_axes(ax, data1, data2, title, ylabel):
    ax.bar("heavy electronic", data1, color="#1DB954")
    ax.bar("metal", data2, color="#FFFFFF", alpha=.9)
    ax.set_title(title, fontname="monospace", backgroundcolor="#191414", color="#FFFFFF")
    ax.set_ylabel(ylabel, fontname="monospace")
    ax.grid(color="#FFFFFF", linestyle="--", alpha=.3)

def makes_subgenres_axes(ax, df, filt1, filt2, metric, xlabel):
    ax.barh(df["genre"][filt1], df[metric][filt1], color="#FFFFFF", label="metal", alpha=.9)
    ax.barh(df["genre"][filt2], df[metric][filt2], color="#1DB954", label="heavy electronic")
    ax.set_title(metric, fontname="monospace", backgroundcolor="#191414", color="#FFFFFF")
    ax.set_xlabel(xlabel, fontname="monospace")
    ax.grid(color="#FFFFFF", linestyle="--", alpha=.3)
    