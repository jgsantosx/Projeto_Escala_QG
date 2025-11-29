# 🎖️ Automação de Escala de Serviço - 2º GMAR (V2.7)

Este projeto é uma ferramenta desenvolvida em Python para automatizar a geração da **Escala de Praia** (Serviço Operacional). O sistema gerencia o ciclo 12x60, processa permutas automaticamente (com validação de regras) e gera um PDF formatado com layout oficial.

## 🚀 Novidades da Versão 2.7

- **📄 Layout Completo e Profissional:**
  - **Cabeçalho:** Inclui escala de Serviço Interno (Oficiais, Motoristas, Prontidão).
  - **Visual:** Tabela centralizada na folha A4 com destaque visual (fundo cinza) nos postos.
  - **Rodapé:** Tabela automática listando as permutas realizadas no dia ("Quem Saiu" vs "Quem Entrou").
- **🔄 Sistema de Permutas Inteligente (Multi-pass):**
  - O robô lê o arquivo `permutas.xlsx`, aceita trocas em qualquer ordem (resolve trocas casadas) e valida regras de negócio.
- **🧠 Distribuição Híbrida:**
  - **Prioridade VIP:** Postos críticos são garantidos primeiro.
  - **Ordem Geográfica:** O restante segue a ordem natural da praia.

## 🛠️ Funcionalidades Principais

- **Ciclo Automático:** Calcula a Ala de serviço (A, B ou C) baseado na data.
- **Efetivo Flexível:** Controle total de vagas por posto via configuração (`config_praia` e `config_interno`).
- **Relatório de Alterações:** Tabela detalhada no final do PDF mostrando as trocas efetivadas.

## 📂 Estrutura de Arquivos

````text
Projeto_Escala_QG/
│
├── inputs/
│   ├── efetivo.xlsx        # Colunas: Nome_Guerra, Ala
│   └── permutas.xlsx       # Colunas: Data, Sai_Nome, Entra_Nome
│
├── outputs/
│   └── escala_praia_FINAL.pdf  # O resultado gerado
│
├── gerador_escala.py       # Motor Lógico Completo (V2.7)
├── README.md               # Documentação
└── .gitignore              # Arquivos ignorados
⚙️ Como Configurar
1. Instalação
Necessário Python 3.x e as bibliotecas:

Bash

pip install pandas openpyxl fpdf
2. Preparando a Escala
Efetivo: Atualize o inputs/efetivo.xlsx com a tropa atual.

Permutas: Se houver trocas, preencha inputs/permutas.xlsx (Data YYYY-MM-DD).

Regras: No arquivo gerador_escala.py, você pode editar:

config_interno: Postos da parte superior (Oficiais, Motoristas).

config_praia: Postos da praia e quantidades.

lista_prioridade_alta: Postos que têm preferência no preenchimento.

▶️ Como Rodar
Execute o script no terminal:

Bash

python gerador_escala.py
O robô informará no terminal as trocas realizadas e gerará o PDF na pasta outputs/.

🚧 Próximos Passos (Roadmap)
[x] Cabeçalho Completo: Escala de Oficiais e Motoristas (Implementado na V2.5).

[x] Relatório de Permutas: Tabela no rodapé (Implementado na V2.7).

[ ] Compilação (.exe): Transformar o script em executável para rodar sem Python.

[ ] Interface Gráfica (GUI): Criar janelas para facilitar o uso.

[ ] Versão 3.0 (Futuro): Implementar distribuição por Antiguidade (Patente).

Desenvolvido para automação administrativa militar.


---

### 2. Atualizar o GitHub

Agora vamos salvar essa documentação junto com o código V2.7 que você já finalizou.

No terminal:

1.  **Adicionar:**
    ```powershell
    git add .
    ```

2.  **Commit (Oficializando a V2.7):**
    ```powershell
    git commit -m "Docs: Atualiza README para V2.7 (Layout Completo e Rodape de Permutas)"
    ```

3.  **Enviar:**
    ```powershell
    git push
    ```

    

Assim que subir, seu projeto estará "Passado a Limpo".

Com o projeto salvo, **qual sua ordem para a próxima etapa?**
1.  Gerar o `.exe` (para você poder mandar o programa para outros computadores)?
2.  Ou iniciar a Interface Gráfica (janelas)?
````
