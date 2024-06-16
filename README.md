![Badge Concluido](http://img.shields.io/static/v1?label=STATUS&message=%20CONCLUIDO&color=GREEN&style=for-the-badge)

# :robot: Automatização de E-mails

  Essa automação se conecta a um servidor de e-mail e faz um filtro: uma busca no e-mail por tipo, por data especifica ou a partir de uma data, busca determinadas mensagens por palavra.
  E para se conectar ao servidor de e-mail será utilizado o protocolo **[IMAP](https://support.microsoft.com/pt-br/office/o-que-s%C3%A3o-imap-e-pop-ca2c5799-49f9-4079-aefe-ddca85d5b1c9#:~:text=O%20IMAP%20permite%20que%20voc%C3%AA,o%20do%20servi%C3%A7o%20de%20email)**.

  Esse método de acesso que garante mais segurança quando precisa marcar e-mails de vários dispositivos diferentes.
  Para fazer uma automação utilizando o **Gmail** é necessário que a autenticação de dois fatores esteja ativada.

  Vá em no menu **Google Apps** do Gmail, opção **Conta**, menu **Segurança**, no campo **Como você faz login no Google** , **Verificação em duas etapas** tem que estar **Ativada**
  No link do **[Myaccount](https://myaccount.google.com/apppasswords)** é possível criar um nome de aplicativo, ele vai passar uma senha, copie essa senha e coloque em um arquivo formato **Json**.  Ex: credenciais_gmail.json.
  Neste arquivo deve conter: e-mail, senha e host do servidor. Host é o endereço IMAP do servidor.

````python
{
    "e-mail": "seuemail@gmail.com",
    "password": "suasenha",
    "host": "imap.gmail.com"
}
````

:movie_camera: VIDEO 01

<img src=".\Animação01.gif" alt="Código funcionando" width="600px" heidth="400px">

Para ler esse arquivo com as credenciais do servidor, **with open(“nome_da_credencial.json”, “r”) as file:**, e colocamos em uma variável chamando o modulo **Json** e com o método **loads** para ele ler o arquivo com o parâmetro **file.read()**.

````python
with open(“nome_da_credencial.json”, “r”) as file:
	credenciais = json.loads(file.read())
````

armazenado cada informação do servidor em uma variável.

````python
email = credenciais[“e-mail”]
senha = credenciais[“passoword”]
servidor = credenciais[“host”]
````

para conectar ao servidor:

````python
with Imbox(
hostname=servidor,
username=email,
password=senha) as imb:

mensagens = imb.messages()
````

para acessar as propriedades das mensagens...
verificar a quantidade de mensagens usamos o **len()**, retornará todas as mensagens do e-mail.

````python
print(len(mensagens))
````

Usando o **for** para iterar com o conteúdo do e-mail, usando o método **keys()** para listar as chaves e suas propriedades. Obs: O Break no final do código para não ler todos os e-mails.

````python
for uid, msg in mensagens:
	print(msg.keys())
	break
````

**Send_from** = Quem enviou – Retorna chave: name, email. Retorna nome do remetente e e-mail.

**Sent_to** = Para quem enviou – Retorna chave: name, email. Retorna nome para quem enviou e e-mail.

**Subjerct** = Assunto – Retorna chave: Texto com conteúdo

**Headers** = Cabeçalhos – Retorna chave: name, value, cliente-ip. Retorna nome SPF (Sender Policy Framework), valor do pass e IP

**Message_id** = Mensagem ID – Retorna chave: Mensagem com ID

**Date** = Data – Retorna chave: Dia da semana, mês, ano, hora. Retorna uma data especifica, a partir de uma data ou anterior a uma data especifica.

**Attachments** = Anexo – Retorna chave: content, size, content-id, filename. Retorna informações sobre anexo como, conteúdo, tipo, tamanho e nome do arquivo.

**Body** = Corpo – Retorna chave: plain, html. Retorna o corpo do e-mail, também em html

Para buscar quem enviou o e-mail e o assunto, podemos juntar os métodos **sent_from** e **subject**, podemos também concatenar com **f string**, com primeiro elemento índice **[0]** e a chave do elemento **‘email’**.

````python
for uid, msg in mensagens:
	print(f”De: {msg.send_from[0][‘email’]}”)
	print(f”Assunto: {msg.subject}”)
	break
````

### :e-mail: Filtrando os e-mails:

Para trazer as mensagens que não forem lidas, passamos um parâmetro para o método **messages()** do **Imbox**, **messages(unread=True)**, para mensagens que forem lidas **messages(unread=False)**

````python
mensagens = imb.messages(unread=True)
````

Para buscar por datas usamos como parâmetro para o método **messages()** do **Imbox**, 
**date__on**, esse parâmetro faz a busca de e-mails por uma data especifica.

````python
mensagens = imb.messages(date__on = data(2024, 02, 15)
````

Para buscar por e-mails após uma data especifica **date__gt**

````python
mensagens = imb.messages(date__gt = data(2024, 02, 15)
````

Para buscar e-mails anterior a uma data especifica **date__lt**

````python
mensagens = imb.messages(date__lt = data(2024, 02, 15)
````

Para retornar só e-mails que esteja marcado com estrelas, passamos como parâmetro **flagged = True**.

````python
mensagens = imb.messages(flagged = True)
````

Para filtrar os e-mails por uma mensagem especifica, passamos como parâmetro uma strig com o parâmetro **subject = “palavra”**

````python
mensagens = imb.messages(subject = “palavra”)
````

Combinando filtros para trazer mais de um resultado, como, por exemplo, filtrar por e-mail recebido e a partir de uma data especifica.

````python
mensagens = imb.messages(sent_from = “google@gmail.com”, data_gt = date(2024, 1, 2))
````

### :paperclip: Trabalhando com anexos:

Primeiro criar uma pasta para que os anexos sejam armazenados, depois usamos o método **attachments** em um **for** para iterar nos e-mails recebidos retornando os anexos.
Usando variáveis para armazenar as chaves **’filename’** e outra variável vai receber o conteúdo binário do anexo **’content’**.

````python
for anexo in msg.attachments:
	nome_arquivo = anexo[‘filename’]
	conteudo = anexo[‘content’]
````
	
Para trabalhar com arquivo no Python usamos o **with open()** como parâmetro a variável com o nome do arquivo e abrir ele no modo de with na forma binária **”wb”**, para salvar na pasta passamos como parâmetro **open(f”anexo/{nome_arquivo}”)**.

````python
with open(f”anexos/{nome_arquivo}”, “wb”) as file:
````

Agora chamamos o arquivo e passamos como método **file.white()** como parâmetro a variável com o conteúdo e com o método **read()**.

````python
with open(f”anexos/{nome_arquivo}”, “wb”) as file:
file.white(conteudo.read())
````

### :joystick: Automatizando outro servidor:

Todos esses métodos funcionam também no servidor **Outlook**, criando uma credencial com o e-mail do **Outlook**, senha e host, basta mudar as informações onde contém o **Gmail**.

````python
{
	“e-mail”: “seuemail@outlook.com”,
	“passord”: “suasenha”,
	“host”: “imap.outlook.com”
}

with open(“credenciais_outlook.json”, “r”) as file:
	credenciais = json.loads(file.read())
````

### :bookmark_tabs: Arquivo Requirements:

É um arquivo de texto formato **.txt** e, neste arquivo, está especificado todos os pacotes e bibliotecas que são utilizados no projeto. Isso ajuda para que se garanta que, se o projeto for usado por outro desenvolvedor, não aconteça erros ou problemas por causa da alguma atualização na versão do pacote ou uma descontinuidade na linguagem Python.

Para instalar, entre no terminal **Ctrl + ‘** e instale o requirements para usar todos os pacotes na mesma versão usada no projeto. 

````python
pip install -r requirements.txt
````


:video_camera: VIDEO 02


<img src=".\Animação03.gif" alt="Código funcionando" width="600px" heidth="400px">

## 📁 Como utilizar o código:

O arquivo **gmail.py** e **outlook.py**, pode ser usado em um terminal:

````python
python gmail.py
````
````python
python outlook.py
````

:film_projector: VIDEO 03

<img src=".\Animação02.gif" alt="Código funcionando" width="600px" heidth="400px">


imbox – Python IMAP
"https://github.com/martinrusev/imbox"

## :computer: Técnicas e Tecnologias utilizadas:

- Técnica de slicing

- Manipulação de strings

- Processos com tarefas repetitivas

- Tratamento de erros

- Estrutura condicional **if**  

- Laço de repetição **for**

- Enviar e-mails de forma automática


	- **Python**


## :books: Bibliotecas:

- **imbox**
  - pip install imbox

- **datetime**



## :electric_plug: Como usar as bibliotecas e seus módulos:

- from imbox import Imbox
- import json
- from datetime import date

