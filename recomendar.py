import streamlit as st

def recomendars(dados, filtros):
    orçamento = filtros.get('orçamento', (float(dados['Orçamento'].min()), float(dados['Orçamento'].max())))
    popularidade = filtros.get('popularidade', (float(dados['Popularidade'].min()), float(dados['Popularidade'].max())))
    receita = filtros.get('receita', (float(dados['Receita'].min()), float(dados['Receita'].max())))
    votação = filtros.get('Votação Média', (float(dados['Votação'].min()), float(dados['Votação'].max())))  
    votos = filtros.get('Quantidade de votos', (float(dados['Votos'].min()), float(dados['Votos'].max())))  
    lucro = filtros.get('Lucro', (float(dados['Lucro'].min()), float(dados['Lucro'].max())))  
    Duração = filtros.get('Duração', (float(dados['Duração'].min()), float(dados['Duração'].max())))  
    generos_selecionados = filtros.get('Gênero(s)', [])
    idioma_selecionado = filtros.get('idioma', None)
    ano_lancamento = filtros.get('ano', (int(dados['Ano'].min()), int(dados['Ano'].max())))
    elenco_selecionado = filtros.get('Elenco', '')
    diretor_selecionado = filtros.get('Diretor', '')
    titulo_selecionado = filtros.get('Título', '')
   
    filmes_recomendados = dados[
        (dados['Orçamento'] >= orçamento[0]) & (dados['Orçamento'] <= orçamento[1]) &
        (dados['Popularidade'] >= popularidade[0]) & (dados['Popularidade'] <= popularidade[1]) &
        (dados['Receita'] >= receita[0]) & (dados['Receita'] <= receita[1]) &
        (dados['Votação'] >= votação[0]) & (dados['Votação'] <= votação[1]) &
        (dados['Votos'] >= votos[0]) & (dados['Votos'] <= votos[1]) &
        (dados['Lucro'] >= lucro[0]) & (dados['Lucro'] <= lucro[1]) &
        (dados['Duração'] >= Duração[0]) & (dados['Duração'] <= Duração[1]) &
        (dados[['gênero1', 'gênero2', 'gênero3']].apply(lambda x: set(x) >= set(generos_selecionados), axis=1)) &
        ((dados['Idioma'] == idioma_selecionado) if idioma_selecionado else True) &
        (((dados['Ano'] >= ano_lancamento[0]) if isinstance(ano_lancamento, tuple) else (dados['Ano'] == ano_lancamento)) if ano_lancamento else True) &
        (dados['Elenco'].str.contains(elenco_selecionado, case=False)) &
        (dados['Diretor'].str.contains(diretor_selecionado, case=False)) &
        (dados['Título'].str.contains(titulo_selecionado, case=False))
    ]
    # Verificar se existem filmes recomendados
    if len(filmes_recomendados) == 0:
        st.warning("Nenhum filme encontrado com os filtros fornecidos.")
        return [], 0, [], [], [], [], [], [], [], [], [], [], [], []  # Retorna listas vazias para todos os valores


    total_filmes_recomendados = len(filmes_recomendados)
    titulos_filmes_recomendados = filmes_recomendados['Título'].tolist()
    sinopse_filmes_recomendados = filmes_recomendados['Sinopse'].tolist()
    ano_filmes_recomendados = filmes_recomendados['Ano'].tolist()
    generos_filmes_recomendados = dados.loc[filmes_recomendados.index, ['gênero1', 'gênero2', 'gênero3']].apply(lambda x: ', '.join(filter(None, x)), axis=1).tolist()

    idioma_filmes_recomendados = filmes_recomendados['Idioma'].tolist()
    votaçao_filmes_recomendados = filmes_recomendados['Votação'].tolist()
    duracao_filmes_recomendados = filmes_recomendados['Duração'].tolist()
    orcamento_filmes_recomendados = filmes_recomendados['Orçamento'].tolist()
    receita_filmes_recomendados = filmes_recomendados['Receita'].tolist()
    lucro_filmes_recomendados = filmes_recomendados['Lucro'].tolist()
    elenco_filmes_recomendados = filmes_recomendados['Elenco'].tolist()
    diretor_filmes_recomendados = filmes_recomendados['Diretor'].tolist()
    titulo_filmes_recomendados = filmes_recomendados['Título'].tolist()
    frase_filmes_recomendados = filmes_recomendados['FraseDestaque'].tolist()
    
    
    return titulos_filmes_recomendados, total_filmes_recomendados, sinopse_filmes_recomendados, ano_filmes_recomendados, generos_filmes_recomendados, idioma_filmes_recomendados, votaçao_filmes_recomendados, duracao_filmes_recomendados, orcamento_filmes_recomendados, receita_filmes_recomendados, lucro_filmes_recomendados, elenco_filmes_recomendados, diretor_filmes_recomendados, titulo_filmes_recomendados, frase_filmes_recomendados
