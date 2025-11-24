import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="⚽ Soccer Prediction Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Datos directamente en el código (para evitar problemas con archivos JSON)
matches_data = {
    'last_updated': '2025-11-23 11:00:00',
    'matches': [
        {
            'match_id': 'ARS-TOT',
            'home_team': 'Arsenal',
            'away_team': 'Tottenham Hotspur',
            'league': 'Premier League',
            'date': '2025-11-23',
            'time': '20:45',
            'home_elo': 94,
            'away_elo': 88,
            'home_tilt': -2.8,
            'away_tilt': -1.7,
            'home_rank': 18,
            'away_rank': 88,
            'home_country_rank': 2,
            'away_country_rank': 9,
            'home_expected_goals': 2.1,
            'away_expected_goals': 1.2
        },
        {
            'match_id': 'INT-MIL',
            'home_team': 'Inter',
            'away_team': 'Milan',
            'league': 'Serie A',
            'date': '2025-11-23',
            'time': '20:45',
            'home_elo': 94,
            'away_elo': 91,
            'home_tilt': 7.1,
            'away_tilt': -1.2,
            'home_rank': 19,
            'away_rank': 45,
            'home_country_rank': 2,
            'away_country_rank': 5,
            'home_expected_goals': 1.8,
            'away_expected_goals': 1.4
        },
        {
            'match_id': 'ELC-RMA',
            'home_team': 'Elche',
            'away_team': 'Real Madrid',
            'league': 'La Liga',
            'date': '2025-11-23',
            'time': '20:45',
            'home_elo': 80,
            'away_elo': 473,
            'home_tilt': -4.1,
            'away_tilt': 21,
            'home_rank': 21,
            'away_rank': 1,
            'home_expected_goals': 0.73,
            'away_expected_goals': 2.8
        }
    ]
}

predictions_data = {
    'ARS-TOT': {
        'probabilities': {
            'home_win': 65.2,
            'draw': 19.7,
            'away_win': 15.1
        },
        'exact_scores': {
            '1-0': 10.2, '2-0': 10.8, '2-1': 9.9, '3-0': 7.7, '3-1': 7.0,
            '0-0': 5.5, '1-1': 8.7, '0-1': 12.0, '1-2': 9.4, '2-2': 3.4
        },
        'handicap': {
            '+1': 23.8, '0': 65.2, '-1': 19.7, '-2': 10.2
        },
        'analysis': {
            'confidence': 'high',
            'expected_goals_total': 3.3,
            'goal_expectation': 'high',
            'recommendation': 'PREDICCIÓN SÓLIDA'
        }
    },
    'INT-MIL': {
        'probabilities': {
            'home_win': 59.4,
            'draw': 20.9,
            'away_win': 19.7
        },
        'exact_scores': {
            '1-0': 8.5, '2-0': 9.2, '2-1': 8.1, '3-0': 6.5, '3-1': 5.8,
            '0-0': 6.2, '1-1': 7.9, '0-1': 10.5, '1-2': 8.2, '2-2': 2.8
        },
        'handicap': {
            '+1': 21.5, '0': 59.4, '-1': 22.1, '-2': 11.8
        },
        'analysis': {
            'confidence': 'medium',
            'expected_goals_total': 3.2,
            'goal_expectation': 'high',
            'recommendation': 'PREDICCIÓN MODERADA'
        }
    },
    'ELC-RMA': {
        'probabilities': {
            'home_win': 11.1,
            'draw': 18.3,
            'away_win': 70.6
        },
        'exact_scores': {
            '0-1': 12.0, '0-2': 8.5, '1-2': 9.4, '0-3': 5.2, '1-3': 4.1,
            '1-1': 8.7, '0-0': 5.5, '1-0': 4.0, '2-1': 3.2, '2-2': 3.4
        },
        'handicap': {
            '+1': 8.1, '+2': 2.4, '0': 11.1, '-1': 24.3
        },
        'analysis': {
            'confidence': 'very_high',
            'expected_goals_total': 3.53,
            'goal_expectation': 'high',
            'recommendation': 'PREDICCIÓN MUY SÓLIDA'
        }
    }
}

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .match-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #1f77b4;
    }
    .prediction-high {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
    }
    .prediction-medium {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
    }
    .prediction-low {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
    }
    .team-box {
        background: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown('<h1 class="main-header">⚽ Soccer Prediction Dashboard</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("🎯 Configuración")
    
    # Selector de partido
    selected_match = st.selectbox(
        "Selecciona un partido:",
        ["Todos los Partidos", "Arsenal vs Tottenham", "Inter vs Milan", "Elche vs Real Madrid"]
    )
    
    # Filtros
    st.subheader("🔍 Filtros")
    show_high_confidence = st.checkbox("Solo predicciones de alta confianza", value=False)
    min_confidence = st.slider("Confianza mínima (%)", 0, 100, 40)
    
    # Información
    st.subheader("ℹ️ Información")
    st.info("""
    Predicciones basadas en:
    - **Sistema ELO** de rating
    - **Machine Learning**
    - **Análisis estadístico**
    """)

# Pestañas principales
tab1, tab2, tab3 = st.tabs(["🏠 Dashboard Principal", "📊 Análisis Detallado", "📈 Comparativas"])

with tab1:
    st.header("🎯 Resumen de Predicciones del Día")
    
    # Mostrar todos los partidos
    for match in matches_data['matches']:
        match_id = match['match_id']
        prediction = predictions_data[match_id]
        
        # Determinar predicción principal
        home_prob = prediction['probabilities']['home_win']
        draw_prob = prediction['probabilities']['draw']
        away_prob = prediction['probabilities']['away_win']
        
        max_prob = max(home_prob, draw_prob, away_prob)
        if max_prob == home_prob:
            main_prediction = f"Victoria del {match['home_team']}"
            confidence = home_prob
            pred_type = 'home_win'
        elif max_prob == draw_prob:
            main_prediction = "Empate"
            confidence = draw_prob
            pred_type = 'draw'
        else:
            main_prediction = f"Victoria del {match['away_team']}"
            confidence = away_prob
            pred_type = 'away_win'
        
        # Aplicar filtros
        if show_high_confidence and confidence < 60:
            continue
        if confidence < min_confidence:
            continue
        
        # Determinar clase CSS según confianza
        if confidence >= 60:
            css_class = "prediction-high"
        elif confidence >= 45:
            css_class = "prediction-medium"
        else:
            css_class = "prediction-low"
        
        # Tarjeta del partido
        with st.container():
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"""
                <div class="match-card {css_class}">
                    <h3>{match['home_team']} 🆚 {match['away_team']}</h3>
                    <p><strong>Liga:</strong> {match['league']} | <strong>Hora:</strong> {match['time']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.metric(
                    label="🎯 Predicción Principal",
                    value=main_prediction,
                    delta=f"{confidence:.1f}% confianza"
                )
            
            with col3:
                st.metric(
                    label="⚽ Goles Esperados",
                    value=f"{match['home_expected_goals']:.1f} - {match['away_expected_goals']:.1f}"
                )
            
            # Gráfico de probabilidades
            prob_data = pd.DataFrame({
                'Resultado': ['Victoria Local', 'Empate', 'Victoria Visitante'],
                'Probabilidad': [home_prob, draw_prob, away_prob]
            })
            
            fig = px.bar(prob_data, x='Resultado', y='Probabilidad', 
                        color='Resultado',
                        color_discrete_map={
                            'Victoria Local': '#28a745',
                            'Empate': '#ffc107', 
                            'Victoria Visitante': '#dc3545'
                        })
            fig.update_layout(
                height=200, 
                showlegend=False, 
                title=f"Probabilidades - {match['home_team']} vs {match['away_team']}",
                xaxis_title="",
                yaxis_title="Probabilidad (%)"
            )
            st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("📊 Análisis Detallado por Partido")
    
    # Selector de partido para análisis detallado
    match_options = {f"{m['home_team']} vs {m['away_team']}": m['match_id'] for m in matches_data['matches']}
    selected_match_name = st.selectbox("Selecciona un partido:", list(match_options.keys()))
    selected_match_id = match_options[selected_match_name]
    
    match = next(m for m in matches_data['matches'] if m['match_id'] == selected_match_id)
    prediction = predictions_data[selected_match_id]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Información del partido
        st.subheader("📋 Información del Partido")
        
        st.write(f"**Liga:** {match['league']}")
        st.write(f"**Fecha y Hora:** {match['date']} | {match['time']}")
        st.write(f"**Rating ELO Local:** {match['home_elo']}")
        st.write(f"**Rating ELO Visitante:** {match['away_elo']}")
        st.write(f"**Tilt Ofensivo Local:** {match['home_tilt']}%")
        st.write(f"**Tilt Ofensivo Visitante:** {match['away_tilt']}%")
        
        # Métricas clave
        st.subheader("📈 Métricas Clave")
        col1_1, col1_2, col1_3 = st.columns(3)
        
        with col1_1:
            st.metric("Goles Esperados Local", f"{match['home_expected_goals']:.2f}")
        with col1_2:
            st.metric("Goles Esperados Visitante", f"{match['away_expected_goals']:.2f}")
        with col1_3:
            total_goals = match['home_expected_goals'] + match['away_expected_goals']
            st.metric("Total Goles Esperados", f"{total_goals:.2f}")
    
    with col2:
        # Gráfico de probabilidades circular
        st.subheader("🎯 Probabilidades de Resultado")
        
        labels = ['Victoria Local', 'Empate', 'Victoria Visitante']
        values = [
            prediction['probabilities']['home_win'], 
            prediction['probabilities']['draw'], 
            prediction['probabilities']['away_win']
        ]
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=labels, 
            values=values, 
            marker_colors=['#28a745', '#ffc107', '#dc3545']
        )])
        fig_pie.update_layout(height=300)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Resultados exactos más probables
    st.subheader("🎲 Resultados Exactos Más Probables")
    
    exact_scores = prediction['exact_scores']
    top_scores = sorted(exact_scores.items(), key=lambda x: x[1], reverse=True)[:10]
    
    scores_df = pd.DataFrame(top_scores, columns=['Resultado', 'Probabilidad (%)'])
    
    fig_scores = px.bar(
        scores_df, 
        x='Resultado', 
        y='Probabilidad (%)',
        title="Top 10 Resultados Más Probables"
    )
    st.plotly_chart(fig_scores, use_container_width=True)
    
    # Análisis de handicap
    st.subheader("📊 Análisis de Handicap")
    
    handicap_data = prediction['handicap']
    handicap_df = pd.DataFrame(
        list(handicap_data.items()), 
        columns=['Handicap', 'Probabilidad (%)']
    )
    
    fig_handicap = px.bar(
        handicap_df, 
        x='Handicap', 
        y='Probabilidad (%)',
        title="Probabilidades de Handicap"
    )
    st.plotly_chart(fig_handicap, use_container_width=True)

with tab3:
    st.header("📈 Comparativa Entre Partidos")
    
    # Datos para comparativa
    comparison_data = []
    for match in matches_data['matches']:
        match_id = match['match_id']
        prediction = predictions_data[match_id]
        
        comparison_data.append({
            'Partido': f"{match['home_team']} vs {match['away_team']}",
            'Liga': match['league'],
            'Prob Victoria Local': prediction['probabilities']['home_win'],
            'Prob Empate': prediction['probabilities']['draw'],
            'Prob Victoria Visitante': prediction['probabilities']['away_win'],
            'ELO Local': match['home_elo'],
            'ELO Visitante': match['away_elo'],
            'Goles Esperados Local': match['home_expected_goals'],
            'Goles Esperados Visitante': match['away_expected_goals'],
            'Confianza Máxima': max(
                prediction['probabilities']['home_win'], 
                prediction['probabilities']['draw'], 
                prediction['probabilities']['away_win']
            )
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Comparativa de probabilidades
        st.subheader("📊 Comparativa de Probabilidades")
        
        fig_comp = go.Figure()
        
        fig_comp.add_trace(go.Bar(
            name='Victoria Local', 
            x=comparison_df['Partido'], 
            y=comparison_df['Prob Victoria Local'],
            marker_color='#28a745'
        ))
        
        fig_comp.add_trace(go.Bar(
            name='Empate', 
            x=comparison_df['Partido'], 
            y=comparison_df['Prob Empate'],
            marker_color='#ffc107'
        ))
        
        fig_comp.add_trace(go.Bar(
            name='Victoria Visitante', 
            x=comparison_df['Partido'], 
            y=comparison_df['Prob Victoria Visitante'],
            marker_color='#dc3545'
        ))
        
        fig_comp.update_layout(
            barmode='group', 
            height=400,
            title="Comparativa de Probabilidades por Partido"
        )
        st.plotly_chart(fig_comp, use_container_width=True)
    
    with col2:
        # Comparativa de ELO
        st.subheader("🏆 Comparativa de Rating ELO")
        
        fig_elo = go.Figure()
        
        fig_elo.add_trace(go.Bar(
            name='ELO Local', 
            x=comparison_df['Partido'], 
            y=comparison_df['ELO Local'],
            marker_color='#1f77b4'
        ))
        
        fig_elo.add_trace(go.Bar(
            name='ELO Visitante', 
            x=comparison_df['Partido'], 
            y=comparison_df['ELO Visitante'],
            marker_color='#ff7f0e'
        ))
        
        fig_elo.update_layout(
            barmode='group', 
            height=400,
            title="Comparativa de Rating ELO"
        )
        st.plotly_chart(fig_elo, use_container_width=True)
    
    # Tabla comparativa
    st.subheader("📋 Tabla Comparativa Completa")
    st.dataframe(
        comparison_df.style.background_gradient(
            subset=['Confianza Máxima'], 
            cmap='YlOrBr'
        ), 
        use_container_width=True
    )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p><strong>⚽ Soccer Prediction Dashboard</strong> - Predicciones basadas en Machine Learning</p>
    <p><em>⚠️ Disclaimer: Las predicciones son basadas en modelos estadísticos. El fútbol es impredecible - ¡disfruta del juego responsablemente!</em></p>
</div>
""", unsafe_allow_html=True)
