# Consultador de CPF

Verifique o status do CPF dos clientes, necessário data de nascimento e CPF do cliente. Esta automatização é capaz de consultar o cpf e data de nascimento passado para comprovar a situação cadastral no site da Receita Federal

## Tecnologias Utilizadas

#### Neste projeto foram usados as seguintes tecnologias:

```
      - Python
      - Selenium
      - Pandas
      - MongoDB
      - TwoCaptcha
```

## Pré Requisitos:

      - Python
      - Pip
      - MongoDB Compass
      - ChromeDriver

# Assim que ter acesso ao código siga o passo a passo :

## Abra o terminal para instalar as dependências no ambiente virtual(venv):

#### Para utilizar o venv se estiver utilizando Linux use o comando:

        source venv/bin/activate

#### Para utilizar o venv se estiver utilizando bash use o comando:

        source venv/Scripts/activate

#### Para utilizar o venv se estiver utilizando PowerShell use o comando:

        venv/Scripts/activate

### Para instalar as dependências use o comando:

         pip install -r requirements.txt

##### Dentro do arquivo requirements.txt está todos as denpendências que o projeto necessita para o código rodar normalmente.

### Crie uma database no MongoDB, com os mesmos nomes:

        DB: "consultar_cpf"
        Collection: "consultar_cpf_collection

#### Caso crie com outros nomes é possível mudar somento o código com o nome correto no script.py:

        mydb = my_client['outro_nome_db']
        mycol = mydb['outro_nome_colletion']

### Caso tenha interesse em colocar outros CPF's, basta criar um novo arquivo csv, excel ou txt e mudar o caminho de acesso, disponível no arquivo script.py:

        file_path = 'exampleOfCPF.csv'

## O Script foi rodado em cima de um navegador Chrome, portando deve se baixar o ChromeDriver disponível aqui: https://chromedriver.chromium.org/downloads(*verificar qual versão do Chrome esta usando!\*)

# Após instalar pode se iniciar o projeto com

        python script.py
