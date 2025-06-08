def format_modified_ai(data):
    if not data:
        return "No AI analysis available for modified sections."
    
    output = ["### 🤖 AI Analysis of Modified Sections"]
    
    for section_id, analysis in data.items():
        output.append(f"#### Section {section_id}")
        output.append(f"**Change Type:** {analysis['change_type'] or 'Not specified'}")
        output.append(f"**Impact:** {analysis['change_impact'] or 'Not specified'}")
        
        if analysis['change_summary']:
            output.append(f"**Summary:** {analysis['change_summary']}")
        
        # output.append("\n**Before:**")
        # output.append(f"> {analysis['old_content']}")
        # output.append("\n**After:**")
        # output.append(f"> {analysis['new_content']}")
        output.append("---")
    
    return "\n\n".join(output)