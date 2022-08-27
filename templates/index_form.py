import streamlit as st
import datetime
from datetime import date
import pandas as pd
import joblib
import requests
import json
import argparse
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


def get_days(date_value):
    today = date.today()
    delta = today - date_value
    return delta.days



# make a title for your webapp
st.title("Credit Scoring Form")

# make a Subheader for your webapp
st.subheader("Saisissez les informations dans les champs ci-dessous")

# Documentation >> st.help(st.form)


# Creating our form fields
with st.form("Credit Scoring Form", clear_on_submit=True):
    # (DAYS_BIRTH) Âge du client en jours au moment de la demande
    # days_birth = st.slider('Entrez votre date de naissance', min_value=18, max_value=100)
    days_birth = st.date_input('Entrez votre date de naissance')
    st.write('Votre date de naissance est:', days_birth)

    # (AMT_ANNUITY) Montant des annuités du prêt (remboursements)
    amt_annuity = st.number_input("Entrez le montant de vos revenus salariés mensuels")
    st.write('Le montant de vos revenus salariés mensuels est:', amt_annuity)

    # (EXT_SOURCE_3) Score normalisé à partir d'une source de données externe
    ext_source_3 = st.number_input('Entrez le montant de vos revenus externes mensuels 3')
    st.write('Le montant de vos revenus salariés mensuels 3 est:', ext_source_3)

    # (EXT_SOURCE_2) Score normalisé à partir d'une source de données externe
    ext_source_2 = st.number_input('Entrez le montant de vos revenus externes mensuels 2')
    st.write('Le montant de vos revenus salariés mensuels 2 est:', ext_source_2)

    # (DAYS_ID_PUBLISH) Combien de jours avant la demande par le client du
    # changement de la pièce d'identité avec laquelle il a demandé le prêt
    days_id_publish = st.date_input("Entrez la date d'expiration de la pièce d'identité utilisée pour votre demande de prêt")
    st.write('La date d\'expiration de la pièce d\'identité utilisée pour votre demande de prêt est:', days_id_publish)

    # (AMT_CREDIT) Montant du crédit accordé pour le prêt
    amt_credit = st.number_input("Entrez le montant de votre crédit")
    st.write('Le montant de votre crédit est:',  amt_credit)

    # (DAYS_LAST_PHONE_CHANGE) Combien de jours avant la demande par le client du changement de son téléphone
    days_last_phone_change = st.date_input("Entrez la date de votre dernier changement de téléphone mobile")
    st.write('La date de votre dernier changement de téléphone mobile est:', days_last_phone_change)

    #(DAYS_EMPLOYED) Nombre de jours écoulés depuis la prise de poste du client dans son emploi actuel
    days_employed = st.date_input("Entrez la date de début de votre contrat de travail")
    st.write('La date de début de votre contrat de travail est:', days_employed)

    # (DAYS_REGISTRATION) Nombre de jours avant la demande par le client de la modification de son inscription
    days_registration = st.date_input("Entrez la date de la première modification votre inscriptiopn")
    st.write('a date de la première modification votre inscriptiopn est:', days_registration)

    # (AMT_GOODS_PRICE) le prix des biens pour lesquels le prêt est accordé
    amt_goods_price = st.number_input("Entrez le montant de la valeur totale des biens pour lesquels le prêt est accordé")
    st.write('Le montant de la valeur totale des biens pour lesquels le prêt est accordé est:', amt_goods_price)


    dashboard = st.checkbox("Afficher les informations client ?")
    submit = st.form_submit_button(label="Envoyer le formulaire")

    # If submit button is pressed
    if submit:
        #app.py
        # URL = "https://github.com/MorgvnMdln/ocr_p07/blob/main/templates/index_form.py"
        # URL = "https://github.com/MorgvnMdln/ocr_p07"
        URL = "http://127.0.0.1:5000/api/predict"

        # defining a params dict for the parameters to be sent to the API
        PARAMS = {
              "days_birth":get_days(days_birth),
              "amt_annuity":amt_annuity,
              "ext_source_3":ext_source_3,
              "ext_source_2":ext_source_2,
              "days_id_publish":get_days(days_id_publish),
              "amt_credit":amt_credit,
              "days_last_phone_change":get_days(days_last_phone_change),
              "days_employed":get_days(days_employed),
              "days_registration":get_days(days_registration),
              "amt_goods_price":amt_goods_price,
              }
        # print(PARAMS)
        # sending get request and saving the response as response object
        r = requests.get(url=URL, params=PARAMS)
        # extracting data in json format
        response = r.json()
        label = response['data']



        #PieChart
        if dashboard:
            # Customer information display : Customer Gender, Age, Family status, Children, …
            st.sidebar.header("**Information client**")
            fig, ax = plt.subplots(figsize=(5,5))
            plt.pie(label, explode=[0, 0.1], labels=['Good', 'Bad'], autopct='%1.1f%%', startangle=90)
            # Change the background color of the plot
            # plt.rcParams['figure.facecolor'] = 'black'
            fig.patch.set_facecolor('#262730')
            st.sidebar.pyplot(fig)


