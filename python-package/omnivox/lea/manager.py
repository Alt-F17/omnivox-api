"""LEA Manager for accessing Learning Environment data."""

import re
import requests
from bs4 import BeautifulSoup
from typing import Optional

from ..exceptions import NetworkError, ParsingError, NotFoundError
from ..utils import decode_html_entities, remove_extra_whitespace, safe_int, safe_float, parse_schedule
from .models import LeaClass, Document, Category, ClassDocumentSummary


class LeaManager:
    """
    Manager for LEA (Learning Environment) operations.
    
    Provides methods to:
    - Get all enrolled classes
    - Get class documents
    - Get document summaries
    
    Reference: omnivox-crawler/src/managers/LeaManager.ts
    """
    
    BASE_URL = "https://www-daw-ovx.omnivox.ca"
    LEA_URL = f"{BASE_URL}/cvir/doce/Default.aspx"
    LEA_COOKIE_URL = "https://dawsoncollege.omnivox.ca/intr/Module/ServicesExterne/Skytech.aspx?IdServiceSkytech=Skytech_Omnivox&lk=%2festd%2fcvie&IdService=CVIE&C=DAW&E=P&L=ANG"
    DOCUMENT_SUMMARY_URL = f"{BASE_URL}/cvir/ddle/SommaireDocuments.aspx"
    
    def __init__(self, session: requests.Session):
        """
        Initialize LEA Manager.
        
        Args:
            session: Authenticated requests session
        """
        self.session = session
        self._classes_cache: list[LeaClass] = []
        self._document_summary_cache: list[ClassDocumentSummary] = []
        self._initialize()
    
    def _initialize(self):
        """Initialize LEA session by getting required cookies."""
        try:
            # Get LEA authentication cookie
            # Reference: omnivox-crawler/src/modules/lea/LeaCookie.ts
            self.session.get(self.LEA_COOKIE_URL)
        except requests.RequestException as e:
            raise NetworkError(f"Failed to initialize LEA session: {str(e)}")
    
    def get_all_classes(self, force_refresh: bool = False) -> list[LeaClass]:
        """
        Get all enrolled classes.
        
        Args:
            force_refresh: If True, bypass cache and fetch fresh data
            
        Returns:
            List of LeaClass objects
            
        Reference: omnivox-crawler/src/modules/lea/Lea.ts
        """
        if self._classes_cache and not force_refresh:
            return self._classes_cache
        
        try:
            response = self.session.get(self.LEA_URL)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            classes = []
            
            # Find all class cards
            card_panels = soup.select('.card-panel')
            
            for card in card_panels:
                try:
                    cls = self._parse_class_card(card)
                    classes.append(cls)
                except Exception as e:
                    # Continue parsing other classes even if one fails
                    print(f"Warning: Failed to parse class card: {e}")
                    continue
            
            self._classes_cache = classes
            return classes
            
        except requests.RequestException as e:
            raise NetworkError(f"Failed to fetch classes: {str(e)}")
    
    def _parse_class_card(self, card) -> LeaClass:
        """
        Parse a class card from HTML.
        
        Args:
            card: BeautifulSoup element for class card
            
        Returns:
            LeaClass object
            
        Reference: omnivox-crawler/src/modules/lea/Lea.ts (lines 10-61)
        """
        # Extract code and title
        title_elem = card.select_one('.card-panel-title')
        if not title_elem:
            raise ParsingError("Could not find class title")
        
        code_title = title_elem.get_text(strip=True)
        
        # Split into code and title (there's a special space character)
        parts = code_title.split(maxsplit=1)
        code = parts[0] if parts else ""
        title = parts[1] if len(parts) > 1 else ""
        
        # Extract section, schedule, and teacher
        desc_elem = card.select_one('.card-panel-desc')
        if desc_elem:
            desc_text = desc_elem.get_text()
            
            # Parse section (between first "0" and " -")
            section_start = desc_text.find('0')
            section_end = desc_text.find(' -')
            section = desc_text[section_start:section_end].strip() if section_start != -1 and section_end != -1 else ""
            
            # Parse schedule (between "- " and last ", ")
            schedule_start = desc_text.find('- ') + 2
            schedule_end = desc_text.rfind(', ')
            schedule_text = desc_text[schedule_start:schedule_end] if schedule_start > 1 and schedule_end != -1 else ""
            schedule = parse_schedule(schedule_text)
            
            # Parse teacher (after last ", ")
            teacher = desc_text[schedule_end + 2:].strip() if schedule_end != -1 else ""
        else:
            section = ""
            schedule = []
            teacher = ""
        
        # Extract grades
        # Reference: archive/omnivox-crawler/src/modules/lea/Lea.ts lines 34-48
        notes = card.select('.note-principale')
        grade = None
        average = None
        median = None
        
        # Grade is always in notes[0]
        if len(notes) > 0:
            grade_text = notes[0].get_text(strip=True)
            # Check if grade is empty (" -  " with special whitespace character)
            # TS: if (grade == " -  ") { grade = undefined; }
            if grade_text and grade_text not in ['-', ' - ', ' -  ']:
                grade = grade_text
        
        # Average and median logic from TypeScript:
        # if (notes.length > 3) {
        #   average = parseInt(notes[2].text);
        #   median = parseInt(notes[3].text);
        # } else {
        #   average = parseInt(notes[1].text) || undefined;
        #   median = parseInt(notes[2].text) || undefined;
        # }
        if len(notes) > 3:
            average = safe_float(notes[2].get_text(strip=True))
            median = safe_float(notes[3].get_text(strip=True))
        elif len(notes) > 1:
            average = safe_float(notes[1].get_text(strip=True))
            if len(notes) > 2:
                median = safe_float(notes[2].get_text(strip=True))
        
        # Extract document/assignment counts
        files = card.select('.file-indicator-number')
        distributed_documents = safe_int(files[0].get_text(strip=True)) if len(files) > 0 else 0
        distributed_assignments = safe_int(files[1].get_text(strip=True)) if len(files) > 1 else 0
        
        return LeaClass(
            code=code,
            title=title,
            teacher=teacher,
            section=section,
            schedule=schedule,
            grade=grade,
            average=average,
            median=median,
            distributed_documents=distributed_documents,
            distributed_assignments=distributed_assignments
        )
    
    def get_class(
        self,
        teacher: Optional[str] = None,
        name: Optional[str] = None,
        code: Optional[str] = None
    ) -> Optional[LeaClass]:
        """
        Find a specific class by teacher, name, or code.
        
        Args:
            teacher: Teacher name to search for (partial match)
            name: Class name to search for (partial match)
            code: Class code to search for (exact match)
            
        Returns:
            LeaClass object if found, None otherwise
        """
        if not self._classes_cache:
            self.get_all_classes()
        
        if teacher:
            return next((c for c in self._classes_cache 
                        if teacher.upper() in c.teacher.upper()), None)
        if name:
            return next((c for c in self._classes_cache 
                        if name.upper() in c.title.upper()), None)
        if code:
            return next((c for c in self._classes_cache 
                        if c.code == code.upper()), None)
        
        return None
    
    def get_class_document_summary(self, force_refresh: bool = False) -> list[ClassDocumentSummary]:
        """
        Get document summary for all classes.
        
        Args:
            force_refresh: If True, bypass cache and fetch fresh data
            
        Returns:
            List of ClassDocumentSummary objects
            
        Reference: omnivox-crawler/src/modules/lea/LeaDocumentSummary.ts
        """
        if self._document_summary_cache and not force_refresh:
            return self._document_summary_cache
        
        try:
            response = self.session.get(self.DOCUMENT_SUMMARY_URL)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            summaries = []
            
            # Find all rows with class document info
            rows = soup.select('.itemDataGrid, .itemDataGridAltern')
            
            for row in rows:
                a_elem = row.select_one('a')
                if not a_elem:
                    continue
                
                name = a_elem.get_text(strip=True)
                href = a_elem.get('href', '')
                
                # Get available documents count (3rd td)
                tds = row.select('td')
                available_docs = tds[2].get_text(strip=True) if len(tds) > 2 else "0"
                
                summaries.append(ClassDocumentSummary(
                    name=name,
                    href=href,
                    available_documents=available_docs
                ))
            
            self._document_summary_cache = summaries
            return summaries
            
        except requests.RequestException as e:
            raise NetworkError(f"Failed to fetch document summary: {str(e)}")
    
    def get_class_documents_by_href(self, href: str) -> list[Category]:
        """
        Get documents for a specific class by href.
        
        Args:
            href: Relative URL to class documents page
            
        Returns:
            List of Category objects containing documents
            
        Reference: omnivox-crawler/src/modules/lea/LeaClassDocuments.ts
        """
        try:
            url = f"{self.BASE_URL}{href}"
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            categories = []
            
            # Find all document categories
            category_tables = soup.select('.CategorieDocumentEtudiant')
            
            for table in category_tables:
                documents = []
                
                # Parse each document row
                rows = table.select('tr')
                for row in rows:
                    name_elem = row.select_one('.lblTitreDocumentDansListe')
                    if not name_elem:
                        continue
                    
                    name = name_elem.get_text(strip=True)
                    
                    # Description cleaning: replace tabs, carriage returns, newlines with single newline
                    # TypeScript: let cleanRegex = RegExp("([\t\r\n]){1,}", "gm");
                    #             description = description.replace(cleanRegex, '\n');
                    desc_elem = row.select_one('.divDescriptionDocumentDansListe')
                    if desc_elem:
                        description = desc_elem.get_text(strip=True)
                        # Replace 1+ occurrences of tab/CR/LF with single newline
                        description = re.sub(r'[\t\r\n]+', '\n', description)
                    else:
                        description = ""
                    
                    # Posted date: TypeScript gets text after "since" 
                    # posted = document.querySelector(".DocDispo")!.text.substring("since".length);
                    posted_elem = row.select_one('.DocDispo')
                    if posted_elem:
                        posted_text = posted_elem.get_text(strip=True)
                        # Remove "since" prefix if present
                        posted = posted_text[len('since'):].strip() if posted_text.startswith('since') else posted_text
                    else:
                        posted = ""
                    
                    # Check if document has been viewed
                    # TypeScript: viewed = document.querySelector("#colonneEtoileVisualisation")!.childNodes.length == 1;
                    viewed_elem = row.select_one('#colonneEtoileVisualisation')
                    viewed = len(viewed_elem.contents) == 1 if viewed_elem else False
                    
                    documents.append(Document(
                        name=name,
                        description=description,
                        posted=posted,
                        viewed=viewed
                    ))
                
                # Get category name
                cat_name_elem = table.select_one('.boutonEnabled')
                category_name = cat_name_elem.get_text(strip=True) if cat_name_elem else "Not categorized"
                
                if documents:  # Only add category if it has documents
                    categories.append(Category(
                        name=category_name,
                        documents=documents
                    ))
            
            return categories
            
        except requests.RequestException as e:
            raise NetworkError(f"Failed to fetch class documents: {str(e)}")
