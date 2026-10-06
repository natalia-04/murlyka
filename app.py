import streamlit as st
from datetime import datetime
import pandas as pd

# ==========================================
#  БАЗА КОМПОНЕНТОВ (v5.5)
# ==========================================
COMPONENTS = {
    "Iso E Super® (IFF)": {"ifra_limit": 20.0, "rec_dose": 20.0, "default_conc": 100},
    "Ivy base 290958 (Firmenich)": {"ifra_limit": 3.0, "rec_dose": 1.5, "default_conc": 100},
    "Habanolide® 947303 (Firmenich)": {"ifra_limit": 100.0, "rec_dose": 5.0, "default_conc": 100},
    "CEDARWOOD HIMALAYAN EO": {"ifra_limit": 100.0, "rec_dose": 5.0, "default_conc": 100},
    "Mentha piperita EO": {"ifra_limit": 100.0, "rec_dose": 1.0, "default_conc": 100},
    "Ethyl Vanillin": {"ifra_limit": 100.0, "rec_dose": 8.0, "default_conc": 100},
    "HELIOTROPIN": {"ifra_limit": 100.0, "rec_dose": 0.8, "default_conc": 100},
    "Floralozone (IFF)": {"ifra_limit": 100.0, "rec_dose": 0.8, "default_conc": 100},
    "Patchouli EO": {"ifra_limit": 100.0, "rec_dose": 5.0, "default_conc": 100},
    "Отдушка Йогурт с курагой (Greenwax)": {"ifra_limit": 6.1, "rec_dose": 3.0, "default_conc": 30},
    "Отдушка Кофейня (Candle Science)": {"ifra_limit": 6.6, "rec_dose": 3.3, "default_conc": 30},
    "Отдушка Манго и кокосовое молоко (Candle Science)": {"ifra_limit": 74.99, "rec_dose": 37.0, "default_conc": 100},
    "Отдушка Пряный мед и тонка (Candle Science)": {"ifra_limit": 17.76, "rec_dose": 8.8, "default_conc": 30},
    "Ароматическое масло Молочный шоколад (Jean Claude)": {"ifra_limit": 35.0, "rec_dose": 17.5, "default_conc": 100},
    "Verdox HC (IFF)": {"ifra_limit": 100.0, "rec_dose": 4.0, "default_conc": 100},
    "Maltol (кристалл)": {"ifra_limit": 100.0, "rec_dose": 4.0, "default_conc": 100},
    "Triplal (IFF)": {"ifra_limit": 2.5, "rec_dose": 0.5, "default_conc": 100},
    "Blueberry Pie Oil (CND)": {"ifra_limit": 100.0, "rec_dose": 5.0, "default_conc": 100},
    "Theaspirane (Givaudan)": {"ifra_limit": 100.0, "rec_dose": 0.5, "default_conc": 100},
    "Delta Dodecalactone": {"ifra_limit": 100.0, "rec_dose": 1.5, "default_conc": 100},
    "Peru Balsam Resinoid": {"ifra_limit": 0.41, "rec_dose": 0.02, "default_conc": 100},
    "Кетон малины": {"ifra_limit": 1.01, "rec_dose": 0.02, "default_conc": 100},
    "Cranberry Perfume Oil (CND)": {"ifra_limit": 100.0, "rec_dose": 5.0, "default_conc": 100},
    "Bacdanol® TOCO (IFF)": {"ifra_limit": 100.0, "rec_dose": 5.0, "default_conc": 100}
}

st.set_page_config(page_title="Murlyka Lab v5.5", page_icon="😺", layout="wide")
st.title("😺 Murlyka Lab v5.5")

tab_constructor, tab_grams = st.tabs(["🎨 Конструктор Аромата", "⚖️ Замес в Граммах"])

# ==========================================
# 🎨 ВКЛАДКА 1: КОНСТРУКТОР АРОМАТА (ЧЕРНОВИК) - ИСПРАВЛЕНО v5.5.1
# ==========================================
with tab_constructor:
    st.header("🎨 Конструктор Аромата")
    st.caption("Проектируй структуру → Получай граммы → Проверяй безопасность.")

    if "constructor_rows" not in st.session_state:
        st.session_state.constructor_rows = []

    # ✅ КОНТЕКСТ
    ctx1, ctx2 = st.columns(2)
    with ctx1:
        target_weight_g = st.number_input("Вес концентрата (г)", min_value=0.01, step=0.01, value=1.0, format="%.2f", key="cw")
    with ctx2:
        target_strength = st.select_slider("Целевая крепость (%)", options=[5, 10, 15, 20, 25, 30], value=15, key="ts_c")

    # ➕ ДОБАВЛЕНИЕ СТРОКИ (ИСПРАВЛЕНИЕ ТИПОВ ДАННЫХ!)
    if st.button("➕ Добавить компонент", use_container_width=True, key="add_row"):
        first_comp = list(COMPONENTS.keys())[0]
        st.session_state.constructor_rows.append({
            "comp": first_comp,
            "conc": float(COMPONENTS[first_comp]["default_conc"]),  # 🔧 ЯВНОЕ ПРЕОБРАЗОВАНИЕ В FLOAT!
            "pct_aroma": 0.0
        })
        st.rerun()

    #  СПИСОК КОМПОНЕНТОВ С ВВОДОМ ЦИФР
    total_pct = 0.0
    rows_to_del = []

    for idx, row in enumerate(st.session_state.constructor_rows):
        c1, c2, c3, c4 = st.columns([3, 1, 1, 0.5])
        
        with c1:
            comp_name = st.selectbox(
                "Компонент", 
                list(COMPONENTS.keys()), 
                index=list(COMPONENTS.keys()).index(row["comp"]),
                key=f"comp_{idx}"
            )
        with c2:
            conc_val = st.number_input(
                "Конц.%", 
                min_value=0.01, max_value=100.0, step=0.1, 
                value=float(row["conc"]), format="%.1f", key=f"conc_{idx}"  # 🔧 ТОЖЕ FLOAT!
            )
        with c3:
            pct_val = st.number_input(
                "% в аромате", 
                min_value=0.0, max_value=100.0, step=0.1, 
                value=row["pct_aroma"], format="%.1f", key=f"pct_{idx}"
            )
            total_pct += pct_val
        with c4:
            if st.button("", key=f"del_{idx}", help="Удалить строку"):
                rows_to_del.append(idx)

        # Обновляем состояние при изменении
        st.session_state.constructor_rows[idx] = {
            "comp": comp_name, "conc": conc_val, "pct_aroma": pct_val
        }

    # Удаление строк после рендера
    for idx in sorted(rows_to_del, reverse=True):
        st.session_state.constructor_rows.pop(idx)
    if rows_to_del: st.rerun()

    # 🟢 ИНДИКАТОР СУММЫ
    sum_color = "green" if abs(total_pct - 100.0) < 0.05 else "red"
    sum_text = f"{total_pct:.1f}%"
    sum_status = "✅ Баланс идеален!" if abs(total_pct - 100.0) < 0.05 else f"⚠️ Не хватает / лишние {abs(100.0 - total_pct):.1f}%"
    
    st.markdown(f"<h3 style='color:{sum_color}; text-align:center;'>Сумма % в аромате: {sum_text} — {sum_status}</h3>", unsafe_allow_html=True)

    # ⚙️ РАСЧЁТ ГРАММОВ И IFRA
    is_valid = abs(total_pct - 100.0) < 0.05 and target_weight_g > 0
    
    if is_valid and st.button("🧮 Рассчитать граммы и проверить IFRA", type="primary", use_container_width=True, key="calc_btn"):
        st.divider()
        
        # Математика перевода % в аромате → граммы
        results = []
        
        # Решаем систему уравнений для точного расчёта чистого масла
        # TotalOil * Σ(%_aroma_i / Conc_i) = Weight
        sum_ratio = sum((r["pct_aroma"] / 100.0) / (r["conc"] / 100.0) for r in st.session_state.constructor_rows)
        total_pure_oil_calc = target_weight_g / sum_ratio if sum_ratio > 0 else 0
        
        has_violation = False
        
        for r in st.session_state.constructor_rows:
            pure_oil_g = total_pure_oil_calc * (r["pct_aroma"] / 100.0)
            comp_grams = pure_oil_g / (r["conc"] / 100.0)
            
            # Расчёт спирта и массы готового
            mass_final_g = total_pure_oil_calc / (target_strength / 100.0) if target_strength > 0 else 0
            alcohol_g = round(mass_final_g - target_weight_g, 3) if mass_final_g > target_weight_g else 0
            
            # % актив. в готовом для IFRA
            active_pct_final = round((pure_oil_g / mass_final_g) * 100, 3) if mass_final_g > 0 else 0
            
            comp_data = COMPONENTS.get(r["comp"], {})
            ifra_limit = comp_data.get("ifra_limit", 100.0)
            
            status = "✅"
            if ifra_limit < 100.0 and active_pct_final > ifra_limit:
                status = " ПРЕВЫШЕНИЕ!"
                has_violation = True
                
            results.append({
                "Компонент": r["comp"],
                "% в аромате": f"{r['pct_aroma']:.1f}%",
                "Конц. %": r["conc"],
                "Граммы (для весов)": round(comp_grams, 4),
                "Чистое масло (г)": round(pure_oil_g, 4),
                "% актив. в готовом": active_pct_final,
                "IFRA лимит": ifra_limit,
                "Статус": status
            })

        df_res = pd.DataFrame(results)
        
        def highlight_viol(row):
            if "ПРЕВЫШЕНИЕ" in str(row["Статус"]): return ["background-color: #ffcccc"] * len(row)
            return [""] * len(row)
            
        st.dataframe(df_res.style.apply(highlight_viol, axis=1), use_container_width=True, hide_index=True)
        
        # Финальная сводка
        m1, m2, m3 = st.columns(3)
        with m1: st.metric("⚖️ Масса концентрата", f"{target_weight_g:.3f} г")
        with m2: st.metric("🍶 Нужно спирта", f"{alcohol_g:.3f} г", delta=f"{target_strength}% EdP")
        with m3: st.metric("🧪 Масса готового", f"{mass_final_g:.3f} г")
        
        if has_violation:
            st.error("🙀🙀🙀 ВНИМАНИЕ: Превышение лимитов IFRA! Скорректируй % в аромате.")
        else:
            st.success("✅ Все компоненты в безопасности! Можно переносить на весы.")
            
        # Копирование граммов
        grams_copy = df_res[["Компонент", "Граммы (для весов)"]].to_csv(sep='\t', index=False)
        st.components.v1.html(f"""
            <button onclick="navigator.clipboard.writeText(`{grams_copy}`);this.innerText='✅ Скопировано!';setTimeout(()=>this.innerText='📋 Скопировать граммы для весов',2000);"
            style="width:100%;padding:10px;border:none;border-radius:6px;background:#4CAF50;color:white;font-size:16px;cursor:pointer;margin-top:10px;">
            📋 Скопировать граммы для весов</button>
        """, height=50)

    elif not is_valid and len(st.session_state.constructor_rows) > 0:
        st.warning("️ Для расчёта сумма % в аромате должна быть ровно 100%.")

# ==========================================
# ⚖️ ВКЛАДКА 2: ЗАМЕС В ГРАММАХ (ФАКТ)
# ==========================================
with tab_grams:
    st.header("⚖️ Замес в Граммах")
    st.caption("Фактический протокол. Взвешивай точно. Безопасность проверяется по факту.")

    if "formula_grams" not in st.session_state:
        st.session_state.formula_grams = []
    if "saved_journal" not in st.session_state:
        st.session_state.saved_journal = None

    target_strength_g = st.select_slider("Желаемая крепость парфюма (%)", options=[5, 10, 15, 20, 25, 30], value=15, key="tgt_str_g")

    a1, a2, a3, a4, a5 = st.columns([2, 1, 1, 1, 1])
    with a1: j_comp = st.selectbox("Компонент", list(COMPONENTS.keys()), key="jcomp")
    with a2: j_concentration = st.selectbox("Конц. %", [100,50,30,20,10,5,2,1], index=0, key="jconc")
    with a3: j_grams = st.number_input("Граммы", min_value=0.001, step=0.001, value=0.030, format="%.3f", key="jgr")
    with a4: j_drops_ref = st.number_input("Капли (справ.)", min_value=0, step=1, value=0, key="jdr_ref")
    with a5: add_btn = st.button("➕", use_container_width=True, key="jbtn")

    if add_btn and j_grams > 0:
        st.session_state.formula_grams.append({
            "label": j_comp, "concentration": j_concentration,
            "grams": float(j_grams), "drops_ref": int(j_drops_ref), "comp_name": j_comp
        })
        st.rerun()

    if st.session_state.formula_grams:
        total_ing = sum(i["grams"] for i in st.session_state.formula_grams)
        total_real_oil = sum(i["grams"] * (i["concentration"] / 100.0) for i in st.session_state.formula_grams)
        
        mass_final_g = total_real_oil / (target_strength_g / 100.0) if target_strength_g > 0 else 0
        alcohol_needed_g = round(mass_final_g - total_ing, 3) if mass_final_g > total_ing else 0
        
        m1, m2, m3 = st.columns(3)
        with m1: st.metric("Масса концентрата", f"{total_ing:.3f} г", delta="авто-сумма")
        with m2: st.metric(" Нужно спирта", f"{alcohol_needed_g:.3f} г", delta=f"{target_strength_g}% EdP")
        with m3: st.metric("Масса готового", f"{mass_final_g:.3f} г")

        if alcohol_needed_g <= 0 and total_ing > 0:
            current_strength = round((total_real_oil / total_ing) * 100, 1) if total_ing > 0 else 0
            st.warning(f"⚠️ Смесь уже крепче {target_strength_g}%! Текущая концентрация масла: ~{current_strength}%")

        st.divider()

        rows = []
        has_violation = False
        for i in st.session_state.formula_grams:
            pc = round((i["grams"] / total_ing) * 100, 2) if total_ing > 0 else 0
            real_oil = i["grams"] * (i["concentration"] / 100.0)
            active_pct_in_final = round((real_oil / mass_final_g) * 100, 3) if mass_final_g > 0 else 0

            comp_data = COMPONENTS.get(i["comp_name"], {})
            ifra_limit = comp_data.get("ifra_limit", 100.0)

            status = "✅"
            if ifra_limit < 100.0 and active_pct_in_final > ifra_limit:
                status = "🙀🙀 ПРЕВЫШЕНИЕ!"
                has_violation = True

            rows.append({
                "Компонент": i["label"], "Конц. %": i["concentration"],
                "Капли (справ.)": i["drops_ref"] if i["drops_ref"] > 0 else "—",
                "Граммы": i["grams"], "Масло (г)": round(real_oil, 3),
                "% конц.": pc, "% актив. готов.": active_pct_in_final,
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
            if "ПРЕВЫШЕНИЕ" in str(row["IFRA"]): return ["background-color: #ffcccc"] * len(row)
            return [""] * len(row)

        st.dataframe(df.style.apply(highlight_violation, axis=1), use_container_width=True, hide_index=True)

        real_oil_pct_conc = round((total_real_oil / total_ing) * 100, 1) if total_ing > 0 else 0
        real_oil_pct_final = round((total_real_oil / mass_final_g) * 100, 1) if mass_final_g > 0 else 0

        s1, s2, s3 = st.columns(3)
        with s1: st.metric("Реальное масло", f"{total_real_oil:.3f} г", f"{real_oil_pct_conc}% в концентрате")
        with s2: st.metric("Итоговая концентрация", f"{real_oil_pct_final}%", f"при {target_strength_g}% крепости")
        with s3: st.metric("Компонентов", f"{len(st.session_state.formula_grams)} шт.")

        if has_violation: st.error("🙀🙀 ВНИМАНИЕ: Превышение лимитов IFRA!")

        st.subheader("️ Управление")
        del_cols = st.columns(min(len(st.session_state.formula_grams), 6))
        for idx, item in enumerate(st.session_state.formula_grams):
            col_idx = idx % 6
            with del_cols[col_idx]:
                short_label = item['label'][:12] + ".." if len(item['label']) > 12 else item['label']
                if st.button(f"❌ {short_label}", key=f"del_g_{idx}", use_container_width=True):
                    st.session_state.formula_grams.pop(idx)
                    st.rerun()

        st.divider()
        tname = st.text_input("Название теста", placeholder="Кофе с пирогом v1.0", key="tn")
        if st.button("💾 Сохранить", type="primary", use_container_width=True, key="sbtn", disabled=has_violation):
            if tname.strip():
                jr = []
                for i in st.session_state.formula_grams:
                    pc = round((i["grams"] / total_ing) * 100, 2) if total_ing > 0 else 0
                    pf = round((i["grams"] / mass_final_g) * 100, 3) if mass_final_g > 0 else 0
                    real_oil = round(i["grams"] * (i["concentration"] / 100.0), 3)
                    jr.append({
                        "Название": tname, "Дата": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Компонент": i["label"], "Конц. %": i["concentration"],
                        "Капли (справ.)": i["drops_ref"] if i["drops_ref"] > 0 else "—",
                        "Граммы": i["grams"], "Масло (г)": real_oil,
                        "% конц.": pc, "% готов.": pf,
                        "Крепость": f"{target_strength_g}%", "Спирт (г)": alcohol_needed_g
                    })
                st.session_state.saved_journal = pd.DataFrame(jr)
                st.success(f"✅ '{tname}' сохранён!")
            else: st.warning("⚠️ Введите название!")

        if st.session_state.saved_journal is not None:
            st.divider()
            st.subheader(" Последний сохранённый тест")
            st.dataframe(st.session_state.saved_journal, use_container_width=True, hide_index=True)
            if st.button("🆕 Новый тест (очистить формулу)", use_container_width=True, key="new_test"):
                st.session_state.formula_grams = []
                st.session_state.saved_journal = None
                st.rerun()
    else:
        st.info("👆 Добавьте ингредиенты выше")
