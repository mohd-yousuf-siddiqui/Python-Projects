import streamlit as st
from bank import Bank

# ── Page Configuration ──────────────────────────────────────────────
st.set_page_config(
    page_title="🏦 Bank Account Manager",
    page_icon="🏦",
    layout="centered"
)

# ── Custom CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        color: #155724;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 8px;
        color: #721c24;
        margin: 1rem 0;
    }
    .info-card {
        padding: 1.5rem;
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 12px;
        color: white;
        margin: 0.5rem 0;
        text-align: center;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        border-radius: 8px 8px 0 0;
    }
</style>
""", unsafe_allow_html=True)

# ── Initialize Bank ─────────────────────────────────────────────────
@st.cache_resource
def get_bank():
    return Bank()

bank = get_bank()

# ── Header ──────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🏦 Bank Account Manager</h1>
    <p>Manage your accounts securely and efficiently</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar Info ────────────────────────────────────────────────────
with st.sidebar:
    st.header("📊 Bank Statistics")
    st.metric("Total Accounts", len(bank.data))
    total_balance = sum(acc.get("balance", 0) for acc in bank.data)
    st.metric("Total Deposits", f"₹{total_balance:,.2f}")
    st.divider()
    st.info("💡 **Tip:** Keep your Account Number and PIN safe. You need both for every transaction.")

# ── Main Tabs ───────────────────────────────────────────────────────
tabs = st.tabs([
    "🆕 Create Account",
    "💰 Deposit",
    "💸 Withdraw",
    "📋 Details",
    "✏️ Update",
    "🗑️ Delete"
])

# ────────────────────────────────────────────────────────────────────
# TAB 1: CREATE ACCOUNT
# ────────────────────────────────────────────────────────────────────
with tabs[0]:
    st.subheader("🆕 Create a New Account")
    st.caption("Fill in the details below to open your bank account.")

    with st.form("create_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("👤 Full Name", placeholder="Name")
            age = st.number_input("🎂 Age", min_value=1, max_value=120, value=18)

        with col2:
            email = st.text_input("📧 Email", placeholder="email@example.com")
            pin = st.number_input(
                "🔐 4-Digit PIN",
                min_value=1000, max_value=9999,
                value=1000, help="Choose a 4-digit PIN for your account"
            )

        submitted = st.form_submit_button("🚀 Create Account", use_container_width=True)

        if submitted:
            result = bank.create_account(name, age, email, pin)

            if result["success"]:
                acc = result["account"]
                st.balloons()
                st.success("✅ Account created successfully!")

                st.markdown(f"""
                <div class="info-card">
                    <h2>🎉 Welcome, {acc['name']}!</h2>
                    <h3>Your Account Number</h3>
                    <h1>{acc['account_no']}</h1>
                    <p>⚠️ Please save this — you'll need it for all transactions.</p>
                </div>
                """, unsafe_allow_html=True)

                with st.expander("📄 Full Account Details"):
                    st.json({
                        "Name": acc["name"],
                        "Age": acc["age"],
                        "Email": acc["email"],
                        "Account No": acc["account_no"],
                        "Balance": f"₹{acc['balance']:,.2f}"
                    })
            else:
                for err in result["errors"]:
                    st.error(f"❌ {err}")

# ────────────────────────────────────────────────────────────────────
# TAB 2: DEPOSIT
# ────────────────────────────────────────────────────────────────────
with tabs[1]:
    st.subheader("💰 Deposit Money")
    st.caption("Add funds to your account securely.")

    with st.form("deposit_form", clear_on_submit=True):
        acc_no = st.text_input("🔢 Account Number", placeholder="ACC-XXXXXX")
        pin = st.number_input("🔐 PIN", min_value=1000, max_value=9999, value=1000)
        amount = st.number_input(
            "💵 Amount to Deposit (₹)",
            min_value=0.0, max_value=100000.0,
            value=0.0, step=100.0
        )

        submitted = st.form_submit_button("💰 Deposit", use_container_width=True)

        if submitted:
            result = bank.deposit(acc_no, pin, amount)
            if result["success"]:
                st.success(result["message"])
                st.metric("New Balance", f"₹{result['new_balance']:,.2f}")
            else:
                st.error(f"❌ {result['error']}")

# ────────────────────────────────────────────────────────────────────
# TAB 3: WITHDRAW
# ────────────────────────────────────────────────────────────────────
with tabs[2]:
    st.subheader("💸 Withdraw Money")
    st.caption("Withdraw funds from your account.")

    with st.form("withdraw_form", clear_on_submit=True):
        acc_no = st.text_input("🔢 Account Number", placeholder="ACC-XXXXXX")
        pin = st.number_input("🔐 PIN", min_value=1000, max_value=9999, value=1000)
        amount = st.number_input(
            "💵 Amount to Withdraw (₹)",
            min_value=0.0, max_value=100000.0,
            value=0.0, step=100.0
        )

        submitted = st.form_submit_button("💸 Withdraw", use_container_width=True)

        if submitted:
            result = bank.withdraw(acc_no, pin, amount)
            if result["success"]:
                st.success(result["message"])
                st.metric("Remaining Balance", f"₹{result['new_balance']:,.2f}")
            else:
                st.error(f"❌ {result['error']}")

# ────────────────────────────────────────────────────────────────────
# TAB 4: DETAILS
# ────────────────────────────────────────────────────────────────────
with tabs[3]:
    st.subheader("📋 Account Details")
    st.caption("View your complete account information.")

    with st.form("details_form"):
        acc_no = st.text_input("🔢 Account Number", placeholder="ACC-XXXXXX")
        pin = st.number_input("🔐 PIN", min_value=1000, max_value=9999, value=1000)

        submitted = st.form_submit_button("🔍 View Details", use_container_width=True)

        if submitted:
            result = bank.get_details(acc_no, pin)

            if result["success"]:
                acc = result["account"]

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("👤 Name", acc["name"])
                with col2:
                    st.metric("🎂 Age", acc["age"])
                with col3:
                    st.metric("💰 Balance", f"₹{acc['balance']:,.2f}")

                st.divider()

                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"📧 **Email:** {acc['email']}")
                with col2:
                    st.info(f"🔢 **Account No:** {acc['account_no']}")

                # Transaction History
                if acc.get("transactions"):
                    st.divider()
                    st.subheader("📜 Transaction History")

                    for i, txn in enumerate(reversed(acc["transactions"]), 1):
                        icon = "🟢" if txn["type"] == "DEPOSIT" else "🔴"
                        st.write(
                            f"{icon} **{txn['type']}** — "
                            f"₹{txn['amount']:,.2f} | "
                            f"Balance after: ₹{txn['balance_after']:,.2f}"
                        )
                else:
                    st.caption("No transactions yet.")
            else:
                st.error(f"❌ {result['error']}")

# ────────────────────────────────────────────────────────────────────
# TAB 5: UPDATE
# ────────────────────────────────────────────────────────────────────
with tabs[4]:
    st.subheader("✏️ Update Account Details")
    st.caption("Modify your name, email, or PIN. Leave fields empty to keep current values.")

    with st.form("update_form", clear_on_submit=True):
        acc_no = st.text_input("🔢 Account Number", placeholder="ACC-XXXXXX")
        current_pin = st.number_input(
            "🔐 Current PIN", min_value=1000, max_value=9999, value=1000
        )

        st.divider()
        st.write("**Enter new values (leave blank / 0 to keep current):**")

        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input("👤 New Name", placeholder="Leave empty for no change")
            new_email = st.text_input("📧 New Email", placeholder="Leave empty for no change")
        with col2:
            new_pin = st.number_input(
                "🔐 New PIN (0 = no change)",
                min_value=0, max_value=9999, value=0
            )

        submitted = st.form_submit_button("✏️ Update Details", use_container_width=True)

        if submitted:
            result = bank.update_details(
                acc_no, current_pin,
                new_name=new_name,
                new_email=new_email,
                new_pin=new_pin
            )
            if result["success"]:
                st.success(f"✅ {result['message']}")
                with st.expander("📄 Updated Details"):
                    acc = result["account"]
                    st.json({
                        "Name": acc["name"],
                        "Email": acc["email"],
                        "Account No": acc["account_no"],
                        "Balance": f"₹{acc['balance']:,.2f}"
                    })
            else:
                st.error(f"❌ {result['error']}")

# ────────────────────────────────────────────────────────────────────
# TAB 6: DELETE
# ────────────────────────────────────────────────────────────────────
with tabs[5]:
    st.subheader("🗑️ Delete Account")
    st.caption("Permanently remove your account. This action cannot be undone.")

    st.warning("⚠️ You must withdraw all funds before deleting your account.")

    with st.form("delete_form", clear_on_submit=True):
        acc_no = st.text_input("🔢 Account Number", placeholder="ACC-XXXXXX")
        pin = st.number_input("🔐 PIN", min_value=1000, max_value=9999, value=1000)
        confirm = st.checkbox("✅ I confirm I want to permanently delete my account")

        submitted = st.form_submit_button(
            "🗑️ Delete Account",
            use_container_width=True,
            type="primary"
        )

        if submitted:
            if not confirm:
                st.error("❌ Please check the confirmation box to proceed.")
            else:
                result = bank.delete_account(acc_no, pin)
                if result["success"]:
                    st.success(f"✅ {result['message']}")
                    st.snow()
                else:
                    st.error(f"❌ {result['error']}")

# ── Footer ──────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<p style='text-align:center; color:gray;'>"
    "🏦 Bank Account Manager • Built with Streamlit"
    "</p>",
    unsafe_allow_html=True
)