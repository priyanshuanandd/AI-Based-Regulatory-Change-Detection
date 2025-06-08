import requests
import json
from typing import List, Dict, Tuple
from concurrent.futures import ThreadPoolExecutor
from difference_utility import SectionChange

# Configuration
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "tinyllama"
MAX_WORKERS = 4
DEFAULT_BATCH_SIZE = 3  # Optimal for TinyLlama

def query_llm(prompt: str) -> Dict:
    """Generic LLM query function with error handling"""
    try:
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "format": "json",
            "stream": False
        }
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=60)
        response.raise_for_status()
        
        full_response = ""
        for line in response.text.splitlines():
            try:
                data = json.loads(line)
                full_response += data.get("response", "")
            except json.JSONDecodeError:
                continue
        
        return json.loads(full_response)
    except Exception as e:
        print(f"LLM query error: {str(e)}")
        return {"error": str(e)}

def analyze_added_sections(added_sections: List[SectionChange]) -> List[Dict]:
    """Analyze added sections with LLM"""
    if not added_sections:
        return []

    def create_prompt(section: SectionChange) -> str:
        return f"""Analyze this regulatory document addition and return JSON with:
        - change_summary: One-sentence summary
        - change_type: ["New Requirement", "Clarification", "Minor Edit"]
        - confidence: High/Medium/Low

        Section: {section.title}
        Content: {section.content[:500]}

        Return ONLY valid JSON:
        {{
            "change_summary": "",
            "change_type": "",
            "confidence": ""
        }}"""

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        prompts = [create_prompt(section) for section in added_sections]
        results = []
        for i, result in enumerate(executor.map(query_llm, prompts)):
            if "error" in result:
                results.append({
                    "change_summary": "Analysis failed",
                    "change_type": "Unknown",
                    "confidence": "Low"
                })
            else:
                results.append({
                    "section_title": added_sections[i].title,
                    **result
                })
    
    return results

def analyze_modified_sections(modified_sections: Dict[str, Dict[str, str]]) -> Dict[str, Dict]:
    """Analyze modified sections with batched LLM queries"""
    if not modified_sections:
        return {}

    sections_list = [
        (section_id, content['old'], content['new'])
        for section_id, content in modified_sections.items()
    ]

    def create_batch_prompt(batch: List[Tuple[str, str, str]]) -> str:
        prompt = """Analyze these document changes. For each, return:
        - section_id: Original identifier
        - change_summary: What changed
        - change_type: ["New Requirement", "Clarification", "Stricter", "Looser", "Minor"]
        - impact: High/Medium/Low
        - confidence: High/Medium/Low

        Return ONLY JSON like:
        [{
            "section_id": "id",
            "change_summary": "...",
            "change_type": "...",
            "impact": "...",
            "confidence": "..."
        }]

        Changes:"""
        
        for section_id, old_content, new_content in batch:
            prompt += f"""
            ---
            ID: {section_id}
            OLD:
            {old_content[:400]}
            NEW:
            {new_content[:400]}
            """
        return prompt

    results = {}
    for i in range(0, len(sections_list), DEFAULT_BATCH_SIZE):
        batch = sections_list[i:i + DEFAULT_BATCH_SIZE]
        try:
            response = query_llm(create_batch_prompt(batch))
            if isinstance(response, list):
                for item in response:
                    results[item['section_id']] = {
                        **item,
                        "old_content": modified_sections[item['section_id']]['old'][:500],
                        "new_content": modified_sections[item['section_id']]['new'][:500]
                    }
            else:
                raise ValueError("Invalid response format")
        except Exception as e:
            print(f"Batch failed: {str(e)}")
            # Fallback to individual processing
            for section_id, old_content, new_content in batch:
                try:
                    single_response = query_llm(create_batch_prompt([(section_id, old_content, new_content)]))
                    if isinstance(single_response, list) and len(single_response) > 0:
                        results[section_id] = {
                            **single_response[0],
                            "old_content": old_content[:500],
                            "new_content": new_content[:500]
                        }
                except Exception:
                    results[section_id] = {
                        "section_id": section_id,
                        "change_summary": "Analysis failed",
                        "change_type": "Unknown",
                        "impact": "Unknown",
                        "confidence": "Low",
                        "old_content": old_content[:500],
                        "new_content": new_content[:500]
                    }
    
    return results