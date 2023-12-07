from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)

#with open('ia_model\\modelo_treinado_base.pkl', 'rb') as file:
    #model = pickle.load(file)


def previsao(dados):
    dados_formulário = pd.DataFrame(dados)

    resultado = model.predict(dados_formulário)

    return resultado