import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Calculadora de Medicamentos", layout="centered")

st.sidebar.title("Menu")
opcao = st.sidebar.radio(
    "Selecione a função:",
    [
        "Cálculo de Dose (máximo e mínimo)",
        "Equivalência entre Medicamentos"
    ]
)

st.title("💊 Calculadora de Medicamentos")

if opcao == "Cálculo de Dose (máximo e mínimo)":
    st.header("Cálculo de Dose Máxima e Mínima")

    st.markdown(
        "Preencha as informações abaixo para calcular a dose mínima e máxima diária de um medicamento, "
        "com resultados para 1x, 2x, 3x e 4x ao dia."
    )
    concentracao = st.number_input("🔬 Concentração (mg/mL)", min_value=0.01, step=0.1, value=100.0, format="%.2f")
    gotas_por_ml = st.number_input("💧 Gotas por mL", min_value=1.0, step=1.0, value=20.0)
    peso = st.number_input("⚖️ Peso do paciente (kg)", min_value=0.01, step=0.1, value=20.0, format="%.2f")
    dose_min_kg = st.number_input("🔻 Dose **mínima** (mg/kg/dia)", min_value=0.01, step=0.1, value=2.5, format="%.2f")
    dose_max_kg = st.number_input("🔺 Dose **máxima** (mg/kg/dia)", min_value=0.01, step=0.1, value=25.0, format="%.2f")

    def calcular_dose(dose_mg_kg):
        total_mg = dose_mg_kg * peso
        total_ml = total_mg / concentracao
        total_gotas = total_ml * gotas_por_ml
        return {
            "mg/dia": round(total_mg, 2),
            "ml/dia": round(total_ml, 2),
            "gotas/dia": round(total_gotas, 2),
            "ml_1x": round(total_ml, 2),
            "ml_2x": round(total_ml / 2, 2),
            "ml_3x": round(total_ml / 3, 2),
            "ml_4x": round(total_ml / 4, 2),
            "gotas_1x": round(total_gotas, 2),
            "gotas_2x": round(total_gotas / 2, 2),
            "gotas_3x": round(total_gotas / 3, 2),
            "gotas_4x": round(total_gotas / 4, 2),
        }

    dose_min = calcular_dose(dose_min_kg)
    dose_max = calcular_dose(dose_max_kg)

    st.markdown("## 💊 Resultado")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔻 Dose **Mínima**")
        st.metric("Total diário (mg)", f"{dose_min['mg/dia']} mg")
        st.write(f"**💧 {dose_min['gotas/dia']} gotas / {dose_min['ml/dia']} mL por dia**")
        st.markdown(f"""
        - **1x/dia**: {dose_min['gotas_1x']} gotas ({dose_min['ml_1x']} mL)
        - **2x/dia**: {dose_min['gotas_2x']} gotas ({dose_min['ml_2x']} mL)
        - **3x/dia**: {dose_min['gotas_3x']} gotas ({dose_min['ml_3x']} mL)
        - **4x/dia**: {dose_min['gotas_4x']} gotas ({dose_min['ml_4x']} mL)
        """)

    with col2:
        st.subheader("🔺 Dose **Máxima**")
        st.metric("Total diário (mg)", f"{dose_max['mg/dia']} mg")
        st.write(f"**💧 {dose_max['gotas/dia']} gotas / {dose_max['ml/dia']} mL por dia**")
        st.markdown(f"""
        - **1x/dia**: {dose_max['gotas_1x']} gotas ({dose_max['ml_1x']} mL)
        - **2x/dia**: {dose_max['gotas_2x']} gotas ({dose_max['ml_2x']} mL)
        - **3x/dia**: {dose_max['gotas_3x']} gotas ({dose_max['ml_3x']} mL)
        - **4x/dia**: {dose_max['gotas_4x']} gotas ({dose_max['ml_4x']} mL)
        """)

elif opcao == "Equivalência entre Medicamentos":
    st.header("Equivalência entre Medicamentos em Solução")
    st.markdown(
        "Preencha as informações dos dois medicamentos. Informe quantas gotas ou mL está utilizando do medicamento A, "
        "e veja automaticamente a dose equivalente para o medicamento B."
    )

    st.subheader("Medicamento A (origem)")
    conc_a = st.number_input("Concentração A (mg/mL)", min_value=0.01, value=100.0, format="%.2f", key="conc_a")
    gotas_a = st.number_input("Gotas por mL A", min_value=1.0, value=20.0, step=1.0, key="gotas_a")

    st.subheader("Medicamento B (destino)")
    conc_b = st.number_input("Concentração B (mg/mL)", min_value=0.01, value=50.0, format="%.2f", key="conc_b")
    gotas_b = st.number_input("Gotas por mL B", min_value=1.0, value=25.0, step=1.0, key="gotas_b")

    st.subheader("Dose utilizada no Medicamento A")
    tipo_dose = st.radio("Como deseja informar a dose de A?", ["Gotas", "mL"], key="tipo_dose")
    dose_a_gotas = dose_a_ml = 0

    if tipo_dose == "Gotas":
        dose_a_gotas = st.number_input("Quantidade de gotas de A", min_value=0.0, value=20.0, step=1.0, key="dose_a_gotas")
        dose_a_ml = dose_a_gotas / gotas_a
    elif tipo_dose == "mL":
        dose_a_ml = st.number_input("Quantidade de mL de A", min_value=0.0, value=1.0, step=0.1, format="%.2f", key="dose_a_ml")
        dose_a_gotas = dose_a_ml * gotas_a

    # Cálculo da dose em mg aplicada
    dose_a_mg = dose_a_ml * conc_a

    # Equivalência no medicamento B
    dose_b_ml = dose_a_mg / conc_b
    dose_b_gotas = dose_b_ml * gotas_b

    st.markdown("---")
    st.markdown("## 🔄 Equivalência de Dose")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("No Medicamento A (original)")
        st.write(f"**{dose_a_gotas:.2f} gotas** ou **{dose_a_ml:.2f} mL**")
        st.write(f"Concentração: {conc_a} mg/mL")
        st.write(f"Total de princípio ativo: **{dose_a_mg:.2f} mg**")

    with col2:
        st.subheader("Equivalente no Medicamento B")
        st.write(f"**{dose_b_gotas:.2f} gotas** ou **{dose_b_ml:.2f} mL**")
        st.write(f"Concentração: {conc_b} mg/mL")
        st.write(f"Total de princípio ativo: **{dose_a_mg:.2f} mg** (mantido)")

st.markdown("---")
st.caption(f"© Petrus Costa {datetime.now().year} • Calculadora para soluções medicamentosas.")
