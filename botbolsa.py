import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
navegador = webdriver.Chrome(options=options)
navegador.get("http://www.statusinvest.com.br")
sleep(3)

data_atual = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
pontuacao = navegador.find_element(By.XPATH, '//*[@id="main-2"]/section[1]/div[2]/div[2]/a[1]/div[1]/strong').text
empresas_val = []
cotacao_val = []
porcentagens_val = []
dados_val = []
dict1 = {}

for i in range(1, 7):
    empresas_val.append(navegador.find_element(By.XPATH,
                                                f'//*[@id="today-acao"]/div/div[2]/div[1]/div/div[{i}]/div[2]/a/h4/small').text)
    porcentagens_val.append(navegador.find_element(By.XPATH,
                                                f'//*[@id="today-acao"]/div/div[2]/div[1]/div/div[{i}]/div[2]/div/span[1]').text.replace(",", "."))
    cotacao_val.append(navegador.find_element(By.XPATH,
                                                f'//*[@id="today-acao"]/div/div[2]/div[1]/div/div[{i}]/div[2]/div/span[2]').text.replace("R$\n", ""))

for a, b, c in zip(empresas_val, cotacao_val, porcentagens_val):
    dict1 = {}
    dict1["Empresa"] = a
    dict1["Cotação (R$)"] = float(b.replace(",", "."))
    dict1["Valorização (%)"] = float(c.replace("\n%", "").replace("arrow_upward\n", ""))
    dict1["Horário"] = data_atual
    dados_val.append(dict1)

with open("valbolsa.json", "r+", encoding='utf-8') as file:
    file_data = json.load(file)
    for dados in dados_val:
       file_data.append(dados)
       file.seek(0)
    json.dump(file_data, file, ensure_ascii=False)

tabela1 = pd.DataFrame.from_records(dados_val, index = [i for i in range(1, 7)])
print(f"A pontuação do Ibovespa no horário {data_atual} é de {float(pontuacao.replace('pts', ''))} pontos.")
print(f"As ações mais valorizadas do Ibovespa até o momento ({data_atual} horas): ")
print(tabela1)

empresas_desv = []
cotacao_desv = []
porcentagens_desv = []
dados_desv = []
dict2 = {}

for i in range(1, 7):
    empresas_desv.append(navegador.find_element(By.XPATH,
                                                f'//*[@id="today-acao"]/div/div[2]/div[2]/div/div[{i}]/div[2]/a/h4/small').text)
    porcentagens_desv.append(navegador.find_element(By.XPATH,
                                                f'//*[@id="today-acao"]/div/div[2]/div[2]/div/div[{i}]/div[2]/div/span[1]').text.replace("arrow_downward\n-", ""))
    cotacao_desv.append(navegador.find_element(By.XPATH,
                                                f'//*[@id="today-acao"]/div/div[2]/div[2]/div/div[{i}]/div[2]/div/span[2]').text.replace("R$\n", ""))

for a, b, c in zip(empresas_desv, cotacao_desv, porcentagens_desv):
    dict2 = {}
    dict2["Empresa"] = a
    dict2["Cotação (R$)"] = float(b.replace(",", "."))
    dict2["Desvalorização (%)"] = float(c.replace("\n%", "").replace(",", "."))
    dict2["Horário"] = data_atual
    dados_desv.append(dict2)

with open("desvalbolsa.json", "r+", encoding='utf-8') as file2:
  file2_data = json.load(file2)
  for dados in dados_desv:
    file2_data.append(dados)
    file2.seek(0)
  json.dump(file2_data, file2, ensure_ascii=False)

tabela2 = pd.DataFrame.from_records(dados_desv, index = [i for i in range(1, 7)])
print(f"As ações mais desvalorizadas do Ibovespa até o momento ({data_atual} horas): ")
print(tabela2)
