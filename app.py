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
                        ["Нет", "Да", "Неизвестно"])
    relatives = 1 if relatives == "Да" else 0

    # Добавить расу

    opsa = st.number_input("""Общий ПСА (нг/мл)""")
    phi = st.number_input("""Индекс здоровья простаты""", min_value=0)

    date = st.date_input("""Дата МРТ""",
                         min_value=datetime.date(1900, 1, 1))
    pi_rads = st.select_slider("Данные МРТ, PI-RADS", [1, 2, 3, 4, 5])
    suspicious_areas = st.radio("""Подозрительные очаги ТРУЗИ/Гистосканирование""",
                                ["Нет", "Да"])

    # УЗИ может быть неизвестно (подумать) (Неизвестно != нет)

    suspicious_areas = 1 if suspicious_areas == "Да" else 0

    volume_of_suspicious_areas = st.number_input("""Обьем подозрительных участков (см3) ТРУЗИ/Гистосканирование""")
    pri = st.radio("""Данные ПРИ (укажите 1 - наличие изменений, подозрительных на рак простаты,
                             0 - отсутствие изменений, подозрительных на рак простаты)""",
                          [0, 1])
    # Обучить вторую модель без ПРИ

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
                        ["No", "Yes", "No information"])
    relatives = 1 if relatives == "Yes" else 0

    opsa = st.number_input("""Total PSA level (ng/ml)""")
    phi = st.number_input("""Prostate health index""", min_value=0)

    date = st.date_input("""Date of MRI""", min_value=datetime.date(1900, 1, 1))
    pi_rads = st.select_slider("PI-RADS", [1, 2, 3, 4, 5])
    suspicious_areas = st.radio("""Suspicious lesions TRUS/HistoScanning""",
                                ["No", "Yes"])
    suspicious_areas = 1 if suspicious_areas == "Yes" else 0

    volume_of_suspicious_areas = st.number_input("""Volume of suspicious prostate lesions TRUS/HistoScanning (cm3)""")
    pri = st.radio("""DRE findings:
                      1 – presence of findings suspicious for prostate cancer
                      0 – no findings suspicious for prostate cancer""",
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
    st.header("""Система поддержки принятия врачебных решений на основе
                 искусственного интеллекта перед проведением биопсии предстательной железы""")
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
                "Рекомендуется выполнение трансректальной биопсии предстательной железы")
        elif prediction >= 40:
            st.warning(
                "Рекомендумется выполнение трансперинеальной фьюжн-биопсии предстательной железы")
        else:
            st.success("Рекомендуется динамическое наблюдение")

    st.divider()

    st.caption("""Разработчики: коллектив врачей Московского урологического центра ММНКЦ им. С.П.Боткина""")
    st.caption("""Контакт для связи: dr.p.arutyunyan@gmail.com""")

else:
    st.header('AI Clinical Decision Support System before Prostate Biopsy')
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


