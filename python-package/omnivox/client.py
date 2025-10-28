"""Main Omnivox API client."""

from .auth import OmnivoxAuth
from .lea.manager import LeaManager
from .mio.manager import MioManager
from .exceptions import AuthenticationError


class OmnivoxClient:
    """
    Main client for interacting with Omnivox.
    
    This class provides a simple interface to authenticate and access
    LEA (Learning Environment) and MIO (Internal Messaging) services.
    
    Example:
        >>> from omnivox import OmnivoxClient
        >>> 
        >>> # Initialize and login
        >>> client = OmnivoxClient("student_id", "password")
        >>> 
        >>> # Access LEA (courses)
        >>> classes = client.lea.get_all_classes()
        >>> for cls in classes:
        ...     print(f"{cls.code}: {cls.title} - {cls.grade}")
        >>> 
        >>> # Access MIO (messages)
        >>> messages = client.mio.get_message_previews()
        >>> for msg in messages:
        ...     print(f"From {msg.author}: {msg.title}")
    """
    
    def __init__(self, username: str, password: str):
        """
        Initialize Omnivox client and authenticate.
        
        Args:
            username: Student ID
            password: Password
            
        Raises:
            AuthenticationError: If login fails
            NetworkError: If connection fails
        """
        # Authenticate
        self._auth = OmnivoxAuth()
        success = self._auth.login(username, password)
        
        if not success:
            raise AuthenticationError("Failed to authenticate with Omnivox")
        
        # Get authenticated session
        session = self._auth.get_session()
        
        # Initialize managers
        self._lea = LeaManager(session)
        self._mio = MioManager(session)
    
    @property
    def lea(self) -> LeaManager:
        """
        Access LEA (Learning Environment) manager.
        
        Returns:
            LeaManager instance
        """
        return self._lea
    
    @property
    def mio(self) -> MioManager:
        """
        Access MIO (Internal Messaging) manager.
        
        Returns:
            MioManager instance
        """
        return self._mio
    
    @property
    def is_authenticated(self) -> bool:
        """Check if client is authenticated."""
        return self._auth.is_authenticated
