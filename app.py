import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# Configuration de la page
st.set_page_config(
    page_title="APEC Auto-Candidature",
    page_icon="🎯",
    layout="wide"
)

# Initialisation de la session
if 'applications' not in st.session_state:
    st.session_state.applications = []
if 'is_running' not in st.session_state:
    st.session_state.is_running = False

# Titre
st.title("🎯 APEC Auto-Candidature")
st.markdown("Automatisez vos candidatures sur APEC")

# Sidebar - Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Identifiants APEC
    st.subheader("Identifiants APEC")
    email = st.text_input("Email APEC", type="default")
    password = st.text_input("Mot de passe APEC", type="password")
    
    st.divider()
    
    # Critères de recherche
    st.subheader("Critères de recherche")
    keywords = st.text_input("Mots-clés", placeholder="Ex: Développeur Python")
    location = st.text_input("Localisation", value="Île-de-France")
    
    contract_type = st.multiselect(
        "Type de contrat",
        ["CDI", "CDD", "Freelance", "Stage"],
        default=["CDI"]
    )
    
    experience = st.selectbox(
        "Expérience",
        ["Débutant", "1-3 ans", "3-5 ans", "5-10 ans", "10+ ans"]
    )
    
    max_applications = st.number_input(
        "Nombre max de candidatures",
        min_value=1,
        max_value=50,
        value=10
    )
    
    st.divider()
    
    # Upload CV
    st.subheader("Documents")
    cv_file = st.file_uploader("CV (PDF)", type=['pdf'])
    cover_letter = st.text_area(
        "Lettre de motivation (template)",
        placeholder="Madame, Monsieur,\n\nJe vous contacte concernant...",
        height=150
    )
    
    st.divider()
    
    # Boutons d'action
    if not st.session_state.is_running:
        if st.button("🚀 Démarrer l'automatisation", type="primary", use_container_width=True):
            if not email or not password:
                st.error("Veuillez entrer vos identifiants APEC")
            elif not keywords:
                st.error("Veuillez entrer des mots-clés")
            elif not cv_file:
                st.error("Veuillez télécharger votre CV")
            else:
                st.session_state.is_running = True
                st.rerun()
    else:
        if st.button("⏸️ Arrêter", type="secondary", use_container_width=True):
            st.session_state.is_running = False
            st.rerun()

# Main area
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total candidatures", len(st.session_state.applications))
with col2:
    success = len([a for a in st.session_state.applications if a['status'] == 'Réussie'])
    st.metric("Réussies", success)
with col3:
    failed = len([a for a in st.session_state.applications if a['status'] == 'Échouée'])
    st.metric("Échouées", failed)

st.divider()

# Zone de process
if st.session_state.is_running:
    st.info("🔄 Automatisation en cours...")
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Simulation du processus
    import time
    for i in range(int(max_applications)):
        status_text.text(f"Traitement de l'offre {i+1}/{max_applications}...")
        progress_bar.progress((i + 1) / max_applications)
        
        # Simulation d'une candidature
        application = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'titre': f"{keywords} - Offre {i+1}",
            'entreprise': f"Entreprise {chr(65 + i % 26)}",
            'localisation': location,
            'status': 'Réussie' if i % 4 != 0 else 'Échouée',
            'lien': f"https://www.apec.fr/offre-{i+1}"
        }
        
        st.session_state.applications.insert(0, application)
        time.sleep(1)
    
    st.session_state.is_running = False
    st.success(f"✅ Automatisation terminée ! {max_applications} offres traitées.")
    st.rerun()

# Historique des candidatures
if st.session_state.applications:
    st.header("📋 Historique des candidatures")
    
    # Convertir en DataFrame
    df = pd.DataFrame(st.session_state.applications)
    
    # Filtres
    col1, col2 = st.columns(2)
    with col1:
        filter_status = st.multiselect(
            "Filtrer par statut",
            options=df['status'].unique(),
            default=df['status'].unique()
        )
    with col2:
        search = st.text_input("Rechercher", placeholder="Titre ou entreprise...")
    
    # Appliquer les filtres
    filtered_df = df[df['status'].isin(filter_status)]
    if search:
        filtered_df = filtered_df[
            filtered_df['titre'].str.contains(search, case=False, na=False) |
            filtered_df['entreprise'].str.contains(search, case=False, na=False)
        ]
    
    # Afficher le tableau
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "lien": st.column_config.LinkColumn("Lien offre"),
            "status": st.column_config.Column(
                "Statut",
                width="small"
            )
        }
    )
    
    # Export
    col1, col2 = st.columns([1, 4])
    with col1:
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Exporter CSV",
            csv,
            "candidatures_apec.csv",
            "text/csv",
            use_container_width=True
        )
    with col2:
        if st.button("🗑️ Effacer l'historique", use_container_width=True):
            st.session_state.applications = []
            st.rerun()
else:
    st.info("👋 Aucune candidature pour le moment. Configurez vos critères et lancez l'automatisation !")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    ⚠️ Utilisez cet outil de manière responsable. Respectez les conditions d'utilisation de l'APEC.
</div>
""", unsafe_allow_html=True)