from flask import Flask, render_template, redirect, url_for
import pandas as pd
import random

app = Flask(__name__)

database_pokemon = pd.read_csv('pokemon.csv')

saldo_utente = 100
collezione_carte = []

probabilita_rarita = ['Comune'] * 70 + ['Non Comune'] * 20 + ['Rara'] * 9 + ['Ultra Rara'] * 1

def crea_bustina():
    pacchetto = []
    bonus_crediti = 0
    numero_carte = 0
    while numero_carte < 5:
        rarita = random.choice(probabilita_rarita)
        carte_disponibili = database_pokemon[database_pokemon['Rarità'] == rarita]
        if not carte_disponibili.empty:
            carta_estratta = carte_disponibili.sample(1).iloc[0]
            pacchetto.append(carta_estratta.to_dict())
            if rarita == 'Comune':
                bonus_crediti += 1
            elif rarita == 'Non Comune':
                bonus_crediti += 5
            elif rarita == 'Rara':
                bonus_crediti += 10
            elif rarita == 'Ultra Rara':
                bonus_crediti += 20
            numero_carte += 1
    return pacchetto, bonus_crediti

def salva_collezione():
    df_collezione = pd.DataFrame(collezione_carte)
    df_collezione.to_csv('pokedex.csv', index=False)

def carica_collezione():
    global collezione_carte
    try:
        collezione_carte = pd.read_csv('pokedex.csv').to_dict(orient='records')
    except FileNotFoundError:
        collezione_carte = []

carica_collezione()

@app.route('/')
def home():
    return render_template('index.html', credito=saldo_utente, carte=collezione_carte)

@app.route('/apri_bustina', methods=['POST'])
def apri_bustina():
    global saldo_utente, collezione_carte
    if saldo_utente >= 10:
        saldo_utente -= 10
        nuovo_pacchetto, crediti_bonus = crea_bustina()
        collezione_carte.extend(nuovo_pacchetto)
        salva_collezione()
        saldo_utente += crediti_bonus
    return redirect(url_for('home'))

@app.route('/credito', methods=['GET'])
def mostra_credito():
    return render_template('punti.html', credito=saldo_utente)

if __name__ == '__main__':
    app.run(debug=True)
