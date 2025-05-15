import streamlit as st
from datetime import datetime
import pandas as pd
import os

# --- Page Config ---
st.set_page_config(page_title="Makahan Store", layout="centered")

# --- Tabs for User and Admin ---
tab1, tab2 = st.tabs(["🛍️ Customer Order", "🔐 Admin Panel"])

# -----------------------
# 🛍️ Tab 1: Customer Order
# -----------------------
with tab1:
    st.title("🛒 Makahan Store")
    st.subheader("Buy Premium Makahan Online")

    with st.expander("👤 Customer Details", expanded=True):
        name = st.text_input("Full Name")
        phone = st.text_input("Phone Number")
        email = st.text_input("Email Address")
        address = st.text_area("Shipping Address")

    with st.expander("📦 Product Selection", expanded=True):
        product_options = {
            "Makahan Nawabi": "Makhana.jpg",
            "Makahan Shahi": "Makhana.jpg",
            "Makahan Sultaana": "Makhana.jpg",
            "Makahan Azaadi": "Makhana.jpg"
        }
        selected_product = st.selectbox("Choose Your Product", list(product_options.keys()))
        st.image(product_options[selected_product], caption=selected_product, use_column_width=True)

    with st.expander("🌟 Rate This Product"):
        rating = st.slider("How would you rate this product?", 1, 5, 4)

    with st.expander("📨 Refer a Friend"):
        ref_name = st.text_input("Friend's Name")
        ref_contact = st.text_input("Friend's Contact Number")

    if st.button("✅ Place Order"):
        if name and phone and address:
            order_data = {
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Customer Name": name,
                "Phone": phone,
                "Email": email,
                "Address": address,
                "Product": selected_product,
                "Rating": rating,
                "Referred Name": ref_name,
                "Referred Contact": ref_contact
            }

            # Save to CSV
            if os.path.exists("orders.csv"):
                df_orders = pd.read_csv("orders.csv")
            else:
                df_orders = pd.DataFrame(columns=order_data.keys())

            df_orders = pd.concat([df_orders, pd.DataFrame([order_data])], ignore_index=True)
            df_orders.to_csv("orders.csv", index=False)

            st.success("🎉 Order placed successfully!")
            st.info(f"Thank you, {name}! We'll deliver your {selected_product} soon.")
        else:
            st.error("⚠️ Please complete all required fields (Name, Phone, Address).")

# -----------------------
# 🔐 Tab 2: Admin Panel
# -----------------------
with tab2:
    st.title("🔐 Admin Dashboard")
    st.caption("Authorized personnel only")

    admin_username = st.text_input("Admin Username", key="admin_user")
    admin_password = st.text_input("Admin Password", type="password", key="admin_pass")

    if st.button("🔓 Login"):
        if admin_username == "admin" and admin_password == "makahan123":
            st.success("✅ Login successful")

            if os.path.exists("orders.csv"):
                df_orders = pd.read_csv("orders.csv")
                st.subheader("📋 All Orders")
                st.dataframe(df_orders)

                st.markdown(f"**🛒 Total Orders:** `{len(df_orders)}`")

                st.markdown("### 📊 Product-wise Sales Count")
                st.bar_chart(df_orders["Product"].value_counts())
            else:
                st.warning("No orders found yet.")
        else:
            st.error("❌ Invalid credentials. Try again.")

# --- Footer ---
st.markdown("---")
st.caption(f"© {datetime.now().year} Makahan Store. All rights reserved.")
