"""
This module holds functions to help create the visualizations in "visualizations.py".
They mainly plot the given data on the provided axes with some preset styles.

Functions:
    make_energy_axes
    make_genres_axes
    makes_subgenres_axes
"""


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
    