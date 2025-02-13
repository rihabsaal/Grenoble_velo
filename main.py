import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from mesures import get_mesures  # Votre module avec les mesures pré-calculées
from PIL import Image
import pandas as pd




# ----------------- Configuration de la page -----------------
st.set_page_config(layout="wide", page_title="Analyse des Accidents", page_icon="🚲")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #F0F2F6;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Injecter du CSS personnalisé pour la sidebar
st.markdown(
    """
    <style>
    /* Couleur de fond de la sidebar */
    .css-1d391kg { 
        background-color: #0D47A1;
        color: white;
    }
    /* Style des éléments de la sidebar */
    .css-1d391kg .css-1aumxhk { 
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Fonction pour afficher une vignette (badge) de titre
def display_vignette(title_text, bg_color="#E1F5FE"):
    st.markdown(
        f"""
        <div style="background-color:{bg_color}; padding:5px; border-radius:5px; margin-bottom:10px;">
            <strong>{title_text}</strong>
        </div>
        """,
        unsafe_allow_html=True
    )

# Charger les mesures
mesures = get_mesures()

# ----------------- Navigation dans la Sidebar -----------------
st.sidebar.title("Navigation")
pages = ["Introduction","Dashboard", "Recommandations"]
page = st.sidebar.radio("Choisissez une page :", pages)

# ----------------- Introduction: Page d'accueil avec images -----------------
if page == "Introduction":

    # Configuration de la page
    def page_1():
        st.title("🚴‍♂ Infrastructures cyclables à Grenoble")
        # Charger les images (remplacez les chemins par vos fichiers)
        image1 = Image.open("velo_acc.jpg")
        st.image(image1, width=600, use_container_width=False)
        st.markdown("</div>", unsafe_allow_html=True)
        # Introduction
        st.markdown(
            """
            Face aux défis environnementaux, le vélo est un levier clé des politiques de mobilité durable. 
            Toutefois, son adoption est freinée par le sentiment d’insécurité, notamment en milieu urbain. 
            Des études montrent que des infrastructures dédiées, comme les pistes cyclables séparées, réduisent significativement les accidents. 
            Malgré des investissements conséquents à Grenoble, la sécurité des cyclistes reste un enjeu majeur.
            """
        )

        # Problématique
        st.subheader("📌 Problématique")
        st.markdown(
            """
            **Quelles sont les solutions à mettre en place pour réduire l’accidentologie cycliste à Grenoble
            en s’appuyant sur les actions efficaces menées dans d’autres villes ?
            """
        )

        # Objectifs
        st.subheader("🎯 Objectifs")
        st.markdown(
            """
            - *Comparer infrastructures et accidentologie* 📊  
            - Analyser le lien entre infrastructure et accident. 
            - Évaluer si un budget élevé pour les infrastructures cyclables réduit effectivement le nombre d’accidents. 

            - *Formuler des recommandations* 📝  
            - Évaluer si l’augmentation du nombre de cyclistes accroît le risque d’accidents  
            - Identifier l’influence du type de voirie sur la sécurité  
            - Déterminer si le budget alloué est suffisant pour garantir la sécurité  
            """
        )

        # Commanditaires et Destinataires
        st.subheader("🏛 Commanditaires et Destinataires")
        st.markdown(
            """
            *Commanditaires* :  
            - La Turbine  
            - Ville de Grenoble  

            *Destinataires* :  
            - *Politiques locaux* (Mairie, Métropole Grenobloise) 🏙  
            """
        )

    # Gestion de la navigation entre pages
    if page == "Introduction":
        page_1()


# ----------------- Dashboard Page -----------------
elif page == "Dashboard":
    # Titre principal du dashboard
    st.markdown("## **🚴‍♂️ Analyse des Infrastructures et de la Sécurité Cycliste : Comparaison Grenoble - Strasbourg**")
    st.markdown("---")

    # --- Section KPI ---
    
    display_vignette("Chiffres Clés", bg_color="#BBDEFB")
    card_style = """
    <style>
        .card {
            background-color: #E3F2FD;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 10px;
            text-align: center;
        }
        .card h4 {
            margin: 0;
            font-size: 16px;
            color: #1565C0;
        }
        .card p {
            margin: 5px 0 0;
            font-size: 18px;
            font-weight: bold;
            color: #0D47A1;
        }
    </style>
    """
    col_kpi_left, col_kpi_right = st.columns(2, gap="medium")
    with col_kpi_left:
        st.markdown("### 📍 Grenoble")
        st.markdown(card_style, unsafe_allow_html=True)
        for label, value in [
            ("Moyenne Annuelle des déplacements", f"{mesures['moyenne_grenoble'] / 1e6:.2f} M"),
            ("Taux d'accidentologie", f"{mesures['taux_accidentologie_grenoble']:.2f} %"),
            ("Population Métropole", f"{mesures['population_grenoble']:,}"),
            ("Superficie Métropole", f"{mesures['superficie_grenoble']} km²")
        ]:
            st.markdown(f'<div class="card"><h4>{label}</h4><p>{value}</p></div>', unsafe_allow_html=True)
    with col_kpi_right:
        st.markdown("### 📍 Strasbourg")
        st.markdown(card_style, unsafe_allow_html=True)
        for label, value in [
            ("Moyenne Annuelle des déplacements", f"{mesures['moyenne_strasbourg'] / 1e6:.2f} M"),
            ("Taux d'accidentologie", f"{mesures['taux_accidentologie_strasbourg']:.2f} %"),
            ("Population Eurométropole", f"{mesures['population_strasbourg']:,}"),
            ("Superficie EuroMétropole", f"{mesures['superficie_strasbourg']} km²")
        ]:
            st.markdown(f'<div class="card"><h4>{label}</h4><p>{value}</p></div>', unsafe_allow_html=True)

    # --- Section Jauges (Indicateurs de sécurité) ---
    st.markdown("---")
    display_vignette("Indicateurs de sécurité", bg_color="#BBDEFB")
    gauge_left, gauge_right = st.columns(2)
    with gauge_left:
        fig_gauge_g = go.Figure(go.Indicator(
            mode="gauge+number",
            value=mesures['taux_accidentologie_grenoble'],
            title={"text": "Taux d'accidentologie - Grenoble"},
            gauge={"axis": {"range": [0, 0.05]}, "bar": {"color": "orange"}}
        ))
        st.plotly_chart(fig_gauge_g, use_container_width=True)
    with gauge_right:
        fig_gauge_s = go.Figure(go.Indicator(
            mode="gauge+number",
            value=mesures['taux_accidentologie_strasbourg'],
            title={"text": "Taux d'accidentologie - Strasbourg"},
            gauge={"axis": {"range": [0, 0.05]}, "bar": {"color": "green"}}
        ))
        st.plotly_chart(fig_gauge_s, use_container_width=True)

    # --- Section Répartition des accidents par type d'infrastructure (Pie Charts) ---
    st.markdown("---")
    display_vignette("Répartition des accidents selon les types d'infrastructure", bg_color="#BBDEFB")
    pie_left, pie_right = st.columns(2)
    with pie_left:
        st.markdown("##### Grenoble")
        st.markdown("<br><br>", unsafe_allow_html=True)
        infra_grenoble_df = mesures['infra_pourcentage_grenoble'].reset_index()
        infra_grenoble_df.columns = ["Amenagement_Infrastructure", "Pourcentage"]
        fig_infra_grenoble = px.pie(
            infra_grenoble_df,
            names="Amenagement_Infrastructure",
            values="Pourcentage",
            color_discrete_sequence=px.colors.sequential.Mint
        )
        fig_infra_grenoble.update_layout(margin=dict(t=50, b=50, l=100, r=100))
        st.plotly_chart(fig_infra_grenoble, use_container_width=True)
    with pie_right:
        st.markdown("##### Strasbourg")
        st.markdown("<br><br>", unsafe_allow_html=True)
        infra_strasbourg_df = mesures['infra_pourcentage_strasbourg'].reset_index()
        infra_strasbourg_df.columns = ["Amenagement_Infrastructure", "Pourcentage"]
        fig_infra_strasbourg = px.pie(
            infra_strasbourg_df,
            names="Amenagement_Infrastructure",
            values="Pourcentage",
            color_discrete_sequence=px.colors.sequential.Mint
        )
        fig_infra_strasbourg.update_layout(margin=dict(t=50, b=50, l=100, r=100))
        st.plotly_chart(fig_infra_strasbourg, use_container_width=True)

    # --- Section Top 5 des combinaisons causant des accidents ---
    st.markdown("---")
    display_vignette("Top 5 des combinaisons de facteurs causant des accidents", bg_color="#BBDEFB")
    combinaisons = mesures['combinaisons_accidents'].sort_values("Nombre_Accidents", ascending=False).head(5)
    combinaisons["Combinaison"] = (
        combinaisons["Situation_Accident"].astype(str) + " | " +
        combinaisons["Amenagement_Infrastructure"].astype(str) + " | " +
        combinaisons["Intersection"].astype(str) + " | " +
        combinaisons["Categorie_Route"].astype(str) + " | " +
        combinaisons["Régime_Circulation"].astype(str)
    )
    fig_comb = px.bar(
        combinaisons,
        x="Combinaison",
        y="Nombre_Accidents",
        color="Combinaison",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_comb.update_layout(
        xaxis_tickangle=-45,
        xaxis_title="",
        yaxis_title="Nombre d'accidents",
        xaxis_showticklabels=False,
        legend_title="Combinaisons",
        legend_orientation="h",
        legend_yanchor="bottom",
        legend_y=0.70,
        legend_xanchor="right",
        legend_x=1.05,
        margin={"t": 80}
    )
    st.plotly_chart(fig_comb, use_container_width=True)

    # --- Section Évolution des taux d'accidents (Infrastructure) ---
    st.markdown("---")
    display_vignette("Évolution des taux d'accidents (pas d'Infrastructure)", bg_color="#BBDEFB")
    fig_infra_evolution = px.line(
        mesures['df_infra_evolution'],
        x="Annee_Accident",
        y="Taux_Accidents",
        color="Metropole",
        line_dash="Amenagement_Infrastructure",
        markers=True,
        title="Évolution des taux d'accidents (par circulation)"
    )
    fig_infra_evolution.update_layout(
        xaxis_title="Année",
        yaxis_title="Taux d'accidents (par circulation)"
    )
    st.plotly_chart(fig_infra_evolution, use_container_width=True)

    # --- Section Évolution des projets et accidents par année ---
    st.markdown("---")
    display_vignette("Évolution des projets et accidents par année", bg_color="#BBDEFB")
    # Récupération des DataFrames pour projets et accidents
    df_projets_grenoble = mesures['df_projets_grenoble']
    df_projets_strasbourg = mesures['df_projets_strasbourg']
    df_accidents_yearly_grenoble = mesures['df_accidents_yearly_grenoble']
    df_accidents_yearly_strasbourg = mesures['df_accidents_yearly_strasbourg']
    common_years = sorted(list(set(df_projets_grenoble["Annee"]).intersection(set(df_projets_strasbourg["Annee"]))))
    if not common_years:
        st.error("Aucune année commune trouvée entre Grenoble et Strasbourg.")
    else:
        common_year_min, common_year_max = min(common_years), max(common_years)
        selected_years = st.slider("Sélectionnez la plage d'années communes", int(common_year_min), int(common_year_max), (int(common_year_min), int(common_year_max)))
        st.write("Années sélectionnées :", selected_years)
        df_projets_grenoble_filtered = df_projets_grenoble[
            (df_projets_grenoble["Annee"].isin(common_years)) &
            (df_projets_grenoble["Annee"] >= selected_years[0]) &
            (df_projets_grenoble["Annee"] <= selected_years[1])
        ]
        df_projets_strasbourg_filtered = df_projets_strasbourg[
            (df_projets_strasbourg["Annee"].isin(common_years)) &
            (df_projets_strasbourg["Annee"] >= selected_years[0]) &
            (df_projets_strasbourg["Annee"] <= selected_years[1])
        ]
        df_accidents_yearly_grenoble_filtered = df_accidents_yearly_grenoble[
            (df_accidents_yearly_grenoble["Annee_Accident"] >= selected_years[0]) &
            (df_accidents_yearly_grenoble["Annee_Accident"] <= selected_years[1])
        ]
        df_accidents_yearly_strasbourg_filtered = df_accidents_yearly_strasbourg[
            (df_accidents_yearly_strasbourg["Annee_Accident"] >= selected_years[0]) &
            (df_accidents_yearly_strasbourg["Annee_Accident"] <= selected_years[1])
        ]
        # Graphique combiné pour Grenoble
        fig_grenoble_combined = make_subplots(specs=[[{"secondary_y": True}]])
        fig_grenoble_combined.add_trace(
            go.Bar(
                x=df_projets_grenoble_filtered["Annee"],
                y=df_projets_grenoble_filtered["Nombre_Projets"],
                name="Projets d'aménagement"
            ),
            secondary_y=False
        )
        fig_grenoble_combined.add_trace(
            go.Scatter(
                x=df_accidents_yearly_grenoble_filtered["Annee_Accident"],
                y=df_accidents_yearly_grenoble_filtered["Nombre_Accidents"],
                name="Accidents",
                mode="lines+markers"
            ),
            secondary_y=True
        )
        # Graphique combiné pour Strasbourg
        fig_strasbourg_combined = make_subplots(specs=[[{"secondary_y": True}]])
        fig_strasbourg_combined.add_trace(
            go.Bar(
                x=df_projets_strasbourg_filtered["Annee"],
                y=df_projets_strasbourg_filtered["Nombre_Projets"],
                name="Projets d'aménagement"
            ),
            secondary_y=False
        )
        fig_strasbourg_combined.add_trace(
            go.Scatter(
                x=df_accidents_yearly_strasbourg_filtered["Annee_Accident"],
                y=df_accidents_yearly_strasbourg_filtered["Nombre_Accidents"],
                name="Accidents",
                mode="lines+markers"
            ),
            secondary_y=True
        )
        max_y_projects = max(df_projets_grenoble_filtered["Nombre_Projets"].max(),
                             df_projets_strasbourg_filtered["Nombre_Projets"].max())
        max_y_accidents = max(df_accidents_yearly_grenoble_filtered["Nombre_Accidents"].max(),
                              df_accidents_yearly_strasbourg_filtered["Nombre_Accidents"].max())
        fig_grenoble_combined.update_layout(
            yaxis=dict(range=[0, max_y_projects], showgrid=False),
            yaxis2=dict(range=[0, max_y_accidents])
        )
        fig_strasbourg_combined.update_layout(
            yaxis=dict(range=[0, max_y_projects], showgrid=False),
            yaxis2=dict(range=[0, max_y_accidents]),
            title_text="Projets d'aménagement et Accidents par année - Strasbourg"
        )
        fig_grenoble_combined.update_xaxes(title_text="Année")
        fig_grenoble_combined.update_yaxes(title_text="Nombre de Projets", secondary_y=False)
        fig_grenoble_combined.update_yaxes(title_text="Nombre d'Accidents", secondary_y=True)
        fig_strasbourg_combined.update_xaxes(title_text="Année")
        fig_strasbourg_combined.update_yaxes(title_text="Nombre de Projets", secondary_y=False)
        fig_strasbourg_combined.update_yaxes(title_text="Nombre d'Accidents", secondary_y=True)
        col_chart_left, col_chart_right = st.columns(2, gap="medium")
        with col_chart_left:
            st.plotly_chart(fig_grenoble_combined, use_container_width=True)
        with col_chart_right:
            st.plotly_chart(fig_strasbourg_combined, use_container_width=True)

        # --- Section Évolution du Budget et du Taux d'Accidentologie (Strasbourg uniquement) ---
        st.markdown("---")
        display_vignette("Évolution du Budget et du Taux d'Accidentologie - Strasbourg", bg_color="#BBDEFB")
        df_budget_yearly = mesures['df_budget_yearly']  # Colonnes: "Année" et "Strasbourg"
        df_accidents_yearly_strasbourg = mesures['df_accidents_yearly_strasbourg']  # Colonnes: "Annee_Accident", "Nombre_Accidents"
        moyenne_strasbourg = mesures['moyenne_strasbourg']
        df_acc = df_accidents_yearly_strasbourg.copy()
        df_acc.rename(columns={"Annee_Accident": "Année"}, inplace=True)
        common_years_budget = sorted(list(set(df_budget_yearly["Année"]).intersection(set(df_acc["Année"]))))
        df_budget_strasbourg_filtered = df_budget_yearly[df_budget_yearly["Année"].isin(common_years_budget)]
        df_acc_filtered = df_acc[df_acc["Année"].isin(common_years_budget)]
        df_acc_filtered = df_acc_filtered.copy()
        df_acc_filtered["Taux_Accidents"] = df_acc_filtered["Nombre_Accidents"] / moyenne_strasbourg
        fig_strasbourg_budget = make_subplots(specs=[[{"secondary_y": True}]])
        fig_strasbourg_budget.add_trace(
            go.Scatter(
                x=df_budget_strasbourg_filtered["Année"],
                y=df_budget_strasbourg_filtered["Strasbourg"],
                name="Budget annuel moyen (€M)",
                mode="lines+markers",
                line=dict(color="blue")
            ),
            secondary_y=False
        )
        fig_strasbourg_budget.add_trace(
            go.Scatter(
                x=df_acc_filtered["Année"],
                y=df_acc_filtered["Taux_Accidents"],
                name="Taux d'accidentologie",
                mode="lines+markers",
                line=dict(color="red", dash="dash")
            ),
            secondary_y=True
        )
        fig_strasbourg_budget.update_layout(
            title="Évolution du Budget et du Taux d'Accidentologie - Strasbourg",
            xaxis_title="Année"
        )
        fig_strasbourg_budget.update_yaxes(title_text="Budget annuel moyen (€M)", secondary_y=False)
        fig_strasbourg_budget.update_yaxes(title_text="Taux d'accidentologie", secondary_y=True)
        fig_strasbourg_budget.update_layout(
            yaxis=dict(showgrid=False, rangemode="tozero")
        )
        st.plotly_chart(fig_strasbourg_budget, use_container_width=True)


# ----------------- Recommandations: Page -----------------

elif page == "Recommandations":
    st.title("Recommandations")
    
    
    # Page de recommandations
    st.title("🚴 Recommandations pour la Sécurité Cycliste")

    st.markdown(
        """
        <style>
            .recommendation-box {
                background-color: #f9f9f9;
                padding: 15px;
                border-radius: 10px;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                font-size: 18px;
                line-height: 1.5;
            }
            .recommendation-box ul {
                padding-left: 20px;
            }
        </style>
        """, 
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="recommendation-box">
            <ul>
                <li><b>Améliorer les routes :</b> Mettre en place des pistes cyclables sécurisées.</li>
                <li><b>Carrefours sécurisés :</b> Ajouter signalisation et feux spécifiques.</li>
                <li><b>Évaluer les infrastructures :</b> Analyser efficacité et fréquentation.</li>
                <li><b>Comparaison avec d'autres villes :</b> Identifier les meilleures pratiques.</li>
                <li><b>Investir dans la sécurité :</b> Développer pistes protégées et passages sécurisés.</li>
                <li><b>Points noirs :</b> Identifier et corriger les zones à risque.</li>
                <li><b>Budget sécurité :</b> Augmenter le financement des aménagements.</li>
                <li><b>Mobilité alternative :</b> Encourager vélo, marche et transports publics.</li>
                <li><b>Sensibilisation :</b> Éduquer sur la sécurité routière.</li>
                <li><b>Suivi et évaluation :</b> Mesurer et ajuster les stratégies.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )