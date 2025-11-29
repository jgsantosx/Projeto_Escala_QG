import pandas as pd
import random
import os
from datetime import datetime, timedelta
from fpdf import FPDF

# --- PASSO 0: PREPARAR AMBIENTE ---
if not os.path.exists('inputs'): os.makedirs('inputs')
if not os.path.exists('outputs'): os.makedirs('outputs')

print("🚀 INICIANDO SISTEMA DE ESCALA (MODO VIDA REAL)...")

# ==============================================================================
# PASSO 1: CONFIGURAÇÃO DOS POSTOS (Garante que o Excel de config esteja certo)
# ==============================================================================
layout_visual_fixo = [
    "JOATINGA", "POSTO 8",
    "CANAL 1", "POSTO BR",
    "CANAL 2", "VIA 11",
    "QUEBRA MAR", "P. RETORNO",
    "POSTO 1", "ILHA 26",
    "TROPICAL", "ILHA 25",
    "BOBS", "ILHA 24",
    "POSTO 2", "ILHA 22",
    "FAROL", "ILHA 20",
    "POSTO 3", "ILHA 18",
    "POSTO 3,5", "ILHA 16",
    "POSTO 4", "ILHA 13",
    "POSTO 5", "ILHA 11",
    "RIVIERA", "ILHA 09",
    "POSTO 6", "ILHA 07",
    "BARRABELA", "ILHA 05",
    "POSTO 7", "" 
]
#PRIORIDADE DE POSTO ENTRE " "
lista_de_prioridades = [ "CANAL 1" ,"QUEBRA MAR" , "POSTO 1"  , "TROPICAL" , "BOBS" , "POSTO 2" , "FAROL" , "POSTO 3"
    
]

print("1️⃣  Atualizando Configuração dos Postos...")
lista_limpa = [p for p in layout_visual_fixo if p != ""]
df_config = pd.DataFrame({'Nome_Posto': lista_limpa})

def calcular_prioridade(nome_posto):
    if nome_posto in lista_de_prioridades:
        return lista_de_prioridades.index(nome_posto)
    return 1000

df_config['Ordem_Preenchimento'] = df_config['Nome_Posto'].apply(calcular_prioridade)
df_config = df_config.sort_values('Ordem_Preenchimento')

# AQUI ESTÁ A CORREÇÃO DO SEU ERRO: Criamos as colunas obrigatórias
df_config['Qtd'] = 2 
df_config['Qualificacao_Necessaria'] = 'GV' 

df_config.to_excel('inputs/configuracao_postos.xlsx', index=False)

# ==============================================================================
# PASSO 2: LEITURA DO EFETIVO (MANUAL)
# ==============================================================================
print("2️⃣  Lendo seu Efetivo Real...")

arquivo_efetivo = 'inputs/efetivo.xlsx'

if os.path.exists(arquivo_efetivo):
    # Lê o arquivo que você editou
    df_efetivo = pd.read_excel(arquivo_efetivo)
    
    # Limpeza básica para evitar erros
    # Garante que as colunas existam, se não, cria vazias
    if 'Ala' not in df_efetivo.columns: df_efetivo['Ala'] = 'A'
    if 'Nome_Guerra' not in df_efetivo.columns: 
        print("❌ ERRO: Seu Excel precisa ter uma coluna chamada 'Nome_Guerra'")
        exit()
        
    # Remove duplicatas (nomes iguais)
    df_efetivo = df_efetivo.drop_duplicates(subset=['Nome_Guerra'])
    print(f"   -> {len(df_efetivo)} militares carregados do Excel.")
    
else:
    print("⚠️  Arquivo 'efetivo.xlsx' não encontrado! Criando um modelo para você preencher...")
    # Cria um modelo vazio com alguns exemplos
    dados_modelo = []
    for ala in ['A', 'B', 'C']:
        for i in range(1, 6): # 5 Exemplos por ala
            dados_modelo.append({'Nome_Guerra': f'Sd Exemplo {i}-{ala}', 'Ala': ala, 'Qualificacao': 'GV'})
    
    df_efetivo = pd.DataFrame(dados_modelo)
    df_efetivo.to_excel(arquivo_efetivo, index=False)
    print("   -> Arquivo modelo criado em 'inputs/efetivo.xlsx'.")
    print("   -> PARE O SCRIPT, edite esse arquivo com seus nomes reais e rode de novo!")

# ==============================================================================
# PASSO 3: MOTOR LÓGICO
# ==============================================================================
print("3️⃣  Calculando Escala...")
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
    
    # Filtra quem é da Ala do dia
    disponiveis = df_efetivo[df_efetivo['Ala'] == ala_dia].to_dict('records')
    random.shuffle(disponiveis) # Mistura para não ser sempre os mesmos nos mesmos postos
    
    # Preenche Postos
    for _, posto in df_config.iterrows():
        nome_posto = posto['Nome_Posto']
        qtd_vagas = 2
        
        nomes_alocados = []
        for _ in range(qtd_vagas):
            if len(disponiveis) > 0:
                militar = disponiveis.pop(0) # Pega e remove da lista
                nomes_alocados.append(militar['Nome_Guerra'])
            else:
                nomes_alocados.append("-") #VAGO
        
        escala_dados.append({
            'Data': dia_str, 
            'Posto': nome_posto, 
            'Militares': nomes_alocados 
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
    pdf.cell(0, 8, f"DATA: {data_coluna} (ALA DO DIA)", 1, 1, 'C', fill=True)
    pdf.ln(2)

    w_posto = 28
    w_mil = 32
    gap = 6
    
    pdf.set_font('Arial', 'B', 7)
    pdf.set_fill_color(50, 50, 50)
    pdf.set_text_color(255, 255, 255)
    
    pdf.cell(w_posto, 5, "POSTO", 1, 0, 'C', fill=True)
    pdf.cell(w_mil, 5, "MILITAR 1", 1, 0, 'C', fill=True)
    pdf.cell(w_mil, 5, "MILITAR 2", 1, 0, 'C', fill=True)
    pdf.cell(gap, 5, "", 0, 0)
    pdf.cell(w_posto, 5, "POSTO", 1, 0, 'C', fill=True)
    pdf.cell(w_mil, 5, "MILITAR 1", 1, 0, 'C', fill=True)
    pdf.cell(w_mil, 5, "MILITAR 2", 1, 1, 'C', fill=True)

    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', '', 7) 

    for i in range(0, len(layout_visual_fixo), 2):
        if i+1 >= len(layout_visual_fixo): break 
        
        posto_esq = layout_visual_fixo[i]
        posto_dir = layout_visual_fixo[i+1]
        
        def desenhar_lado(nome_posto):
            pdf.set_text_color(0, 0, 0); pdf.set_font('Arial', '', 7)
            if nome_posto == "":
                pdf.cell(w_posto + w_mil*2, 6, "", 0, 0)
                return

            pdf.cell(w_posto, 6, nome_posto, 1, 0, 'C')

            try:
                lista_nomes = df_matriz.loc[nome_posto, data_coluna]
                if not isinstance(lista_nomes, list): lista_nomes = ["---", "---"]
            except: lista_nomes = ["---", "---"]

            for nome in lista_nomes[:2]: 
                if nome == "-" or nome == "---":  #VAGO
                    pdf.set_font('Arial', 'B', 6)
                else:
                    pdf.set_text_color(0, 0, 0); pdf.set_font('Arial', '', 7)
                pdf.cell(w_mil, 6, str(nome), 1, 0, 'C')

        desenhar_lado(posto_esq)
        pdf.cell(gap, 6, "", 0, 0)
        desenhar_lado(posto_dir)
        pdf.ln() 

pdf.output('outputs/escala_praia_FINAL.pdf')
print("\n✅ SUCESSO! PDF gerado com base no seu Excel.")