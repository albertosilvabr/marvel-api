import hashlib
import time
import re
import requests
from keys import PUBLIC_KEY, PRIVATE_KEY
import mysql.connector
from mysql.connector import Error
from connection_db import *


#Formata as informações do Hash
def getHashAndKeys():
    m = hashlib.md5()
    ts = str(time.time())
    m.update(bytes(ts, 'utf-8')) 
    m.update(bytes(PRIVATE_KEY, 'utf-8'))
    m.update(bytes(PUBLIC_KEY, 'utf-8'))

    dic = {
        "ts": ts,
        "apikey": PUBLIC_KEY, 
        "hash": m.hexdigest()
    }

    return dic

#Checar se banco do MySQL está online
def isOnlineMySQL():
    cnn = accessDB()
    try:       
        cnn.openConnection()
        cnn.closeConnection()
        return True
    except Error as e:
        return False 

#Criar as tabelas de Characters, Comics e OBT
def createTables():

    cnn = accessDB()

    sql = """
            DROP TABLE IF EXISTS characters;
            CREATE TABLE characters (
                    id          bigint(20)   NULL,
                    name        varchar(100) NULL,
                    description MEDIUMTEXT   NULL,
                    modified    varchar(50)  NULL,
                    resourceuri varchar(100) NULL 
            ) ;       
    """
    cnn.executeDDL(sql)

    sql = """
            DROP TABLE IF EXISTS comics;
            CREATE TABLE comics (
                    id                 bigint(20)   NULL,
                    digitalid          bigint(20)   NULL,
                    title              varchar(999) NULL,
                    issuenumber        int          NULL,
                    variantgescription varchar(999) NULL,
                    description        MEDIUMTEXT   NULL,
                    modified           varchar(50)  NULL,
                    diamondcode        varchar(100) NULL,        
                    isbn               varchar(100) NULL,
                    upc                varchar(100) NULL,
                    ean                varchar(100) NULL,
                    issn               varchar(100) NULL,        
                    formatt            varchar(50)  NULL,
                    pagecount          INT          NULL,
                    resourceuri        varchar(100) NULL,
                    characterId        bigint(20)   NULL,
                    charactername      varchar(100) NULL

            );      
        """
    cnn.executeDDL(sql)

    sql = """
            DROP TABLE IF EXISTS obt_marvel;
            CREATE TABLE obt_marvel (
                    character_id           bigint(20) NULL,
                    character_name         varchar(100) NULL,
                    character_description  mediumtext,
                    character_modified     varchar(50) NULL,
                    comic_id               bigint(20) NULL,
                    title_comic            varchar(100) NULL,
                    format_comic           varchar(50) NULL  
            ); 
        """

    cnn.executeDDL(sql)    

#Tratar alguns caracteres com podem ocasionar erros ao inserir dados no banco MySQL
def resolveSpecialString(s):
    if s is None:
        return ""
    if s is not None or s != "" or s is not None:
        return s.replace('\"','\\"') \
                .replace('\r','') 
                #.replace('File','') \
                #.replace('Dogs','') 

#Pegar os dados de Characters
def getCharactersAPI():

    limit = 100
    offset = 0
    interactions = range(10)

    ts = str(time.time())
    key_api_marvel = (ts + PRIVATE_KEY + PUBLIC_KEY).encode("UTF-8")
    hash = hashlib.md5(key_api_marvel).hexdigest()

    for n in interactions:

        #Requisição para API da Marvel - Characters
        parameters = f"ts={ts}&limit={limit}&offset={offset}&apikey={PUBLIC_KEY}&hash={hash}"
        url = f"https://gateway.marvel.com/v1/public/characters?{parameters}"
        characters = requests.get(url)

        if characters.status_code == 200:

            cnn = accessDB()
            cnn.openConnection()

            characters = characters.json()
            
            for i in characters["data"]["results"]:

                sql = f"""
                            INSERT INTO characters 
                                    (id,
                                        name, 
                                        description, 
                                        modified, 
                                        resourceuri) 
                                VALUES 
                                        ({i['id']}, 
                                         "{resolveSpecialString(i['name'])}", 
                                        "{resolveSpecialString(i['description'])}", 
                                        '{i['modified']}', 
                                        '{i['resourceURI']}')  
                """

                cnn.executeDML(sql)

            offset += limit

            cnn.closeConnection()    

#Pegar os dados dos itens Characters aninhado em Comics
def getCharactersInComicsItems(i, sql):

    _sql = ""
    _index = 0
    _count = i["characters"]["returned"]

    if _count == 0:
       _sql =  sql.replace("<@param1>", "0").replace("<@param2>", "") 
       return _sql 

    for items in i["characters"]["items"]:
        _index += 1
        charId = re.search(r'/characters/(\d+)', items['resourceURI']) 
        _sql+=  sql.replace("<@param1>", charId[1]) \
                    .replace("<@param2>", items['name']) 
        if _index < _count:
             _sql+=  ","  

    return _sql 

#Pegar os dados de Comics
def getComicsAPI():

    limit = 100
    offset = 0
    interactions = range(10)

    ts = str(time.time())
    key_api_marvel = (ts + PRIVATE_KEY + PUBLIC_KEY).encode("UTF-8")
    hash = hashlib.md5(key_api_marvel).hexdigest()

    for n in interactions:

        #Requisição para API da Marvel - Comics
        parameters = f"ts={ts}&limit={limit}&offset={offset}&apikey={PUBLIC_KEY}&hash={hash}"
        url = f"https://gateway.marvel.com:443/v1/public/comics?{parameters}"
        comics = requests.get(url)

        if comics.status_code == 200:

            cnn = accessDB()
            cnn.openConnection()

            comics = comics.json()

            for i in comics["data"]["results"]: 
                sql = f"""
                            (  
                                {i['id']}, 
                                {i['digitalId']},
                                "{resolveSpecialString(i['title'])}", 
                                {i['issueNumber']},
                                "{i['variantDescription']}", 
                                "{resolveSpecialString(i['description'])}", 
                                '{i['modified']}', 
                                '{i['diamondCode']}', 
                                '{i['isbn']}', 
                                '{i['upc']}', 
                                '{i['ean']}', 
                                '{i['issn']}', 
                                '{i['format']}', 
                                {i['pageCount']}, 
                                '{i['resourceURI']}'
                                ,<@param1>
                                ,"<@param2>"
                            )     
                        """

                sql = getCharactersInComicsItems(i, sql)
                
                sql = f"""
                            INSERT INTO comics
                                    (id, 
                                    digitalid, 
                                    title, 
                                    issuenumber, 
                                    variantgescription, 
                                    description, 
                                    modified, 
                                    diamondcode, 
                                    isbn, 
                                    upc, 
                                    ean, 
                                    issn, 
                                    formatt, 
                                    pagecount, 
                                    resourceuri, 
                                    characterId, 
                                    charactername)
                            VALUES   {sql}         
                        """        
                cnn.executeDML(sql)

            offset += limit

            cnn.closeConnection()

#Agregar os dados na tabels OBT
def aggregateCharactersAndComics():
    cnn = accessDB()
    cnn.openConnection()
    sql = """

            INSERT  INTO obt_marvel
            SELECT ch.id          AS character_Id
                , ch.name        AS character_name
                , ch.description AS character_description
                , ch.modified    AS character_modified
                , c.id           AS comic_id
                , c.title        AS title_comic
                , c.formatt 
            FROM `characters` ch INNER JOIN comics c ON ch.id = c.characterId 
            WHERE c.id = 103371
            GROUP BY ch.id 
                , ch.name
                , ch.description
                , ch.modified
                , c.id 
                , c.title
                , c.formatt      

        """
    cnn.executeDML(sql)
    cnn.closeConnection()

def main():

    
    print("\n")
    print("Olá usuário!")
    print("\n")

    PUBLIC_KEY = input("Entre com sua public key: ")
    PRIVATE_KEY = input("Entre com sua private key: ")
    print("\n\n\n")

    print("[Aguarde a finalização das etapas de capitura e processamento dos dados]") 
    print("\n")

    #Inicio das etapas de captura e processamento dos dados
    print("Step 1: Criando tabelas Characters e Comics.")
    createTables()
    print("        Tabelas criadas com sucecesso!\n")
   
    print("Step 2: Buscando dados de Characters.")
    getCharactersAPI()
    print("        Busca realizada com sucesso!\n")

    print("Step 3:  Buscando dados de Comics.")
    getComicsAPI()
    print("         Busca realizada com sucesso!\n")

    print("Step 4: Criando a tabela OBT.")
    aggregateCharactersAndComics()
    print("        Tabela OBT criada com sucesso!\n\n")    

    print("Processo finalizado com sucesso!\n")

if __name__ == "__main__":

    if isOnlineMySQL() == True:
        main()
    else:
        print("O container do banco MySQL não está online.")