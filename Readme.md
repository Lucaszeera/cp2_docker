# Fichas de pacientes
<br>

### Arquitetura do projeto: 

![Imagem da arquitetura](https://github.com/Lucaszeera/cp2_docker/blob/main/img/_arquitetura.jpeg?raw=true)

## **Primeiramente você deve ter em sua máquina**

* Python 3.9    https://www.python.org/downloads/release/python-390/
* Flask 2.0.2   https://pypi.org/project/Flask/
* Docker        https://www.docker.com/products/docker-desktop/
* MariaDB       https://mariadb.org/download/?t=mariadb&p=mariadb&r=11.1.0&os=windows&cpu=x86_64&pkg=msi&m=fder

### após isso, segue os passos para clonagem e execução
1 - Clique no botão verde "< > Code" e copie a url de clonagem.

2 - Crie uma pasta na sua máquina no local de sua preferência

3 - Abra o CMD e entre nesta pasta que você criou

4 - Execute o comando "git clone" e cole a url que você copiou:
```
git clone (url)
```

5 - Entre nessa pasta clonada executando ``cd nomeDaPasta`` e execute o build do composer através desse comando: 
```
docker-compose up -d --build
```

6 - Inicie o docker com o comando:
```
docker-compose start
```
7 - Para executar comandos dentro do container db em execução através de um shell interativo, execute esse comando:
```
docker container exec -it db bash
```

### Agora você pode criar um usuário pelo root

1 - Execute o comando a seguir para se conectar ao servidor de banco de dados como usuario root:
```
mysql -u root -p 
```
2 - Agora para criar o seu login com id e senha execute esse comando:
```
create user 'seuUsuario'@'localhost' identified by 'suaSenha'
```
3 - Agora para garantir que esse usuário tenha acesso sobre as tabelas do banco de dados execute esse comando:
```
grant all on patient * TO 'seuUsuario'@'localhost
```
***Caso esses comandos acima não funcionem diretamente no seu cmd, execute-os pelo terminal do docker**

### após isso, você pode executar o primeiro comando de conexão ao servidor, mas pelo seu usuário

Execute o comando:
```
mysql -u seuUsuario -p 
```
Ele irá pedir sua senha e depois que você informar corretamente, você pode executar os comandos sobre o banco de dados

execute "``use patient``" para acessar o banco de dados

A partir daqui você pode executar todos os comandos de banco de dados como "``select * from patient``"
