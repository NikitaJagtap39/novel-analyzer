import streamlit as st
from query_vector_db import query_novel
from rag_pipeline import generate_answer

st.set_page_config(
    page_title="Novel Analyzer",
    page_icon="📖",
    layout="wide"
)

st.title("📖 Novel Analyzer - Ask Questions about your Novel")
st.markdown("Enter a question about your novel. The system will provide an answer with page references from the book.")

# Input box for user question
user_question = st.text_input("Ask your question here:")

# Number of top documents to retrieve
top_n = st.slider("Number of top pages to consider:", 1, 10, 5)

# Store answers and context in session state
if "history" not in st.session_state:
    st.session_state.history = []

if st.button("Get Answer"):
    if not user_question.strip():
        st.warning("Please enter a question!")
    else:
        with st.spinner("Generating answer..."):
            try:
                # 1️⃣ Generate answer
                answer = generate_answer(user_question, top_n=top_n)
                
                # 2️⃣ Get top matching pages for reference
                results = query_novel(user_question, n_results=top_n)
                top_docs = results["documents"][0]
                top_metas = results["metadatas"][0]

                # 3️⃣ Save in session state
                st.session_state.history.append({
                    "question": user_question,
                    "answer": answer,
                    "docs": [(top_metas[i]["page"], top_docs[i]) for i in range(len(top_docs))]
                })

                # 4️⃣ Display the answer
                st.subheader("Answer:")
                st.write(answer)

                # 5️⃣ Show page references in an expandable section
                with st.expander("Show top matching pages (page references)"):
                    for page_num, doc in st.session_state.history[-1]["docs"]:
                        st.markdown(f"**Page {page_num}:**\n{doc[:500]}{'...' if len(doc) > 500 else ''}")

            except Exception as e:
                st.error(f"Error generating answer: {e}")

# Optional: show previous questions & answers
if st.session_state.history:
    st.markdown("---")
    st.subheader("Previous Questions & Answers")
    for idx, item in enumerate(reversed(st.session_state.history), 1):
        st.markdown(f"**Q{idx}: {item['question']}**")
        st.write(item['answer'])
