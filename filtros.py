import streamlit as st
import pandas as pd

# Função para carregar os dados do arquivo CSV
@st.cache_data
def carregar_dados():
    tabela = pd.read_parquet("dfmelhor01.parquet")
    return tabela

def converter_para_horas_minutos(duracao_minutos):
    horas = int(duracao_minutos) // 60
    minutos = int(duracao_minutos) % 60
    if horas == 1:
        horas_str = "hora"
    else:
        horas_str = "horas"
    if minutos == 1:
        minutos_str = "minuto"
    else:
        minutos_str = "minutos"
    return f"{horas} {horas_str} e {minutos} {minutos_str}"


def pagina_filtros():
    st.sidebar.markdown("# Filtros")
    dados = carregar_dados()

    # Definir um dicionário para armazenar os valores dos filtros
    filtros = st.session_state.get('filtros', {})
    # Obtém os anos mínimos e máximos de lançamento
    ano_minimo = int(dados['Ano'].min())
    ano_maximo = int(dados['Ano'].max())
    # Adicionar botões na barra lateral para selecionar os filtros
    filtro_selecionado = st.sidebar.radio("Selecione o filtro:", 
                                          ['Votação Média (0 a 10)', 'Lançamento (Ano)', 'Gênero(s)', 'Quantidade de votos', 'Duração (minutos)', 'Idioma', 
                                           'Popularidade','Elenco', 'Diretor', 'Título (inglês)', 'Orçamento (U$)', 'Receita (U$)', 'Lucro do Filme (U$)'], 
                                          key='radio_buttons')

    # Verifica qual filtro foi selecionado e exibe o controle correspondente
    if filtro_selecionado == 'Orçamento (U$)':
        novo_filtro = st.sidebar.slider("Orçamento (U$)", float(dados['Orçamento'].min()), float(dados['Orçamento'].max()), filtros.get('orçamento', (float(dados['Orçamento'].min()), float(dados['Orçamento'].max()))))
        if novo_filtro != filtros.get('orçamento', (float(dados['Orçamento'].min()), float(dados['Orçamento'].max()))):
            filtros['orçamento'] = novo_filtro
    elif filtro_selecionado == 'Popularidade':
        novo_filtro = st.sidebar.slider("Popularidade", float(dados['Popularidade'].min()), float(dados['Popularidade'].max()), filtros.get('popularidade', (float(dados['Popularidade'].min()), float(dados['Popularidade'].max()))))
        if novo_filtro != filtros.get('popularidade', (float(dados['Popularidade'].min()), float(dados['Popularidade'].max()))):
            filtros['popularidade'] = novo_filtro
    elif filtro_selecionado == 'Receita (U$)':
        novo_filtro = st.sidebar.slider("Receita (U$)", float(dados['Receita'].min()), float(dados['Receita'].max()), filtros.get('receita', (float(dados['Receita'].min()), float(dados['Receita'].max()))))
        if novo_filtro != filtros.get('receita', (float(dados['Receita'].min()), float(dados['Receita'].max()))):
            filtros['receita'] = novo_filtro
    elif filtro_selecionado == 'Votação Média (0 a 10)':
        novo_filtro = st.sidebar.slider("Votação Média", float(dados['Votação'].min()), float(dados['Votação'].max()), filtros.get('votação', (float(dados['Votação'].min()), float(dados['Votação'].max()))))
        if novo_filtro != filtros.get('Votação Média', (float(dados['Votação'].min()), float(dados['Votação'].max()))):
            filtros['Votação Média'] = novo_filtro
    elif filtro_selecionado == 'Quantidade de votos':
        novo_filtro = st.sidebar.slider("Quantidade de Votos", float(dados['Votos'].min()), float(dados['Votos'].max()), filtros.get('Quantidade de votos', (float(dados['Votos'].min()), float(dados['Votos'].max()))))
        if novo_filtro != filtros.get('Quantidade de votos', (float(dados['Votos'].min()), float(dados['Votos'].max()))):
            filtros['Quantidade de votos'] = novo_filtro
    elif filtro_selecionado == 'Lucro do Filme (U$)':
        novo_filtro = st.sidebar.slider("Lucro do Filme (U$)", float(dados['Lucro'].min()), float(dados['Lucro'].max()), filtros.get('Lucro do Filme (U$)', (float(dados['Lucro'].min()), float(dados['Lucro'].max()))))
        if novo_filtro != filtros.get('Lucro do Filme (U$)', (float(dados['Lucro'].min()), float(dados['Lucro'].max()))):
            filtros['Lucro'] = novo_filtro
    elif filtro_selecionado == 'Duração (minutos)':
        # Obter os valores mínimo e máximo da duração em minutos
        duracao_min_minutos = dados['Duração'].min()
        duracao_max_minutos = dados['Duração'].max()

        # Formatar os valores mínimos e máximos em horas e minutos
        duracao_min_formatada = converter_para_horas_minutos(duracao_min_minutos)
        duracao_max_formatada = converter_para_horas_minutos(duracao_max_minutos)

        # Definir valores padrão para o slider
        valor_padrao = (duracao_min_minutos, duracao_max_minutos)

        # Criar o slider na barra lateral
        novo_filtro = st.sidebar.slider("Duração", duracao_min_minutos, duracao_max_minutos, valor_padrao, format="%d minutos")

        # Atualizar os filtros se houver uma mudança
        if novo_filtro != filtros.get('Duração', valor_padrao):
            filtros['Duração'] = novo_filtro
    elif filtro_selecionado == 'Gênero(s)':
        generos_disponiveis = pd.concat([dados['gênero1'], dados['gênero2'], dados['gênero3']]).dropna().unique()
        genero1 = st.sidebar.selectbox("Selecione o primeiro gênero:", [''] + list(generos_disponiveis), index=0)
        genero2 = st.sidebar.selectbox("Selecione o segundo gênero:", [''] + list(generos_disponiveis), index=0)
        genero3 = st.sidebar.selectbox("Selecione o terceiro gênero:", [''] + list(generos_disponiveis), index=0)
        generos_selecionados = [genero for genero in [genero1, genero2, genero3] if genero]
        if generos_selecionados != filtros.get('Gênero(s)', []):
            filtros['Gênero(s)'] = generos_selecionados
    elif filtro_selecionado == 'Idioma':
        idiomas_disponiveis = dados['Idioma'].dropna().unique()
        idioma_selecionado = st.sidebar.selectbox("Selecione o idioma:", [''] + list(idiomas_disponiveis), index=0)
        filtros['idioma'] = idioma_selecionado
    elif filtro_selecionado == 'Lançamento (Ano)':
        st.sidebar.subheader('Ano de Lançamento')
        opcoes_ano = ['Intervalo de Anos', 'Ano Único']
        tipo_ano = st.sidebar.radio("Escolha o tipo de ano:", opcoes_ano)
        if tipo_ano == 'Intervalo de Anos':
            ano_minimo = int(dados['Ano'].min())
            ano_maximo = int(dados['Ano'].max())
            ano_intervalo = st.sidebar.slider("Selecione um intervalo de anos:", ano_minimo, ano_maximo, (ano_minimo, ano_maximo))
            filtros['ano'] = ano_intervalo
        elif tipo_ano == 'Ano Único':
            ano_selecionado = st.sidebar.number_input("Digite o ano de lançamento:", min_value=int(dados['Ano'].min()), max_value=int(dados['Ano'].max()))
            filtros['ano'] = ano_selecionado
    elif filtro_selecionado == 'Elenco':
        elenco_input = st.sidebar.text_input("Digite o nome do ator:", value=filtros.get('Elenco', ''))
        confirmar_elenco = st.sidebar.button("Confirmar")

        if elenco_input:
            filtros['Elenco'] = elenco_input.strip()

        if confirmar_elenco:
            filtros['Elenco'] = elenco_input.strip()

    elif filtro_selecionado == 'Diretor':
        diretor_input = st.sidebar.text_input("Digite o nome do diretor:", value=filtros.get('Diretor', ''))
        confirmar_diretor = st.sidebar.button("Confirmar")

        if diretor_input:
            filtros['Diretor'] = diretor_input.strip()

        if confirmar_diretor:
            filtros['Diretor'] = diretor_input.strip()

    
    
    elif filtro_selecionado == 'Título (inglês)':
        diretor_input = st.sidebar.text_input("Digite o nome do título do filme em inglês:", value=filtros.get('Diretor', ''))
        confirmar_diretor = st.sidebar.button("Confirmar")

        if diretor_input:
            filtros['Título'] = diretor_input.strip()

        if confirmar_diretor:
            filtros['Título'] = diretor_input.strip()
    
    
    # Salvar os filtros na sessão
    st.session_state['filtros'] = filtros

    # Exibir os filtros selecionados na tela central
    st.markdown('<div style="font-size:22px; font-weight:bold; color:#FF9999; text-align: center;">Filtros Selecionados:</div>', unsafe_allow_html=True)

    html_div = "<div style='display: flex; flex-wrap: wrap; justify-content: center;'>"
    for chave, valor in filtros.items():
        coluna = chave.capitalize()
        if isinstance(valor, tuple):
            if chave == 'Votação Média':
                valor_str = f"<span style='color:#FF9999;'>{valor[0]:.2f}</span> a <span style='color:#FF9999;'>{valor[1]:.2f}</span>"
            elif chave in ['orçamento', 'receita', 'Lucro']:
                valor_min = int(valor[0])
                valor_max = int(valor[1])
                valor_str = f"<span style='font-size:19px; font-weight:italic; color:#FF9999;'>U$ {valor_min:,d}</span> a <span style='font-size:19px; font-weight:italic; color:#FF9999;'> U$ {valor_max:,d}</span>"
            else:
                valor_min, valor_max = valor
                valor_str = f"<span style='color:#FF9999;'>{int(valor_min)}</span> a <span style='color:#FF9999;'>{int(valor_max)}</span>"
        else:
            if isinstance(valor, list):
                if chave == 'Gênero(s)':
                    valor_str = ', '.join(f"<span style='color:#FF9999;'>{v}</span>" for v in valor) if valor else 'Nenhum'
                else:
                    valor_str = ', '.join(valor) if valor else 'Nenhum'
            else:
                valor_str = f"<span style='color:#FF9999;'>{valor}</span>"

        html_div += f"<div style='margin: 5px;'><span style='font-size:20px; font-weight:bold; color:#FFFFFF;'>{coluna}:</span> <span style='font-size:18px;'>{valor_str}</span></div>"

    html_div += "</div>"
    st.markdown(html_div, unsafe_allow_html=True)

    return dados, filtros

