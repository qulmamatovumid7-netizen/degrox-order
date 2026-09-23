from datetime import datetime
import json
import os
import pandas as pd
import streamlit as st

# Страница созламалари
st.set_page_config(
    page_title="Degrox & Virexo - Буюртма бериш тизими",
    page_icon="Virexo.png",
    layout="centered",
)

# Сессияни текшириш (саҳифа янilanganda ҳам йўқолмаслиги учун)
if "authenticated" not in st.session_state:
  # Агар URL'да логиндан ўтгани ҳақида белги бўлса, уни сақлаб қоламиз
  if (
      "logged_in" in st.query_params
      and st.query_params["logged_in"] == "true"
  ):
    st.session_state["authenticated"] = True
  else:
    st.session_state["authenticated"] = False

# Агар тизимга кирмаган бўлса, Логин ойнасини кўрсатиш
if not st.session_state["authenticated"]:
  st.markdown(
      "<h2 style='text-align: center;'>🔐 Тизимга кириш</h2>",
      unsafe_allow_html=True,
  )

  col1, col2, col3 = st.columns([1, 2, 1])
  with col2:
    with st.form("login_form"):
      username = st.text_input("Логин")
      password = st.text_input("Пароль", type="password")
      submit_button = st.form_submit_button(
          "Кириш", use_container_width=True, type="primary"
      )

      if submit_button:
        if username == "Virexo+" and password == "220926":
          st.session_state["authenticated"] = True
          # URL'га белги қўшиб қўямиз, шунда саҳифа янilanganda ҳам сессия ўчиб кетмайди
          st.query_params["logged_in"] = "true"
          st.success("Хуш келибсиз!")
          st.rerun()
        else:
          st.error("Логин ёки пароль нотўғри!")
  st.stop()  # Логин тўғри киритилмагунча қолган кодни тўхтатиб туради

# ==========================================
# АГАР ТИЗИМГА МУВАФФАҚИЯТЛИ КИРИЛГАН БЎЛСА:
# ==========================================

# Чиқиш (Logout) тугмаси
if st.sidebar.button("🚪 Тизимдан чиқиш"):
  st.session_state["authenticated"] = False
  # URL параметрини ҳам тозалаб юборамиз
  if "logged_in" in st.query_params:
    del st.query_params["logged_in"]
  st.rerun()

# JSON файл номи
DATA_FILE = "orders.json"


# Маълумотларни ўқиш функцияси
def load_data():
  if os.path.exists(DATA_FILE):
    try:
      with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    except:
      return []
  return []


# Маълумотларни сақлаш функцияси
def save_data(data):
  with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


# Логотипларни саҳифа юқорисида ёнма-ён чиқариш
l_col1, l_col2 = st.columns(2)
with l_col1:
  if os.path.exists("Degrox.png"):
    st.image("Degrox.png", width=180)
with l_col2:
  if os.path.exists("Virexo.png"):
    st.image("Virexo.png", width=180)

st.markdown("---")

# Вкладкаларни яратиш (Иккита ойна)
tab1, tab2 = st.tabs(["📦 Буюртма бериш", "📋 Буюртмалар тарихи"])

with tab1:
  st.markdown(
      """
        <div style='text-align: center;'>
            <h1>📦 Degrox & Virexo - Буюртма бериш тизими</h1>
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

        tarkib = []
        for nomi, miqdor in miqdorlar.items():
          if miqdor > 0:
            narxi = mahsulotlar_narxlari[nomi]
            tarkib.append(
                {"mahsulot": nomi, "miqdor": miqdor, "narx": narxi * miqdor}
            )

        yangi_buyurtma = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S"),
            "vaqt": vaqt,
            "agent": agent_ismi,
            "dokon": dokon_nomi,
            "manzil": dokon_manzili,
            "telefon": dokon_tel,
            "tulov": f"{tulov_turi} ({muddati} кун)",
            "tarkib": tarkib,
            "jami": jami_summa,
            "status": "⏳ Кутилмоқда",
        }

        all_orders = load_data()
        all_orders.insert(0, yangi_buyurtma)
        save_data(all_orders)

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

        for item in tarkib:
          st.write(
              f"- {item['mahsulot']} x {item['miqdor']} та ="
              f" {item['narx']:,} сўм".replace(",", " ")
          )

        st.markdown(f"### Жами: {jami_summa:,} сўм".replace(",", " "))

      except Exception as e:
        st.error(f"Маълумотларни сақлашда хатолик юз берди: {e}")

with tab2:
  st.markdown("### 📋 Дўконларнинг буюртмалар тарихи")

  orders = load_data()

  if orders:
    df_export = []
    for o in orders:
      tarkib_str = "; ".join(
          [f"{i['mahsulot']}: {i['miqdor']} та" for i in o["tarkib"]]
      )
      df_export.append({
          "Vaqt": o["vaqt"],
          "Agent": o["agent"],
          "Dokon": o["dokon"],
          "Manzil": o["manzil"],
          "Telefon": o["telefon"],
          "Tarkibi": tarkib_str,
          "Jami Сумма": o["jami"],
          "Tolov": o["tulov"],
          "Status": o["status"],
      })

    df_dl = pd.DataFrame(df_export)
    csv_data = df_dl.to_csv(index=False, encoding="utf-8-sig").encode(
        "utf-8-sig"
    )

    col_d1, col_d2 = st.columns(2)
    with col_d1:
      st.download_button(
          label="📥 Жадвални Excel форматида юклаб олиш",
          data=csv_data,
          file_name="degrox_store_orders.csv",
          mime="text/csv",
          use_container_width=True,
      )
    with col_d2:
      if st.button(
          "🗑️ Барча тарихни тозалаш",
          type="secondary",
          use_container_width=True,
      ):
        if os.path.exists(DATA_FILE):
          os.remove(DATA_FILE)
        st.success("Буюртмалар тарихи тозаланди!")
        st.rerun()

    st.markdown("---")

    for index, order in enumerate(orders):
      with st.container(border=True):
        col_c1, col_c2 = st.columns([3, 1])

        with col_c1:
          st.markdown(
              f"### 🏪 {order['dokon']} &nbsp;&nbsp; <span"
              f" style='font-size:14px; color:gray;'>({order['vaqt']})</span>",
              unsafe_allow_html=True,
          )
          st.write(
              f"📍 **Манзил:** {order['manzil']} &nbsp;&nbsp;|&nbsp;&nbsp; 📞"
              f" **Тел:** {order['telefon']} &nbsp;&nbsp;|&nbsp;&nbsp; 👤"
              f" **Агент:** {order['agent']}"
          )
          st.write(f"💳 **Тўлов:** {order['tulov']}")

        with col_c2:
          status_options = [
              "⏳ Кутилмоқда",
              "🚚 Йўлда",
              "✅ Етказиб берилди",
              "❌ Бекор қилинди",
          ]
          current_status = (
              order["status"]
              if order["status"] in status_options
              else "⏳ Кутилмоқда"
          )

          yangi_status = st.selectbox(
              "Статус",
              options=status_options,
              index=status_options.index(current_status),
              key=f"status_{order['id']}",
          )

          if yangi_status != order["status"]:
            orders[index]["status"] = yangi_status
            save_data(orders)
            st.rerun()

        st.markdown("**Харид қилинган маҳсулотлар:**")
        for item in order["tarkib"]:
          st.markdown(
              f"- {item['mahsulot']} — **{item['miqdor']} та** ({item['narx']:,}"
              f" сўм)".replace(",", " ")
          )

        st.markdown(
            f"**Жами сумма:** <span"
            f" style='color:green; font-size:18px;'><b>{order['jami']:,} сўм</b></span>"
            .replace(",", " "),
            unsafe_allow_html=True,
        )
  else:
    st.info(
        "Ҳозирча буюртмалар мавжуд эмас. Биринчи буюртмани бериб кўринг!"
    )
