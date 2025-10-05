"""
Tests para Google OAuth Service
"""
import pytest
from unittest.mock import Mock, patch
from app.services.google_service import GoogleOAuthService


class TestGoogleOAuthService:
    """Tests para GoogleOAuthService"""
    
    def test_generate_pkce_challenge(self):
        """Test generación de PKCE challenge"""
        service = GoogleOAuthService()
        code_verifier, code_challenge = service.generate_pkce_challenge()
        
        assert isinstance(code_verifier, str)
        assert isinstance(code_challenge, str)
        assert len(code_verifier) >= 43
        assert len(code_challenge) >= 43
    
    def test_generate_pkce_challenge_uniqueness(self):
        """Test que los challenges son únicos"""
        service = GoogleOAuthService()
        
        challenge1 = service.generate_pkce_challenge()
        challenge2 = service.generate_pkce_challenge()
        
        assert challenge1[0] != challenge2[0]  # code_verifier
        assert challenge1[1] != challenge2[1]  # code_challenge
    
    @patch('app.services.google_service.Flow')
    def test_get_authorization_url(self, mock_flow):
        """Test obtención de URL de autorización"""
        # Mock del flow
        mock_flow_instance = Mock()
        mock_flow_instance.authorization_url.return_value = (
            "https://accounts.google.com/o/oauth2/auth?test=1",
            "test-state"
        )
        mock_flow.from_client_config.return_value = mock_flow_instance
        
        service = GoogleOAuthService()
        auth_url, code_verifier = service.get_authorization_url()
        
        assert isinstance(auth_url, str)
        assert isinstance(code_verifier, str)
        assert "accounts.google.com" in auth_url
        assert "oauth2" in auth_url
    
    @patch('app.services.google_service.Flow')
    def test_exchange_code_for_token_success(self, mock_flow):
        """Test intercambio exitoso de código por token"""
        # Mock del flow
        mock_flow_instance = Mock()
        mock_credentials = Mock()
        mock_flow_instance.fetch_token.return_value = None
        mock_flow_instance.credentials = mock_credentials
        mock_flow.from_client_config.return_value = mock_flow_instance
        
        service = GoogleOAuthService()
        result = service.exchange_code_for_token("test-code", "test-verifier")
        
        assert result == mock_credentials
        mock_flow_instance.fetch_token.assert_called_once_with(
            code="test-code",
            code_verifier="test-verifier"
        )
    
    @patch('app.services.google_service.Flow')
    def test_exchange_code_for_token_failure(self, mock_flow):
        """Test fallo en intercambio de código por token"""
        # Mock del flow que lanza excepción
        mock_flow_instance = Mock()
        mock_flow_instance.fetch_token.side_effect = Exception("Token exchange failed")
        mock_flow.from_client_config.return_value = mock_flow_instance
        
        service = GoogleOAuthService()
        result = service.exchange_code_for_token("test-code", "test-verifier")
        
        assert result is None
    
    @patch('googleapiclient.discovery.build')
    def test_get_user_info_success(self, mock_build):
        """Test obtención exitosa de información de usuario"""
        # Mock del servicio
        mock_service = Mock()
        mock_userinfo = Mock()
        mock_userinfo.get.return_value.execute.return_value = {
            'id': '123456789',
            'email': 'test@example.com',
            'name': 'Test User',
            'picture': 'https://example.com/pic.jpg',
            'verified_email': True
        }
        mock_service.userinfo.return_value = mock_userinfo
        mock_build.return_value = mock_service
        
        service = GoogleOAuthService()
        mock_credentials = Mock()
        result = service.get_user_info(mock_credentials)
        
        assert result is not None
        assert result['id'] == '123456789'
        assert result['email'] == 'test@example.com'
        assert result['name'] == 'Test User'
        assert result['verified_email'] is True
    
    @patch('googleapiclient.discovery.build')
    def test_get_user_info_failure(self, mock_build):
        """Test fallo en obtención de información de usuario"""
        # Mock del build que lanza excepción
        mock_build.side_effect = Exception("API call failed")
        
        service = GoogleOAuthService()
        mock_credentials = Mock()
        result = service.get_user_info(mock_credentials)
        
        assert result is None
    
    def test_refresh_token_success(self):
        """Test refresh exitoso de token"""
        service = GoogleOAuthService()
        
        # Mock credentials que necesitan refresh
        mock_credentials = Mock()
        mock_credentials.expired = True
        mock_credentials.refresh_token = "refresh-token"
        mock_credentials.refresh.return_value = None
        
        result = service.refresh_token(mock_credentials)
        
        assert result == mock_credentials
        mock_credentials.refresh.assert_called_once()
    
    def test_refresh_token_no_refresh_needed(self):
        """Test cuando no se necesita refresh"""
        service = GoogleOAuthService()
        
        # Mock credentials que no necesitan refresh
        mock_credentials = Mock()
        mock_credentials.expired = False
        
        result = service.refresh_token(mock_credentials)
        
        assert result == mock_credentials
        mock_credentials.refresh.assert_not_called()
    
    def test_refresh_token_failure(self):
        """Test fallo en refresh de token"""
        service = GoogleOAuthService()
        
        # Mock credentials que fallan al hacer refresh
        mock_credentials = Mock()
        mock_credentials.expired = True
        mock_credentials.refresh_token = "refresh-token"
        mock_credentials.refresh.side_effect = Exception("Refresh failed")
        
        result = service.refresh_token(mock_credentials)
        
        assert result is None
