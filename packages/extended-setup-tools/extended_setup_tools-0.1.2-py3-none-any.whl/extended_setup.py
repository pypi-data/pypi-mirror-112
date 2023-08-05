
from collections import namedtuple

__title__ = 'extended-setup-tools'
__author__ = 'Peter Zaitcev / USSX Hares'
__license__ = 'BSD 2-clause'
__copyright__ = 'Copyright 2021 Peter Zaitcev'
__version__ = '0.1.2'

VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')
version_info = VersionInfo(*__version__.split('.'), releaselevel='alpha', serial=0)

import os
import re
from io import StringIO
from glob import iglob
from typing import *
from typing.io import *
from distutils.core import Command

try:
    from functools import cached_property
except ImportError:
    from functools import wraps
    _MISSING = object()
    def cached_property(prop_func: Callable[[Any], Any]):
        @property
        @wraps(prop_func)
        def wrapper(self):
            cache_dict = getattr(self, '__cached_prop_cache__', _MISSING)
            if (cache_dict is _MISSING):
                cache_dict = dict()
                self.__cached_prop_cache__ = cache_dict
            
            cache = cache_dict.get(prop_func.__name__, _MISSING)
            if (cache is _MISSING):
                result = prop_func(self)
                cache_dict[prop_func.__name__] = result
            else:
                result = cache
            
            return result
        return wrapper

from setuptools import setup as setuptools_setup, find_packages

Version = Union[Tuple[int, ...], str]

class ExtendedSetupManager:
    root_module_name: str
    sources_dir: str
    
    def __init__(self, root_module_name: str, sources_dir: str = 'src'):
        self.root_module_name = root_module_name
        self.sources_dir = sources_dir
    
    def __repr__(self):
        fields = ', '.join(f'{f}={getattr(self, f)!r}' for f in self.__annotations__.keys())
        return f'{type(self).__qualname__}({fields})'
    
    # region Requirements
    @cached_property
    def requirements(self) -> List[str]:
        requirements = [ ]
        for r in [ 'requirements/requirements.txt', 'requirements.txt' ]:
            if (os.path.isfile(r)):
                with open(r) as f:
                    requirements = [ l.strip() for l in f ]
        
        return requirements
    
    @cached_property
    def setup_requirements(self) -> List[str]:
        setup_requires = [ 'wheel' ]
        for r in [ 'requirements/setup-requirements.txt', 'setup-requirements.txt' ]:
            if (os.path.isfile(r)):
                with open(r) as f:
                    setup_requires = [ l.strip() for l in f ]
        
        return setup_requires
    @cached_property
    def test_requirements(self) -> List[str]:
        tests_require = [ ]
        for r in [ 'requirements/test-requirements.txt', 'test-requirements.txt' ]:
            if (os.path.isfile(r)):
                with open(r) as f:
                    tests_require = [ l.strip() for l in f]
        
        return tests_require
    @cached_property
    def extra_requirements(self) -> Dict[str, List[str]]:
        extras_require = { }
        for r in iglob('requirements/requirements-*.txt'):
            with open(r) as f:
                reqs = [ l.strip() for l in f ]
                feature_name = re.match(r'requirements-(.*)\.txt', os.path.basename(r)).group(1).title()
                extras_require[feature_name] = reqs
        extras_require.setdefault('all', sum(extras_require.values(), list()))
        
        return extras_require
    # endregion
    
    # region Init Script
    @property
    def init_script_file(self) -> TextIO:
        return open(os.path.join(self.sources_dir, self.root_module_name, '__init__.py'), 'rt')
    
    @cached_property
    def init_script_content(self) -> str:
        with self.init_script_file as f:
            return f.read()
    
    def find_in_init(self, key: str) -> Optional[str]:
        p = re.compile(rf'^__{key}__\s*=\s*(?P<quote>[\'"])(?P<data>.*?(?!(?P=quote)).)?(?P=quote)', re.MULTILINE)
        m = p.search(self.init_script_content)
        return m and m.group('data')
    
    @cached_property
    def name(self) -> str:
        return self.find_in_init('title')
    
    @cached_property
    def raw_version(self) -> str:
        return self.find_in_init('version')
    
    @cached_property
    def version(self) -> str:
        version = self.raw_version
        if (version.endswith(('a', 'b', 'rc'))):
            # append version identifier based on commit count
            try:
                import subprocess
                p = subprocess.Popen(['git', 'rev-list', '--count', 'HEAD'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = p.communicate()
                if out:
                    version += out.decode('utf-8').strip()
                p = subprocess.Popen(['git', 'rev-parse', '--short', 'HEAD'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = p.communicate()
                if out:
                    version += '+g' + out.decode('utf-8').strip()
            except Exception:
                pass
        
        return version

    @cached_property
    def licence(self) -> str:
        return self.find_in_init('license')
    # endregion
    
    # region Descriptions
    @property
    def readme_file(self) -> TextIO:
        for f in os.listdir('.'):
            name, sep, ext = f.rpartition('.')
            if (not sep): continue
            if (ext.lower() not in { 'md', 'markdown' }): continue
            if (name.lower() != 'readme'): continue
            
            return open(f, 'rt')
        return StringIO \
(f'''
# Package {self.name}
 - Version: {self.version}
 - ReadMe: **TBD**
''')
    @cached_property
    def readme(self) -> str:
        with self.readme_file as f:
            return f.read()
    
    @cached_property
    def url_prefix(self):
        return 'https://gitlab.com/Hares-Lab/'
    @cached_property
    def url(self):
        return self.url_prefix + self.name
    # endregion
    
    # region Tests
    @classmethod
    def discover_and_run_tests(cls):
        import os
        import sys
        import unittest
        from HtmlTestRunner import HTMLTestRunner
        
        # get setup.py directory
        setup_file = sys.modules['__main__'].__file__
        setup_dir = os.path.abspath(os.path.dirname(setup_file))
        test_loader = unittest.defaultTestLoader
        test_runner = HTMLTestRunner(template=os.path.join(setup_dir, 'test', 'report-template.html'), combine_reports=False)
        test_suite = test_loader.discover(setup_dir)
        test_result = test_runner.run(test_suite)
        exit(int(not test_result.wasSuccessful()))
    
    @property
    def TestCommand(self) -> Type[Command]:
        manager = self
        try:
            from setuptools.command.test import test as TestCommand
            
            class DiscoverTest(TestCommand):
                def finalize_options(self):
                    TestCommand.finalize_options(self)
                    self.test_args = []
                    self.test_suite = True
                def run_tests(self):
                    manager.discover_and_run_tests()
        
        except ImportError:
            from distutils.core import Command
            class DiscoverTest(Command):
                user_options = list()
                def initialize_options(self):
                    pass
                def finalize_options(self):
                    pass
                def run(self):
                    manager.discover_and_run_tests()
            TestCommand = DiscoverTest
        
        return DiscoverTest
    # endregion
    
    # region Dist Utils
    @cached_property
    def packages(self) -> List[str]:
        return find_packages(self.sources_dir)
    
    @cached_property
    def packages_dir(self) -> Dict[str, str]:
        return { '': self.sources_dir }
    
    @cached_property
    def commands(self) -> Dict[str, Type[Command]]:
        return dict(test=self.TestCommand)
    # endregion
    
    def make_setup_kwargs(self, *, short_description: str, min_python_version: Optional[Version], **kwargs):
        own_kwargs = dict \
        (
            name = self.name,
            url = self.url,
            version = self.version,
            packages = self.packages,
            package_dir = self.packages_dir,
            cmdclass = self.commands,
            description = short_description,
            long_description = self.readme,
            long_description_content_type = 'text/markdown',
            include_package_data = True,
            setup_requires = self.setup_requirements,
            install_requires = self.requirements,
            tests_require = self.test_requirements,
            extras_require = self.extra_requirements,
        )
        
        if (isinstance(min_python_version, tuple)):
            min_python_version = '.'.join(min_python_version)
        if (isinstance(min_python_version, str)):
            own_kwargs['python_requires'] = f'>={min_python_version}'
        
        own_kwargs.update(kwargs)
        return own_kwargs
    
    def setup(self, *, short_description: str, classifiers: List[str], min_python_version: Optional[Version] = None, **kwargs):
        return setuptools_setup(**self.make_setup_kwargs(short_description=short_description, classifiers=classifiers, min_python_version=min_python_version, **kwargs))


class SingleScriptModuleSetup(ExtendedSetupManager):
    script_name: str
    
    def __init__(self, script_name: str):
        super(SingleScriptModuleSetup, self).__init__(script_name, '.')
        self.script_name = script_name
    
    @property
    def init_script_file(self) -> TextIO:
        return open(f'{self.script_name}.py')
    
    def make_setup_kwargs(self, **kwargs):
        result = super().make_setup_kwargs(**kwargs)
        result.pop('packages', None)
        result.pop('package_dir', None)
        result.setdefault('py_modules', [ self.script_name ])
        return result


__all__ = \
[
    'version_info',
    '__title__',
    '__author__',
    '__license__',
    '__copyright__',
    '__version__',
    
    'ExtendedSetupManager',
    'SingleScriptModuleSetup',
]
