 import streamlit as st
import requests

def predict_location(x1, x2):
    y = -38.01 - 0.18 * x1 + 1.02 * x2
    return y

# Function to fetch data from Thingspeak
def fetch_data_from_thingspeak():
    api_key = "CN9Q31O2X9MM1SVD"
    channel_id = "2405457"
    url = f"https://api.thingspeak.com/channels/{channel_id}/feeds.json?api_key={api_key}&results=1"

    try:
        response = requests.get(url)
        data = response.json()["feeds"][0]
        return float(data["field1"]), float(data["field3"])
    except Exception as e:
        st.error(f"Error fetching data from Thingspeak: {e}")
        return None, None

# Main Streamlit app
def main():
    st.title('Pertamina Field')
    st.subheader('FOL (Finding Oil Losses)')
    st.subheader('Prediksi Lokasi Kebocoran Line BJG-TPN Regresi Model')

    # Fetch data from Thingspeak
    x1, x2 = fetch_data_from_thingspeak()

    # Display fetched data in input fields
    if x1 is not None and x2 is not None:
        Titik_1_PSI = st.text_input('Input Pressure di titik 1 (PSI)', value=str(x1))
        Titik_2_PSI = st.text_input('Input Pressure di titik 2 (PSI)', value=str(x2))

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
    else:
        st.warning("Failed to fetch data from Thingspeak. Please check your API key and channel ID.")

if __name__ == "__main__":
    main()
