import json
import os
import sys
from argparse import ArgumentParser
from typing import Optional
from zipfile import ZipFile

try:
	from mcdreforged.constants import core_constant, plugin_constant
	from mcdreforged.mcdr_server import MCDReforgedServer
except ModuleNotFoundError:
	print('It seems that you have not installed all require modules')
	raise


def environment_check():
	python_version = sys.version_info.major + sys.version_info.minor * 0.1
	if python_version < 3.6:
		print('Python 3.6+ is needed')
		raise Exception('Python version {} is too old'.format(python_version))


def entry_point():
	environment_check()
	if len(sys.argv) == 1:
		run_mcdr()
	else:
		parser = ArgumentParser(
			prog=core_constant.PACKAGE_NAME,
			description='{} CLI'.format(core_constant.NAME),
		)
		subparsers = parser.add_subparsers(title='Command', help='Available commands', dest='subparser_name')

		subparsers.add_parser('start', help='Start {}'.format(core_constant.NAME))
		subparsers.add_parser('gendefault', help='Generate default configure and permission files here')

		parser_pack = subparsers.add_parser('pack', help='Pack plugin files into a {} plugin'.format(plugin_constant.PACKED_PLUGIN_FILE_SUFFIX))
		parser_pack.add_argument('-i', '--input', help='The input directory which the plugin is in, default: current directory', default='.')
		parser_pack.add_argument('-o', '--output', help='The output directory to store the packed plugin, default: current directory', default='.')
		parser_pack.add_argument('-n', '--name', help='A specific name to the output packed plugin file. If not given the metadata specific name or a default one will be used', default=None)
		parser_pack.add_argument('--keep-pycache', help='Keep __pycache__ folder if appended', action='store_true')

		result = parser.parse_args()
		# print(result)

		if result.subparser_name == 'start':
			run_mcdr()
		elif result.subparser_name == 'gendefault':
			MCDReforgedServer(generate_default_only=True)
		elif result.subparser_name == 'pack':
			make_packed_plugin(result.input, result.output, result.name, keep_pycache=result.keep_pycache)


def run_mcdr():
	print('{} {} is starting up'.format(core_constant.NAME, core_constant.VERSION))
	print('{} is open source, u can find it here: {}'.format(core_constant.NAME, core_constant.GITHUB_URL))
	try:
		mcdreforged_server = MCDReforgedServer()
	except:
		print('Fail to initialize {}'.format(core_constant.NAME_SHORT))
		raise
	else:
		if mcdreforged_server.is_initialized():
			mcdreforged_server.start()
		else:
			# If it's not initialized, config file or permission file is missing
			# Just dont do anything to let the user to check the files
			pass


def make_packed_plugin(input_dir: str, output_dir: str, file_name: Optional[str], *, keep_pycache: bool = False):
	if not os.path.isdir(input_dir):
		print('Invalid input directory {}'.format(input_dir))
		return
	if not os.path.isdir(output_dir):
		os.makedirs(output_dir)

	meta_file_path = os.path.join(input_dir, plugin_constant.PLUGIN_META_FILE)
	req_file_path = os.path.join(input_dir, plugin_constant.PLUGIN_REQUIREMENTS_FILE)
	if not os.path.isfile(meta_file_path):
		print('Plugin metadata file {} not found'.format(meta_file_path))
		return
	try:
		with open(meta_file_path, encoding='utf8') as meta_file:
			meta = json.load(meta_file)  # type: dict
		assert isinstance(meta, dict)
	except Exception as e:
		print('Fail to load plugin metadata from {}: {}'.format(meta_file_path, e))
		return
	plugin_id = meta.get('id')
	if not plugin_id:
		print('Plugin id not found in metadata')
		return
	plugin_version = meta.get('version', '?')
	if file_name is None:
		file_name = meta.get('archive_name')
	if file_name is None:
		file_name = '{}-v{}'.format(meta.get('name').replace(' ', '') or plugin_id, plugin_version)
	file_name: str
	file_name = file_name.format(id=plugin_id, version=plugin_version) + plugin_constant.PACKED_PLUGIN_FILE_SUFFIX

	def write_directory(directory: str):
		if os.path.isdir(directory):
			dir_arc = os.path.basename(directory)
			zip_file.write(directory, arcname=dir_arc)
			print('Creating directory: {} -> {}'.format(directory, dir_arc))
			for dir_path, dir_names, file_names in os.walk(directory):
				if not keep_pycache and os.path.basename(dir_path) == '__pycache__':
					continue
				for file_name_ in file_names + dir_names:
					full_path = os.path.join(dir_path, file_name_)
					if not keep_pycache and os.path.isdir(full_path) and os.path.basename(full_path) == '__pycache__':
						continue
					arc_name = os.path.join(os.path.basename(directory), full_path.replace(directory, '', 1).lstrip(os.sep))
					zip_file.write(full_path, arcname=arc_name)
					print('Writing: {} -> {}'.format(full_path, arc_name))

	print('Packing plugin "{}" into "{}" ...'.format(plugin_id, file_name))
	with ZipFile(os.path.join(output_dir, file_name), 'w') as zip_file:
		zip_file.write(meta_file_path, os.path.basename(meta_file_path))
		if os.path.isfile(req_file_path):
			zip_file.write(req_file_path, os.path.basename(req_file_path))
		write_directory(os.path.join(input_dir, plugin_id))
		for resource_path in meta.get('resources', []):
			write_directory(os.path.join(input_dir, resource_path))

	print('Done')
