import cv2
import face_recognition
import time
import os
from sympy import false, true

# Importa a rotina de enviar os dados para nuvem
from EnviarDadosNuvem import enviar_dados_nuvem

isReconheceu = bool(false)
arquivo_imagem = "C:/Users/Teste/Desktop/Faculdade/ProjetoRF/Rostos/Leonardo.jpeg"

imagem_pessoa1 = face_recognition.load_image_file(arquivo_imagem)
pessoa1_face_encoding = face_recognition.face_encodings(imagem_pessoa1)[0]

# Inicializa a captura de vídeo da câmera
taxa_de_quadros = 30
video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FPS, taxa_de_quadros)
tempo_limite = 30 * 1000
inicio_tempo = time.time() * 1000  # Obtém o tempo atual em milissegundos

while True:
    # Captura o quadro da câmera
    ret, frame = video_capture.read()

    # Encontra todos os rostos no quadro
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Inicialize uma lista para os nomes das pessoas reconhecidas
    nomes_encontrados = []

    # Compare os rostos encontrados com o rosto conhecido
    for face_encoding in face_encodings:
        match = face_recognition.compare_faces([pessoa1_face_encoding], face_encoding)
        nome = "Desconhecido"

        # Se encontrarmos uma correspondência, use o nome conhecido
        if match[0]:
            nome = os.path.splitext(arquivo_imagem)[0].split('/')[-1]
            isReconheceu = true

        nomes_encontrados.append(nome)

    # Desenhe caixas ao redor dos rostos encontrados e exiba os nomes
    for (top, right, bottom, left), nome in zip(face_locations, nomes_encontrados):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, nome, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    # Mostre o quadro resultante
    cv2.imshow('Video', frame)

    # Verifique se o tempo limite foi atingido
    tempo_atual = time.time() * 1000
    if tempo_atual - inicio_tempo >= tempo_limite:
        break
    elif isReconheceu == true:
        print("reconheceu")
        enviar_dados_nuvem(nome)
        time.sleep(2)
        break
    # Pare o loop quando pressionar a tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libere a captura de vídeo e feche a janela
video_capture.release()
cv2.destroyAllWindows()
