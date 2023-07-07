from oscal_clpy.runtime import JavaRuntime
import pytest

class TestJavaRuntime:
    def test_jvm_start(self):
        jvm = JavaRuntime()
        from java.lang import System
        assert 'gov.nist.secauto.oscal.tools.oscal-cli.cli-core-0.3.3.jar' in System.getProperty('java.class.path')
        jvm.stop()
