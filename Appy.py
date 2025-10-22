import streamlit as st
import pandas as pd

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
    st.header("Adaugă Runde")
    
    st.write("**Lipește rundele aici (câte una pe linie):**")
    st.code("3856671	22. 10. 2025	4:27	36, 52, 22, 47, 2, 50, 62, 63, 21, 10, 54, 34")
    
    # Text area mare pentru multiple runde
    rounds_input = st.text_area(
        "Lipește toate rundele (poți adăuga 500-5000 runde):",
        placeholder="3856671	22. 10. 2025	4:27	36, 52, 22, 47, 2, 50, 62, 63, 21, 10, 54, 34\n3856672	22. 10. 2025	4:28	15, 30, 45, 60, 12, 24, 36, 48, 3, 6, 9, 18",
        height=300
    )
    
    col1, col2, col3 = st.columns([1, 1, 3])
    
    with col1:
        if st.button("➕ Adaugă Rundele", type="primary"):
            if rounds_input.strip():
                lines = rounds_input.strip().split('\n')
                added_count = 0
                error_count = 0
                
                for line in lines:
                    if line.strip():
                        try:
                            # Split by tab
                            parts = line.strip().split('\t')
                            
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
                                added_count += 1
                            else:
                                error_count += 1
                        except Exception as e:
                            error_count += 1
                
                if added_count > 0:
                    st.success(f"✅ {added_count} runde adăugate cu succes!")
                if error_count > 0:
                    st.warning(f"⚠️ {error_count} runde nu au putut fi adăugate (format incorect)")
                
                st.rerun()
            else:
                st.error("⚠️ Te rog introdu cel puțin o rundă!")
    
    with col2:
        if st.session_state.rounds:
            if st.button("🗑️ Șterge Tot"):
                st.session_state.rounds = []
                st.rerun()
    
    # Afișare număr de runde
    if st.session_state.rounds:
        st.divider()
        st.subheader(f"📊 Total Runde: {len(st.session_state.rounds)}")
        
        # Afișare primele 10 runde ca preview
        st.write("**Preview (primele 10 runde):**")
        df_preview = pd.DataFrame(st.session_state.rounds[:10])
        st.dataframe(df_preview, use_container_width=True, hide_index=True)
        
        if len(st.session_state.rounds) > 10:
            st.info(f"... și încă {len(st.session_state.rounds) - 10} runde")
        
        # Buton export CSV
        col_export1, col_export2 = st.columns([1, 4])
        with col_export1:
            df_all = pd.DataFrame(st.session_state.rounds)
            csv = df_all.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descarcă toate rundele (CSV)",
                data=csv,
                file_name="runde_complete.csv",
                mime="text/csv",
            )

# ========== OPȚIUNEA 2: EXTRAGE NUMERE ==========
elif option == "🎯 Extrage Numere":
    st.header("Extrage Numere")
    
    if not st.session_state.rounds:
        st.warning("⚠️ Nu ai nicio rundă adăugată! Mergi la 'Adaugă Runde' mai întâi.")
    else:
        st.write(f"**Total runde disponibile: {len(st.session_state.rounds)}**")
        
        st.divider()
        
        # Buton de extragere
        if st.button("🔍 Extrage Numerele", type="primary", use_container_width=False):
            st.success(f"✅ {len(st.session_state.rounds)} seturi de numere extrase!")
            
            st.divider()
            st.subheader("📋 Numerele Extrase")
            
            # Creare listă cu toate numerele
            all_numbers = []
            for round_data in st.session_state.rounds:
                all_numbers.append(round_data['Numere'])
            
            # Afișare în text area mare
            numbers_text = "\n".join(all_numbers)
            
            st.text_area(
                f"Toate numerele ({len(all_numbers)} runde):",
                value=numbers_text,
                height=400
            )
            
            # Buton descărcare
            col_download1, col_download2 = st.columns([1, 4])
            with col_download1:
                st.download_button(
                    label="📥 Descarcă Numerele (TXT)",
                    data=numbers_text.encode('utf-8'),
                    file_name="numere_extrase.txt",
                    mime="text/plain",
                )
            
            # Preview primele 5 runde
            st.divider()
            st.write("**Preview (primele 5 seturi de numere):**")
            
            for idx, numbers in enumerate(all_numbers[:5], 1):
                st.markdown(f"""
                <div style="
                    background-color: #f0f2f6;
                    padding: 15px;
                    border-radius: 8px;
                    margin: 10px 0;
                    font-size: 18px;
                    font-weight: bold;
                ">
                    Rundă #{idx}: {numbers}
                </div>
                """, unsafe_allow_html=True)
            
            if len(all_numbers) > 5:
                st.info(f"... și încă {len(all_numbers) - 5} seturi de numere")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    Made with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)