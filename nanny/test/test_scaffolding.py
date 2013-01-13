# coding: utf-8
import unittest
import tempfile
from pkg_resources import resource_filename
from scaffolding import Scanner, Templater, Generator

TEMPLATES = resource_filename(__name__, "data/templates")

class TestScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = Scanner(templates=TEMPLATES, template="test")

    def test_fetch_variables(self):
        """
        測試抓取一個 template 中的變數
        """
        variables = self.scanner.fetch_variables(
                "src/coffee/{{resource}}/index.coffee")
        expected = ["resource_class",
                    "resource_collection_class",
                    "resource_url",
                    "resource_collection_variable",
                    "resource"
                ]
        self.assertListEqual(sorted(variables), sorted(expected))

    def test_scan(self):
        result = self.scanner.scan()
        expected = [u'test',
                    u'resource_url',
                    u'resource_collection_class',
                    u'resource_collection_variable',
                    u'resource_class',
                    u'resource']
        self.assertListEqual(sorted(result), sorted(expected))

class TestTemplater(unittest.TestCase):
    def setUp(self):
        self.templater = Templater(template="test", templates=TEMPLATES)

    def test_render_yaml(self):
        result = self.templater.render_yaml([ "a", "b"])
        expected = """\
a:
  description: ''
  example: ''
b:
  description: ''
  example: ''
c:
  description: ''
  example: test
"""
        self.assertMultiLineEqual(expected, result)

class TestGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = Generator(template="test", templates=TEMPLATES)

    def test_generate_final(self):
        import os, shutil
        tempdir = os.path.join(tempfile.gettempdir(), "scaffolding_test")
        # remove existed
        if os.path.exists(tempdir):
            shutil.rmtree(tempdir)
        os.mkdir(tempdir)

        self.generator.generate_final(self.generator.load_dynamic({
            'test': 'test value',
            'resource_url': 'xxx/xxx/xxx',
            'resource_collection_class': 'Class',
            'resource_collection_variable': 'variable',
            'resource_class': 'Class'
            # 'resource': 'a/b/c'
            }), tempdir)

        self.assertDirectoryEqual(tempdir,
                                  resource_filename(__name__,
                                                    "data/test_generate_final"))

    def assertDirectoryEqual(self, d1, d2):
        import os
        walk1 = os.walk(d1)
        walk2 = os.walk(d2)

        for root, dirs, files in walk1:
            try:
                root2, dirs2, files2 = walk2.next()
            except StopIteration:
                raise AssertionError("two directories are not equal.")

            self.assertListEqual(dirs, dirs2)
            self.assertListEqual(files, files2)

            for f in files:
                with open(os.path.join(root, f)) as result:
                    with open(os.path.join(root2, f)) as result2:
                        self.assertMultiLineEqual(result.read(), result2.read())

        try:
            walk2.next()
        except StopIteration:
            return

        raise AssertionError("two directories are not equals.")

