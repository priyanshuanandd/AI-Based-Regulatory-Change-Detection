import streamlit as st
from api_client import *
from formatters.sections import format_sections
from formatters.paragraphs import format_paragraphs
from formatters.added_ai import format_added_ai
from formatters.modified_ai import format_modified_ai

# Page configuration
st.set_page_config(
    page_title="Document Comparison Tool",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'results' not in st.session_state:
    st.session_state.results = {
        'sections': None,
        'paragraphs': None,
        'added_ai': None,
        'modified_ai': None
    }

if 'current_step' not in st.session_state:
    st.session_state.current_step = 0

# Header with styling
st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1 style="color: #1f77b4; margin-bottom: 0.5rem;">📄 Document Comparison Tool</h1>
    <p style="color: #666; font-size: 1.1rem;">Compare and analyze differences between document versions</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# File upload section with improved layout
st.markdown("### 📁 Upload Documents")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Original Version**")
    old_file = st.file_uploader(
        "Choose the old version file", 
        type=["txt"], 
        key="old_file",
        help="Upload the original document version"
    )

with col2:
    st.markdown("**Updated Version**")
    new_file = st.file_uploader(
        "Choose the new version file", 
        type=["txt"], 
        key="new_file",
        help="Upload the updated document version"
    )

if old_file and new_file:
    st.markdown("---")
    
    # Display file info
    st.markdown("### ✅ Files Loaded")
    info_col1, info_col2 = st.columns(2)
    
    with info_col1:
        st.info(f"📋 **Original:** {old_file.name}")
    
    with info_col2:
        st.info(f"📋 **Updated:** {new_file.name}")
    
    st.markdown("---")
    
    # Analysis buttons with improved styling and sequential order
    st.markdown("### 🔍 Analysis Options")
    st.markdown("Complete the analyses in order. Each step builds upon the previous one:")
    
    # Progress indicator
    progress_text = f"**Progress: Step {st.session_state.current_step + 1} of 4**"
    if st.session_state.current_step == 4:
        progress_text = "**✅ All analyses completed!**"
    st.markdown(progress_text)
    
    # Progress bar
    progress_value = st.session_state.current_step / 4
    st.progress(progress_value)
    
    # Create columns for buttons with better spacing
    cols = st.columns([1, 1, 1, 1])
    
    button_style = """
    <style>
    .stButton > button {
        width: 100%;
        height: 3rem;
        border-radius: 10px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton > button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }
    </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)
    
    # Step 1: Compare Sections
    with cols[0]:
        step1_disabled = st.session_state.current_step < 0
        step1_completed = st.session_state.current_step > 0
        
        button_text = "✅ 1. Sections Done" if step1_completed else "🔄 1. Compare Sections"
        button_type = "secondary" if step1_completed else "primary"
        
        if st.button(button_text, use_container_width=True, type=button_type, disabled=step1_disabled or step1_completed):
            with st.spinner("Comparing sections..."):
                st.session_state.results['sections'] = compare_sections(old_file, new_file)
                st.session_state.current_step = 1
            st.success("Section comparison completed!")
            st.rerun()
    
    # Step 2: Compare Paragraphs
    with cols[1]:
        step2_disabled = st.session_state.current_step < 1
        step2_completed = st.session_state.current_step > 1
        
        button_text = "✅ 2. Paragraphs Done" if step2_completed else "📝 2. Compare Paragraphs"
        button_type = "secondary" if step2_completed else "primary"
        
        if st.button(button_text, use_container_width=True, type=button_type, disabled=step2_disabled or step2_completed):
            with st.spinner("Comparing paragraphs..."):
                st.session_state.results['paragraphs'] = compare_paragraphs(old_file, new_file)
                st.session_state.current_step = 2
            st.success("Paragraph comparison completed!")
            st.rerun()
    
    # Step 3: Analyze Added
    with cols[2]:
        step3_disabled = st.session_state.current_step < 2
        step3_completed = st.session_state.current_step > 2
        
        button_text = "✅ 3. Added Done" if step3_completed else "➕ 3. Analyze Added"
        button_type = "secondary" if step3_completed else "primary"
        
        if st.button(button_text, use_container_width=True, type=button_type, disabled=step3_disabled or step3_completed):
            with st.spinner("Analyzing added sections..."):
                st.session_state.results['added_ai'] = analyze_added_sections(old_file, new_file)
                st.session_state.current_step = 3
            st.success("Added sections analysis completed!")
            st.rerun()
    
    # Step 4: Analyze Modified
    with cols[3]:
        step4_disabled = st.session_state.current_step < 3
        step4_completed = st.session_state.current_step > 3
        
        button_text = "✅ 4. Modified Done" if step4_completed else "✏️ 4. Analyze Modified"
        button_type = "secondary" if step4_completed else "primary"
        
        if st.button(button_text, use_container_width=True, type=button_type, disabled=step4_disabled or step4_completed):
            with st.spinner("Analyzing modified sections..."):
                st.session_state.results['modified_ai'] = analyze_modified_sections(old_file, new_file)
                st.session_state.current_step = 4
            st.success("Modified sections analysis completed!")
            st.rerun()
    
    st.markdown("---")
    
    # Results section with better organization
    has_results = any(st.session_state.results.values())
    
    if has_results:
        st.markdown("### 📊 Analysis Results")
        
        # Create tabs for better organization of results
        tabs = st.tabs(["📋 Sections", "📝 Paragraphs", "➕ Added", "✏️ Modified"])
        
        with tabs[0]:
            if st.session_state.results['sections']:
                st.markdown("#### Section Comparison Results")
                st.markdown(format_sections(st.session_state.results['sections']))
            else:
                st.info("No section comparison results yet. Click the 'Compare Sections' button above.")
        
        with tabs[1]:
            if st.session_state.results['paragraphs']:
                st.markdown("#### Paragraph Comparison Results")
                st.markdown(format_paragraphs(st.session_state.results['paragraphs']))
            else:
                st.info("No paragraph comparison results yet. Click the 'Compare Paragraphs' button above.")
        
        with tabs[2]:
            if st.session_state.results['added_ai']:
                st.markdown("#### Added Sections Analysis")
                st.markdown(format_added_ai(st.session_state.results['added_ai']))
            else:
                st.info("No added sections analysis yet. Click the 'Analyze Added' button above.")
        
        with tabs[3]:
            if st.session_state.results['modified_ai']:
                st.markdown("#### Modified Sections Analysis")
                st.markdown(format_modified_ai(st.session_state.results['modified_ai']))
            else:
                st.info("No modified sections analysis yet. Click the 'Analyze Modified' button above.")
        
        # Add a reset workflow button
        st.markdown("---")
        col_reset1, col_reset2 = st.columns([1, 1])
        
        with col_reset1:
            if st.button("🔄 Reset Workflow", type="secondary"):
                st.session_state.results = {
                    'sections': None,
                    'paragraphs': None,
                    'added_ai': None,
                    'modified_ai': None
                }
                st.session_state.current_step = 0
                st.success("Workflow reset! Start from Step 1.")
                st.rerun()
        
        with col_reset2:
            if st.button("🗑️ Clear All Results", type="secondary"):
                st.session_state.results = {
                    'sections': None,
                    'paragraphs': None,
                    'added_ai': None,
                    'modified_ai': None
                }
                st.session_state.current_step = 0
                st.success("All results cleared!")
                st.rerun()
    
    else:
        st.markdown("### 📊 Analysis Results")
        st.info("👆 Run an analysis above to see results here")

else:
    # Instructions when no files are uploaded
    st.markdown("### 📋 Instructions")
    st.markdown("""
    1. **Upload Files**: Choose your original and updated document versions above
    2. **Run Analysis**: Click the analysis buttons to compare your documents
    3. **View Results**: Results will appear in organized tabs below
    
    **Supported Analysis Types (Sequential Order):**
    - 🔄 **Step 1 - Section Comparison**: Compare major sections between versions
    - 📝 **Step 2 - Paragraph Comparison**: Detailed paragraph-level differences  
    - ➕ **Step 3 - Added Content**: Identify newly added sections
    - ✏️ **Step 4 - Modified Content**: Analyze changes to existing sections
    
    *Note: Each step must be completed in order to unlock the next one.*
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 1rem;'>"
    "📄 Document Comparison Tool | Built with Streamlit"
    "</div>", 
    unsafe_allow_html=True
)