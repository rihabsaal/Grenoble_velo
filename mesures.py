import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt




# --- Charger les données ---
df_accidents = pd.read_csv("AccidentsVelo_modifie.csv")
df_accidents["Amenagement_Infrastructure"] = df_accidents["Amenagement_Infrastructure"].replace("Aucun", "Aucune infrastructure")

# Données de déplacements à vélo
df_grenoble = pd.read_csv("evolution_pratique_velo_grenoble.csv", sep=";")
df_strasbourg = pd.read_csv("evolution_pratique_velo_strasbourg.csv", sep=";")

# Vérifier les colonnes disponibles
print("Colonnes Grenoble:", df_grenoble.columns)
print("Colonnes Strasbourg:", df_strasbourg.columns)

# --- Calculer la moyenne des déplacements ---
moyenne_grenoble = df_grenoble["Nombre de deplacements en velo"].mean()
moyenne_strasbourg = df_strasbourg["Estimation annuelle (365 jours)"].mean()

# --- Calcul du taux d'accidentologie ---
nb_accidents_grenoble = len(df_accidents[df_accidents["Metropole"] == "Grenoble"])
nb_accidents_strasbourg = len(df_accidents[df_accidents["Metropole"] == "Strasbourg"])

taux_accidentologie_grenoble = (nb_accidents_grenoble / moyenne_grenoble)* 100
taux_accidentologie_strasbourg = (nb_accidents_strasbourg / moyenne_strasbourg)* 100


# Filtrer uniquement pour Grenoble et Strasbourg
villes_ciblees = ["Grenoble", "Strasbourg"]

# Calculer le pourcentage des types d'infrastructure pour chaque ville
infra_pourcentage_grenoble = (
    df_accidents[df_accidents["Metropole"] == "Grenoble"]
    .groupby("Amenagement_Infrastructure")
    .size()
    .div(len(df_accidents[df_accidents["Metropole"] == "Grenoble"])) * 100
)

infra_pourcentage_strasbourg = (
    df_accidents[df_accidents["Metropole"] == "Strasbourg"]
    .groupby("Amenagement_Infrastructure")
    .size()
    .div(len(df_accidents[df_accidents["Metropole"] == "Strasbourg"])) * 100
)

# Calculer le pourcentage des situations d'accidents pour chaque ville
situation_pourcentage_grenoble = (
    df_accidents[df_accidents["Metropole"] == "Grenoble"]
    .groupby("Situation_Accident")
    .size()
    .div(len(df_accidents[df_accidents["Metropole"] == "Grenoble"])) * 100
)

situation_pourcentage_strasbourg = (
    df_accidents[df_accidents["Metropole"] == "Strasbourg"]
    .groupby("Situation_Accident")
    .size()
    .div(len(df_accidents[df_accidents["Metropole"] == "Strasbourg"])) * 100
)

# Affichage des résultats
print("📊 Pourcentage des types d'infrastructure à Grenoble :")
print(infra_pourcentage_grenoble)

print("\n📊 Pourcentage des types d'infrastructure à Strasbourg :")
print(infra_pourcentage_strasbourg)

print("\n📊 Pourcentage des situations d'accidents à Grenoble :")
print(situation_pourcentage_grenoble)

print("\n📊 Pourcentage des situations d'accidents à Strasbourg :")
print(situation_pourcentage_strasbourg)


# Regrouper par plusieurs facteurs et compter le nombre d'occurrences
combinaisons_accidents = df_accidents.groupby([
    "Situation_Accident", 
    "Amenagement_Infrastructure", 
    "Intersection", 
    "Categorie_Route", 
    "Régime_Circulation"
]).size().reset_index(name="Nombre_Accidents")

# Trier par le nombre d'accidents décroissant pour voir les combinaisons les plus fréquentes
combinaisons_accidents = combinaisons_accidents.sort_values(by="Nombre_Accidents", ascending=False)

# Afficher les 10 combinaisons les plus fréquentes
#print(combinaisons_accidents.head(10))

# Prendre les 5 combinaisons les plus fréquentes
top_combinations = combinaisons_accidents.head(5)



print(nb_accidents_grenoble)




# --- Calcul de l'évolution temporelle ---

moyennes_circulation = {
    "Grenoble": moyenne_grenoble,
    "Strasbourg": moyenne_strasbourg
}


# Pour l'infrastructure : on garde uniquement les accidents sur "Aucun" pour Grenoble et Strasbourg
df_infra_evolution = df_accidents[
    (df_accidents["Metropole"].isin(["Grenoble", "Strasbourg"])) &
    (df_accidents["Amenagement_Infrastructure"].isin(["Aucune infrastructure"]))
]
df_infra_evolution_grouped = (
    df_infra_evolution
    .groupby(["Annee_Accident", "Metropole", "Amenagement_Infrastructure"])
    .size()
    .reset_index(name="Nombre_Accidents")
)

# Ajouter le taux d'accidents relatif à la circulation
df_infra_evolution_grouped["Taux_Accidents"] = df_infra_evolution_grouped.apply(
    lambda row: row["Nombre_Accidents"] / moyennes_circulation[row["Metropole"]],
    axis=1
)


# Pour la situation : on garde uniquement les accidents sur "Sur chaussée" et "Piste cyclable" pour Grenoble et Strasbourg
df_situation_evolution = df_accidents[
    (df_accidents["Metropole"].isin(["Grenoble", "Strasbourg"])) &
    (df_accidents["Situation_Accident"].isin(["Sur chaussée", "Sur piste cyclable"]))
]
df_situation_evolution_grouped = (
    df_situation_evolution
    .groupby(["Annee_Accident", "Metropole", "Situation_Accident"])
    .size()
    .reset_index(name="Nombre_Accidents")
)

# Ajouter le taux d'accidents relatif à la circulation
df_situation_evolution_grouped["Taux_Accidents"] = df_situation_evolution_grouped.apply(
    lambda row: row["Nombre_Accidents"] / moyennes_circulation[row["Metropole"]],
    axis=1
)


# 1. Importer les CSV
df_amenagement_grenoble = pd.read_csv("pistes_grenoble.csv")
df_amenagement_strasbourg = pd.read_csv("pistes_strasbourg.csv")

# 2. Convertir la date de mise à jour en datetime et extraire l'année
# Supposons que la colonne s'appelle "date_mise_a_jour"
df_amenagement_grenoble["annee_maj"] = pd.to_datetime(df_amenagement_grenoble["annee_maj"])
df_amenagement_strasbourg["date_mise_a_jour"] = pd.to_datetime(df_amenagement_strasbourg["date_mise_a_jour"])

df_amenagement_grenoble["Annee"] = df_amenagement_grenoble["annee_maj"].dt.year
df_amenagement_strasbourg["Annee"] = df_amenagement_strasbourg["date_mise_a_jour"].dt.year

# 3. Identifier un point géo2d unique

# 4. Calculer le nombre de projets uniques par année (en tenant compte des mises à jour multiples)
# On considère qu'un projet correspond à un point géo2d unique.
kpi_grenoble = df_amenagement_grenoble.groupby("Annee")["coord"].nunique()
kpi_strasbourg = df_amenagement_strasbourg.groupby("Annee")["coordonnees"].nunique()

# 5. Trouver l'année avec le maximum de projets pour chaque ville
max_year_grenoble = kpi_grenoble.idxmax()
max_count_grenoble = kpi_grenoble.max()

max_year_strasbourg = kpi_strasbourg.idxmax()
max_count_strasbourg = kpi_strasbourg.max()

# Construire un KPI pertinent pour chaque ville
kpi_results = {
    "Grenoble": {
         "annee_max_projets": max_year_grenoble,
         "nombre_projets_max": max_count_grenoble,
         "projets_par_annee": kpi_grenoble.to_dict()  # Pour avoir le détail par année
    },
    "Strasbourg": {
         "annee_max_projets": max_year_strasbourg,
         "nombre_projets_max": max_count_strasbourg,
         "projets_par_annee": kpi_strasbourg.to_dict()
    }
}

# Pour Grenoble
df_projets_grenoble = pd.DataFrame(
    list(kpi_results["Grenoble"]["projets_par_annee"].items()),
    columns=["Annee", "Nombre_Projets"]
)
df_projets_grenoble = df_projets_grenoble.sort_values(by="Nombre_Projets", ascending=False)

# Pour Strasbourg
df_projets_strasbourg = pd.DataFrame(
    list(kpi_results["Strasbourg"]["projets_par_annee"].items()),
    columns=["Annee", "Nombre_Projets"]
)
df_projets_strasbourg = df_projets_strasbourg.sort_values(by="Nombre_Projets", ascending=False)

print("KPIs des projets d'aménagement :")
print(kpi_results)



# Calcul de l'évolution annuelle du nombre d'accidents pour Grenoble
df_accidents_yearly_grenoble = (
    df_accidents[df_accidents["Metropole"] == "Grenoble"]
    .groupby("Annee_Accident")
    .size()
    .reset_index(name="Nombre_Accidents")
)
# Calcul de l'évolution annuelle du nombre d'accidents pour Grenoble
df_accidents_yearly_strasbourg = (
    df_accidents[df_accidents["Metropole"] == "Strasbourg"]
    .groupby("Annee_Accident")
    .size()
    .reset_index(name="Nombre_Accidents")
)


population_grenoble = 450000
population_strasbourg = 520000

superficie_grenoble = 546
superficie_strasbourg = 337.6








# Définir la plage d'années souhaitée
years = list(range(2012, 2027))  # de 2012 à 2026

# Pour Strasbourg :
# - 2016 : 7M (issue de la tranche 2012-2016)
# - 2017-2020 : 12M (tranche 2017-2020)
# - 2021-2026 : 16.7M (tranche 2021-2026)
budget_strasbourg = []
for year in years:
    if 2012 <= year <= 2016:
        budget_strasbourg.append(7)
    elif 2017 <= year <= 2020:
        budget_strasbourg.append(12)
    elif 2021 <= year <= 2026:
        budget_strasbourg.append(16.7)

# Pour Grenoble :
# - 2016 : 6M
# - 2017-2023 : 6M
# - 2024 et les années suivantes : 8.4M (augmentation à partir de 2024, puis reporté)
budget_grenoble = []
for year in years:
    if 2012 <= year < 2016:
        budget_grenoble.append(0)
    elif 2016 <= year <= 2023:
        budget_grenoble.append(6)
    elif year >= 2024:
        budget_grenoble.append(8.4)

# Création du DataFrame
df_budget_yearly = pd.DataFrame({
    "Année": years,
    "Grenoble": budget_grenoble,
    "Strasbourg": budget_strasbourg
})

# Affichage du DataFrame
print(df_budget_yearly)






# --- Retourner les résultats ---
def get_mesures():
    return {
        "moyenne_grenoble": moyenne_grenoble,
        "moyenne_strasbourg": moyenne_strasbourg,
        "taux_accidentologie_grenoble": taux_accidentologie_grenoble,
        "taux_accidentologie_strasbourg": taux_accidentologie_strasbourg,
        "nb_accidents_grenoble": nb_accidents_grenoble,
        "nb_accidents_strasbourg": nb_accidents_strasbourg,
        "combinaisons_accidents": combinaisons_accidents,
        "infra_pourcentage_strasbourg": infra_pourcentage_strasbourg,
        "infra_pourcentage_grenoble": infra_pourcentage_grenoble,
        "situation_pourcentage_strasbourg": situation_pourcentage_strasbourg,
        "situation_pourcentage_grenoble": situation_pourcentage_grenoble,
        "df_infra_evolution": df_infra_evolution_grouped,
        "df_situation_evolution": df_situation_evolution_grouped,
        "df_projets_grenoble": df_projets_grenoble,
        "df_projets_strasbourg" : df_projets_strasbourg,
        "df_accidents_yearly_grenoble" : df_accidents_yearly_grenoble,
        "df_accidents_yearly_strasbourg" : df_accidents_yearly_strasbourg,
        "population_grenoble" : population_grenoble,
        "population_strasbourg" : population_strasbourg,
        "superficie_strasbourg" : superficie_strasbourg,
        "superficie_grenoble": superficie_grenoble,
        "df_budget_yearly" : df_budget_yearly
    }

