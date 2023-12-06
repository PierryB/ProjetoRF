import firebase_admin
import datetime
from firebase_admin import credentials
from firebase_admin import firestore

# Use o caminho real para o arquivo de configuração JSON do Firebase
cred = credentials.Certificate("C:/Users/Teste/Desktop/Faculdade/ProjetoRF/firebaseAuth.json")
firebase_admin.initialize_app(cred)

def enviar_dados_nuvem(nome_usuario):

    data_hora_atual = datetime.datetime.now()

    data_formatada = data_hora_atual.strftime("%d/%m/%Y")
    hora_formatada = data_hora_atual.strftime("%H:%M:%S")

    print("Data formatada:", data_formatada)
    print("Hora formatada:", hora_formatada)
    print("Usuário: " + nome_usuario)

    db = firestore.client()

    dados = {
        "data": data_formatada,
        "hora": hora_formatada,
        "nome_usuario": nome_usuario
    }

    nome_colecao = "registros"
    db.collection(nome_colecao).add(dados)
