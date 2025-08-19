"""
Tests for the CLI module.

This module tests the argparse-based CLI functionality.
"""

import pytest
from unittest.mock import patch, MagicMock
import sys
from io import StringIO

from wt_tools.cli import (
    create_session,
    attach_session,
    new_window,
    goto_window,
    close_window,
    list_sessions,
    list_windows,
    main
)


class TestCLI:
    """Test cases for CLI functionality."""
    
    @patch('wt_tools.cli.libtmux.Server')
    def test_create_session_new(self, mock_server):
        """Test creating a new session."""
        # Mock server and session
        mock_server_instance = MagicMock()
        mock_server.return_value = mock_server_instance
        mock_server_instance.find_where.return_value = None
        mock_session = MagicMock()
        mock_server_instance.new_session.return_value = mock_session
        
        # Test function
        create_session("test_session")
        
        # Verify calls
        mock_server_instance.find_where.assert_called_once_with({"session_name": "test_session"})
        mock_server_instance.new_session.assert_called_once_with(session_name="test_session", attach=True)
    
    @patch('wt_tools.cli.libtmux.Server')
    def test_create_session_exists(self, mock_server):
        """Test creating a session that already exists."""
        # Mock server and existing session
        mock_server_instance = MagicMock()
        mock_server.return_value = mock_server_instance
        mock_existing_session = MagicMock()
        mock_server_instance.find_where.return_value = mock_existing_session
        
        # Test function
        create_session("existing_session")
        
        # Verify calls
        mock_server_instance.find_where.assert_called_once_with({"session_name": "existing_session"})
        mock_existing_session.attach_session.assert_called_once()
    
    @patch('wt_tools.cli.libtmux.Server')
    def test_attach_session_exists(self, mock_server):
        """Test attaching to an existing session."""
        # Mock server and session
        mock_server_instance = MagicMock()
        mock_server.return_value = mock_server_instance
        mock_session = MagicMock()
        mock_server_instance.find_where.return_value = mock_session
        
        # Test function
        attach_session("test_session")
        
        # Verify calls
        mock_server_instance.find_where.assert_called_once_with({"session_name": "test_session"})
        mock_session.attach_session.assert_called_once()
    
    @patch('wt_tools.cli.libtmux.Server')
    def test_attach_session_not_found(self, mock_server):
        """Test attaching to a non-existent session."""
        # Mock server
        mock_server_instance = MagicMock()
        mock_server.return_value = mock_server_instance
        mock_server_instance.find_where.return_value = None
        mock_server_instance.sessions = [MagicMock(session_name="other_session")]
        
        # Test function should exit
        with pytest.raises(SystemExit):
            attach_session("nonexistent_session")
    
    @patch('wt_tools.cli.libtmux.Server')
    def test_new_window(self, mock_server):
        """Test creating a new window."""
        # Mock server and session
        mock_server_instance = MagicMock()
        mock_server.return_value = mock_server_instance
        mock_session = MagicMock()
        mock_server_instance.get_current_session.return_value = mock_session
        mock_window = MagicMock()
        mock_window.window_name = "new_window"
        mock_window.window_index = 2
        mock_session.new_window.return_value = mock_window
        
        # Test function
        new_window()
        
        # Verify calls
        mock_server_instance.get_current_session.assert_called_once()
        mock_session.new_window.assert_called_once()
    
    @patch('wt_tools.cli.libtmux.Server')
    def test_new_window_no_session(self, mock_server):
        """Test creating a window when not in a tmux session."""
        # Mock server
        mock_server_instance = MagicMock()
        mock_server.return_value = mock_server_instance
        mock_server_instance.get_current_session.return_value = None
        
        # Test function should exit
        with pytest.raises(SystemExit):
            new_window()
    
    @patch('wt_tools.cli.libtmux.Server')
    def test_goto_window(self, mock_server):
        """Test going to a specific window."""
        # Mock server and session
        mock_server_instance = MagicMock()
        mock_server.return_value = mock_server_instance
        mock_session = MagicMock()
        mock_server_instance.get_current_session.return_value = mock_session
        mock_window = MagicMock()
        mock_window.window_name = "target_window"
        mock_session.find_where.return_value = mock_window
        
        # Test function
        goto_window(3)
        
        # Verify calls
        mock_server_instance.get_current_session.assert_called_once()
        mock_session.find_where.assert_called_once_with({"window_index": 3})
        mock_window.select_window.assert_called_once()
    
    @patch('wt_tools.cli.libtmux.Server')
    def test_goto_window_not_found(self, mock_server):
        """Test going to a non-existent window."""
        # Mock server and session
        mock_server_instance = MagicMock()
        mock_server.return_value = mock_server_instance
        mock_session = MagicMock()
        mock_server_instance.get_current_session.return_value = mock_session
        mock_session.find_where.return_value = None
        mock_session.windows = [MagicMock(window_index=1, window_name="window1")]
        
        # Test function should exit
        with pytest.raises(SystemExit):
            goto_window(99)
    
    @patch('wt_tools.cli.libtmux.Server')
    def test_close_window(self, mock_server):
        """Test closing a window."""
        # Mock server and session
        mock_server_instance = MagicMock()
        mock_server.return_value = mock_server_instance
        mock_session = MagicMock()
        mock_server_instance.get_current_session.return_value = mock_session
        mock_session.windows = [MagicMock(), MagicMock()]  # Multiple windows
        mock_window = MagicMock()
        mock_window.window_name = "test_window"
        mock_window.window_index = 1
        mock_session.get_current_window.return_value = mock_window
        
        # Test function
        close_window()
        
        # Verify calls
        mock_server_instance.get_current_session.assert_called_once()
        mock_session.get_current_window.assert_called_once()
        mock_window.kill_window.assert_called_once()
    
    @patch('wt_tools.cli.libtmux.Server')
    def test_list_sessions(self, mock_server):
        """Test listing sessions."""
        # Mock server and sessions
        mock_server_instance = MagicMock()
        mock_server.return_value = mock_server_instance
        mock_session1 = MagicMock(session_name="session1", attached=True)
        mock_session2 = MagicMock(session_name="session2", attached=False)
        mock_server_instance.sessions = [mock_session1, mock_session2]
        
        # Test function
        list_sessions()
        
        # Verify server was accessed
        mock_server.assert_called_once()
    
    @patch('wt_tools.cli.libtmux.Server')
    def test_list_windows(self, mock_server):
        """Test listing windows."""
        # Mock server and session
        mock_server_instance = MagicMock()
        mock_server.return_value = mock_server_instance
        mock_session = MagicMock()
        mock_session.session_name = "test_session"
        mock_server_instance.get_current_session.return_value = mock_session
        mock_window1 = MagicMock(window_index=1, window_name="window1", window_active=True)
        mock_window2 = MagicMock(window_index=2, window_name="window2", window_active=False)
        mock_session.windows = [mock_window1, mock_window2]
        
        # Test function
        list_windows()
        
        # Verify calls
        mock_server_instance.get_current_session.assert_called_once()


class TestMainCLI:
    """Test cases for the main CLI function."""
    
    @patch('sys.argv', ['wt', '--help'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_help(self, mock_stdout):
        """Test main function with help argument."""
        with pytest.raises(SystemExit):
            main()
        
        output = mock_stdout.getvalue()
        assert "wt-tools - Tmux session and window management utilities" in output
    
    @patch('sys.argv', ['wt', 'session', '--help'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_session_help(self, mock_stdout):
        """Test main function with session help."""
        with pytest.raises(SystemExit):
            main()
        
        output = mock_stdout.getvalue()
        assert "Session commands" in output
    
    @patch('sys.argv', ['wt', 'window', '--help'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_window_help(self, mock_stdout):
        """Test main function with window help."""
        with pytest.raises(SystemExit):
            main()
        
        output = mock_stdout.getvalue()
        assert "Window commands" in output
    
    @patch('wt_tools.cli.list_sessions')
    @patch('sys.argv', ['wt', 'session', 'list'])
    def test_main_session_list(self, mock_list_sessions):
        """Test main function with session list command."""
        main()
        mock_list_sessions.assert_called_once()
    
    @patch('wt_tools.cli.list_windows')
    @patch('sys.argv', ['wt', 'window', 'list'])
    def test_main_window_list(self, mock_list_windows):
        """Test main function with window list command."""
        main()
        mock_list_windows.assert_called_once()
