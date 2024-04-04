import streamlit as st
import pandas as pd
from filtros import pagina_filtros, converter_para_horas_minutos
from recomendar import recomendars
from deep_translator import GoogleTranslator


# Configurar a página como wide
st.set_page_config(layout="wide")

# Título do web app
st.markdown('<div style="font-size:48px; font-weight:bold; text-align: center;">Recomendação de Filmes</div>', unsafe_allow_html=True)

# Importar os filtros
dados, filtros = pagina_filtros()

# Função para dividir um texto longo em partes menores
def dividir_texto(texto, tamanho_maximo):
    """
    Função para dividir um texto longo em partes menores.

    Args:
        texto (str): O texto a ser dividido.
        tamanho_maximo (int): O tamanho máximo de cada parte.

    Returns:
        list: Uma lista contendo as partes divididas do texto.
    """
    partes = []
    for i in range(0, len(texto), tamanho_maximo):
        partes.append(texto[i:i + tamanho_maximo])
    return partes

# Função para traduzir um texto
def traduzir_texto(texto, idioma_origem='en', idioma_destino='pt'):
    """
    Função para traduzir um texto para outro idioma.

    Args:
        texto (str): O texto a ser traduzido.
        idioma_origem (str): O idioma de origem do texto (padrão: 'en').
        idioma_destino (str): O idioma de destino para a tradução (padrão: 'pt').

    Returns:
        str: O texto traduzido ou None se ocorrer um erro.
    """
    try:
        # Verificar se o texto está vazio ou é None
        if not texto:
            return None

        # Verificar se o texto é do tipo string
        if isinstance(texto, str):
            # Verificar se o texto excede o limite máximo de caracteres
            if len(texto) > 5000:
                # Dividir o texto em partes menores
                partes = dividir_texto(texto, 4000)
                # Inicializar uma lista para armazenar as traduções das partes
                traducoes = []
                # Traduzir cada parte separadamente
                for parte in partes:
                    traducao_parte = GoogleTranslator(source=idioma_origem, target=idioma_destino).translate(parte)
                    traducoes.append(traducao_parte)
                # Juntar as traduções das partes em um único texto
                traducao = " ".join(traducoes)
            else:
                # O texto é curto o suficiente para ser traduzido inteiro
                traducao = GoogleTranslator(source=idioma_origem, target=idioma_destino).translate(texto)
            
            return traducao
        else:
            # Se não for uma string, retornar None
            return None
    except Exception as e:
        st.error(f"Erro ao traduzir texto: {e}")
        return None

    
    
# Botão para recomendar filmes
if st.sidebar.button("Recomendar Filmes"):
    
    titulos_filmes_recomendados, total_filmes_recomendados, sinopse_filmes_recomendados, ano_filmes_recomendados, generos_filmes_recomendados, idioma_filmes_recomendados, votaçao_filmes_recomendados, duracao_filmes_recomendados, orcamento_filmes_recomendados, receita_filmes_recomendados, lucro_filmes_recomendados, elenco_filmes_recomendados, diretor_filmes_recomendados, titulo_filmes_recomendados, frase_filmes_recomendados= recomendars(dados, filtros)

    # Exibir o número total de filmes recomendados com estilo personalizado e centralizado
    st.markdown('<div class="centralizado">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:26px; font-weight:bold; text-align: center;">Total de Filmes Recomendados:</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:30px;font-weight:bold;color:#FFFF00; text-align: center;">{total_filmes_recomendados}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Exibir os títulos e sinopses traduzidas dos filmes recomendados

    for titulo, sinopse, ano, generos, idioma, votacao, duracao, orcamento, receita, lucro, elenco, diretor, frase in zip(titulos_filmes_recomendados, sinopse_filmes_recomendados, ano_filmes_recomendados, generos_filmes_recomendados, idioma_filmes_recomendados, votaçao_filmes_recomendados, duracao_filmes_recomendados, orcamento_filmes_recomendados, receita_filmes_recomendados, lucro_filmes_recomendados, elenco_filmes_recomendados, diretor_filmes_recomendados, frase_filmes_recomendados):
        
       
        sinopse_traduzida = traduzir_texto(sinopse) 
        titulo_traduzida = traduzir_texto(titulo)
        frase_traduzida = traduzir_texto(frase)
       
        if sinopse_traduzida and titulo_traduzida and frase_traduzida is not None:
            # Concatenar os gêneros em uma única string
            generos = dados.loc[dados['Título'] == titulo, ['gênero1', 'gênero2', 'gênero3']].values.tolist()[0]
            generos_str = ", ".join(filter(lambda x: x != 'Desconhecido', generos))

            # Aplicar a cor vermelha apenas aos valores dentro das chaves
            generos_html = ", ".join(f"<span style='color:#FF9999;'>{genero}</span>" for genero in generos_str.split(", "))

            # Aplicar a cor vermelha apenas aos valores dentro das chaves
            votacao_html = f"<span style='color:#FF9999;'>{votacao}</span>"
            idioma_html = f"<span style='color:#FF9999;'>{idioma}</span>"
            ano_html = f"<span style='color:#FF9999;'>{ano}</span>"
            # Converter duração para horas e minutos
            duracao_horas_minutos = converter_para_horas_minutos(duracao)
            duracao_html = f"<span style='font-size:16px; font-weight:italic; color:#FF9999;'>{duracao_horas_minutos}</span>"

            # Format orçamento, receita, and lucro using f-strings with comma separation
            orcamento_inteiro = int(orcamento)  # Convert to integer
            orcamento_formatado = f"<span style='font-size:16px; font-weight:italic; color:#FF9999;'>U$ {orcamento_inteiro:,d}</span>"

            receita_inteira = int(receita)
            receita_formatada = f"<span style='font-size:16px; font-weight:italic; color:#FF9999;'>U$ {receita_inteira:,d}</span>"

            lucro_inteiro = int(lucro)
            lucro_formatado = f"<span style='font-size:16px; font-weight:italic; color:#FF9999;'>U$ {lucro_inteiro:,d}</span>"

            st.markdown(f"<p style='font-size:28px; font-weight:bold; color:#6baed6;'>{titulo_traduzida}  <span style='font-size:18px; font-weight:italic; color:#FF9999;'>({titulo})</span>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:18px; font-weight:italic; font-family: helvetica;'>{frase_traduzida}</p>", unsafe_allow_html=True)


            
            st.markdown(f"<p style='font-size:17px; font-weight:italic;'>{sinopse_traduzida}</p>", unsafe_allow_html=True)
            
            
            # Supondo que `elenco` seja a string contendo o elenco completa
            elenco_html = ""
            for parte in elenco.split(";"):
                partes = parte.split("como")  # Divide a parte em duas: antes e depois de "como"
                for i, subparte in enumerate(partes):
                    if i < len(partes) - 1:
                        elenco_html += f"<span style='color:#FF9999;'>{subparte.strip()}</span> como "
                    else:
                        elenco_html += f"{subparte.strip()}; "

            # Remova o último ';' da string, se houver
            elenco_html = elenco_html.rstrip(";")

            diretor_html = f"<span style='font-size:16px; font-weight:italic; color:#FF9999;'>{diretor}</span>"    
            # Exibir os detalhes dos filmes em colunas
            col1, col2, col3 = st.columns(3)

            # Detalhes do filme: Gênero(s), Votação Média, Idioma
            col1.markdown(f"<p style='font-size:16px; font-weight:italic;'>Gênero(s): {generos_html}</p>", unsafe_allow_html=True)
            col1.markdown(f"<p style='font-size:16px; font-weight:italic;'>Votação Média: {votacao_html}</p>", unsafe_allow_html=True)
            col1.markdown(f"<p style='font-size:16px; font-weight:italic;'>Idioma: {idioma_html}</p>", unsafe_allow_html=True)

            # Detalhes do filme: Ano de Lançamento, Duração, Orçamento
            col2.markdown(f"<p style='font-size:16px; font-weight:italic;'>Ano de Lançamento: {ano_html}</p>", unsafe_allow_html=True)
            col2.markdown(f"<p style='font-size:16px; font-weight:italic;'>Duração: {duracao_html}</p>", unsafe_allow_html=True)
            col2.markdown(f"<p style='font-size:16px; font-weight:italic;'>Diretor(a): {diretor_html}</p>", unsafe_allow_html=True)
            # Detalhes do filme: Receita, Lucro do Filme
            if orcamento_inteiro != 0:
                orcamento_texto = f"Orçamento: <span style='color:#FF9999;'>U$ {orcamento_inteiro:,}</span>"
            else:
                orcamento_texto = "Orçamento: <span style='color:#FF9999;'>Sem informações</span>"

            if receita_inteira != 0:
                receita_texto = f"Receita: U$ <span style='color:#FF9999;'>{receita_inteira:,}</span>"
            else:
                receita_texto = "Receita: <span style='color:#FF9999;'>Sem informações</span>"

            if lucro_inteiro != 0:
                lucro_texto = f"Lucro: U$ <span style='color:#FF9999;'>{lucro_inteiro:,}</span>"
            else:
                lucro_texto = "Lucro: <span style='color:#FF9999;'>Sem informações</span>"

            col3.markdown(f"<p style='font-size:16px; font-weight:italic;'>{orcamento_texto}</p>", unsafe_allow_html=True)
            col3.markdown(f"<p style='font-size:16px; font-weight:italic;'>{receita_texto}</p>", unsafe_allow_html=True)
            col3.markdown(f"<p style='font-size:16px; font-weight:italic;'>{lucro_texto}</p>", unsafe_allow_html=True)

            # Agora, você pode exibir o elenco com cores diferentes
            st.markdown(f"<p style='font-size:16px; font-weight:italic;'>Elenco: {elenco_html}</p>", unsafe_allow_html=True)

