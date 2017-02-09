from __future__ import absolute_import
from src.lib import Variables
from src.lib.PackageManager import PackageManager


class ArgParser:

    def __init__(self, args):
        self.args = map(lambda x: x.lower(), args)
        self.manager = PackageManager()
        self.tmp_packages = []
        for package in self.manager.local_packages:
            self.tmp_packages.append(package['name'])

    def parse(self):

        if len(self.args) > 1:

            if self.args[1] == 'help' or self.args[1] == '--help' or self.args[1] == '-h':
                self.help()

            elif self.args[1] == 'about' or self.args[1] == '--about':
                self.about()

            elif self.args[1] == 'upgrade':
                self.upgrade()

            elif self.args[1] == 'doctor':
                self.doctor()

            elif self.args[1] == 'installed':
                self.manager.installed()

            elif self.args[1] == 'list':
                self.manager.list()

            elif self.args[1] == 'search':
                for i in range(2, len(self.args)):
                    self.manager.search(self.args[i])

            elif self.args[1] == 'info':
                for i in range(2, len(self.args)):
                    self.manager.info(self.args[i])

            elif self.args[1] == 'install':
                for i in range(2, len(self.args)):
                    self.manager.install(self.args[i])

            elif self.args[1] == 'update':
                for i in range(2, len(self.args)):
                    self.manager.update(self.args[i])

            elif self.args[1] == 'rollback':
                for i in range(2, len(self.args)):
                    self.manager.rollback(self.args[i])

            elif self.args[1] == 'uninstall':
                for i in range(2, len(self.args)):
                    self.manager.uninstall(self.args[i])

            elif self.args[1] in self.tmp_packages:
                klass = self.args[1].capitalize()
                package = 'packages.' + self.args[1] + '.' + klass
                mod = __import__(package, fromlist=[klass])
                mod.run(self.args)

            else:
                print('Command or package not found ...')
        else:
            self.help()

    def doctor(self):
        self.manager.doctor()

    @staticmethod
    def upgrade():
        print('Coming soon ...')

    @staticmethod
    def about():
        print('Author: Martin Proks <martin.proks@outlook.com>')
        print('Bug report: https://github.com/matq007/src/issues')
        print(Variables.INTRO)

    @staticmethod
    def help():
        print('Example usage:')
        print('\tsrc [about|upgrade|doctor]')
        print('\tsrc [installed|list]')
        print('\tsrc search <package>')
        print('\tsrc install <package>')
        print('\tsrc update <package>')
        print('\tsrc rollback <package>')
        print('\tsrc uninstall <package>')



