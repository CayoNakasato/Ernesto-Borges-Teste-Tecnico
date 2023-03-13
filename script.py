import pandas as pd
import ipdb
from selenium import webdriver
from selenium.webdriver.common.by import By
from twocaptcha import TwoCaptcha
import pymongo

import time

file_path = 'examplesOfCPF.csv'
url_do_form = 'https://servicos.receita.fazenda.gov.br/servicos/cpf/consultasituacao/ConsultaPublica.asp'

my_client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = my_client["consultar_cpf"]
mycol = mydb["consultar_cpf_collection"]

df = pd.read_csv(file_path, sep=';')

clients_list = []

print("Loop para pegar cada dado(CPF e data de nascimento) e a cada um deles realizar a pesquisa no site da RF")
for index, row in df.iterrows():
    client_info = {}

    print("Instanciando o driver do selenium do Chrome")
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    driver.get(url_do_form)

    print("Dando um tempo para página carregar os elementos")
    time.sleep(3)

    print("Selecionando os inputs que vamos trabalhar")
    element_cpf = driver.find_element(By.XPATH, '//*[@id="txtCPF"]')

    element_birthDate = driver.find_element(By.XPATH, '//*[@id="txtDataNascimento"]')

    print("Enviando aos inputs selecionados as informações que estamos passando pelo dataframe")
    element_cpf.send_keys(str(row['CPF']))

    element_birthDate.send_keys(str(row['DataNascimento']))

    print("Script de decriptação de hcaptcha")
    captcha_resolvido = False
    captcha = driver.find_element(By.XPATH, '//*[@id="hcaptcha"]')

    if captcha:
        print("Captcha encontrado")
        cont_captcha = 0
        while not captcha_resolvido: 
            cont_captcha += 1
            solver = TwoCaptcha('dc287f2fd747481db4fd175a55f2b042')
            if solver:
                print('Autenticação com serviço do captcha ocorreu com sucesso')
                print(f"INICIANDO A QUEBRA DO CATPCHA, TENTATIVA: {cont_captcha}")

                data_sitekey = driver.find_element(By.XPATH, '//*[@id="hcaptcha"]').get_attribute("data-sitekey")

                id_tag = driver.find_element(By.XPATH, '//*[@id="hcaptcha"]/iframe').get_attribute("data-hcaptcha-widget-id")

                print(f'Identificação do captcha: {data_sitekey}')
                print(f'Identificação do padrão do id do h-captcha: {id_tag}')
                try:
                    resultado = solver.hcaptcha(data_sitekey, url_do_form)
                except solver.exceptions as captchaerro:
                    print(f"EXCESSÁO NO CAPTCHA - {captchaerro.__cause__}")
                    captcha_resolvido = False
                    continue
                if resultado:
                    token = resultado['code']
                    print('Token obtido do serviço')
                    print('Registrando controle de captcha')
                    print(f'Verificando o response do h-captcha!')
                    hr = driver.find_element(By.ID, f'h-captcha-response-{id_tag}')
                    print(f'Fazendo o injection de Javascript dentro do código com a resposta do captcha.')

                    driver.execute_script(f"arguments[0].innerHTML = '{token}';", hr)

                    submit = driver.find_element(By.XPATH, '//*[@id="hcaptcha"]')

                    if submit:
                        submit.submit()
                        captcha_resolvido = True
                        print(f"CATPCHA RESOLVIDO NA TENTATIVA: {cont_captcha}")
    else:
        submit = driver.find_element(By.XPATH, '//*[@id="id_submit"]')
        if submit:
            submit.submit()
            print(f"Submit no formulário")

    print("Dando mais alguns segundos para carregar os elementos da página")
    time.sleep(3)

    print("Selecionando elementos que necessitamos para obter as informações na página")
    elementos = driver.find_elements(By.XPATH, '//*[@id="mainComp"]/div[2]/p/span/b')

    print("Criando um dict com as informações de cada cliente")
    client_info["CPF"] = elementos[0].text
    client_info["Nome"] = elementos[1].text
    client_info["DataNascimento"] = elementos[2].text
    client_info["statusCPF"] = elementos[3].text

    print("Armazenando cada cliente em uma list")
    clients_list.append(client_info)

print("Inserindo os clientes dento da collection da db")
new_client = mycol.insert_many(clients_list)

print("Armazenando todos os dados em uma variavel")
clients = mycol.find()

print("Criando um arquivo excel")
writer = pd.ExcelWriter('CPFsConsultados.xlsx', engine='xlsxwriter')

print("Criando um novo data frame")
principal_df = pd.DataFrame(columns=["CPF", "Nome", "DataNascimento", "statusCPF"])

print("Aqui uma função para validar o status do CPF para os status tratados da maneira correta")


def status_converter(client):
    match client['statusCPF']:
        case "PENDENTE DE REGULARIZAÇÃO":
            client['statusCPF'] = 0

        case "REGULAR":
            client['statusCPF'] = 1

        case "CANCELADO":
            client['statusCPF'] = 2

        case "SUSPENSO":
            client['statusCPF'] = 3

        case "TITULAR FALECIDO ":
            client['statusCPF'] = 4

    return client


print("Loop para adicionar cada cliente no excel, sempre adicionando um de cada vez")
for client in clients:
    status_converter(client)
    principal_df = principal_df.append(client, ignore_index=True)

print("Transformando o dataframe principal em excel")
principal_df.to_excel(writer, sheet_name='CPF_Info')

print("Terminando o excel com seu fechamento e arquivo criado na raiz do projeto")
writer.close()
