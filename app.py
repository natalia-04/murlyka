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
# 🔝 КАЛЬКУЛЯТОР БЕЗОПАСНОСТИ (КАК БЫЛО)
# ==========================================
st.header("🧪 Калькулятор Безопасности")

unit_mode = st.radio("Единицы:", ["💧 В каплях", "⚖️ В граммах"], horizontal=True, key="calc_unit")

if unit_mode == "💧 В каплях":
    cv1, cv2 = st.columns(2)
    with cv1: calc_conc_drops = st.number_input("Капли концентрата", min_value=1, value=30, step=1, key="ccd")
    with cv2: calc_alc_drops = st.number_input("Капли спирта", min_value=0, value=30, step=1, key="cad")
    calc_total_drops = calc_conc_drops + calc_alc_drops
    st.caption(f"Всего в смеси: **{calc_total_drops} капель**")
else:
    cv1, cv2 = st.columns(2)
    with cv1: calc_conc = st.slider("Концентрат (г)", 0.01, 50.0, 1.0, step=0.01, format="%.2f", key="ccg")
    with cv2: calc_alc = st.slider("Спирт (г)", 0.0, 100.0, 1.0, step=0.01, format="%.2f", key="cag")
    calc_total = calc_conc + calc_alc
    st.caption(f"Готовый продукт: **{calc_total:.2f} г**")

cc1, cc2 = st.columns(2)
with cc1: calc_comp = st.selectbox("Компонент", list(COMPONENTS.keys()), key="ccomp")
with cc2: calc_concentration = st.selectbox("Концентрация (%)", [100,50,30,20,10,5,2,1], index=0, key="cconc")

if st.button("Рассчитать!", type="primary", use_container_width=True, key="cbtn"):
    d = COMPONENTS[calc_comp]
    cf = calc_concentration / 100.0
    
    if unit_mode == "💧 В каплях":
        # Объёмный % лимита в смеси
        max_vol_pct = d["ifra_limit"] / cf if cf > 0 else 0
        # Сколько капель компонента можно добавить в эту смесь
        safe_drops = round((max_vol_pct / 100) * calc_total_drops, 1)
        
        st.divider()
        st.subheader(f"📊 {calc_comp}")
        m1, m2 = st.columns(2)
        with m1: st.metric("Безопасно капель", f"≈ {safe_drops} кап.")
        with m2: st.metric("Лимит IFRA", f"{d['ifra_limit']}%")
        st.caption(f"Для смеси из {calc_conc_drops} кап. концентрата + {calc_alc_drops} кап. спирта")
        
    else:
        e_ifra = 100.0 if d["ifra_limit"] == 100.0 else d["ifra_limit"] / cf
        e_rec = d["rec_dose"] / cf
        mx = round(calc_total * e_ifra / 100, 3)
        rc = round(calc_total * e_rec / 100, 3)
        st.divider()
        st.subheader(f"📊 {calc_comp}")
        m1, m2 = st.columns(2)
        with m1: st.metric("Рекомендуемая доза", f"{rc} г", f"{e_rec:.2f}%")
        with m2: st.metric("Максимум по IFRA", f"{mx} г", f"{e_ifra:.2f}%")

st.divider()

# ==========================================
# 👇 ЖУРНАЛ: ДВА РЕЖИМА ЧЕРЕЗ ВКЛАДКИ
# ==========================================
tab_drops, tab_grams = st.tabs(["💧 Капли (To Do)", "⚖️ Граммы (Замес)"])

# === ВКЛАДКА 1: КАПЛИ (TO DO) ===
with tab_drops:
    st.header("📝 Черновик в каплях")
    st.caption("Меняй капли концентрата/спирта — проценты и IFRA пересчитаются автоматически.")

    if "formula_drops" not in st.session_state:
        st.session_state.formula_drops = []

    # ✅ ЖИВЫЕ ПОЛЯ: изменение мгновенно обновляет всю таблицу
    dc1, dc2 = st.columns(2)
    with dc1: 
        total_conc_drops = st.number_input(
            "Капли концентрата (всего)", 
            min_value=1, 
            value=st.session_state.get("tcd_val", 30), 
            step=1, 
            key="tcd"
        )
        st.session_state.tcd_val = total_conc_drops
        
    with dc2: 
        total_alc_drops = st.number_input(
            "Капли спирта", 
            min_value=0, 
            value=st.session_state.get("tad_val", 30), 
            step=1, 
            key="tad"
        )
        st.session_state.tad_val = total_alc_drops
    
    total_mixture_drops = total_conc_drops + total_alc_drops
    st.caption(f"Всего в смеси: **{total_mixture_drops} капель**")

    a1, a2, a3, a4 = st.columns([2, 1, 1, 1])
    with a1: d_comp = st.selectbox("Компонент", list(COMPONENTS.keys()), key="d_comp")
    with a2: d_conc = st.selectbox("Конц. %", [100,50,30,20,10,5,2,1], index=0, key="d_conc")
    with a3: d_drops = st.number_input("Капли компонента", min_value=0, step=1, value=1, key="d_drops")
    with a4: d_add = st.button("➕ Добавить", use_container_width=True, key="d_btn")

    if d_add and d_drops > 0:
        st.session_state.formula_drops.append({
            "Компонент": d_comp,
            "Конц. %": d_conc,
            "Капли": d_drops
        })
        st.rerun()

    # ✅ ДИНАМИЧЕСКИЙ ПЕРЕСЧЁТ: таблица строится заново при каждом изменении полей
    if st.session_state.formula_drops:
        rows = []
        for item in st.session_state.formula_drops:
            vol_pct_in_mix = (item["Капли"] / total_mixture_drops) * 100 if total_mixture_drops > 0 else 0
            real_oil_pct = round(vol_pct_in_mix * (item["Конц. %"] / 100.0), 2)
            
            comp_data = COMPONENTS.get(item["Компонент"], {})
            ifra_limit = comp_data.get("ifra_limit", 100.0)
            
            status = "✅"
            if ifra_limit < 100.0 and real_oil_pct > ifra_limit:
                status = "🙀🙀🙀"

            rows.append({
                "Компонент": item["Компонент"],
                "Конц. %": item["Конц. %"],
                "Капли": item["Капли"],
                "% актив. (объёмн.)": real_oil_pct,
                "IFRA": status
            })

        df_drops = pd.DataFrame(rows)
        
        def highlight_violation_drops(row):
            if "🙀" in str(row["IFRA"]):
                return ["background-color: #ffcccc"] * len(row)
            return [""] * len(row)

        st.dataframe(df_drops.style.apply(highlight_violation_drops, axis=1), use_container_width=True, hide_index=True)

        copy_drops = df_drops.to_csv(sep='\t', index=False)
        st.components.v1.html(f"""
            <button onclick="navigator.clipboard.writeText(`{copy_drops}`);this.innerText='✅ Скопировано!';setTimeout(()=>this.innerText='📋 Скопировать To Do',2000);"
            style="width:100%;padding:8px;border:none;border-radius:6px;background:#4CAF50;color:white;font-size:14px;cursor:pointer;margin-top:10px;">
            📋 Скопировать To Do</button>
        """, height=45)

        del_cols = st.columns(min(len(st.session_state.formula_drops), 6))
        for idx, item in enumerate(st.session_state.formula_drops):
            col_idx = idx % 6
            with del_cols[col_idx]:
                short = item['Компонент'][:10] + ".." if len(item['Компонент']) > 10 else item['Компонент']
                if st.button(f"❌ {short}", key=f"del_d_{idx}", use_container_width=True):
                    st.session_state.formula_drops.pop(idx)
                    st.rerun()

        if st.button("🆕 Очистить To Do", use_container_width=True, key="clear_drops"):
            st.session_state.formula_drops = []
            st.rerun()
    else:
        st.info("👆 Добавь компоненты выше")

# === ВКЛАДКА 2: ГРАММЫ (ЗАМЕС) ===
with tab_grams:
    st.header("⚖️ Замес в граммах")
    st.caption("Точность. Безопасность. Экспорт в Google Таблицу.")

    if "formula_grams" not in st.session_state:
        st.session_state.formula_grams = []
    if "saved_journal" not in st.session_state:
        st.session_state.saved_journal = None

    jv1, jv2 = st.columns(2)
    with jv1: j_conc = st.number_input("Концентрат (г)", min_value=0.01, step=0.01, value=1.0, format="%.2f", key="jcg")
    with jv2: j_alc = st.number_input("Спирт (г)", min_value=0.0, step=0.01, value=1.0, format="%.2f", key="jag")
    j_total = j_conc + j_alc
    st.caption(f"Готовый продукт: **{j_total:.2f} г**")

    a1, a2, a3, a4, a5 = st.columns([2, 1, 1, 1, 1])
    with a1: j_comp = st.selectbox("Компонент", list(COMPONENTS.keys()), key="jcomp")
    with a2: j_concentration = st.selectbox("Конц. %", [100,50,30,20,10,5,2,1], index=0, key="jconc")
    with a3: j_grams = st.number_input("Граммы", min_value=0.001, step=0.001, value=0.030, format="%.3f", key="jgr")
    with a4: j_drops_ref = st.number_input("Капли (справ.)", min_value=0, step=1, value=0, key="jdr_ref")
    with a5: add_btn = st.button("➕", use_container_width=True, key="jbtn")

    if add_btn and j_grams > 0:
        st.session_state.formula_grams.append({
            "label": j_comp,
            "concentration": j_concentration,
            "grams": float(j_grams),
            "drops_ref": int(j_drops_ref),
            "comp_name": j_comp
        })
        st.rerun()

    if st.session_state.formula_grams:
        total_ing = sum(i["grams"] for i in st.session_state.formula_grams)
        rows = []
        has_violation = False
        total_real_oil = 0

        for i in st.session_state.formula_grams:
            pc = round((i["grams"] / total_ing) * 100, 2) if total_ing > 0 else 0
            real_oil = i["grams"] * (i["concentration"] / 100.0)
            total_real_oil += real_oil
            active_pct_in_final = round((real_oil / j_total) * 100, 3) if j_total > 0 else 0

            comp_data = COMPONENTS.get(i["comp_name"], {})
            ifra_limit = comp_data.get("ifra_limit", 100.0)

            status = "✅"
            if ifra_limit < 100.0 and active_pct_in_final > ifra_limit:
                status = "ПРЕВЫШЕНИЕ! 🙀🙀🙀"
                has_violation = True

            rows.append({
                "Компонент": i["label"],
                "Конц. %": i["concentration"],
                "Капли (справ.)": i["drops_ref"] if i["drops_ref"] > 0 else "—",
                "Граммы": i["grams"],
                "Масло (г)": round(real_oil, 3),
                "% конц.": pc,
                "% актив. готов.": active_pct_in_final,
                "IFRA": status
            })

        df = pd.DataFrame(rows)

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

        real_oil_pct_conc = round((total_real_oil / total_ing) * 100, 1) if total_ing > 0 else 0
        real_oil_pct_final = round((total_real_oil / j_total) * 100, 1) if j_total > 0 else 0

        s1, s2, s3 = st.columns(3)
        with s1: st.metric("Всего грамм", f"{total_ing:.3f}")
        with s2: st.metric("Реальное масло", f"{total_real_oil:.3f} г", f"{real_oil_pct_conc}% в концентрате")
        with s3: st.metric("Итоговая концентрация", f"{real_oil_pct_final}%", "в готовом продукте")

        if has_violation:
            st.error("🙀 ВНИМАНИЕ: Превышение лимитов IFRA!")

        if abs(total_ing - j_conc) > 0.001:
            st.warning(f"⚠️ Сумма ингредиентов ({total_ing:.3f} г) ≠ концентрату ({j_conc:.2f} г)")

        st.subheader("🗑️ Управление")
        del_cols = st.columns(min(len(st.session_state.formula_grams), 6))
        for idx, item in enumerate(st.session_state.formula_grams):
            col_idx = idx % 6
            with del_cols[col_idx]:
                short_label = item['label'][:12] + ".." if len(item['label']) > 12 else item['label']
                if st.button(f"❌ {short_label}", key=f"del_g_{idx}", use_container_width=True):
                    st.session_state.formula_grams.pop(idx)
                    st.rerun()

        
    else:
        st.info("👆 Добавьте ингредиенты выше")
