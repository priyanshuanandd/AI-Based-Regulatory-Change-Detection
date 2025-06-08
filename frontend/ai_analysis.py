import streamlit as st

def display_ai_analysis(before_text, after_text, added_results=None, modified_results=None):
    st.markdown("### 🤖 AI Analysis of Added Sections")
    if added_results:
        for result in added_results:
            st.markdown(f"#### {result.get('section_title', 'Untitled Section')}")
            analysis = result.get("analysis", {})
            st.markdown(f"**Summary:** {analysis.get('change_summary', 'N/A')}")
            st.markdown(f"**Type:** `{analysis.get('change_type', 'Unknown')}`")
            st.markdown("**Content:**")
            st.code(result.get("section_content", "No content available"))
    else:
        st.info("No added sections found in AI analysis.")

    st.markdown("### 🤖 AI Analysis of Modified Sections")
    if modified_results:
        for section_id, analysis in modified_results.items():
            st.markdown(f"#### {section_id}")
            cols = st.columns(2)
            with cols[0]:
                st.markdown("**Old Version**")
                st.code(analysis.get("old_content", "N/A"))
            with cols[1]:
                st.markdown("**New Version**")
                st.code(analysis.get("new_content", "N/A"))
            st.markdown(f"**Summary:** {analysis.get('change_summary', 'N/A')}")
            st.markdown(f"**Type:** `{analysis.get('change_type', 'Unknown')}`")
            st.markdown(f"**Impact:** `{analysis.get('change_impact', 'Unknown')}`")
    else:
        st.info("No modified sections found in AI analysis.")
