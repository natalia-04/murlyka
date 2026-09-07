# 🧪 ПАРФЮМЕРНЫЙ КАЛЬКУЛЯТОР MURLYKA v2.4 WEB
# Сохрани как app.py и запусти: streamlit run app.py

import streamlit as st

# === БАЗА КОМПОНЕНТОВ (ИЗ ТВОЕГО ФИНАЛЬНОГО СПИСКА) ===
COMPONENTS = {
    "Iso E Super® (IFF)": {"ifra_limit": 20.0, "rec_dose": 20.0},
    "Ivy base 290958 (Firmenich)": {"ifra_limit": 3.0, "rec_dose": 1.5},
    "Habanolide® 947303 (Firmenich)": {"ifra_limit": 100.0, "rec_dose": 5.0},
    "CEDARWOOD HIMALAYAN EO": {"ifra_limit": 100.0, "rec_dose": 5.0},
    "Mentha piperita EO": {"ifra_limit": 100.0, "rec_dose": 1.0},
    "Ethyl Vanillin": {"ifra_limit": 100.0, "rec_dose": 8.0},
    "HELIOTROPIN": {"ifra_limit": 100.0, "rec_dose": 0.8},
    "Floralozone (IFF)": {"ifra_limit": 100.0, "rec_dose": 0.8},
    "Patchouli EO": {"ifra_limit": 100.0, "rec_dose": 5.0},
    "Отдушка Йогурт с курагой (Greenwax)": {"ifra_limit": 6.1, "rec_dose": 3.0},
    "Отдушка Кофейня (Candle Science)": {"ifra_limit": 6.6, "rec_dose": 3.3},
    "Отдушка Манго и кокосовое молоко (Candle Science)": {"ifra_limit": 74.99, "rec_dose": 37.0},
    "Отдушка Пряный мед и тонка (Candle Science)": {"ifra_limit": 17.76, "rec_dose": 8.8},
    "Ароматическое масло Молочный шоколад (Jean Claude)": {"ifra_limit": 35.0, "rec_dose": 17.5},
    "Verdox HC (IFF)": {"ifra_limit": 100.0, "rec_dose": 4.0},
    "Maltol (кристалл)": {"ifra_limit": 100.0, "rec_dose": 4.0},
    "Triplal (IFF)": {"ifra_limit": 2.5, "rec_dose": 0.5},
    "Blueberry Pie Oil (CND)": {"ifra_limit": 100.0, "rec_dose": 5.0},
    "Theaspirane (Givaudan)": {"ifra_limit": 100.0, "rec_dose": 0.5},
    "Delta Dodecalactone": {"ifra_limit": 100.0, "rec_dose": 1.5},
    "Peru Balsam Resinoid": {"ifra_limit": 0.41, "rec_dose": 0.02},
    "Cranberry Perfume Oil (CND)": {"ifra_limit": 100.0, "rec_dose": 5.0},
    "Bacdanol® TOCO (IFF)": {"ifra_limit": 100.0, "rec_dose": 5.0}
}

# === НАСТРОЙКА СТРАНИЦЫ ===
st.set_page_config(page_title="Murlyka Calculator", page_icon="🐱", layout="centered")
st.title("🧪 Парфюмерный Калькулятор Murlyka")
st.caption("Расчёт безопасных доз с учётом концентрации дилюции")

# === ИНТЕРФЕЙС ===
col1, col2 = st.columns(2)

with col1:
    drops = st.slider("Капель в тесте", min_value=1, max_value=100, value=30)
    component = st.selectbox("Компонент", list(COMPONENTS.keys()))

with col2:
    concentration = st.selectbox(
        "Концентрация (%)",
        options=[100, 50, 30, 20, 10, 5, 2, 1],
        index=0
    )

# === РАСЧЁТ И ВЫВОД ===
if st.button("Рассчитать!", type="primary", use_container_width=True):
    data = COMPONENTS[component]
    conc_fraction = concentration / 100.0
    
    effective_ifra = data["ifra_limit"] / conc_fraction
    effective_rec = data["rec_dose"] / conc_fraction
    
    max_drops = round(drops * effective_ifra / 100, 3)
    rec_drops = round(drops * effective_rec / 100, 3)
    
    st.divider()
    st.subheader(f" {component}")
    
    m1, m2 = st.columns(2)
    with m1:
        st.metric("Рекомендуемая доза", f"{rec_drops} кап.", f"{effective_rec:.2f}%")
    with m2:
        st.metric("Максимум по IFRA", f"{max_drops} кап.", f"{effective_ifra:.2f}%")
    
    if max_drops < rec_drops:
        st.error("⚠️ Рекомендуемая доза превышает лимит IFRA!")
    else:
        st.success("✅ Доза в пределах безопасности")
