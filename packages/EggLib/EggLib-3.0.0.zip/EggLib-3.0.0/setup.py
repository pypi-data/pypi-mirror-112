import os
import sys
from glob import glob
from importlib import import_module

from setuptools import Extension, find_packages, setup
from setuptools.command.install import install
from setuptools import Command

HERE = os.path.abspath(os.path.dirname(__file__))

# get specific options
_DEBUG = False
i = 1
while i < len(sys.argv):
    if sys.argv[i] == '--debug':
        _DEBUG = True
        del sys.argv[i]
    else:
        i += 1

########################################################################
# get Version of module
def read(rel_path):
    """read the file and return the lines"""
    with open(os.path.join(HERE, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    """try to find __version__ on the egglib __init__ file"""
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


NAME = 'egglib'
VERSION = get_version(os.path.join(r"src", "egglib", "__init__.py"))
pkg_list = [NAME]
pkg_list += [NAME + "." + sub for sub in find_packages(os.path.join(r"src", "egglib"))]

# Common flags for both release and debug builds.
if _DEBUG:
    extra_compile_args = ["-g", "-O0", "-DDEBUG"]
else:
    extra_compile_args = ['-O3', '-g0']

########################################################################
# make custom commands
class BuildPDF(Command):
    """To run latexpdf with sphinx-build command system"""
    user_options = [
            ('source-dir=', 's', 'doc source directory'),
            ('output-dir=', 'o', 'output directory'),
    ]

    def initialize_options(self):
        self.source_dir = os.path.abspath(os.path.join('doc'))
        self.output_dir = os.path.abspath(os.path.join('doc', 'build'))

    def finalize_options(self):
        self.source_dir = os.path.abspath(self.source_dir)
        self.output_dir = os.path.abspath(self.output_dir)
        if self.source_dir is None:
            raise Exception("Parameter --source-dir is missing")
        if self.output_dir is None:
            raise Exception("Parameter --output-dir is missing")
        if not os.path.isdir(self.source_dir):
            raise Exception("Source directory does not exist: {0}".format(self.source_dir))
        if not os.path.isdir(self.output_dir):
            raise Exception("Output directory does not exist: {0}".format(self.output_dir))

    def run(self):
        from subprocess import Popen, PIPE
        # print("####################")
        cmd = 'sphinx-build -M latexpdf {0} {1}'.format(self.source_dir, self.output_dir)
        print("Use command line to build: '{0}'\n".format(cmd))
        p = Popen(cmd.split(), stdout=PIPE)
        # Grab stdout line by line as it becomes available.  This will loop until
        # p terminates.
        while p.poll() is None:
            line = p.stdout.readline().decode('UTF-8').strip()  # This blocks until it receives a newline.
            print(line)
        # When the subprocess terminates there might be unconsumed output
        # that still needs to be processed.
        print(p.stdout.read().decode('UTF-8').strip())


########################################################################
# extension module
binding = Extension(NAME + '._eggwrapper',
                    sources=glob(os.path.join(r'src', 'cppfiles', '*.cpp')),
                    library_dirs=[os.getcwd(), ],  # path to .a or .so file(s)
                    language='c++',
                    include_dirs=[os.path.join(r'src', 'cppfiles')],
                    swig_opts=['-python', '-c++', '-builtin', '-Wall'],
                    extra_compile_args=extra_compile_args)

########################################################################
# main function
def main():
    setup(
            cmdclass={'build_pdf': BuildPDF},

            # Project information
            name="EggLib",
            version=VERSION,
            url='https://egglib.org/',
            project_urls={
                    "Bug Tracker"  : "https://gitlab.com/demita/egglib/-/issues",
                    "Documentation": "https://egglib.org/",
                    "Source Code"  : "https://gitlab.com/demita/egglib/-/tree/master",
            },
            download_url="https://pypi.org/project/EggLib/{0}/#files".format(VERSION),
            author='Stéphane De Mita, Mathieu Siol',
            author_email='demita@gmail.com',
            license='GPL v3',
            description='Evolutionary Genetics and Genomics Library',
            long_description=open(os.path.join(HERE, 'README.rst'), encoding='utf-8').read(),
            long_description_content_type='text/x-rst',

            # docs compilation utils
            command_options={
                    'build_sphinx': {
                            'project'   : ('setup.py', NAME),
                            'version'   : ('setup.py', VERSION),
                            'release'   : ('setup.py', VERSION),
                            'source_dir': ('setup.py', os.path.join(r'doc')),
                            'build_dir' : ('setup.py', os.path.join(r'doc', 'build')),

                    }},
            # Package information
            package_dir={'egglib': os.path.join(r'src', 'egglib')},
            packages=pkg_list,
            ext_modules=[binding],
            install_requires=[],
            setup_requires=[],

            # Pypi information
            platforms=['platform-independent'],
            classifiers=[
                    "Programming Language :: Python :: 3.6",
                    "Programming Language :: Python :: 3.7",
                    "Programming Language :: Python :: 3.8",
                    "Programming Language :: Python :: 3.9",
                    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
                    "Operating System :: OS Independent"],
            extras_require={
                    'doc': ['numpydoc'],
            },
            options={
                    'bdist_wheel':
                        {'universal': True}
            },
            # scripts=['./scripts/'],
            zip_safe=False,  # Don't install the lib as an .egg zipfile
            # entry_points={
            #         'egglib': ["./scr/egglib=__init__"]
            # },
    )


if __name__ == '__main__':
    main()
