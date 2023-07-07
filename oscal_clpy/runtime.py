#!/usr/bin/env python3

import jpype as jpype
import jpype.imports as java_imports
import jpype.types as java_types
import typing
import os
from .types import _PathOrStr
from .utils import is_interactive


class JavaRuntime:
    def __init__(
        self,
        *jvmargs: str,
        jvmpath: typing.Optional[_PathOrStr] = jpype.getDefaultJVMPath(),
        classpath: typing.Optional[typing.Sequence[_PathOrStr]] = [f"{os.path.dirname(__file__)}/../vendor/lib/*"],
        ignoreUnrecognized: bool = False,
        convertStrings: bool = False,
        interrupt: bool = not is_interactive()
    ):
        self.jvmargs = jvmargs
        self.jvmpath = jvmpath
        self.classpath = classpath
        self.ignoreUnrecognized = ignoreUnrecognized
        self.convertStrings = convertStrings
        self.interrupt = interrupt

    def start(self):
        """Initialize a running Java Virtual Machine.
        """
        try:
            jpype.startJVM(
                classpath=self.classpath,
                ignoreUnrecognized=self.ignoreUnrecognized,
                convertStrings=self.convertStrings,
                interrupt=self.interrupt
            )
        except:
            raise

    def stop(self):
        """Initialize a running Java Virtual Machine.
        """
        try:
            jpype.shutdownJVM()
        except:
            raise
