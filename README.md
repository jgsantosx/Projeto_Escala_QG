# 🎖️ Automação de Escala de Serviço - 2º GMAR (V2.0)

Este projeto é uma ferramenta desenvolvida em Python para automatizar a geração da **Escala de Praia** (Serviço Operacional). O sistema gerencia o ciclo 12x60, processa permutas automaticamente (com validação de regras) e gera um PDF formatado para impressão.

## 🚀 Novidades da Versão 2.4

- **🔄 Sistema de Permutas Inteligente:**
  - O robô lê o arquivo `permutas.xlsx` e substitui o titular pelo substituto.
  - **Multi-pass:** Aceita permutas em qualquer ordem no Excel (resolve trocas "casadas").
  - **O Juiz:** Valida se os militares existem e aplica regras de negócio (ex: alerta troca na mesma Ala).
- **🧠 Distribuição Híbrida:**
  - **Prioridade VIP:** Postos críticos (ex: Posto 3, Quebra Mar) são garantidos primeiro.
  - **Ordem Geográfica:** O restante do efetivo é distribuído seguindo a ordem natural da praia (Joatinga -> Ilhas).
- **🔢 Efetivo Flexível:** Controle total sobre quantos militares vão em cada posto (1, 2, 3...) via configuração.

## 🛠️ Funcionalidades Principais

- **Ciclo Automático:** Calcula a Ala de serviço (A, B ou C) baseado na data.
- **Geração de PDF:** Layout visual com duas colunas, seguindo o padrão operacional.
- **Alertas de Erro:** Avisa no terminal se uma permuta falhar ou se faltar efetivo.

## 📂 Estrutura de Arquivos

````text
Projeto_Escala_QG/
│
├── inputs/
│   ├── efetivo.xlsx        # Colunas: Nome_Guerra, Ala
│   └── permutas.xlsx       # Colunas: Data, Sai_Nome, Entra_Nome (NOVO!)
│
├── outputs/
│   └── escala_praia_FINAL.pdf  # O resultado gerado
│
├── gerador_escala.py       # Motor Lógico (V2.4)
├── README.md               # Documentação
└── .gitignore              # Arquivos ignorados
⚙️ Como Configurar
1. Instalação
Necessário Python 3.x e as bibliotecas:

Bash

pip install pandas openpyxl fpdf
2. Preparando a Escala
Efetivo: Atualize o inputs/efetivo.xlsx com a tropa atual.

Permutas: Se houver trocas, preencha inputs/permutas.xlsx.

Formato da Data: YYYY-MM-DD (Ex: 2025-12-01).

Nomes: Devem ser idênticos aos do arquivo de efetivo.

Regras: No arquivo gerador_escala.py, você pode editar:

lista_prioridade_alta: Postos que furam a fila.

config_postos: Quantidade de vagas por posto e ordem visual.

▶️ Como Rodar
Execute o script no terminal:

Bash

python gerador_escala.py
O robô informará no terminal as trocas realizadas e gerará o PDF na pasta outputs/.

🚧 Próximos Passos (Roadmap)
[ ] Cabeçalho Completo: Adicionar escala de Oficiais, Motoristas e Prontidão (Parte superior do PDF).

[ ] Interface Gráfica (GUI): Criar janelas para facilitar o uso por outros militares.

[ ] Versão 3.0 (Futuro): Implementar "Distribuição por Antiguidade".

Criar lógica onde militares de maior patente têm prioridade nos postos principais.

Desenvolvido para automação administrativa militar.


---

### 2. Arquivo `.gitignore` (Confirmação)
Só para garantir que está igual ao que combinamos (esse arquivo não precisa mexer se já estiver lá):

```text
# Ignorar arquivos temporários do Python
__pycache__/
*.py[cod]

# Ignorar arquivos gerados (Outputs)
outputs/*.pdf
outputs/*.xlsx

# Ignorar arquivos de sistema
.DS_Store
Thumbs.db

# Opcional: Ignorar credenciais
credentials/*.json
token.json
````
