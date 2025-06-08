import requests
import json
from typing import List, Dict
from difference_utility import SectionChange

# Configuration
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "tinyllama"  # Change to your preferred model

def analyze_changes_with_llm(section: SectionChange) -> Dict:
    
    prompt = f"""
    As a regulatory document expert, analyze the section below and return a JSON object with:
    - change_summary: A one-sentence summary of the section's purpose or change,output "INSIGNIFICANT" for cases you dont know answer to
    - change_type: One of "New Requirement", "Clarification of Existing Requirement", "Deletion of Requirement", or "Minor Edit" (use for formatting/typo changes only).

    Section Title: {section.title}
    Section Content: {section.content}

    Rules:
    - Use only the provided title and content.
    - Make change_summary specific (e.g., "Sets new audit deadline" not "New requirement").
    - If unclear, default change_type to "Clarification of Existing Requirement".
    - Return only a valid JSON object with the two fields, no extra text.

    Return:
    {{
        "change_summary": "",
        "change_type": ""
    }}
    """
    
    try:
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "format": "json",
            "stream": False
        }
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        
        # Ollama returns newline-delimited JSON
        full_response = ""
        for line in response.text.splitlines():
            data = json.loads(line)
            full_response += data.get("response", "")
        
        return json.loads(full_response)
    except Exception as e:
        print(f"Error querying LLM: {e}")
        return {
            "change_summary": "Analysis failed",
            "change_type": "Unknown"
        }

def analyze_added_sections(added_sections: List[SectionChange]) -> List[Dict]:
    """
    Public interface for analyzing added sections
    """
    if not added_sections:
        return []
    
    return [analyze_changes_with_llm(section) for section in added_sections]

def analyze_modified_sections(modified_sections: Dict[str, Dict[str, str]]) -> Dict[str, Dict]:
    """
    Analyze modified sections with LLM
    Args:
        modified_sections: Dictionary {section_id: {'old': old_content, 'new': new_content}}
    Returns:
        Dictionary {section_id: analysis_result} with same structure as added sections
    """
    if not modified_sections:
        return {}

    results = {}
    for section_id, content in modified_sections.items():
        prompt = f"""
        Analyze this regulatory document change and return JSON with:
        - section_id: Original section identifier
        - change_summary:  A one-sentence summary of the section's modification,output "INSIGNIFICANT" for cases you dont know answer to
        - change_type: One of ["New Requirement", "Clarification", 
                          "Stricter Requirement", "Looser Requirement", "Minor Edit"]
        - change_impact: Low/Medium/High impact assessment

        Section ID: {section_id}
        OLD VERSION:
        {content['old'][:400]}
        NEW VERSION:
        {content['new'][:400]}

        Return ONLY valid JSON with no additional text or formatting:
        {{
            "section_id": "{section_id}",
            "change_summary": "",
            "change_type": "",
            "change_impact": ""
        }}
        """
        
        try:
            payload = {
                "model": MODEL_NAME,
                "prompt": prompt,
                "format": "json",
                "stream": False
            }
            response = requests.post(OLLAMA_API_URL, json=payload)
            response.raise_for_status()
            
            # Ollama returns newline-delimited JSON
            full_response = ""
            for line in response.text.splitlines():
                data = json.loads(line)
                full_response += data.get("response", "")
            
            result = json.loads(full_response)
            results[section_id] = result
        except Exception as e:
            print(f"Error analyzing section {section_id}: {e}")
            results[section_id] = {
                "section_id": section_id,
                "change_summary": "Analysis failed",
                "change_type": "Unknown",
                "change_impact": "Unknown"
            }

    return results