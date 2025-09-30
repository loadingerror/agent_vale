# ChallangeAgentsAi

O desafio consiste em: "Desenvolver um mini‑assistente conversacional (RAG‑based) que orquestra múltiplas tools via LangChain + LangGraph e oferece interface gráfica para o usuário final".

[![python](https://img.shields.io/badge/python-3.12%2B-blue.svg)](./)

## Sumário
- [Visão Geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Uso](#uso)
- [Configuração](#configuração)
- [Estrutura do Repositório](#estrutura-do-repositório)
- [Qualidade & Testes](#qualidade--testes)
- [Contato](#contato)

## Visão Geral
O projeto consiste em uma criação de um asisstente conversacional que utiliza o modelo LangChain com uma interface gráfica simplificada para o ussuário final. Apesar de haver uma lista de requisitos obrigatórios, por nao concordar com algumas práticas nem todos os requisitos foram atendidos da maneira solicitada. </br>

Pontos a serem considerados: </br>
Definição de Contexto RAG</br>
- O fluxo entre ferramentas (tools) e o RAG não está documentado. É necessário esclarecer como os dois componentes se integram e qual a lógica de orquestração envolvida.

Estrutura de Pastas vs. Imports em Python</br>
- A justificativa para a estrutura de diretórios não foi apresentada. Atualmente, ela pode conflitar com o mecanismo de import do Python (ex.: ModuleNotFoundError). Sugere-se documentar a convenção adotada ou reestruturar.

Terminologia não padronizada</br>
- Foram utilizados termos próprios que não aparecem nos documentos oficiais do framework escolhido. É importante alinhar nomenclatura com a terminologia oficial para evitar ambiguidades.

Objetos indefinidos</br>
- Alguns objetos foram mencionados/instanciados sem definição clara (interfaces, contratos ou diagramas). É preciso detalhar responsabilidades e formato esperado.

Regras de qualidade de código</br>
- Não há definição de padrões como PEP8, por exemplo. Um guia de estilo e um pre-commit configurado ajudariam a garantir consistência.

- Uso de terminologia interna não explicada</br>
Conceitos como “fallback para tool” foram introduzidos sem explicação. Requer documentação de quando e como esses mecanismos devem ser aplicados.

Limitações de embeddings</br>
- A dependência de embeddings específicos pode limitar o uso de modelos alternativos ou aumentar custos. Esse ponto deveria estar registrado nos pré-requisitos e na análise de trade-offs.

Critérios de escalabilidade</br>
- A arquitetura não define requisitos de escalabilidade (ex.: uso de async/await, aiohttp, filas, workers). Esses aspectos precisam ser considerados para ambientes produtivos.

## Arquitetura
Explique em alto nível (pode incluir um diagrama no futuro).

## Requisitos
- Python 3.12.3
- Docker 
- 


## Instalação
```bash
git clone https://github.com/<org>/<repo>.git
cd <repo>
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Uso


## Estrutura do Repositório
```bash
.
├── app/               # núcleo do app 
├── graph/             # grafos do LangGraph 
├── tools/             # integrações/tools 
├── ui/                # frontend (Streamlit) e assets da interface
├── vector_db/         # RAG: scripts de ingestão, esquemas, migrações, seeds, utils
├── tests/             # testes unitários
├── requirements.txt   # dependências do projeto
└── README.md          # visão geral, setup e instruções
```

## Contato
Marina
marinaslferreira@gmail.com 



