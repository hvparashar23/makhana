import streamlit as st
from datetime import datetime
import pandas as pd 
import os 

# Page configuration
st.set_page_config(page_title="Makahan Store", layout="centered")

st.title("🛒 Welcome to Makahan Store")
st.subheader("Buy Quality Products Online")

# --- Customer Details ---
st.header("👤 Customer Details")
name = st.text_input("Full Name")
phone = st.text_input("Phone Number")
email = st.text_input("Email Address")
address = st.text_area("Shipping Address")

# --- Product Selection ---
st.header("📦 Choose Your Makahan")

product_options = {
    "Makahan Nawabi": "Makhana.jpg",
    "Makahan Shahi": "Makhana.jpg",
    "Makahan Sultaana": "Makhana.jpg",
    "Makahan Azaadi": "Makhana.jpg"
}

selected_product = st.selectbox("Select a product to view and order", list(product_options.keys()))

# Show image of selected product
st.image(product_options[selected_product], caption=selected_product, use_column_width=True)

# --- Rating ---
st.header("🌟 Rate this product")
rating = st.slider("How would you rate this product?", 1, 5, 4)

# --- Referral ---
st.header("📨 Refer to a Friend")
ref_name = st.text_input("Friend's Name")
ref_contact = st.text_input("Friend's Contact Number")

# --- Submit Order ---
if st.button("🛍️ Place Order"):
    if name and phone and address:
        # Collect order details
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

        # Load existing CSV or create a new one
        if os.path.exists("orders.csv"):
            df_orders = pd.read_csv("orders.csv")
        else:
            df_orders = pd.DataFrame(columns=order_data.keys())

        # Append new order and save
        df_orders = pd.concat([df_orders, pd.DataFrame([order_data])], ignore_index=True)
        df_orders.to_csv("orders.csv", index=False)

        st.success("✅ Order placed successfully and saved!")
        st.info(f"Thank you, {name}! We'll deliver your {selected_product} soon.")
    else:
        st.error("⚠️ Please fill in your name, phone, and address to place an order.")

st.markdown("---")
st.caption(f"© {datetime.now().year} Makahan Store. All rights reserved.")

# -----------------------------
# 🔐 Admin Dashboard (Protected)
# -----------------------------
st.markdown("---")
st.header("🔐 Admin Dashboard")

admin_username = st.text_input("Admin Username")
admin_password = st.text_input("Admin Password", type="password")

if st.button("Login"):
    if admin_username == "admin" and admin_password == "makahan123":  # You can change this
        st.success("Login successful!")

        # Display order data
        if os.path.exists("orders.csv"):
            df_orders = pd.read_csv("orders.csv")
            st.subheader("📋 All Orders")
            st.dataframe(df_orders)

            st.markdown(f"**🛒 Total Orders:** {len(df_orders)}")

            # Optional: Show product-wise count
            st.markdown("### 🧾 Product-wise Sales Count")
            st.bar_chart(df_orders["Product"].value_counts())

        else:
            st.warning("No orders placed yet.")
    else:
        st.error("Invalid credentials. Please try again.")
