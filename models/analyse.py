import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

# Charger les données
data = pd.read_csv('../data/merged_69.csv', sep=';')

# Titre de l'application
st.title("Analyse des Performances Energétiques des Logements")

# KPI 1: Consommation énergétique moyenne par m² (Gauge Chart)
st.header("Consommation énergétique moyenne par m²")
mean_energy = data['Conso_5_usages_par_m²_é_primaire'].mean()

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=mean_energy,
    title={'text': "Consommation moyenne (kWh/m²)"},
    gauge={'axis': {'range': [0, max(data['Conso_5_usages_par_m²_é_primaire'])]},
           'bar': {'color': "blue"}}
))
st.plotly_chart(fig)

# KPI 2: Émissions GES moyennes par m² (Line Chart)
st.header("Émissions de GES moyennes par m²")
if 'Date' in data.columns:  # Vérifie si des données temporelles sont présentes
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
    data = data.dropna(subset=['Date'])
    ges_time = data.groupby(data['Date'].dt.year)['Emission_GES_5_usages_énergie_n°2'].mean()

    fig, ax = plt.subplots()
    ax.plot(ges_time.index, ges_time.values, color='green', marker='o')
    ax.set_title("Évolution des émissions GES moyennes par an")
    ax.set_xlabel("Année")
    ax.set_ylabel("Émissions GES (kgCO2/m²)")
    st.pyplot(fig)
else:
    mean_ges = data['Emission_GES_5_usages_énergie_n°2'].mean()
    st.metric("Émissions moyennes (kgCO2/m²)", f"{mean_ges:.2f}")

# KPI 3: Répartition des classes énergétiques (DPE) (Pie Chart)
st.header("Répartition des classes énergétiques (DPE)")
dpe_counts = data['Classe_DPE'].value_counts()
fig, ax = plt.subplots()
ax.pie(dpe_counts, labels=dpe_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
ax.axis('equal')
st.pyplot(fig)

# KPI 4: Coût énergétique moyen par type (Group Bar Chart)
st.header("Coût énergétique moyen par type")
costs = {
    "Chauffage": data['Coût_chauffage_dépensier'].mean(),
    "Refroidissement": data['Coût_refroidissement_dépensier'].mean(),
    "Auxiliaires": data['Coût_auxiliaires'].mean()
}
cost_df = pd.DataFrame.from_dict(costs, orient='index', columns=['Coût moyen (€)'])
st.bar_chart(cost_df)

# KPI 5: Distribution de la qualité de l'isolation (Histogram)
st.header("Qualité de l'isolation des menuiseries")
insulation_counts = data['Qualité_isolation_menuiseries'].value_counts()
fig, ax = plt.subplots()
sns.barplot(x=insulation_counts.index, y=insulation_counts.values, ax=ax, palette="coolwarm")
ax.set_xlabel("Qualité de l'isolation")
ax.set_ylabel("Nombre de logements")
st.pyplot(fig)

st.write("Les KPI ci-dessus fournissent une vue d'ensemble de la performance énergétique des logements.")
