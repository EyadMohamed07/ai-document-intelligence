import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="AI Document Intelligence System",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Document Intelligence System")
st.markdown("Automated RAG-powered extraction, analysis, and question answering.")

# ----------------- Sidebar Configuration -----------------
st.sidebar.header("⚙️ Server Configuration")
api_base_url = st.sidebar.text_input(
    "Kaggle API URL",
    placeholder="https://xxxx.ngrok-free.app"
).strip().rstrip('/')

# Header to automatically bypass the free ngrok browser warning screen
NGROK_HEADERS = {"ngrok-skip-browser-warning": "69420"}

st.sidebar.header("📁 Document Management")
uploaded_file = st.sidebar.file_uploader("Upload PDF Document", type=["pdf"])

# ----------------- Validation & Upload Handling -----------------
if not api_base_url:
    st.warning("⚠️ Please provide the public Kaggle ngrok API URL in the sidebar.")
elif uploaded_file is None:
    st.info("👈 Please upload a PDF document from the sidebar to start.")
else:
    # Trigger indexing automatically when a new document is uploaded
    if "indexed_file" not in st.session_state or st.session_state.indexed_file != uploaded_file.name:
        with st.spinner("Uploading and indexing document on Kaggle GPU..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                response = requests.post(
                    f"{api_base_url}/upload",
                    files=files,
                    headers=NGROK_HEADERS,
                    timeout=180
                )
                if response.status_code == 200:
                    st.session_state.indexed_file = uploaded_file.name
                    st.sidebar.success(f"✅ Document '{uploaded_file.name}' indexed successfully!")
                else:
                    st.sidebar.error(f"Server Error ({response.status_code}): {response.text}")
            except requests.exceptions.RequestException as e:
                st.sidebar.error(f"Failed to connect to Kaggle backend: {e}")

    # ----------------- Main Interface Tabs -----------------
    tab1, tab2 = st.tabs(["📊 Document Intelligence", "💬 Ask Document"])

    # ----------------- TAB 1: Document Intelligence -----------------
    with tab1:
        st.subheader("Automated Document Intelligence")
        st.caption("Extracts executive summary, key points, risks, and references into a structured schema.")
        
        if st.button("Generate Intelligence Summary", type="primary"):
            with st.spinner("Analyzing document structure and constraints on GPU (this may take 30–60s)..."):
                try:
                    response = requests.get(
                        f"{api_base_url}/intelligence",
                        headers=NGROK_HEADERS,
                        timeout=300
                    )
                    if response.status_code == 200:
                        data = response.json()
                        st.success("Extraction completed successfully!")
                        
                        # Structured JSON rendering
                        if "Document" in data or "Summary" in data:
                            st.markdown(f"### 📑 **{data.get('Document', 'Document Analysis')}**")
                            st.info(f"**Executive Summary:**\n\n{data.get('Summary', 'N/A')}")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown("#### 📌 Key Points")
                                points = data.get("Key Points", [])
                                if isinstance(points, list):
                                    for pt in points:
                                        st.write(f"- {pt}")
                                else:
                                    st.write(points)
                            
                            with col2:
                                st.markdown("#### ⚠️ Risks & Constraints")
                                risks = data.get("Risks")
                                if risks:
                                    st.warning(risks)
                                else:
                                    st.success("No explicit risks, penalties, or liabilities identified.")
                                    
                            st.markdown("#### 📚 References & Evidence")
                            refs = data.get("References", "N/A")
                            if isinstance(refs, list):
                                for ref in refs:
                                    st.caption(f"• {ref}")
                            else:
                                st.caption(refs)
                        else:
                            st.write(data)
                    else:
                        st.error(f"Server Error ({response.status_code}): {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Connection timed out or failed: {e}")

    # ----------------- TAB 2: Interactive Q&A -----------------
    with tab2:
        st.subheader("Interactive Q&A with Grounded Citations")
        user_query = st.text_input("Enter your question about the uploaded document:")
        
        if st.button("Submit Question") and user_query:
            with st.spinner("Retrieving relevant context and generating grounded answer..."):
                try:
                    response = requests.post(
                        f"{api_base_url}/ask",
                        data={"question": user_query},
                        headers=NGROK_HEADERS,
                        timeout=180
                    )
                    if response.status_code == 200:
                        qa_result = response.json()
                        st.markdown("### 💡 Answer")
                        st.write(qa_result.get("answer", qa_result))
                        
                        sources = qa_result.get("sources")
                        if sources:
                            st.markdown("#### 📖 Sources & Citations")
                            st.caption(sources)
                    else:
                        st.error(f"Server Error ({response.status_code}): {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Connection failed: {e}")