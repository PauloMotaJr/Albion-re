# Albion Market & Craft - Fase 1: Infraestrutura

## Visão Geral

Esta é a **Fase 1** do projeto, focada em estabelecer uma infraestrutura sólida com Django + PostgreSQL + Docker Compose.

### Escopo Atual (Fase 1)

- ✅ Django modular monolítico
- ✅ PostgreSQL com volumes persistentes
- ✅ Docker Compose único (web + db)
- ✅ Página inicial funcional
- ✅ Configuração via variáveis de ambiente
- ⏳ **Não implementado:** collector, worker, Nginx, autenticação, modelos de negócio

## Inicialização Rápida

### 1. Clonar e configurar ambiente

```bash
git clone <url-do-repositorio>
cd albion_market_craft

# Criar arquivo .env a partir do template
cp .env.example .env

# Substituir valores sensíveis em .env:
#   - DB_PASSWORD (gerar senha forte)
#   - DJANGO_SECRET_KEY (gerar com comando abaixo)
python -c "import secrets; print(secrets.token_urlsafe(50))" > secret_key.txt
```

### 2. Build e inicialização dos containers

```bash
# Build + start dos serviços web + db
docker-compose up --build -d web db

# Verificar logs do banco para confirmar conexão
docker-compose logs db | grep "database ready"

# Acessar aplicação via browser:
#   http://127.0.0.1:8000 (porta exposta apenas em localhost)
```

### 3. Executar migrações Django (apenas uma vez)

```bash
docker-compose exec web python manage.py migrate --no-input

# Verificar migrations concluídas
docker-compose exec web python manage.py showmigrations
```

## Estrutura do Projeto

```
albion_market_craft/
├── docker-compose.yaml        # Definição dos serviços (web + db)
├── Dockerfile                 # Imagem Python otimizada para todos os containers
├── requirements.txt           # Dependências Python
├── .env.example               # Template de variáveis ambiente (versionado)
├── .gitignore                 # Git ignore para não commitar sensíveis
├── .dockerignore              # Exclusões no build Docker
├── README.md                  # Este arquivo (documentação)
├── manage.py                  # Django management script
├── albionmarket/              # Aplicação Django principal
│   ├── __init__.py
│   ├── settings/base.py       # Configuração base (carregada via env)
│   ├── urls.py                # URLs principais (redireciona para home)
│   ├── wsgi.py               # WSGI handler padrão Django
│   └── asgi.py               # ASGI handler padrão Django
├── templates/                 # Templates HTML
│   ├── base.html             # Template base com links staticfiles
│   └── home.html             # Página inicial (renderizada por views/home.py)
```

## Variáveis de Ambiente Principais

| Variável | Descrição | Valor Padrão (.env.example) |
|----------|-----------|------------------------------|
| `DB_NAME` | Nome do banco PostgreSQL | `albion_market` |
| `DB_USER` | Usuário do banco | `albin_user` |
| `DB_PASSWORD` | Senha do usuário (gerar forte!) | `changeme_secure_password_123` |
| `DJANGO_SECRET_KEY` | Chave secreta Django (**NÃO** incluir credenciais reais) | Gera via comando Python |
| `DJANGO_DEBUG` | Ativar modo debug Django | `True` (desativar em produção!) |
| `LOG_LEVEL` | Nível de logging | `INFO` |

### Como gerar valores seguros para produção:

```bash
# Senha forte para banco de dados
python -c "import secrets; print(secrets.token_urlsafe(32))" > .env.db_password.txt

# Chave secreta Django
python -c "import secrets; print(secrets.token_urlsafe(64))" > .env.secret_key.txt
```

## Comandos Úteis

### Inicialização desenvolvimento (web + db)

```bash
docker-compose up --build -d web db
```

### Verificar logs do banco de dados

```bash
docker-compose logs db | grep -i "ready\|error"
```

### Executar shell no container web

```bash
docker-compose exec web python manage.py shell
```

### Rodar migrations Django (apenas uma vez após mudar schema)

```bash
docker-compose exec web python manage.py migrate --no-input
```

### Reset do banco de dados (cuidado: apaga todos os dados!)

```bash
# Opção 1: Recriar containers com volume excluído
docker-compose up -d --force-recreate --remove-orphans

# Opção 2: Drop e recriar banco (perde todos os dados existentes)
docker-compose exec db pg_dropdatabase albion_market
docker-compose exec db psql -U albin_user -c "CREATE DATABASE albion_market;" -d postgres
```

## Troubleshooting Básico

### Container web não inicia

```bash
# Verificar logs do container
docker-compose logs web | tail -100

# Verificar se banco está saudável
docker-compose exec db psql -U albin_user -d albion_market -c "SELECT 1"
```

### Migrations Django falharam

```bash
# Reentrar no container e rodar migrations novamente
docker-compose exec web python manage.py migrate --no-input

# Se continuar falhando, verificar erros no log
docker-compose logs web | grep -i "error\|exception"
```

### Acesso ao console Python do banco para troubleshooting

```bash
docker-compose exec db bash
psql -U albin_user -d albion_market -c "SHOW DATABASES;"
```

## Segurança Recomendada

1. **NUNCA** incluir `.env*` com credenciais reais no Git
2. Usar `.env` (sem versionamento) para desenvolvimento e produção
3. Em produção, gerar `DJANGO_SECRET_KEY` forte via comando Python
4. Ativar `DJANGO_DEBUG=False` em produção
5. Não expor container `web` diretamente à internet sem Nginx ou reverse proxy

## Licença

[Inserir licença aqui - por padrão Apache 2.0 ou MIT]