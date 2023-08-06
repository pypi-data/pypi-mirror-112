from setuptools import setup
import os
import sys
from pybind11.setup_helpers import Pybind11Extension, build_ext
from pybind11 import get_cmake_dir
import glob 

__version__ = "0.1.0"

cppfiles = glob.glob('cpp/*.cpp') + glob.glob('cpp/*/*.cpp')
for fname in ['main_directed.cpp', 'main_undirected.cpp', 'oslom_net_check_overlap.cpp', 'main_body.cpp', 'standard_include.cpp', 'try_homeless_dir.cpp', 'oslom_net_unions.cpp', 'try_homeless_undir.cpp']:
    cppfiles = [u for u in cppfiles if fname not in u]

undircppfiles = [u for u in cppfiles if 'oslom_python_dir.cpp' not in u 
                and '_dir' not in u 
                and not os.path.split(u)[-1].startswith("dir")
                and ('dir_weighted_tabdeg.cpp' not in u or 'undir_weighted_tabdeg.cpp' in u)]

dircppfiles = [u for u in cppfiles if 'oslom_python_undir.cpp' not in u 
             and '_undir' not in u 
             and not os.path.split(u)[-1].startswith("undir")
             and 'undir_weighted_tabdeg.cpp' not in u]

print("undir", " ".join(undircppfiles))
print("dir", " ".join(dircppfiles))

ext_modules = [
    Pybind11Extension("coslomundir",
                      undircppfiles,
                      define_macros=[('VERSION_INFO', __version__)],
                      include_dirs=[ 'cpp'],
                      extra_compile_args=["-O3", '-std=c++17' ],
                      extra_link_args=['-lstdc++fs'],
                      language='c++',
                      ),
    Pybind11Extension("coslomdir",
                      dircppfiles,
                      define_macros=[('VERSION_INFO', __version__)],
                      include_dirs=[ 'cpp'],
                      extra_compile_args=["-O3", '-std=c++17' ],
                      extra_link_args=['-lstdc++fs'],
                      language='c++',
                      ),
]

setup(
    name="pyoslom",
    version=__version__,
    author="Bo CHen",
    author_email="bochen0909@gmail.com",
    url="https://bochen0909@github.com/bochen0909/pyoslom.git",
    description="OSLOM graph clustering algorithm",
    long_description="",
    ext_modules=ext_modules,
    extras_require={"test": "pytest"},
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    packages=['pyoslom'],
    package_dir={'pyoslom': 'src/pyoslom'},
)
