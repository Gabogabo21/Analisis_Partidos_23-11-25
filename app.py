import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Configuración inicial
plt.style.use('default')
sns.set_palette("husl")

# Datos de los partidos
matches_data = {
    'match_id': ['ARS-TOT', 'INT-MIL', 'ELC-RMA'],
    'home_team': ['Arsenal', 'Inter', 'Elche'],
    'away_team': ['Tottenham', 'Milan', 'Real Madrid'],
    'league': ['Premier League', 'Serie A', 'La Liga'],
    'date': ['2025-11-23', '2025-11-23', '2025-11-23'],
    'time': ['20:45', '20:45', '20:45'],
    
    # Datos ELO y probabilidades
    'home_elo': [94, 94, 80],
    'away_elo': [88, 91, 473],
    'home_tilt': [-2.8, 7.1, -4.1],
    'away_tilt': [-1.7, -1.2, 21],
    'home_rank': [18, 19, 21],
    'away_rank': [88, 45, 1],
    'home_country_rank': [2, 2, None],
    'away_country_rank': [9, 5, None],
    
    # Probabilidades de victoria
    'home_win_prob': [65.2, 59.4, 11.1],
    'draw_prob': [19.7, 20.9, 18.3],
    'away_win_prob': [15.1, 19.7, 70.6],
    
    # Goles esperados
    'home_expected_goals': [2.1, 1.8, 0.73],
    'away_expected_goals': [1.2, 1.4, 2.8]
}

# Crear DataFrame principal
df_matches = pd.DataFrame(matches_data)

# Datos de resultados exactos (probabilidades)
exact_scores = {
    'ARS-TOT': {
        '1-0': 10.2, '2-0': 10.8, '2-1': 9.9, '3-0': 7.7, '3-1': 7.0,
        '0-0': 5.5, '1-1': 8.7, '0-1': 12.0, '1-2': 9.4, '2-2': 3.4
    },
    'INT-MIL': {
        '1-0': 8.5, '2-0': 9.2, '2-1': 8.1, '3-0': 6.5, '3-1': 5.8,
        '0-0': 6.2, '1-1': 7.9, '0-1': 10.5, '1-2': 8.2, '2-2': 2.8
    },
    'ELC-RMA': {
        '0-1': 12.0, '0-2': 8.5, '1-2': 9.4, '0-3': 5.2, '1-3': 4.1,
        '1-1': 8.7, '0-0': 5.5, '1-0': 4.0, '2-1': 3.2, '2-2': 3.4
    }
}

# Datos de handicap
handicap_data = {
    'ARS-TOT': {'+1': 23.8, '0': 65.2, '-1': 19.7, '-2': 10.2},
    'INT-MIL': {'+1': 21.5, '0': 59.4, '-1': 22.1, '-2': 11.8},
    'ELC-RMA': {'+1': 8.1, '+2': 2.4, '0': 11.1, '-1': 24.3}
}

print("=== DASHBOARD DE PREDICCIÓN DE PARTIDOS ===")
print(f"Fecha: {datetime.now().strftime('%d/%m/%Y')}")
print("=" * 50)

# 1. VISUALIZACIÓN PRINCIPAL DE PROBABILIDADES
def create_probability_dashboard():
    fig = make_subplots(
        rows=2, cols=3,
        subplot_titles=[f"{row['home_team']} vs {row['away_team']}" for _, row in df_matches.iterrows()] + 
                      [f"Distribución {row['home_team']} vs {row['away_team']}" for _, row in df_matches.iterrows()],
        specs=[[{"type": "pie"}, {"type": "pie"}, {"type": "pie"}],
               [{"type": "bar"}, {"type": "bar"}, {"type": "bar"}]]
    )
    
    for i, (_, match) in enumerate(df_matches.iterrows()):
        # Gráficos de torta (probabilidades)
        labels = ['Victoria Local', 'Empate', 'Victoria Visitante']
        values = [match['home_win_prob'], match['draw_prob'], match['away_win_prob']]
        
        fig.add_trace(
            go.Pie(labels=labels, values=values, name=f"{match['home_team']} vs {match['away_team']}"),
            row=1, col=i+1
        )
        
        # Gráficos de barras (resultados exactos)
        match_scores = exact_scores[match['match_id']]
        scores = list(match_scores.keys())
        probs = list(match_scores.values())
        
        fig.add_trace(
            go.Bar(x=scores, y=probs, name="Resultados Exactos"),
            row=2, col=i+1
        )
    
    fig.update_layout(height=800, showlegend=False, title_text="Dashboard de Predicciones - Todos los Partidos")
    fig.show()

create_probability_dashboard()

# 2. ANÁLISIS DETALLADO POR PARTIDO
def detailed_match_analysis():
    for _, match in df_matches.iterrows():
        print(f"\n🔍 ANÁLISIS DETALLADO: {match['home_team']} vs {match['away_team']}")
        print("-" * 60)
        
        # Información básica
        print(f"📅 Liga: {match['league']} | ⏰ Hora: {match['time']}")
        print(f"🏆 Ranking ELO: {match['home_team']} ({match['home_elo']}) vs {match['away_team']} ({match['away_elo']})")
        print(f"📊 Tilt Ofensivo: {match['home_team']} ({match['home_tilt']}%) vs {match['away_team']} ({match['away_tilt']}%)")
        
        # Predicción principal
        max_prob = max(match['home_win_prob'], match['draw_prob'], match['away_win_prob'])
        if max_prob == match['home_win_prob']:
            prediction = f"Victoria del {match['home_team']}"
        elif max_prob == match['draw_prob']:
            prediction = "Empate"
        else:
            prediction = f"Victoria del {match['away_team']}"
            
        print(f"🎯 PREDICCIÓN PRINCIPAL: {prediction} ({max_prob:.1f}% probabilidad)")
        
        # Goles esperados
        print(f"⚽ Goles Esperados: {match['home_team']} ({match['home_expected_goals']:.2f}) - {match['away_team']} ({match['away_expected_goals']:.2f})")
        
        # Resultados más probables
        match_scores = exact_scores[match['match_id']]
        top_scores = sorted(match_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        print("📈 Resultados más probables:")
        for score, prob in top_scores:
            print(f"   {score}: {prob}%")
        
        # Análisis de handicap
        handicap = handicap_data[match['match_id']]
        print("🎲 Análisis de Handicap:")
        for h, prob in handicap.items():
            print(f"   Handicap {h}: {prob}%")

detailed_match_analysis()

# 3. COMPARATIVA ENTRE PARTIDOS
def comparative_analysis():
    print("\n📊 COMPARATIVA ENTRE PARTIDOS")
    print("=" * 50)
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Gráfico 1: Probabilidades de victoria comparadas
    teams = [f"{row['home_team']}\nvs\n{row['away_team']}" for _, row in df_matches.iterrows()]
    home_probs = df_matches['home_win_prob']
    draw_probs = df_matches['draw_prob']
    away_probs = df_matches['away_win_prob']
    
    x = np.arange(len(teams))
    width = 0.25
    
    axes[0,0].bar(x - width, home_probs, width, label='Victoria Local', alpha=0.8)
    axes[0,0].bar(x, draw_probs, width, label='Empate', alpha=0.8)
    axes[0,0].bar(x + width, away_probs, width, label='Victoria Visitante', alpha=0.8)
    
    axes[0,0].set_xlabel('Partidos')
    axes[0,0].set_ylabel('Probabilidad (%)')
    axes[0,0].set_title('Comparativa de Probabilidades de Resultado')
    axes[0,0].set_xticks(x)
    axes[0,0].set_xticklabels(teams, rotation=45)
    axes[0,0].legend()
    axes[0,0].grid(True, alpha=0.3)
    
    # Gráfico 2: Rating ELO comparado
    axes[0,1].bar(x - 0.2, df_matches['home_elo'], 0.4, label='ELO Local', alpha=0.7)
    axes[0,1].bar(x + 0.2, df_matches['away_elo'], 0.4, label='ELO Visitante', alpha=0.7)
    axes[0,1].set_xlabel('Partidos')
    axes[0,1].set_ylabel('Rating ELO')
    axes[0,1].set_title('Comparativa de Rating ELO')
    axes[0,1].set_xticks(x)
    axes[0,1].set_xticklabels(teams, rotation=45)
    axes[0,1].legend()
    axes[0,1].grid(True, alpha=0.3)
    
    # Gráfico 3: Goles esperados
    axes[1,0].bar(x - 0.2, df_matches['home_expected_goals'], 0.4, label='Goles Local', alpha=0.7)
    axes[1,0].bar(x + 0.2, df_matches['away_expected_goals'], 0.4, label='Goles Visitante', alpha=0.7)
    axes[1,0].set_xlabel('Partidos')
    axes[1,0].set_ylabel('Goles Esperados')
    axes[1,0].set_title('Comparativa de Goles Esperados')
    axes[1,0].set_xticks(x)
    axes[1,0].set_xticklabels(teams, rotation=45)
    axes[1,0].legend()
    axes[1,0].grid(True, alpha=0.3)
    
    # Gráfico 4: Tilt ofensivo
    axes[1,1].bar(x - 0.2, df_matches['home_tilt'], 0.4, label='Tilt Local', alpha=0.7)
    axes[1,1].bar(x + 0.2, df_matches['away_tilt'], 0.4, label='Tilt Visitante', alpha=0.7)
    axes[1,1].set_xlabel('Partidos')
    axes[1,1].set_ylabel('Tilt Ofensivo (%)')
    axes[1,1].set_title('Comparativa de Tilt Ofensivo')
    axes[1,1].set_xticks(x)
    axes[1,1].set_xticklabels(teams, rotation=45)
    axes[1,1].legend()
    axes[1,1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

comparative_analysis()

# 4. PREDICCIONES FINALES Y RECOMENDACIONES
def final_predictions():
    print("\n🎯 PREDICCIONES FINALES Y RECOMENDACIONES")
    print("=" * 60)
    
    recommendations = []
    
    for _, match in df_matches.iterrows():
        home_team = match['home_team']
        away_team = match['away_team']
        home_prob = match['home_win_prob']
        draw_prob = match['draw_prob']
        away_prob = match['away_win_prob']
        
        # Determinar predicción principal
        if home_prob > away_prob and home_prob > draw_prob:
            prediction = f"✅ VICTORIA DE {home_team.upper()}"
            confidence = home_prob
        elif away_prob > home_prob and away_prob > draw_prob:
            prediction = f"✅ VICTORIA DE {away_team.upper()}"
            confidence = away_prob
        else:
            prediction = "⚖️ EMPATE"
            confidence = draw_prob
        
        # Análisis de valor
        expected_goals = match['home_expected_goals'] + match['away_expected_goals']
        goal_expectation = "ALTA" if expected_goals > 2.5 else "MEDIA" if expected_goals > 1.5 else "BAJA"
        
        # Recomendación
        if confidence > 60:
            recommendation = "💪 PREDICCIÓN SÓLIDA"
        elif confidence > 45:
            recommendation = "🤔 PREDICCIÓN MODERADA"
        else:
            recommendation = "⚠️ PARTIDO INCIERTO"
        
        print(f"\n🏆 {home_team} vs {away_team}")
        print(f"   {prediction} ({confidence:.1f}% confianza)")
        print(f"   📊 Expectativa de goles: {goal_expectation} ({expected_goals:.2f} goles totales)")
        print(f"   💡 Recomendación: {recommendation}")
        
        # Resultado exacto más probable
        match_scores = exact_scores[match['match_id']]
        most_probable_score = max(match_scores.items(), key=lambda x: x[1])
        print(f"   🎯 Resultado exacto más probable: {most_probable_score[0]} ({most_probable_score[1]}%)")
        
        recommendations.append({
            'partido': f"{home_team} vs {away_team}",
            'prediccion': prediction,
            'confianza': confidence,
            'recomendacion': recommendation
        })
    
    return recommendations

# Ejecutar análisis final
final_recommendations = final_predictions()

# 5. RESUMEN EJECUTIVO
print("\n" + "=" * 70)
print("📋 RESUMEN EJECUTIVO - PREDICCIONES DEL DÍA")
print("=" * 70)

for i, rec in enumerate(final_recommendations, 1):
    print(f"\n{i}. {rec['partido']}")
    print(f"   Predicción: {rec['prediccion']}")
    print(f"   Nivel de confianza: {rec['confianza']:.1f}%")
    print(f"   Recomendación: {rec['recomendacion']}")

print("\n" + "=" * 70)
print("⚠️ NOTA: Estas predicciones están basadas en modelos de machine learning")
print("y análisis estadístico. El fútbol es impredecible - ¡disfruta del juego!")
print("=" * 70)

# 6. DATAFRAME CONSOLIDADO
print("\n📁 DATOS COMPLETOS DE PREDICCIÓN")
print("=" * 50)
display_df = df_matches[['home_team', 'away_team', 'home_win_prob', 'draw_prob', 'away_win_prob', 
                         'home_elo', 'away_elo', 'home_expected_goals', 'away_expected_goals']].copy()
display_df.columns = ['Local', 'Visitante', 'Prob Victoria Local', 'Prob Empate', 'Prob Victoria Visitante',
                     'ELO Local', 'ELO Visitante', 'Goles Esp. Local', 'Goles Esp. Visitante']
display(display_df.round(2))
