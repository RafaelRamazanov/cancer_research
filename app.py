import streamlit as st
import pandas as pd
import datetime
from model import Classifier

language = st.sidebar.selectbox('', ['ru', 'en'])

st.image("logo.png", width=500)

def get_input_ru():
    height = st.number_input("Рост, см", min_value=0)
    weight = st.number_input("Вес, кг", min_value=0)
    date_of_birth = st.date_input("Дата рождения",
                                  min_value=datetime.date(1900, 1, 1))
    relatives = st.radio("""Наличие рака простаты у ближайших родственников""",
                        ["Нет", "Да"])
    relatives = 1 if relatives == "Да" else 0

    opsa = st.number_input("""оПСА (нг/мл)""")
    phi = st.number_input("""Индекс здоровья простаты""", min_value=0)

    date = st.date_input("""Дата МРТ""",
                         min_value=datetime.date(1900, 1, 1))
    pi_rads = st.select_slider("Данные МРТ, PI-RADS", [1, 2, 3, 4, 5])
    suspicious_areas = st.radio("""Подозрительные очаги при УЗИ""",
                                ["Нет", "Да"])
    suspicious_areas = 1 if suspicious_areas == "Да" else 0

    volume_of_suspicious_areas = st.number_input("""Обьем подозрительных участков (см3)""")
    pri = st.radio("""Данные ПРИ (укажите 1 - при наличии подозрительных изменений (уплотнение и др.),
                             0 - при гомогенной железе без изменений)""",
                          [0, 1])

    date_of_birth = (pd.to_datetime('today') - pd.to_datetime(date_of_birth)).days
    date = (pd.to_datetime('today') - pd.to_datetime(date)).days

    features = [date_of_birth,
                height,
                weight,
                relatives,
                opsa,
                phi,
                date,
                pi_rads,
                pri,
                suspicious_areas,
                volume_of_suspicious_areas]

    return features

def get_input_en():
    height = st.number_input("Height, cm", min_value=0)
    weight = st.number_input("Weight, cm", min_value=0)
    date_of_birth = st.date_input("Date of birth",
                                  min_value=datetime.date(1900, 1, 1))
    relatives = st.radio("""Positive family history of prostate cancer""",
                        ["No", "Yes"])
    relatives = 1 if relatives == "Yes" else 0

    opsa = st.number_input("""Total PSA level""")
    phi = st.number_input("""Prostate health index""", min_value=0)

    date = st.date_input("""Date of MRI""",
                         min_value=datetime.date(1900, 1, 1))
    pi_rads = st.select_slider("PI-RADS", [1, 2, 3, 4, 5])
    suspicious_areas = st.radio("""Suspicious lesions on TRUS""",
                                ["No", "Yes"])
    suspicious_areas = 1 if suspicious_areas == "Yes" else 0

    volume_of_suspicious_areas = st.number_input("""Volume of suspicious prostate lesions on TRUS (cm3)""")
    pri = st.radio("""DRE findings:
                      1 - suspicious changes (e.g., induration, nodularity)
                      0 - normal (homogeneous prostate))""",
                    [0, 1])

    date_of_birth = (pd.to_datetime('today') - pd.to_datetime(date_of_birth)).days
    date = (pd.to_datetime('today') - pd.to_datetime(date)).days

    features = [date_of_birth,
                height,
                weight,
                relatives,
                opsa,
                phi,
                date,
                pi_rads,
                pri,
                suspicious_areas,
                volume_of_suspicious_areas]

    return features

if language == 'ru':
    st.header('ИИ-система поддержки принятия решений при проведении биопсии предстательной железы')
    features = get_input_ru()
    with open('warning_ru.txt', 'r', encoding="utf8") as f:
        warning = f.read()

    with st.expander("Информация"):
        st.warning(warning)

    if st.button('Получить результат'):
        model = Classifier()
        prediction = int(model.predict([features])[0][1] * 100)

        st.text("Вероятность наличия рака предстательной железы: {:.2f}%".format(prediction))

        if prediction >= 80:
            st.error(
                "Рекомендуется выполнение трансректальной биопсии предстательной железы (Transrectal prostate biopsy is recommended)")
        elif prediction >= 40:
            st.warning(
                "Рекомендумется выполнение трансперинеальной фьюжн-биопсии предстательной железы (Fusion-guided transperineal prostate biopsy is recommended)")
        else:
            st.success("Рекомендуется динамическое наблюдение (Active surveillance is recommended)")

    st.divider()

    st.caption("""Разработчики: коллектив врачей Московского урологического центра ММНКЦ им. С.П.Боткина""")
    st.caption("""Контакт для связи: dr.p.arutyunyan@gmail.com""")

else:
    st.header('AI Decision Support for Prostate Biopsy')
    features = get_input_en()
    with open('warning_en.txt', 'r', encoding="utf8") as f:
        warning = f.read()

    with st.expander("Information"):
        st.warning(warning)

    if st.button('Get result'):
        model = Classifier()
        prediction = int(model.predict([features])[0][1] * 100)

        st.text("Probability of prostate cancer presence: {:.2f}%".format(prediction))

        if prediction >= 80:
            st.error(
                "Transrectal prostate biopsy is recommended")
        elif prediction >= 40:
            st.warning(
                "Fusion-guided transperineal prostate biopsy is recommended")
        else:
            st.success("Active surveillance is recommended")

    st.divider()

    st.caption("""Developed by: Medical team of the Moscow Urology Center, Botkin Hospital""")
    st.caption("Contact: dr.p.arutyunyan@gmail.com")


