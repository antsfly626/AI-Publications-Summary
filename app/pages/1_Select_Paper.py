import streamlit as st
import requests
import random

st.set_page_config(page_title="Select Paper", page_icon="📄")

st.title("📄 Select a Research Paper")
st.markdown("Ask a question or describe the topic you’re looking for, and I’ll find the most relevant papers for you.")

# User input 
query = st.text_input("🧠 What kind of paper are you looking for?", placeholder="e.g., Studies on Mars atmospheric composition")

# Simulated paper database / API search (replace with NASA Data later) 
def mock_search_papers(query):
    mock_db = [
        {
            "title": "Analysis of Mars Atmospheric Dust using OSDR Data",
            "authors": ["Smith, A.", "Johnson, L."],
            "year": 2024,
            "summary": "This study analyzes atmospheric dust data from Mars collected by NASA OSDR and evaluates its spectral characteristics.",
            "link": "https://nasa.gov/mars-dust-study",
        },
        {
            "title": "Lunar Surface Reflectivity and Particle Scattering",
            "authors": ["Chen, Y.", "Patel, R."],
            "year": 2023,
            "summary": "A study on the scattering behavior of lunar dust particles and their impact on surface reflectivity and optical imaging.",
            "link": "https://nasa.gov/lunar-reflectivity",
        },
        {
            "title": "Astrobiological Indicators in Martian Ice Layers",
            "authors": ["Garcia, M.", "Williams, K."],
            "year": 2025,
            "summary": "Investigates potential astrobiological markers preserved in Martian polar ice using data from the ExoMars mission.",
            "link": "https://nasa.gov/martian-ice-biology",
        },
    ]
    # Randomly return 2-3 mock matches for now
    random.shuffle(mock_db)
    return mock_db[:2]

# Perform search 
if query:
    with st.spinner("🔍 Searching papers..."):
        results = mock_search_papers(query)

    if results:
        st.subheader("Top Results")
        for i, paper in enumerate(results, start=1):
            with st.expander(f"{i}. {paper['title']} ({paper['year']})"):
                st.markdown(f"**Authors:** {', '.join(paper['authors'])}")
                st.markdown(f"**Summary:** {paper['summary']}")
                st.markdown(f"[🔗 View Full Paper]({paper['link']})")

                if st.button(f"Select this paper", key=f"select_{i}"):
                    st.session_state["selected_paper"] = paper
                    st.success(f"✅ Selected: {paper['title']}")
                    st.switch_page("pages/2_Describe_Paper.py")
    else:
        st.warning("No results found. Try rephrasing your question.")
else:
    st.info("Type a topic or question above to begin your paper search.")
