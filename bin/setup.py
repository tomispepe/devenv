#! /usr/bin/env python

import os
import re
import subprocess as sp

def main():
	print str().ljust(75, '#')
	print '## Developer Environment Setup for Mac OS X'.ljust(72) + ' ##'
	print str().ljust(75, '#') + '\n'
	
	# check in on the version of OS X we are running under
	output = Shell().call_out('/usr/bin/sw_vers -productVersion')['output'][0]
	osx_ver = float(re.match('(10\.\d+)\.\d+', output).groups()[0])
	
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
	]
	
	def run(self):
		for pkg in self.packages:
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
		return self.shell.call(['/usr/bin/which', '-s', pkg.name])['result'] == 0
	
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
		
	def pkg_brew_ins(self, pkg):
		self.shell.call('brew install %s' % pkg.name)
	
	def pkg_brew_check(self, pkg):
		output = self.shell.call_out('brew info %s' % pkg.name)['output'][0].split('\n')
		for line in output:
			if line == 'Not installed':
				return False
			elif line.find('Error:') != -1:
				self.shell.ohai(line)
				exit(1)
		return True
	
if __name__ == '__main__':
	main()

