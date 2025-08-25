import streamlit as st
import pandas as pd
from datetime import datetime
import base64
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch

# Configuração da página
st.set_page_config(
    page_title="Checklist Veicular - CFR004",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado com gradientes
st.markdown("""
<style>
    /* Importar fonte */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Reset e configurações globais */
    .main > div {
        padding-top: 2rem;
    }

    /* Ocultar elementos do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Título principal com gradiente */
    .main-title {
        background: linear-gradient(135deg, #F7931E 0%, #000000 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(247, 147, 30, 0.3);
    }

    .main-title h1 {
        margin: 0;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 2.2rem;
    }

    .main-title .subtitle {
        margin: 0.5rem 0 0 0;
        font-size: 1rem;
        opacity: 0.9;
        font-weight: 400;
    }

    /* Títulos de seção com gradiente */
    .section-title {
        background: linear-gradient(135deg, #F7931E 0%, #000000 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 1.5rem 0 1rem 0;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1.1rem;
        box-shadow: 0 4px 15px rgba(247, 147, 30, 0.2);
    }

    /* Cards das seções */
    .section-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        border: 1px solid #f0f0f0;
    }

    /* Estilo dos checkboxes e radio buttons */
    .stCheckbox > label {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        color: #333;
    }

    .stRadio > label {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        color: #333;
    }

    /* Inputs */
    .stSelectbox > label,
    .stTextInput > label,
    .stDateInput > label,
    .stTextArea > label {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        color: #333;
        font-size: 0.9rem;
    }

    /* Botões personalizados */
    .stButton > button {
        background: linear-gradient(135deg, #F7931E 0%, #e8850c 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(247, 147, 30, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(247, 147, 30, 0.4);
    }

    /* Status indicators */
    .status-conforme {
        background: #d4edda;
        color: #155724;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 500;
        text-align: center;
        margin: 0.5rem 0;
    }

    .status-nao-conforme {
        background: #f8d7da;
        color: #721c24;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 500;
        text-align: center;
        margin: 0.5rem 0;
    }

    /* Métricas */
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
        border-left: 4px solid #F7931E;
    }

    /* Responsividade */
    @media (max-width: 768px) {
        .main-title h1 {
            font-size: 1.8rem;
        }

        .section-title {
            font-size: 1rem;
            padding: 0.8rem 1rem;
        }

        .section-card {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)


# Base de veículos
@st.cache_data
def load_vehicles():
    return [
        {"Placa": "BCQ0937", "Modelo": "F4000", "Ano": 2018},
        {"Placa": "JJB4E57", "Modelo": "CARGO 1217", "Ano": 2001},
        {"Placa": "NCF3078", "Modelo": "L200 OUTDOOR", "Ano": 2009},
        {"Placa": "NFW2H74", "Modelo": "CARGO 1317F", "Ano": 2005},
        {"Placa": "NRP2E59", "Modelo": "L200 TRITON 3.2 D", "Ano": 2011},
        {"Placa": "OFP1B78", "Modelo": "13.190 CRM 4X2", "Ano": 2012},
        {"Placa": "OGI3J31", "Modelo": "L200 TRITON 3.2 D", "Ano": 2012},
        {"Placa": "OLI7180", "Modelo": "L200 TRITON GLS D", "Ano": 2015},
        {"Placa": "PHK5D53", "Modelo": "STRADA FREEDOM CD13", "Ano": 2016},
        {"Placa": "PHL2H91", "Modelo": "S10 LT", "Ano": 2016},
        {"Placa": "PHL8286", "Modelo": "STRADA FREEDOM CD13", "Ano": 2017},
        {"Placa": "PHM3F50", "Modelo": "BROSS 160CC", "Ano": 2016},
        {"Placa": "QVN9H33", "Modelo": "HB20 10M VISION", "Ano": 2021},
        {"Placa": "QZK5H16", "Modelo": "S10 HC DD4A", "Ano": 2022},
        {"Placa": "RXE8A01", "Modelo": "SAVEIRO CS RB MF", "Ano": 2021},
        {"Placa": "SHF6D51", "Modelo": "TECTOR 170E21", "Ano": 2023},
        {"Placa": "SHK5E03", "Modelo": "TECTOR 170E21", "Ano": 2023},
        {"Placa": "SUY9E91", "Modelo": "SAVEIRO CS RB MF", "Ano": 2024},
        {"Placa": "SYC0A30", "Modelo": "STRADA FREEDOM CD13", "Ano": 2023},
        {"Placa": "SYN1C01", "Modelo": "TECTOR 170E21", "Ano": 2022},
        {"Placa": "SZF6E61", "Modelo": "SAVEIRO CS RB MF", "Ano": 2024},
        {"Placa": "TAU9G16", "Modelo": "17.210 CRM 4X2", "Ano": 2024},
        {"Placa": "TAU9G17", "Modelo": "17.210 CRM 4X2", "Ano": 2024},
        {"Placa": "TDT0I33", "Modelo": "STRADA FREEDOM CD13", "Ano": 2025},
        {"Placa": "TDT3G89", "Modelo": "STRADA FREEDOM CD13", "Ano": 2025},
        {"Placa": "TDT3H12", "Modelo": "STRADA FREEDOM CD13", "Ano": 2025},
        {"Placa": "TDT3H26", "Modelo": "STRADA FREEDOM CD13", "Ano": 2025}
    ]


# Inicializar session state
if 'checklist_data' not in st.session_state:
    st.session_state.checklist_data = {}


# Função para gerar PDF
def generate_pdf(data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1 * inch)

    # Estilos
    styles = getSampleStyleSheet()

    # Estilo personalizado para título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=HexColor('#F7931E'),
        fontName='Helvetica-Bold'
    )

    # Estilo para seções
    section_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=HexColor('#000000'),
        fontName='Helvetica-Bold'
    )

    elements = []

    # Cabeçalho
    title = Paragraph("CHECKLIST CAMINHÃO MUNCK - INSPEÇÃO<br/>ID: CFR004", title_style)
    elements.append(title)
    elements.append(Spacer(1, 20))

    # Dados da inspeção
    elements.append(Paragraph("DADOS DA INSPEÇÃO", section_style))
    inspetor = data.get('inspetor', 'Não informado')
    data_inspecao = data.get('data_inspecao', 'Não informada')
    elements.append(Paragraph(f"<b>Inspetor:</b> {inspetor}", styles['Normal']))
    elements.append(Paragraph(f"<b>Data:</b> {data_inspecao}", styles['Normal']))
    elements.append(Spacer(1, 15))

    # Dados do veículo
    elements.append(Paragraph("DADOS DO VEÍCULO", section_style))
    placa = data.get('placa', 'Não informada')
    modelo = data.get('modelo', 'Não informado')
    ano = data.get('ano', 'Não informado')
    elements.append(Paragraph(f"<b>Placa:</b> {placa}", styles['Normal']))
    elements.append(Paragraph(f"<b>Modelo:</b> {modelo}", styles['Normal']))
    elements.append(Paragraph(f"<b>Ano:</b> {ano}", styles['Normal']))
    elements.append(Spacer(1, 15))

    # Dados do motorista
    elements.append(Paragraph("DADOS DO MOTORISTA", section_style))
    motorista = data.get('motorista', 'Não informado')
    cat_cnh = data.get('cat_cnh', 'Não informada')
    data_cnh = data.get('data_cnh', 'Não informada')
    aso = data.get('aso', 'Não informado')
    elements.append(Paragraph(f"<b>Motorista:</b> {motorista}", styles['Normal']))
    elements.append(Paragraph(f"<b>Cat. CNH:</b> {cat_cnh}", styles['Normal']))
    elements.append(Paragraph(f"<b>Data Validade CNH:</b> {data_cnh}", styles['Normal']))
    elements.append(Paragraph(f"<b>Possui ASO válido:</b> {aso}", styles['Normal']))
    elements.append(Spacer(1, 20))

    # Sistemas - criar tabela para cada seção
    sistemas = [
        ("SISTEMA DE ILUMINAÇÃO", [
            ("Luz Alta", data.get('luz_alta', 'N/I')),
            ("Luz Baixa", data.get('luz_baixa', 'N/I')),
            ("Lanternas Dianteiras", data.get('lanternas_diant', 'N/I')),
            ("Setas Dianteiras", data.get('setas_diant', 'N/I')),
            ("Setas Traseiras", data.get('setas_tras', 'N/I')),
            ("Luz de Ré", data.get('luz_re', 'N/I')),
            ("Luz de Freios", data.get('luz_freios', 'N/I')),
            ("Luz de Painel", data.get('luz_painel', 'N/I')),
            ("Iluminação Interna", data.get('luz_interna', 'N/I'))
        ]),
        ("SISTEMA MECÂNICO", [
            ("Sistema de Freio", data.get('freio', 'N/I')),
            ("Freio de Estacionamento", data.get('freio_estac', 'N/I')),
            ("Reduzida do Motor", data.get('reduzida', 'N/I')),
            ("Sistema de Ventilação", data.get('ventilacao', 'N/I')),
            ("Motor em Geral", data.get('motor', 'N/I')),
            ("Sistema de Direção", data.get('direcao', 'N/I')),
            ("Sistema de Aceleração", data.get('aceleracao', 'N/I')),
            ("Sistema de Embreagem", data.get('embreagem', 'N/I')),
            ("Limpador de Vidros", data.get('limpador', 'N/I')),
            ("Velocímetro/Tacógrafo", data.get('velocimetro', 'N/I')),
            ("Sistema de Refrigeração", data.get('refrigeracao', 'N/I')),
            ("Macaco Hidráulico", data.get('macaco_hidraulico', 'N/I')),
            ("Condições do Chassi", data.get('chassi', 'N/I'))
        ]),
        ("SISTEMA DE RODAGEM", [
            ("Pneus Traseiros", data.get('pneus_tras', 'N/I')),
            ("Pneus Dianteiros", data.get('pneus_diant', 'N/I')),
            ("Parafusos/Porcas", data.get('parafusos', 'N/I')),
            ("Estepes", data.get('estepes', 'N/I')),
            ("Rodas", data.get('rodas', 'N/I'))
        ]),
        ("SISTEMA HIDRÁULICO", [
            ("Sistema de Direção Hidráulica", data.get('direcao_hidraulica', 'N/I'))
        ]),
        ("ITENS DE SEGURANÇA", [
            ("Cinto de Segurança", data.get('cinto', 'N/I')),
            ("Extintor de Incêndio", data.get('extintor', 'N/I')),
            ("Catalizador/Escapamento", data.get('catalizador', 'N/I')),
            ("Silencioso/Escapamento", data.get('silencioso', 'N/I')),
            ("Bancos/Estofados", data.get('bancos', 'N/I')),
            ("Airbag's", data.get('airbags', 'N/I')),
            ("Sinal Sonoro de Ré", data.get('sinal_re', 'N/I')),
            ("Triângulo", data.get('triangulo', 'N/I')),
            ("Macaco", data.get('macaco', 'N/I'))
        ]),
        ("CONSERVAÇÃO", [
            ("Lataria em Geral", data.get('lataria', 'N/I')),
            ("Pintura", data.get('pintura', 'N/I')),
            ("Para-brisa Dianteiro/Traseiro", data.get('parabrisa', 'N/I')),
            ("Carroceria/Assoalho", data.get('carroceria', 'N/I')),
            ("Portas, Vidros e Maçanetas", data.get('portas', 'N/I')),
            ("Espelhos Retrovisores", data.get('espelhos', 'N/I')),
            ("Caixa de Ferramentas Básicas", data.get('ferramentas', 'N/I')),
            ("Pedais", data.get('pedais', 'N/I')),
            ("Catracas", data.get('catracas', 'N/I')),
            ("Cintas de Amarração", data.get('cintas', 'N/I'))
        ])
    ]

    for sistema_nome, itens in sistemas:
        elements.append(Paragraph(sistema_nome, section_style))

        # Criar tabela
        table_data = [['Item', 'Status']]
        for item_nome, status in itens:
            status_text = {'conforme': 'Conforme', 'nc': 'Não Conforme', 'na': 'N/A'}.get(status, 'N/I')
            table_data.append([item_nome, status_text])

        table = Table(table_data, colWidths=[4 * inch, 1.5 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#F7931E')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        elements.append(table)
        elements.append(Spacer(1, 15))

    # Resultado da inspeção
    elements.append(Paragraph("RESULTADO DA INSPEÇÃO", section_style))
    resultado = data.get('resultado_inspecao', 'Não informado')
    if resultado == 'conforme':
        resultado_text = "CONFORME"
        color = HexColor('#28a745')
    elif resultado == 'nao_conforme':
        resultado_text = "NÃO CONFORME"
        color = HexColor('#dc3545')
    else:
        resultado_text = "NÃO INFORMADO"
        color = HexColor('#6c757d')

    result_style = ParagraphStyle(
        'Result',
        parent=styles['Normal'],
        fontSize=14,
        textColor=color,
        fontName='Helvetica-Bold',
        alignment=TA_CENTER
    )

    elements.append(Paragraph(resultado_text, result_style))
    elements.append(Spacer(1, 30))

    # Assinaturas
    elements.append(Paragraph("ASSINATURAS", section_style))
    sig_table = Table([
        ['Responsável pela Inspeção', 'Operador do Veículo'],
        ['_' * 30, '_' * 30]
    ], colWidths=[2.75 * inch, 2.75 * inch])

    sig_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 1), (-1, 1), 20)
    ]))

    elements.append(sig_table)

    # Rodapé
    elements.append(Spacer(1, 30))
    footer_text = f"Gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}"
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    elements.append(Paragraph(footer_text, footer_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer


# Interface principal
def main():
    # Título principal
    st.markdown("""
    <div class="main-title">
        <h1>🚛 CHECKLIST CAMINHÃO MUNCK</h1>
        <p class="subtitle">Sistema de Inspeção Veicular - ID: CFR004</p>
    </div>
    """, unsafe_allow_html=True)

    vehicles = load_vehicles()

    # Sidebar com informações
    with st.sidebar:
        st.markdown("### 📊 Informações do Sistema")
        st.info(f"**Total de Veículos:** {len(vehicles)}")
        st.success("**Status:** Online")
        st.markdown("**Versão:** 1.0")

        if st.button("🗑️ Limpar Formulário", type="secondary"):
            st.session_state.checklist_data = {}
            st.rerun()

    # Dados da Inspeção
    st.markdown('<div class="section-title">📋 DADOS DA INSPEÇÃO</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            inspetor = st.text_input("👤 Inspetor:", key="inspetor")

        with col2:
            data_inspecao = st.date_input("📅 Data da Inspeção:", datetime.now(), key="data_inspecao")

        st.markdown('</div>', unsafe_allow_html=True)

    # Dados do Veículo
    st.markdown('<div class="section-title">🚗 DADOS DO VEÍCULO</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)

        with col1:
            placas = [""] + [v["Placa"] for v in vehicles]
            placa_selecionada = st.selectbox("🏷️ Placa:", placas, key="placa")

        # Buscar dados do veículo
        veiculo_dados = None
        if placa_selecionada:
            veiculo_dados = next((v for v in vehicles if v["Placa"] == placa_selecionada), None)

        with col2:
            modelo = st.text_input("🚛 Modelo:",
                                   value=veiculo_dados["Modelo"] if veiculo_dados else "",
                                   disabled=True, key="modelo")

        with col3:
            ano = st.text_input("📆 Ano:",
                                value=str(veiculo_dados["Ano"]) if veiculo_dados else "",
                                disabled=True, key="ano")

        st.markdown('</div>', unsafe_allow_html=True)

    # Dados do Motorista
    st.markdown('<div class="section-title">👨‍💼 DADOS DO MOTORISTA</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            motorista = st.text_input("👤 Nome do Motorista:", key="motorista")
            cat_cnh = st.selectbox("🎫 Categoria CNH:", ["", "C", "D", "E"], key="cat_cnh")

        with col2:
            data_cnh = st.date_input("📅 Data Validade CNH:", key="data_cnh")
            aso = st.radio("🏥 Possui ASO válido?", ["Sim", "Não"], key="aso", horizontal=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Função auxiliar para criar seção de checklist
    def create_checklist_section(title, items, obs_key):
        st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)

        with st.container():
            st.markdown('<div class="section-card">', unsafe_allow_html=True)

            # Criar colunas para os itens
            for i, (item_key, item_name) in enumerate(items):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f"**{item_name}**")

                with col2:
                    status = st.selectbox(
                        "Status",
                        ["", "Conforme", "N.C.", "N/A"],
                        key=item_key,
                        label_visibility="collapsed"
                    )

                    # Mostrar indicador visual do status
                    if status == "Conforme":
                        st.markdown('<div class="status-conforme">✅ Conforme</div>', unsafe_allow_html=True)
                    elif status == "N.C.":
                        st.markdown('<div class="status-nao-conforme">❌ Não Conforme</div>', unsafe_allow_html=True)

            # Campo de observações
            st.markdown("---")
            observacoes = st.text_area(f"📝 Observações - {title}:", key=obs_key, height=100)

            st.markdown('</div>', unsafe_allow_html=True)

    # Seções do checklist
    create_checklist_section("💡 1. SISTEMA DE ILUMINAÇÃO", [
        ("luz_alta", "1.1 Luz Alta"),
        ("luz_baixa", "1.2 Luz Baixa"),
        ("lanternas_diant", "1.3 Lanternas Dianteiras"),
        ("setas_diant", "1.4 Setas Dianteiras"),
        ("setas_tras", "1.5 Setas Traseiras"),
        ("luz_re", "1.6 Luz de Ré"),
        ("luz_freios", "1.7 Luz de Freios"),
        ("luz_painel", "1.8 Luz de Painel"),
        ("luz_interna", "1.9 Iluminação Interna")
    ], "obs_iluminacao")

    create_checklist_section("⚙️ 2. SISTEMA MECÂNICO", [
        ("freio", "2.1 Sistema de Freio"),
        ("freio_estac", "2.2 Freio de Estacionamento"),
        ("reduzida", "2.3 Reduzida do Motor"),
        ("ventilacao", "2.4 Sistema de Ventilação"),
        ("motor", "2.5 Motor em Geral"),
        ("direcao", "2.6 Sistema de Direção"),
        ("aceleracao", "2.7 Sistema de Aceleração"),
        ("embreagem", "2.8 Sistema de Embreagem"),
        ("limpador", "2.9 Limpador de Vidros"),
        ("velocimetro", "2.10 Velocímetro/Tacógrafo"),
        ("refrigeracao", "2.11 Sistema de Refrigeração"),
        ("macaco_hidraulico", "2.12 Macaco Hidráulico"),
        ("chassi", "2.13 Condições do Chassi")
    ], "obs_mecanico")

    create_checklist_section("🛞 3. SISTEMA DE RODAGEM", [
        ("pneus_tras", "3.1 Pneus Traseiros"),
        ("pneus_diant", "3.2 Pneus Dianteiros"),
        ("parafusos", "3.3 Parafusos/Porcas"),
        ("estepes", "3.4 Estepes"),
        ("rodas", "3.5 Rodas")
    ], "obs_rodagem")

    create_checklist_section("🔧 4. SISTEMA HIDRÁULICO", [
        ("direcao_hidraulica", "4.1 Sistema de Direção Hidráulica")
    ], "obs_hidraulico")

    create_checklist_section("🛡️ 5. ITENS DE SEGURANÇA", [
        ("cinto", "5.1 Cinto de Segurança"),
        ("extintor", "5.2 Extintor de Incêndio"),
        ("catalizador", "5.3 Catalizador/Escapamento"),
        ("silencioso", "5.4 Silencioso/Escapamento"),
        ("bancos", "5.5 Bancos/Estofados"),
        ("airbags", "5.6 Airbag's"),
        ("sinal_re", "5.7 Sinal Sonoro de Ré"),
        ("triangulo", "5.8 Triângulo"),
        ("macaco", "5.9 Macaco")
    ], "obs_seguranca")

    create_checklist_section("🏗️ 6. CONSERVAÇÃO", [
        ("lataria", "6.1 Lataria em Geral"),
        ("pintura", "6.2 Pintura"),
        ("parabrisa", "6.3 Para-brisa Dianteiro/Traseiro"),
        ("carroceria", "6.4 Carroceria/Assoalho"),
        ("portas", "6.5 Portas, Vidros e Maçanetas"),
        ("espelhos", "6.7 Espelhos Retrovisores"),
        ("ferramentas", "6.8 Caixa de Ferramentas Básicas"),
        ("pedais", "6.9 Pedais"),
        ("catracas", "6.10 Catracas"),
        ("cintas", "6.11 Cintas de Amarração")
    ], "obs_conservacao")

    # Resultado da Inspeção
    st.markdown('<div class="section-title">✅ 7. RESULTADO DA INSPEÇÃO</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 1, 1])

        with col2:
            resultado = st.radio(
                "**Resultado Final:**",
                ["Conforme", "Não Conforme"],
                key="resultado_inspecao",
                horizontal=True
            )

        if resultado == "Conforme":
            st.success("🎉 **VEÍCULO APROVADO** - Todas as verificações estão em conformidade!")
        else:
            st.error("⚠️ **VEÍCULO REPROVADO** - Há itens não conformes que precisam de atenção!")

        st.markdown("---")

        # Estatísticas da inspeção
        col1, col2, col3, col4 = st.columns(4)

        # Contar status dos itens
        all_items = [
            "luz_alta", "luz_baixa", "lanternas_diant", "setas_diant", "setas_tras",
            "luz_re", "luz_freios", "luz_painel", "luz_interna", "freio", "freio_estac",
            "reduzida", "ventilacao", "motor", "direcao", "aceleracao", "embreagem",
            "limpador", "velocimetro", "refrigeracao", "macaco_hidraulico", "chassi",
            "pneus_tras", "pneus_diant", "parafusos", "estepes", "rodas",
            "direcao_hidraulica", "cinto", "extintor", "catalizador", "silencioso",
            "bancos", "airbags", "sinal_re", "triangulo", "macaco", "lataria",
            "pintura", "parabrisa", "carroceria", "portas", "espelhos",
            "ferramentas", "pedais", "catracas", "cintas"
        ]

        conformes = sum(1 for item in all_items if st.session_state.get(item) == "Conforme")
        nao_conformes = sum(1 for item in all_items if st.session_state.get(item) == "N.C.")
        nao_se_aplica = sum(1 for item in all_items if st.session_state.get(item) == "N/A")
        nao_verificados = len(all_items) - conformes - nao_conformes - nao_se_aplica

        with col1:
            st.markdown(
                f'<div class="metric-card"><h3 style="color: #28a745; margin: 0;">{conformes}</h3><p style="margin: 0;">Conformes</p></div>',
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f'<div class="metric-card"><h3 style="color: #dc3545; margin: 0;">{nao_conformes}</h3><p style="margin: 0;">Não Conformes</p></div>',
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f'<div class="metric-card"><h3 style="color: #6c757d; margin: 0;">{nao_se_aplica}</h3><p style="margin: 0;">N/A</p></div>',
                unsafe_allow_html=True
            )

        with col4:
            st.markdown(
                f'<div class="metric-card"><h3 style="color: #ffc107; margin: 0;">{nao_verificados}</h3><p style="margin: 0;">Pendentes</p></div>',
                unsafe_allow_html=True
            )

        # Assinaturas
        st.markdown("### ✍️ Assinaturas")
        col1, col2 = st.columns(2)

        with col1:
            st.text_input("👨‍🔧 Responsável pela Inspeção:", key="assinatura_responsavel")

        with col2:
            st.text_input("👨‍✈️ Operador do Veículo:", key="assinatura_operador")

        st.markdown('</div>', unsafe_allow_html=True)

    # Botões de ação
    st.markdown("---")
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col2:
        if st.button("💾 Salvar Dados", type="primary", use_container_width=True):
            # Salvar dados no session state
            for key in st.session_state:
                if key not in ['checklist_data']:
                    st.session_state.checklist_data[key] = st.session_state[key]

            st.success("✅ Dados salvos com sucesso!")

    with col3:
        if st.button("📄 Gerar PDF", type="primary", use_container_width=True):
            # Preparar dados para PDF
            pdf_data = {}

            # Dados básicos
            pdf_data.update({
                'inspetor': st.session_state.get('inspetor', ''),
                'data_inspecao': str(st.session_state.get('data_inspecao', '')),
                'placa': st.session_state.get('placa', ''),
                'modelo': st.session_state.get('modelo', ''),
                'ano': st.session_state.get('ano', ''),
                'motorista': st.session_state.get('motorista', ''),
                'cat_cnh': st.session_state.get('cat_cnh', ''),
                'data_cnh': str(st.session_state.get('data_cnh', '')),
                'aso': st.session_state.get('aso', ''),
                'resultado_inspecao': 'conforme' if st.session_state.get(
                    'resultado_inspecao') == 'Conforme' else 'nao_conforme'
            })

            # Itens de verificação
            status_mapping = {
                'Conforme': 'conforme',
                'N.C.': 'nc',
                'N/A': 'na'
            }

            for item in all_items:
                value = st.session_state.get(item, '')
                pdf_data[item] = status_mapping.get(value, 'n_i')

            try:
                with st.spinner("Gerando PDF..."):
                    pdf_buffer = generate_pdf(pdf_data)

                    # Nome do arquivo
                    placa = st.session_state.get('placa', 'SemPlaca')
                    data_str = datetime.now().strftime('%Y%m%d')
                    filename = f"Checklist_{placa}_{data_str}.pdf"

                    st.download_button(
                        label="⬇️ Download PDF",
                        data=pdf_buffer.getvalue(),
                        file_name=filename,
                        mime="application/pdf",
                        type="primary",
                        use_container_width=True
                    )

                    st.success("✅ PDF gerado com sucesso!")

            except Exception as e:
                st.error(f"❌ Erro ao gerar PDF: {str(e)}")
                st.info("💡 Certifique-se de que todos os campos obrigatórios estão preenchidos.")


if __name__ == "__main__":
    main()