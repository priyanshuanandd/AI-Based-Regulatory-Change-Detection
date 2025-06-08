import requests
import json
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor
from difference_utility import SectionChange

# Configuration
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "tinyllama"  # Change to your preferred model
MAX_WORKERS = 4  # Number of parallel requests

def analyze_changes_with_llm(sections: List[SectionChange]) -> List[Dict]:
    """
    Analyze added sections with LLM in batches
    Returns list of analysis results in the same order as input sections
    """
    def create_prompt(section: SectionChange) -> str:
        return f"""
        Analyze this regulatory document change and return JSON with:
        - change_summary: One-sentence summary of the change
        - change_type: Categorize as "New Requirement", "Clarification of Existing Requirement", 
                      "Deletion of Requirement", or "Minor Edit"

        Section Title: {section.title}
        Section Content: {section.content}

        Return ONLY valid JSON with no additional text or formatting:
        {{
            "change_summary": "",
            "change_type": ""
        }}
        """

    def query_llm(prompt: str) -> Dict:
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

    # Process sections in parallel batches
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        prompts = [create_prompt(section) for section in sections]
        results = list(executor.map(query_llm, prompts))
    
    return results

def analyze_added_sections(added_sections: List[SectionChange]) -> List[Dict]:
    """
    Public interface for analyzing added sections
    """
    if not added_sections:
        return []
    
    return analyze_changes_with_llm(added_sections)



def analyze_modified_sections(modified_sections: Dict[str, Dict[str, str]]) -> Dict[str, Dict]:
    """
    Analyze modified sections with LLM in batches
    Args:
        modified_sections: Dictionary {section_id: {'old': old_content, 'new': new_content}}
    Returns:
        Dictionary {section_id: analysis_result} with same structure as added sections
    """
    if not modified_sections:
        return {}

    # Convert to list of tuples for batch processing
    sections_list = [
        (section_id, content['old'], content['new'])
        for section_id, content in modified_sections.items()
    ]

    def create_diff_prompt(batch: List[Tuple[str, str, str]]) -> str:
        prompt = """Analyze these regulatory document changes and return a JSON array where each item contains:
        - "section_id": Original section identifier
        - "change_summary": One-sentence summary of the modification
        - "change_type": One of ["New Requirement", "Clarification", 
                            "Stricter Requirement", "Looser Requirement", "Minor Edit"]
        - "change_impact": Low/Medium/High impact assessment

        For each change, compare the OLD and NEW versions:

        Return ONLY valid JSON formatted like this:
        [
            {
                "section_id": "section_1",
                "change_summary": "...",
                "change_type": "...",
                "change_impact": "..."
            }
        ]

        Changes to analyze:
        """
        
        for section_id, old_content, new_content in batch:
            prompt += f"""
            ---
            Section ID: {section_id}
            OLD VERSION:
            {old_content[:400]}
            NEW VERSION:
            {new_content[:400]}
            """
        return prompt

    def process_batch(batch: List[Tuple[str, str, str]]) -> Dict[str, Dict]:
        try:
            prompt = create_diff_prompt(batch)
            response = query_llm(prompt)
            return {item['section_id']: item for item in response}
        except Exception as e:
            print(f"Batch analysis failed: {e}")
            return {}

    # Process in batches of 3 (optimal for TinyLlama)
    batch_size = 3
    results = {}
    for i in range(0, len(sections_list), batch_size):
        batch = sections_list[i:i + batch_size]
        batch_results = process_batch(batch)
        
        # Fallback to individual processing if batch fails
        if not batch_results:
            print(f"Falling back to individual processing for batch {i//batch_size}")
            for section_id, old_content, new_content in batch:
                try:
                    single_result = process_batch([(section_id, old_content, new_content)])
                    results.update(single_result)
                except Exception:
                    results[section_id] = {
                        "section_id": section_id,
                        "change_summary": "Analysis failed",
                        "change_type": "Unknown",
                        "change_impact": "Unknown"
                    }
        else:
            results.update(batch_results)

    return results


