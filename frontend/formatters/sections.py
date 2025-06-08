def format_sections(data):
    if not data:
        return "No section changes found"
    
    output = []
    
    if data['added_sections']:
        output.append("### Added Sections")
        for section in data['added_sections']:
            output.append(f"**{section['title']}**")
            output.append(f"```\n{section['content']}\n```")
    
    if data['deleted_sections']:
        output.append("### Deleted Sections")
        for section in data['deleted_sections']:
            output.append(f"~~{section['title']}~~")
            output.append(f"```\n{section['content']}\n```")
    
    if not output:
        return "No significant changes between sections"
    
    return "\n\n".join(output)