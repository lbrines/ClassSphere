"""
Test file for configuration setup verification

CRITICAL OBJECTIVES:
- Verify Python 3.11.4 is being used
- Verify FastAPI and Pydantic v2 are properly installed
- Verify project structure is correct

DEPENDENCIES:
- Python 3.11.4
- FastAPI 0.104.1
- Pydantic 2.5.0
"""

import pytest
import sys
from pathlib import Path

# BEGINNING: Critical tests for core functionality
def test_python_version():
    """Test that Python 3.11.4 is being used"""
    # Arrange & Act
    version = sys.version_info
    
    # Assert
    assert version.major == 3
    assert version.minor == 11
    assert version.micro == 4

def test_fastapi_import():
    """Test that FastAPI can be imported"""
    # Arrange & Act
    try:
        import fastapi
        from fastapi import FastAPI
        
        # Assert
        assert fastapi.__version__ == "0.104.1"
        assert FastAPI is not None
    except ImportError as e:
        pytest.fail(f"FastAPI import failed: {e}")

def test_pydantic_v2_import():
    """Test that Pydantic v2 can be imported"""
    # Arrange & Act
    try:
        import pydantic
        from pydantic import BaseModel
        
        # Assert
        assert pydantic.__version__ == "2.5.0"
        assert BaseModel is not None
    except ImportError as e:
        pytest.fail(f"Pydantic v2 import failed: {e}")

# MIDDLE: Detailed implementation tests
def test_project_structure():
    """Test that project structure is correct"""
    # Arrange
    base_path = Path(__file__).parent.parent.parent
    
    # Act & Assert: Check main directories exist
    assert (base_path / "src" / "app").exists()
    assert (base_path / "src" / "app" / "api").exists()
    assert (base_path / "src" / "app" / "core").exists()
    assert (base_path / "src" / "app" / "models").exists()
    assert (base_path / "src" / "app" / "services").exists()
    assert (base_path / "src" / "app" / "middleware").exists()
    assert (base_path / "tests" / "unit").exists()
    assert (base_path / "tests" / "integration").exists()
    assert (base_path / "tests" / "e2e").exists()

def test_requirements_file():
    """Test that requirements.txt exists and has correct content"""
    # Arrange
    base_path = Path(__file__).parent.parent.parent.parent
    
    # Act
    requirements_file = base_path / "requirements.txt"
    
    # Assert
    assert requirements_file.exists()
    
    with open(requirements_file, 'r') as f:
        content = f.read()
        assert "fastapi==0.104.1" in content
        assert "pydantic==2.5.0" in content
        assert "pytest==7.4.3" in content

# END: Verification and next steps
def test_uvicorn_import():
    """Test that uvicorn can be imported"""
    # Arrange & Act
    try:
        import uvicorn
        
        # Assert
        assert uvicorn.__version__ == "0.24.0"
    except ImportError as e:
        pytest.fail(f"Uvicorn import failed: {e}")

def test_redis_import():
    """Test that redis can be imported"""
    # Arrange & Act
    try:
        import redis
        
        # Assert
        assert redis.__version__ == "5.0.1"
    except ImportError as e:
        pytest.fail(f"Redis import failed: {e}")