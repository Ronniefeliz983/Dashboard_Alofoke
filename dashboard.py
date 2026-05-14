import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import numpy as np

st.set_page_config(
    page_title="Auditoría de Red · Alofoke",
    page_icon="📊",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
@import url('https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css');

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    background-color: #f8fafc !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stHeader"] { display: none !important; }
.block-container { padding: 24px 32px !important; max-width: 100% !important; }

.topbar {
    background: #ffffff;
    height: 52px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: -24px -32px 16px -32px;
    padding: 0 32px;
    border-bottom: 1px solid #e2e8f0;
    position: sticky; top: 0; z-index: 100;
}
.topbar-left { display: flex; align-items: center; gap: 24px; }
.topbar-brand {
    font-size: 13px; font-weight: 700; color: #0f172a; letter-spacing: 0.02em;
    white-space: nowrap;
}
.topbar-nav { display: flex; align-items: center; gap: 2px; }
.nav-link {
    padding: 7px 16px;
    font-size: 12px; font-weight: 500; color: #64748b;
    border-radius: 8px;
    text-decoration: none !important;
    transition: all 0.15s;
}
.nav-link:hover { color: #0f172a; background: #f1f5f9; }
.nav-link.active { color: #1d4ed8; background: #eff6ff; font-weight: 600; }
.topbar-right { display: flex; align-items: center; gap: 12px; }
.topbar-pill {
    background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 20px;
    padding: 5px 14px; font-size: 11px; color: #1d4ed8; display: flex; align-items: center; gap: 6px; font-weight: 500;
}
.topbar-pill .dot { width: 6px; height: 6px; border-radius: 50%; background: #3b82f6; display: inline-block; }
.topbar-avatar {
    width: 30px; height: 30px; border-radius: 50%; background: #3b82f6;
    display: flex; align-items: center; justify-content: center;
    font-size: 12px; font-weight: 700; color: #ffffff;
}

.separator {
    height: 1px;
    background: linear-gradient(90deg, #e2e8f0 0%, #e2e8f0 50%, transparent 100%);
    margin: 0 32px;
}

.summary-banner {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-left: 3px solid #3b82f6;
    border-radius: 12px;
    padding: 14px 20px;
    display: flex;
    align-items: center;
    gap: 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.summary-badge {
    background: #eff6ff; border: 0.5px solid #bfdbfe; border-radius: 6px; padding: 5px 12px;
    font-size: 10px; font-weight: 600; color: #1d4ed8; text-transform: uppercase;
    letter-spacing: 0.1em; white-space: nowrap;
}
.summary-text { font-size: 12px; color: #6b7290; line-height: 1.6; flex: 1; }
.summary-text strong { color: #1a1e2e; }
.summary-stat { text-align: center; flex-shrink: 0; padding-left: 15px; border-left: 1px solid #e2e6f0; }
.summary-stat .pct { font-size: 20px; font-weight: 600; color: #0f172a; line-height: 1; }
.summary-stat .lbl { font-size: 9px; color: #9ba3c0; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 2px; }

.kpi-row { display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; }
.kpi-row-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
.kpi-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 16px 20px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    transition: box-shadow 0.2s, transform 0.2s;
}
.kpi-card:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    transform: translateY(-1px);
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 3px 3px 0 0;
    background: #3b82f6;
}
.kpi-card.slate::before  { background: #64748b; }
.kpi-card.darkred::before{ background: #dc2626; }
.kpi-card.green::before  { background: #10b981; }
.kpi-card.amber::before  { background: #f59e0b; }

.kpi-label { font-size: 10px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 6px; font-weight: 500; }
.kpi-value { font-size: 22px; font-weight: 700; color: #0f172a; line-height: 1.2; }
.kpi-sub   { font-size: 11px; margin-top: 5px; display: flex; align-items: center; gap: 5px; color: #64748b; }
.kpi-icon-bg { position: absolute; right: 14px; top: 50%; transform: translateY(-50%); font-size: 32px; opacity: 0.06; color: #0f172a; }

.chart-wrap {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.chart-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 14px 20px 12px;
    border-bottom: 1px solid #f1f5f9;
}
.chart-title  { font-size: 13px; font-weight: 600; color: #0f172a; margin: 0; }
.chart-sub    { font-size: 11px; color: #64748b; margin-top: 3px; display: flex; align-items: center; gap: 14px; }
.legend-dot   { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 4px; vertical-align: middle; }
.legend-dash  { display: inline-block; width: 16px; height: 0; border-top: 2px dashed #94a3b8; margin-right: 4px; vertical-align: middle; }

* { font-family: 'Inter', sans-serif !important; }

.spam-table { width: 100%; border-collapse: collapse; font-size: 11px; }
.spam-table th { font-size: 9px; text-transform: uppercase; letter-spacing: 0.08em; color: #94a3b8; font-weight: 500; padding: 0 0 10px 0; border-bottom: 1px solid #f1f5f9; text-align: left; }
.spam-table td { padding: 7px 0; border-bottom: 1px solid #f8fafc; vertical-align: middle; }
.spam-table tr:last-child td { border-bottom: none; }
.rank-badge { display: inline-flex; width: 20px; height: 20px; background: #eff6ff; border-radius: 6px; align-items: center; justify-content: center; font-size: 10px; color: #3b82f6; font-weight: 700; }
.spam-msg  { color: #475569; max-width: 180px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; display: inline-block; }
.spam-user { color: #1d4ed8; font-weight: 600; max-width: 120px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; display: inline-block; }
.bar-wrap  { background: #f1f5f9; border-radius: 4px; height: 6px; width: 60px; overflow: hidden; }
.bar-fill  { height: 6px; border-radius: 4px; background: #3b82f6; }
.count-cell { color: #94a3b8; font-size: 10px; text-align: right; }

.section-label { font-size: 10px; text-transform: uppercase; letter-spacing: 0.12em; color: #94a3b8; font-weight: 500; margin-bottom: 0; margin-top: 14px; }
.footer {
    font-size: 10px; color: #94a3b8;
    display: flex; justify-content: space-between;
    padding: 12px 0 24px;
    border-top: 1px solid #e2e8f0;
    margin-top: 20px;
}

[data-testid="stPlotlyChart"] { margin: 0 !important; padding: 0 !important; }
[data-testid="stPlotlyChart"] > div { border-radius: 0 0 12px 12px !important; background: #fff !important; }

/* Badge de nivel para bots */
.nivel-critico { background:#fef2f2;color:#dc2626;border:1px solid #fecaca;border-radius:5px;padding:2px 8px;font-size:9px;font-weight:600; }
.nivel-alto    { background:#fffbeb;color:#d97706;border:1px solid #fde68a;border-radius:5px;padding:2px 8px;font-size:9px;font-weight:600; }
.nivel-medio   { background:#f8fafc;color:#64748b;border:1px solid #e2e8f0;border-radius:5px;padding:2px 8px;font-size:9px;font-weight:600; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# CARGA DE DATOS
# ─────────────────────────────────────────────
@st.cache_data(show_spinner="Procesando telemetría...")
def cargar_datos():
    try:
        df_radar = pd.read_excel("alofoke_radar_envivo.xlsx")
        df_radar.columns = df_radar.columns.str.strip()
        if 'Timestamp' not in df_radar.columns:
            df_radar = pd.read_excel("alofoke_radar_envivo.xlsx", sheet_name=1)
            df_radar.columns = df_radar.columns.str.strip()
    except Exception as e:
        st.error(f"❌ Error al cargar radar: {e}")
        return None, None

    try:
        df_chat = pd.read_excel("alofoke_chat_envivo.xlsx")
        df_chat.columns = df_chat.columns.str.strip()
    except Exception as e:
        st.error(f"❌ Error al cargar chat: {e}")
        return None, None

    df_radar['Timestamp'] = pd.to_datetime(df_radar['Timestamp'])
    df_chat['Timestamp']  = pd.to_datetime(df_chat['Timestamp'])
    df_radar['Minuto'] = df_radar['Timestamp'].dt.floor('min')
    df_chat['Minuto']  = df_chat['Timestamp'].dt.floor('min')
    df_radar = df_radar.sort_values('Timestamp').reset_index(drop=True)
    df_radar['Delta_Viewers'] = df_radar['Viewers_Concurrentes'].diff().fillna(0)
    df_radar['Delta_Likes']   = df_radar['Likes_Acumulados'].diff().fillna(0)
    chat_vel = df_chat.groupby('Minuto').size().reset_index(name='Mensajes_Por_Minuto')
    df_master = pd.merge(df_radar, chat_vel, on='Minuto', how='left')
    df_master['Mensajes_Por_Minuto'] = df_master['Mensajes_Por_Minuto'].fillna(0)
    df_chat['Mensaje_Limpio'] = df_chat['Mensaje'].astype(str).str.strip()
    return df_master, df_chat

df_master_raw, df_chat_raw = cargar_datos()

if df_master_raw is None or df_chat_raw is None:
    st.warning("⚠️ Faltan archivos de datos.")
    st.stop()


# ─────────────────────────────────────────────
# TOPBAR + NAVEGACIÓN
# ─────────────────────────────────────────────
params = st.query_params
nav_section = params.get("section", "general")

if nav_section == "general":
    seccion_activa = "📊 Vista General"
elif nav_section == "bots":
    seccion_activa = "📊 Análisis de Patrones de Mensajes"
else:
    seccion_activa = "📈 Engagement y Densidad"

is_gen = 'active' if nav_section == 'general' else ''
is_bot = 'active' if nav_section == 'bots' else ''
is_eng = 'active' if nav_section == 'engagement' else ''

st.markdown(f"""
<div class="topbar">
    <div class="topbar-left">
        <span class="topbar-brand">📊 Telemetría</span>
        <nav class="topbar-nav">
            <a href="?section=general" target="_self" class="nav-link {is_gen}">📊 Vista General</a>
            <a href="?section=bots" target="_self" class="nav-link {is_bot}">📊 Patrones de Mensajes</a>
            <a href="?section=engagement" target="_self" class="nav-link {is_eng}">📈 Engagement</a>
        </nav>
    </div>
    <div class="topbar-right">
        <span class="topbar-pill"><span class="dot"></span> Live · Pipeline Activo</span>
        <span class="topbar-avatar">TF</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FILTROS (colapsables)
# ─────────────────────────────────────────────
min_time = df_master_raw['Timestamp'].min().to_pydatetime()
max_time = df_master_raw['Timestamp'].max().to_pydatetime()

show_filters = st.checkbox("Mostrar filtros", value=True, label_visibility="collapsed")

if show_filters:
    c1, c2 = st.columns([3, 1], gap="large")
    with c1:
        time_range = st.slider(
            "Ventana de Tiempo",
            min_value=min_time, max_value=max_time, value=(min_time, max_time),
            format="DD/MM - HH:mm",
            label_visibility="collapsed",
        )
    with c2:
        search_user = st.text_input("Filtrar por Usuario", placeholder="Buscar @usuario...", label_visibility="collapsed")
else:
    time_range = (min_time, max_time)
    search_user = ""

st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PROCESAMIENTO GLOBAL
# ─────────────────────────────────────────────
mask_master = (df_master_raw['Timestamp'] >= time_range[0]) & (df_master_raw['Timestamp'] <= time_range[1])
df_master = df_master_raw.loc[mask_master].reset_index(drop=True)

mask_chat = (df_chat_raw['Timestamp'] >= time_range[0]) & (df_chat_raw['Timestamp'] <= time_range[1])
if search_user:
    mask_chat = mask_chat & df_chat_raw['Autor'].str.contains(search_user, case=False, na=False)
df_chat = df_chat_raw.loc[mask_chat].reset_index(drop=True)

UMBRAL_ATIPICO = 15000

if not df_master.empty:
    max_viewers      = df_master['Viewers_Concurrentes'].max()
    max_salto_pos    = df_master['Delta_Viewers'].max()
    max_salto_neg    = df_master['Delta_Viewers'].min()
    eventos_atipicos = len(df_master[df_master['Delta_Viewers'].abs() > UMBRAL_ATIPICO])
    df_master['Ratio_Likes_Viewers'] = (df_master['Likes_Acumulados'] / df_master['Viewers_Concurrentes'].replace(0, 1)) * 100
else:
    max_viewers = max_salto_pos = max_salto_neg = eventos_atipicos = 0

total_msgs     = len(df_chat)
autores_unicos = df_chat['Autor'].nunique()

patron_bots = r'AAAAA|Thời|ChúaGiêsu'
if not df_chat.empty:
    df_bots = df_chat[df_chat['Autor'].str.contains(patron_bots, case=False, na=False)].copy()
    if not df_bots.empty:
        df_bots = df_bots.sort_values(['Autor', 'Timestamp'])
        df_bots['Intervalo'] = df_bots.groupby('Autor')['Timestamp'].diff().dt.total_seconds()
        cadencia_avg = df_bots['Intervalo'].mean()
    else:
        cadencia_avg = 0.0
else:
    df_bots = pd.DataFrame()
    cadencia_avg = 0.0

def fmt_k(v):
    if abs(v) >= 1_000_000: return f"{v/1_000_000:.2f}M"
    if abs(v) >= 1_000:     return f"{v/1_000:.1f}k"
    return f"{int(v):,}"


# =====================================================================
# SECCIONES
# =====================================================================

if seccion_activa == "📊 Vista General":

    st.markdown(f"""
    <div class="summary-banner">
        <div class="summary-badge">ℹ️ Resumen Técnico</div>
        <div class="summary-text">
            Durante el período evaluado, se registró una concurrencia máxima de
            <strong>{fmt_k(max_viewers)} espectadores</strong>.
            El análisis detectó <strong>{eventos_atipicos} eventos de fluctuación atípica</strong>
            (variaciones superiores a {fmt_k(UMBRAL_ATIPICO)} conexiones por intervalo).
            Se capturaron un total de <strong>{fmt_k(total_msgs)}</strong> registros de interacción textual.
        </div>
        <div class="summary-stat">
            <div class="pct">{eventos_atipicos}</div>
            <div class="lbl">Eventos<br>Atípicos</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="section-label">Métricas de Concurrencia e Interacción</p>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="kpi-row">
        <div class="kpi-card">
            <div class="kpi-label">Concurrencia Pico</div>
            <div class="kpi-value">{fmt_k(max_viewers)}</div>
            <div class="kpi-sub"><i class="ti ti-activity"></i> Espectadores máx. simultáneos</div>
            <i class="ti ti-users kpi-icon-bg"></i>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Fluctuación Máx (+)</div>
            <div class="kpi-value">+{fmt_k(max_salto_pos)}</div>
            <div class="kpi-sub"><i class="ti ti-arrow-up-right"></i> Mayor incremento por intervalo</div>
            <i class="ti ti-chart-line-up kpi-icon-bg"></i>
        </div>
        <div class="kpi-card darkred">
            <div class="kpi-label">Fluctuación Máx (-)</div>
            <div class="kpi-value">{fmt_k(max_salto_neg)}</div>
            <div class="kpi-sub"><i class="ti ti-arrow-down-right"></i> Mayor descenso por intervalo</div>
            <i class="ti ti-chart-line-down kpi-icon-bg"></i>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Eventos Atípicos</div>
            <div class="kpi-value">{eventos_atipicos}</div>
            <div class="kpi-sub"><i class="ti ti-alert-circle"></i> Variaciones > {fmt_k(UMBRAL_ATIPICO)}</div>
            <i class="ti ti-radar kpi-icon-bg"></i>
        </div>
        <div class="kpi-card slate">
            <div class="kpi-label">Volumen de Chat</div>
            <div class="kpi-value">{fmt_k(total_msgs)}</div>
            <div class="kpi-sub"><i class="ti ti-message-2"></i> {autores_unicos:,} autores únicos</div>
            <i class="ti ti-message-circle kpi-icon-bg"></i>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="section-label" style="margin-top:10px">Análisis Comparativo: Conexiones de Red vs Volumen Textual</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="chart-wrap" style="border-radius:10px 10px 0 0;border-bottom:none;padding-bottom:0;">
        <div class="chart-header">
            <div>
                <div class="chart-title">Comportamiento Multivariable</div>
                <div class="chart-sub">
                    <span><span class="legend-dot" style="background:#3b82f6;"></span>Conexiones totales</span>
                    <span><span class="legend-dash"></span>Mensajes por minuto</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not df_master.empty:
        fig_main = make_subplots(specs=[[{"secondary_y": True}]])
        fig_main.add_trace(go.Scatter(
            x=df_master['Timestamp'], y=df_master['Viewers_Concurrentes'],
            name='Viewers Concurrentes', line=dict(color='#3b82f6', width=2),
            fill='tozeroy', fillcolor='rgba(59,130,246,0.10)',
            hovertemplate='<b>%{x|%d/%m %H:%M}</b><br>👥 Viewers: <b>%{y:,.0f}</b><extra></extra>',
        ), secondary_y=False)
        fig_main.add_trace(go.Scatter(
            x=df_master['Timestamp'], y=df_master['Mensajes_Por_Minuto'],
            name='Mensajes por minuto', line=dict(color='#64748b', width=1.5, dash='dot'),
            hovertemplate='<b>%{x|%d/%m %H:%M}</b><br>💬 Msgs/min: <b>%{y:,.0f}</b><extra></extra>',
        ), secondary_y=True)
        fig_main.update_layout(
            height=380,
            paper_bgcolor='#ffffff', plot_bgcolor='#ffffff',
            hovermode='x unified',
            margin=dict(t=36,b=40,l=60,r=70),
            showlegend=True,
            legend=dict(
                orientation='h', x=0, y=1.12,
                font=dict(size=10, color='#6b7290'),
                bgcolor='rgba(0,0,0,0)',
                itemsizing='constant',
            ),
            font=dict(family='Inter', size=10, color='#9ba3c0'),
        )
        fig_main.update_xaxes(
            title_text='Hora del stream',
            title_font=dict(size=9, color='#9ba3c0'),
            tickformat='%H:%M',
            showgrid=True, gridcolor='rgba(0,0,0,0.04)',
            tickfont=dict(size=9, color='#9ba3c0'),
            showline=False,
        )
        fig_main.update_yaxes(
            secondary_y=False,
            tickformat='.2s', showgrid=True, gridcolor='rgba(0,0,0,0.04)',
            tickfont=dict(size=9, color='#3b82f6'),
            title_text='👥 Viewers concurrentes',
            title_font=dict(size=9, color='#3b82f6'),
            title_standoff=8,
        )
        fig_main.update_yaxes(
            secondary_y=True,
            tickformat='.0f', showgrid=False,
            tickfont=dict(size=9, color='#64748b'),
            title_text='💬 Mensajes / minuto',
            title_font=dict(size=9, color='#64748b'),
            title_standoff=8,
        )
        st.plotly_chart(fig_main, use_container_width=True, config={'displayModeBar': False})
        st.markdown('<div style="background:#fff;border:1px solid #e2e8f0;border-top:none;border-radius:0 0 12px 12px;height:6px;margin-top:-8px;"></div>', unsafe_allow_html=True)

    col_sp, col_dv = st.columns([3, 2], gap="medium")
    with col_sp:
        if not df_chat.empty:
            top_spam = df_chat.groupby(['Autor','Mensaje_Limpio']).size().reset_index(name='Repeticiones')
            top_spam = top_spam.sort_values(by='Repeticiones', ascending=False).head(8).reset_index(drop=True)
            max_rep  = top_spam['Repeticiones'].max() if not top_spam.empty else 1
        else:
            top_spam = pd.DataFrame(columns=['Autor','Mensaje_Limpio','Repeticiones'])
            max_rep = 1

        rows_html = ""
        for i, row in top_spam.iterrows():
            pct   = int(row['Repeticiones'] / max_rep * 100)
            rep_k = f"{row['Repeticiones']/1000:.1f}k" if row['Repeticiones'] >= 1000 else str(row['Repeticiones'])
            autor_e = str(row['Autor'])[:15].replace('<','&lt;').replace('>','&gt;')
            msg_e   = str(row['Mensaje_Limpio'])[:35].replace('<','&lt;').replace('>','&gt;')
            rows_html += f"""<tr>
                <td><span class="rank-badge">{i+1}</span></td>
                <td><span class="spam-user">{autor_e}</span></td>
                <td><span class="spam-msg">{msg_e}</span></td>
                <td><div class="bar-wrap"><div class="bar-fill" style="width:{pct}%"></div></div></td>
                <td class="count-cell">{rep_k}</td>
            </tr>"""
        if not rows_html:
            rows_html = "<tr><td colspan='5' style='text-align:center;color:#9ba3c0;padding:20px;'>Sin datos</td></tr>"

        st.markdown(f"""
        <div class="chart-wrap">
            <div class="chart-header">
                <div>
                    <div class="chart-title">Mensajes con Mayor Índice de Repetición</div>
                    <div class="chart-sub">Usuarios con mayor número de envíos de texto idéntico durante el stream</div>
                </div>
            </div>
            <div style="padding:10px 16px 14px;">
                <table class="spam-table">
                    <thead><tr><th style="width:28px">#</th><th style="width:120px">Usuario</th><th>Cadena de Texto</th><th style="width:70px">Volumen</th><th style="width:40px;text-align:right">Total</th></tr></thead>
                    <tbody>{rows_html}</tbody>
                </table>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_dv:
        st.markdown("""
        <div class="chart-wrap" style="border-radius:10px 10px 0 0;border-bottom:none;padding-bottom:0;">
            <div class="chart-header">
                <div>
                    <div class="chart-title">Variación Neta de Conexiones (Delta)</div>
                    <div class="chart-sub"><span><span class="legend-dot" style="background:#3b82f6;"></span>Incremento</span><span><span class="legend-dot" style="background:#dc2626;"></span>Descenso</span></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if not df_master.empty:
            colores_dv = ['rgba(59,130,246,0.6)' if v >= 0 else 'rgba(220,38,38,0.6)' for v in df_master['Delta_Viewers']]
            fig_dv = go.Figure(go.Bar(
                x=df_master['Timestamp'], y=df_master['Delta_Viewers'],
                marker_color=colores_dv, marker_line_width=0,
                hovertemplate='<b>%{x|%d/%m %H:%M}</b><br>Variación: <b>%{y:+,.0f}</b> viewers<extra></extra>',
                name='Δ Viewers',
            ))
            fig_dv.update_layout(
                height=340,
                paper_bgcolor='#ffffff', plot_bgcolor='#ffffff',
                margin=dict(t=8,b=44,l=60,r=16),
                showlegend=False,
                font=dict(family='Inter',size=9,color='#9ba3c0'),
                annotations=[dict(
                    x=0.01, y=0, xref='paper', yref='y',
                    text='← sin cambio', showarrow=False,
                    font=dict(size=8, color='#c0c4d0'), xanchor='left',
                )],
            )
            fig_dv.update_xaxes(
                tickformat='%H:%M',
                tickfont=dict(size=9, color='#9ba3c0'),
                title_text='Hora del stream',
                title_font=dict(size=9, color='#9ba3c0'),
                showgrid=False, showline=False,
            )
            fig_dv.update_yaxes(
                tickformat='.2s',
                title_text='Δ Viewers por intervalo',
                title_font=dict(size=9, color='#9ba3c0'),
                title_standoff=6,
                gridcolor='rgba(0,0,0,0.04)', showgrid=True, showline=False,
                zeroline=True, zerolinecolor='rgba(0,0,0,0.15)', zerolinewidth=1.5,
                tickfont=dict(size=9,color='#9ba3c0'),
            )
            st.plotly_chart(fig_dv, use_container_width=True, config={'displayModeBar': False})
        st.markdown('<div style="background:#fff;border:1px solid #e2e8f0;border-top:none;border-radius:0 0 12px 12px;height:6px;margin-top:-8px;"></div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
elif seccion_activa == "📊 Análisis de Patrones de Mensajes":

    st.markdown('<p class="section-label">Análisis de Comportamiento en el Chat</p>', unsafe_allow_html=True)

    bots_unicos  = df_bots['Autor'].nunique() if not df_bots.empty else 0
    intervalo_min = df_bots['Intervalo'].min() if not df_bots.empty and 'Intervalo' in df_bots.columns else 0.0
    pct_trafico  = (len(df_bots) / total_msgs * 100) if total_msgs > 0 else 0.0

    # KPIs
    st.markdown(f"""
    <div class="kpi-row">
        <div class="kpi-card slate">
            <div class="kpi-label">Mensajes con Patrón Repetitivo</div>
            <div class="kpi-value">{len(df_bots):,}</div>
            <div class="kpi-sub"><i class="ti ti-message-repeat"></i> ~{pct_trafico:.2f}% del tráfico total</div>
            <i class="ti ti-message-repeat kpi-icon-bg"></i>
        </div>
        <div class="kpi-card darkred">
            <div class="kpi-label">Frecuencia Media de Envío</div>
            <div class="kpi-value">{cadencia_avg:.1f} seg</div>
            <div class="kpi-sub"><i class="ti ti-clock"></i> Velocidad fuera del rango habitual</div>
            <i class="ti ti-clock kpi-icon-bg"></i>
        </div>
        <div class="kpi-card amber">
            <div class="kpi-label">Intervalo Mínimo entre Mensajes</div>
            <div class="kpi-value">{intervalo_min:.1f} seg</div>
            <div class="kpi-sub"><i class="ti ti-bolt"></i> Velocidad no consistente con uso manual</div>
            <i class="ti ti-bolt kpi-icon-bg"></i>
        </div>
        <div class="kpi-card darkred">
            <div class="kpi-label">Cuentas con Patrón Atípico</div>
            <div class="kpi-value">{bots_unicos:,}</div>
            <div class="kpi-sub"><i class="ti ti-fingerprint"></i> Perfiles con comportamiento estadísticamente inusual</div>
            <i class="ti ti-fingerprint kpi-icon-bg"></i>
        </div>
        <div class="kpi-card green">
            <div class="kpi-label">% de Redundancia Textual</div>
            <div class="kpi-value">{(df_bots['Mensaje_Limpio'].duplicated().sum() / len(df_bots) * 100) if not df_bots.empty and len(df_bots)>0 else 0:.1f}%</div>
            <div class="kpi-sub"><i class="ti ti-copy"></i> Proporción de texto duplicado sobre el total</div>
            <i class="ti ti-copy kpi-icon-bg"></i>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="section-label" style="margin-top:14px">Perfil de Cuentas con Actividad Inusual</p>', unsafe_allow_html=True)

    # ── Fila superior: tabla de perfiles + gráfico concentración temporal ──
    col_bt, col_bc = st.columns([3, 2], gap="medium")

    with col_bt:
        resumen_bots = pd.DataFrame()
        if not df_bots.empty:
            resumen_bots = (
                df_bots.groupby('Autor')
                .agg(
                    Total_Msgs=('Mensaje_Limpio','count'),
                    Cadencia_Avg=('Intervalo','mean'),
                )
                .reset_index()
                .sort_values('Total_Msgs', ascending=False)
                .head(10)
            )
            resumen_bots['Cadencia_Avg'] = resumen_bots['Cadencia_Avg'].fillna(0)

            max_msgs_b = resumen_bots['Total_Msgs'].max() if len(resumen_bots) > 0 else 1
            rows_bot = ""
            for i, r in resumen_bots.iterrows():
                pct_bar = int(r['Total_Msgs'] / max_msgs_b * 100)
                if r['Cadencia_Avg'] < 5:
                    nivel = '<span class="nivel-critico">🔴 ALTA FREQ.</span>'
                elif r['Cadencia_Avg'] < 15:
                    nivel = '<span class="nivel-alto">🟠 MEDIA FREQ.</span>'
                else:
                    nivel = '<span class="nivel-medio">🟡 BAJA FREQ.</span>'
                autor_e = str(r['Autor'])[:20].replace('<','&lt;').replace('>','&gt;')
                rows_bot += f"""<tr>
                    <td><span class="spam-user">{autor_e}</span></td>
                    <td style="text-align:center;font-weight:700;color:#1a1e2e">{int(r['Total_Msgs']):,}</td>
                    <td><div class="bar-wrap"><div class="bar-fill" style="width:{pct_bar}%;background:#3b82f6"></div></div></td>
                    <td style="text-align:center;color:#dc2626;font-weight:600">{r['Cadencia_Avg']:.1f}s</td>
                    <td>{nivel}</td>
                </tr>"""
        else:
            rows_bot = "<tr><td colspan='5' style='text-align:center;color:#9ba3c0;padding:20px;'>Sin patrones inusuales detectados en este rango</td></tr>"

        st.markdown(f"""
        <div class="chart-wrap">
            <div class="chart-header">
                <div>
                    <div class="chart-title">Perfil de Cuentas con Actividad Inusual</div>
                    <div class="chart-sub">Resumen de volumen y velocidad por cuenta con patrones atípicos</div>
                </div>
            </div>
            <div style="padding:10px 16px 14px;overflow-x:auto;">
                <table class="spam-table">
                    <thead><tr>
                        <th>Usuario</th><th style="text-align:center">Msgs</th><th style="width:70px">Vol.</th>
                        <th style="text-align:center">Cadencia Avg</th><th>Nivel</th>
                    </tr></thead>
                    <tbody>{rows_bot}</tbody>
                </table>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_bc:
        st.markdown("""
        <div class="chart-wrap" style="border-radius:10px 10px 0 0;border-bottom:none;padding-bottom:0;">
            <div class="chart-header">
                <div>
                    <div class="chart-title">Concentración Temporal de Mensajes con Patrón Inusual</div>
                    <div class="chart-sub">Volumen de mensajes con patrón de alta frecuencia por minuto</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if not df_bots.empty:
            bot_por_min = df_bots.groupby('Minuto').size().reset_index(name='Msgs_Bot')
            fig_bot = go.Figure(go.Bar(
                x=bot_por_min['Minuto'], y=bot_por_min['Msgs_Bot'],
                name='Mensajes con patrón inusual',
                marker_color='rgba(59,130,246,0.7)', marker_line_width=0,
                hovertemplate='<b>%{x|%H:%M}</b><br>📨 Mensajes: <b>%{y:,}</b><extra></extra>',
            ))
            fig_bot.update_layout(
                height=300,
                paper_bgcolor='#ffffff', plot_bgcolor='#ffffff',
                margin=dict(t=8,b=44,l=52,r=16),
                showlegend=False,
                font=dict(family='Inter',size=9,color='#9ba3c0'),
            )
            fig_bot.update_xaxes(
                tickformat='%H:%M',
                title_text='Hora del stream',
                title_font=dict(size=9, color='#9ba3c0'),
                showgrid=False, tickfont=dict(size=9,color='#9ba3c0'),
            )
            fig_bot.update_yaxes(
                title_text='Mensajes / minuto',
                title_font=dict(size=9, color='#dc2626'),
                showgrid=True, gridcolor='rgba(0,0,0,0.04)',
                tickfont=dict(size=9,color='#3b82f6'),
                title_standoff=6,
            )
            st.plotly_chart(fig_bot, use_container_width=True, config={'displayModeBar': False})
        st.markdown('<div style="background:#fff;border:1px solid #e2e8f0;border-top:none;border-radius:0 0 12px 12px;height:6px;margin-top:-8px;"></div>', unsafe_allow_html=True)

    # ── Fila inferior: Top 5 mensajes más repetidos como tabla ──
    if not df_bots.empty:
        st.markdown('<p class="section-label" style="margin-top:14px">Top 5 · Mensajes con Mayor Índice de Repetición</p>', unsafe_allow_html=True)

        top_reps = (
            df_bots.groupby('Mensaje_Limpio').size()
            .reset_index(name='Repeticiones')
            .sort_values('Repeticiones', ascending=False)
            .head(5)
            .reset_index(drop=True)
        )
        max_rep_t = top_reps['Repeticiones'].max() if not top_reps.empty else 1

        rows_top5 = ""
        medal = ['🥇','🥈','🥉','4°','5°']
        for i, r in top_reps.iterrows():
            pct_bar = int(r['Repeticiones'] / max_rep_t * 100)
            rep_fmt = f"{r['Repeticiones']/1000:.1f}k" if r['Repeticiones'] >= 1000 else f"{int(r['Repeticiones']):,}"
            pct_total = (r['Repeticiones'] / total_msgs * 100) if total_msgs > 0 else 0
            msg_e = str(r['Mensaje_Limpio']).replace('<','&lt;').replace('>','&gt;')
            rows_top5 += f"""<tr>
                <td style="text-align:center;font-size:14px;padding-right:8px;">{medal[i]}</td>
                <td style="max-width:420px;">
                    <span style="font-size:12px;color:#1e293b;font-weight:500;word-break:break-word;">{msg_e}</span>
                </td>
                <td style="min-width:100px;padding:0 12px;">
                    <div style="background:#f1f5f9;border-radius:5px;height:7px;overflow:hidden;">
                        <div style="width:{pct_bar}%;height:7px;border-radius:5px;background:#3b82f6;"></div>
                    </div>
                </td>
                <td style="text-align:right;font-size:13px;font-weight:700;color:#0f172a;white-space:nowrap;">{rep_fmt}</td>
                <td style="text-align:right;font-size:10px;color:#94a3b8;white-space:nowrap;padding-left:10px;">{pct_total:.2f}% del chat</td>
            </tr>"""

        if not rows_top5:
            rows_top5 = "<tr><td colspan='5' style='text-align:center;color:#9ba3c0;padding:20px;'>Sin datos</td></tr>"

        st.markdown(f"""
        <div class="chart-wrap">
            <div class="chart-header">
                <div>
                    <div class="chart-title">Top 5 · Cadenas de Texto con Mayor Repetición</div>
                    <div class="chart-sub">Mensajes enviados de forma idéntica y repetitiva por las cuentas con patrón atípico detectado</div>
                </div>
            </div>
            <div style="padding:12px 20px 16px;">
                <table style="width:100%;border-collapse:collapse;">
                    <thead>
                        <tr>
                            <th style="font-size:9px;text-transform:uppercase;letter-spacing:0.08em;color:#94a3b8;font-weight:500;padding-bottom:10px;border-bottom:1px solid #f1f5f9;width:32px;">#</th>
                            <th style="font-size:9px;text-transform:uppercase;letter-spacing:0.08em;color:#94a3b8;font-weight:500;padding-bottom:10px;border-bottom:1px solid #f1f5f9;text-align:left;">Cadena de Texto</th>
                            <th style="font-size:9px;text-transform:uppercase;letter-spacing:0.08em;color:#94a3b8;font-weight:500;padding-bottom:10px;border-bottom:1px solid #f1f5f9;width:100px;">Volumen</th>
                            <th style="font-size:9px;text-transform:uppercase;letter-spacing:0.08em;color:#94a3b8;font-weight:500;padding-bottom:10px;border-bottom:1px solid #f1f5f9;text-align:right;width:60px;">Total</th>
                            <th style="font-size:9px;text-transform:uppercase;letter-spacing:0.08em;color:#94a3b8;font-weight:500;padding-bottom:10px;border-bottom:1px solid #f1f5f9;text-align:right;width:90px;">% Chat</th>
                        </tr>
                    </thead>
                    <tbody style="font-family:'Inter',sans-serif;">
                        {rows_top5}
                    </tbody>
                </table>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
elif seccion_activa == "📈 Engagement y Densidad":
    col_rl, col_hm = st.columns([1, 1], gap="medium")

    with col_rl:
        st.markdown('<p class="section-label">Análisis de Engagement (Likes vs Viewers)</p>', unsafe_allow_html=True)
        st.markdown("""
        <div class="chart-wrap" style="border-radius:10px 10px 0 0;border-bottom:none;padding-bottom:0;">
            <div class="chart-header">
                <div>
                    <div class="chart-title">Ratio de Conversión Likes/Viewers</div>
                    <div class="chart-sub">En el pico (22:54) viewers +18k, pero likes solo +25 — crecimiento de viewers no correlacionado con el engagement medible.</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if not df_master.empty:
            fig_ratio = make_subplots(specs=[[{"secondary_y": True}]])
            fig_ratio.add_trace(go.Scatter(
                x=df_master['Timestamp'], y=df_master['Viewers_Concurrentes'],
                name='Viewers concurrentes',
                line=dict(color='#3b82f6',width=1.5),
                fill='tozeroy', fillcolor='rgba(59,130,246,0.06)',
                hovertemplate='<b>%{x|%H:%M}</b><br>👥 Viewers: <b>%{y:,.0f}</b><extra></extra>',
            ), secondary_y=False)
            fig_ratio.add_trace(go.Scatter(
                x=df_master['Timestamp'], y=df_master['Ratio_Likes_Viewers'],
                name='Ratio Likes / Viewers (%)',
                line=dict(color='#f59e0b',width=1.5),
                hovertemplate='<b>%{x|%H:%M}</b><br>❤️ Likes / Viewers: <b>%{y:.3f}%</b><br><i>(más alto = más engagement real)</i><extra></extra>',
            ), secondary_y=True)
            fig_ratio.update_layout(
                height=380,
                paper_bgcolor='#ffffff', plot_bgcolor='#ffffff',
                hovermode="x unified",
                margin=dict(t=40,b=44,l=60,r=70),
                showlegend=True,
                legend=dict(
                    orientation='h', x=0, y=1.12,
                    font=dict(size=10, color='#6b7290'),
                    bgcolor='rgba(0,0,0,0)',
                ),
                font=dict(family='Inter',size=9,color='#9ba3c0'),
            )
            fig_ratio.update_xaxes(
                tickformat='%H:%M',
                title_text='Hora del stream',
                title_font=dict(size=9, color='#9ba3c0'),
                showgrid=True, gridcolor='rgba(0,0,0,0.04)',
                tickfont=dict(size=9,color='#9ba3c0'),
            )
            fig_ratio.update_yaxes(
                secondary_y=False,
                tickformat='.2s',
                title_text='👥 Viewers concurrentes',
                title_font=dict(size=9, color='#3b82f6'),
                showgrid=True, gridcolor='rgba(0,0,0,0.04)',
                tickfont=dict(size=9,color='#3b82f6'),
                title_standoff=8,
            )
            fig_ratio.update_yaxes(
                secondary_y=True,
                tickformat='.3f',
                ticksuffix='%',
                title_text='❤️ Likes / Viewers (%)',
                title_font=dict(size=9, color='#f59e0b'),
                showgrid=False,
                tickfont=dict(size=9,color='#f59e0b'),
                title_standoff=8,
            )
            st.plotly_chart(fig_ratio, use_container_width=True, config={'displayModeBar': False})
        st.markdown('<div style="background:#fff;border:1px solid #e2e8f0;border-top:none;border-radius:0 0 12px 12px;height:6px;margin-top:-8px;"></div>', unsafe_allow_html=True)

    with col_hm:
        st.markdown('<p class="section-label">Densidad: Autores Únicos vs Viewers</p>', unsafe_allow_html=True)
        st.markdown("""
        <div class="chart-wrap" style="border-radius:10px 10px 0 0;border-bottom:none;padding-bottom:0;">
            <div class="chart-header">
                <div>
                    <div class="chart-title">Mapa de Calor — Participantes Únicos por Hora</div>
                    <div class="chart-sub">El pico de participantes únicos fue 20:00 con 10,726 usuarios — contrasta con los ~2M viewers registrados</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if not df_chat.empty:
            df_chat_hm = df_chat.copy()
            df_chat_hm['Hora'] = df_chat_hm['Timestamp'].dt.hour
            df_chat_hm['Dia']  = df_chat_hm['Timestamp'].dt.strftime('%d/%m')
            heatmap_data = df_chat_hm.groupby(['Dia','Hora'])['Autor'].nunique().unstack().fillna(0)
            fig_heat = go.Figure(data=go.Heatmap(
                z=heatmap_data.values,
                x=[f"{h:02d}:00" for h in heatmap_data.columns],
                y=heatmap_data.index.astype(str),
                colorscale='Blues',
                colorbar=dict(
                    title=dict(text='Usuarios únicos', side='right', font=dict(size=9, color='#6b7290')),
                    tickfont=dict(size=9, color='#9ba3c0'),
                    thickness=12,
                ),
                hovertemplate='📅 Día: <b>%{y}</b><br>🕐 Hora: <b>%{x}</b><br>👤 Usuarios únicos que escribieron: <b>%{z:,.0f}</b><extra></extra>',
            ))
            fig_heat.update_layout(
                height=380,
                paper_bgcolor='#ffffff', plot_bgcolor='#ffffff',
                margin=dict(t=8,b=44,l=60,r=80),
                font=dict(family='Inter',size=9,color='#9ba3c0'),
            )
            fig_heat.update_xaxes(
                title_text='Hora del día',
                title_font=dict(size=9, color='#9ba3c0'),
                tickfont=dict(size=9, color='#9ba3c0'),
            )
            fig_heat.update_yaxes(
                title_text='Fecha',
                title_font=dict(size=9, color='#9ba3c0'),
                tickfont=dict(size=9, color='#9ba3c0'),
            )
            st.plotly_chart(fig_heat, use_container_width=True, config={'displayModeBar': False})
        st.markdown('<div style="background:#fff;border:1px solid #e2e8f0;border-top:none;border-radius:0 0 12px 12px;height:6px;margin-top:-8px;"></div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
    <span>📡 {len(df_master):,} lecturas de telemetría procesadas</span>
    <span>TFG · Análisis Analítico de Datos · 2026</span>
</div>
""", unsafe_allow_html=True)
