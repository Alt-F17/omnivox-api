"""Data models for MIO (Internal Messaging)."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class MioPreview:
    """
    Represents a preview of a message in MIO inbox.
    
    Reference: omnivox-crawler/src/types/mio/MioPreview.ts
    """
    id: str                     # Message ID
    author: str                 # Sender name
    title: str                  # Message subject
    short_desc: str             # Message preview text
    
    def __repr__(self) -> str:
        return f"MioPreview(from='{self.author}', title='{self.title}')"


@dataclass
class Mio:
    """
    Represents a complete message in MIO.
    
    Reference: omnivox-crawler/src/types/mio/Mio.ts
    """
    id: str                     # Message ID
    author: str                 # Sender name
    recipient: str              # Recipient name(s)
    title: str                  # Message subject
    date: str                   # Date sent
    content: str                # Message body
    
    def __repr__(self) -> str:
        return f"Mio(from='{self.author}', title='{self.title}', date='{self.date}')"


@dataclass
class SearchUser:
    """
    Represents a user from MIO search results.
    
    Reference: omnivox-crawler/src/types/SearchUser.ts
    """
    numero: str                             # Student/user ID
    titre: str                              # User name
    username: str                           # Username
    type_item_selectionne: int              # User type (3 = student)
    type_item_string: str                   # User type string (e.g., "Etudiant")
    
    # Optional fields from search
    description: Optional[str] = None
    nb_etudiants: int = 0
    nb_enseignants: int = 0
    nb_individus: int = 0
    
    def __repr__(self) -> str:
        return f"SearchUser('{self.titre}', {self.type_item_string})"
    
    @classmethod
    def from_api_response(cls, data: dict) -> 'SearchUser':
        """
        Create SearchUser from API response data.
        
        Args:
            data: Dictionary from Omnivox API
            
        Returns:
            SearchUser object
        """
        return cls(
            numero=data.get('Numero', ''),
            titre=data.get('Titre', ''),
            username=data.get('Username', ''),
            type_item_selectionne=data.get('TypeItemSelectionne', 0),
            type_item_string=data.get('TypeItemString', ''),
            description=data.get('Description'),
            nb_etudiants=data.get('NbEtudiants', 0),
            nb_enseignants=data.get('NbEnseignants', 0),
            nb_individus=data.get('NbIndividus', 0),
        )
