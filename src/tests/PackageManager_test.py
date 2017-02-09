from __future__ import absolute_import

import sys
import unittest
from StringIO import StringIO
from src.lib.PackageManager import PackageManager


class PackageManger_test(unittest.TestCase):

    def setUp(self):
        self.manager = PackageManager()
        self.output = StringIO()
        self.saved_stdout = sys.stdout
        sys.stdout = self.output

    def test_search(self):
        self.manager.search('emotion')
        res = self.output.getvalue().encode('UTF-8').split(' ')[0][5:]
        assert res == 'emotion'

    def test_info(self):
        self.manager.info('emotion')
        res = self.output.getvalue().encode('UTF-8').split('\n')
        assert len(res) == 4

    def test_install(self):
        self.manager.install('emotion')
        assert len(self.manager.local_packages) == 1

    def test_uninstall(self):
        self.manager.uninstall('emotion')
        assert len(self.manager.local_packages) == 0

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(PackageManger_test)
    unittest.TextTestRunner(verbosity=2).run(suite)
