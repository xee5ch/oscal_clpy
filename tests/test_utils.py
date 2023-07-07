from oscal_clpy.utils import JavaRuntimeContext
import pytest
from unittest.mock import mock_open, patch, MagicMock

class TestJavaRuntimeContext:
    @patch('oscal_clpy.utils.check_output')
    def test_exec_good(self, mock_check_output):
        mock_check_output.return_value = (
            b'openjdk "99" 3000-01-01\n'
            b'OpenJDK Runtime Environment (build 99+10-1234)\n'
            b'OpenJDK 64-Bit Server VM (build 99+10-1234, mixed mode, sharing)\n'
        )
        jvm_context = JavaRuntimeContext()
        assert jvm_context.version == 99
        assert jvm_context.vm.version == '99+10-1234'
        assert jvm_context.runtime.version == jvm_context.vm.version
        assert jvm_context.is_valid == True

    @patch('oscal_clpy.utils.check_output')
    def test_exec_bad(self, mock_check_output):
        mock_check_output.return_value = (
            b'Unrecognized option: -bad-arg'
            b'Error: Could not create the Java Virtual Machine.'
            b'Error: A fatal exception has occurred. Program will exit.'
        )
        jvm_context = JavaRuntimeContext(cmd=['java', '-no-such-arg'])        
        assert jvm_context.version == None
        assert jvm_context.vm.version == None
        assert jvm_context.runtime.version == None
        assert jvm_context.is_valid == False

    def test_string_wellformed(self):
        jvm_context = JavaRuntimeContext(
            version=''.join([
                'openjdk "99" 3000-01-01\n',
                'OpenJDK Runtime Environment (build 99+10-1234)\n',
                'OpenJDK 64-Bit Server VM (build 99+10-1234, mixed mode, sharing)\n'
            ])
        )
        assert jvm_context.version == 99
        assert jvm_context.vm.version == '99+10-1234'
        assert jvm_context.runtime.version == jvm_context.vm.version
        assert jvm_context.is_valid == True

    def test_string_malformed(self):
        jvm_context = JavaRuntimeContext(
            version='openjdk version 100 bad format'
        )
        assert jvm_context.version == None
        assert jvm_context.vm.version == None
        assert jvm_context.runtime.version == None
        assert jvm_context.is_valid == False

    @patch('oscal_clpy.utils.check_output')
    def test_is_compatible_current(self, mock_check_output):
        mock_check_output.return_value = (
            b'openjdk version "17" 2021-09-14\n'
            b'OpenJDK Runtime Environment (build 17+35-2724)\n'
            b'OpenJDK 64-Bit Server VM (build 17+35-2724, mixed mode, sharing)\n'
        )
        jvm_context = JavaRuntimeContext()
        assert jvm_context.is_compatible == True

    @patch('oscal_clpy.utils.check_output')
    def test_is_compatible_future(self, mock_check_output):
        mock_check_output.return_value = (
            b'openjdk "99" 3000-01-01\n'
            b'OpenJDK Runtime Environment (build 99+10-1234)\n'
            b'OpenJDK 64-Bit Server VM (build 99+10-1234, mixed mode, sharing)\n'
        )
        jvm_context = JavaRuntimeContext()
        assert jvm_context.is_valid == True and jvm_context.is_compatible == True

    @patch('oscal_clpy.utils.check_output')
    def test_isnt_compatible(self, mock_check_output):
        mock_check_output.return_value = (
            b'openjdk version "11" 2018-09-25\n'
            b'OpenJDK Runtime Environment 18.9 (build 11+28)\n'
            b'OpenJDK 64-Bit Server VM 18.9 (build 11+28, mixed mode)\n'
        )
        jvm_context = JavaRuntimeContext()
        assert jvm_context.is_valid == True and jvm_context.is_compatible == False
