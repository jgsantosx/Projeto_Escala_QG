# 🎖️ Automação de Escala de Serviço - 2º GMAR

Este projeto é uma ferramenta desenvolvida em Python para automatizar a geração da **Escala de Praia** (Serviço Operacional). O sistema calcula o ciclo de serviço (12x60), distribui o efetivo disponível baseando-se em regras de prioridade e gera um PDF pronto para impressão.

## 🚀 Funcionalidades

* **Ciclo Automático:** Calcula a Ala de serviço (A, B ou C) baseado na data.
* **Distribuição Inteligente (Híbrida):**
    * *Prioridade Alta (VIP):* Postos críticos são preenchidos primeiro.
    * *Ordem Geográfica:* O restante segue a ordem natural da praia (Joatinga -> Ilhas).
* **Efetivo Variável:** Permite definir quantos militares (1, 2, 3...) cada posto necessita.
* **Geração de PDF:** Cria um arquivo PDF com layout oficial (duas colunas) usando a biblioteca `FPDF`.
* **Entrada de Dados:** Lê o efetivo de um arquivo Excel (`efetivo.xlsx`).

## 🛠️ Tecnologias Utilizadas

* Python 3.x
* **Pandas:** Manipulação de dados e lógica de tabelas.
* **FPDF:** Geração do layout do PDF.
* **OpenPyXL:** Leitura de arquivos Excel.

## 📂 Estrutura do Projeto

```text
Projeto_Escala_QG/
│
├── inputs/
│   └── efetivo.xlsx        # Lista com Nome_Guerra e Ala dos militares
│
├── outputs/
│   └── escala_praia_FINAL.pdf  # O resultado gerado
│
├── gerador_escala.py       # O código fonte principal (Motor Lógico)
├── README.md               # Documentação
└── .gitignore              # Arquivos ignorados pelo Git
⚙️ Como Configurar
1. Pré-requisitos
Certifique-se de ter o Python instalado. Instale as dependências:

Bash

pip install pandas openpyxl fpdf
2. Configurar o Efetivo
Edite o arquivo inputs/efetivo.xlsx. Ele deve conter as colunas:

Nome_Guerra (Ex: Sd Silva)

Ala (A, B ou C)

3. Ajustar Regras de Negócio
No arquivo gerador_escala.py, você pode editar as variáveis no topo:

lista_prioridade_alta: Adicione aqui os postos que devem ser preenchidos primeiro.

config_postos: Define a quantidade de vagas (Qtd) e a ordem visual de impressão.

▶️ Como Rodar
Execute o script principal no terminal:

Bash

python gerador_escala.py
O PDF será gerado na pasta outputs/.

🚧 Próximos Passos (Roadmap)
[ ] Implementar módulo de Permutas (Trocas de serviço).

[ ] Adicionar cabeçalho com escala de Oficiais e Motoristas.

[ ] Interface gráfica simples (GUI).

Desenvolvido para automação administrativa militar.


---

### 2. O Arquivo `.gitignore`
Esse arquivo é crucial. Ele diz para o GitHub: *"Não suba arquivos inúteis, nem arquivos gerados, nem senhas"*.

Crie um arquivo chamado `.gitignore` (sim, começa com ponto e não tem nome antes) e cole isso dentro:

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

# Opcional: Ignorar o efetivo real se tiver dados sensíveis
# Se for só teste, pode deixar comentado (#)
# inputs/efetivo.xlsx

# Ignorar credenciais (se formos usar Google API no futuro)
credentials/*.json
token.json