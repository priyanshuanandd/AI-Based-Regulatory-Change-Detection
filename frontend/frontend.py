import streamlit as st
import requests
from io import StringIO
from ai_analysis import display_ai_analysis

BACKEND_URL = "http://localhost:8000"

def get_section_changes(before_text: str, after_text: str):
    files = {
        "old_version": ("old.txt", StringIO(before_text)),
        "new_version": ("new.txt", StringIO(after_text))
    }
    try:
        return requests.post(f"{BACKEND_URL}/compare/sections", files=files)
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to backend (sections): {e}")
        return None

def get_modified_paragraphs(before_text: str, after_text: str):
    files = {
        "old_version": ("old.txt", StringIO(before_text)),
        "new_version": ("new.txt", StringIO(after_text))
    }
    try:
        return requests.post(f"{BACKEND_URL}/compare/paragraphs", files=files)
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to backend (paragraphs): {e}")
        return None

def get_ai_analysis(before_text: str, after_text: str):
    files = {
        "old_version": ("old.txt", StringIO(before_text)),
        "new_version": ("new.txt", StringIO(after_text))
    }
    try:
        added_resp = requests.post(f"{BACKEND_URL}/added/ai", files=files)
        modified_resp = requests.post(f"{BACKEND_URL}/modified/ai", files=files)
        return added_resp, modified_resp
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to backend (AI analysis): {e}")
        return None, None

def main():
    st.set_page_config(page_title="Document Change Analyzer", layout="wide")
    st.title("📝 Advanced Document Change Analyzer")

    col1, col2 = st.columns(2)
    with col1:
        before_file = st.file_uploader("Original Version", type=["txt"], key="before_file")
    with col2:
        after_file = st.file_uploader("Updated Version", type=["txt"], key="after_file")

    if before_file is not None:
        st.session_state["before_text"] = before_file.read().decode("utf-8")
    if after_file is not None:
        st.session_state["after_text"] = after_file.read().decode("utf-8")

    before_text = st.session_state.get("before_text", "")
    after_text = st.session_state.get("after_text", "")

    if st.button("Analyze Changes", key="analyze_changes"):
        if before_text and after_text:
            st.session_state["run_analysis"] = True
            st.session_state["ai_analysis_done"] = False  # reset AI analysis flag
        else:
            st.warning("Please upload both the original and updated text files.")

    if st.session_state.get("run_analysis", False):
        # Section Changes
        with st.spinner("Identifying document changes..."):
            section_response = get_section_changes(before_text, after_text)

        if section_response and section_response.status_code == 200:
            section_results = section_response.json()

            with st.expander(f"➕ Added Sections ({len(section_results.get('added_sections', []))})", expanded=True):
                added_sections = section_results.get("added_sections", [])
                if added_sections:
                    for section in added_sections:
                        st.markdown(f"#### {section.get('title', 'Untitled Section')}")
                        st.code(section.get("content", "No content available"))
                else:
                    st.info("No sections were added")

            with st.expander(f"➖ Deleted Sections ({len(section_results.get('deleted_sections', []))})", expanded=True):
                deleted_sections = section_results.get("deleted_sections", [])
                if deleted_sections:
                    for section in deleted_sections:
                        st.markdown(f"#### {section.get('title', 'Untitled Section')}")
                        st.code(section.get("content", "No content available"))
                else:
                    st.info("No sections were deleted")

        else:
            st.error(f"Error analyzing documents: {section_response.text if section_response else 'No response'}")
            return

        # Modified Sections
        with st.expander("🔄 Modified Sections", expanded=True):
            with st.spinner("Fetching modified section comparison..."):
                modified_response = get_modified_paragraphs(before_text, after_text)

            if modified_response and modified_response.status_code == 200:
                modified_sections = modified_response.json()
                if modified_sections:
                    similarity_threshold = 0.90
                    any_modified = False

                    for section_title, data in modified_sections.items():
                        modified_paragraphs = data.get("modified_paragraphs", [])

                        if not modified_paragraphs:
                            continue

                        section_displayed = False
                        for para in modified_paragraphs:
                            similarity = para.get("similarity", 1.0)
                            old_para = para.get("old_paragraph", "").strip()
                            new_para = para.get("new_paragraph", "").strip()

                            if similarity < similarity_threshold and old_para != new_para:
                                if not section_displayed:
                                    st.markdown(f"### 📝 {section_title}")
                                    section_displayed = True
                                cols = st.columns(2)
                                with cols[0]:
                                    st.markdown("**Old Version**")
                                    st.code(old_para)
                                with cols[1]:
                                    st.markdown("**New Version**")
                                    st.code(new_para)
                                any_modified = True

                    if not any_modified:
                        st.info("No significantly modified sections found.")
                else:
                    st.info("No sections were modified.")
            else:
                st.error(f"Error fetching modified sections: {modified_response.text if modified_response else 'No response'}")

        # Run AI analysis automatically here (once per full analysis)
        if not st.session_state.get("ai_analysis_done", False):
            with st.spinner("Analyzing changes with AI..."):
                added_resp, modified_resp = get_ai_analysis(before_text, after_text)
                st.session_state["ai_added_resp"] = added_resp.json() if added_resp and added_resp.status_code == 200 else None
                st.session_state["ai_modified_resp"] = modified_resp.json() if modified_resp and modified_resp.status_code == 200 else None
                st.session_state["ai_analysis_done"] = True

        # Display AI analysis results
        display_ai_analysis(
            before_text,
            after_text,
            st.session_state.get("ai_added_resp"),
            st.session_state.get("ai_modified_resp")
        )

if __name__ == "__main__":
    main()
