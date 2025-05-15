import streamlit as st
from datetime import datetime
import pandas as pd 
import os
from fpdf import FPDF
import smtplib
from email.message import EmailMessage

# Page configuration
st.set_page_config(page_title="Makahan Store", layout="centered")

# Ensure inventory.csv exists
inventory_path = "inventory.csv"
if not os.path.exists(inventory_path):
    initial_inventory = pd.DataFrame({
        "Product": ["Makahan Nawabi", "Makahan Shahi", "Makahan Sultaana", "Makahan Azaadi"],
        "Stock": [10, 10, 10, 10]
    })
    initial_inventory.to_csv(inventory_path, index=False)

# Ensure orders.csv exists
orders_path = "orders.csv"
if not os.path.exists(orders_path):
    orders_df = pd.DataFrame(columns=[
        "Date", "Customer Name", "Phone", "Email", "Address", "Product",
        "Quantity", "Rating", "Referred Name", "Referred Contact"
    ])
    orders_df.to_csv(orders_path, index=False)

# Tabs for customer and admin
tab1, tab2 = st.tabs(["🍭️ Customer Order", "🔐 Admin Dashboard"])

# ---------------------------
# Customer Order Tab
# ---------------------------
with tab1:
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
    st.image(product_options[selected_product], caption=selected_product, use_column_width=True)

    # --- Quantity Selection ---
    quantity = st.number_input("Enter quantity to order", min_value=1, step=1, value=1)

    # --- Rating ---
    st.header("🌟 Rate this product")
    rating = st.slider("How would you rate this product?", 1, 5, 4)

    # --- Referral ---
    st.header("📨 Refer to a Friend")
    ref_name = st.text_input("Friend's Name")
    ref_contact = st.text_input("Friend's Contact Number")

    # --- Submit Order ---
    if st.button("🖕 Place Order"):
        if name and phone and address:
            inventory_df = pd.read_csv(inventory_path)
            current_stock = inventory_df.loc[inventory_df['Product'] == selected_product, 'Stock'].values[0]
            
            if quantity <= current_stock:
                order_data = {
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Customer Name": name,
                    "Phone": phone,
                    "Email": email,
                    "Address": address,
                    "Product": selected_product,
                    "Quantity": quantity,
                    "Rating": rating,
                    "Referred Name": ref_name,
                    "Referred Contact": ref_contact
                }
                df_orders = pd.read_csv(orders_path)
                df_orders = pd.concat([df_orders, pd.DataFrame([order_data])], ignore_index=True)
                df_orders.to_csv(orders_path, index=False)

                # Update inventory
                inventory_df.loc[inventory_df['Product'] == selected_product, 'Stock'] -= quantity
                inventory_df.to_csv(inventory_path, index=False)

                st.success(f"✅ Order placed successfully for {quantity} units!")
                st.info(f"Thank you, {name}! We'll deliver your {quantity} units of {selected_product} soon.")

                # Check for low stock and alert
                low_stock_threshold = 2
                new_stock = inventory_df.loc[inventory_df['Product'] == selected_product, 'Stock'].values[0]
                if new_stock <= low_stock_threshold:
                    try:
                        msg = EmailMessage()
                        msg['Subject'] = 'Stock Alert: Low Stock Warning'
                        msg['From'] = 'your_email@example.com'
                        msg['To'] = 'admin_email@example.com'
                        msg.set_content(f"Product '{selected_product}' is running low on stock. Only {new_stock} left.")
                        st.info("⚠️ Admin alerted of low stock via email.")
                    except Exception as e:
                        st.error(f"Low stock alert failed: {e}")
            else:
                st.warning(f"🚨 Only {current_stock} units of {selected_product} are available. Please reduce quantity.")
        else:
            st.error("⚠️ Please fill in your name, phone, and address to place an order.")

# ---------------------------
# Admin Dashboard Tab
# ---------------------------
with tab2:
    st.header("🔐 Admin Dashboard")

    admin_username = st.text_input("Admin Username")
    admin_password = st.text_input("Admin Password", type="password")

    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:
        if st.button("Login"):
            if admin_username == "admin" and admin_password == "harsh123":
                st.success("Login successful!")
                st.session_state.admin_logged_in = True
            else:
                st.error("Invalid credentials. Please try again.")

    if st.session_state.admin_logged_in:
        if os.path.exists(orders_path):
            df_orders = pd.read_csv(orders_path)
            st.subheader("📋 All Orders")
            st.dataframe(df_orders)
            st.markdown(f"**🛒 Total Orders:** {len(df_orders)}")
            st.markdown("### 🧮 Product-wise Sales Count")
            st.bar_chart(df_orders["Product"].value_counts())

        inventory_df = pd.read_csv(inventory_path)
        st.subheader("📦 Current Inventory")
        st.dataframe(inventory_df)

        # Option to place an order to supplier
        st.markdown("### ✉️ Place Order to Supplier")
        supplier_email = st.text_input("Supplier Email")
        supplier_product = st.selectbox("Select Product", inventory_df["Product"], key="supplier")
        supplier_quantity = st.number_input("Quantity to Order", min_value=1, step=1)
        if st.button("Send Order Email"):
            try:
                msg = EmailMessage()
                msg['Subject'] = 'Stock Order Request'
                msg['From'] = 'hvparashar23@gmail.com'
                msg['To'] = supplier_email
                msg.set_content(f"Please send {supplier_quantity} units of {supplier_product} to replenish our stock.")
                with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                    smtp.starttls()
                    password1= 'kvhc dofx brsm roqw'.replace('\xa0',' ')
                    smtp.login('hvparashar23@gmail.com',password1 )
                    smtp.send_message(msg)
                st.success(f"Order email sent for {supplier_quantity} units of {supplier_product} to {supplier_email}.")
            except Exception as e:
                st.error(f"Failed to send email: {e}")

        # Option to update inventory
        st.markdown("### ✏️ Update Inventory")
        for index, row in inventory_df.iterrows():
            new_stock = st.number_input(f"Stock for {row['Product']}", value=int(row['Stock']), step=1, key=row['Product'])
            inventory_df.at[index, 'Stock'] = new_stock
        if st.button("Update Stock"):
            inventory_df.to_csv(inventory_path, index=False)
            st.success("✅ Inventory updated.")

        # Generate PDF invoice for last order
        if st.button("🧾 Generate Invoice for Last Order"):
            def generate_invoice():
                df = pd.read_csv(orders_path)
                if df.empty:
                    return "No orders found."
                last_order = df.iloc[-1]
                price_map = {
                    "Makahan Nawabi": 250,
                    "Makahan Shahi": 220,
                    "Makahan Sultaana": 200,
                    "Makahan Azaadi": 180
                }
                product = last_order["Product"]
                price = price_map.get(product, 0)
                quantity = last_order.get("Quantity", 1)
                total_price = price * quantity

                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt="Makahan Store - Invoice", ln=True, align='C')
                pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
                pdf.ln(10)
                pdf.cell(200, 10, txt=f"Customer: {last_order['Customer Name']}", ln=True)
                pdf.cell(200, 10, txt=f"Phone: {last_order['Phone']}", ln=True)
                pdf.cell(200, 10, txt=f"Address: {last_order['Address']}", ln=True)
                pdf.cell(200, 10, txt=f"Product: {product}", ln=True)
                pdf.cell(200, 10, txt=f"Quantity: {quantity}", ln=True)
                pdf.cell(200, 10, txt=f"Price per unit: Rs{price}", ln=True)
                pdf.cell(200, 10, txt=f"Total Price: Rs{total_price}", ln=True)
                pdf.cell(200, 10, txt=f"Rating: {last_order['Rating']}/5", ln=True)

                pdf_file = "invoice_last_order.pdf"
                pdf.output(pdf_file)
                return pdf_file

            invoice = generate_invoice()
            st.success(f"Invoice generated: {invoice}")
            with open(invoice, "rb") as f:
                st.download_button(label="📥 Download Invoice",data=f,file_name=invoice,mime="application/pdf")


st.markdown("---")
st.caption(f"© {datetime.now().year} Makahan Store. All rights reserved.")
