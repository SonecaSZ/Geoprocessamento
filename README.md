👨‍💻 Autor

Desenvolvido por *Raul Ferreira de Aguiar Junior*
RGM: *30590388*
🗺️ Projeto: Persistência Poliglota e Geoprocessamento (AV1)

Este projeto implementa uma solução de *Persistência Poliglota*, combinando:  
- *SQLite* → dados estruturados (Estados e Cidades).  
- *MongoDB Atlas* → dados geoespaciais (Locais e Pontos Turísticos).  
- *Streamlit* → interface interativa e visualização em mapa.  

🔎 O sistema realiza operações de *geoprocessamento*, como cálculo de distância entre coordenadas e busca de pontos de interesse por proximidade.

⚙️ Tecnologias Utilizadas

| Categoria | Tecnologia | Função |
|-----------|------------|--------|
| *Interface*| [Streamlit](https://streamlit.io/) | Dashboard interativo para cadastro e visualização no mapa |
| *Banco Relacional* | [SQLite3](https://www.sqlite.org/) | Armazenamento de dados estruturados (Estados e Cidades) |
| *Banco NoSQL* | [MongoDB Atlas](https://www.mongodb.com/atlas) | Armazenamento de documentos JSON com coordenadas geográficas |
| *Geoprocessamento* | [Haversine (Python)](https://pypi.org/project/haversine/) | Cálculo de distâncias entre coordenadas em KM |

---

🚀 Como Executar o Projeto

🔧 1. Pré-requisitos
- [Python 3.10+](https://www.python.org/downloads/) instalado.
- Conta configurada no [MongoDB Atlas](https://www.mongodb.com/atlas).

📦 2. Instalação de Dependências

No terminal, dentro da pasta do projeto:

```bash
pip install -r requirements.txt
```

🌍 3. Configuração do MongoDB Atlas

Defina a variável de ambiente `MONGO_URI` com sua string de conexão:  

| Sistema Operacional | Comando |
|----------------------|---------|
| *Windows (PowerShell)* | `$env:MONGO_URI='SUA_URI_COMPLETA'` |
| *Linux/macOS* | `export MONGO_URI='SUA_URI_COMPLETA'` |

⚠️ *Importante:* substitua `SUA_URI_COMPLETA` pela string real fornecida pelo Atlas.

---

▶️ 4. Executando a Aplicação

No mesmo terminal onde a variável de ambiente foi definida, rode:

```bash
streamlit run app.py
```

A aplicação abrirá em:  
👉 [http://localhost:8501](http://localhost:8501)


📚 Documentação

Para explicação detalhada da arquitetura, exemplos de consultas e capturas da interface, consulte:  

📄 *[DOCUMENTACAO.md](DOCUMENTACAO.md)*


