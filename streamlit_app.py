import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Bibliothèque de matériaux avec leur conductivité thermique (en W/m.K)
materiaux = {
    "Acier": 50.0,
    "Aluminium": 235.0,
    "Cuivre": 398.0,
    "Béton": 1.4,
    "Polystyrène expansé (EPS)": 0.03,
    "Verre": 1.0,
    "Bois": 0.12,
    "Argile": 1.5
}


# Streamlit sliders for hyperparameters
st.sidebar.header("Conduction thermique dans une paroi")


# Paramètres de l'utilisateur
temperature_surface1 = st.sidebar.slider("Température de la surface 1 (T1)", min_value=0, max_value=100, value=20)
temperature_surface2 = st.sidebar.slider("Température de la surface 2 (T2)", min_value=0, max_value=100, value=80)
n_couches = st.sidebar.slider("Nombre de couches dans la paroi", min_value=1, max_value=5, value=2)


# Listes pour stocker les matériaux et épaisseurs des différentes couches
materiaux_couches = []
epaisseurs_couches = []

# Demander à l'utilisateur de choisir les matériaux et les épaisseurs pour chaque couche
for i in range(n_couches):
    st.sidebar.subheader(f"Couche {i + 1}")
    
    # Choisir le matériau pour chaque couche
    materiau = st.sidebar.selectbox(f"Choisir un matériau pour la couche {i + 1}", list(materiaux.keys()), key=f"materiau_{i}")
    materiaux_couches.append(materiau)
    
    # Choisir l'épaisseur de chaque couche
    epaisseur = st.sidebar.slider(f"Épaisseur de la couche {i + 1} (m)", min_value=0.1, max_value=5.0, value=1.0, step=0.1, key=f"epaisseur_{i}")
    epaisseurs_couches.append(epaisseur)



# Calcul de la température à travers la paroi
# On va parcourir chaque couche et calculer la température à chaque position en fonction des matériaux et de leur épaisseur
longueur_totale = sum(epaisseurs_couches)
x = np.linspace(0, longueur_totale, 1000)
temperature = np.zeros_like(x)
resistance_totale = sum(epaisseurs_couches[i]/materiaux[materiaux_couches[i]] for i in range(n_couches))
flux_chaleur = (temperature_surface2 - temperature_surface1) / resistance_totale

# On calcule la température à chaque position x en fonction des couches
x = [0]
temperature = [temperature_surface1]
for i in range(n_couches):
    # Récupérer la conductivité thermique du matériau de la couche
    resistance = epaisseurs_couches[i]/materiaux[materiaux_couches[i]]
    temperature.append(flux_chaleur * resistance + temperature[-1])
    x.append(x[-1] + epaisseurs_couches[i])
    

# Affichage du graphique
fig, ax = plt.subplots()
ax.plot(x, temperature, label="Température dans la paroi")

# Ajouter des lignes pour chaque changement de matériau
position_initiale = 0
for i in range(n_couches):
    ax.axvline(x=position_initiale, color='black', linestyle='--', label=f"Changement de matériau {i + 1}")
    position_initiale += epaisseurs_couches[i]

# Détails du graphique
ax.set_xlabel("Position dans la paroi (m)")
ax.set_ylabel("Température (°C)")
ax.set_title("Évolution de la température dans la paroi")
ax.legend()

# Affichage dans Streamlit
st.pyplot(fig)

st.warning(f"Flux surfacique dans le mur: {flux_chaleur} W/m²")
st.warning(f"Résistance équivalente: {resistance_totale} m².K/W")
