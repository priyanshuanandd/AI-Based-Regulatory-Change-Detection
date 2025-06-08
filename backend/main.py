from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List, Optional, Dict
from difference_utility import (
    SectionComparisonResult,
    ParagraphComparisonResult,
    compare_sections,
    analyze_paragraph_changes,
    generate_cache_key
)
from llm_utility import analyze_added_sections,analyze_modified_sections

app = FastAPI()

# In-memory cache (replace with Redis in production)
document_cache = {}

@app.post("/compare/sections", response_model=SectionComparisonResult)
async def compare_sections_endpoint(
    old_version: UploadFile = File(...),
    new_version: UploadFile = File(...)
):
    """First-pass comparison identifying added/deleted sections"""
    try:
        old_text = (await old_version.read()).decode('utf-8')
        new_text = (await new_version.read()).decode('utf-8')
        
        cache_key = generate_cache_key(old_text, new_text)
        if cache_key in document_cache:
            return document_cache[cache_key]['section_result']
        
        comparison = compare_sections(old_text, new_text)
        
        # Store intermediate results for paragraph analysis
        document_cache[cache_key] = {
            'section_result': SectionComparisonResult(
                added_sections=comparison['added_sections'],
                deleted_sections=comparison['deleted_sections']
            ),
            'common_sections': comparison['common_sections'],
            'old_section_map': comparison['old_section_map'],
            'new_section_map': comparison['new_section_map']
        }
        
        return document_cache[cache_key]['section_result']
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/compare/paragraphs", response_model=Dict[str, ParagraphComparisonResult])
async def compare_paragraphs_endpoint(
    old_version: UploadFile = File(...),
    new_version: UploadFile = File(...),
    section_filter: Optional[List[str]] = None
):
    """Second-pass comparison analyzing paragraph changes in modified sections"""
    try:
        old_text = (await old_version.read()).decode('utf-8')
        new_text = (await new_version.read()).decode('utf-8')
        
        cache_key = generate_cache_key(old_text, new_text)
        if cache_key not in document_cache:
            # Ensure section comparison was done first
            await compare_sections_endpoint(
                UploadFile(filename="old.txt", file=old_version.file),
                UploadFile(filename="new.txt", file=new_version.file)
            )
        
        cache_data = document_cache[cache_key]
        results = {}
        
        # Filter sections to analyze if specified
        sections_to_analyze = section_filter if section_filter else cache_data['common_sections']
        
        for section_id in sections_to_analyze:
            if section_id not in cache_data['common_sections']:
                continue
            
            old_content = cache_data['old_section_map'][section_id]
            new_content = cache_data['new_section_map'][section_id]
            
            if old_content != new_content:
                para_results = analyze_paragraph_changes(old_content, new_content)
                results[section_id] = para_results
        
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "cache_size": len(document_cache)}


@app.post("/added/ai", response_model=List[Dict])
async def analyze_added_sections_with_ai(
    old_version: UploadFile = File(...),
    new_version: UploadFile = File(...)
):
    """
    Analyze added sections with AI
    """
    try:
        old_text = (await old_version.read()).decode('utf-8')
        new_text = (await new_version.read()).decode('utf-8')
        
        cache_key = generate_cache_key(old_text, new_text)
        if cache_key not in document_cache:
            # Ensure section comparison was done first
            await compare_sections_endpoint(
                UploadFile(filename="old.txt", file=old_version.file),
                UploadFile(filename="new.txt", file=new_version.file)
            )
        
        cache_data = document_cache[cache_key]
        added_sections = cache_data['section_result'].added_sections
        
        # Analyze added sections with LLM
        analysis_results = analyze_added_sections(added_sections)
        
        # Combine section data with analysis
        results = []
        for section, analysis in zip(added_sections, analysis_results):
            results.append({
                "section_title": section.title,
                "section_content": section.content,
                "analysis": analysis
            })
        
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    


@app.post("/modified/ai", response_model=Dict[str, Dict])
async def analyze_modified_sections_with_ai(
    old_version: UploadFile = File(...),
    new_version: UploadFile = File(...),
    batch_size: int =3
):
    """
    Analyze modified sections with AI
    Returns:
        {
            "section_id": {
                "change_summary": "...",
                "change_type": "...",
                "change_impact": "...",
                "old_content": "...",  # Truncated
                "new_content": "..."   # Truncated
            }
        }
    """
    try:
        old_text = (await old_version.read()).decode('utf-8')
        new_text = (await new_version.read()).decode('utf-8')
        
        cache_key = generate_cache_key(old_text, new_text)
        if cache_key not in document_cache:
            await compare_sections_endpoint(
                UploadFile(filename="old.txt", file=old_version.file),
                UploadFile(filename="new.txt", file=new_version.file)
            )
        
        cache_data = document_cache[cache_key]
        modified_sections = {
            section_id: {
                'old': cache_data['old_section_map'][section_id],
                'new': cache_data['new_section_map'][section_id]
            }
            for section_id in cache_data['common_sections']
            if cache_data['old_section_map'][section_id] != cache_data['new_section_map'][section_id]
        }

        analysis_results = analyze_modified_sections(modified_sections)
        
        # Enrich with content snippets
        for section_id, result in analysis_results.items():
            result.update({
                'old_content': modified_sections[section_id]['old'][:500] + '...',
                'new_content': modified_sections[section_id]['new'][:500] + '...'
            })
        
        return analysis_results
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))