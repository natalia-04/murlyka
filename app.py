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

st.set_page_config(page_title="Murlyka Lab", page_icon="😺", layout="wide")
st.title("😺 Murlyka Lab")

# ==========================================
# 🔝 ВЕРХ: КАЛЬКУЛЯТОР БЕЗОПАСНОСТИ
# ==========================================
st.header("🧪 Калькулятор Безопасности")

# ✅ ВЫБОР ЕДИНИЦ ИЗМЕРЕНИЯ
unit_mode = st.radio("Единицы измерения", ["Капли", "Граммы"], horizontal=True, key="calc_unit")

cv1, cv2 = st.columns(2)
with cv1:
    if unit_mode == "Капли":
        calc_conc = st.slider("Концентрат (кап.)", 1, 100, 30, key="ccd")
    else:
        calc_conc = st.number_input("Концентрат (г)", min_value=0.01, step=0.01, value=1.0, format="%.2f", key="ccg")
with cv2:
    if unit_mode == "Капли":
        calc_alc = st.slider("Спирт (кап.)", 0, 200, 30, key="cad")
    else:
        calc_alc = st.number_input("Спирт (г)", min_value=0.0, step=0.01, value=1.0, format="%.2f", key="cag")

calc_total = calc_conc + calc_alc
unit_label = "капель" if unit_mode == "Капли" else "г"
st.caption(f"Готовый продукт: **{calc_total:.2f} {unit_label}**")

cc1, cc2 = st.columns(2)
with cc1: calc_comp = st.selectbox("Компонент", list(COMPONENTS.keys()), key="ccomp")
with cc2: calc_concentration = st.selectbox("Концентрация (%)", [100,50,30,20,10,5,2,1], index=0, key="cconc")

if st.button("Рассчитать!", type="primary", use_container_width=True, key="cbtn"):
    d = COMPONENTS[calc_comp]
    cf = calc_concentration / 100.0
    e_ifra = 100.0 if d["ifra_limit"] == 100.0 else d["ifra_limit"] / cf
    e_rec = d["rec_dose"] / cf
    
    # ✅ Расчёт максимума в выбранных единицах
    mx_raw = calc_total * e_ifra / 100
    rc_raw = calc_total * e_rec / 100
    
    if unit_mode == "Капли":
        mx = int(mx_raw)
        rc = round(rc_raw, 1)
    else:
        mx = round(mx_raw, 3)
        rc = round(rc_raw, 3)
    
    st.divider()
    st.subheader(f"📊 {calc_comp}")
    m1, m2 = st.columns(2)
    with m1: st.metric("Рекомендуемая доза", f"{rc} {unit_label}", f"{e_rec:.2f}%")
    with m2: st.metric("Максимум по IFRA", f"{mx} {unit_label}", f"{e_ifra:.2f}%")

# ==========================================
# 👇 НИЗ: ЖУРНАЛ ТЕСТОВ
# ==========================================
st.divider()
st.header("📓 Журнал Тестов")

if "formula" not in st.session_state:
    st.session_state.formula = []
if "saved_journal" not in st.session_state:
    st.session_state.saved_journal = None

# ✅ ВЫБОР ЕДИНИЦ ДЛЯ ЖУРНАЛА
journal_unit = st.radio("Единицы измерения", ["Капли", "Граммы"], horizontal=True, key="jour_unit")

jv1, jv2 = st.columns(2)
with jv1:
    if journal_unit == "Капли":
        j_conc = st.slider("Концентрат (кап.)", 1, 100, 30, key="jcd")
    else:
        j_conc = st.number_input("Концентрат (г)", min_value=0.01, step=0.01, value=1.0, format="%.2f", key="jcg")
with jv2:
    if journal_unit == "Капли":
        j_alc = st.slider("Спирт (кап.)", 0, 200, 30, key="jad")
    else:
        j_alc = st.number_input("Спирт (г)", min_value=0.0, step=0.01, value=1.0, format="%.2f", key="jag")

j_total = j_conc + j_alc
ju_label = "капель" if journal_unit == "Капли" else "г"
st.caption(f"Готовый продукт: **{j_total:.2f} {ju_label}**")

st.subheader("🧪 Добавить ингредиент")
a1, a2, a3, a4 = st.columns([2,2,1,1])
with a1: j_comp = st.selectbox("Компонент", list(COMPONENTS.keys()), key="jcomp")
with a2: j_concentration = st.selectbox("Концентрация (%)", [100,50,30,20,10,5,2,1], index=0, key="jconc")
with a3:
    if journal_unit == "Капли":
        j_amount = st.number_input("Капель", min_value=1, step=1, value=1, key="jdr")
    else:
        j_amount = st.number_input("Граммов", min_value=0.001, step=0.001, value=0.03, format="%.3f", key="jgr")
with a4: add_btn = st.button("➕ Добавить", use_container_width=True, key="jbtn")

if add_btn:
    lbl = f"{j_comp} ({j_concentration}%)" if j_concentration < 100 else f"{j_comp} (чистый)"
    st.session_state.formula.append({
        "label": lbl, 
        "amount": float(j_amount),
        "comp_name": j_comp,
        "concentration": j_concentration,
        "unit": journal_unit
    })
    st.rerun()

if st.session_state.formula:
    st.divider()
    total_ing = sum(i["amount"] for i in st.session_state.formula)
    
    rows = []
    has_violation = False
    total_real_oil = 0
    
    for idx, i in enumerate(st.session_state.formula):
        pc = round((i["amount"]/total_ing)*100, 2) if total_ing > 0 else 0
        
        # ✅ Реальное чистое масло
        real_oil = i["amount"] * (i["concentration"] / 100.0)
        total_real_oil += real_oil
        
        # ✅ % активного в готовом (работает и для капель, и для граммов!)
        active_pct_in_final = round((real_oil / j_total) * 100, 3) if j_total > 0 else 0
        
        comp_data = COMPONENTS.get(i["comp_name"], {})
        ifra_limit = comp_data.get("ifra_limit", 100.0)
        
        status = "✅"
        if ifra_limit < 100.0 and active_pct_in_final > ifra_limit:
            status = "🙀🙀🙀 ПРЕВЫШЕНИЕ!"
            has_violation = True
        
        rows.append({
            "Компонент": i["label"], 
            ju_label.capitalize(): i["amount"],
            "Реальное масло": round(real_oil, 3),
            "% конц.": pc, 
            "% актив. в готов.": active_pct_in_final,
            "IFRA": status
        })
    
    df = pd.DataFrame(rows)
    
    # ✅ КОПИРОВАНИЕ
    copy_text = df.to_csv(sep='\t', index=False)
    st.components.v1.html(f"""
        <button onclick="navigator.clipboard.writeText(`{copy_text}`);this.innerText='✅ Скопировано!';setTimeout(()=>this.innerText='📋 Скопировать таблицу',2000);"
        style="width:100%;padding:10px;border:none;border-radius:6px;background:#ff4b4b;color:white;font-size:16px;cursor:pointer;">
        📋 Скопировать таблицу</button>
    """, height=50)
    
    def highlight_violation(row):
        if "ПРЕВЫШЕНИЕ" in str(row["IFRA"]):
            return ["background-color: #ffcccc"] * len(row)
        return [""] * len(row)
    
    st.dataframe(df.style.apply(highlight_violation, axis=1), use_container_width=True, hide_index=True)
    
    # ✅ ИТОГОВАЯ СТАТИСТИКА
    real_oil_pct_conc = round((total_real_oil / total_ing) * 100, 1) if total_ing > 0 else 0
    real_oil_pct_final = round((total_real_oil / j_total) * 100, 1) if j_total > 0 else 0
    
    s1, s2, s3 = st.columns(3)
    with s1: st.metric(f"Всего {ju_label}", f"{total_ing:.2f}")
    with s2: st.metric("Реальное масло", f"{total_real_oil:.2f}", f"{real_oil_pct_conc}% в концентрате")
    with s3: st.metric("Итоговая концентрация", f"{real_oil_pct_final}%", "в готовом продукте")
    
    if has_violation:
        st.error("🙀🙀🙀 ВНИМАНИЕ: Превышение лимитов IFRA!")
    
    if abs(total_ing - j_conc) > 0.01:
        st.warning(f"⚠️ Сумма ингредиентов ({total_ing:.2f}) ≠ концентрату ({j_conc:.2f})")

    # ✅ УДАЛЕНИЕ
    st.subheader("🗑️ Управление")
    del_cols = st.columns(min(len(st.session_state.formula), 6))
    for idx, item in enumerate(st.session_state.formula):
        col_idx = idx % 6
        with del_cols[col_idx]:
            short_label = item['label'][:12] + ".." if len(item['label']) > 12 else item['label']
            if st.button(f"❌ {short_label}", key=f"del_{idx}", use_container_width=True):
                st.session_state.formula.pop(idx)
                st.rerun()

    # ✅ СОХРАНЕНИЕ
    st.divider()
    tname = st.text_input("Название теста", placeholder="Живой Лес v4.0", key="tn")
    
    if st.button("💾 Сохранить", type="primary", use_container_width=True, key="sbtn", disabled=has_violation):
        if tname.strip():
            jr = []
            for i in st.session_state.formula:
                pc = round((i["amount"]/total_ing)*100, 2) if total_ing > 0 else 0
                pf = round((i["amount"]/j_total)*100, 3) if j_total > 0 else 0
                real_oil = round(i["amount"] * (i["concentration"] / 100.0), 3)
                jr.append({"Название": tname, "Дата": datetime.now().strftime("%Y-%m-%d %H:%M"),
                           "Компонент": i["label"], ju_label.capitalize(): i["amount"],
                           "Реальное масло": real_oil, "% конц.": pc, "% готов.": pf})
            st.session_state.saved_journal = pd.DataFrame(jr)
            st.success(f"✅ '{tname}' сохранён!")
        else:
            st.warning("⚠️ Введите название!")
    
    if st.session_state.saved_journal is not None:
        st.divider()
        st.subheader("💾 Последний сохранённый тест")
        st.dataframe(st.session_state.saved_journal, use_container_width=True, hide_index=True)
        if st.button("🆕 Новый тест (очистить формулу)", use_container_width=True, key="new_test"):
            st.session_state.formula = []
            st.session_state.saved_journal = None
            st.rerun()

else:
    st.info("👆 Добавьте ингредиенты выше")
