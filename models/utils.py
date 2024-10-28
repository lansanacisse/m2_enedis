import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from io import BytesIO
import streamlit as st


def create_pie_chart(labels, sizes):
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")  # Assure que le graphique est un cercle
    return fig


def create_bar_chart(labels, sizes):
    fig, ax = plt.subplots()
    ax.bar(labels, sizes)
    return fig


def create_line_chart(labels, sizes):
    fig, ax = plt.subplots()
    ax.plot(
        labels, sizes, marker="o"
    )  # Ajout de marqueurs pour une meilleure lisibilité
    return fig


def create_histogram(sizes, labels):
    fig, ax = plt.subplots()
    ax.hist(sizes, bins=len(labels), edgecolor="black")
    return fig


# Créer un graphique en pgn
def save_fig_as_png(fig, filename):
    buf = BytesIO()
    fig.savefig(buf, format="png")
    st.download_button(
        label="Télécharger l'image",
        data=buf,
        file_name=f"{filename}.png",
        mime="image/png",
    )
