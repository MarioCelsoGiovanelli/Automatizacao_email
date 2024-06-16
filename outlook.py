from imbox import Imbox
import json
from datetime import date

# Abrindo o arquivo de credenciais:
with open("credenciais_outlook.json", "r") as file:
    credenciais = json.loads(file.read())

email = credenciais["e-mail"]
senha = credenciais["password"]
servidor = credenciais["host"]

# Chamando a classe Imbox:
with Imbox(
    hostname=servidor,
    username=email,
    password=senha) as imb:

    # Retornar só mensagens não lidas:
    mensagens = imb.messages(unread = True, date__gt = date(2024, 5, 10))

    if not mensagens:
        print("Ocorreu um erro!")

    # Verificando a quantidade de e-mail:
    print(len(mensagens))

    # Acessando as mensagens:
    for uid, msg in mensagens:
        print(f"De: {msg.sent_from[0]['email']}")
        print(f"Assunto: {msg.subject}")
        
        for anexo in msg.attachments:
            nome_arquivo = anexo['filename']
            conteudo = anexo['content']

            with open(f"anexos/{nome_arquivo}", "wb") as file:
                file.write(conteudo.read())

            print(anexo['filename'])

        print("\n")