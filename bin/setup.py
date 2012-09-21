#! /usr/bin/env python

import os
import platform
import re
import subprocess as sp
import json
import tempfile as tf
import shutil

sc_name = 'setup-py'
tmpdir = tf.mkdtemp('-' + sc_name)

def main():
    print str().ljust(75, '#')
    print '## Developer Environment Setup for Mac OS X'.ljust(72) + ' ##'
    print str().ljust(75, '#') + '\n'
    
    print 'tmpdir: ' + tmpdir

    # check in on the version of OS X we are running under
    osx_ver = float(re.match('(10\.\d+)\.\d+', platform.mac_ver()[0]).groups()[0])
    
    if osx_ver < 10.8:
        Shell().ohai('This script requires Mac OS X 10.8 or newer\n')
        exit(1)
    
    # check for 421 or newer of Xcode CLI tools
    output = Shell().call_out(['/bin/sh', '-c', '/usr/bin/cc --version 2> /dev/null'])['output'][0]
    output = re.search('tags/Apple/clang-(\d+)', output)
    
    if output is None:
        tools_ver = 0
    else:
        tools_ver = int(output.groups()[0])
    
    if tools_ver < 421:
        Shell().ohai('Please install the "Command Line Tools for Xcode": http://connect.apple.com\n')   
        exit(1)
        
    # initiate package installation
    PackageInstaller().run()

class Shell():

    def call(self, command, returnOutput=False):
        if type(command) == str:
            command = command.split(' ')
        
        if returnOutput == True:
            process = sp.Popen(command, stdout=sp.PIPE)
        else:
            process = sp.Popen(command)
        
        output = process.communicate()
        return {'result': process.returncode, 'output': output}

    def call_out(self, command):
        return self.call(command, True)
    
    def curl_download(self, url, name):
        tmpFile = tmpdir + '/' + name
        self.call(['/bin/sh', '-c', 'curl -fkL# %s > %s' % (url, tmpFile)])
        return tmpFile
    
    # For escape codes: http://linuxgazette.net/issue65/padala.html
    def ohai(self, msg):
        print '\x1B[1;34m==> \x1B[1;30m%s\x1B[0;0m' % msg
    
    def ohay(self, msg):
        print '\x1B[1;32m==> \x1B[0;30m%s\x1B[0;0m' % msg

class Package():
    name = str
    type = str
    
    def __init__(self, name, type=None):
        self.name = name
        self.type = type

    def get_desc(self):
        if self.type is not None:
            return self.type + ':' + self.name
        return self.name

class PackageInstaller():

    shell = Shell()
    packages = [
        Package('brew'),
        Package('subversion', 'brew'),
        Package('watch',      'brew'),
        Package('wget',       'brew'),
        Package('ack',        'brew'),
        Package('textmate'),
        Package('dropbox'),
    ]
    
    def run(self):
        for pkg in self.packages:
            print
            self.shell.ohai('Checking for %s package...' % pkg.get_desc())
            if self.installed(pkg) == False:
                self.shell.ohay('Installing package %s...' % pkg.get_desc())
                self.pkg_get_method('ins', pkg)(pkg)
            else:
                self.shell.ohay('Package %s is installed.' % pkg.get_desc())
    
    def installed(self, pkg):
        return self.pkg_get_method('check', pkg)(pkg)
    
    def pkg_get_method(self, op_type, pkg):
        if pkg.type is not None:
            op_type = '%s_%s' % (pkg.type, op_type)
        return getattr(self, 'pkg_%s_%s' % (op_type, pkg.name), getattr(self, 'pkg_%s' % op_type))
    
    def pkg_ins(self, pkg):
        self.shell.ohai('Error: Missing pkg_ins method for %s package.' % pkg.get_desc())
        exit(1)
        
    def pkg_check(self, pkg):
        self.shell.ohai('Error: Missing pkg_check method for %s package.' % pkg.get_desc())
        exit(1)
    
    def pkg_ins_brew(self, pkg):
        self.shell.call(['/bin/sh', '-c', 'curl -fsSkL raw.github.com/mxcl/homebrew/go | ruby'])
        self.shell.ohai('Running brew doctor')
        
        output = self.shell.call_out('brew doctor')['output']
        if output[0] != 'Your system is raring to brew.\n':
            for line in output:
                if line is not None:
                    print line
            self.shell.ohai('Please resolve the issues brew doctor reported and try again.')
            exit(1)
        else:
            print 'Your system is raring to brew.'
        
    def pkg_check_brew(self, pkg):
        if os.path.exists('/usr/local/bin/brew'):
            return True
        return False
        
    def pkg_brew_ins(self, pkg):
        self.shell.call('/usr/local/bin/brew install %s' % pkg.name)
    
    def pkg_brew_check(self, pkg):
        output = self.shell.call_out('/usr/local/bin/brew info %s' % pkg.name)['output'][0].split('\n')
        for line in output:
            if line == 'Not installed':
                return False
            elif line.find('Error:') != -1:
                self.shell.ohai(line)
                exit(1)
        return True
        
    def pkg_ins_textmate(self, pkg):
        print 'Finding the latest version'
        output = self.shell.call_out('curl -fsSkL https://api.github.com/repos/textmate/textmate/downloads')['output'][0]
        latest = json.loads(output)[0]          # this assumes that the latest version is the most recent download
        
        print 'Downloading ' + latest['name']
        tmpFile = self.shell.curl_download(latest['html_url'], latest['name'])
        self.shell.call(['/usr/bin/tar', '-xjf', tmpFile, '-C', '/Applications/'])
        os.unlink(tmpFile)
        
        print 'Installing command line tool'
        shutil.copy('/Applications/TextMate.app/Contents/Resources/mate', '/usr/local/bin/mate')
        mate_ver = self.shell.call_out('/usr/local/bin/mate --version')['output'][0].split(' ')[1]
        self.shell.call('/usr/bin/defaults write com.macromates.TextMate.preview mateInstallPath /usr/local/bin/mate')
        self.shell.call('/usr/bin/defaults write com.macromates.TextMate.preview mateInstallVersion ' + mate_ver)
        self.shell.call('/usr/bin/defaults write com.macromates.TextMate mateInstallPath /usr/local/bin/mate')
        self.shell.call('/usr/bin/defaults write com.macromates.TextMate mateInstallVersion ' + mate_ver)
        
    def pkg_check_textmate(self, pkg):
        if os.path.exists('/Applications/TextMate.app'):
            return True
        return False
    
    def pkg_ins_dropbox(self, pkg):
        print 'Downloading Dropbox for Mac'
        tmpFile = self.shell.curl_download('https://www.dropbox.com/download?plat=mac', 'dropbox.dmg')
        
        print 'Mouting disk image'
        mountPoint = self.shell.call_out('/usr/bin/hdiutil mount ' + tmpFile)['output'][0].strip().split('\n').pop().strip().split('\t').pop()

        print 'Copying application'
        self.shell.call(['/bin/cp', '-a', mountPoint + '/Dropbox.app', '/Applications/Dropbox.app'])
        self.shell.call(['/usr/bin/hdiutil', 'unmount', mountPoint])
        
        print 'Launching application'
        self.shell.call(['/usr/bin/open', '/Applications/Dropbox.app'])
        
        os.unlink(tmpFile)
        
    def pkg_check_dropbox(self, pkg):
        if os.path.exists('/Applications/DropBox.app'):
            return True
        return False
    
if __name__ == '__main__':
    main()

