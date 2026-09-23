from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

# Страница созламалари
st.set_page_config(
    page_title="Degrox - Буюртма бериш тизими", page_icon="📦", layout="centered"
)

# Google Sheets уланиши
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

# st.secrets орқали Google credentials маълумотларини оламиз
try:
  creds_dict = dict(st.secrets["gcp_service_account"])
  creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
  client = gspread.authorize(creds)
  # Жадвал номи ёки URL манзили
  sheet = client.open("degrox_orders").sheet1  # Жадвал номини текшириб қўйинг
except Exception as e:
  st.error(f"Google Жадвалга уланишда хатолик: {e}")

# Сарлавҳа
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

# 1. Дўкон ва Агент маълумотлари
st.markdown("### 1. Дўкон ва Агент маълумотлари")
col1, col2 = st.columns(2)

with col1:
  agent_ismi = st.text_input("Агентнинг исми (Ф.И.О.)", value="Умид")
  dokon_nomi = st.text_input("Дўкон номи", value="Жаҳонгир")

with col2:
  dokon_manzili = st.text_input("Дўкон манзили (Мўлжал)", value="Соғдияна")
  dokon_tel = st.text_input("Дўкон телефон рақами", value="+998997779787")

# Тўлов шартлари
col_t1, col_t2 = st.columns(2)
with col_t1:
  tulov_turi = st.selectbox("Тўлов тури", ["Қарз", "Нақд", "Пластик"])
with col_t2:
  muddati = st.number_input(
      "Тўлов муддати (кун)", min_value=0, max_value=90, value=7
  )

st.markdown("---")

# 2. Маҳсулотлар рўйхати ва нархлари
st.markdown("### 2. Маҳсулотлар ва миқдорларни танланг")
st.write("Қуйидаги маҳсулотларнинг миқдорини киритинг:")

# Маҳсулотлар луғати (Номи: Нархи)
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

# Жами суммани кўрсатиш
st.info(f"### Жами буюртма суммаси: {jami_summa:,} сўм".replace(",", " "))

# 3. Буюртмани тасдиқлаш ва юбориш
if st.button(
    "🚀 Буюртмани тасдиқлаш ва юбориш", type="primary", use_container_width=True
):
  if jami_summa == 0:
    st.warning("Илтимос, камида битта маҳсулот миқдорини киритинг!")
  else:
    try:
      vaqt = datetime.now().strftime("%Y-%m-%d %H:%M")
      agent = agent_ismi
      dokon_full = f"{dokon_manzili} / {dokon_nomi}"

      # Танланган барча маҳсулотларни Google Жадвалга алоҳида сатрлар қилиб ёзиш
      sanoq = 0
      for nomi, miqdor in miqdorlar.items():
        if miqdor > 0:
          # Жадвалдаги устунлар тартиби: Vaqt, Agent, Mahsulot, Miqdor, Tulov, Muddati, Dokon
          sheet.append_row(
              [vaqt, agent, nomi, miqdor, tulov_turi, int(muddati), dokon_full]
          )
          sanoq += 1

      st.success(
          f"🎉 Барча тасдиқланган маҳсулотлар ({sanoq} турдаги) Google Жадвалга"
          " муваффақиятли ёзилди!"
      )

      # Буюртма чекини чиқариш
      st.markdown("### Буюртма чеки:")
      st.markdown(
          f"""
            <div style='background-color: #f0f2f6; padding: 15px; border-radius: 10px;'>
                <p><b>Дўкон:</b> {dokon_nomi}</p>
                <p><b>Манзил:</b> {dokon_manzili}</p>
                <p><b>Агент:</b> {agent_ismi}</p>
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
