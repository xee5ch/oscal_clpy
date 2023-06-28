from logging import getLogger
from dataclasses import dataclass
import re
from subprocess import check_output, STDOUT
from typing import IO, List, Optional

logger = getLogger(__name__)

@dataclass
class JavaRuntime:
    name: str | None = None
    version: str | None = None

@dataclass
class JavaVirtualMachine:
    name: str | None = None
    version: str | None = None
    info: str | None = None

class JavaRuntimeContext:
    def __init__(self, cmd=['java', '-version'], version=''):
        try:
            _version = version if version else check_output(cmd, stderr=STDOUT).decode()
            # https://openjdk.org/jeps/223#Launcher
            pattern = re.compile(
                r'([\w\s]+) "(\d+)" ([0-9]{4}-[0-9]{2}-[0-9]{2})\n'
                r'([\w\s]+) \(build ([0-9-+]+)\)\n'
                r'([\-\w\s]+) \(build ([0-9-+]+), ([,\w\s]+)\)\n'
            )
            result = re.search(pattern, _version)
            matches = result.groups()
            # Name indices for clarity
            prefix_index = 0
            version_index = 1
            # version_release_date_index = 2
            runtime_name_index = 3
            runtime_version_index = 4
            vm_name_index = 5
            vm_version_index = 6
            vm_info_index = 7         
            self.runtime = JavaRuntime()
            self.vm = JavaVirtualMachine()
            self.prefix = matches[prefix_index]
            self.version = int(matches[version_index])
            self.runtime = JavaRuntime(
                name=matches[runtime_name_index],
                version=matches[runtime_version_index]
            )
            self.vm = JavaVirtualMachine(
                name=matches[vm_name_index],
                version=matches[vm_version_index],
                info=matches[vm_info_index]
            )
            self.is_valid = True
        except:
            self.prefix = None
            self.version = None
            self.runtime = JavaRuntime()
            self.vm = JavaVirtualMachine()
            self.is_valid = False
