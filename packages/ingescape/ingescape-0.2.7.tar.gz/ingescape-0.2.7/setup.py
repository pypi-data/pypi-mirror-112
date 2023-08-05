# -*- coding: utf-8 -*-
#distutils: language = c
#distutils: sources = /usr/local/Frameworks/
__author__ = "vaugien"
__copyright__ = "Copyright © 2018 ingenuity."
__license__ = "All rights reserved."
__version__ = "0.2.7"

import sys
import setuptools
from distutils.core import setup, Extension
import os

if sys.platform == "win32":
      sys.path.extend("C:/Program Files/ingescape/include")
      sys.path.extend("C:/Program Files/ingescape/lib",)
      inc_dirs = ["C:/Program Files/ingescape/include", "./"]
      lib_dirs = ["C:/Program Files/ingescape/lib"]
      src = ["ingescapePython.c",  "admin.c", 
            "data.c",  "definition.c",  "mapping.c", 
            "freezecallback.c", "init.c",
            "input.c",  "observecallback.c", 
            "output.c",  "parameter.c", 
            "start.c",  "stopcallback.c", 
            "advanced.c", "call.c", 
            "unixfunctions.c", "agentEvent.c"]
else:
      sys.path.extend("/usr/local/include/")
      sys.path.extend("/usr/local/lib/")
      inc_dirs = ["", "/usr/local/include"]
      lib_dirs = ["/usr/local/lib"]
      src = ["ingescapePython.c",  "admin.c", 
            "data.c",  "definition.c",  
            "mapping.c", "freezecallback.c", 
            "init.c", "input.c", 
            "observecallback.c", "output.c", 
            "parameter.c", "start.c", 
            "stopcallback.c", "advanced.c", 
            "call.c", "agentEvent.c"]

link_args = ["-lingescape"]

# the c extension module

extension_mod = Extension("ingescape", src, 
            extra_compile_args=["-g", "-lingescape"],  
            include_dirs = inc_dirs, 
            libraries = ["ingescape"],
            library_dirs = lib_dirs)

setup(name =  "ingescape",
      author = "Natanael Vaugien",
      author_email = "vaugien@ingenuity.io",
      version =  "0.2.7",
      license =  "Copyright © 2018-2021 ingenuity. All rights reserved.",
      ext_modules = [extension_mod])
