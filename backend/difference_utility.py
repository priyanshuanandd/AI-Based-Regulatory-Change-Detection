from typing import List, Dict, Tuple, Optional
import difflib
import re
import hashlib
from pydantic import BaseModel

class SectionChange(BaseModel):
    title: str
    content: str

class ParagraphChange(BaseModel):
    old_paragraph: Optional[str] = None
    new_paragraph: Optional[str] = None
    similarity: Optional[float] = None

class SectionComparisonResult(BaseModel):
    added_sections: List[SectionChange]
    deleted_sections: List[SectionChange]

class ParagraphComparisonResult(BaseModel):
    added_paragraphs: List[ParagraphChange]
    deleted_paragraphs: List[ParagraphChange]
    modified_paragraphs: List[ParagraphChange]

def generate_cache_key(old_text: str, new_text: str) -> str:
    """Generate a unique key for caching document comparisons"""
    combined = old_text + new_text
    return hashlib.md5(combined.encode()).hexdigest()

def preprocess_text(text: str) -> List[str]:
    """Split text into sections with improved header detection"""
    sections = re.split(
        r'\n(?=\d+\.\d*\s+[A-Z][^\n]+|\n\[SECTION|ARTICLE|\n\s*[A-Z][A-Z\s]+\n|\n\s*[IVX]+\.\s|\n\s*\(\w\)\s)',
        text.strip()
    )
    return [s.strip() for s in sections if s.strip()]

def get_section_identifier(section: str) -> str:
    """Create a consistent identifier for each section"""
    first_line = section.split('\n')[0].strip()
    normalized = re.sub(r'[^\w\s]', '', first_line.lower())
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    return normalized[:100]

def compare_sections(old_text: str, new_text: str) -> Dict:
    """Identify added and deleted sections between documents"""
    old_sections = preprocess_text(old_text)
    new_sections = preprocess_text(new_text)
    
    old_map = {get_section_identifier(s): s for s in old_sections}
    new_map = {get_section_identifier(s): s for s in new_sections}
    
    old_keys = set(old_map.keys())
    new_keys = set(new_map.keys())
    
    added = [SectionChange(title=k, content=new_map[k]) for k in new_keys - old_keys]
    deleted = [SectionChange(title=k, content=old_map[k]) for k in old_keys - new_keys]
    
    return {
        'added_sections': added,
        'deleted_sections': deleted,
        'common_sections': list(old_keys & new_keys),
        'old_section_map': old_map,
        'new_section_map': new_map
    }

def split_into_paragraphs(text: str) -> List[str]:
    """Improved paragraph splitting that handles various formats"""
    paragraphs = re.split(r'\n\s*\n|\n\s*[\-\*•]\s+', text.strip())
    return [p.strip() for p in paragraphs if p.strip() and len(p.strip()) > 10]

def compare_paragraphs(old_para: str, new_para: str) -> Tuple[bool, float]:
    """Compare paragraphs with improved similarity detection"""
    old_normalized = re.sub(r'\s+', ' ', old_para.strip().lower())
    new_normalized = re.sub(r'\s+', ' ', new_para.strip().lower())
    
    if old_normalized == new_normalized:
        return (False, 1.0)
    
    matcher = difflib.SequenceMatcher(None, old_normalized, new_normalized)
    ratio = matcher.ratio()
    
    return (0.3 < ratio < 0.9, ratio)

def analyze_paragraph_changes(old_content: str, new_content: str) -> ParagraphComparisonResult:
    """Detailed paragraph-level comparison with improved change detection"""
    old_paras = split_into_paragraphs(old_content)
    new_paras = split_into_paragraphs(new_content)
    
    added = []
    deleted = []
    modified = []
    
    sm = difflib.SequenceMatcher(None, old_paras, new_paras)
    
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            continue
        elif tag == 'delete':
            deleted.extend([ParagraphChange(old_paragraph=p) for p in old_paras[i1:i2]])
        elif tag == 'insert':
            added.extend([ParagraphChange(new_paragraph=p) for p in new_paras[j1:j2]])
        elif tag == 'replace':
            for i in range(i1, i2):
                for j in range(j1, j2):
                    is_modified, ratio = compare_paragraphs(old_paras[i], new_paras[j])
                    if is_modified:
                        modified.append(ParagraphChange(
                            old_paragraph=old_paras[i],
                            new_paragraph=new_paras[j],
                            similarity=ratio
                        ))
                    else:
                        deleted.append(ParagraphChange(old_paragraph=old_paras[i]))
                        added.append(ParagraphChange(new_paragraph=new_paras[j]))
    
    return ParagraphComparisonResult(
        added_paragraphs=added,
        deleted_paragraphs=deleted,
        modified_paragraphs=modified
    )