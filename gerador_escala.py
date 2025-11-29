import pandas as pd
import random
import os
import warnings
from datetime import datetime, timedelta
from fpdf import FPDF

# --- CONFIGURAÇÃO DE SILÊNCIO ---
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# --- PASSO 0: PREPARAR AMBIENTE ---
if not os.path.exists('inputs'): os.makedirs('inputs')
if not os.path.exists('outputs'): os.makedirs('outputs')

print("🚀 INICIANDO SISTEMA DE ESCALA (V2.7 - COM RELATÓRIO DE TROCAS)...")

# ==============================================================================
# 🧠 O JUIZ DAS PERMUTAS
# ==============================================================================
def validar_cadastro(nome_sai, nome_entra, df_efetivo):
    dados_sai = df_efetivo[df_efetivo['Nome_Guerra'] == nome_sai]
    dados_entra = df_efetivo[df_efetivo['Nome_Guerra'] == nome_entra]
    
    if dados_sai.empty: return False, f"Militar {nome_sai} não encontrado."
    if dados_entra.empty: return False, f"Militar {nome_entra} não encontrado."
    
    return True, "Ok"

# ==============================================================================
# PASSO 1: CONFIGURAÇÃO
# ==============================================================================
lista_prioridade_alta = ["OF. CHEFE DE OPERAÇÕES", "ADJUNTO AO OF. DE DIA", "POSTO 3"] 

ORDEM_GEOGRAFICA = [
    "JOATINGA", "CANAL 1", "CANAL 2", "QUEBRA MAR", "POSTO 1", 
    "TROPICAL", "BOBS", "POSTO 2", "FAROL", "POSTO 3", 
    "POSTO 3,5", "POSTO 4", "POSTO 5", "RIVIERA", "POSTO 6", 
    "BARRABELA", "POSTO 7", "POSTO 8", "VIA 11", "P. RETORNO",
    "ILHA 26", "ILHA 25", "ILHA 24", "ILHA 22", "ILHA 20", 
    "ILHA 18", "ILHA 16", "ILHA 13", "ILHA 11", "ILHA 09", 
    "ILHA 07", "ILHA 05"
]

config_interno = [
    {"Nome": "OF. CHEFE DE OPERAÇÕES",       "Qtd": 1},
    {"Nome": "ADJUNTO AO OF. DE DIA",        "Qtd": 1},
    {"Nome": "OF DE RAS AOS DESTACAMENTOS",  "Qtd": 1},
    {"Nome": "COMUNICAÇÃO (24H)",            "Qtd": 2},
    {"Nome": "COMAT/SOP",                    "Qtd": 2},
    {"Nome": "ENCARREGADO DE MOT/MOT ASE",   "Qtd": 1},
    {"Nome": "MOT. AR-SOS",                  "Qtd": 1},
    {"Nome": "MOTO AQUÁTICA (24H)",          "Qtd": 2},
    {"Nome": "SUPERVISOR 24H",               "Qtd": 1},
    {"Nome": "GUARNIÇÃO ASE 489 (24x72)",    "Qtd": 2}
]

config_praia = [
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

print("1️⃣  Unificando Configurações...")
todos_postos = config_interno + config_praia
df_config = pd.DataFrame(todos_postos)

def calcular_peso(nome_posto):
    if nome_posto in lista_prioridade_alta: return lista_prioridade_alta.index(nome_posto)
    if nome_posto in ORDEM_GEOGRAFICA: return 1000 + ORDEM_GEOGRAFICA.index(nome_posto)
    return 9999

df_config['Ordem_Matematica'] = df_config['Nome'].apply(calcular_peso)
df_ordem_preenchimento = df_config.sort_values('Ordem_Matematica')

# ==============================================================================
# PASSO 2: LEITURA DO EFETIVO E PERMUTAS
# ==============================================================================
print("2️⃣  Lendo Arquivos...")

arquivo_efetivo = 'inputs/efetivo.xlsx'
if os.path.exists(arquivo_efetivo):
    df_efetivo = pd.read_excel(arquivo_efetivo)
    if 'Ala' not in df_efetivo.columns: df_efetivo['Ala'] = 'A'
    df_efetivo = df_efetivo.drop_duplicates(subset=['Nome_Guerra'])
else:
    print("❌ ERRO CRÍTICO: 'efetivo.xlsx' não encontrado!")
    exit()

arquivo_permutas = 'inputs/permutas.xlsx'
df_permutas = pd.DataFrame() 
if os.path.exists(arquivo_permutas):
    try:
        df_permutas = pd.read_excel(arquivo_permutas)
        df_permutas['Data'] = pd.to_datetime(df_permutas['Data']).dt.strftime('%Y-%m-%d')
    except: pass

# ==============================================================================
# PASSO 3: MOTOR LÓGICO
# ==============================================================================
print("3️⃣  Processando Escala...")
DATA_INICIO = '2025-12-01'
DATA_FIM = '2025-12-01' 
CICLO = ['A', 'B', 'C']

escala_dados = []
relatorio_permutas = {} # <--- NOVO: Guarda o histórico do dia
data_atual = datetime.strptime(DATA_INICIO, '%Y-%m-%d')
data_final = datetime.strptime(DATA_FIM, '%Y-%m-%d')
idx_ala = 0 

while data_atual <= data_final:
    dia_str = data_atual.strftime('%Y-%m-%d')
    ala_dia = CICLO[idx_ala % 3]
    
    tropa_do_dia = df_efetivo[df_efetivo['Ala'] == ala_dia].copy()
    
    # Inicializa lista de trocas do dia
    relatorio_permutas[dia_str] = []

    if not df_permutas.empty:
        trocas_pendentes = df_permutas[df_permutas['Data'] == dia_str].to_dict('records')
        houve_mudanca = True
        while houve_mudanca and len(trocas_pendentes) > 0:
            houve_mudanca = False
            proxima_rodada = []
            for troca in trocas_pendentes:
                quem_sai = troca['Sai_Nome']
                quem_entra = troca['Entra_Nome']
                cadastro_ok, msg = validar_cadastro(quem_sai, quem_entra, df_efetivo)
                if cadastro_ok:
                    if quem_sai in tropa_do_dia['Nome_Guerra'].values:
                        tropa_do_dia = tropa_do_dia[tropa_do_dia['Nome_Guerra'] != quem_sai]
                        dados_entra = df_efetivo[df_efetivo['Nome_Guerra'] == quem_entra]
                        tropa_do_dia = pd.concat([tropa_do_dia, dados_entra])
                        print(f"   ✅ TROCA ACEITA: {quem_sai} <-> {quem_entra}")
                        
                        # LOG PARA O PDF
                        relatorio_permutas[dia_str].append({'Sai': quem_sai, 'Entra': quem_entra})
                        houve_mudanca = True
                    elif quem_entra in tropa_do_dia['Nome_Guerra'].values:
                        print(f"   ⛔ NEGADO: {quem_entra} JÁ está na escala.")
                    else:
                        proxima_rodada.append(troca)
                else:
                    print(f"   ⛔ ERRO CADASTRO: {msg}")
            trocas_pendentes = proxima_rodada

    disponiveis = tropa_do_dia.to_dict('records')
    random.shuffle(disponiveis)
    
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

    for item in todos_postos:
        nome = item['Nome']
        lista_final = temp_alocacao.get(nome, ["", "", ""])
        while len(lista_final) < 3: lista_final.append("")
        
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
print("4️⃣  Gerando PDF Completo...")

class PDFPraia(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 8, 'ESCALA DE SERVIÇO - 2º GMAR', 0, 1, 'C')
        self.ln(2)

    def draw_box(self, titulo, conteudo, x, y, w, h):
        self.set_xy(x, y)
        self.set_font('Helvetica', 'B', 7)
        self.set_fill_color(240, 240, 240)
        self.cell(w, 5, titulo, 1, 0, 'L', fill=True)
        self.set_xy(x, y + 5)
        self.set_font('Helvetica', '', 7)
        self.set_fill_color(255, 255, 255)
        texto_nomes = ""
        if isinstance(conteudo, list):
            nomes_limpos = [n for n in conteudo if n != "" and n != "---"]
            texto_nomes = " / ".join(nomes_limpos)
            if not nomes_limpos and "---" in conteudo: texto_nomes = "---"
        else:
            texto_nomes = str(conteudo)
        self.multi_cell(w, 5, texto_nomes, 1, 'L', fill=True)

pdf = PDFPraia('P', 'mm', 'A4')
pdf.set_auto_page_break(auto=True, margin=5) 
x_central = 31

for data_coluna in df_matriz.columns:
    pdf.add_page()
    
    # 1. TÍTULO
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_fill_color(200, 200, 200)
    pdf.cell(0, 8, f"DATA: {data_coluna} (SERVIÇO DE 24H)", 1, 1, 'C', fill=True)
    pdf.ln(2)

    # 2. CABEÇALHO (INTERNO)
    y_start = pdf.get_y()
    altura_box = 10 
    for i in range(0, len(config_interno), 2):
        if i >= len(config_interno): break
        item_esq = config_interno[i]
        try: nomes_esq = df_matriz.loc[item_esq['Nome'], data_coluna]
        except: nomes_esq = [""]
        pdf.draw_box(item_esq['Nome'], nomes_esq, 10, y_start, 90, altura_box)
        if i + 1 < len(config_interno):
            item_dir = config_interno[i+1]
            try: nomes_dir = df_matriz.loc[item_dir['Nome'], data_coluna]
            except: nomes_dir = [""]
            pdf.draw_box(item_dir['Nome'], nomes_dir, 105, y_start, 90, altura_box)
        y_start += altura_box + 2 

    pdf.set_y(y_start + 5) 

    # 3. PRAIA (CENTRALIZADO)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_fill_color(50, 50, 50); pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 8, "DISTRIBUIÇÃO DE PRAIA", 1, 1, 'C', fill=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)
    
    w_posto = 28
    w_mil = 22 
    gap = 4
    
    pdf.set_x(x_central)
    pdf.set_font('Helvetica', 'B', 6)
    pdf.set_fill_color(220, 220, 220)
    pdf.cell(w_posto, 5, "POSTO", 1, 0, 'C', fill=True)
    pdf.cell(w_mil*2, 5, "MILITARES", 1, 0, 'C', fill=True)
    pdf.cell(gap, 5, "", 0, 0)
    pdf.cell(w_posto, 5, "POSTO", 1, 0, 'C', fill=True)
    pdf.cell(w_mil*2, 5, "MILITARES", 1, 1, 'C', fill=True)
    pdf.set_text_color(0, 0, 0); pdf.set_font('Helvetica', '', 7) 

    for i in range(0, len(config_praia), 2):
        if i+1 >= len(config_praia): break 
        posto_esq = config_praia[i]['Nome']
        posto_dir = config_praia[i+1]['Nome']
        pdf.set_x(x_central) 
        def desenhar_lado(nome_posto):
            pdf.set_text_color(0, 0, 0); pdf.set_font('Helvetica', '', 6)
            if nome_posto == "":
                pdf.cell(w_posto + w_mil*2, 6, "", 0, 0)
                return
            pdf.set_fill_color(240, 240, 240)
            pdf.cell(w_posto, 6, nome_posto, 1, 0, 'C', fill=True) 
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

    # 4. TABELA DE PERMUTAS (NOVO RODAPÉ)
    pdf.ln(5) # Espaço
    trocas_do_dia = relatorio_permutas.get(data_coluna, [])
    
    if trocas_do_dia:
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_fill_color(50, 50, 50); pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 6, "ALTERAÇÕES / PERMUTAS DO DIA", 1, 1, 'L', fill=True)
        
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('Helvetica', 'B', 7)
        pdf.set_fill_color(220, 220, 220)
        
        # Cabeçalho da Tabela Permutas
        w_sai = 95
        w_entra = 95
        pdf.cell(w_sai, 5, "SAI (TITULAR)", 1, 0, 'C', fill=True)
        pdf.cell(w_entra, 5, "ENTRA (SUBSTITUTO)", 1, 1, 'C', fill=True)
        
        pdf.set_font('Helvetica', '', 7)
        for troca in trocas_do_dia:
            pdf.cell(w_sai, 5, troca['Sai'], 1, 0, 'C')
            pdf.cell(w_entra, 5, troca['Entra'], 1, 1, 'C')
    else:
        # Se não houver permutas, mostra aviso discreto
        pdf.set_font('Helvetica', 'I', 8)
        pdf.cell(0, 6, "Sem permutas registradas para esta data.", 0, 1, 'C')

pdf.output('outputs/escala_praia_FINAL.pdf')
print("\n✅ SUCESSO! PDF V2.7 Gerado (Com Tabela de Permutas).")