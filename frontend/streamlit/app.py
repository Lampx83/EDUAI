import streamlit as st
import requests
import json

# =========================
# CONFIG
# =========================
API_BASE = "http://localhost:8011"

st.set_page_config(
    page_title="EDUAI Backend Test UI",
    layout="wide",
)

st.title("EDUAI – Backend Test Frontend (Streamlit)")
st.caption("Frontend tối giản – chỉ dùng để test FastAPI backend")

# =========================
# SESSION STATE
# =========================
if "token" not in st.session_state:
    st.session_state.token = None

# =========================
# 1. LOGIN
# =========================
st.header("1️⃣ Login")

with st.form("login_form"):
    col1, col2 = st.columns(2)
    with col1:
        username = st.text_input("Username", value="admin")
    with col2:
        password = st.text_input("Password", type="password", value="admin123")

    login_btn = st.form_submit_button("Login")

if login_btn:
    try:
        resp = requests.post(
            f"{API_BASE}/auth/login",
            json={
                "username": username,
                "password": password,
            },
            timeout=10,
        )

        if resp.status_code == 200:
            st.session_state.token = resp.json()["access_token"]
            st.success("Login successful")
        else:
            st.error(f"Login failed: {resp.text}")

    except Exception as exc:
        st.error(str(exc))

if st.session_state.token:
    st.markdown("**JWT Token:**")
    st.code(st.session_state.token, language="text")

# =========================
# 2. SEMANTIC SEARCH
# =========================
st.header("2️⃣ Semantic Search")

query = st.text_area(
    "Query (ngôn ngữ tự nhiên)",
    placeholder="Ví dụ: Kinh tế quốc dân",
    height=80,
)

top_k = st.slider(
    "Top K",
    min_value=1,
    max_value=20,
    value=5,
)

search_btn = st.button("Search")

if search_btn:
    if not st.session_state.token:
        st.warning("Vui lòng login trước")
    elif not query.strip():
        st.warning("Query không được để trống")
    else:
        try:
            headers = {
                "Authorization": f"Bearer {st.session_state.token}"
            }

            payload = {
                "query": query,
                "top_k": top_k,
            }

            resp = requests.post(
                f"{API_BASE}/search/semantic",
                json=payload,
                headers=headers,
                timeout=30,
            )

            if resp.status_code != 200:
                st.error(f"Search failed: {resp.text}")
            else:
                data = resp.json()

                # =========================
                # RAW RESPONSE
                # =========================
                st.subheader("📦 Raw API Response")
                st.json(data)

                # =========================
                # HUMAN-READABLE VIEW
                # =========================
                st.subheader("📄 Results")

                results = data.get("results", [])
                if not results:
                    st.info("No results")
                else:
                    for idx, r in enumerate(results, 1):
                        title = (
                            f"[{idx}] "
                            f"score={r['score']:.4f} | "
                            f"file={r['file_hash']} | "
                            f"chunk={r['chunk_id']}"
                        )
                        with st.expander(title):
                            st.write(r["text"])
                            st.caption(
                                f"section={r.get('section_id')} | "
                                f"token_estimate={r.get('token_estimate')}"
                            )

        except Exception as exc:
            st.error(str(exc))

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption(
    "EDUAI Streamlit Frontend – dùng cho test & debug backend. "
    "Không phải frontend sản phẩm."
)
