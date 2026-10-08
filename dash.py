import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

dados = pd.read_excel('dados.xlsx',sheet_name='Base de dados')

def visao_geral():
    st.title("Visão geral")
    col1,col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.metric("Total de participantes:",len(dados))
    
    with col2:
        with st.container(border=True):
            st.metric("Idade média dos paricipantes:",round(dados['Idade'].mean()))

    col3,col4 = st.columns(2)

    with col3:
        with st.container(border=True):
            st.metric('Renda mensal média:',f"R${dados['Renda Mensal'].mean():,.2f}")

    with col4:
        with st.container(border=True):
            st.metric('Gasto mensal médio',f"R${dados['Gasto mensal medio'].mean():,.2f}")
    
    st.subheader("Situação de endividamento")
    contagem = dados["Endividamento"].value_counts().reset_index()
    contagem.columns = ["Situação", "Quantidade"]

    fig = px.pie(
        contagem,
        names="Situação",
        values="Quantidade",
        hole=0.5
        )

    st.plotly_chart(fig, use_container_width=True)

def perfil_participante():
    st.title("Perfil dos participantes")
    col1,col2 = st.columns(2)

    with col1:
        st.subheader("Faixa etária")
        fig = px.histogram(dados,x='Idade',nbins=9)
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        contagem = dados["Genero"].value_counts().reset_index()
        contagem.columns = ["Gênero", "Quantidade"]
        st.subheader("Gênero")

        fig = px.pie(
        contagem,
        names="Gênero",
        values="Quantidade",
        hole=0.5
        )
        st.plotly_chart(fig, use_container_width=True)

    col3,col4 = st.columns(2)

    with col3:
        st.subheader("Fonte de renda")
        contagem = dados["Fonte de Renda"].value_counts().reset_index()
        contagem.columns = ["Fonte de Renda", "Quantidade"]
        fig = px.bar(
            contagem,
            x="Quantidade",
            y="Fonte de Renda",
            orientation="h",
            labels={"Quantidade": "Participantes"}
        )
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.subheader("Idade por gênero")
        fig = px.box(dados, x="Genero", y="Idade")
        st.plotly_chart(fig, use_container_width=True)
        
def renda_gasto():
    st.title("Renda e gasto")
    col1,col2,col3= st.columns(3)
    with col1:
        with st.container(border=True):
            st.metric('Renda mensal média:',f"R${dados['Renda Mensal'].mean():,.2f}")

    with col2:
        with st.container(border=True):
            st.metric('Gasto mensal médio:',f"R${dados['Gasto mensal medio'].mean():,.2f}")
    
    with col3:
        with st.container(border=True):
            st.metric('Poupança mensal média:',f"R$ {dados['Poupanca media mensal'].mean():,.2f}")
    
    col4,col5 = st.columns(2)
    with col4:
        st.subheader("Distribuição da renda")
        fig = px.histogram(dados, x="Renda Mensal", nbins=10)
        st.plotly_chart(fig, use_container_width=True)

    with col5:
        st.subheader("Distribuição dos gastos")
        fig = px.histogram(dados,x="Gasto mensal medio",nbins=10)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Renda x Gasto")
    fig = px.scatter(
        dados,
        x='Renda Mensal',
        y='Gasto mensal medio',
        color='Reserva financeira',
        color_discrete_map={"Sim": "#4C78A8","Não": "#B0B8C4"},
        trendline="ols",
        trendline_scope="overall",
        labels={
            "Renda Mensal": "Renda mensal (R$)",
            "Gasto mensal medio":"Gasto médio mensal (R$)",
            "Reserva financeira": "Possui reserva?"
        }
    )
    for trace in fig.data:
        if trace.mode and "lines" in trace.mode:
            trace.line.dash = "dash"
    
    st.plotly_chart(fig,use_container_width=True)

    st.subheader("Salário e gasto médio por gênero")
    dff = dados.groupby('Genero')[['Renda Mensal', 'Gasto mensal medio','Poupanca media mensal']].mean().reset_index()
    fig = px.bar(
        dff, 
        x="Genero", 
        y=["Renda Mensal", "Gasto mensal medio",'Poupanca media mensal'], 
        barmode="group", 
        labels={"value": "Valor (R$)", "variable": "Categoria"}
    )
    st.plotly_chart(fig,use_container_width=True)
    
    st.subheader("Comprometimento da Renda por Gênero")
    dados_limpos = dados.copy()
    medias_absolutas = dados_limpos.groupby('Genero')[['Renda Mensal', 'Gasto mensal medio', 'Poupanca media mensal']].mean().reset_index()

    medias_absolutas['Taxa de Gastos (%)'] = (medias_absolutas['Gasto mensal medio'] / medias_absolutas['Renda Mensal']) * 100
    medias_absolutas['Taxa de Poupança (%)'] = (medias_absolutas['Poupanca media mensal'] / medias_absolutas['Renda Mensal']) * 100

    fig_taxas = px.bar(
        medias_absolutas,
        x="Genero",
        y=['Taxa de Gastos (%)', 'Taxa de Poupança (%)'],
        barmode="group",
        labels={'value': 'Porcentagem da Renda (%)', 'variable': 'Indicador', 'Genero': ''}
    )
    st.plotly_chart(fig_taxas,use_container_width=True)

def endividamento():
    st.title("Endividamento")

    contagem = dados["Endividamento"].value_counts().reset_index()
    contagem.columns = ["Situação", "Quantidade"]

    col1,col2 = st.columns(2)

    with col1:
        st.subheader("Proporção de endividados")
        fig = px.pie(
            contagem,
            names="Situação",
            values="Quantidade",
            hole=0.5
        )
        st.plotly_chart(fig,use_container_width=True)
    
    with col2:
        st.subheader("Nível de endividamento")
        valores = dados["Nivel de endividamento"].value_counts().reset_index()
        valores.columns = ["Nível", "Quantidade"]
        fig = px.bar(
            valores,
            x="Nível",
            y="Quantidade",
            labels={"Nível": "Nível de endividamento"}
        )
        st.plotly_chart(fig,use_container_width=True)

    col3,col4 = st.columns(2)

    with col3:
        st.subheader("Quantidade de dívidas atrasadas")
        valores = dados["Quantidade de dividas atrasadas"].value_counts().sort_index().reset_index()
        valores.columns = ["Dívidas atrasadas", "Participantes"]
        fig = px.bar(
            valores,
            x="Dívidas atrasadas",
            y="Participantes"
        )
        st.plotly_chart(fig,use_container_width=True)

    with col4:
        st.subheader("Renda e gasto por endividamento")
        dff = dados.groupby("Endividamento")[["Renda Mensal", "Gasto mensal medio"]].mean().reset_index()
        fig = px.bar(
            dff,
            x="Endividamento",
            y=["Renda Mensal", "Gasto mensal medio"],
            barmode="group",
            labels={"value": "Valor médio (R$)", "variable": "Categoria", "Endividamento": "Possui dívidas?"}
        )
        st.plotly_chart(fig,use_container_width=True)

    st.subheader("Conhecimento financeiro por situação de endividamento")
    fig = px.histogram(
        dados,
        x="Nivel de conhecimento Financeiro",
        color="Endividamento",
        barmode="group",
        labels={
            "Nivel de conhecimento Financeiro": "Conhecimento financeiro",
            "Endividamento": "Possui dívidas?",
            "count": "Participantes"
        }
    )
    st.plotly_chart(fig,use_container_width=True)

def poupanca_reserva():
    st.title("Poupança e reserva")

    col1,col2 = st.columns(2)

    with col1:
        st.subheader("Participantes com reserva financeira")
        contagem = dados["Reserva financeira"].value_counts().reset_index()
        contagem.columns = ["Reserva", "Quantidade"]
        fig = px.pie(
            contagem,
            names="Reserva",
            values="Quantidade",
            hole=0.5
        )
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        st.subheader("Frequência com que guardam dinheiro")
        contagem = dados["Frequencia que guarda dinheiro"].value_counts().reset_index()
        contagem.columns = ["Frequência", "Quantidade"]
        fig = px.bar(
            contagem,
            x="Frequência",
            y="Quantidade",
            labels={"Frequência": "Frequência de poupança"}
        )
        st.plotly_chart(fig,use_container_width=True)

    col3,col4 = st.columns(2)

    with col3:
        st.subheader("Distribuição da poupança mensal")
        fig = px.histogram(
            dados,
            x="Poupanca media mensal",
            nbins=10,
            labels={"Poupanca media mensal": "Poupança mensal (R$)"}
        )
        st.plotly_chart(fig,use_container_width=True)

    with col4:
        st.subheader("Poupança média por reserva financeira")
        dff = dados.groupby("Reserva financeira")["Poupanca media mensal"].mean().reset_index()
        fig = px.bar(
            dff,
            x="Reserva financeira",
            y="Poupanca media mensal",
            labels={
                "Reserva financeira": "Possui reserva?",
                "Poupanca media mensal": "Poupança média (R$)"
            }
        )
        st.plotly_chart(fig,use_container_width=True)

    st.subheader("Frequência de poupança por gênero")
    fig = px.histogram(
        dados,
        x="Frequencia que guarda dinheiro",
        color="Genero",
        barmode="group",
        labels={
            "Frequencia que guarda dinheiro": "Frequência de poupança",
            "Genero": "Gênero",
            "count": "Participantes"
        }
    )
    st.plotly_chart(fig,use_container_width=True)

def investimentos_conhecimento():
    st.title("Investimentos e conhecimento financeiro")

    col1,col2 = st.columns(2)

    with col1:
        st.subheader("Quantidade de investimentos")
        contagem = dados["Quantidade de investimentos"].value_counts().sort_index().reset_index()
        contagem.columns = ["Investimentos", "Participantes"]
        fig = px.bar(
            contagem,
            x="Investimentos",
            y="Participantes"
        )
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        st.subheader("Nível de conhecimento financeiro")
        contagem = dados["Nivel de conhecimento Financeiro"].value_counts().reset_index()
        contagem.columns = ["Conhecimento", "Participantes"]
        fig = px.bar(
            contagem,
            x="Conhecimento",
            y="Participantes"
        )
        st.plotly_chart(fig,use_container_width=True)

    col3,col4 = st.columns(2)

    with col3:
        st.subheader("Investimentos por conhecimento financeiro")
        dff = dados.groupby("Nivel de conhecimento Financeiro")["Quantidade de investimentos"].mean().reset_index()
        fig = px.bar(
            dff,
            x="Nivel de conhecimento Financeiro",
            y="Quantidade de investimentos",
            labels={
                "Nivel de conhecimento Financeiro": "Conhecimento financeiro",
                "Quantidade de investimentos": "Média de investimentos"
            }
        )
        st.plotly_chart(fig,use_container_width=True)

    with col4:
        st.subheader("Investimentos por gênero")
        dff = dados.groupby("Genero")["Quantidade de investimentos"].mean().reset_index()
        fig = px.bar(
            dff,
            x="Genero",
            y="Quantidade de investimentos",
            labels={
                "Genero": "Gênero",
                "Quantidade de investimentos": "Média de investimentos"
            }
        )
        st.plotly_chart(fig,use_container_width=True)

def habitos_objetivos():
    st.title("Hábitos financeiros e objetivos")

    col1,col2 = st.columns(2)

    with col1:
        st.subheader("Método de controle de gastos")
        contagem = dados["Controle de gastos"].value_counts().reset_index()
        contagem.columns = ["Método", "Participantes"]
        fig = px.bar(
            contagem,
            x="Participantes",
            y="Método",
            orientation="h"
        )
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        st.subheader("Frequência do controle de gastos")
        contagem = dados["Frequencia do controle"].value_counts().reset_index()
        contagem.columns = ["Frequência", "Participantes"]
        fig = px.bar(
            contagem,
            x="Frequência",
            y="Participantes"
        )
        st.plotly_chart(fig,use_container_width=True)

    col3,col4 = st.columns(2)

    with col3:
        st.subheader("Frequência de gastos não planejados")
        contagem = dados["Frequencia de gastos nao planejados"].value_counts().reset_index()
        contagem.columns = ["Frequência", "Participantes"]
        fig = px.bar(
            contagem,
            x="Frequência",
            y="Participantes"
        )
        st.plotly_chart(fig,use_container_width=True)

    with col4:
        st.subheader("Frequência do controle por gênero")
        fig = px.histogram(
        dados,
        x="Frequencia do controle",
        color="Genero",
        barmode="group",
        labels={
            "Frequencia do controle": "Frequência do controle",
            "Genero": "Gênero",
            "count": "Participantes"
        }
    )
        st.plotly_chart(fig,use_container_width=True)
    
    st.subheader("Principais objetivos financeiros")
    contagem = dados["Principal objetivo financeiro"].value_counts().reset_index()
    contagem.columns = ["Objetivo", "Participantes"]
    fig = px.pie(
        contagem,
        names="Objetivo",
        values="Participantes",
        hole=0.5,
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)


with st.sidebar:
    st.subheader("Navegação")

    pagina = st.radio(
        "Selecione uma página:",
        [
            "Visão geral",
            "Perfil dos participantes",
            "Renda e gasto",
            "Endividamento",
            "Poupança e reserva",
            "Investimentos e conhecimento",
            "Hábitos e objetivos"
        ],
        index=0
    )

if pagina == "Visão geral":
    visao_geral()
elif pagina == "Perfil dos participantes":
    perfil_participante()
elif pagina == "Renda e gasto":
    renda_gasto()
elif pagina == "Endividamento":
    endividamento()
elif pagina == "Poupança e reserva":
    poupanca_reserva()
elif pagina == "Investimentos e conhecimento":
    investimentos_conhecimento()
elif pagina == "Hábitos e objetivos":
    habitos_objetivos()