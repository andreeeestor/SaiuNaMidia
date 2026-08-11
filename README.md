# SaiuNaMídia - COPASA

O **SaiuNaMídia** é uma aplicação web desenvolvida exclusivamente para apoiar e otimizar o fluxo de trabalho do setor de publicidade da **COPASA**.

A plataforma funciona como um explorador e repositório de arquivos focado em mídia (imagens, banners e peças publicitárias), fornecendo uma interface rica, leve e intuitiva (estilo **Google Drive / Finder**), permitindo o armazenamento na nuvem, organização por pastas, geração/compartilhamento imediato de URLs e **extração inteligente de mídias via IA**.

---

## 📌 Motivação e Arquitetura (Migração Vanilla JS)

Originalmente estruturado em **Next.js**, o projeto foi reformulado para **HTML5, CSS3 e JavaScript puro (Vanilla)** (`template/index.html`).

### Por que a mudança?
- **Integração com o Portal WCM HCL da COPASA:** A arquitetura baseada em Web Standards puros permite incorporar facilmente os componentes, folhas de estilo e scripts diretamente como portlets e blocos de conteúdo no sistema de gerenciamento de conteúdo institucional (**HCL Digital Experience / WCM**), sem overhead de build ou dependências de runtime de frameworks.
- **Alta Performance e Baixo Acoplamento:** Carregamento ultra-rápido, sem bundlers complexos no frontend.

---

## 🚀 Principais Funcionalidades

- **Dashboard Estilo Explorer (Clone Drive/Finder):** Modos de visualização em Grid (Grade) e List (Lista).
- **Aba "Extrator IA":** Extração automática da **imagem principal da matéria** e da **logo do portal de notícias** a partir de uma URL informada.
- **Hospedagem em Nuvem via Cloudinary:** Upload direto para o Cloudinary com geração automática de URLs otimizadas para cópia e compartilhamento imediato.
- **Navegação por Pastas:** Estrutura em árvore ilimitada com suporte a navegação em migalhas de pão (*Breadcrumb*).
- **Visualização Rápida (Lightbox):** Pré-visualização com um único clique e funcionalidade de cópia de link direto em 1 clique.
- **Ações em Lote e Seleção Múltipla:** Caixas de seleção para exclusão e movimentação em lote paralelas.
- **Menu de Contexto (Right-click):** Acesso rápido a ações (copiar URL, visualizar, mover e deletar).
- **Design System COPASA:** Interface responsiva, limpa e alinhada à identidade da companhia.

---

## 🛠️ Tecnologias Utilizadas

### Frontend
- **HTML5 & CSS3 Vanilla:** Variáveis CSS nativas e layout responsivo com Flexbox/Grid.
- **JavaScript ES6+:** Manipulação assíncrona com `fetch` e `Promise.all`, com deleção e movimentação em lote paralelas.

### Backend & Serviços
- **Python (>= 3.12):** FastAPI / Uvicorn para gestão da API de dados, rotas de upload e IA.
- **Gerenciador de Pacotes:** `uv` (Fast Python package installer).
- **Cloudinary:** Serviço em nuvem para hospedagem das imagens, armazenamento seguro e geração de URLs de entrega de alta disponibilidade.
- **Groq API & Llama 3.1 8B Instant:** Processamento leve e ultra-rápido para extração de mídias e logos em matérias jornalísticas.

---

## 🤖 Extrator IA (Groq & Llama 3.1 8B)

A aplicação conta com uma aba dedicada de **Extrator IA**:

- **Modelo utilizado:** `llama-3.1-8b-instant` (modelo leve, econômico e de altíssima velocidade hospedado no Groq).
- **Funcionamento:**
  1. O usuário cola a URL da matéria de jornal/portal.
  2. O backend faz o download e parse das tags HTML e OpenGraph (`og:image`, `logo`, etc.).
  3. O modelo da IA seleciona e retorna a URL exata da **Imagem da Notícia** e a URL da **Logo do Veículo**.

---

## 📦 Como Executar o Projeto Localmente

### Pré-requisitos
- Python 3.12+
- Gerenciador [`uv`](https://github.com/astral-sh/uv)

### Configuração de Variáveis de Ambiente (`.env`)

Crie um arquivo `.env` na raiz do projeto:

```env
# Autenticação
AUTH_USER=lala
AUTH_PASSWORD=querida

# Cloudinary
CLOUDINARY_CLOUD_NAME=seu_cloud_name
CLOUDINARY_API_KEY=sua_api_key
CLOUDINARY_API_SECRET=seu_api_secret

# Groq AI (Opcional - usa modelo leve llama-3.1-8b-instant)
GROQ_API_KEY=sua_groq_api_key
```

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd saiunamidia
   ```

2. **Sincronize/Instale as dependências com `uv`:**
   ```bash
   uv sync
   ```

3. **Inicie o servidor de desenvolvimento:**
   ```bash
   uv run python main.py
   ```

4. **Acesse a aplicação:**
   Abra `http://localhost:8000` no seu navegador.

---

*Desenvolvido para facilitar e otimizar o dia a dia da Publicidade da COPASA.*
