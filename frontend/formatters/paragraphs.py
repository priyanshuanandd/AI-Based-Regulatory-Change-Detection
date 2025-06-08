def format_paragraphs(data):
    if not data:
        return "No paragraph changes detected in modified sections."
    
    output = []
    
    for section_id, changes in data.items():
        output.append(f"### Section: {section_id}")
        
        if changes['modified_paragraphs']:
            output.append("#### Modified Paragraphs")
            for para in changes['modified_paragraphs']:
                output.append(f"**Similarity:** {para['similarity']:.0%}")
                output.append("**Old version:**")
                output.append(f"> {para['old_paragraph']}")
                output.append("**New version:**")
                output.append(f"> {para['new_paragraph']}")
                output.append("---")
        
        if changes['added_paragraphs']:
            output.append("#### Added Paragraphs")
            for para in changes['added_paragraphs']:
                output.append(f"> {para['new_paragraph']}")
        
        if changes['deleted_paragraphs']:
            output.append("#### Deleted Paragraphs")
            for para in changes['deleted_paragraphs']:
                output.append(f"> ~~{para['old_paragraph']}~~")
    
    return "\n\n".join(output)