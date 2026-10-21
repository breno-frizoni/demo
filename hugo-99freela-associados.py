import datetime
import pandas as pd
import streamlit as st

# Configuração da Página
st.set_page_config(
    page_title="Gestão de Associados - Adapt4",
    page_icon="🛡️",
    layout="wide",
)

# Inicialização do Banco de Dados Simulado na Sessão
if "associados" not in st.session_state:
  st.session_state.associados = pd.DataFrame([
      {
          "id": 1,
          "nome": "Carlos Silva",
          "cpf": "123.456.789-00",
          "matricula": "10025",
          "status": "Em dia",
          "email": "carlos.silva@email.com",
      },
      {
          "id": 2,
          "nome": "Ana Souza",
          "cpf": "987.654.321-11",
          "matricula": "10026",
          "status": "Devedor",
          "email": "ana.souza@email.com",
      },
      {
          "id": 3,
          "nome": "Marcos Oliveira",
          "cpf": "456.789.123-22",
          "matricula": "10027",
          "status": "Desfiliado",
          "email": "marcos.oly@email.com",
      },
  ])

if "logs_pagamentos" not in st.session_state:
  st.session_state.logs_pagamentos = pd.DataFrame([
      {
          "data": "2026-05-10",
          "matricula": "10025",
          "nome": "Carlos Silva",
          "valor": 150.00,
          "forma": "Desconto em Folha (ECONSIG)",
          "status": "Processado",
      },
      {
          "data": "2026-04-10",
          "matricula": "10025",
          "nome": "Carlos Silva",
          "valor": 150.00,
          "forma": "Desconto em Folha (SEPLAG)",
          "status": "Processado",
      },
  ])

# Sidebar - Controle de Acesso e Navegação
st.sidebar.title("Portal do Sistema")
perfil = st.sidebar.selectbox(
    "Selecionar Perfil de Acesso", ["Funcionário / Admin", "Associado"]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "Desenvolvido por **Adapt4**\nArquitetura Segura & Integração Consignatárias"
)

# ==========================================
# VISÃO DO ASSOCIADO
# ==========================================
if perfil == "Associado":
  st.title("👤 Portal do Associado")

  # Simulação de seleção de associado logado
  nomes_associados = st.session_state.associados["nome"].tolist()
  usuario_selecionado = st.sidebar.selectbox(
      "Simular login como:", nomes_associados
  )

  dados_user = st.session_state.associados[
      st.session_state.associados["nome"] == usuario_selecionado
  ].iloc[0]

  # Abas do Associado
  aba1, aba2 = st.tabs(["Carteira", "Histórico de Mensalidades"])

  with aba1:
    st.subheader("Carteirinha Digital de Associado")
    col1, col2 = st.columns([2, 1])

    with col1:
      st.markdown(
          f"**Nome:** {dados_user['nome']}\n\n"
          f"**Matrícula:** {dados_user['matricula']}\n\n"
          f"**CPF:** {dados_user['cpf']}\n\n"
          f"**E-mail:** {dados_user['email']}"
      )

      # Indicador Visual de Status
      if dados_user["status"] == "Em dia":
        st.success(f"Status Atual: **{dados_user['status']}**")
      elif dados_user["status"] == "Devedor":
        st.warning(f"Status Atual: **{dados_user['status']}**")
      else:
        st.error(f"Status Atual: **{dados_user['status']}**")

    with col2:
      st.markdown("**QR Code de Validação**")
      # Simulação visual de QR Code usando Markdown/HTML estilizado
      qr_code_mock = f"""
            <div style="background-color:white;padding:15px;text-align:center;border-radius:10px;border:2px solid #ddd;">
                <p style="font-size:11px;color:#333;margin-bottom:5px;">VAL_ID:{dados_user['matricula']}-{dados_user['status']}</p>
                <h1 style="font-size:40px;margin:0;">📱</h1>
                <p style="font-size:10px;color:#666;margin-top:5px;">Aponte a câmera do funcionário</p>
            </div>
            """
      st.markdown(qr_code_mock, unsafe_allow_html=True)

  with aba2:
    st.subheader("Histórico de Mensalidades e Descontos")
    historico_user = st.session_state.logs_pagamentos[
        st.session_state.logs_pagamentos["matricula"] == dados_user["matricula"]
    ]
    if not historico_user.empty:
      st.dataframe(historico_user, use_container_width=True)
    else:
      st.info(
          "Nenhum registro de pagamento encontrado para esta matrícula no"
          " período."
      )

# ==========================================
# VISÃO DO FUNCIONÁRIO / ADMINISTRADOR
# ==========================================
else:
  st.title("🛠️ Painel Administrativo - Funcionários")

  tab_func1, tab_func2, tab_func3 = st.tabs([
      "👥 Gestão de Associados",
      "📥 Retorno eConsig / SEPLAG",
      "🔍 Leitor de QR Code (Validação)",
  ])

  with tab_func1:
    st.subheader("Base de Associados Cadastrados")
    # Edição interativa da tabela de associados
    edited_df = st.data_editor(
        st.session_state.associados, use_container_width=True, num_rows="dynamic"
    )
    if st.button("Salvar Alterações na Base"):
      st.session_state.associados = edited_df
      st.success("Dados atualizados e log de alterações registrado com sucesso!")

  with tab_func2:
    st.subheader("Importação de Arquivo de Retorno (Consignatárias)")
    st.markdown(
        "Faça o upload do arquivo de retorno fornecido pelo sistema"
        " **ECONSIG** ou **SEPLAG** para processamento automático dos"
        " descontos em folha e atualização de logs."
    )

    tipo_sistema = st.radio("Selecione o convênio:", ["ECONSIG", "SEPLAG"])
    arquivo_retorno = st.file_uploader(
        "Enviar arquivo de remessa/retorno (.txt / .csv)",
        type=["txt", "csv", "ret"],
    )

    if arquivo_retorno is not None:
      st.info(
          f"Arquivo {arquivo_retorno.name} carregado com sucesso para o sistema"
          f" {tipo_sistema}!"
      )
      if st.button("Processar Arquivo de Retorno"):
        # Simulando adição de log automático
        novo_log = pd.DataFrame([{
            "data": str(datetime.date.today()),
            "matricula": "10025",
            "nome": "Carlos Silva",
            "valor": 150.00,
            "forma": f"Desconto em Folha ({tipo_sistema})",
            "status": "Processado via Importação",
        }])
        st.session_state.logs_pagamentos = pd.concat(
            [st.session_state.logs_pagamentos, novo_log], ignore_index=True
        )
        st.success(
            "Processamento concluído! Mensalidades atualizadas e logs de"
            " auditoria gerados."
        )

    st.markdown("---")
    st.subheader("Log Geral de Alterações e Pagamentos")
    st.dataframe(st.session_state.logs_pagamentos, use_container_width=True)

  with tab_func3:
    st.subheader("Validação em Tempo Real via QR Code")
    st.markdown(
        "Simule a leitura do QR Code da carteirinha do associado no ponto de"
        " atendimento."
    )

    matricula_busca = st.text_input(
        "Digite ou escaneie o código da matrícula:", placeholder="Ex: 10025"
    )

    if matricula_busca:
      resultado = st.session_state.associados[
          st.session_state.associados["matricula"] == matricula_busca
      ]

      if not resultado.empty:
        assoc = resultado.iloc[0]
        st.markdown("### Resultado da Consulta:")
        st.write(f"**Nome:** {assoc['nome']}")
        st.write(f"**CPF:** {assoc['cpf']}")

        status_atual = assoc["status"]
        if status_atual == "Em dia":
          st.success(
              "✅ **ASSOCIADO ATIVO E REGULAR** (Liberado para atendimento e"
              " benefícios)"
          )
        elif status_atual == "Devedor":
          st.warning(
              "⚠️ **ASSOCIADO COM PENDÊNCIAS FINANCEIRAS** (Verificar"
              " mensalidades)"
          )
        else:
          st.error(
              "❌ **ASSOCIADO DESFILIADO** (Sem direito a benefícios ou"
              " atendimento)"
          )
      else:
        st.error(
            "Matrícula não encontrada na base de dados. Verifique o código"
            " informado."
        )