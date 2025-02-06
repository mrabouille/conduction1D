import numpy as np
import matplotlib.pyplot as plt

# Titre de l'application
st.title("Conduction thermique dans une paroi")

# Paramètres de l'utilisateur
conductivite = st.slider("Conductivité thermique (k)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
temperature_surface1 = st.slider("Température de la surface 1 (T1)", min_value=0, max_value=100, value=20)
temperature_surface2 = st.slider("Température de la surface 2 (T2)", min_value=0, max_value=100, value=80)
epaisseur_paroi = st.slider("Épaisseur de la paroi (L)", min_value=0.1, max_value=10.0, value=2.0, step=0.1)


# Calcul de la température en fonction de l'épaisseur
# Création d'un tableau de positions x de 0 à L
x = np.linspace(0, epaisseur_paroi, 100)

# Application de la formule de conduction thermique
temperature = temperature_surface1 + ((temperature_surface2 - temperature_surface1) / epaisseur_paroi) * x


# Affichage du graphique
fig, ax = plt.subplots()
ax.plot(x, temperature, label="Température dans la paroi")
ax.set_xlabel("Position dans la paroi (m)")
ax.set_ylabel("Température (°C)")
ax.set_title("Évolution de la température dans la paroi")
ax.legend()

# Affichage dans Streamlit
st.pyplot(fig)
