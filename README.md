# 🎖️ Automação de Escala de Serviço - 2º GMAR (V3.2)

Ferramenta desenvolvida em Python para automatizar a geração da **Escala de Praia** (Serviço Operacional). O sistema gerencia o ciclo 12x60, processa permutas, respeita qualificações (OF, SGT, MOT, GV) e gera PDFs formatados.

## 🚀 Novidades da Versão 3.2

- **🎮 Menu Interativo:** Ao iniciar, o sistema pergunta:
  - _Data Inicial:_ Você escolhe quando começar.
  - _Quantidade:_ Você define quantos dias gerar (1 dia, 1 semana, etc.).
- **👮 Distribuição por Qualificação:**
  - O robô lê a coluna `Qualificacao` no Excel.
  - Só escala Oficiais para chefia, Motoristas para viaturas e GVs para a praia.
  - Se faltar especialista, alerta no PDF (`FALTA MOT`).
- **✨ Visual Limpo:** Removeu prefixos repetitivos (ex: "GV") do PDF, mantendo apenas a graduação e nome.

## 🛠️ Funcionalidades

- **Ciclo Automático:** Calcula a Ala (A, B, C) baseado na data escolhida.
- **Permutas Inteligentes:** Resolve trocas "casadas" (A substitui B, C substitui A) automaticamente.
- **Layout Oficial:** PDF centralizado, com cabeçalho de Serviço Interno e rodapé de alterações.

## 📂 Estrutura de Arquivos

```text
Projeto_Escala_QG/
│
├── inputs/
│   ├── efetivo.xlsx        # Colunas: Nome_Guerra, Ala, Qualificacao (NOVO!)
│   └── permutas.xlsx       # Colunas: Data, Sai_Nome, Entra_Nome
│
├── outputs/
│   └── Escala_DD-MM-AAAA.pdf  # Arquivos gerados
│
├── gerador_escala.py       # Motor Lógico V3.2
├── GeradorEscalaGMAR.exe   # Executável (Opcional)
└── README.md               # Documentação
⚙️ Como Configurar
1. Excel de Efetivo (inputs/efetivo.xlsx)
Deve conter a coluna Qualificacao com as siglas:

OF: Oficiais

SGT: Sargentos/Subtenentes

MOT: Motoristas

COM: Comunicação

GV: Guarda-Vidas (Padrão)

2. Regras de Negócio (gerador_escala.py)
No início do código, você pode ajustar:

config_interno e config_praia: Quantidade e Requisito (Req) de cada posto.

lista_prioridade_alta: Postos que são preenchidos primeiro.

▶️ Como Rodar
Execute o script ou o .exe.

Responda as perguntas no terminal:

>> Data de Início [Enter para HOJE]: >> Quantos dias gerar? [Enter para 1]:

Pegue seu PDF na pasta outputs.

Desenvolvido para automação administrativa militar.
```
