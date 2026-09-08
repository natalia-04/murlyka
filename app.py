import streamlit as st
from datetime import datetime
import pandas as pd

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

st.set_page_config(page_title="Murlyka Lab", page_icon="🐱", layout="wide")
st.title("🐱 Murlyka Lab")

# ==========================================
# 🔝 ВЕРХ: КАЛЬКУЛЯТОР БЕЗОПАСНОСТИ (С ДВУМЯ БЕГУНКАМИ!)
# ==========================================
st.header("🧪 Калькулятор Безопасности")
st.caption("Проверка лимитов IFRA в ГОТОВОМ продукте")

cv1, cv2 = st.columns(2)
with cv1: calc_conc_drops = st.slider("Капель концентрата", 1, 100, 30, key="ccd")
with cv2: calc_alc_drops = st.slider("Капель спирта", 0, 200, 30, key="cad")
calc_total = calc_conc_drops + calc_alc_drops
st.caption(f"Итого готовый продукт: **{calc_total} капель**")

cc1, cc2 = st.columns(2)
with cc1: calc_comp = st.selectbox("Компонент", list(COMPONENTS.keys()), key="ccomp")
with cc2: calc_conc = st.selectbox("Концентрация (%)", [100,50,30,20,10,5,2,1], index=0, key="cconc")

if st.button("Рассчитать!", type="primary", use_container_width=True, key="cbtn"):
    d = COMPONENTS[calc_comp]
    cf = calc_conc / 100.0
    e_ifra = 100.0 if d["ifra_limit"] == 100.0 else d["ifra_limit"] / cf
    e_rec = d["rec_dose"] / cf
    # ✅ Считаем максимум в КОНЦЕНТРАТЕ, но исходя из объёма ГОТОВОГО продукта
    mx = round(calc_total * e_ifra / 100, 3)
    rc = round(calc_total * e_rec / 100, 3)
    st.divider()
    st.subheader(f"📊 {calc_comp}")
    m1, m2 = st.columns(2)
    with m1: st.metric("Рекомендуемая доза", f"{rc} кап.", f"{e_rec:.2f}%")
    with m2: st.metric("Максимум по IFRA", f"{mx} кап.", f"{e_ifra:.2f}%")

# ==========================================
# 👇 НИЗ: ЖУРНАЛ ТЕСТОВ (С ДВУМЯ БЕГУНКАМИ!)
# ==========================================
st.divider()
st.header("📓 Журнал Тестов")
st.caption("Сборка формулы + запись % в готовом продукте")

if "formula" not in st.session_state:
    st.session_state.formula = []

jv1, jv2 = st.columns(2)
with jv1: j_conc_drops = st.slider("Капель концентрата", 1, 100, 30, key="jcd")
with jv2: j_alc_drops = st.slider("Капель спирта", 0, 200, 30, key="jad")
j_total = j_conc_drops + j_alc_drops
st.caption(f"Итого готовый продукт: **{j_total} капель**")

st.subheader("🧪 Добавить ингредиент")
a1, a2, a3, a4 = st.columns([2,2,1,1])
with a1: j_comp = st.selectbox("Компонент", list(COMPONENTS.keys()), key="jcomp")
with a2: j_concentration = st.selectbox("Концентрация (%)", [100,50,30,20,10,5,2,1], index=0, key="jconc")
with a3: j_drops = st.number_input("Капель", min_value=0.0, step=0.5, value=1.0, key="jdr")
with a4: add_btn = st.button("➕ Добавить", use_container_width=True, key="jbtn")

if add_btn and j_drops > 0:
    lbl = f"{j_comp} ({j_concentration}%)" if j_concentration < 100 else f"{j_comp} (чистый)"
    st.session_state.formula.append({"label": lbl, "drops": j_drops})
    st.rerun()

if st.session_state.formula:
    st.divider()
    total_ing = sum(i["drops"] for i in st.session_state.formula)
    rows = []
    for i in st.session_state.formula:
        pc = round((i["drops"]/total_ing)*100, 2) if total_ing > 0 else 0
        pf = round((i["drops"]/j_total)*100, 3) if j_total > 0 else 0
        rows.append({"Компонент": i["label"], "Капли": i["drops"], "% в концентрате": pc, "% в готовом": pf})
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    if abs(total_ing - j_conc_drops) > 0.5:
        st.warning(f"⚠️ Сумма ингредиентов ({total_ing}) ≠ концентрату ({j_conc_drops})")

    tname = st.text_input("Название теста", placeholder="Живой Лес v4.0", key="tn")
    if st.button("💾 Сохранить", type="primary", use_container_width=True, key="sbtn"):
        if tname.strip():
            jr = []
            for i in st.session_state.formula:
                pc = round((i["drops"]/total_ing)*100, 2) if total_ing > 0 else 0
                pf = round((i["drops"]/j_total)*100, 3) if j_total > 0 else 0
                jr.append({"Название": tname, "Дата": datetime.now().strftime("%Y-%m-%d %H:%M"),
                           "Компонент": i["label"], "Капли": i["drops"], "% конц.": pc, "% готов.": pf})
            st.success(f"✅ '{tname}' сохранён!")
            st.dataframe(pd.DataFrame(jr), use_container_width=True, hide_index=True)
            st.session_state.formula = []
            st.rerun()
        else:
            st.warning("⚠️ Введите название!")
else:
    st.info("👆 Добавьте ингредиенты выше")
