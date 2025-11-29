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

print("🚀 INICIANDO SISTEMA DE ESCALA (V3.2 - CONTROLE TOTAL)...")

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
    {"Nome": "OF. CHEFE DE OPERAÇÕES",       "Qtd": 1, "Req": "OF"},
    {"Nome": "ADJUNTO AO OF. DE DIA",        "Qtd": 1, "Req": "SGT"},
    {"Nome": "OF DE RAS AOS DESTACAMENTOS",  "Qtd": 1, "Req": "OF"},
    {"Nome": "COMUNICAÇÃO (24H)",            "Qtd": 2, "Req": "COM"},
    {"Nome": "COMAT/SOP",                    "Qtd": 2, "Req": "GV"},
    {"Nome": "ENCARREGADO DE MOT/MOT ASE",   "Qtd": 1, "Req": "MOT"},
    {"Nome": "MOT. AR-SOS",                  "Qtd": 1, "Req": "MOT"},
    {"Nome": "MOTO AQUÁTICA (24H)",          "Qtd": 2, "Req": "MOT"},
    {"Nome": "SUPERVISOR 24H",               "Qtd": 1, "Req": "SGT"},
    {"Nome": "GUARNIÇÃO ASE 489 (24x72)",    "Qtd": 2, "Req": "GV"}
]

config_praia = [
    {"Nome": "JOATINGA",    "Qtd": 2, "Req": "GV"}, 
    {"Nome": "POSTO 8",     "Qtd": 2, "Req": "GV"},
    {"Nome": "CANAL 1",     "Qtd": 1, "Req": "GV"}, 
    {"Nome": "POSTO BR",    "Qtd": 0, "Req": "GV"},
    {"Nome": "CANAL 2",     "Qtd": 2, "Req": "GV"}, 
    {"Nome": "VIA 11",      "Qtd": 1, "Req": "GV"},
    {"Nome": "QUEBRA MAR",  "Qtd": 2, "Req": "GV"}, 
    {"Nome": "P. RETORNO",  "Qtd": 1, "Req": "GV"},
    {"Nome": "POSTO 1",     "Qtd": 2, "Req": "GV"}, 
    {"Nome": "ILHA 26",     "Qtd": 1, "Req": "GV"},
    {"Nome": "TROPICAL",    "Qtd": 2, "Req": "GV"}, 
    {"Nome": "ILHA 25",     "Qtd": 1, "Req": "GV"},
    {"Nome": "BOBS",        "Qtd": 2, "Req": "GV"}, 
    {"Nome": "ILHA 24",     "Qtd": 1, "Req": "GV"},
    {"Nome": "POSTO 2",     "Qtd": 2, "Req": "GV"}, 
    {"Nome": "ILHA 22",     "Qtd": 1, "Req": "GV"},
    {"Nome": "FAROL",       "Qtd": 2, "Req": "GV"}, 
    {"Nome": "ILHA 20",     "Qtd": 1, "Req": "GV"},
    {"Nome": "POSTO 3",     "Qtd": 2, "Req": "GV"}, 
    {"Nome": "ILHA 18",     "Qtd": 1, "Req": "GV"},
    {"Nome": "POSTO 3,5",   "Qtd": 2, "Req": "GV"}, 
    {"Nome": "ILHA 16",     "Qtd": 1, "Req": "GV"},
    {"Nome": "POSTO 4",     "Qtd": 2, "Req": "GV"}, 
    {"Nome": "ILHA 13",     "Qtd": 1, "Req": "GV"},
    {"Nome": "POSTO 5",     "Qtd": 2, "Req": "GV"}, 
    {"Nome": "ILHA 11",     "Qtd": 1, "Req": "GV"},
    {"Nome": "RIVIERA",     "Qtd": 2, "Req": "GV"}, 
    {"Nome": "ILHA 09",     "Qtd": 1, "Req": "GV"},
    {"Nome": "POSTO 6",     "Qtd": 2, "Req": "GV"}, 
    {"Nome": "ILHA 07",     "Qtd": 1, "Req": "GV"},
    {"Nome": "BARRABELA",   "Qtd": 2, "Req": "GV"}, 
    {"Nome": "ILHA 05",     "Qtd": 1, "Req": "GV"},
    {"Nome": "POSTO 7",     "Qtd": 2, "Req": "GV"}, 
    {"Nome": "",            "Qtd": 0, "Req": "INDIFERENTE"}
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
    
    if 'Qualificacao' not in df_efetivo.columns:
        print("⚠️ AVISO: Coluna 'Qualificacao' não encontrada. Assumindo GV.")
        df_efetivo['Qualificacao'] = 'GV'
        
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
# PASSO 3: MOTOR LÓGICO COM MENU DE OPÇÕES
# ==============================================================================
print("\n3️⃣  CONFIGURAÇÃO DA OPERAÇÃO:")

# --- PERGUNTA 1: DATA INICIAL ---
input_data = input(">> Data de Início (dd/mm/aaaa) [Enter para HOJE]: ").strip()
if input_data:
    try:
        data_inicio_dt = datetime.strptime(input_data, '%d/%m/%Y')
    except ValueError:
        print("❌ Data inválida! Usando HOJE como padrão.")
        data_inicio_dt = datetime.now()
else:
    data_inicio_dt = datetime.now()

# --- PERGUNTA 2: QUANTIDADE ---
input_qtd = input(">> Quantos dias gerar? [Enter para 1 dia]: ").strip()
if input_qtd:
    try:
        dias_a_gerar = int(input_qtd)
    except ValueError:
        dias_a_gerar = 1
else:
    dias_a_gerar = 1

# Calcula data final
data_limite = data_inicio_dt + timedelta(days=dias_a_gerar - 1)

print(f"\n   🔄 Processando de {data_inicio_dt.strftime('%d/%m/%Y')} até {data_limite.strftime('%d/%m/%Y')}...")

# --- MARCO ZERO ---
DATA_REFERENCIA_STR = '2025-12-01' 
ALA_REFERENCIA = 'A'
data_ref_dt = datetime.strptime(DATA_REFERENCIA_STR, '%Y-%m-%d')
CICLO = ['A', 'B', 'C']
idx_ref = CICLO.index(ALA_REFERENCIA)

data_processamento = data_inicio_dt

while data_processamento <= data_limite:
    dia_str = data_processamento.strftime('%Y-%m-%d')
    dia_br = data_processamento.strftime('%d/%m/%Y')
    nome_arquivo_br = data_processamento.strftime('%d-%m-%Y')
    
    dias_passados = (data_processamento - data_ref_dt).days
    idx_ala_atual = (idx_ref + dias_passados) % 3
    ala_dia = CICLO[idx_ala_atual]
    
    print(f"   --> Gerando {dia_br} (Ala {ala_dia})...")
    
    tropa_do_dia = df_efetivo[df_efetivo['Ala'] == ala_dia].copy()
    relatorio_permutas_dia = []

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
                        relatorio_permutas_dia.append({'Sai': quem_sai, 'Entra': quem_entra})
                        houve_mudanca = True
                    elif quem_entra in tropa_do_dia['Nome_Guerra'].values:
                        pass
                    else:
                        proxima_rodada.append(troca)
            trocas_pendentes = proxima_rodada

    disponiveis = tropa_do_dia.to_dict('records')
    random.shuffle(disponiveis)
    
    temp_alocacao = {} 
    
    for _, posto in df_ordem_preenchimento.iterrows():
        nome_posto = posto['Nome']
        qtd_vagas = posto['Qtd']
        req_qualificacao = posto.get('Req', 'INDIFERENTE')
        
        nomes_alocados = []
        if nome_posto != "": 
            for _ in range(qtd_vagas):
                candidato_escolhido = None
                for militar in disponiveis:
                    qualif_militar = militar.get('Qualificacao', 'GV')
                    if req_qualificacao == 'INDIFERENTE' or req_qualificacao == qualif_militar:
                        candidato_escolhido = militar
                        break
                
                if candidato_escolhido:
                    nomes_alocados.append(candidato_escolhido['Nome_Guerra'])
                    disponiveis.remove(candidato_escolhido)
                else:
                    if req_qualificacao == 'INDIFERENTE': nomes_alocados.append("---")
                    else: nomes_alocados.append(f"---")

            temp_alocacao[nome_posto] = nomes_alocados

    # ==============================================================================
    # PASSO 4: PDF FINAL
    # ==============================================================================
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
                nomes_limpos = [n for n in conteudo if n != "" and n != "---" and not n.startswith("FALTA")]
                if nomes_limpos:
                    # Remove GV visualmente
                    nomes_sem_gv = [n.replace("GV ", "") for n in nomes_limpos]
                    texto_nomes = " / ".join(nomes_sem_gv)
                else:
                    texto_nomes = "---"
            else:
                texto_nomes = str(conteudo).replace("GV ", "")
            
            if "FALTA" in str(conteudo): self.set_text_color(255, 0, 0)
            else: self.set_text_color(0, 0, 0)

            self.multi_cell(w, 5, texto_nomes, 1, 'L', fill=True)
            self.set_text_color(0, 0, 0)

    pdf = PDFPraia('P', 'mm', 'A4')
    pdf.set_auto_page_break(auto=True, margin=5) 
    x_central = 31

    pdf.add_page()
    
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_fill_color(200, 200, 200)
    pdf.cell(0, 8, f"DATA: {dia_br} (ALA {ala_dia})", 1, 1, 'C', fill=True)
    pdf.ln(2)

    y_start = pdf.get_y()
    altura_box = 10 
    for i in range(0, len(config_interno), 2):
        if i >= len(config_interno): break
        item_esq = config_interno[i]
        nomes_esq = temp_alocacao.get(item_esq['Nome'], ["---"])
        pdf.draw_box(item_esq['Nome'], nomes_esq, 10, y_start, 90, altura_box)
        
        if i + 1 < len(config_interno):
            item_dir = config_interno[i+1]
            nomes_dir = temp_alocacao.get(item_dir['Nome'], ["---"])
            pdf.draw_box(item_dir['Nome'], nomes_dir, 105, y_start, 90, altura_box)
        y_start += altura_box + 2 

    pdf.set_y(y_start + 5) 

    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_fill_color(50, 50, 50); pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 8, "DISTRIBUIÇÃO DE PRAIA", 1, 1, 'C', fill=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)
    
    w_posto = 28; w_mil = 22; gap = 4
    
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
            nomes = temp_alocacao.get(nome_posto, ["---", "---"])
            while len(nomes) < 2: nomes.append("")
            
            for idx in [0, 1]:
                txt = str(nomes[idx])
                txt_limpo = txt.replace("GV ", "")
                if "FALTA" in txt:
                    pdf.set_text_color(255, 0, 0)
                    pdf.set_font('Helvetica', 'B', 5)
                    pdf.cell(w_mil, 6, txt_limpo, 1, 0, 'C')
                elif txt == "---":
                    pdf.set_text_color(200, 200, 200)
                    pdf.set_font('Helvetica', '', 7)
                    pdf.cell(w_mil, 6, txt_limpo, 1, 0, 'C')
                else:
                    pdf.set_text_color(0, 0, 0)
                    pdf.set_font('Helvetica', '', 7)
                    pdf.cell(w_mil, 6, txt_limpo, 1, 0, 'C')
        desenhar_lado(posto_esq)
        pdf.cell(gap, 6, "", 0, 0)
        desenhar_lado(posto_dir)
        pdf.ln() 

    pdf.ln(5) 
    if relatorio_permutas_dia:
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_fill_color(50, 50, 50); pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 6, "ALTERAÇÕES / PERMUTAS DO DIA", 1, 1, 'L', fill=True)
        pdf.set_text_color(0, 0, 0); pdf.set_font('Helvetica', 'B', 7); pdf.set_fill_color(220, 220, 220)
        pdf.cell(95, 5, "SAI (TITULAR)", 1, 0, 'C', fill=True)
        pdf.cell(95, 5, "ENTRA (SUBSTITUTO)", 1, 1, 'C', fill=True)
        pdf.set_font('Helvetica', '', 7)
        for troca in relatorio_permutas_dia:
            sai_limpo = troca['Sai'].replace("GV ", "")
            entra_limpo = troca['Entra'].replace("GV ", "")
            pdf.cell(95, 5, sai_limpo, 1, 0, 'C')
            pdf.cell(95, 5, entra_limpo, 1, 1, 'C')
    else:
        pdf.set_font('Helvetica', 'I', 8)
        pdf.cell(0, 6, "Sem permutas registradas para esta data.", 0, 1, 'C')

    caminho_arquivo = f"outputs/Escala_{nome_arquivo_br}.pdf"
    pdf.output(caminho_arquivo)
    print(f"   ✅ Gerado: {caminho_arquivo}")

    data_processamento += timedelta(days=1)

print("\n🚀 PROCESSO CONCLUÍDO!")
input("Pressione ENTER para fechar...")