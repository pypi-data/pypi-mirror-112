import os
import argparse
import subprocess
import re
import platform
from pypi_simple import PyPISimple
from collections import namedtuple, OrderedDict

#-------------------------------------------------------------------------------
class Plugin:
	def __init__(self, name, version, url, conditions):
		self.name = name
		self.version = version
		self.url = url
		self.conditions = conditions

	def eval(self, mods):
		if len(self.conditions) == 0:
			return True

		for c in self.conditions:
			if isinstance(c, bool):
				if c:
					return True
			elif isinstance(c, str):
				if c in mods:
					return True
			else:
				error('unknown error')
		return False

	def __repr__(self):
		return '[Plugin name={}, version={}, url={}, conditions={}]'.format(self.name, self.version, self.url, self.conditions)

s_modules	= OrderedDict()
s_reverse	= OrderedDict()
s_installed	= None
s_pip		= None

#-------------------------------------------------------------------------------
def error(msg):
	print('aborted: {}'.format(msg))
	exit(1)

#-------------------------------------------------------------------------------
def add(module, version, url, mod, conds):
	if mod not in s_modules:
		s_modules[mod] = []
	s_modules[mod].append(Plugin(module, version, url, conds))
	s_reverse[module] = mod

#-------------------------------------------------------------------------------
arch = platform.machine()
add('nec-sol-core', '0.4.2.0', 'https://dav.neclab.eu/sol4ve/v0.4.2.0', 'core', [])
add('nec-sol-device-x86', '0.4.2.0', 'https://dav.neclab.eu/sol4ve/v0.4.2.0', 'core', [arch == 'x86_64',])
add('nec-sol-device-x86', '0.4.2.0', 'https://dav.neclab.eu/sol4ve/v0.4.2.0', 'x86', [])
add('nec-sol-device-nvidia', '0.4.2.0', 'https://dav.neclab.eu/sol4all/v0.4.2.0', 'nvidia', [])
add('nec-sol-device-ve', '0.4.2.0', 'https://dav.neclab.eu/sol4ve/v0.4.2.0', 've', [])
add('nec-sol-jit-gcc', '0.4.2.0', 'https://dav.neclab.eu/sol4ve/v0.4.2.0', 'core', [])
add('nec-sol-jit-dot', '0.4.2.0', 'https://dav.neclab.eu/sol4ve/v0.4.2.0', 'core', [])
add('nec-sol-jit-python', '0.4.2.0', 'https://dav.neclab.eu/sol4ve/v0.4.2.0', 'core', [])
add('nec-sol-jit-ispc', '0.4.2.0', 'https://dav.neclab.eu/sol4all/v0.4.2.0', 'x86', [])
add('nec-sol-jit-ncc', '0.4.2.0', 'https://dav.neclab.eu/sol4ve/v0.4.2.0', 've', [])
add('nec-sol-jit-nvcc', '0.4.2.0', 'https://dav.neclab.eu/sol4all/v0.4.2.0', 'nvidia', [])
add('nec-sol-backend-dfp', '0.4.2.0', 'https://dav.neclab.eu/sol4ve/v0.4.2.0', 'core', [])
add('nec-sol-backend-dnn', '0.4.2.0', 'https://dav.neclab.eu/sol4ve/v0.4.2.0', 'core', [])
add('nec-sol-backend-mkl', '0.4.2.0', 'https://dav.neclab.eu/sol4all/v0.4.2.0', 'x86', [])
add('nec-sol-backend-dnnl', '0.4.2.0', 'https://dav.neclab.eu/sol4all/v0.4.2.0', 'x86', [])
add('nec-sol-backend-nnpack', '0.4.2.0', 'https://dav.neclab.eu/sol4all/v0.4.2.0', 'x86', [])
add('nec-sol-backend-ispc', '0.4.2.0', 'https://dav.neclab.eu/sol4all/v0.4.2.0', 'x86', [])
add('nec-sol-backend-ispc-x86', '0.4.2.0', 'https://dav.neclab.eu/sol4all/v0.4.2.0', 'x86', [])
add('nec-sol-backend-cuda', '0.4.2.0', 'https://dav.neclab.eu/sol4all/v0.4.2.0', 'nvidia', [])
add('nec-sol-backend-cublas', '0.4.2.0', 'https://dav.neclab.eu/sol4all/v0.4.2.0', 'nvidia', [])
add('nec-sol-backend-cudnn', '0.4.2.0', 'https://dav.neclab.eu/sol4all/v0.4.2.0', 'nvidia', [])
add('nec-sol-backend-cudnn-bundle', '8.0.5', 'https://dav.neclab.eu/sol4all/bundle', 'cudnn', [])
add('nec-sol-backend-ncc', '0.4.2.0', 'https://dav.neclab.eu/sol4ve/v0.4.2.0', 've', [])
add('nec-sol-backend-veblas', '0.4.2.0', 'https://dav.neclab.eu/sol4ve/v0.4.2.0', 've', [])
add('nec-sol-backend-vednn', '0.4.2.0', 'https://dav.neclab.eu/sol4ve/v0.4.2.0', 've', [])
add('nec-sol-backend-veasl', '0.4.2.0', 'https://dav.neclab.eu/sol4ve/v0.4.2.0', 've', [])
add('nec-sol-framework-pytorch-python', '0.4.2.0', 'https://dav.neclab.eu/sol4ve/v0.4.2.0', 'pytorch', [])
add('nec-sol-framework-pytorch', '0.4.2.0', 'https://dav.neclab.eu/sol4ve/v0.4.2.0', 'pytorch', [])
add('torch', '1.9.0+cu111', 'https://download.pytorch.org/whl/torch_stable.html', 'pytorch', [])
add('torchvision', '0.10.0+cu111', 'https://download.pytorch.org/whl/torch_stable.html', 'torchvision', [])
add('nec-sol-framework-pytorch-x86', '0.4.2.0', 'https://dav.neclab.eu/sol4ve/v0.4.2.0', 'pytorch', [arch == 'x86_64','x86',])
add('nec-sol-framework-pytorch-nvidia', '0.4.2.0', 'https://dav.neclab.eu/sol4all/v0.4.2.0', 'pytorch', ['nvidia',])
add('nec-sol-framework-pytorch-ve', '0.4.2.0', 'https://dav.neclab.eu/sol4ve/v0.4.2.0', 'pytorch', ['ve',])
add('nec-sol-framework-pytorch-ve-native', '0.4.2.0', 'https://dav.neclab.eu/sol4ve/v0.4.2.0', 'pytorch', ['ve',])
add('nec-sol-framework-tensorflow', '0.4.2.0', 'https://dav.neclab.eu/sol4ve/v0.4.2.0', 'tensorflow', [])
add('nec-sol-framework-tensorflow-python', '0.4.2.0', 'https://dav.neclab.eu/sol4ve/v0.4.2.0', 'tensorflow', [])
add('nec-sol-framework-tensorflow-runtime', '0.4.2.0', 'https://dav.neclab.eu/sol4all/v0.4.2.0', 'tensorflow', [])
add('nec-sol-framework-tensorflow-x86', '0.4.2.0', 'https://dav.neclab.eu/sol4ve/v0.4.2.0', 'tensorflow', [arch == 'x86_64','x86',])
add('nec-sol-framework-tensorflow-nvidia', '0.4.2.0', 'https://dav.neclab.eu/sol4all/v0.4.2.0', 'tensorflow', ['nvidia',])
add('nec-sol-framework-tensorflow-ve', '0.4.2.0', 'https://dav.neclab.eu/sol4ve/v0.4.2.0', 'tensorflow', ['ve',])
add('nec-sol-framework-tensorflow-ve-native', '0.4.2.0', 'https://dav.neclab.eu/sol4ve/v0.4.2.0', 'tensorflow', ['ve',])
add('nec-sol-framework-numpy', '0.4.2.0', 'https://dav.neclab.eu/sol4ve/v0.4.2.0', 'numpy', [])
add('nec-sol-framework-onnx', '0.4.2.0', 'https://dav.neclab.eu/sol4ve/v0.4.2.0', 'onnx', [])
add('nec-sol-docs', '0.4.2.0', 'https://dav.neclab.eu/sol4ve/v0.4.2.0', 'core', [])
add('nec-sol-tests', '0.4.2.0', 'https://dav.neclab.eu/sol4all/v0.4.2.0', 'tests', [])


#-------------------------------------------------------------------------------
def run(cmd):
	ret = subprocess.run(cmd)
	if ret.returncode != 0:
		error("PIP error detected")

#-------------------------------------------------------------------------------
def run_output(cmd):
	ret = subprocess.run(cmd, stdout=subprocess.PIPE)
	if ret.returncode != 0:
		error("PIP error detected")
	return ret.stdout.decode('utf-8')

#-------------------------------------------------------------------------------
def get_plugins(ignore_error=False):
	global s_installed
	if s_installed is None:
		input = run_output([s_pip, 'list', 'installed']).split('\n')
		s_installed = []
		prog = re.compile('^(nec-sol[a-z0-9-]+)\s+([0-9\.]+)')
		for x in input:
			match = prog.match(x)
			if match:
				s_installed.append((match[1], match[2]))

		if not ignore_error and len(s_installed) == 0:
			error('SOL seems not to be installed on your system.')

	return s_installed

#-------------------------------------------------------------------------------
def get_modules(ignore_error=False):
	output = set()
	for p, v in get_plugins(ignore_error):
		output.add((s_reverse[p], v))
	output = list(output)
	output.sort()
	return output

#-------------------------------------------------------------------------------
def check_mods(mods):
	mods.append("core") # always needed

	plugins = []
	urls	= set()

	for m in mods:
		if m not in s_modules:
			print("Unknown module: {}".format(m))
		else:
			for p in s_modules[m]:
				if p.eval(mods):
					plugins.append((p.name, p.version))
					if p.url:
						urls.add(p.url)

	urls = list(urls)
	plugins.sort()
	urls.sort()

	return plugins, urls

#-------------------------------------------------------------------------------
def check_version(mods):
	if len(mods) == 0:
		version = None
	else:
		version = mods[0]
		if version == '0.4.2.0':
			error("You are already using v{}".format(version))

	try:
		with PyPISimple() as client:
			info = client.get_project_page("nec-sol")
	except:
		error("Can't connect to PyPI")
	
	if version is None:
		version = info.packages[-1].version
	else:
		def checkVersion():
			for p in info.packages:
				if p.version == version:
					return True
			return False

		if not checkVersion():
			error("Unknown version v{}".format(version))
	return version

#-------------------------------------------------------------------------------
# Callbacks
#-------------------------------------------------------------------------------
def install(args):
	mods = list(m for m, v in get_modules(ignore_error=True))
	mods = mods + args.modules
	mods = list(set(mods)) # remove duplicates
	plugins, urls = check_mods(mods)

	cmd = [s_pip, 'install']
	if args.user:
		cmd.append('--user')

	for p, v in plugins:
		if v:
			cmd.append('{}=={}'.format(p, v))
		else:
			cmd.append(p)

	if args.local:
		cmd.append('-f')
		cmd.append('.')
	else:
		if args.trust:
			cmd.append('--trusted-host')
			cmd.append('dav.neclab.eu')
		
		for u in urls:
			cmd.append('-f')
			cmd.append(u)

	run(cmd)

#-------------------------------------------------------------------------------
def upgrade(args):
	version = check_version(args.modules)

	# Get currently installed SOL ----------------------------------------------
	plugins	= get_plugins()
	mods	= get_modules()

	# Upgrade NEC-SOL ----------------------------------------------------------
	cmd = [s_pip, 'install']
	if args.user:
		cmd.append('--user')
	cmd.append('nec-sol=={}'.format(version))
	if args.local:
		cmd.append('-f')
		cmd.append('.')
	run(cmd)

	# Uninstall old SOL plugins ------------------------------------------------
	cmd = [s_pip, 'uninstall', '-y']
	for p, v in plugins:
		cmd.append(p)
	run(cmd)

	# Install new SOL modules --------------------------------------------------
	cmd = ['python3', '-m', 'nec-sol', 'install']
	for m, v in mods:
		cmd.append(m)
	if args.local:	cmd.append('--local')
	if args.user:	cmd.append('--user')
	if args.trust:	cmd.append('--trust')
	run(cmd)   

#-------------------------------------------------------------------------------
def uninstall(args):
	plugins = get_plugins()

	if len(args.modules) > 0:
		todelete = []
		for p, v in plugins:
			if s_reverse[p] in args.modules:
				todelete.append((p, v))
		plugins = todelete

	if len(plugins) == 0:
		error('None of these modules are currently installed.')
	
	print('Are you sure you want to uninstall the following PIP packages? ')
	for p, v in plugins:
		print('- {} v{}'.format(p, v))
	print('')
	val = input('[y/N]: ')
	
	if val == 'y':
		cmd = [s_pip, 'uninstall', '-y']
		for p, v in plugins:
			cmd.append(p)
		run(cmd)
	else:
		error('user declined uninstallation')

#-------------------------------------------------------------------------------
def download(args):
	plugins, urls = check_mods(args.modules)

	cmd = [s_pip, 'download']
	for p, v in plugins:
		if v:
			cmd.append('{}=={}'.format(p, v))
		else:
			cmd.append(p)

	if args.trust:
		cmd.append('--trusted-host')
		cmd.append('dav.neclab.eu')

	for u in urls:
		cmd.append('-f')
		cmd.append(u)

	run(cmd)

#-------------------------------------------------------------------------------
def list_installed():
	print("Installed SOL Modules:")
	for m, v in get_modules():
		print('- {} v{}'.format(m, v))

#-------------------------------------------------------------------------------
def list_installed_plugins():	
	print("Installed SOL Plugins:")
	for p, v in get_plugins():
		print('- {} v{}'.format(p, v))

#-------------------------------------------------------------------------------
def list_available():	
	print("Available SOL Modules:")
	for m in s_modules.keys():
		print('- {}'.format(m))

#-------------------------------------------------------------------------------
if __name__ == '__main__':
	print('## NEC-SOL Package Manager v0.4.2.0')
	print('')

	parser = argparse.ArgumentParser()
	parser.add_argument('cmd', default='help', choices=['install', 'download', 'upgrade', 'uninstall', 'list_installed', 'list_available', 'list_installed_plugins'])
	parser.add_argument('-l', '--local', action='store_true')
	parser.add_argument('-u', '--user', action='store_true')
	parser.add_argument('-t', '--trust', action='store_true')
	parser.add_argument('modules', type=str, nargs='*', help='')
	args = parser.parse_args()

	s_pip = os.environ.get('NEC_SOL_PIP', 'pip3')

	if args.cmd == 'install':
		install(args)
	elif args.cmd == 'download':
		download(args)
	elif args.cmd == 'upgrade':
		upgrade(args)
	elif args.cmd == 'uninstall':
		uninstall(args)
	elif args.cmd == 'list_installed':
		list_installed()
	elif args.cmd == 'list_installed_plugins':
		list_installed_plugins()
	elif args.cmd == 'list_available':
		list_available()
	else:
		raise Exception('unknown nec-sol command: {}'.format(args.cmd))
