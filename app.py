import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Configuration de la page
st.set_page_config(page_title="Data Workflow - Projet FOODTOOL", layout="wide")

# --- CHARGEMENT DES DONNÉES ---
@st.cache_data
def load_data():
    try:
        agri = pd.read_csv('agribalyse_simule.csv')
        off = pd.read_csv('openfoodfacts_simule.csv')
        df = pd.merge(off, agri, left_on='ingredients_text', right_on='ingredient_name', how='left')
        df['impact_co2_total'] = df['co2_eq_per_kg'] * 0.1 
        return df
    except Exception as e:
        st.error(f"Erreur de lecture des fichiers : {e}")
        return pd.DataFrame()

df_clean = load_data()

if not df_clean.empty:
    # --- TITRE ENCADRÉ (Style INRAE) ---
    st.markdown("""
        <div style="background-color: #00a388; padding: 40px; border-radius: 10px; text-align: center; margin-bottom: 30px;">
            <h1 style="color: white; margin: 0;">Analyse d'Empreinte Environnementale</h1>
            <p style="color: white; font-size: 1.2em; opacity: 0.9;">Prototype de Workflow Statistique pour l'UMR ITAP - INRAE</p>
        </div>
    """, unsafe_allow_html=True)
    
    # --- LIGNE CORRIGÉE (Elle doit être décalée vers la droite) ---
    st.info("Ce tableau de bord compare l'impact carbone des produits et identifie des archétypes via Machine Learning.")

    # --- BARRE LATÉRALE ---
    st.sidebar.header("🔍 Paramètres d'Analyse")
    categories = ["Toutes"] + list(df_clean['category'].unique())
    selected_cat = st.sidebar.selectbox("Filtrer par catégorie alimentaire", categories)

    df_filtered = df_clean if selected_cat == "Toutes" else df_clean[df_clean['category'] == selected_cat]

    # --- SECTION 1 : BENCHMARKING & CLUSTERING ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Distribution & Benchmarking")
        avg_impact = df_filtered['impact_co2_total'].mean()
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.histplot(df_filtered['impact_co2_total'], kde=True, color="#00a388", ax=ax)
        ax.axvline(avg_impact, color='red', linestyle='--', label=f'Moyenne: {avg_impact:.2f}')
        ax.set_title("Répartition des impacts (données nettoyées)")
        ax.legend()
        st.pyplot(fig)
        # Affichage des deux métriques clés côte à côte
        m1, m2 = st.columns(2)
	# On utilise une unité plus courte ou on élargit l'affichage
        m1.metric(label="Impact Carbone Moyen", value=f"{avg_impact:.3f} kg CO2e")
        
        avg_water = df_filtered['water_footprint_per_kg'].mean() * 0.1 
        # moyenne par portion
        m2.metric(label="Empreinte Eau Moyenne", value=f"{avg_water:.1f} Litres")

    with col2:
        st.subheader("🎯 Clustering (Archétypes)")
        features = df_clean[['co2_eq_per_kg', 'water_footprint_per_kg']].fillna(0)
        scaled = StandardScaler().fit_transform(features)
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        df_clean['cluster'] = kmeans.fit_predict(scaled)
        
        fig2, ax2 = plt.subplots(figsize=(8, 6))
        sns.scatterplot(data=df_clean, x='co2_eq_per_kg', y='water_footprint_per_kg', 
                        hue='cluster', palette='viridis', s=150, ax=ax2)
        ax2.set_title("Identification des profils d'impact")
        st.pyplot(fig2)

    # --- SECTION 2 : PERSPECTIVES DOCTORALES ---
    st.markdown("""
        <div style="background-color: #e8f4f8; padding: 20px; border-radius: 10px; border-left: 5px solid #007bff; margin-top: 20px;">
            <p style="color: #004085; margin: 0; font-weight: bold;">
                Perspectives doctorales : Ce workflow sera étendu par des méthodes d'inférence bayésienne pour l'estimation précise des recettes.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # --- SECTION 3 : DONNÉES BRUTES ---
    st.divider()
    st.subheader("📋 Vue détaillée des données")
    st.dataframe(df_filtered[['product_name', 'category', 'impact_co2_total']], use_container_width=True)