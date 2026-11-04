# app.py
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import json
import time
import plotly.express as px
from core.map_data import get_brazil_states_graph
from core.graph_coloring import welsh_powell_coloring, dsatur_coloring, validate_coloring

st.set_page_config(page_title="Coloração de Mapas - Teoria dos Grafos", layout="wide")

st.title("🗺️ Aplicação Prática: Coloração de Mapas e Grafos")
st.markdown("**Tema 8:** Coloração de Grafos aplicada à alocação de recursos geográficos sem conflitos.")

# Sidebar para controles
st.sidebar.header("⚙️ Painel de Controle")

modo_execucao = st.sidebar.radio("Selecione o Modo:", ["Visualização Principal", "Análise de Estresse (Benchmark)"])

if modo_execucao == "Visualização Principal":
    tipo_instancia = st.sidebar.selectbox(
        "Origem dos Dados:",
        ["Mapa do Brasil (Completo - 27 estados)", "Arquivo JSON Externo (Casos de Teste)", "Grafo Completo K5 (Desafio)"]
    )

    G = nx.Graph()

    if "Brasil" in tipo_instancia:
        adj = get_brazil_states_graph()
        for state, neighbors in adj.items():
            for n in neighbors:
                G.add_edge(state, n)
    elif "JSON" in tipo_instancia:
        try:
            with open("data/custom_graphs.json", "r", encoding="utf-8") as f:
                data_dict = json.load(f)
            nome_grafo = st.sidebar.selectbox("Selecione a instância do arquivo:", list(data_dict.keys()))
            adj = data_dict[nome_grafo]
            for node, neighbors in adj.items():
                for n in neighbors:
                    G.add_edge(node, n)
        except FileNotFoundError:
            st.sidebar.error("Arquivo data/custom_graphs.json não encontrado!")
    else:
        G = nx.complete_graph(5, create_using=nx.Graph())
        mapping = {i: f"V{i+1}" for i in range(5)}
        G = nx.relabel_nodes(G, mapping)

    algoritmo_escolhido = st.sidebar.selectbox(
        "Escolha o Algoritmo de Coloração:",
        ["Comparar Ambos (Welsh-Powell vs DSATUR)", "Welsh-Powell", "DSATUR"]
    )

    velocidade_animacao = st.sidebar.slider("Velocidade da Animação (segundos):", 0.0, 1.0, 0.1)

    st.sidebar.markdown(f"---")
    st.sidebar.info(f"**Estatísticas do Grafo:**\n- Vértices: {G.number_of_nodes()}\n- Arestas: {G.number_of_edges()}")

    # Execução e Medição de Tempo
    res_wp, res_dsat = None, None
    tempo_wp, tempo_dsat = 0, 0

    if algoritmo_escolhido in ["Welsh-Powell", "Comparar Ambos (Welsh-Powell vs DSATUR)"]:
        inicio = time.time()
        res_wp = welsh_powell_coloring(G)
        tempo_wp = (time.time() - inicio) * 1000
        cores_wp = max(res_wp.values()) + 1
        val_wp, msg_wp = validate_coloring(G, res_wp)

    if algoritmo_escolhido in ["DSATUR", "Comparar Ambos (Welsh-Powell vs DSATUR)"]:
        inicio = time.time()
        res_dsat = dsatur_coloring(G)
        tempo_dsat = (time.time() - inicio) * 1000
        cores_dsat = max(res_dsat.values()) + 1
        val_dsat, msg_dsat = validate_coloring(G, res_dsat)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Resultados e Análise de Desempenho")
        
        if res_wp is not None:
            st.markdown(f"**Algoritmo Welsh-Powell:**")
            st.write(f"- Cores utilizadas: `{cores_wp}`")
            st.write(f"- Tempo de execução: `{tempo_wp:.4f} ms`")
            st.write(f"- Validação: `{msg_wp}`")
            st.markdown("---")

        if res_dsat is not None:
            st.markdown(f"**Algoritmo DSATUR:**")
            st.write(f"- Cores utilizadas: `{cores_dsat}`")
            st.write(f"- Tempo de execução: `{tempo_dsat:.4f} ms`")
            st.write(f"- Validação: `{msg_dsat}`")

    # Seleção de resultado para exibição
    coloring_to_display = res_wp if (res_wp is not None) else res_dsat

    with col2:
        st.subheader("🎨 Visualização Gráfica Passo a Passo")
        
        btn_animar = st.button("▶️ Executar Coloração Passo a Passo")
        
        fig, ax = plt.subplots(figsize=(8, 6))
        palette = ['#FF6B6B', '#4D96FF', '#6BCB77', '#FFD93D', '#9370DB', '#FF8C00', '#00CED1']
        pos = nx.spring_layout(G, seed=42)

        plot_spot = st.empty()

        if btn_animar:
            current_colors = {}
            for node in G.nodes():
                current_colors[node] = coloring_to_display[node]
                
                color_map = []
                for n in G.nodes():
                    if n in current_colors:
                        c_idx = current_colors[n] % len(palette)
                        color_map.append(palette[c_idx])
                    else:
                        color_map.append('#D3D3D3') # Cor cinza para não coloridos
                
                fig, ax = plt.subplots(figsize=(8, 6))
                nx.draw(
                    G, pos, with_labels=True, node_color=color_map, 
                    node_size=700, font_size=10, font_weight='bold', 
                    edge_color='gray', ax=ax
                )
                plot_spot.pyplot(fig)
                plt.close(fig)
                time.sleep(velocidade_animacao)
        else:
            color_map = [palette[coloring_to_display.get(n, 0) % len(palette)] for n in G.nodes()]
            nx.draw(
                G, pos, with_labels=True, node_color=color_map, 
                node_size=700, font_size=10, font_weight='bold', 
                edge_color='gray', ax=ax
            )
            plot_spot.pyplot(fig)
            plt.close(fig)

    # Tabela detalhada
    st.markdown("---")
    st.subheader("📋 Tabela de Atribuição de Cores")
    df_res = pd.DataFrame(list(coloring_to_display.items()), columns=['Vértice / Região', 'Cor Atribuída (ID)'])
    df_res['Cor Atribuída (ID)'] = df_res['Cor Atribuída (ID)'] + 1 
    st.dataframe(df_res.sort_values(by='Cor Atribuída (ID)').reset_index(drop=True), use_container_width=True)

else:
    st.subheader("📈 Teste de Estresse e Comparativo de Escala")
    st.markdown("Esta seção gera grafos sintéticos aleatórios de dimensões crescentes para comparar a eficiência do **Welsh-Powell** vs **DSATUR**.")
    
    max_nodes = st.slider("Selecione o limite de Vértices para o Teste:", 10, 150, 50, step=10)
    
    if st.button("🚀 Iniciar Teste de Desempenho"):
        dados_benchmark = []
        progress_bar = st.progress(0)
        
        node_sizes = list(range(10, max_nodes + 1, 10))
        for idx, n_nodes in enumerate(node_sizes):
            # Gerar grafo aleatório Erdos-Renyi
            G_bench = nx.erdos_renyi_graph(n=n_nodes, p=0.2, seed=42)
            
            # WP
            t0 = time.time()
            res_wp = welsh_powell_coloring(G_bench)
            t_wp = (time.time() - t0) * 1000
            
            # DSATUR
            t0 = time.time()
            res_dsat = dsatur_coloring(G_bench)
            t_dsat = (time.time() - t0) * 1000
            
            dados_benchmark.append({"Vértices": n_nodes, "Tempo (ms)": t_wp, "Algoritmo": "Welsh-Powell"})
            dados_benchmark.append({"Vértices": n_nodes, "Tempo (ms)": t_dsat, "Algoritmo": "DSATUR"})
            
            progress_bar.progress((idx + 1) / len(node_sizes))
            
        df_bench = pd.DataFrame(dados_benchmark)
        fig_plotly = px.line(df_bench, x="Vértices", y="Tempo (ms)", color="Algoritmo", markers=True, title="Desempenho em Escala: Welsh-Powell vs DSATUR")
        st.plotly_chart(fig_plotly, use_container_width=True)