from oscal_clpy.utils import JavaRuntimeContext
import pytest

class TestJavaRuntimeContext:
    def test_exec_good(self):
        jrc = JavaRuntimeContext()
        assert jrc.version == 17
        assert jrc.vm.version == '17+35-2724'
        assert jrc.runtime.version == jrc.vm.version
        assert jrc.is_valid == True

    def test_exec_bad(self):
        jrc = JavaRuntimeContext(cmd=['java', '-no-such-arg'])        
        assert jrc.version == None
        assert jrc.vm.version == None
        assert jrc.runtime.version == None
        assert jrc.is_valid == False

    def test_string_wellformed(self):
        jrc = JavaRuntimeContext(
            version='openjdk version "17" 2021-09-14\nOpenJDK Runtime Environment (build 17+35-2724)\nOpenJDK 64-Bit Server VM (build 17+35-2724, mixed mode, sharing)\n'
        )
        assert jrc.version == 17
        assert jrc.vm.version == '17+35-2724'
        assert jrc.runtime.version == jrc.vm.version
        assert jrc.is_valid == True

    def test_string_malformed(self):
        jrc = JavaRuntimeContext(
            version='openjdk version 100 bad format'
        )
        assert jrc.version == None
        assert jrc.vm.version == None
        assert jrc.runtime.version == None
        assert jrc.is_valid == False
