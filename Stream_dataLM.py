import streamlit as st


def predict_location(x1, x2):
    y = -38.01 - 0.18 * x1 + 1.02 * x2
    return y

# Main Streamlit app
def main():
    st.title('Pertamina Field')
    st.subheader('FOL (Finding Oil Losses)')
    st.subheader('Prediksi Lokasi Kebocoran Line BJG-TPN Regresi Model')

    Titik_1_PSI = st.text_input('Input Pressure di titik 1 (PSI)')
    Titik_2_PSI = st.text_input('Input Pressure di titik 2 (PSI)')

    if st.button('Prediksi Lokasi'):
        try:
            x1 = float(Titik_1_PSI)
            x2 = float(Titik_2_PSI)
            prediksi_lokasi = predict_location(x1, x2)
            
            if prediksi_lokasi <= 0: # titik nol
                suspect_loct = 'It is safe that there is no fluid flowingr'
            elif prediksi_lokasi >= 26.38: # total panjang trunkline
                suspect_loct = 'Safe, there are no leaks'
            else:
                suspect_loct = f'Estimated leak location {prediksi_lokasi} KM'
            st.success(suspect_loct)
        except Exception as e:
            st.error(f"Error predicting location: {e}")

if __name__ == "__main__":
    main()
