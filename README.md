🪖 Projeto Escala QG - Automação de Escala de Praia (2º GMAR)
Este projeto é uma ferramenta de automação desenvolvida em Python para gerar a escala de serviço diária de Guarda-Vidas. O sistema respeita o ciclo de 12x60, realiza a distribuição de efetivo em duplas por posto e gera um PDF formatado pronto para impressão.

🚀 Funcionalidades Principais
Ciclo Automático: Identifica automaticamente a Ala do dia (A, B ou C).

Alocação em Duplas: Preenche cada posto com 2 militares (Canga).

Sistema de Prioridade Tática: Preenche primeiro os postos críticos (ex: Posto 2, Posto 3) antes dos postos periféricos.

Alerta de Efetivo: Se houver falta de pessoal, o sistema marca os postos descobertos em VERMELHO com o texto "FALTA EFETIVO", mantendo os postos prioritários preenchidos.

Anti-Repetição: Garante que o mesmo militar não seja escalado duas vezes no mesmo dia.

PDF Oficial: Gera um arquivo visual com layout fixo (Joatinga a Ilha 05).

📂 Estrutura do Projeto
Plaintext

Projeto_Escala_QG/
│
├── 📂 inputs/
│   ├── efetivo.xlsx            # LISTA DE MILITARES (Você edita aqui)
│   └── configuracao_postos.xlsx # Regras geradas pelo sistema (Não mexer)
│
├── 📂 outputs/
│   └── escala_praia_FINAL.pdf  # O RESULTADO FINAL (O PDF gerado)
│
└── 📄 sistema_escala_final.py  # O CÓDIGO (O cérebro da operação)
🛠️ Pré-requisitos e Instalação
Para rodar o sistema, você precisa ter o Python instalado no computador.

Instalar Bibliotecas: Abra o terminal (Prompt de Comando) e rode:

PowerShell

py -m pip install pandas openpyxl fpdf
🕹️ Como Usar (Passo a Passo)
1. Atualizar o Efetivo (Adicionar/Remover Militares)
Toda a gestão de pessoal é feita pelo Excel.

Vá na pasta inputs/.

Abra o arquivo efetivo.xlsx.

Adicionar: Escreva o Nome_Guerra, a Ala (A, B ou C) e a Qualificacao (GV).

Remover: Basta apagar a linha do militar.

Salvar e fechar o arquivo.

2. Gerar a Escala
Abra o terminal na pasta do projeto.

Execute o comando:

PowerShell

py sistema_escala_final.py
O sistema lerá o Excel, calculará a distribuição e gerará o PDF.

3. Pegar o Resultado
Vá na pasta outputs/.

Abra o arquivo escala_praia_FINAL.pdf.

Verifique se há postos em VERMELHO (indicando falta de efetivo).

⚙️ Configurações Avançadas (Editando o Código)
Algumas regras estão definidas dentro do arquivo sistema_escala_final.py. Para alterá-las, clique com o botão direito no arquivo e escolha "Editar" ou abra no Bloco de Notas.

Alterar a Prioridade dos Postos
Procure pela lista lista_de_prioridades no início do código.

Os postos no topo da lista recebem soldados primeiro.

Os postos que não estiverem na lista ficam por último.

Python

lista_de_prioridades = [
    "POSTO 2",  # <--- Prioridade Máxima
    "POSTO 1",
    "POSTO 3",
    ...
]
Simular Data Específica
Procure pelas variáveis DATA_INICIO e DATA_FIM dentro do "PASSO 3".

Python

DATA_INICIO = '2025-12-01' # Mude para a data que deseja gerar
DATA_FIM = '2025-12-01'
⚠️ Solução de Problemas Comuns
Erro "Permission Denied" ao salvar:

Verifique se o arquivo efetivo.xlsx ou o PDF final estão abertos. Feche-os e tente rodar de novo.

PDF saiu todo vermelho:

Verifique se a Data configurada no código corresponde a uma Ala que tem militares cadastrados no Excel. (Ex: Se o dia é Ala A, mas só tem nomes na Ala B no Excel, ninguém será escalado).

Nomes repetidos:

O sistema remove duplicatas automaticamente, mas verifique se no Excel não há nomes escritos com espaços diferentes (ex: "Silva" e "Silva ").

Desenvolvido para uso interno do Quartel.