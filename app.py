import streamlit as st
import pickle
import pandas as pd
import datetime

st.image(r"C:\Users\Rafael\cancer_research\logo.png", width=500)
st.header('ИИ-система поддержки принятия решений при проведении биопсии предстательной железы')
st.subheader('AI Decision Support for Prostate Biopsy')

height = st.number_input("Рост, см (Height, cm)")
weight = st.number_input("Вес, кг (Weight, cm)")
date_of_birth = st.date_input("Дата рождения (Date of birth)", min_value=datetime.date(1900, 1, 1))
relatives = st.number_input("""Наличие рака простаты у ближайших родственников (Positive family history of prostate cancer)""")
opsa = st.number_input("""оПСА (нг/мл)
                          (Total PSA level)""")
phi = st.number_input("Индекс здоровья простаты, Prostate health index")
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

with open(r'C:\Users\Rafael\cancer_research\model_cancer.pkl', 'rb') as f:
    clf = pickle.load(f)

prediction = clf.predict_proba(features)[1]

st.warning("""Данный сервис предназначен для профессионального использования медицинскими специалистами и применяется как инструмент вспомогательной оценки при определении целесообразности выполнения биопсии предстательной железы.
Результаты, предоставляемые сервисом, имеют информационный характер и не заменяют клинических рекомендаций специалиста.

Используя сервис, медицинский работник:
• подтверждает, что действует в пределах своей профессиональной компетенции и ответственности
• осознаёт, что решения о назначении диагностических процедур и вмешательств принимаются на основании комплексной клинической оценки, а не исключительно на основе данных, полученных с использованием сервиса
• подтверждает, что данные вводятся добровольно и в соответствии с действующим законодательством
• принимает, что авторы и правообладатели программного продукта не несут ответственности за возможные последствия клинических решений, принятых с его использованием

Все права на программное обеспечение принадлежат авторам. Незаконное копирование, модификация или распространение запрещены и преследуются в соответствии с законодательством Российской Федерации.

This service is intended for use by medical professionals as a support tool when assessing the need for prostate biopsy. The results are informational and do not replace clinical judgment.
By using the service, the healthcare professional:
• confirms they act within their competence
• understands that clinical decisions must be based on full evaluation, not only service data
• agrees that data entry is voluntary and compliant with the law
• accepts that the authors are not responsible for medical decisions made using the tool

All software rights are reserved. Unauthorized use, copying, or distribution is prohibited under Russian law.""")

if st.button('Получить результат'):

    st.text("Вероятность наличия рака предстательной железы: {:.2f}%".format(prediction))

    if prediction >= 0.5:
        st.error("Рекомендуется выполнение трансректальной биопсии предстательной железы (Transrectal prostate biopsy is recommended)")
    elif prediction >= 0.424:
        st.warning("Рекомендумется выполнение трансперинеальной фьюжн-биопсии предстательной железы (Fusion-guided transperineal prostate biopsy is recommended)")
    else:
        st.success("Рекомендуется динамическое наблюдение (Active surveillance is recommended)")

st.divider()

st.caption("""Разработчики: коллектив врачей Московского урологического центра ММНКЦ им. С.П.Боткина""")
st.caption("""Developed by: Medical team of the Moscow Urology Center, Botkin Hospital""")

st.caption("""Контакт для связи: dr.p.arutyunyan@gmail.com""")
st.caption("Contact: dr.p.arutyunyan@gmail.com")
