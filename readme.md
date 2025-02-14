# 🚀 CodeBanAPI

Este projeto é uma API de um projeto de kanban com **FastAPI** e hospedada na **Vercel** utilizando banco de dados hospedado na MongoDB.

Caso tente a importação do projeto para uso próprio é necessário mudar/criar uma collection no MongoDB

## 📌 Requisitos

Antes de executar o projeto, certifique-se de ter instalado:

- [Python 3.8+](https://www.python.org/downloads/)
- [Pip](https://pip.pypa.io/en/stable/installation/)

## 🔧 Instalação

Clone o repositório:

```sh
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

Crie um ambiente virtual (opcional, mas recomendado):
```sh
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

Instale as dependências:
```sh
pip install -r requirements.txt
```
▶️ Executando a API Localmente
Para iniciar a API localmente, execute:
```sh
uvicorn api:app --reload
```
A API estará disponível em:
```sh
http://127.0.0.1:8000
```

- [Documentação da API](https://apicodeban.vercel.app/docs)