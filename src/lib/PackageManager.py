from __future__ import print_function
from __future__ import absolute_import

import json
import os
import shutil
import sys
import tarfile
from hashlib import md5
import requests

from src.lib.Logger import Logger
from src.lib import Variables
from src.lib.BColors import BColors


class PackageManager:
    def __init__(self):
        self.packages = []
        self.local_json = []
        self.local_packages = []
        self.url = Variables.URL

        if not os.path.exists(Variables.PACKAGE_JSON):
            print('File %s doesn\'t exists, creating new one' % Variables.PACKAGE_JSON)
            content = '{"packages": []}'
            with open(Variables.PACKAGE_JSON, 'w') as f:
                f.write(content)
            f.close()

        self.__reload_packages()

        # REMOTE SERVER JSON
        try:
            r = requests.get(self.url, timeout=5)
            self.packages = json.loads(r.content)['packages']
        except requests.exceptions.Timeout:
            print('Timeout reached ... ')
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(-1)

    def __reload_packages(self):
        json_data = open(Variables.PACKAGE_JSON).read()
        self.local_json = json.loads(json_data)
        self.local_packages = self.local_json['packages']

    def __find(self, name, remote=True):
        if remote:
            source = self.packages
        else:
            source = self.local_packages
        for i in range(len(source)):
            if source[i]['name'] == name:
                return i

        return -1

    def __install_dep(self, index):
        requirements = ''
        requirements_file = os.path.expanduser(os.path.join(
            Variables.PACKAGE_FOLDER,
            self.packages[index]['name'],
            'requirements.txt'
        ))
        if os.path.exists(requirements_file):
            with open(requirements_file, 'r') as f:
                for line in f.read().splitlines():
                    requirements += line + ' '
            f.close()

            command = '***********************************\n' \
                      'Please run manually:\n\tsudo pip install %s\n' \
                      '***********************************' % requirements
            print(command)

    def __install_ins(self, index):
        instructions = os.path.expanduser(os.path.join(
            Variables.PACKAGE_FOLDER,
            self.packages[index]['name'],
            'INSTALL'
        ))
        if os.path.exists(instructions):
            with open(instructions, 'r') as f:
                for line in f.read().splitlines():
                    print(line)
            f.close()

    def __update_json(self, operation, package, index):
        if operation == 'add':
            del package['rollback']
            self.local_json['packages'].append(package)
            with open(Variables.PACKAGE_JSON, 'w') as f:
                json.dump(self.local_json, f)
            f.close()
            self.__reload_packages()

        elif operation == 'remove':
            del self.local_json['packages'][index]
            with open(Variables.PACKAGE_JSON, 'w') as f:
                json.dump(self.local_json, f)
            f.close()
            self.__reload_packages()

        elif operation == 'rollback':
            self.local_json['packages'].append(package)
            with open(Variables.PACKAGE_JSON, 'w') as f:
                json.dump(self.local_json, f)
            f.close()
            self.__reload_packages()

        else:
            Logger().error('__update_json, operation: %s' % operation)

    def __update(self, name):
        index = self.__find(name, False)
        remote_index = self.__find(name)
        if self.local_packages[index]['version'] < self.packages[remote_index]['version']:
            print('Updating %s from (%s) to (%s)' %
                  (name, self.local_packages[index]['version'], self.packages[remote_index]['version']))
            tmp_file = os.path.expanduser(
                os.path.join(Variables.TMP_FOLDER, self.packages[remote_index]['name'])) + Variables.EXTENSION
            self.download(self.packages[remote_index]['url'], tmp_file)
            print('Verifying checksum ...')

            # CHECKSUM MD5
            if self.packages[remote_index]['checksum'] == self.md5sum(tmp_file):
                print('Uninstalling old version install new version')
                self.uninstall(name)
                self.extract_file(tmp_file, Variables.PACKAGE_FOLDER)

                # INSTALL DEPENDENCIES from requirements.txt
                self.__install_dep(remote_index)

                # SHOW INSTALL INSTRUCTIONS
                self.__install_ins(remote_index)

                # ADD PACKAGE INFO INTO local packages.json
                self.__update_json('add', self.packages[remote_index], None)

            else:
                print(BColors.WARNING + 'Checksum failed... Download again?' + BColors.ENDC)
                Logger().error('Checksum failed for %s value: %s expected: %s'
                               % (name, self.md5sum(tmp_file), self.packages[remote_index]['checksum']))

    def __remove(self, index):
        dest = os.path.expanduser(os.path.join(
            Variables.PACKAGE_FOLDER,
            self.local_packages[index]['name']
        ))
        shutil.rmtree(dest, ignore_errors=True)
        self.__update_json('remove', None, index)

    def search(self, name):
        index = self.__find(name)
        if index == -1:
            print(BColors.FAIL + 'Package %s not found' % name + BColors.ENDC)
        else:
            line_width = 20
            print(BColors.OKGREEN + self.packages[index]['name'].ljust(line_width) + BColors.ENDC +
                  "%s" % str(self.packages[index]['description']))

    def info(self, name):
        index = self.__find(name)
        if index == -1:
            print(BColors.FAIL + 'No info for %s found' % name + BColors.ENDC)
        else:
            print('Name: %s\n'
                  'Version: %s\n'
                  'Description: %s' % (
                      BColors.OKGREEN + str(self.packages[index]['name']) + BColors.ENDC,
                      BColors.OKGREEN + (self.packages[index]['version']) + BColors.ENDC,
                      BColors.OKGREEN + (self.packages[index]['description']) + BColors.ENDC)
                  )

    def install(self, name):

        if self.__find(name) != -1:
            remote_index = self.__find(name)
            if self.__find(name, False) == -1:

                tmp_file = os.path.expanduser(
                    os.path.join(Variables.TMP_FOLDER, self.packages[remote_index]['name'])) + Variables.EXTENSION

                self.download(self.packages[remote_index]['url'], tmp_file)

                print('Verifying checksum ...')
                # CHECKSUM MD5
                if self.packages[remote_index]['checksum'] == self.md5sum(tmp_file):
                    self.extract_file(tmp_file, Variables.PACKAGE_FOLDER)

                    # INSTALL DEPENDENCIES from requirements.txt
                    self.__install_dep(remote_index)

                    # SHOW INSTALL INSTRUCTIONS
                    self.__install_ins(remote_index)

                    # ADD PACKAGE INFO INTO local packages.json
                    self.__update_json('add', self.packages[remote_index], None)

                else:
                    print('Checksum failed... Download again?')
                    Logger().error('Checksum failed for %s value: %s expected: %s'
                                   % (name, self.md5sum(tmp_file), self.packages[remote_index]['checksum']))
            else:
                index = self.__find(name, False)
                print('Package %s(%s) is already installed ...' %
                      (BColors.OKGREEN + self.packages[index]['name'], self.packages[index]['version'] + BColors.ENDC))
        else:
            print(BColors.FAIL + 'Package %s not found ...' % name + BColors.ENDC)

    def update(self, option=None):
        if option is None:
            for package in self.local_packages:
                self.__update(package)
        else:
            for package in option:
                self.__update(package)

    def rollback(self, name):
        remote_index = self.__find(name)
        if remote_index != -1:
            index = self.__find(name, False)
            if self.local_packages[index]['checksum'] != self.packages[remote_index]['rollback']['checksum']:
                tmp_file = os.path.expanduser(
                    os.path.join(Variables.TMP_FOLDER, self.packages[remote_index]['name'])) + Variables.EXTENSION

                self.download(self.packages[remote_index]['rollback']['url'], tmp_file)

                print('Verifying checksum ...')
                # CHECKSUM MD5
                if self.packages[remote_index]['rollback']['checksum'] == self.md5sum(tmp_file):
                    self.extract_file(tmp_file, Variables.PACKAGE_FOLDER)

                    index = self.__find(name, False)
                    self.__update_json('remove', None, index)

                    # INSTALL DEPENDENCIES from requirements.txt
                    self.__install_dep(remote_index)

                    # SHOW INSTALL INSTRUCTIONS
                    self.__install_ins(remote_index)

                    # ADD PACKAGE INFO INTO local packages.json
                    self.__update_json('rollback', self.packages[remote_index]['rollback'], None)
                else:
                    print(BColors.WARNING + 'Checksum failed... Download again?' + BColors.ENDC)
                    Logger().error('Checksum failed for %s value: %s expected: %s'
                                   % (name, self.md5sum(tmp_file), self.packages[remote_index]['checksum']))
            else:
                print(BColors.OKGREEN + 'Package %s already rollbacked ...' % name + BColors.ENDC)
        else:
            print(BColors.FAIL + 'Package %s not found ...' % name + BColors.ENDC)

    def uninstall(self, name):
        index = self.__find(name, False)

        if index != -1:
            self.__remove(index)
            print(BColors.OKGREEN + 'Package %s removed ...' % name + BColors.ENDC)
        else:
            print(BColors.FAIL + 'Package %s not found ...' % name + BColors.ENDC)

    def installed(self):
        if len(self.local_packages) < 1:
            print(BColors.FAIL + 'No packages installed ...' + BColors.ENDC)
        else:
            for package in self.local_packages:
                print(BColors.OKBLUE + str(package['name']).capitalize() + " [%s]" % package['version'] + BColors.ENDC
                )

    def list(self):
        line_width = 20
        for package in self.packages:
            print(BColors.OKBLUE + str(package['name']).capitalize() + '(' + package['version'] + ')'.ljust(line_width) +
                  BColors.ENDC + "%s" % str(package['description']))

    def doctor(self):
        print('Comming soon')

    @staticmethod
    def md5sum(filename):
        if not os.path.exists(filename):
            return -1
        hash = md5()
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(128 * hash.block_size), b""):
                hash.update(chunk)
        f.close()
        return hash.hexdigest()

    @staticmethod
    def extract_file(compressed_file, to_directory):
        if compressed_file.endswith('.tar.gz') or compressed_file.endswith(Variables.EXTENSION):
            opener, mode = tarfile.open, 'r:gz'
        else:
            print('Could not extract `%s` as no appropriate extractor is found')

        cwd = os.getcwd()
        os.chdir(to_directory)

        try:
            file = opener(compressed_file, mode)
            try:
                file.extractall()
            except Exception as e:
                Logger().warning(e.message)
            finally:
                file.close()
        finally:
            os.chdir(cwd)

    @staticmethod
    def download(url, tmp_file):
        r = requests.get(url, stream=True)
        with open(tmp_file, 'w+') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
        f.close()
