import streamlit as st
import pandas as pd
import re

# Configurare pagină
st.set_page_config(page_title="Generator Numere", page_icon="🎲", layout="wide")

# Titlu principal
st.title("🎲 Aplicație Gestionare Runde")

# Inițializare session state
if 'rounds' not in st.session_state:
    st.session_state.rounds = []

# Sidebar pentru navigare
option = st.sidebar.selectbox(
    "Alege o opțiune:",
    ["📝 Adaugă Runde", "🎯 Extrage Numere"]
)

# ========== OPȚIUNEA 1: ADAUGĂ RUNDE ==========
if option == "📝 Adaugă Runde":
    st.header("Adaugă Runde Noi")
    
    st.write("**Formatul rundei:**")
    st.code("3856673	22. 10. 2025	4:29	24, 16, 8, 29, 56, 27, 63, 2, 64, 30, 1, 66")
    
    # Input pentru rundă
    round_input = st.text_area(
        "Lipește runda aici:",
        placeholder="3856673	22. 10. 2025	4:29	24, 16, 8, 29, 56, 27, 63, 2, 64, 30, 1, 66",
        height=100
    )
    
    col1, col2, col3 = st.columns([1, 1, 3])
    
    with col1:
        if st.button("➕ Adaugă Rundă", type="primary"):
            if round_input.strip():
                try:
                    # Split by tab
                    parts = round_input.strip().split('\t')
                    
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
                        
                        st.success(f"✅ Rundă {round_id} adăugată!")
                        st.rerun()
                    else:
                        st.error("⚠️ Formatul nu este corect!")
                except Exception as e:
                    st.error(f"⚠️ Eroare: {str(e)}")
            else:
                st.error("⚠️ Te rog introdu o rundă!")
    
    with col2:
        if st.session_state.rounds:
            if st.button("🗑️ Șterge Ultima"):
                st.session_state.rounds.pop()
                st.rerun()
    
    # Afișare runde
    if st.session_state.rounds:
        st.divider()
        st.subheader(f"📊 Rundele Tale ({len(st.session_state.rounds)} runde)")
        
        # Creare DataFrame
        df = pd.DataFrame(st.session_state.rounds)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Butoane export și ștergere
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 3])
        
        with col_btn1:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descarcă CSV",
                data=csv,
                file_name="runde.csv",
                mime="text/csv",
            )
        
        with col_btn2:
            if st.button("🗑️ Șterge Tot"):
                st.session_state.rounds = []
                st.rerun()

# ========== OPȚIUNEA 2: EXTRAGE NUMERE ==========
elif option == "🎯 Extrage Numere":
    st.header("Extrage Numere")
    
    if not st.session_state.rounds:
        st.warning("⚠️ Nu ai nicio rundă adăugată! Mergi la 'Adaugă Runde' mai întâi.")
    else:
        st.write(f"**Total runde disponibile: {len(st.session_state.rounds)}**")
        
        # Tabel cu rundele
        st.divider()
        st.subheader("📋 Rundele Tale")
        
        df = pd.DataFrame(st.session_state.rounds)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Buton de extragere
        st.divider()
        st.subheader("🎯 Extragere Numere")
        
        if st.button("🔍 Extrage Numerele", type="primary", use_container_width=False):
            st.success("✅ Numere extrase cu succes!")
            
            st.divider()
            
            # Afișare numere pentru fiecare rundă
            for idx, round_data in enumerate(st.session_state.rounds, 1):
                st.markdown(f"**Rundă #{idx}** (ID: {round_data['Id']})")
                
                numbers = round_data['Numere']
                
                # Afișare în cutie mare
                st.markdown(f"""
                <div style="
                    background-color: #f0f2f6;
                    padding: 20px;
                    border-radius: 10px;
                    font-size: 20px;
                    font-weight: bold;
                    margin: 10px 0;
                ">
                    {numbers}
                </div>
                """, unsafe_allow_html=True)
                
                # Cod pentru copy-paste
                st.code(numbers, language=None)
                
                st.markdown("---")
            
            # Export toate numerele
            st.divider()
            st.subheader("📥 Export Toate Numerele")
            
            all_numbers = "\n".join([round_data['Numere'] for round_data in st.session_state.rounds])
            
            col_export1, col_export2 = st.columns([4, 1])
            
            with col_export1:
                st.text_area(
                    "Toate numerele (câte o rundă pe linie):",
                    value=all_numbers,
                    height=200
                )
            
            with col_export2:
                st.download_button(
                    label="📥 Descarcă TXT",
                    data=all_numbers.encode('utf-8'),
                    file_name="numere_extrase.txt",
                    mime="text/plain",
                )

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    Made with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)