# app.py
import streamlit as st
import pandas as pd
from db_sqlite import create_tables, insert_estado, insert_cidade, list_estados, list_cidades_by_estado
from db_mongo import insert_local, find_locais_by_city, find_all_locais, find_locais_nearby

st.set_page_config(page_title='Persistência Poliglota - AV1', layout='wide')

# inicializa sqlite
create_tables()

st.title('Projeto: Persistência Poliglota (SQLite + MongoDB) e Geoprocessamento')

with st.sidebar:
    st.header('Cadastrar')
    tab = st.radio('Escolha o que cadastrar:', ['Estado', 'Cidade', 'Local (MongoDB)'])

    if tab == 'Estado':
        nome_estado = st.text_input('Nome do estado')
        if st.button('Salvar Estado'):
            if nome_estado.strip():
                _id = insert_estado(nome_estado.strip())
                st.success(f'Estado salvo com id {_id}')
            else:
                st.error('Informe o nome do estado')

    if tab == 'Cidade':
        estados = list_estados()
        estados_map = {e[1]: e[0] for e in estados}
        nome_cidade = st.text_input('Nome da cidade', key='cidade_nome')
        estado_sel = st.selectbox('Estado', ['-- selecione --'] + [e[1] for e in estados])
        if st.button('Salvar Cidade'):
            if nome_cidade.strip() and estado_sel != '-- selecione --':
                estado_id = estados_map[estado_sel]
                cid = insert_cidade(nome_cidade.strip(), estado_id)
                st.success(f'Cidade salva com id {cid}')
            else:
                st.error('Informe nome da cidade e selecione estado')

    if tab == 'Local (MongoDB)':
        st.write('Cadastre um ponto de interesse (será salvo no MongoDB)')
        nome_local = st.text_input('Nome do local', key='local_nome')
        descricao = st.text_area('Descrição', key='local_desc')
        estados = list_estados()
        estados_map = {e[1]: e[0] for e in estados}
        if estados:
            estado_selected = st.selectbox('Estado (do local)', ['-- selecione --'] + [e[1] for e in estados], key='local_estado')
            cidade_options = []
            if estado_selected != '-- selecione --':
                estado_id = estados_map[estado_selected]
                cidade_options = [c[1] for c in list_cidades_by_estado(estado_id)]
        else:
            estado_selected = '-- selecione --'
            cidade_options = []

        cidade_selected = st.selectbox('Cidade (do local)', ['-- selecione --'] + cidade_options, key='local_cidade')
        lat = st.number_input('Latitude', format='%.6f', key='lat')
        lon = st.number_input('Longitude', format='%.6f', key='lon')

        if st.button('Salvar Local (MongoDB)'):
            if not nome_local.strip():
                st.error('Informe nome do local')
            elif cidade_selected == '-- selecione --':
                st.error('Selecione a cidade do local')
            else:
                doc = {
                    'nome_local': nome_local.strip(),
                    'descricao': descricao.strip(),
                    'cidade': cidade_selected,
                    'estado': estado_selected,
                    'coordenadas': {'latitude': float(lat), 'longitude': float(lon)}
                }
                _id = insert_local(doc)
                st.success(f'Local salvo no MongoDB com id {_id}')

# Main area
st.header('Consultas e Mapas')

c1, c2 = st.columns([1, 1])

with c1:
    st.subheader('Consultar locais por cidade')
    estados = list_estados()
    estados_map = {e[1]: e[0] for e in estados}
    estado_sel = st.selectbox('Estado (para consulta)', ['-- selecione --'] + [e[1] for e in estados], key='consulta_estado')
    if estado_sel != '-- selecione --':
        estado_id = estados_map[estado_sel]
        cidades = list_cidades_by_estado(estado_id)
        cidade_names = [c[1] for c in cidades]
        cidade_sel = st.selectbox('Cidade (para consulta)', ['-- selecione --'] + cidade_names, key='consulta_cidade')
        if cidade_sel != '-- selecione --':
            locais = find_locais_by_city(cidade_sel)
            st.write(f'Encontrados {len(locais)} locais em {cidade_sel}')
            if locais:
                df = pd.DataFrame([{
                    'nome_local': l.get('nome_local'),
                    'descricao': l.get('descricao'),
                    'latitude': l.get('coordenadas', {}).get('latitude'),
                    'longitude': l.get('coordenadas', {}).get('longitude')
                } for l in locais])
                st.dataframe(df)
                # st.map espera colunas 'lat' e 'lon'
                st.map(df.rename(columns={'latitude':'lat','longitude':'lon'}).dropna(subset=['lat','lon']))

with c2:
    st.subheader('Buscar locais próximos (raio em km)')
    lat0 = st.number_input('Latitude central', format='%.6f', key='search_lat')
    lon0 = st.number_input('Longitude central', format='%.6f', key='search_lon')
    radius = st.number_input('Raio (km)', value=10.0, format='%.1f', key='radius')
    if st.button('Buscar próximos'):
        if lat0 == 0 and lon0 == 0:
            st.warning('Informe coordenadas diferentes de 0')
        else:
            nearby = find_locais_nearby(lat0, lon0, float(radius))
            st.write(f'Encontrados {len(nearby)} locais em até {radius} km')
            if nearby:
                df2 = pd.DataFrame([{
                    'nome_local': l.get('nome_local'),
                    'descricao': l.get('descricao'),
                    'latitude': l.get('coordenadas', {}).get('latitude'),
                    'longitude': l.get('coordenadas', {}).get('longitude'),
                    'dist_km': l.get('_distance_km')
                } for l in nearby])
                st.dataframe(df2)
                st.map(df2.rename(columns={'latitude':'lat','longitude':'lon'}).dropna(subset=['lat','lon']))

st.markdown('---')
st.subheader('Todos os locais (visualização rápida)')
all_locais = find_all_locais()
if all_locais:
    df_all = pd.DataFrame([{
        'nome_local': l.get('nome_local'),
        'descricao': l.get('descricao'),
        'cidade': l.get('cidade'),
        'estado': l.get('estado'),
        'latitude': l.get('coordenadas', {}).get('latitude'),
        'longitude': l.get('coordenadas', {}).get('longitude')
    } for l in all_locais])
    st.dataframe(df_all)
    st.map(df_all.rename(columns={'latitude':'lat','longitude':'lon'}).dropna(subset=['lat','lon']))
else:
    st.info('Nenhum local cadastrado no MongoDB ainda.')

st.info('Dica: preencha alguns Estados e Cidades na barra lateral para poder cadastrar Locais no MongoDB.')
