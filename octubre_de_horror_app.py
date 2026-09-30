import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Octubre de Horror 🎃 - Club de Lectura",
    page_icon="💀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados (Tema Oscuro Terrorífico)
st.markdown("""
<style>
    .main {
        background-color: #0e0e12;
        color: #e0e0e0;
    }
    .stApp {
        background: linear-gradient(180deg, #0a0a0f 0%, #16121e 100%);
    }
    h1, h2, h3 {
        color: #ff4b4b !important;
        font-family: 'Georgia', serif;
    }
    .stMetric {
        background-color: #1a1a24;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #332233;
    }
    .story-card {
        background-color: #181822;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #ff4b4b;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .story-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #fca311;
    }
    .story-meta {
        font-size: 0.9rem;
        color: #a0a0b0;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Dataset de los 27 cuentos
STORIES_DATA = [
    # Semana 1
    {"fecha": "01 Oct (Jue)", "semana": "Semana 1", "titulo": "La caída de la Casa Usher", "autor": "Edgar Allan Poe", "duracion": "30-40 min", "subgenero": "Gótico / Psicología", "sinopsis": "Un visitante acude a la decadente mansión de su amigo Roderick Usher, presenciando el colapso mental y físico de la familia y la casa."},
    {"fecha": "02 Oct (Vie)", "semana": "Semana 1", "titulo": "The Mezzotint (El grabado)", "autor": "M. R. James", "duracion": "30-40 min", "subgenero": "Fantasmas / Anticuario", "sinopsis": "Un grabado antiguo cambia gradualmente de aspecto, revelando la espeluznante venganza de un espectro del pasado."},
    {"fecha": "04 Oct (Dom)", "semana": "Semana 1", "titulo": "Los sauces", "autor": "Algernon Blackwood", "duracion": "50-70 min", "subgenero": "Horror Cósmico / Naturaleza", "sinopsis": "Dos piragüistas atrapados en una isla del Danubio enfrentan fuerzas elementales e incomprensibles que acechan en los matorrales."},
    
    # Semana 2
    {"fecha": "05 Oct (Lun)", "semana": "Semana 2", "titulo": "La pata de mono", "autor": "W. W. Jacobs", "duracion": "20-25 min", "subgenero": "Maldiciones / Tragedia", "sinopsis": "Un talismán místico concede tres deseos, pero cada uno se cumple cobrando un precio horripilante."},
    {"fecha": "06 Oct (Mar)", "semana": "Semana 2", "titulo": "El gran dios Pan", "autor": "Arthur Machen", "duracion": "60-90 min", "subgenero": "Horror Deidario / Ocultismo", "sinopsis": "Un experimento quirúrgico para ver el mundo espiritual desata una presencia diabólica e indómita en la sociedad victoriana."},
    {"fecha": "07 Oct (Mié)", "semana": "Semana 2", "titulo": "La habitación roja", "autor": "H. G. Wells", "duracion": "20-30 min", "subgenero": "Casa Embrujada / Paranoia", "sinopsis": "Un escéptico decide pasar la noche en una estancia supuestamente maldita para demostrar que los fantasmas no existen."},
    {"fecha": "08 Oct (Jue)", "semana": "Semana 2", "titulo": "¡Silba y acudiré!", "autor": "M. R. James", "duracion": "40-50 min", "subgenero": "Fantasmas / Anticuario", "sinopsis": "Un profesor encuentra un antiguo silbato de bronce en ruinas templarias y al soplarlo despierta una entidad que lo persigue."},
    {"fecha": "09 Oct (Vie)", "semana": "Semana 2", "titulo": "El papel de pared amarillo", "autor": "Charlotte Perkins Gilman", "duracion": "25-35 min", "subgenero": "Terror Psicológico / Aislamiento", "sinopsis": "Una mujer confinada en una habitación por un tratamiento de reposo comienza a obsesionarse con los patrones del papel tapiz."},
    {"fecha": "11 Oct (Dom)", "semana": "Semana 2", "titulo": "El Horla", "autor": "Guy de Maupassant", "duracion": "45-60 min", "subgenero": "Vampirismo Invisible / Locura", "sinopsis": "Un hombre registra en su diario la perturbadora sospecha de estar siendo controlado por una criatura invisible e inmortal."},

    # Semana 3
    {"fecha": "12 Oct (Lun)", "semana": "Semana 3", "titulo": "La cosa maldita", "autor": "Ambrose Bierce", "duracion": "15-25 min", "subgenero": "Monstruos / Invisible", "sinopsis": "Una investigación revela la existencia de una bestia implacable cuya presencia es invisible para el ojo humano."},
    {"fecha": "13 Oct (Mar)", "semana": "Semana 3", "titulo": "El Wendigo", "autor": "Algernon Blackwood", "duracion": "50-70 min", "subgenero": "Folklore / Horror Salvaje", "sinopsis": "Durante una cacería en los bosques de Canadá, una expedición se topa con el mítico espíritu del aire que rapta a los hombres."},
    {"fecha": "14 Oct (Mié)", "semana": "Semana 3", "titulo": "La música de Erich Zann", "autor": "H. P. Lovecraft", "duracion": "20-30 min", "subgenero": "Horror Cósmico / Música", "sinopsis": "Un estudiante descubre que las extrañas melodías de un violista mudo mantienen a raya abismos de oscuridad fuera del cosmos."},
    {"fecha": "15 Oct (Jue)", "semana": "Semana 3", "titulo": "La casa vacía", "autor": "Algernon Blackwood", "duracion": "25-35 min", "subgenero": "Casa Embrujada", "sinopsis": "Un investigador psíquico y su tía se adentran en una residencia abandonada marcada por un crimen espantoso."},
    {"fecha": "16 Oct (Vie)", "semana": "Semana 3", "titulo": "La lotería", "autor": "Shirley Jackson", "duracion": "20-30 min", "subgenero": "Horror Social / Tradición", "sinopsis": "Un pequeño pueblo realiza su rito anual de lotería, ocultando una siniestra y macabra costumbre bajo su aparente normalidad."},
    {"fecha": "18 Oct (Dom)", "semana": "Semana 3", "titulo": "La voz en la noche", "autor": "William Hope Hodgson", "duracion": "30-40 min", "subgenero": "Horror Corporal / Mutación", "sinopsis": "Unos marineros varados en la noche escuchan la angustiosa confesión de una víctima infectada por un hongo parásito."},

    # Semana 4
    {"fecha": "19 Oct (Lun)", "semana": "Semana 4", "titulo": "El reparador de reputaciones", "autor": "Robert W. Chambers", "duracion": "40-50 min", "subgenero": "El Rey de Amarillo / Paranoia", "sinopsis": "Tras sufrir una lesión en la cabeza y leer una obra prohibida, un hombre se sumerge en delirios de grandeza militar y conspiración."},
    {"fecha": "20 Oct (Mar)", "semana": "Semana 4", "titulo": "El gato negro", "autor": "Edgar Allan Poe", "duracion": "20-30 min", "subgenero": "Gótico / Culpabilidad", "sinopsis": "Un hombre presa del alcoholismo comete actos atroces que son trágicamente sacados a la luz por la intervención sobrenatural de un gato."},
    {"fecha": "21 Oct (Mié)", "semana": "Semana 4", "titulo": "Casting the Runes", "autor": "M. R. James", "duracion": "45-60 min", "subgenero": "Ocultismo / Maldiciones", "sinopsis": "Un investigador recibe disimuladamente un papel con pergaminos rúnicos que invocan a un demonio para matarlo en pocos días."},
    {"fecha": "22 Oct (Jue)", "semana": "Semana 4", "titulo": "Los blancos", "autor": "Arthur Machen", "duracion": "50-70 min", "subgenero": "Paganismo / Ocultismo", "sinopsis": "El diario de una niña detalla su gradual iniciación en ritos antiguos y secretos perturbadores de la naturaleza."},
    {"fecha": "23 Oct (Vie)", "semana": "Semana 4", "titulo": "El color que cayó del cielo", "autor": "H. P. Lovecraft", "duracion": "50-70 min", "subgenero": "Horror Cósmico / Ciencia Ficción", "sinopsis": "Un meteorito impacta en una granja, liberando un color alienígena e incalculable que muta y consume la vida a su alrededor."},
    {"fecha": "25 Oct (Dom)", "semana": "Semana 4", "titulo": "La habitación de la torre", "autor": "E. F. Benson", "duracion": "30-40 min", "subgenero": "Pesadillas / Vampirismo", "sinopsis": "Un joven sufre durante años una recurrente pesadilla que se vuelve escalofriantemente real durante una visita de fin de semana."},

    # Semana 5
    {"fecha": "26 Oct (Lun)", "semana": "Semana 5", "titulo": "Los pájaros", "autor": "Daphne du Maurier", "duracion": "45-60 min", "subgenero": "Naturaleza Hostil", "sinopsis": "De forma inexplicable, las aves comienzan a atacar organizadamente a los seres humanos a lo largo de las costas de Inglaterra."},
    {"fecha": "27 Oct (Mar)", "semana": "Semana 5", "titulo": "Owl Creek Bridge", "autor": "Ambrose Bierce", "duracion": "15-20 min", "subgenero": "Guerra / Percepción", "sinopsis": "Un prisionero de la Guerra Civil estadounidense experimenta una impactante distorsión del tiempo y la conciencia ante la horca."},
    {"fecha": "28 Oct (Mié)", "semana": "Semana 5", "titulo": "Después (Afterward)", "autor": "Edith Wharton", "duracion": "30-40 min", "subgenero": "Fantasmas / Culpa Financiera", "sinopsis": "Una pareja se muda a una casa de campo donde sólo se descubre que un fantasma ha estado presente mucho tiempo después de verlo."},
    {"fecha": "29 Oct (Jue)", "semana": "Semana 5", "titulo": "Ellos (They)", "autor": "Rudyard Kipling", "duracion": "40-50 min", "subgenero": "Fantasmas / Duelo", "sinopsis": "Un automovilista descubre una remota mansión habitada por una anciana ciega y los espíritus transparentes de niños fallecidos."},
    {"fecha": "30 Oct (Vie)", "semana": "Semana 5", "titulo": "Sleepy Hollow", "autor": "Washington Irving", "duracion": "45-60 min", "subgenero": "Leyenda / Folklore", "sinopsis": "El maestro de escuela Ichabod Crane es perseguido en la noche de la cañada por la aterradora figura del Jinete Sin Cabeza."},
    {"fecha": "31 Oct (Sáb)", "semana": "Semana 5", "titulo": "Markheim (Cierre Halloween)", "autor": "Robert Louis Stevenson", "duracion": "40-50 min", "subgenero": "Moralidad / Diablo", "sinopsis": "Tras cometer un asesinato en una tienda de antigüedades el día de Navidad, un hombre es visitado por una entidad misteriosa."}
]

# Inicializar Estado de la Sesión para almacenar calificaciones
if "ratings" not in st.session_state:
    st.session_state.ratings = {}
if "reviews" not in st.session_state:
    st.session_state.reviews = {}
if "read_status" not in st.session_state:
    st.session_state.read_status = {}

# --- SIDEBAR: Filtros y Progreso ---
st.sidebar.image("https://img.icons8.com/color/96/pumpkin.png", width=80)
st.sidebar.title("Navegación 💀")

semanas_opciones = ["Todas", "Semana 1", "Semana 2", "Semana 3", "Semana 4", "Semana 5"]
semana_filtro = st.sidebar.selectbox("Filtrar por Semana:", semanas_opciones)

busqueda = st.sidebar.text_input("Buscar cuento o autor:", "")

st.sidebar.markdown("---")
st.sidebar.subheader("📊 Tu Progreso del Mes")
total_leidos = sum(1 for status in st.session_state.read_status.values() if status)
porcentaje = int((total_leidos / len(STORIES_DATA)) * 100)

st.sidebar.progress(porcentaje / 100)
st.sidebar.write(f"**{total_leidos} de {len(STORIES_DATA)}** cuentos leídos ({porcentaje}%)")

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Califica cada relato con estrellas (1 a 5 💀) para armar el ranking oficial del club.")

# --- ENCABEZADO PRINCIPAL ---
st.title("🎃 Octubre de Horror: Club de Lectura")
st.caption("Evaluador interactivo y registro de lecturas para el mes del terror")

# Métricas Principales
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Obras", len(STORIES_DATA))
with col2:
    st.metric("Leídos", total_leidos)
with col3:
    ratings_vals = list(st.session_state.ratings.values())
    avg_rating = round(sum(ratings_vals) / len(ratings_vals), 1) if ratings_vals else "N/A"
    st.metric("Promedio General", f"{avg_rating} 💀" if avg_rating != "N/A" else "Sin datos")
with col4:
    st.metric("Tiempo Medio", "~35 min/cuento")

st.markdown("---")

# PESTAÑAS PRINCIPALES
tab1, tab2, tab3 = st.tabs(["📚 Catálogo & Evaluador", "🏆 Ranking & Estadísticas", "💬 Preguntas de Debate"])

# --- TAB 1: CATÁLOGO Y EVALUADOR ---
with tab1:
    # Filtrar datos
    cuentos_filtrados = STORIES_DATA
    if semana_filtro != "Todas":
        cuentos_filtrados = [c for c in cuentos_filtrados if c["semana"] == semana_filtro]
    if busqueda:
        cuentos_filtrados = [c for c in cuentos_filtrados if busqueda.lower() in c["titulo"].lower() or busqueda.lower() in c["autor"].lower()]

    st.subheader(f"Mostrando {len(cuentos_filtrados)} relato(s)")

    for item in cuentos_filtrados:
        key = item["titulo"]
        
        with st.container():
            st.markdown(f"""
            <div class="story-card">
                <span class="story-title">🗓️ {item['fecha']} — {item['titulo']}</span><br/>
                <span class="story-meta">✍️ <b>{item['autor']}</b> | ⏱️ {item['duracion']} | 🏷️ <i>{item['subgenero']}</i></span><br/>
                <p>{item['sinopsis']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            c_check, c_rate, c_review = st.columns([1, 2, 3])
            
            with c_check:
                is_read = st.checkbox("¿Leído? ✅", key=f"read_{key}", value=st.session_state.read_status.get(key, False))
                st.session_state.read_status[key] = is_read
            
            with c_rate:
                rating_labels = {1: "1 💀 (Mediocre)", 2: "2 💀 (Pasable)", 3: "3 💀 (Bueno)", 4: "4 💀 (Aterrador)", 5: "5 💀 (Obra Maestra)"}
                current_val = st.session_state.ratings.get(key, 3)
                user_rating = st.select_slider(
                    "Calificación:",
                    options=[1, 2, 3, 4, 5],
                    value=current_val,
                    format_func=lambda x: f"{x} 💀",
                    key=f"rate_{key}"
                )
                st.session_state.ratings[key] = user_rating
            
            with c_review:
                user_rev = st.text_input("Comentario rápido:", value=st.session_state.reviews.get(key, ""), key=f"rev_{key}")
                st.session_state.reviews[key] = user_rev
            
            st.markdown("---")

# --- TAB 2: RANKING Y ESTADÍSTICAS ---
with tab2:
    st.subheader("🏆 Ranking de Cuentos del Club")
    
    if not st.session_state.ratings:
        st.warning("Aún no has calificado ningún cuento. ¡Comienza a evaluar en el catálogo!")
    else:
        ranking_list = []
        for c in STORIES_DATA:
            t = c["titulo"]
            if t in st.session_state.ratings:
                ranking_list.append({
                    "Título": t,
                    "Autor": c["autor"],
                    "Calificación": st.session_state.ratings[t],
                    "Reseña": st.session_state.reviews.get(t, ""),
                    "Leído": "Sí" if st.session_state.read_status.get(t, False) else "No"
                })
        
        df_rank = pd.DataFrame(ranking_list).sort_values(by="Calificación", ascending=False)
        
        st.dataframe(
            df_rank,
            column_config={
                "Calificación": st.column_config.NumberColumn("Estrellas/Calaveras", format="%d 💀")
            },
            use_container_width=True
        )
        
        # Botón de Descarga
        csv = df_rank.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Exportar mis calificaciones (CSV)",
            data=csv,
            file_name="mis_calificaciones_octubre_de_horror.csv",
            mime="text/csv"
        )

# --- TAB 3: PREGUNTAS DE DEBATE ---
with tab3:
    st.subheader("💬 Guía de Preguntas para las Reuniones del Club")
    
    st.markdown("""
    ### 🏛️ **Semana 1: Decadencia y Horror Cósmico**
    * **1 Oct - La caída de la Casa Usher (Poe):** ¿Consideran que la casa tiene vida propia o es solo el reflejo del colapso mental de Roderick?
    * **2 Oct - The Mezzotint (James):** ¿Qué tan efectivo es el recurso del grabado cambiante frente a un susto directo?
    * **4 Oct - Los sauces (Blackwood):** ¿En qué momento se rompe la barrera entre la paranoia humana y la fuerza sobrenatural?
    
    ### 👁️ **Dinámica para el Sábado Libre:**
    > *"¿Cuál de las tres atmósferas de la primera semana te provocó mayor inquietud y por qué?"*
    """)
