import streamlit as st
from datetime import datetime
import pandas as pd

# === БАЗА КОМПОНЕНТОВ ===
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

if "formula" not in st.session_state:
    st.session_state.formula = []

st.set_page_config(page_title="Murlyka Lab Journal", page_icon="🐱", layout="wide")
st.title("📓 Лабораторный Журнал Murlyka")

# === ДВА БЕГУНКА ОБЪЁМА ===
st.subheader("⚗️ Объём теста")
vol_col1, vol_col2 = st.columns(2)
with vol_col1:
    concentrate_drops = st.slider("Капель концентрата", min_value=1, max_value=100, value=30, key="conc_vol")
with vol_col2:
    alcohol_drops = st.slider("Капель спирта", min_value=0, max_value=200, value=30, key="alc_vol")

total_final_drops = concentrate_drops + alcohol_drops
st.caption(f"Итого готовый продукт: **{total_final_drops} капель**")

# === ДОБАВЛЕНИЕ ИНГРЕДИЕНТА ===
st.divider()
st.subheader("🧪 Добавить ингредиент")
add_col1, add_col2, add_col3, add_col4 = st.columns([2, 2, 1, 1])

with add_col1:
    component = st.selectbox("Компонент", list(COMPONENTS.keys()), key="comp_select")
with add_col2:
    concentration = st.selectbox(
        "Концентрация (%)",
        options=[100, 50, 30, 20, 10, 5, 2, 1],
        index=0,
        key="conc_select"
    )
with add_col3:
    drops = st.number_input("Капель", min_value=0.0, step=0.5, value=1.0, key="drops_input")
with add_col4:
    add_btn = st.button("➕ Добавить", use_container_width=True)

if add_btn and drops > 0:
    label = f"{component} ({concentration}%)" if concentration < 100 else f"{component} (чистый)"
    st.session_state.formula.append({
        "label": label,
        "drops": drops,
        "concentration": concentration
    })
    st.rerun()

# === ТАБЛИЦА ФОРМУЛЫ ===
if st.session_state.formula:
    st.divider()
    st.subheader("📋 Текущая формула")
    
    total_ing_drops = sum(item["drops"] for item in st.session_state.formula)
    
    rows = []
    for item in st.session_state.formula:
        pct_conc = round((item["drops"] / total_ing_drops) * 100, 2) if total_ing_drops > 0 else 0
        pct_final = round((item["drops"] / total_final_drops) * 100, 3) if total_final_drops > 0 else 0
        rows.append({
            "Компонент": item["label"],
            "Капли": item["drops"],
            "% в концентрате": pct_conc,
            "% в готовом": pct_final
        })
    
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Предупреждение если сумма капель ингредиентов != объёму концентрата
    if abs(total_ing_drops - concentrate_drops) > 0.5:
        st.warning(f"⚠️ Сумма ингредиентов ({total_ing_drops} кап.) ≠ объёму концентрата ({concentrate_drops} кап.)")
    
    # === СОХРАНЕНИЕ ===
    st.divider()
    test_name = st.text_input("Название теста", placeholder="Например: Живой Лес v4.0")
    
    if st.button("💾 Сохранить в журнал", type="primary", use_container_width=True):
        if test_name.strip():
            journal_rows = []
            for item in st.session_state.formula:
                pct_conc = round((item["drops"] / total_ing_drops) * 100, 2) if total_ing_drops > 0 else 0
                pct_final = round((item["drops"] / total_final_drops) * 100, 3) if total_final_drops > 0 else 0
                journal_rows.append({
                    "Название": test_name,
                    "Дата": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Компонент": item["label"],
                    "Капли": item["drops"],
                    "% конц.": pct_conc,
                    "% готов.": pct_final
                })
            
            st.success(f"✅ Тест '{test_name}' сохранён!")
            st.dataframe(pd.DataFrame(journal_rows), use_container_width=True, hide_index=True)
            st.session_state.formula = []
            st.rerun()
        else:
            st.warning("⚠️ Введите название теста!")
else:
    st.info("👆 Добавьте ингредиенты выше")
