import streamlit as st
import pandas as pd
import datetime
from model import Classifier

st.image("logo.png", width=500)
st.header('ИИ-система поддержки принятия решений при проведении биопсии предстательной железы')
st.subheader('AI Decision Support for Prostate Biopsy')


def get_input():
    height = st.number_input("Рост, см (Height, cm)")
    weight = st.number_input("Вес, кг (Weight, cm)")
    date_of_birth = st.date_input("Дата рождения (Date of birth)",
                                  min_value=datetime.date(1900, 1, 1))
    relatives = st.number_input("""Наличие рака простаты у ближайших родственников 
                                   (Positive family history of prostate cancer)""")
    opsa = st.number_input("""оПСА (нг/мл)
                          (Total PSA level)""")
    phi = st.number_input("""Индекс здоровья простаты,
                            Prostate health index""")
    date = st.date_input("""Дата МРТ (Date of MRI)""",
                         min_value=datetime.date(1900, 1, 1))
    pi_rads = st.number_input("Данные МРТ, PI-RADS")
    suspicious_areas = st.number_input("""Подозрительные очаги при УЗИ
                                       (Suspicious lesions on TRUS)""")
    volume_of_suspicious_areas = st.number_input("""Обьем подозрительных участков (см3)
                                                    (Volume of suspicious prostate lesions on TRUS (cm3))""")
    pri = st.number_input("""Данные ПРИ (укажите 1 - при наличии подозрительных изменений (уплотнение и др.),
                             0 - при гомогенной железе без изменений) 
                            (DRE findings:
                            1 - suspicious changes (e.g., induration, nodularity)
                            0 - normal (homogeneous prostate))""")

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

features = get_input()
with open('warning.txt', 'r', encoding="utf8") as f:
    warning = f.read()

st.warning(warning)

if st.button('Получить результат'):
    model = Classifier()
    prediction = model.predict(features)[1]

    st.text("Вероятность наличия рака предстательной железы: {:.2f}%".format(prediction))

    if prediction >= 0.5:
        st.error("Рекомендуется выполнение трансректальной биопсии предстательной железы (Transrectal prostate biopsy is recommended)")
    elif prediction >= 0.45:
        st.warning("Рекомендумется выполнение трансперинеальной фьюжн-биопсии предстательной железы (Fusion-guided transperineal prostate biopsy is recommended)")
    else:
        st.success("Рекомендуется динамическое наблюдение (Active surveillance is recommended)")

st.divider()

st.caption("""Разработчики: коллектив врачей Московского урологического центра ММНКЦ им. С.П.Боткина""")
st.caption("""Developed by: Medical team of the Moscow Urology Center, Botkin Hospital""")

st.caption("""Контакт для связи: dr.p.arutyunyan@gmail.com""")
st.caption("Contact: dr.p.arutyunyan@gmail.com")
