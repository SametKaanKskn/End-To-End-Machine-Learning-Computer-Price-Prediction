import streamlit as st
import pandas as pd
import joblib

# Önceden eğitilmiş modelin yükledim
regressor = joblib.load("../Servisleme/Gradient_Boosting_Regresyon_model.pkl")


def main():

    st.set_page_config(
        page_title='Bilgisayar Fiyatı Tahmini Uygulaması',
        page_icon='💻',
        layout='wide',
        initial_sidebar_state='expanded'
    )

    

    # Parametre seçimleri için sidebar oluşturdum
    with st.sidebar:
        st.subheader('Parametre Seçimleri')

        # İşlemci Markası labelEncoder yaptıgım için hangi indekslerdeyse onun ismini yazmasını sagladım
        islemci_marka_dict = {'Intel': 1, 'Apple': 0, 'AMD': 2, 'Samsung': 7, 'Qualcomm': 6, 'MediaTek': 4, 'INTEL®': 3, 'Unisoc': 8, 'Spreadtrum': 5}
        islemci_markasi_options = list(islemci_marka_dict.keys())
        selected_islemci_marka_name = st.selectbox('İşlemci Markası', islemci_markasi_options)
        selected_islemci_marka_index = islemci_marka_dict[selected_islemci_marka_name]

        # İşlemci Teknolojisi labelEncoder yaptıgım için hangi indekslerdeyse onun ismini yazmasını sagladım
        islemci_teknolojisi_dict = {
            'Core i5': 17, 'Core i7': 19, 'M2': 33, 'Core i9': 20, 'M1': 28, 'Ryzen™ 7': 44, 'A14': 0, 'Ryzen™ 5': 42,
            'Core i3': 16, 'Exynos 1380': 11, 'M3 Pro': 29, 'M3': 26, 'A15': 1, 'A13': 2, 'Ryzen™ 9': 43, 'Quad-Core': 38,
            'Snapdragon® 8 Gen 2': 50, 'Qualcomm Snapdragon': 49, 'Celeron': 9, 'Mediatek': 27, 'M2 Pro': 34, 'Qualcomm SM6375': 51,
            'MT8781': 31, 'Intel® Core™ i5': 18, 'UniSOC T618': 48, 'Snapdragon 720G': 47, 'Octa Core': 36, 'Helio P60T': 24,
            'Qualcomm SM8450': 52, 'Qualcomm Snapdragon™ 680': 46, 'M2 Max': 35, 'Ryzen™ 3': 41, 'Unisoc T610': 45,
            'M3 Max': 30, 'MT8183': 32, 'Qualcomm SM7225': 53, '10. nesil Intel® Core™ i5': 13, '11. nesil Intel® Core™ i5': 14,
            'Ryzen™ Z1': 40, 'Intel® Core™ i3': 15, 'Ryzen™ Z1 Extreme': 39, 'Pentium® Silver': 37, 'MT8786': 25,
            'MT8788': 23, 'Snapdragon 8cx Gen 2': 21, 'Snapdragon 685': 22, 'Spreadtrum T610': 54, 'MT8167': 12
        }
        islemci_teknolojisi_options = list(islemci_teknolojisi_dict.keys())
        selected_islemci_teknolojisi_name = st.selectbox('İşlemci Teknolojisi', islemci_teknolojisi_options)
        selected_islemci_teknolojisi_index = islemci_teknolojisi_dict[selected_islemci_teknolojisi_name]

        # Marka labelEncoder yaptıgım için hangi indekslerdeyse onun ismini yazmasını sagladım
        marka_dict = {'Apple': 0, 'Asus': 1, 'Lenovo': 9, 'Hp': 4, 'Samsung': 14, 'Casper': 3, 'Acer': 2, 'Dell': 5, 'Msi': 10,
                      'Huawei': 6, 'EXPER': 7, 'Tcl': 15, 'Everpad': 8, 'Honor': 11, 'Hometech': 12, 'OMEN': 13, 'Xiaomi': 16,
                      'S-Link': 17}
        marka_options = list(marka_dict.keys())
        selected_marka_name = st.selectbox('Marka', marka_options)
        selected_marka_index = marka_dict[selected_marka_name]

        # İşlemci Nesli  bu kategorik veriler dışarısında veri olmayacagını için bunları göstermesini sagladım
        islemci_nesli_options = [13, 12, 10, 11, 7, 5, 6, 9]
        islemci_nesli = st.selectbox('İşlemci Nesli', islemci_nesli_options)

        # İşlemci Çekirdek Sayısı bu kategorik veriler dışarısında veri olmayacagını için bunları göstermesini sagladım
        islemci_cekirdek_sayisi_options = [8, 12, 6, 10, 14, 11, 4, 24, 2, 16]
        islemci_cekirdek_sayisi = st.selectbox('İşlemci Çekirdek Sayısı', islemci_cekirdek_sayisi_options)

        # İşlemci Ön Bellek bu kategorik veriler dışarısında veri olmayacagını için bunları göstermesini sagladım
        islemci_on_bellek_options = [20, 12, 24, 16, 36, 8, 18, 4, 30, 10, 18, 6, 64, 2, 32]
        islemci_on_bellek = st.selectbox('İşlemci Ön Bellek (MB)', islemci_on_bellek_options)

    
    st.markdown(
        """
        <style>
        body {
            background-color: #f3f3f3; /* Arka plan rengi */
            color: #333; /* Yazı rengi */
        }
        .sidebar .sidebar-content {
            background-color: #2e2e2e; /* Sidebar arka plan rengi */
            color: #fff; /* Sidebar yazı rengi */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Tahmin düğmesi
    if st.button('Fiyatı Tahmin Et'):
        input_data = {
            'islemci_markasi': selected_islemci_marka_index,
            'islemci_nesli': islemci_nesli,
            'islemci_teknolojisi': selected_islemci_teknolojisi_index,
            'islemci_cekirdek_sayisi': islemci_cekirdek_sayisi,
            'islemci_on_bellek': islemci_on_bellek,
            'marka': selected_marka_index
        }

        input_df = pd.DataFrame([input_data])
        prediction = regressor.predict(input_df)

        # Seçilen parametreleri gösterilmesini sagladım
        st.subheader('Seçilen Parametreler')
        st.write(f"İşlemci Markası: {selected_islemci_marka_name}")
        st.write(f"İşlemci Teknolojisi: {selected_islemci_teknolojisi_name}")
        st.write(f"Marka: {selected_marka_name}")
        st.write(f"İşlemci Nesli: {islemci_nesli}")
        st.write(f"İşlemci Çekirdek Sayısı: {islemci_cekirdek_sayisi}")
        st.write(f"İşlemci Ön Bellek: {islemci_on_bellek} MB")

        
        st.success(f"Tahmini Fiyat: {prediction[0]:,.2f} TL")

if __name__ == "__main__":
    main()
