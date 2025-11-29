import pandas as pd
import random
import os
import warnings # <--- O SILENCIADOR
from datetime import datetime, timedelta
from fpdf import FPDF

# --- CONFIGURAÇÃO DE SILÊNCIO ---
# Ignora avisos de versão (Deprecation) para limpar o terminal
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# --- PASSO 0: PREPARAR AMBIENTE ---
if not os.path.exists('inputs'): os.makedirs('inputs')
if not os.path.exists('outputs'): os.makedirs('outputs')

print("🚀 INICIANDO SISTEMA DE ESCALA (VERSÃO 2.1 - CLEAN)...")

# ==============================================================================
# PASSO 1: CONFIGURAÇÃO (VISUAL, QUANTIDADE E PRIORIDADE)
# ==============================================================================

# A. LISTA DE PRIORIDADE ALTA (VIP)
lista_prioridade_alta = ["POSTO 3", "QUEBRA MAR"] 

# B. ORDEM GEOGRÁFICA PADRÃO
ORDEM_GEOGRAFICA = [
    "JOATINGA", "CANAL 1", "CANAL 2", "QUEBRA MAR", "POSTO 1", 
    "TROPICAL", "BOBS", "POSTO 2", "FAROL", "POSTO 3", 
    "POSTO 3,5", "POSTO 4", "POSTO 5", "RIVIERA", "POSTO 6", 
    "BARRABELA", "POSTO 7", "POSTO 8", "VIA 11", "P. RETORNO",
    "ILHA 26", "ILHA 25", "ILHA 24", "ILHA 22", "ILHA 20", 
    "ILHA 18", "ILHA 16", "ILHA 13", "ILHA 11", "ILHA 09", 
    "ILHA 07", "ILHA 05"
]

# C. CONFIGURAÇÃO VISUAL E DE QUANTIDADE
config_postos = [
    {"Nome": "JOATINGA",    "Qtd": 2}, 
    {"Nome": "POSTO 8",     "Qtd": 2},
    {"Nome": "CANAL 1",     "Qtd": 1}, 
    {"Nome": "POSTO BR",    "Qtd": 0},
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
df_config = pd.DataFrame(config_postos)

def calcular_peso(nome_posto):
    if nome_posto in lista_prioridade_alta: return lista_prioridade_alta.index(nome_posto)
    if nome_posto in ORDEM_GEOGRAFICA: return 1000 + ORDEM_GEOGRAFICA.index(nome_posto)
    return 9999

df_config['Ordem_Matematica'] = df_config['Nome'].apply(calcular_peso)
df_ordem_preenchimento = df_config.sort_values('Ordem_Matematica')

# ==============================================================================
# PASSO 2: LEITURA DO EFETIVO E PERMUTAS
# ==============================================================================
print("2️⃣  Lendo Arquivos (Efetivo + Permutas)...")

# Leitura do Efetivo
arquivo_efetivo = 'inputs/efetivo.xlsx'
if os.path.exists(arquivo_efetivo):
    df_efetivo = pd.read_excel(arquivo_efetivo)
    if 'Ala' not in df_efetivo.columns: df_efetivo['Ala'] = 'A'
    df_efetivo = df_efetivo.drop_duplicates(subset=['Nome_Guerra'])
else:
    print("❌ ERRO CRÍTICO: 'efetivo.xlsx' não encontrado!")
    exit()

# Leitura das Permutas
arquivo_permutas = 'inputs/permutas.xlsx'
df_permutas = pd.DataFrame() 
if os.path.exists(arquivo_permutas):
    try:
        df_permutas = pd.read_excel(arquivo_permutas)
        df_permutas['Data'] = pd.to_datetime(df_permutas['Data']).dt.strftime('%Y-%m-%d')
        print(f"   -> {len(df_permutas)} permutas carregadas.")
    except Exception as e:
        print(f"⚠️ Aviso: Erro ao ler permutas ({e}). Seguindo sem trocas.")
else:
    print("⚠️ Aviso: Arquivo 'permutas.xlsx' não existe. Nenhuma troca será feita.")

# ==============================================================================
# PASSO 3: MOTOR LÓGICO
# ==============================================================================
print("3️⃣  Processando Escala e Trocas...")
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
    
    # A. Filtra Tropa do Dia
    tropa_do_dia = df_efetivo[df_efetivo['Ala'] == ala_dia].copy()
    
    # B. Aplica Permutas
    if not df_permutas.empty:
        trocas_hoje = df_permutas[df_permutas['Data'] == dia_str]
        
        for _, troca in trocas_hoje.iterrows():
            quem_sai = troca['Sai_Nome']
            quem_entra = troca['Entra_Nome']
            
            if quem_sai in tropa_do_dia['Nome_Guerra'].values:
                tropa_do_dia = tropa_do_dia[tropa_do_dia['Nome_Guerra'] != quem_sai]
                print(f"   🔄 TROCA REALIZADA: Saiu {quem_sai}")
            
            dados_entra = df_efetivo[df_efetivo['Nome_Guerra'] == quem_entra]
            if not dados_entra.empty:
                tropa_do_dia = pd.concat([tropa_do_dia, dados_entra])
                print(f"   🔄 TROCA REALIZADA: Entrou {quem_entra}")
            else:
                print(f"   ⚠️ ERRO: {quem_entra} não está no cadastro de efetivo!")

    # C. Converte para lista e embaralha
    disponiveis = tropa_do_dia.to_dict('records')
    random.shuffle(disponiveis)
    
    # D. Loop de Preenchimento
    temp_alocacao = {} 
    
    for _, posto in df_ordem_preenchimento.iterrows():
        nome_posto = posto['Nome']
        qtd_vagas = posto['Qtd']
        
        nomes_alocados = []
        if nome_posto != "": 
            for _ in range(qtd_vagas):
                if len(disponiveis) > 0:
                    militar = disponiveis.pop(0)
                    nomes_alocados.append(militar['Nome_Guerra'])
                else:
                    nomes_alocados.append("---")
            temp_alocacao[nome_posto] = nomes_alocados

    # E. Organiza para Visualização
    for item in config_postos:
        nome = item['Nome']
        if nome in temp_alocacao:
            lista_final = temp_alocacao[nome]
            while len(lista_final) < 3: lista_final.append("")
        else:
            lista_final = ["", "", ""] 
            
        escala_dados.append({
            'Data': dia_str, 
            'Posto': nome, 
            'Militares': lista_final
        })
    
    data_atual += timedelta(days=1)
    idx_ala += 1

df_final = pd.DataFrame(escala_dados)
df_matriz = df_final.pivot_table(index='Posto', columns='Data', values='Militares', aggfunc=lambda x: x)

# ==============================================================================
# PASSO 4: PDF FINAL
# ==============================================================================
print("4️⃣  Gerando PDF...")

class PDFPraia(FPDF):
    def header(self):
        # Alterei para Helvetica para evitar avisos de fonte
        self.set_font('Helvetica', 'B', 10)
        self.cell(0, 8, 'ESCALA DE PRAIA - 2 GMAR', 0, 1, 'C')
        self.ln(2)

pdf = PDFPraia('P', 'mm', 'A4')
pdf.set_auto_page_break(auto=True, margin=5) 

for data_coluna in df_matriz.columns:
    pdf.add_page()
    
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_fill_color(220, 220, 220)
    pdf.cell(0, 8, f"DATA: {data_coluna}", 1, 1, 'C', fill=True)
    pdf.ln(2)

    w_posto = 28
    w_mil = 22 
    gap = 4
    
    pdf.set_font('Helvetica', 'B', 6)
    pdf.set_fill_color(50, 50, 50); pdf.set_text_color(255, 255, 255)
    pdf.cell(w_posto, 5, "POSTO", 1, 0, 'C', fill=True)
    pdf.cell(w_mil*2, 5, "MILITARES", 1, 0, 'C', fill=True)
    pdf.cell(gap, 5, "", 0, 0)
    pdf.cell(w_posto, 5, "POSTO", 1, 0, 'C', fill=True)
    pdf.cell(w_mil*2, 5, "MILITARES", 1, 1, 'C', fill=True)

    pdf.set_text_color(0, 0, 0); pdf.set_font('Helvetica', '', 7) 

    for i in range(0, len(config_postos), 2):
        if i+1 >= len(config_postos): break 
        
        posto_esq = config_postos[i]['Nome']
        posto_dir = config_postos[i+1]['Nome']
        
        def desenhar_lado(nome_posto):
            pdf.set_text_color(0, 0, 0); pdf.set_font('Helvetica', '', 6)
            if nome_posto == "":
                pdf.cell(w_posto + w_mil*2, 6, "", 0, 0)
                return

            pdf.cell(w_posto, 6, nome_posto, 1, 0, 'C')
            
            nomes = ["", ""]
            try:
                lista = df_matriz.loc[nome_posto, data_coluna]
                if isinstance(lista, list): nomes = lista
            except: pass
            
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
print("\n✅ SUCESSO! PDF gerado e terminal limpo.")