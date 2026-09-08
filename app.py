import streamlit as st
from datetime import datetime
import pandas as pd
import uuid

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

st.set_page_config(page_title="Murlyka Lab", page_icon="🐱", layout="wide")
st.title("🐱 Murlyka Lab")

# Инициализация состояния
if "formula" not in st.session_state:
    st.session_state.formula = []

# ==========================================
# 🔝 ВЕРХ: КАЛЬКУЛЯТОР БЕЗОПАСНОСТИ
# ==========================================
st.header("🧪 Калькулятор Безопасности")

cv1, cv2 = st.columns(2)
with cv1: calc_conc_drops = st.slider("Капель концентрата", 1, 100, 30, key="ccd")
with cv2: calc_alc_drops = st.slider("Капель спирта", 0, 200, 30, key="cad")
calc_total = calc_conc_drops + calc_alc_drops
st.caption(f"Готовый продукт: **{calc_total} капель**")

cc1, cc2 = st.columns(2)
with cc1: calc_comp = st.selectbox("Компонент", list(COMPONENTS.keys()), key="ccomp")
with cc2: calc_conc = st.selectbox("Концентрация (%)", [100,50,30,20,10,5,2,1], index=0, key="cconc")

if st.button("Рассчитать!", type="primary", use_container_width=True, key="cbtn"):
    d = COMPONENTS[calc_comp]
    cf = calc_conc / 100.0
    e_ifra = 100.0 if d["ifra_limit"] == 100.0 else d["ifra_limit"] / cf
    e_rec = d["rec_dose"] / cf
    mx = int(calc_total * e_ifra / 100)
    rc = round(calc_total * e_rec / 100, 1)
    st.divider()
    st.subheader(f"📊 {calc_comp}")
    m1, m2 = st.columns(2)
    with m1: st.metric("Рекомендуемая доза", f"{rc} кап.", f"{e_rec:.2f}%")
    with m2: st.metric("Максимум по IFRA", f"{mx} кап.", f"{e_ifra:.2f}%")

# ==========================================
# 👇 НИЗ: ЖУРНАЛ ТЕСТОВ (СТАБИЛЬНАЯ ВЕРСИЯ)
# ==========================================
st.divider()
st.header("📓 Журнал Тестов")

jv1, jv2 = st.columns(2)
with jv1: j_conc_drops = st.slider("Капель концентрата", 1, 100, 30, key="jcd")
with jv2: j_alc_drops = st.slider("Капель спирта", 0, 200, 30, key="jad")
j_total = j_conc_drops + j_alc_drops
st.caption(f"Готовый продукт: **{j_total} капель**")

# ✅ ИСПОЛЬЗУЕМ st.form ДЛЯ СТАБИЛЬНОГО ДОБАВЛЕНИЯ
st.subheader("🧪 Добавить ингредиент")
with st.form("add_form", clear_on_submit=True):
    fa1, fa2, fa3, fa4 = st.columns([2,2,1,1])
    with fa1: f_comp = st.selectbox("Компонент", list(COMPONENTS.keys()), key="fcomp")
    with fa2: f_conc = st.selectbox("Концентрация (%)", [100,50,30,20,10,5,2,1], index=0, key="fconc")
    with fa3: f_drops = st.number_input("Капель", min_value=1, step=1, value=1, key="fdr")
    with fa4: submitted = st.form_submit_button("➕ Добавить", use_container_width=True)

if submitted and f_drops >= 1:
    lbl = f"{f_comp} ({f_conc}%)" if f_conc < 100 else f"{f_comp} (чистый)"
    st.session_state.formula.append({
        "id": str(uuid.uuid4())[:8],
        "label": lbl,
        "drops": int(f_drops),
        "comp_name": f_comp,
        "concentration": f_conc
    })

# ✅ УДАЛЕНИЕ ЧЕРЕЗ СЕЛЕКТОР (100% СТАБИЛЬНО)
if st.session_state.formula:
    st.divider()
    
    # Расчёт таблицы
    total_ing = sum(i["drops"] for i in st.session_state.formula)
    rows = []
    has_violation = False
    
    for i in st.session_state.formula:
        pc = round((i["drops"]/total_ing)*100, 2) if total_ing > 0 else 0
        pf_total = round((i["drops"]/j_total)*100, 3) if j_total > 0 else 0
        
        comp_data = COMPONENTS.get(i["comp_name"], {})
        ifra_limit = comp_data.get("ifra_limit", 100.0)
        active_pct_in_final = pf_total * (i["concentration"] / 100.0)
        
        status = "✅"
        if ifra_limit < 100.0 and active_pct_in_final > ifra_limit:
            status = "❌ ПРЕВЫШЕНИЕ!"
            has_violation = True
        
        rows.append({
            "Компонент": i["label"],
            "Капли": i["drops"],
            "% конц.": pc,
            "% актив. в готов.": round(active_pct_in_final, 3),
            "IFRA": status
        })
    
    df = pd.DataFrame(rows)
    
    def highlight_violation(row):
        if "ПРЕВЫШЕНИЕ" in str(row["IFRA"]):
            return ["background-color: #ffcccc"] * len(row)
        return [""] * len(row)
    
    st.dataframe(df.style.apply(highlight_violation, axis=1), use_container_width=True, hide_index=True)
    
    if has_violation:
        st.error("🚨 ВНИМАНИЕ: Превышение лимитов IFRA!")
    
    if abs(total_ing - j_conc_drops) > 0:
        st.warning(f"⚠️ Сумма ингредиентов ({total_ing}) ≠ концентрату ({j_conc_drops})")

    # ✅ УДАЛЕНИЕ: выбираем из списка → удаляем по ID
    st.subheader("🗑️ Удалить ингредиент")
    del_options = {f"{i['label']} ({i['drops']} кап.)": i["id"] for i in st.session_state.formula}
    del_selected = st.selectbox("Выберите для удаления", options=list(del_options.keys()), key="del_sel")
    if st.button("❌ Удалить выбранный", key="del_btn"):
        target_id = del_options[del_selected]
        st.session_state.formula = [x for x in st.session_state.formula if x["id"] != target_id]
        st.rerun()

    # ✅ КОПИРОВАНИЕ
    st.divider()
    copy_text = df.to_csv(sep='\t', index=False)
    st.text_area("📋 Скопируйте таблицу (Ctrl+C)", value=copy_text, height=150, key="copy_area")
    st.caption("TSV-формат — идеально для Excel/Notion")

    # Сохранение
    tname = st.text_input("Название теста", placeholder="Живой Лес v4.0", key="tn")
    save_disabled = has_violation
    if st.button("💾 Сохранить", type="primary", use_container_width=True, key="sbtn", disabled=save_disabled):
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
    st.info("👆 Добавьте ингредиенты выше через форму")
