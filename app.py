import datetime
import requests
import streamlit as st

# Страница созламалари
st.set_page_config(
    page_title="Degrox - Буюртма тизими", page_icon="📦", layout="centered"
)

# Логотипни чиқариш
try:
    st.image("Лого/Degrox.png", width=200)
except:
    pass

st.title("📦 Degrox - Буюртма бериш тизими")
st.write(
    "Дўкон маълумотларини бир марта киритинг ва керакли маҳсулотлар миқдорини танлаб буюртма беринг!"
)

# Google Apps Script Web App URL
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzEJ7N03E3QBevX2iNfoN7CeNa-lQ1fSwqxtoQbLD-1dFZ0g4bEvwtlhWsJP5H5QbEvTg/exec"

# Маҳсулотлар каталоги ва нархлари (сўмда)
PRODUCTS_CATALOG = {
    "Гел для посуды 450 мл": 5200,
    "Казан Degrox 500 мл": 11500,
    "Анти-жир Degrox 500 мл": 11500,
    "Жиро удалитель Degrox 500 мл": 11500,
    "Анти-жир Verixo 500 мл": 18000,
    "Унверсальный очиститель 500 мл": 15000,
    "Стекло очиститель (Арзон) 500 мл": 5300,
    "Стекло очиститель (Киммат) 500 мл": 8600,
}

# --- 1-ҚАДАМ: Умумий маълумотлар (Дўкон ва Агент) ---
st.subheader("1. Дўкон ва Агент маълумотлари")

col1, col2 = st.columns(2)
with col1:
    agent_name = st.text_input("Агентнинг исми (Ф.И.О.)")
    shop_name = st.text_input("Дўкон номи")

with col2:
    shop_address = st.text_input("Дўкон манзили (Мўлжал)")
    shop_phone = st.text_input("Дўкон телефон рақами", value="+998")

st.divider()

# --- 2-ҚАДАМ: Маҳсулотларни танлаш ва миқдорини киритиш ---
st.subheader("2. Маҳсулотлар ва миқдорларни танланг")
st.write("Қуйидаги маҳсулотларнинг миқдорини киритинг:")

order_items = []
total_sum = 0

for product_name, price in PRODUCTS_CATALOG.items():
    col_p1, col_p2 = st.columns([3, 1])
    with col_p1:
        st.write(f"**{product_name}**\n\n*Нархи:* {price:,.0f} сўм")
    with col_p2:
        qty = st.number_input(
            "Сони",
            min_value=0,
            max_value=1000,
            value=0,
            step=1,
            key=f"prod_{product_name}",
            label_visibility="collapsed",
        )

    if qty > 0:
        item_total = qty * price
        total_sum += item_total
        order_items.append(
            {
                "name": product_name,
                "price": price,
                "qty": qty,
                "total": item_total,
            }
        )
    st.divider()

# Умумий суммани кўрсатиш
if total_sum > 0:
    st.info(f"🧮 **Жами буюртма суммаси:** {total_sum:,.0f} сўм")

# --- 3-ҚАДАМ: Буюртмани юбориш ---
if st.button("🚀 Буюртмани тасдиқлаш ва юбориш", type="primary", use_container_width=True):
    if not agent_name.strip():
        st.error("Илтимос, агент исмини киритинг!")
    elif not shop_name.strip():
        st.error("Илтимос, дўкон номини киритинг!")
    elif len(order_items) == 0:
        st.warning("Илтимос, камида битта маҳсулот миқдорини кўрсатинг!")
    else:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with st.spinner("Буюртма юборилмоқда..."):
            success_count = 0
            fail_count = 0

            for item in order_items:
                payload = {
                    "date": current_time,
                    "agent": agent_name,
                    "shop_name": shop_name,
                    "shop_address": shop_address,
                    "shop_phone": shop_phone,
                    "category": "Маҳсулотлар",
                    "product_name": f"{item['name']} ({item['price']} сўм)",
                    "quantity": item["qty"],
                    "total_price": item["total"],
                }

                try:
                    response = requests.post(
                        GOOGLE_SCRIPT_URL, json=payload, timeout=10
                    )
                    if response.status_code == 200:
                        success_count += 1
                    else:
                        fail_count += 1
                except:
                    fail_count += 1

            if success_count > 0 and fail_count == 0:
                st.success(
                    f"🎉 Барча маҳсулотлар муваффақиятли буюртма қилинди ва Google Жадвалга ёзилди!"
                )
                st.balloons()

                st.write("### Буюртма чеки:")
                st.info(
                    f"**Дўкон:** {shop_name}\n\n**Манзил:** {shop_address}\n\n**Агент:** {agent_name}"
                )
                for item in order_items:
                    st.write(
                        f"- {item['name']} x {item['qty']} та = **{item['total']:,.0f} сўм**"
                    )
                st.write(f"### Жами: {total_sum:,.0f} сўм")
            else:
                st.warning(
                    "⚠️ Буюртма юборилди, лекин Google Script URL манзилини ёки интернетни текширинг!"
                )
