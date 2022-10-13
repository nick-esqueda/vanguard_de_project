from matplotlib import pyplot as plt
from .utils import DB, make_energy_axes, make_genres_axes, make_subgenres_axes


plt.style.use("dark_background")

# CREATE PLOTS ##################################
def energy_vs_loudness_tempo(db: DB):
    df = db.query("SELECT * FROM track_features")

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
    make_energy_axes(ax1, df, "loudness", "loudness (lufs)")
    make_energy_axes(ax2, df, "tempo", "tempo (bpm)")

    plt.tight_layout()
    plt.savefig("app/images/energy-vs-loudness-tempo.png", bbox_inches='tight', pad_inches=.8)
    print("\tDone creating the Energy vs. Loudness and Tempo plot")

def loudness_vs_danceability(db: DB):
    df = db.query("SELECT * FROM track_features")

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
    print("\tDone creating the Loudness vs. Danceability plot")

def genre_style_comparison(db: DB):
    # GET DATA
    df = db.query("SELECT * FROM V_genre_features")
    
    df.sort_values("loudness", ascending=True, inplace=True) # to visually order the plot by loudness.

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
    print("\tDone creating the Genre Style Comparison plot")

def subgenre_style_comparison(db: DB):
    # GET DATA
    df = db.query("SELECT * FROM V_genre_features")
    
    df.sort_values("loudness", ascending=True, inplace=True) # to visually order the plot by loudness.

    # GROUP DATA
    metal_filter = df["genre"].isin(["djent", "alternative metal", "deathcore"])
    elec_filter = df["genre"].isin(["dubstep", "brostep", "deathstep", "canadian electronic"])

    # PLOT DATA
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 6))
    fig.suptitle('sub-genre style comparisons', fontsize=18, fontname="monospace", y=1.02, backgroundcolor="#FFFFFF", color="#191414")
    make_subgenres_axes(ax1, df, metal_filter, elec_filter, "danceability", "danceability score")
    make_subgenres_axes(ax2, df, metal_filter, elec_filter, "loudness", "avg loudness (lufs)")
    make_subgenres_axes(ax3, df, metal_filter, elec_filter, "tempo", "tempo (bpm)")
    make_subgenres_axes(ax4, df, metal_filter, elec_filter, "valence", "valence score")

    plt.figlegend(["metal", "heavy electronic"], loc='lower center', bbox_to_anchor=(0.5, -0.1))
    plt.tight_layout()
    plt.savefig("app/images/sub-genre-style-comparison.png", bbox_inches='tight', pad_inches=.6)
    print("\tDone creating the Sub-Genre Style Comparison plot")
