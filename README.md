# Backend

# 1. Passo a Passo para Configuração e Instalação de Dependências

###### Clonar o Projeto

```bash
git clone git@github.com:GaropaBus/garopabus-backend.git
cd garopabus-backend
```

## 2. Criar e Ativar o Ambiente Virtual (Virtualenv)

### No Linux/MacOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### No Windows:

```bash
python -m venv venv
venv\Scripts\activat
```

## 3. Instalar as Dependências

Com o ambiente virtual ativado, instale as dependências do projeto usando o arquivo `pyproject.toml`

```bash
pip install -e .
```

Este comando instala todas as dependências listadas no `pyproject.toml` e prepara o projeto para ser usado no ambiente virtual.

## 4. Adicionar Novas Dependências

### A) Para Adicionar uma Nova Dependência ao Projeto:

1. **Instale a Dependência com `pip`:**

   Primeiro, instale a dependência desejada (por exemplo, `requests`):

   ```bash
   pip install requests
   ```
   ```bash
   pip freeze
   ```
   Ira instalar e listar as dependecias instaladas e sua respectiva versão
2. **Adicionar ao Arquivo `pyproject.toml`:**

   Após a instalação, adicione a dependência no seu arquivo `pyproject.toml` na seção `[project] > dependencies`:

   Exemplo:

   ```toml
   dependencies = [
       "requests==2.32.3",
       "aiohttp==3.10.5",
       # outras dependências
   ]
   ```
