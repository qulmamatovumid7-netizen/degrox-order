from datetime import datetime
import os
import pandas as pd
import streamlit as st

# Страница созламалари
st.set_page_config(
    page_title="Degrox - Буюртма бериш тизими", page_icon="📦", layout="centered"
)

# CSV файл номи
CSV_FILE = "orders.csv"

# Вкладкаларни яратиш (Иккита ойна)
tab1, tab2 = st.tabs(["📦 Буюртма бериш", "📋 Буюртмалар тарихи"])

with tab1:
  st.markdown(
      """
        <div style='text-align: center;'>
            <h1>📦 Degrox - Буюртма бериш тизими</h1>
            <p style='color: gray;'>Дўкон маълумотларини киритинг ва керакли маҳсулотлар миқдорини танлаб буюртма беринг!</p>
        </div>
    """,
      unsafe_allow_html=True,
  )

  st.markdown("---")
  st.markdown("### 1. Дўкон ва Агент маълумотлари")
  col1, col2 = st.columns(2)

  with col1:
    agent_ismi = st.text_input("Агентнинг исми (Ф.И.О.)", value="Умид")
    dokon_nomi = st.text_input("Дўкон номи", value="Жаҳонгир")

  with col2:
    dokon_manzili = st.text_input("Дўкон манзили (Мўлжал)", value="Соғдияна")
    dokon_tel = st.text_input("Дўкон телефон рақами", value="+998997779787")

  col_t1, col_t2 = st.columns(2)
  with col_t1:
    tulov_turi = st.selectbox("Тўлов тури", ["Қарз", "Нақд", "Пластик"])
  with col_t2:
    muddati = st.number_input(
        "Тўлов муддати (кун)", min_value=0, max_value=90, value=7
    )

  st.markdown("---")
  st.markdown("### 2. Маҳсулотлар ва миқдорларни танланг")

  mahsulotlar_narxlari = {
      "Гель для посуды 450 мл": 5200,
      "Казан Degrox 500 мл": 11500,
      "Анти-жир Degrox 500 мл": 11500,
      "Жиро удалитель Degrox 500 мл": 11500,
      "Анти-жир Verixo 500 мл": 18000,
      "Универсальный очиститель 500 мл": 15000,
      "Стекло очиститель (Арзон) 500 мл": 5300,
      "Стекло очиститель (Киммат) 500 мл": 8600,
  }

  miqdorlar = {}
  jami_summa = 0

  for nomi, narxi in mahsulotlar_narxlari.items():
    c1, c2 = st.columns([3, 1])
    with c1:
      st.markdown(f"**{nomi}**")
      st.caption(f"Нархи: {narxi:,} сўм".replace(",", " "))
    with c2:
      miqdor = st.number_input(
          "Миқдор",
          min_value=0,
          max_value=1000,
          value=0,
          key=nomi,
          label_visibility="collapsed",
      )
      miqdorlar[nomi] = miqdor

    jami_summa += miqdor * narxi
    st.markdown("---")

  st.info(f"### Жами буюртма суммаси: {jami_summa:,} сўм".replace(",", " "))

  if st.button(
      "🚀 Буюртмани тасдиқлаш ва юбориш",
      type="primary",
      use_container_width=True,
  ):
    if jami_summa == 0:
      st.warning("Илтимос, камида битта маҳсулот миқдорини киритинг!")
    else:
      try:
        vaqt = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Буюртма қилинган маҳсулотларни матн кўринишида йиғамиз
        tanlangan_mahsulotlar_list = []
        for nomi, miqdor in miqdorlar.items():
          if miqdor > 0:
            tanlangan_mahsulotlar_list.append(f"{nomi}: {miqdor} та")

        mahsulotlar_matni = "; ".join(tanlangan_mahsulotlar_list)

        yangi_buyurtma = {
            "Vaqt": vaqt,
            "Agent": agent_ismi,
            "Dokon": dokon_nomi,
            "Manzil": dokon_manzili,
            "Telefon": dokon_tel,
            "Buyurtma_tarkibi": mahsulotlar_matni,
            "Jami_Summa": jami_summa,
            "Tulov_turi": f"{tulov_turi} ({muddati} кун)",
            "Status": "⏳ Кутилмоқда",
        }

        df_yangi = pd.DataFrame([yangi_buyurtma])

        # Агар эски форматдаги файл мавжуд бўлса, уни янги форматга ўтказиш ёки янгидан бошлаш учун ўчирамиз
        if os.path.exists(CSV_FILE):
          df_eski = pd.read_csv(CSV_FILE)
          # Агар эски файлда янги устунлар бўлмаса, файлни тозалаб юборамиз (структура бузилмаслиги учун)
          if "Buyurtma_tarkibi" not in df_eski.columns:
            df_final = df_yangi
          else:
            df_final = pd.concat([df_eski, df_yangi], ignore_index=True)
        else:
          df_final = df_yangi

        df_final.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")

        st.success(
            "🎉 Дўконнинг умумий буюртмаси тизимга муваффақиятли сақланди!"
        )

        st.markdown("### Буюртма чеки:")
        st.markdown(
            f"""
                <div style='background-color: #f0f2f6; padding: 15px; border-radius: 10px;'>
                    <p><b>Дўкон:</b> {dokon_nomi}</p>
                    <p><b>Манзил:</b> {dokon_manzili}</p>
                    <p><b>Агент:</b> {agent_ismi}</p>
                    <p><b>Телефон:</b> {dokon_tel}</p>
                    <p><b>Тўлов тури:</b> {tulov_turi} ({muddati} кун)</p>
                </div>
                """,
            unsafe_allow_html=True,
        )

        for nomi, miqdor in miqdorlar.items():
          if miqdor > 0:
            narxi = mahsulotlar_narxlari[nomi]
            st.write(
                f"- {nomi} x {miqdor} та = {miqdor * narxi:,} сўм".replace(
                    ",", " "
                )
            )

        st.markdown(f"### Жами: {jami_summa:,} сўм".replace(",", " "))

      except Exception as e:
        st.error(f"Маълумотларни сақлашда хатолик юз берди: {e}")

with tab2:
  st.markdown("### 📋 Дўконларнинг умумий буюртмалар тарихи")

  if os.path.exists(CSV_FILE):
    df_orders = pd.read_csv(CSV_FILE)

    # Агар эски форматдаги файл бўлса, фойдаланувчуга уни тозалашни маслаҳат берамиз
    if "Buyurtma_tarkibi" not in df_orders.columns:
      st.warning(
          "⚠️ Эски форматдаги буюртмалар аниқланди. Янги умумий буюртмалар"
          " тизимига ўтиш учун илтимос, пастдаги тугма орқали тарихни"
          " тозалаб юборинг!"
      )
      if st.button("🗑️ Эски тарихни тозалаш", type="primary"):
        os.remove(CSV_FILE)
        st.success("Тарих тозаланди! Энди янги буюртма беришингиз мумкин.")
        st.rerun()
    else:
      if not df_orders.empty:
        st.write(
            "Ҳар бир дўкон буюртмаси битта сатрда кўрсатилган. Статусни"
            " ўзгартириб сақлашингиз мумкин:"
        )

        # Интерактив жадвал
        edited_df = st.data_editor(
            df_orders,
            column_config={
                "Status": st.column_config.SelectboxColumn(
                    "Статус",
                    help="Буюртма ҳолатини танланг",
                    options=[
                        "⏳ Кутилмоқда",
                        "🚚 Йўлда",
                        "✅ Етказиб берилди",
                        "❌ Бекор қилинди",
                    ],
                    required=True,
                ),
                "Jami_Summa": st.column_config.NumberColumn(
                    "Жами сумма (сўм)", format="%d сўм"
                ),
            },
            use_container_width=True,
            num_rows="fixed",
            key="store_orders_editor",
        )

        # Ўзгаришларни сақлаш тугмаси
        if st.button("💾 Статусларни сақлаш", type="primary"):
          edited_df.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")
          st.success("Буюртмалар статуслари муваффақиятли сақланди!")
          st.rerun()

        st.markdown("---")

        col_btn1, col_btn2 = st.columns(2)

        with col_btn1:
          csv_data = edited_df.to_csv(index=False, encoding="utf-8-sig").encode(
              "utf-8-sig"
          )
          st.download_button(
              label="📥 Жадвални Excel форматида юклаб олиш",
              data=csv_data,
              file_name="degrox_store_orders.csv",
              mime="text/csv",
              use_container_width=True,
          )

        with col_btn2:
          if st.button(
              "🗑️ Буюртмалар тарихини тозалаш",
              type="secondary",
              use_container_width=True,
          ):
            os.remove(CSV_FILE)
            st.success("Буюртмалар тарихи муваффақиятли тозаланди!")
            st.rerun()
      else:
        st.info("Ҳозирча буюртмалар мавжуд эмас.")
  else:
    st.info(
        "Ҳозирча буюртмалар мавжуд эмас. Биринчи буюртмани бериб кўринг!"
    )
