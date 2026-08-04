# 🚀 HubCleaner AI

> **Automação, Higienização de Dados e Inteligência Artificial para Gestão Eficiente de Leads.**

O **HubCleaner AI** é uma solução em Python desenvolvida para automatizar a leitura, validação e higienização de bases de dados de leads. Integrando a API do **Google Gemini (LLM)** e **Webhooks do Discord**, a aplicação analisa cadastros, qualifica informações em tempo real e notifica equipes de vendas/operações de forma instantânea.

---

## 📌 Funcionalidades Principais

- 🔄 **Consumo e Higienização de Dados:** Leitura e padronização automática de dados de leads vindos de APIs/CRMs.
- 🧠 **Análise Inteligente com IA:** Utilização do modelo Google Gemini para classificar e enriquecer informações dos leads.
- 🔔 **Notificações em Tempo Real:** Disparo de alertas formatados via Webhook para canais do Discord.
- 🛡️ **Tratamento Robusto de Erros:** Gerenciamento nativo de exceções de API, incluindo suporte a limites de cota (*Rate Limit / HTTP 429*).
- 🧩 **Arquitetura Modular:** Código estruturado de forma desacoplada em serviços reutilizáveis.

---

## 🛠️ Tech Stack

- **Linguagem:** Python 3.10+
- **Inteligência Artificial:** Google Gemini API (google-generativeai)
- **Integrações:** Discord Webhooks (Notificações)
- **Gestão de Variáveis:** python-dotenv
- **Controle de Versão:** Git / GitHub
