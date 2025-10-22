import streamlit as st
import pandas as pd
import re

# Configurare pagină
st.set_page_config(page_title="Generator Numere", page_icon="🎲", layout="wide")

# Titlu principal
st.title("🎲 Aplicație Gestionare Runde")

# Inițializare session state pentru păstrarea datelor
if 'rounds' not in st.session_state:
    st.session_state.rounds = []

# Sidebar pentru navigare
option = st.sidebar.selectbox(
    "Alege o opțiune:",
    ["📝 Adaugă Rundă", "🎯 Extrage Numere"]
)

# ========== OPȚIUNEA 1: ADAUGĂ RUNDĂ ==========
if option == "📝 Adaugă Rundă":
    st.header("Adaugă Rundă Nouă")
    
    st.write("**Copiază și lipește runda în formatul:**")
    st.code("3856680	22. 10. 2025	4:36	3, 50, 55, 56, 40, 9, 51, 36, 6, 46, 37, 5")
    
    # Input pentru runda completă
    round_input = st.text_area(
        "Lipește runda aici:",
        placeholder="3856680	22. 10. 2025	4:36	3, 50, 55, 56, 40, 9, 51, 36, 6, 46, 37, 5",
        height=100,
        key="round_input"
    )
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        # Buton pentru adăugare
        if st.button("➕ Adaugă Rundă", type="primary"):
            if round_input.strip():
                try:
                    # Procesare input - split by tab sau multiple spații
                    parts = re.split(r'\t+|\s{2,}', round_input.strip())
                    
                    if len(parts) >= 4:
                        round_id = parts[0].strip()
                        round_date = parts[1].strip()
                        round_time = parts[2].strip()
                        numbers = parts[3].strip()
                        
                        # Creare rundă
                        round_data = {
                            'Id': round_id,
                            'Data': round_date,
                            'Ora': round_time,
                            'Numere': numbers
                        }
                        
                        # Adăugare în session state
                        st.session_state.rounds.append(round_data)
                        
                        st.success(f"✅ Rundă {round_id} adăugată cu succes!")
                        
                        # Clear input
                        st.session_state.round_input = ""
                        st.rerun()
                    else:
                        st.error("⚠️ Formatul nu este corect! Asigură-te că ai toate cele 4 părți separate prin TAB.")
                except Exception as e:
                    st.error(f"⚠️ Eroare la procesare: {str(e)}")
            else:
                st.error("⚠️ Te rog introdu o rundă!")
    
    with col2:
        # Buton pentru ștergere ultimă rundă
        if st.session_state.rounds:
            if st.button("🗑️ Șterge Ultima Rundă"):
                st.session_state.rounds.pop()
                st.rerun()
    
    # Afișare toate rundele
    if st.session_state.rounds:
        st.divider()
        st.subheader("📊 Rundele Tale")
        
        # Creare DataFrame
        df = pd.DataFrame(st.session_state.rounds)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        col_export1, col_export2 = st.columns([1, 4])
        
        with col_export1:
            # Opțiune de export CSV
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descarcă CSV",
                data=csv,
                file_name="runde.csv",
                mime="text/csv",
            )
        
        with col_export2:
            # Buton pentru ștergere toate rundele
            if st.button("🗑️ Șterge Toate Rundele", type="secondary"):
                st.session_state.rounds = []
                st.rerun()

# ========== OPȚIUNEA 2: EXTRAGE NUMERE ==========
elif option == "🎯 Extrage Numere":
    st.header("Extrage Doar Numerele")
    
    if not st.session_state.rounds:
        st.warning("⚠️ Nu ai nicio rundă adăugată! Mergi la 'Adaugă Rundă' pentru a adăuga runde.")
    else:
        st.write(f"**Total runde: {len(st.session_state.rounds)}**")
        
        # Afișare toate numerele
        st.divider()
        
        for idx, round_data in enumerate(st.session_state.rounds, 1):
            # Afișare info rundă
            st.markdown(f"**Rundă #{idx}** - ID: {round_data['Id']} | Data: {round_data['Data']} | Ora: {round_data['Ora']}")
            
            # Afișare numere în cutie mare
            numbers = round_data['Numere']
            
            st.markdown(f"""
            <div style="
                background-color: #f0f2f6;
                padding: 20px;
                border-radius: 10px;
                font-size: 20px;
                font-weight: bold;
                margin: 10px 0 20px 0;
            ">
                {numbers}
            </div>
            """, unsafe_allow_html=True)
            
            # Buton pentru copiere
            st.code(numbers, language=None)
        
        # Export toate numerele
        st.divider()
        st.subheader("📋 Export Toate Numerele")
        
        all_numbers = "\n".join([round_data['Numere'] for round_data in st.session_state.rounds])
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.text_area(
                "Toate numerele:",
                value=all_numbers,
                height=200
            )
        
        with col2:
            # Buton descărcare text
            st.download_button(
                label="📥 Descarcă TXT",
                data=all_numbers.encode('utf-8'),
                file_name="numere.txt",
                mime="text/plain",
            )

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    Made with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)
