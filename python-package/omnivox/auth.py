"""Authentication module for Omnivox API."""

import requests
from bs4 import BeautifulSoup
from typing import Optional

from .exceptions import AuthenticationError, NetworkError
from .utils import extract_k_token


class OmnivoxAuth:
    """
    Handles authentication with Omnivox.
    
    This class manages the session and cookies required to interact with Omnivox.
    It uses the same authentication flow as the TypeScript implementation.
    
    Reference: omnivox-crawler/src/modules/Login.ts
    """
    
    BASE_URL = "https://dawsoncollege.omnivox.ca"
    LOGIN_URL = f"{BASE_URL}/intr/Module/Identification/Login/Login.aspx"
    
    def __init__(self):
        """Initialize authentication with a new session."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })
        self._authenticated = False
    
    def login(self, username: str, password: str) -> bool:
        """
        Authenticate with Omnivox.
        
        Args:
            username: Student ID
            password: Password
            
        Returns:
            True if login successful
            
        Raises:
            AuthenticationError: If login fails
            NetworkError: If network request fails
        """
        try:
            # Step 1: Get login page to extract 'k' token
            response = self.session.get(self.LOGIN_URL)
            response.raise_for_status()
            
            # Step 2: Extract hidden 'k' token from HTML
            k_token = extract_k_token(response.text)
            if not k_token:
                raise AuthenticationError("Could not extract authentication token from login page")
            
            # Step 3: Submit login credentials
            login_data = {
                'NoDa': username,
                'PasswordEtu': password,
                'k': k_token
            }
            
            response = self.session.post(
                self.LOGIN_URL,
                data=login_data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            response.raise_for_status()
            
            # Step 4: Check if login was successful
            # Successful login contains "headerNavbarLink" in the response
            if 'headerNavbarLink' in response.text:
                self._authenticated = True
                return True
            else:
                raise AuthenticationError("Invalid credentials")
                
        except requests.RequestException as e:
            raise NetworkError(f"Network error during login: {str(e)}")
    
    @property
    def is_authenticated(self) -> bool:
        """Check if currently authenticated."""
        return self._authenticated
    
    def get_session(self) -> requests.Session:
        """
        Get the authenticated session.
        
        Returns:
            requests.Session object with cookies
            
        Raises:
            AuthenticationError: If not authenticated
        """
        if not self._authenticated:
            raise AuthenticationError("Not authenticated. Call login() first.")
        return self.session
