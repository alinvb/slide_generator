"""
executive_search.py - Automatic Executive/Management Team Search and Population
Provides functionality to automatically search for and populate executive profiles
"""

import re
from typing import Dict, List, Optional, Tuple
import json
from datetime import datetime

class ExecutiveSearchEngine:
    """
    Automated executive search and profile generation system
    Integrates with external data sources to populate management team slides
    """
    
    def __init__(self):
        self.executive_titles = [
            'CEO', 'Chief Executive Officer', 'President',
            'CFO', 'Chief Financial Officer',
            'COO', 'Chief Operating Officer', 
            'CRO', 'Chief Risk Officer',
            'CTO', 'Chief Technology Officer',
            'CDO', 'Chief Digital Officer',
            'CHRO', 'Chief Human Resources Officer',
            'General Counsel', 'Chief Legal Officer',
            'Managing Director', 'Executive Director',
            'Head of', 'VP', 'Vice President'
        ]
        
        self.company_data_cache = {}
    
    def extract_executive_names_from_text(self, text: str) -> List[Dict]:
        """
        Extract executive names and titles from provided text/research
        Enhanced to handle structured research format
        """
        executives = []
        
        # First try to parse structured format (like Arab Bank research)
        structured_execs = self._parse_structured_executive_text(text)
        if structured_execs:
            executives.extend(structured_execs)
        
        # Also try paragraph-based parsing for additional coverage
        paragraphs = text.split('\n\n')
        
        for paragraph in paragraphs:
            # Look for title patterns
            for title in self.executive_titles:
                if title.lower() in paragraph.lower():
                    # Found executive title, try to extract name and details
                    exec_data = self._parse_executive_paragraph(paragraph, title)
                    if exec_data and not self._is_duplicate_executive(exec_data, executives):
                        executives.append(exec_data)
                        break
        
        return executives
    
    def _parse_structured_executive_text(self, text: str) -> List[Dict]:
        """
        Parse structured executive research text like Arab Bank format
        """
        executives = []
        lines = text.split('\n')
        
        current_executive = None
        collecting_bullets = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if this line is an executive title
            is_executive_title = False
            for title in self.executive_titles:
                if title.lower() in line.lower() and len(line) < 100:
                    is_executive_title = True
                    
                    # Save previous executive if we have one
                    if current_executive and current_executive.get('experience_bullets'):
                        executives.append(current_executive)
                    
                    # Start new executive
                    current_executive = {
                        'title': line,
                        'role_title': line,
                        'name': self._extract_name_from_title(line),
                        'role': title,
                        'experience_bullets': [],
                        'years_experience': self._extract_experience_years(line),
                        'education': [],
                        'previous_roles': []
                    }
                    collecting_bullets = True
                    break
            
            # If we're collecting bullets and this isn't a title, add as experience
            if collecting_bullets and not is_executive_title and current_executive:
                if len(line) > 20:  # Meaningful content
                    # Extract years of experience if found
                    years_exp = self._extract_experience_years(line)
                    if years_exp != "Extensive experience":
                        current_executive['years_experience'] = years_exp
                    
                    # Extract education
                    education = self._extract_education(line)
                    if education:
                        current_executive['education'].extend(education)
                    
                    # Extract previous roles
                    prev_roles = self._extract_previous_roles(line)
                    if prev_roles:
                        current_executive['previous_roles'].extend(prev_roles)
                    
                    # Add as experience bullet
                    if not line.endswith('.'):
                        line += '.'
                    current_executive['experience_bullets'].append(line)
        
        # Don't forget the last executive
        if current_executive and current_executive.get('experience_bullets'):
            executives.append(current_executive)
        
        return executives
    
    def _is_duplicate_executive(self, new_exec: Dict, existing_execs: List[Dict]) -> bool:
        """
        Check if this executive is already in the list
        """
        new_title = new_exec.get('title', '').lower()
        new_role = new_exec.get('role', '').lower()
        
        for existing in existing_execs:
            existing_title = existing.get('title', '').lower()
            existing_role = existing.get('role', '').lower()
            
            # Check for similarity in titles or roles
            if (new_title in existing_title or existing_title in new_title or
                new_role == existing_role):
                return True
        
        return False
    
    def _parse_executive_paragraph(self, paragraph: str, title: str) -> Optional[Dict]:
        """
        Parse a paragraph to extract executive information
        Enhanced to handle detailed research format like Arab Bank data
        """
        lines = paragraph.split('\n')
        
        # Look for the title line
        title_line = None
        title_line_idx = -1
        
        for i, line in enumerate(lines):
            line_clean = line.strip()
            if title.lower() in line_clean.lower():
                title_line = line_clean
                title_line_idx = i
                break
        
        if not title_line:
            return None
        
        # Extract all content after the title line as experience bullets
        experience_bullets = []
        
        # Get all lines after the title
        content_lines = lines[title_line_idx + 1:] if title_line_idx >= 0 else lines
        
        for line in content_lines:
            line = line.strip()
            if line and len(line) > 15:  # Skip very short lines
                # Clean up the line
                if line.endswith('.'):
                    experience_bullets.append(line)
                elif len(line) > 30:  # Long descriptive lines even without period
                    experience_bullets.append(line + '.')
        
        # If we didn't get enough bullets from the structured approach, 
        # try to extract from the whole paragraph
        if len(experience_bullets) < 2:
            # Split paragraph into sentences and filter meaningful ones
            sentences = []
            for sentence in paragraph.split('.'):
                sentence = sentence.strip()
                if (len(sentence) > 20 and 
                    not sentence.lower().startswith(title.lower()) and
                    any(keyword in sentence.lower() for keyword in 
                        ['experience', 'responsible', 'leads', 'oversees', 'previously', 
                         'background', 'developed', 'expert', 'holds', 'years'])):
                    sentences.append(sentence + '.')
            
            if sentences:
                experience_bullets = sentences[:5]
        
        # Create executive profile
        executive = {
            'title': title,
            'role_title': title,  # Add role_title for slide compatibility
            'name': self._extract_name_from_title(title_line),
            'role': title,
            'experience_bullets': experience_bullets[:5],  # Limit to 5 bullets
            'years_experience': self._extract_experience_years(paragraph),
            'education': self._extract_education(paragraph),
            'previous_roles': self._extract_previous_roles(paragraph)
        }
        
        return executive
    
    def _extract_name_from_title(self, title_line: str) -> str:
        """
        Try to extract name from title line (often not available in research)
        """
        # Remove common title words
        name_line = title_line
        for title in self.executive_titles:
            name_line = re.sub(rf'\b{title}\b', '', name_line, flags=re.IGNORECASE)
        
        # Clean up and return
        name_line = re.sub(r'[–—-]+', '', name_line).strip()
        name_line = re.sub(r'\s+', ' ', name_line).strip()
        
        # If we get a reasonable name, return it; otherwise use role
        if len(name_line) > 2 and len(name_line) < 50:
            return name_line
        else:
            return "Executive Name"  # Placeholder when name not found
    
    def _extract_experience_years(self, text: str) -> str:
        """
        Extract years of experience from text
        """
        # Look for patterns like "25+ years", "20+ years experience", etc.
        patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'(\d+)\+?\s*years?\s*in',
            r'(\d+)\+?\s*years?'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return f"{match.group(1)}+ years"
        
        return "Extensive experience"
    
    def _extract_education(self, text: str) -> List[str]:
        """
        Extract education information from text
        """
        education = []
        
        # Common education patterns
        edu_patterns = [
            r'MBA\b',
            r'CPA\b',
            r'LLM\b',
            r'Bachelor',
            r'Master',
            r'PhD',
            r'degree[s]?\s+in\s+([^.]+)',
            r'Certified\s+([^.]+)'
        ]
        
        for pattern in edu_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                education.append(match.group(0))
        
        return education[:3]  # Limit to 3 items
    
    def _extract_previous_roles(self, text: str) -> List[str]:
        """
        Extract previous roles and companies
        """
        roles = []
        
        # Look for "Previously" patterns
        prev_patterns = [
            r'Previously\s+([^.]+)\.',
            r'Former\s+([^.]+)\.',
            r'Served\s+as\s+([^.]+)\.',
        ]
        
        for pattern in prev_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                roles.append(match.group(1).strip())
        
        return roles[:3]  # Limit to 3 previous roles
    
    def auto_populate_management_team(self, company_name: str, research_text: str = None) -> Dict:
        """
        Automatically populate management team slide data
        """
        executives = []
        
        if research_text:
            # Extract from provided research
            executives = self.extract_executive_names_from_text(research_text)
        
        if not executives:
            # Generate template executives if no data found
            executives = self._generate_template_executives(company_name)
        
        # Split into left and right columns (balanced distribution)
        mid_point = len(executives) // 2
        
        return {
            'title': f'{company_name} - Senior Management Team',
            'left_column_profiles': executives[:mid_point] if mid_point > 0 else executives[:3],
            'right_column_profiles': executives[mid_point:] if mid_point > 0 else executives[3:],
            'total_executives': len(executives),
            'last_updated': datetime.now().strftime('%Y-%m-%d'),
            'source': 'auto_generated' if not research_text else 'research_provided'
        }
    
    def _generate_template_executives(self, company_name: str) -> List[Dict]:
        """
        Generate template executive profiles when no data is available
        """
        template_executives = [
            {
                'title': 'Chief Executive Officer',
                'name': 'CEO Name',
                'role': 'CEO',
                'experience_bullets': [
                    f'Leads overall strategy and operations for {company_name}',
                    '20+ years of executive leadership experience',
                    'Proven track record in driving growth and operational excellence',
                    'Previously held senior roles at leading industry companies',
                    'Advanced degree in business or related field'
                ],
                'years_experience': '20+ years',
                'education': ['MBA', 'Bachelor\'s Degree'],
                'previous_roles': ['Senior executive roles at industry leaders']
            },
            {
                'title': 'Chief Financial Officer',
                'name': 'CFO Name', 
                'role': 'CFO',
                'experience_bullets': [
                    'Oversees all financial planning and analysis',
                    'Extensive experience in financial management and reporting',
                    'Led multiple capital raising and M&A transactions',
                    'Strong background in investor relations',
                    'CPA certification and advanced finance education'
                ],
                'years_experience': '15+ years',
                'education': ['CPA', 'MBA'],
                'previous_roles': ['Finance leadership at public companies']
            },
            {
                'title': 'Chief Operating Officer',
                'name': 'COO Name',
                'role': 'COO', 
                'experience_bullets': [
                    'Responsible for day-to-day operations and execution',
                    'Expert in operational efficiency and process optimization',
                    'Led digital transformation initiatives',
                    'Strong background in technology and operations',
                    'Proven ability to scale operations globally'
                ],
                'years_experience': '18+ years',
                'education': ['MBA', 'Engineering Degree'],
                'previous_roles': ['Operations leadership roles']
            }
        ]
        
        return template_executives

def enhance_management_team_with_search(company_name: str, research_data: str = None) -> Dict:
    """
    Enhanced function to automatically populate management team data
    """
    search_engine = ExecutiveSearchEngine()
    return search_engine.auto_populate_management_team(company_name, research_data)

# Integration function for slide generation
def auto_generate_management_data(company_name: str, provided_research: str = None) -> Dict:
    """
    Main integration function for automatic management team data generation
    """
    print(f"[EXECUTIVE SEARCH] Auto-generating management team data for {company_name}")
    
    if provided_research:
        print(f"[EXECUTIVE SEARCH] Using provided research data ({len(provided_research)} characters)")
    else:
        print(f"[EXECUTIVE SEARCH] No research provided, generating template data")
    
    return enhance_management_team_with_search(company_name, provided_research)