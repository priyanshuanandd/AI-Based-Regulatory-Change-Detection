def format_added_ai(data):
    if not data:
        return "No AI analysis available for added sections."
    
    output = ["### 🤖 AI Analysis of Added Sections"]
    
    for section in data:
        output.append(f"#### Section : {section['section_title']}")
        output.append(f"**Content:**\n{section['section_content']}")
        output.append(f"**Analysis:**")
        output.append(f"- Summary: {section['analysis']['change_summary']}")
        output.append(f"- Type: {section['analysis']['change_type']}")
        output.append("---")
    
    return "\n\n".join(output)