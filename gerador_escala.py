import pandas as pd
import random
import os
from datetime import datetime, timedelta
from fpdf import FPDF

# --- PASSO 0: PREPARAR AMBIENTE ---
if not os.path.exists('inputs'): os.makedirs('inputs')
if not os.path.exists('outputs'): os.makedirs('outputs')

print("🚀 INICIANDO SISTEMA DE ESCALA (ORDEM HÍBRIDA)...")

# ==============================================================================
# PASSO 1: CONFIGURAÇÃO (VISUAL, QUANTIDADE E PRIORIDADE)
# ==============================================================================

# A. LISTA DE PRIORIDADE ALTA (VIP)
# Coloque aqui SOMENTE os postos que você quer "furar a fila" de preenchimento.
# Se deixar vazio [], ele segue a ordem geográfica pura.
lista_prioridade_alta = ["", ""] 

# B. ORDEM GEOGRÁFICA PADRÃO (A Regra da Praia)
# Essa é a ordem que o robô seguirá se o posto não for VIP.
ORDEM_GEOGRAFICA = [
    "JOATINGA", "CANAL 1", "CANAL 2", "QUEBRA MAR", "POSTO 1", 
    "TROPICAL", "BOBS", "POSTO 2", "FAROL", "POSTO 3", 
    "POSTO 3,5", "POSTO 4", "POSTO 5", "RIVIERA", "POSTO 6", 
    "BARRABELA", "POSTO 7", "POSTO 8", "VIA 11", "P. RETORNO",
    "ILHA 26", "ILHA 25", "ILHA 24", "ILHA 22", "ILHA 20", 
    "ILHA 18", "ILHA 16", "ILHA 13", "ILHA 11", "ILHA 09", 
    "ILHA 07", "ILHA 05"
]

# C. CONFIGURAÇÃO VISUAL E DE QUANTIDADE (O que sai no PDF)
# Aqui você define a Quantidade (Qtd) e a posição no papel.
config_postos = [
    {"Nome": "JOATINGA",    "Qtd": 2}, 
    {"Nome": "POSTO 8",     "Qtd": 2},
    {"Nome": "CANAL 1",     "Qtd": 1}, 
    {"Nome": "POSTO BR",    "Qtd": 0}, # Posto BR não estava na lista geo, mantive 0 ou ajuste
    {"Nome": "CANAL 2",     "Qtd": 2}, 
    {"Nome": "VIA 11",      "Qtd": 1},
    {"Nome": "QUEBRA MAR",  "Qtd": 2}, 
    {"Nome": "P. RETORNO",  "Qtd": 1},
    {"Nome": "POSTO 1",     "Qtd": 2}, 
    {"Nome": "ILHA 26",     "Qtd": 1},
    {"Nome": "TROPICAL",    "Qtd": 2}, 
    {"Nome": "ILHA 25",     "Qtd": 1},
    {"Nome": "BOBS",        "Qtd": 2}, 
    {"Nome": "ILHA 24",     "Qtd": 1},
    {"Nome": "POSTO 2",     "Qtd": 2}, 
    {"Nome": "ILHA 22",     "Qtd": 1},
    {"Nome": "FAROL",       "Qtd": 2}, 
    {"Nome": "ILHA 20",     "Qtd": 1},
    {"Nome": "POSTO 3",     "Qtd": 2}, 
    {"Nome": "ILHA 18",     "Qtd": 1},
    {"Nome": "POSTO 3,5",   "Qtd": 2}, 
    {"Nome": "ILHA 16",     "Qtd": 1},
    {"Nome": "POSTO 4",     "Qtd": 2}, 
    {"Nome": "ILHA 13",     "Qtd": 1},
    {"Nome": "POSTO 5",     "Qtd": 2}, 
    {"Nome": "ILHA 11",     "Qtd": 1},
    {"Nome": "RIVIERA",     "Qtd": 2}, 
    {"Nome": "ILHA 09",     "Qtd": 1},
    {"Nome": "POSTO 6",     "Qtd": 2}, 
    {"Nome": "ILHA 07",     "Qtd": 1},
    {"Nome": "BARRABELA",   "Qtd": 2}, 
    {"Nome": "ILHA 05",     "Qtd": 1},
    {"Nome": "POSTO 7",     "Qtd": 2}, 
    {"Nome": "",            "Qtd": 0}
]

print("1️⃣  Calculando Ordem de Preenchimento...")

# Cria DataFrame
df_config = pd.DataFrame(config_postos)

# --- A MÁGICA DA PRIORIDADE ---
def calcular_peso(nome_posto):
    # 1. Se estiver na lista VIP, prioridade máxima (0 a 999)
    if nome_posto in lista_prioridade_alta:
        return lista_prioridade_alta.index(nome_posto)
    
    # 2. Se não for VIP, usa a ordem geográfica (1000 pra cima)
    if nome_posto in ORDEM_GEOGRAFICA:
        return 1000 + ORDEM_GEOGRAFICA.index(nome_posto)
    
    # 3. Se não estiver em lista nenhuma, fica pro final
    return 9999

df_config['Ordem_Matematica'] = df_config['Nome'].apply(calcular_peso)

# Ordena o DataFrame para o Robô preencher na ordem certa
# (Isso não muda o PDF, só muda quem ganha soldado primeiro)
df_ordem_preenchimento = df_config.sort_values('Ordem_Matematica')

# ==============================================================================
# PASSO 2: LEITURA DO EFETIVO
# ==============================================================================
print("2️⃣  Lendo Efetivo...")
arquivo_efetivo = 'inputs/efetivo.xlsx'

if os.path.exists(arquivo_efetivo):
    df_efetivo = pd.read_excel(arquivo_efetivo)
    if 'Ala' not in df_efetivo.columns: df_efetivo['Ala'] = 'A'
    if 'Nome_Guerra' not in df_efetivo.columns: 
        print("❌ ERRO: Coluna 'Nome_Guerra' não encontrada!")
        exit()
    df_efetivo = df_efetivo.drop_duplicates(subset=['Nome_Guerra'])
else:
    print("⚠️  Arquivo efetivo.xlsx não encontrado.")
    exit()

# ==============================================================================
# PASSO 3: MOTOR LÓGICO
# ==============================================================================
print("3️⃣  Calculando Distribuição...")
DATA_INICIO = '2025-12-01'
DATA_FIM = '2025-12-01' 
CICLO = ['A', 'B', 'C']

escala_dados = []
data_atual = datetime.strptime(DATA_INICIO, '%Y-%m-%d')
data_final = datetime.strptime(DATA_FIM, '%Y-%m-%d')
idx_ala = 0 

while data_atual <= data_final:
    dia_str = data_atual.strftime('%Y-%m-%d')
    ala_dia = CICLO[idx_ala % 3]
    
    # Filtra e embaralha a tropa do dia
    disponiveis = df_efetivo[df_efetivo['Ala'] == ala_dia].to_dict('records')
    random.shuffle(disponiveis)
    
    # Loop de preenchimento (SEGUE A ORDEM MATEMÁTICA CALCULADA)
    # Primeiro os VIPs, depois a Joatinga, Canal 1, etc...
    temp_alocacao = {} # Guarda quem foi pra onde temporariamente
    
    for _, posto in df_ordem_preenchimento.iterrows():
        nome_posto = posto['Nome']
        qtd_vagas = posto['Qtd']
        
        nomes_alocados = []
        if nome_posto != "": # Ignora os vazios visuais
            for _ in range(qtd_vagas):
                if len(disponiveis) > 0:
                    militar = disponiveis.pop(0)
                    nomes_alocados.append(militar['Nome_Guerra'])
                else:
                    nomes_alocados.append("---")
            
            # Guarda na memória temporária
            temp_alocacao[nome_posto] = nomes_alocados

    # Agora joga para a lista final (para depois gerar o PDF)
    # Precisamos iterar sobre a config visual ORIGINAL para manter a ordem do PDF
    for item in config_postos:
        nome = item['Nome']
        if nome in temp_alocacao:
            lista_final = temp_alocacao[nome]
            # Completa com vazio visual se precisar
            while len(lista_final) < 3: lista_final.append("")
        else:
            lista_final = ["", "", ""] # Caso seja espaço vazio ou posto sem alocação
            
        escala_dados.append({
            'Data': dia_str, 
            'Posto': nome, 
            'Militares': lista_final
        })
    
    data_atual += timedelta(days=1)
    idx_ala += 1

df_final = pd.DataFrame(escala_dados)
# Cria matriz segura
df_matriz = df_final.pivot_table(index='Posto', columns='Data', values='Militares', aggfunc=lambda x: x)

# ==============================================================================
# PASSO 4: PDF FINAL
# ==============================================================================
print("4️⃣  Gerando PDF...")

class PDFPraia(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 10)
        self.cell(0, 8, 'ESCALA DE PRAIA - 2 GMAR', 0, 1, 'C')
        self.ln(2)

pdf = PDFPraia('P', 'mm', 'A4')
pdf.set_auto_page_break(auto=True, margin=5) 

for data_coluna in df_matriz.columns:
    pdf.add_page()
    
    pdf.set_font('Arial', 'B', 12)
    pdf.set_fill_color(220, 220, 220)
    pdf.cell(0, 8, f"DATA: {data_coluna}", 1, 1, 'C', fill=True)
    pdf.ln(2)

    w_posto = 28
    w_mil = 22 
    gap = 4
    
    # Cabeçalho
    pdf.set_font('Arial', 'B', 6)
    pdf.set_fill_color(50, 50, 50); pdf.set_text_color(255, 255, 255)
    pdf.cell(w_posto, 5, "POSTO", 1, 0, 'C', fill=True)
    pdf.cell(w_mil*2, 5, "MILITARES", 1, 0, 'C', fill=True)
    pdf.cell(gap, 5, "", 0, 0)
    pdf.cell(w_posto, 5, "POSTO", 1, 0, 'C', fill=True)
    pdf.cell(w_mil*2, 5, "MILITARES", 1, 1, 'C', fill=True)

    pdf.set_text_color(0, 0, 0); pdf.set_font('Arial', '', 7) 

    # Desenho Visual (Segue a ordem de config_postos, não a de preenchimento)
    for i in range(0, len(config_postos), 2):
        if i+1 >= len(config_postos): break 
        
        posto_esq = config_postos[i]['Nome']
        posto_dir = config_postos[i+1]['Nome']
        
        def desenhar_lado(nome_posto):
            pdf.set_text_color(0, 0, 0); pdf.set_font('Arial', '', 6)
            if nome_posto == "":
                pdf.cell(w_posto + w_mil*2, 6, "", 0, 0)
                return

            pdf.cell(w_posto, 6, nome_posto, 1, 0, 'C')
            
            nomes = ["", ""]
            try:
                # Recupera a lista que guardamos lá no Passo 3
                # Como não estamos lendo do Excel Pivotado visualmente, e sim direto da memória
                # Precisamos garantir a busca correta. 
                # (Ajuste rápido: o df_matriz usa Posto como índice)
                lista = df_matriz.loc[nome_posto, data_coluna]
                if isinstance(lista, list): nomes = lista
            except: pass
            
            # Se for "---", pinta de vermelho pra alertar falta
            if nomes[0] == "---": pdf.set_text_color(255, 0, 0)
            pdf.cell(w_mil, 6, str(nomes[0]), 1, 0, 'C')
            
            if nomes[1] == "---": pdf.set_text_color(255, 0, 0)
            else: pdf.set_text_color(0, 0, 0)
            pdf.cell(w_mil, 6, str(nomes[1]), 1, 0, 'C')

        desenhar_lado(posto_esq)
        pdf.cell(gap, 6, "", 0, 0)
        desenhar_lado(posto_dir)
        pdf.ln() 

pdf.output('outputs/escala_praia_FINAL.pdf')
print("\n✅ SUCESSO! PDF gerado com ordem Geográfica e Prioridades.")