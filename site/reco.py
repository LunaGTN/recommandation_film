def afficher_reco():
    import streamlit as st
    import pandas as pd
    df_poster = pd.read_parquet('poster.parquet')
    df_reco = pd.read_parquet('reco.parquet')

    st.markdown("""
        <style>
        /* Style pour le texte */
        p {
            text-align: center;
            font-size: 20px;
            color: white;
        }
        iframe {
                text-align: center;
                }
        </style>""", unsafe_allow_html=True)

    st.markdown("<p>Soirée entre amis, film en solo, en couple ou en famille ?</p>", unsafe_allow_html = True)
    #st.markdown("""
    #<div style="display: flex; justify-content: center; align-items: center; margin-top: 20px;">
       # <iframe src="https://giphy.com/embed/KzzQ0lEye5zhwlPajK" width="480" height="360" frameBorder="0" class="giphy-embed" allowFullScreen></iframe>
    #</div>
    #""", unsafe_allow_html=True)

    st.markdown("<p>Tapez le début d’un titre qui vous plaît, choisissez parmi les suggestions, et laissez notre système dénicher 5 films qui pourraient vous divertir!</p>", unsafe_allow_html=True )


    col1, col2, col3 = st.columns([2, 3, 2])  # Centrer et définir les proportions
    with col2:
        option = st.selectbox(
            "selection film",
            options=df_poster["id"],
            format_func=lambda x: x if st.session_state.get("search_query", "").lower() in x.lower() else None, index=None, placeholder="Choisissez un film",
            label_visibility = "hidden"
        )
    image_url = "https://image.tmdb.org/t/p/original"

    if option:
        resultat = df_reco.loc[df_reco["id"] == option]
        if not resultat.empty: 
            # Recherche de l'index de la source
            recherche = resultat["source"].iloc[0]
            titre_str =  df_poster["id"].iloc[recherche]
            liste_titre = titre_str.split("-")
            titre_no_date = " ".join(liste_titre[:-1])

            print(df_poster["id"].iloc[recherche])
            if df_poster['poster_path'].iloc[recherche] is None:
                poster_url = "https://i.imghippo.com/files/ZOcN3975ToU.png"
            else:
                poster_url = image_url + df_poster['poster_path'].iloc[recherche]

            # **Affichage du premier film (au-dessus des recommandations)**
            st.markdown(
                f"""
                <div style="text-align: center;">
                    <h2>Film sélectionné</h2>
                    <p><strong>{titre_no_date}</strong></p>
                    <img src="{poster_url}" alt="Poster" style="width: 250px;">
                    <p>📅 <strong>Année :</strong> {df_poster['année'].iloc[recherche]}</p>
                    <p>🎥 <strong>Réalisateur :</strong> {df_poster['Real'].iloc[recherche]}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Ajouter un séparateur et plusieurs espaces vides
            st.empty()
            st.divider()
            st.empty()
        
            
            # **Affichage des recommandations**
            st.markdown(
                f"""
                <div style="text-align: center;">
                    <h2>Suggestions similaires</h2>
                """,
                unsafe_allow_html=True
            )
            columns = st.columns(5)  # Création des 5 colonnes
            
            # Récupération des recommandations
            recos = list(resultat[["r1", "r2", "r3", "r4", "r5"]].values)[0]
            titres = df_poster["id"].iloc[recos].tolist()
            annee = df_poster["année"].iloc[recos].tolist()
            real = df_poster["Real"].iloc[recos].tolist()
            poster = df_poster["poster_path"].iloc[recos].tolist()

            st.text(recos)

            # Affichage des recommandations dans les colonnes
            for i, (titre, annee, realisateur, poster_path) in enumerate(zip(titres, annee, real, poster)):
                liste_titre_reco = titre.split("-")
                titre_no_date_reco = " ".join(liste_titre_reco[:-1])
                with columns[i % 5]:  # Répartir les films sur 5 colonnes
                    st.markdown(f"{titre_no_date_reco}", unsafe_allow_html=True )
                    if poster_path is None :
                        st.image("logo_sans_fond.png", width=150)
                        st.text(f"📅 Année : {annee}")
                        st.text(f"🎥 Réalisateur : {realisateur}")
                    else:
                        st.image(f"{image_url}{poster_path}", width=150)
                        st.text(f"📅 Année : {annee}")
                        st.text(f"🎥 Réalisateur : {realisateur}")
                    
        else:
            st.warning("Aucun résultat trouvé pour cette sélection.")

    else:
        with col2:
            st.info("Veuillez chercher un film.")
