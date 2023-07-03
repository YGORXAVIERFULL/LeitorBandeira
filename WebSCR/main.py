import requests
from bs4 import BeautifulSoup
import pprint
import dataBaseSeting as db
#-----------------CONEXAO BANCO----------------------#
import pyodbc

conexao = None
try:
    
    server = db.server
    database = db.database
    username = db.username
    password = db.password

    # Crie a string de conexão
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={db.server};DATABASE={db.database};UID={db.username};PWD={db.password}'
    conn = pyodbc.connect(connection_string)
    print("Conexão estabelecida com sucesso!")
    select = conn.cursor()



except pyodbc.Error as ex:  # ERRO DA CONEXÃO
    sqlstate = ex.args[0]
    print("falha na conexão"+sqlstate)
#------------------------------------------------------#

Cabecalho = {'user-agent': 'Mozilla/5.0'}
#----------------------------------WEB SCREPPING---------------------------------#
Dados = requests.get(r'https://www.gov.br/aneel/pt-br/assuntos/tarifas/bandeiras-tarifarias', headers= Cabecalho)
Dados_Texto = Dados.text
Dados_retirados = BeautifulSoup(Dados_Texto, 'html.parser')
Dados_filtrados = Dados_retirados.find_all('div', {'id': 'parent-fieldname-text'})[0]#.contents[3]
Dados_filtrados = Dados_retirados.find_all('div', {'id': 'parent-fieldname-text'})[0].contents[14]


verde = str(Dados_retirados.find_all('div', {'id': 'parent-fieldname-text'})[0].contents[14].contents[1]).replace('<li>', '').replace('</li>','').replace("</strong>",'').replace('<strong>','')
#---------------------------------- FIM WEB SCREPPING---------------------------------#

#-----------------------------------AMARELO-------------------------------------------#
amarelo = str(Dados_retirados.find_all('div', {'id': 'parent-fieldname-text'})[0].contents[14].contents[3]).replace('<li>', '').replace('</li>','').replace("</strong>",'').replace('<strong>','')
amareloPrice = (amarelo[amarelo.find("R$")+2:95]).replace(",",".").strip()

#print(amareloPrice)

select = conn.cursor()
UpDateAmarelo= ("UPDATE DBO.BandeirasTarifarias SET valor_incremento = {0} WHERE bandeira = 'AMARELA'".format(amareloPrice))
select.execute(UpDateAmarelo)

#-----------------------------------VERMELHO1-------------------------------------------#
vermelho1 = str(Dados_retirados.find_all('div', {'id': 'parent-fieldname-text'})[0].contents[14].contents[5]).replace('<li>', '').replace('</li>','').replace("</strong>",'').replace('<strong>','')
vermelho1Price = (vermelho1[vermelho1.find("R$")+2:105]).replace(",",".").strip()

UpDateVermelho1= ("UPDATE DBO.BandeirasTarifarias SET valor_incremento = {0} WHERE bandeira = 'VERMELHA 1'".format(vermelho1Price))
select.execute(UpDateVermelho1)


#-----------------------------------VERMELHO2-------------------------------------------#
vermelho2 = str(Dados_retirados.find_all('div', {'id': 'parent-fieldname-text'})[0].contents[14].contents[7]).replace('<li>', '').replace('</li>','').replace("</strong>",'').replace('<strong>','')
vermelho2Price = (vermelho2[vermelho2.find("R$")+2:110]).replace(",",".").strip()

UpDateVermelho2= ("UPDATE DBO.BandeirasTarifarias SET valor_incremento = {0} WHERE bandeira = 'VERMELHA 2'".format(vermelho2Price))
select.execute(UpDateVermelho2)

dataAll = select.execute("SELECT * FROM DBO.BandeirasTarifarias").fetchall()
print(dataAll)