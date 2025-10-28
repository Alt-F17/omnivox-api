"""MIO Manager for accessing Internal Messaging data."""

import re
import requests
from bs4 import BeautifulSoup
from typing import Optional

from ..exceptions import NetworkError, ParsingError, NotFoundError
from ..utils import decode_html_entities, remove_extra_whitespace
from .models import Mio, MioPreview, SearchUser


class MioManager:
    """
    Manager for MIO (Internal Messaging) operations.
    
    Provides methods to:
    - Get message previews
    - Get full message content
    - Search for users
    - Send messages
    
    Reference: omnivox-crawler/src/managers/MioManager.ts
    """
    
    BASE_URL = "https://dawsoncollege.omnivox.ca"
    MIO_URL = f"{BASE_URL}/WebApplication/Module.MIOE"
    MIO_LOGIN_URL = f"{MIO_URL}/Login.aspx?ReturnUrl=%2fWebApplication%2fModule.MIOE%2fDefault.aspx"
    MIO_LIST_URL = f"{MIO_URL}/Commun/Message/MioListe.aspx"
    MIO_DETAIL_URL = f"{MIO_URL}/Commun/Message/MioDetail.aspx"
    
    def __init__(self, session: requests.Session):
        """
        Initialize MIO Manager.
        
        Args:
            session: Authenticated requests session
        """
        self.session = session
        self._cached_messages: dict[str, Mio] = {}
        self._initialize()
    
    def _initialize(self):
        """
        Initialize MIO session by getting required cookies.
        
        Reference: omnivox-crawler/src/modules/MioCookie.ts
        """
        try:
            # Get MIO authentication cookies
            self.session.get(self.MIO_LOGIN_URL)
        except requests.RequestException as e:
            raise NetworkError(f"Failed to initialize MIO session: {str(e)}")
    
    def get_message_previews(self) -> list[MioPreview]:
        """
        Get list of message previews (inbox).
        
        Returns:
            List of MioPreview objects (up to 50 recent messages)
            
        Reference: archive/omnivox-crawler/src/modules/Mio.ts
        """
        try:
            response = self.session.get(self.MIO_LIST_URL)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            previews = []
            
            # Extract message IDs from checkboxes (pattern: chk + 37 chars)
            # TypeScript: let idRegex: RegExp = new RegExp("chk.{37}", 'gm');
            # ids = [...request.data.matchAll(idRegex)].map(match => match[0].substring(3));
            id_pattern = re.compile(r'chk.{37}', re.IGNORECASE | re.MULTILINE)
            id_matches = id_pattern.findall(response.text)
            ids = [match[3:] for match in id_matches]  # Remove "chk" prefix (first 3 chars)
            
            # Extract authors
            authors = [elem.get_text(strip=True) for elem in soup.select('.name')]
            
            # Extract titles
            title_divs = soup.select('.lsTdTitle > div > em')
            titles = [elem.get_text(strip=True) for elem in title_divs]
            
            # Extract short descriptions
            desc_divs = soup.select('.lsTdTitle > div')
            short_descs = [remove_extra_whitespace(elem.get_text(strip=True)) for elem in desc_divs]
            
            # Combine into MioPreview objects
            # TypeScript loop: for (let i = 0; i < ids[i].length; i++)
            # This looks like a bug in TS (should be ids.length), but we'll match the intent
            for i in range(min(len(ids), len(authors), len(titles), len(short_descs))):
                previews.append(MioPreview(
                    id=ids[i],
                    author=authors[i],
                    title=titles[i],
                    short_desc=short_descs[i]
                ))
            
            return previews
            
        except requests.RequestException as e:
            raise NetworkError(f"Failed to fetch message previews: {str(e)}")
    
    def get_message_by_id(self, message_id: str) -> Mio:
        """
        Get full message content by ID.
        
        Args:
            message_id: Message ID (UUID format)
            
        Returns:
            Mio object with full message content
            
        Raises:
            NotFoundError: If message not found
            
        Reference: archive/omnivox-crawler/src/modules/MioDetail.ts
        """
        # Check cache first
        if message_id in self._cached_messages:
            return self._cached_messages[message_id]
        
        try:
            url = f"{self.MIO_DETAIL_URL}?m={message_id}"
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Check if message exists
            # TypeScript: if (!contenuWrapper) { throw new Error("mio not found") };
            content_wrapper = soup.select_one('#contenuWrapper')
            if not content_wrapper:
                raise NotFoundError(f"Message {message_id} not found")
            
            # Extract message content
            # TypeScript: let messageBody = root.querySelector("#contenuWrapper")!.text;
            #             messageBody = removeSpaces(messageBody);
            content = content_wrapper.get_text(strip=True)
            content = remove_extra_whitespace(content)
            
            # Extract metadata - TypeScript uses .textContent for these
            # const from: string = root.querySelector(".cDe")!.textContent;
            from_elem = soup.select_one('.cDe')
            to_elem = soup.select_one('#tdACont')
            title_elem = soup.select_one('.cSujet')
            date_elem = soup.select_one('.cDate')
            
            mio = Mio(
                id=message_id,
                author=from_elem.get_text(strip=True) if from_elem else "",
                recipient=to_elem.get_text(strip=True) if to_elem else "",
                title=title_elem.get_text(strip=True) if title_elem else "",
                date=date_elem.get_text(strip=True) if date_elem else "",
                content=content
            )
            
            # Cache the message
            self._cached_messages[message_id] = mio
            return mio
            
        except requests.RequestException as e:
            raise NetworkError(f"Failed to fetch message: {str(e)}")
    
    def search_users(self, name: str) -> list[SearchUser]:
        """
        Search for users by name.
        
        Args:
            name: Name to search for
            
        Returns:
            List of SearchUser objects
            
        Note: This method is incomplete in the TypeScript version.
              Full implementation requires getting search token first.
              
        Reference: omnivox-crawler/src/modules/mio/MioSearchUser.ts
        """
        # TODO: Implement user search
        # Requires:
        # 1. Get compose page token (MioGetCompose)
        # 2. Get search panel cookie (MioGetSearchPanelCookie)
        # 3. Get search panel token (MioGetSearchPanel)
        # 4. Search with token (MioSearchUser)
        raise NotImplementedError("User search not yet implemented")
    
    def send_message(self, recipients: list[SearchUser], title: str, message: str):
        """
        Send a message to users.
        
        Args:
            recipients: List of SearchUser objects to send to
            title: Message subject
            message: Message body
            
        Note: This method is incomplete in the TypeScript version.
              Full implementation requires multiple API calls.
              
        Reference: omnivox-crawler/src/modules/mio/MioSend.ts
        """
        # TODO: Implement message sending
        # Requires:
        # 1. Get compose form parameters (MioGetCompose)
        # 2. Add each recipient (MioAddUserAsRecipient)
        # 3. Save recipients (MioSaveRecipient)
        # 4. Send message (MioSend)
        raise NotImplementedError("Message sending not yet implemented")
