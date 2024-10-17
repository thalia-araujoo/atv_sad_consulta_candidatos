import streamlit as st
import pandas as pd
import altair as alt

# Título da aplicação
st.title("Consultas dos candidatos das eleições de 2024")

# Componente de upload de arquivo
uploaded_files = st.file_uploader(
    "Escolha um arquivo CSV", type="csv", accept_multiple_files=True
)

# Exibe o conteúdo ou processa o arquivo após o upload
if uploaded_files is not None:
    try:
        for uploaded_file in uploaded_files:
            df = pd.read_csv(uploaded_file, encoding='ISO-8859-1', sep=';')

            # Exibe a prévia dos dados
            st.subheader(f"Candidatos do {df['SG_UF'].unique()[0]}")
            st.dataframe(df.head(), use_container_width=True)

            # Exibe o número total de linhas e colunas
            st.write(f"Total de linhas: {df.shape[0]}")
            st.write(f"Total de colunas: {df.shape[1]}")

            st.subheader("Distribuição por grau de instrução")
            grau_instrucao_count = df.groupby('DS_GRAU_INSTRUCAO').size().reset_index(name='count')
            st.bar_chart(grau_instrucao_count.set_index('DS_GRAU_INSTRUCAO'), stack=False)

            # Verificar se as colunas DS_GENERO e DS_GRAU_INSTRUCAO estão presentes no dataset
            if 'DS_GENERO' not in df.columns or 'DS_GRAU_INSTRUCAO' not in df.columns:
                st.error("O arquivo não contém as colunas necessárias ('DS_GENERO', 'DS_GRAU_INSTRUCAO').")
            else:
                # Agrupar os dados por gênero e grau de instrução e contar as ocorrências
                genero_grau_count = df.groupby(['DS_GENERO', 'DS_GRAU_INSTRUCAO']).size().reset_index(name='count')

                # Criar o gráfico com Altair
                st.subheader("Gráfico de Barras - Gênero vs Grau de Instrução (Lado a Lado)")
                chart = alt.Chart(genero_grau_count).mark_bar().encode(
                    x=alt.X('DS_GRAU_INSTRUCAO:N', title='Grau de Instrução'),  # O eixo X será o grau de instrução
                    y=alt.Y('count:Q', title='Contagem'),  # O eixo Y será a contagem
                    color='DS_GENERO:N',  # Coloração por gênero
                    tooltip=['DS_GRAU_INSTRUCAO', 'DS_GENERO', 'count']  # Tooltip para exibir detalhes
                ).properties(
                    title='Distribuição de Gênero por Grau de Instrução',  # Título do gráfico
                    width=500,  # Largura do gráfico
                    height=400   # Altura do gráfico
                ).configure_axis(
                    labelFontSize=12,
                    titleFontSize=14
                ).configure_legend(
                    labelFontSize=12
                )

                # Exibir o gráfico
                st.altair_chart(chart, use_container_width=True)

            # Verifica se a coluna CD_COR_RACA está presente no dataset
            if 'CD_COR_RACA' not in df.columns:
                st.error("O arquivo não contém a coluna necessária ('CD_COR_RACA').")
            else:
                # Agrupar os dados por cor/raça e contar as ocorrências
                cor_raca_count = df['DS_COR_RACA'].value_counts().reset_index()
                cor_raca_count.columns = ['Cor/Raça', 'Count']

                # Criar o gráfico de pizza com Altair
                st.subheader("Gráfico de Pizza - Distribuição de Cor/Raça dos Candidatos")
                chart = alt.Chart(cor_raca_count).mark_arc(innerRadius=90).encode(
                    theta=alt.Theta(field='Count', type='quantitative', title='Contagem'),
                    color=alt.Color(field='Cor/Raça', type='nominal', title='Cor/Raça', legend=alt.Legend(title='Cor/Raça')),
                    tooltip=['Cor/Raça', 'Count']
                ).properties(
                    title='Distribuição de Cor/Raça dos Candidatos',  # Título do gráfico
                    width=400,  # Largura do gráfico
                    height=400   # Altura do gráfico
                )

                # Exibir o gráfico
                st.altair_chart(chart, use_container_width=True)

            # Verifica se a coluna CD_GENERO está presente no dataset
            if 'CD_GENERO' not in df.columns:
                st.error("O arquivo não contém a coluna necessária ('CD_GENERO').")
            else:
                # Agrupar os dados por Homem/Mulher e contar as ocorrências
                homem_mulher_count = df['DS_GENERO'].value_counts().reset_index()
                homem_mulher_count.columns = ['Homem/Mulher', 'Count']

                # Criar o gráfico de pizza com Altair
                st.subheader("Gráfico de Pizza - Distribuição de Homem/Mulher dos Candidatos")
                chart = alt.Chart(homem_mulher_count).mark_arc(innerRadius=90).encode(
                    theta=alt.Theta(field='Count', type='quantitative', title='Contagem'),
                    color=alt.Color(field='Homem/Mulher', type='nominal', title='Homem/Mulher', legend=alt.Legend(title='Homem/Mulher')),
                    tooltip=['Homem/Mulher', 'Count']
                ).properties(
                    title='Distribuição de Homens e Mulheres dos Candidatos',  # Título do gráfico
                    width=400,  # Largura do gráfico
                    height=400   # Altura do gráfico
                )

                # Exibir o gráfico
                st.altair_chart(chart, use_container_width=True)
    
            # Verifica se as colunas necessárias estão presentes no dataset
            if 'SG_PARTIDO' not in df.columns or 'CD_GENERO' not in df.columns:
                st.error("O arquivo não contém as colunas necessárias ('SG_PARTIDO' ou 'CD_GENERO').")
            else:
                # Filtra apenas as mulheres
                mulheres_df = df[df['CD_GENERO'] == 2]  # Supondo que '2' representa mulheres

                # Agrupa os dados por partido e conta as ocorrências
                mulheres_por_partido = mulheres_df['SG_PARTIDO'].value_counts().reset_index()
                mulheres_por_partido.columns = ['Partido', 'Número de Mulheres']

                # Ordena os partidos do maior para o menor número de mulheres
                mulheres_por_partido = mulheres_por_partido.sort_values(by='Número de Mulheres', ascending=False)

                # Criar o gráfico de torres com Altair
                st.subheader("Gráfico de Torres - Mulheres por Partido")
                chart = alt.Chart(mulheres_por_partido).mark_bar().encode(
                    x=alt.X('Partido:N', title='Partido', sort='-y'),  # Partido no eixo x
                    y=alt.Y('Número de Mulheres:Q', title='Número de Mulheres'),  # Número de mulheres no eixo y
                    tooltip=['Partido', 'Número de Mulheres']
                ).properties(
                    title='Número de Mulheres por Partido',  # Título do gráfico
                    width=600,  # Largura do gráfico
                    height=400   # Altura do gráfico
                )

                # Exibir o gráfico
                st.altair_chart(chart, use_container_width=True)

            # Verifica se as colunas necessárias estão presentes no dataset
            if 'SG_PARTIDO' not in df.columns or 'CD_GENERO' not in df.columns:
                st.error("O arquivo não contém as colunas necessárias ('SG_PARTIDO' ou 'CD_GENERO').")
            else:
                # Agrupa os dados por partido e gênero
                genero_partido = df.groupby(['SG_PARTIDO', 'CD_GENERO']).size().reset_index(name='Contagem')

                # Mapeia 1 para homens e 2 para mulheres, assumindo que 'CD_GENERO' segue essa convenção
                genero_partido['Gênero'] = genero_partido['CD_GENERO'].map({1: 'Homens', 2: 'Mulheres'})

                # Criar o gráfico de torres lado a lado com Altair
                st.subheader("Gráfico de Torres - Homens e Mulheres por Partido")
                chart = alt.Chart(genero_partido).mark_bar().encode(
                    x=alt.X('SG_PARTIDO:N', title='Partido', sort='-y'),  # Partido no eixo x
                    y=alt.Y('Contagem:Q', title='Número de Pessoas'),  # Contagem no eixo y
                    color=alt.Color('Gênero:N', title='Gênero'),  # Colore por gênero (Homens/Mulheres)
                    tooltip=['SG_PARTIDO', 'Gênero', 'Contagem']
                ).properties(
                    title='Distribuição de Homens e Mulheres por Partido',  # Título do gráfico
                    width=600,  # Largura do gráfico
                    height=400   # Altura do gráfico
                )

                # Exibir o gráfico
                st.altair_chart(chart, use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {str(e)}")
