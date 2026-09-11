import streamlit as st
from datetime import datetime
import pandas as pd

# ==========================================
# 🐱 БАЗА КОМПОНЕНТОВ
# ==========================================
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

# ⚖️ ФИЗИЧЕСКИЕ КОНСТАНТЫ ДЛЯ ПЕРЕВОДА КАПЕЛЬ В ГРАММЫ
DROP_WEIGHT_G = 0.03      # Средний вес капли парфюмерной смеси (г)
CONCENTRATE_DENSITY = 0.95 # Относительная плотность концентрата

st.set_page_config(page_title="Murlyka Lab", page_icon="😺", layout="wide")
st.title("😺 Murlyka Lab")

# ==========================================
# 👇 ЖУРНАЛ: ДВА РЕЖИМА
# ==========================================
tab_drops, tab_grams = st.tabs(["💧 Капли (Черновик)", "⚖️ Граммы (Замес)"])

# === 💧 ВКЛАДКА 1: КАПЛИ (ЧЕРНОВИК С ФИЗИКОЙ) ===
with tab_drops:
    st.header("📝 Черновик в каплях")
    st.caption("Задай масштаб и крепость. Безопасность считается в граммах «под капотом».")

    if "formula_drops" not in st.session_state:
        st.session_state.formula_drops = []

    # ✅ КОНТЕКСТ: Масштаб + Цель
    ctx1, ctx2 = st.columns(2)
    with ctx1:
        total_conc_drops = st.number_input(
            "Капли концентрата (всего)",
            min_value=1, value=30, step=1, key="tcd"
        )
    with ctx2:
        target_strength = st.select_slider(
            "Желаемая крепость парфюма (%)",
            options=[5, 10, 15, 20, 25, 30], value=15, key="tgt_str"
        )

    # ⚖️ РАСЧЁТ МАССЫ «ПОД КАПОТОМ»
    mass_concentrate_g = total_conc_drops * DROP_WEIGHT_G * CONCENTRATE_DENSITY
    mass_final_product_g = mass_concentrate_g / (target_strength / 100.0) if target_strength > 0 else 0

    info1, info2, info3 = st.columns(3)
    with info1: st.metric("≈ Масса концентрата", f"{mass_concentrate_g:.3f} г")
    with info2: st.metric("≈ Масса готового", f"{mass_final_product_g:.3f} г")
    with info3: st.metric("≈ Нужно спирта", f"{mass_final_product_g - mass_concentrate_g:.3f} г")

    st.divider()

    # ➕ ДОБАВЛЕНИЕ ИНГРЕДИЕНТА
    a1, a2, a3, a4 = st.columns([2, 1, 1, 1])
    with a1: d_comp = st.selectbox("Компонент", list(COMPONENTS.keys()), key="d_comp")
    with a2: d_conc = st.selectbox("Конц. %", [100,50,30,20,10,5,2,1], index=0, key="d_conc")
    with a3: d_drops = st.number_input("Капли", min_value=0, step=1, value=1, key="d_drops")
    with a4: d_add = st.button("➕ Добавить", use_container_width=True, key="d_btn")

    if d_add and d_drops > 0:
        st.session_state.formula_drops.append({
            "Компонент": d_comp,
            "Конц. %": d_conc,
            "Капли": d_drops
        })
        st.rerun()

    # 🔄 ДИНАМИЧЕСКИЙ ПЕРЕСЧЁТ ВСЕЙ СМЕСИ
    if st.session_state.formula_drops:
        rows = []
        for item in st.session_state.formula_drops:
            # Перевод капель компонента в граммы чистого вещества
            mass_component_g = item["Капли"] * DROP_WEIGHT_G * CONCENTRATE_DENSITY
            mass_pure_oil_g = mass_component_g * (item["Конц. %"] / 100.0)

            # % актив. в готовом продукте (МАССОВЫЙ!)
            active_pct_mass = round((mass_pure_oil_g / mass_final_product_g) * 100, 3) if mass_final_product_g > 0 else 0

            comp_data = COMPONENTS.get(item["Компонент"], {})
            ifra_limit = comp_data.get("ifra_limit", 100.0)

            status = "✅"
            if ifra_limit < 100.0 and active_pct_mass > ifra_limit:
                status = "🙀🙀🙀"

            rows.append({
                "Компонент": item["Компонент"],
                "Конц. %": item["Конц. %"],
                "Капли": item["Капли"],
                "% актив. (масс.)": active_pct_mass,
                "IFRA лимит": ifra_limit,
                "Статус": status
            })

        df_drops = pd.DataFrame(rows)

        def highlight_violation_drops(row):
            if "🙀" in str(row["Статус"]):
                return ["background-color: #ffcccc"] * len(row)
            return [""] * len(row)

        st.dataframe(
            df_drops.style.apply(highlight_violation_drops, axis=1),
            use_container_width=True, hide_index=True
        )

        # 📋 КОПИРОВАНИЕ
        copy_drops = df_drops.to_csv(sep='\t', index=False)
        st.components.v1.html(f"""
            <button onclick="navigator.clipboard.writeText(`{copy_drops}`);this.innerText='✅ Скопировано!';setTimeout(()=>this.innerText='📋 Скопировать черновик',2000);"
            style="width:100%;padding:8px;border:none;border-radius:6px;background:#4CAF50;color:white;font-size:14px;cursor:pointer;margin-top:10px;">
            📋 Скопировать черновик</button>
        """, height=45)

        # 🗑️ УДАЛЕНИЕ
        del_cols = st.columns(min(len(st.session_state.formula_drops), 6))
        for idx, item in enumerate(st.session_state.formula_drops):
            col_idx = idx % 6
            with del_cols[col_idx]:
                short = item['Компонент'][:10] + ".." if len(item['Компонент']) > 10 else item['Компонент']
                if st.button(f"❌ {short}", key=f"del_d_{idx}", use_container_width=True):
                    st.session_state.formula_drops.pop(idx)
                    st.rerun()

        if st.button("🆕 Очистить черновик", use_container_width=True, key="clear_drops"):
            st.session_state.formula_drops = []
            st.rerun()
    else:
        st.info("👆 Добавь компоненты выше")


# === ⚖️ ВКЛАДКА 2: ГРАММЫ (ЗАМЕС С АВТОМАТИЧЕСКОЙ МАССОЙ) ===
with tab_grams:
    st.header("⚖️ Замес в граммах")
    st.caption("Добавляй ингредиенты → масса считается сама → спирт обновляется мгновенно.")

    if "formula_grams" not in st.session_state:
        st.session_state.formula_grams = []
    if "saved_journal" not in st.session_state:
        st.session_state.saved_journal = None

    # ✅ ЖЕЛАЕМАЯ КРЕПОСТЬ (ЕДИНСТВЕННЫЙ РУЧНОЙ ПАРАМЕТР)
    target_strength_g = st.select_slider(
        "Желаемая крепость парфюма (%)",
        options=[5, 10, 15, 20, 25, 30], value=15, key="tgt_str_g"
    )

    # ➕ ДОБАВЛЕНИЕ ИНГРЕДИЕНТОВ
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

    # 📊 ТАБЛИЦА И РАСЧЁТЫ
    if st.session_state.formula_grams:
        # ✅ МАССА КОНЦЕНТРАТА = СУММА ВСЕХ ИНГРЕДИЕНТОВ (АВТОМАТИЧЕСКИ!)
        total_ing = sum(i["grams"] for i in st.session_state.formula_grams)
        
        # ⚖️ РАСЧЁТ СПИРТА НА ОСНОВЕ ЖИВОЙ МАССЫ
        mass_final_g = total_ing / (target_strength_g / 100.0) if target_strength_g > 0 else 0
        alcohol_needed_g = round(mass_final_g - total_ing, 3) if mass_final_g > total_ing else 0
        
        m1, m2, m3 = st.columns(3)
        with m1: st.metric("Масса концентрата", f"{total_ing:.3f} г", delta="авто-сумма")
        with m2: st.metric("🍶 Нужно спирта", f"{alcohol_needed_g:.3f} г", delta=f"{target_strength_g}% EdP")
        with m3: st.metric("Масса готового", f"{mass_final_g:.3f} г")

        if alcohol_needed_g <= 0 and total_ing > 0:
            current_strength = round((total_ing / mass_final_g) * 100, 1) if mass_final_g > 0 else 0
            st.warning(f"⚠️ Смесь уже крепче {target_strength_g}%! Текущая: ~{current_strength}%")

        st.divider()

        rows = []
        has_violation = False
        total_real_oil = 0

        for i in st.session_state.formula_grams:
            pc = round((i["grams"] / total_ing) * 100, 2) if total_ing > 0 else 0
            real_oil = i["grams"] * (i["concentration"] / 100.0)
            total_real_oil += real_oil
            active_pct_in_final = round((real_oil / mass_final_g) * 100, 3) if mass_final_g > 0 else 0

            comp_data = COMPONENTS.get(i["comp_name"], {})
            ifra_limit = comp_data.get("ifra_limit", 100.0)

            status = "✅"
            if ifra_limit < 100.0 and active_pct_in_final > ifra_limit:
                status = "🙀🙀🙀 ПРЕВЫШЕНИЕ!"
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
        real_oil_pct_final = round((total_real_oil / mass_final_g) * 100, 1) if mass_final_g > 0 else 0

        s1, s2, s3 = st.columns(3)
        with s1: st.metric("Реальное масло", f"{total_real_oil:.3f} г", f"{real_oil_pct_conc}% в концентрате")
        with s2: st.metric("Итоговая концентрация", f"{real_oil_pct_final}%", f"при {target_strength_g}% крепости")
        with s3: st.metric("Компонентов", f"{len(st.session_state.formula_grams)} шт.")

        if has_violation:
            st.error("🙀🙀🙀 ВНИМАНИЕ: Превышение лимитов IFRA!")

        # 🗑️ УПРАВЛЕНИЕ
        st.subheader("🗑️ Управление")
        del_cols = st.columns(min(len(st.session_state.formula_grams), 6))
        for idx, item in enumerate(st.session_state.formula_grams):
            col_idx = idx % 6
            with del_cols[col_idx]:
                short_label = item['label'][:12] + ".." if len(item['label']) > 12 else item['label']
                if st.button(f"❌ {short_label}", key=f"del_g_{idx}", use_container_width=True):
                    st.session_state.formula_grams.pop(idx)
                    st.rerun()

        # 💾 СОХРАНЕНИЕ
        st.divider()
        tname = st.text_input("Название теста", placeholder="Живой Лес v4.0", key="tn")

        if st.button("💾 Сохранить", type="primary", use_container_width=True, key="sbtn", disabled=has_violation):
            if tname.strip():
                jr = []
                for i in st.session_state.formula_grams:
                    pc = round((i["grams"] / total_ing) * 100, 2) if total_ing > 0 else 0
                    pf = round((i["grams"] / mass_final_g) * 100, 3) if mass_final_g > 0 else 0
                    real_oil = round(i["grams"] * (i["concentration"] / 100.0), 3)
                    jr.append({
                        "Название": tname,
                        "Дата": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Компонент": i["label"],
                        "Конц. %": i["concentration"],
                        "Капли (справ.)": i["drops_ref"] if i["drops_ref"] > 0 else "—",
                        "Граммы": i["grams"],
                        "Масло (г)": real_oil,
                        "% конц.": pc,
                        "% готов.": pf,
                        "Крепость": f"{target_strength_g}%",
                        "Спирт (г)": alcohol_needed_g
                    })
                st.session_state.saved_journal = pd.DataFrame(jr)
                st.success(f"✅ '{tname}' сохранён!")
            else:
                st.warning("⚠️ Введите название!")

        if st.session_state.saved_journal is not None:
            st.divider()
            st.subheader("💾 Последний сохранённый тест")
            st.dataframe(st.session_state.saved_journal, use_container_width=True, hide_index=True)
            if st.button("🆕 Новый тест (очистить формулу)", use_container_width=True, key="new_test"):
                st.session_state.formula_grams = []
                st.session_state.saved_journal = None
                st.rerun()
    else:
        st.info("👆 Добавьте ингредиенты выше")
