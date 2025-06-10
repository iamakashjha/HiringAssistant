"""
Utility functions for the TalentScout Hiring Assistant.
"""

import re
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime

def extract_email(text: str) -> Optional[str]:
    """Extract email address from text."""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(email_pattern, text)
    return match.group(0) if match else None

def extract_phone(text: str) -> Optional[str]:
    """Extract phone number from text."""
    phone_pattern = r'\b(?:\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
    match = re.search(phone_pattern, text)
    return match.group(0) if match else None

def extract_years_experience(text: str) -> Optional[int]:
    """Extract years of experience from text."""
    years_pattern = r'\b(\d+)\s*(?:years?|yrs?)\s*(?:of)?\s*experience\b'
    match = re.search(years_pattern, text.lower())
    return int(match.group(1)) if match else None

def extract_name(text: str) -> Optional[str]:
    """Extract name from text."""
    # Look for common name patterns
    name_patterns = [
        r'name\s*(?:is)?\s*:?\s*([A-Za-z\s]+)',
        r'my\s+name\s+is\s+([A-Za-z\s]+)',
        r'i\s+am\s+([A-Za-z\s]+)',
        r'^([A-Za-z\s]+)$'  # If the entire text is just a name
    ]
    
    for pattern in name_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            if len(name.split()) >= 2:  # Ensure it's a full name
                return name
    return None

def extract_position(text: str) -> Optional[str]:
    """Extract desired position from text."""
    position_patterns = [
        r'position\s*(?:is)?\s*:?\s*([A-Za-z\s]+)',
        r'role\s*(?:is)?\s*:?\s*([A-Za-z\s]+)',
        r'looking\s+for\s+([A-Za-z\s]+)\s+position',
        r'desired\s+position\s+is\s+([A-Za-z\s]+)'
    ]
    
    for pattern in position_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None

def extract_location(text: str) -> Optional[str]:
    """Extract location from text."""
    location_patterns = [
        r'location\s*(?:is)?\s*:?\s*([A-Za-z\s,]+)',
        r'based\s+in\s+([A-Za-z\s,]+)',
        r'from\s+([A-Za-z\s,]+)',
        r'currently\s+in\s+([A-Za-z\s,]+)'
    ]
    
    for pattern in location_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None

def parse_candidate_info(text: str) -> Dict[str, str]:
    """Parse candidate information from text."""
    info = {
        'name': extract_name(text),
        'email': extract_email(text),
        'phone': extract_phone(text),
        'years_experience': extract_years_experience(text),
        'position': extract_position(text),
        'location': extract_location(text)
    }
    return {k: v for k, v in info.items() if v is not None}

def save_conversation(conversation_history: List[Dict], candidate_info: Dict) -> str:
    """Save conversation history to a CSV file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"conversation_{timestamp}.csv"
    
    # Convert conversation history to DataFrame
    df = pd.DataFrame(conversation_history)
    
    # Add candidate info
    for key, value in candidate_info.items():
        df[key] = value
    
    # Save to CSV
    df.to_csv(filename, index=False)
    return filename

def is_conversation_ending(text: str) -> bool:
    """Check if the text indicates the conversation should end."""
    ending_phrases = [
        'exit', 'quit', 'bye', 'goodbye', 'end', 'stop',
        'thank you', 'thanks', 'that\'s all', 'that is all'
    ]
    return any(phrase in text.lower() for phrase in ending_phrases)

def format_tech_stack(tech_stack: str) -> List[str]:
    """Format tech stack string into a list of technologies."""
    # Split by common delimiters
    tech_list = re.split(r'[,;]|\band\b', tech_stack)
    
    # Clean up each technology
    tech_list = [tech.strip().lower() for tech in tech_list]
    
    # Remove empty strings and duplicates
    tech_list = list(set(filter(None, tech_list)))
    
    return tech_list 