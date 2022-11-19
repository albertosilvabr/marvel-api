## Prática com a API da Marvel.

### Tópicos

- [Objetivo](https://github.com/albertosilvabr/marvel-api#objetivo)
- [Contexto da solução](https://github.com/albertosilvabr/marvel-api#contexto-da-solu%C3%A7%C3%A3o)
- [Desenho arquitetural da solução](https://github.com/albertosilvabr/marvel-api#desenho-arquitetural-da-solu%C3%A7%C3%A3o)
- [Pré-requisitos](https://github.com/albertosilvabr/marvel-api#pr%C3%A9-requisitos)
- [Passos para subir os serviços necessários para o teste](https://github.com/albertosilvabr/marvel-api#passos-para-subir-os-servi%C3%A7os-necess%C3%A1rios-para-o-teste)

### Objetivo

Utilizar a API da Marvel para buscar todos os Comics e Characters.


### Contexto da solução

Consiste em criar dois serviços em Docker:

- Container da linguagem de programação Python para conectar com API 
para buscar e processar os dados requisitados
- Container do banco de dados MySQL para salvar os dados processados

### Desenho arquitetural da solução

<div align="center">
        <img src="https://user-images.githubusercontent.com/16995695/202827451-febbd954-b8c8-499a-a80f-b4fabe330f9d.png" />
</div>


### Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/)
- [Docker-Compose](https://docs.docker.com/compose/gettingstarted/)
- [Public key e Private key](https://developer.marvel.com/account)

### Passos para subir os serviços necessários para o teste

1. Clonando o repositório

```sh
$ git clone https://github.com/albertosilvabr/marvel-api.git
```

2. Iniciando os serviçes do MySQL e Python

```sh
$ cd marvel-api
$ make start-services
```
3. Check se os serviços foram iniciandos
```sh
$ docker ps

output:
CONTAINER ID   IMAGE               COMMAND                  CREATED          STATUS      PORTS                   NAMES
d772b479a064   marvel-api_python   "python3"                14 minutes ago   Up 14 min.                          python
f6f37f692661   mysql:latest        "docker-entrypoint.s…"   14 minutes ago   Up 14 min.  0.0.0.0:3306->3306/tcp  mysql
```

4. Buscar os dados de Characters e Comics  

```sh
$ make get-data-marvel-api
```

Neste passo será solicitado a public key e private key necessárias para requisitar os dados via API. Veja como consegui-las em: (https://developer.marvel.com/account)

```sh
Entre com sua public key:
```

Após informar a public key e private key, as seguintes etapas serão executadas 

```sh
Step 1: Criando tabelas Characters e Comics
        Tabelas criadas com sucecesso!

Step 2: Buscando dados de Characters
        Busca realizada com sucesso!

Step 3:  Buscando dados de Comics
         Busca realizada com sucesso!

Step 4: Criando a tabela OBT
        Tabela OBT criada com sucesso!


Processo finalizado com sucesso!
```

3. Consultando os dados salvosdas tabelas criadas no banco MySQL através do MySQL CLI

- Acessa o container do banco MySQL
```sh
$ make mysql-cli 
```

- Login para executar query via linha de comando, informe este password **rootpass** quando solicitado 
```sh
bash-4.4# mysql -u root -p
Enter password:
```

- Lista os bancos de dados
```sh
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| marveldb           |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.00 sec)
```

- Seleciona o banco de dados **marveldb**
```sh
mysql> USE marveldb;
```

- Consultando os dados da tabela Characters;
```sh
mysql> SELECT id, name FROM characters LIMIT 4;
+---------+--------------+
| id      | name         |
+---------+--------------+
| 1011334 | 3-D Man      |
| 1017100 | A-Bomb (HAS) |
| 1009144 | A.I.M.       |
| 1010699 | Aaron Stack  |
+---------+--------------+
4 rows in set (0.00 sec)
```

- Consultando os dados da tabela Comics;
```sh
mysql> SELECT id, title FROM comics LIMIT 4;
+-------+--------------------------+
| id    | title                    |
+-------+--------------------------+
| 82967 | Marvel Previews (2017)   |
| 82965 | Marvel Previews (2017)   |
| 82970 | Marvel Previews (2017)   |
| 37504 | Marvels Vol. 1 (1994) #7 |
+-------+--------------------------+
4 rows in set (0.00 sec)

```

- Consultando os dados da tabela OBT
```sh
mysql> SELECT character_id
            , MID(character_description,1,30) AS character_description
            , comic_id
            , MID(title_comic,1,30) AS title_comic 
            , format_comic 
         FROM  obt_marvel LIMIT 2;
+--------------+-----------------------+----------+----------------------+------------------------+
| character_id | character_description | comic_id | title_comic          | format_comic           |
+--------------+-----------------------+----------+----------------------+------------------------+
|      1009144 | AIM is a terrorist o  |   103371 | Avengers Unlimited I | Digital Vertical Comic |
|      1009368 | Wounded, captured an  |   103371 | Avengers Unlimited I | Digital Vertical Comic |
+--------------+-----------------------+----------+----------------------+------------------------+
2 rows in set (0.00 sec)
```
