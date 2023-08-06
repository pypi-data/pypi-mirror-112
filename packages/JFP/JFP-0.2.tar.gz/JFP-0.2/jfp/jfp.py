#coding:utf-8
#!/usr/bin/python

import argparse
import os
import zipfile


parser = argparse.ArgumentParser(description='Start Args')
parser.add_argument('--create','-C', help='Newest file for create patch file', type=str, default=None)
parser.add_argument('--apply','-A', help='Patch with a patch file', type=str, default=None)
parser.add_argument('--file', '-F', help='Other file', type=str, default=None)
parser.add_argument('--output', '-O', help='Output file', type=str, default=None)
parser.add_argument('--desc', '-D', help='Description of this patch', type=str, default=None)
args = parser.parse_args()

def main():
	if args.create == None and args.apply == None:
		print('Error argument, Type --help')
		exit()

	if args.create is not None:
		if args.create is None or args.file is None:
			print('Need newest and oldest file path')
			exit()
		z_oldest = zipfile.ZipFile(args.file, 'r')
		z_newest = zipfile.ZipFile(args.create, 'r')
		z_patch = zipfile.ZipFile(args.output, 'w')
		if args.desc is not None:
			z_patch.desc = args.desc.encode('utf-8')
		o_files = z_oldest.namelist()
		n_files = z_newest.namelist()
		for n_file in n_files:
			should_patch = False
			save_type = zipfile.ZIP_DEFLATED
			if n_file in o_files:
				n_info = z_newest.getinfo(n_file)
				save_type = n_info.compress_type
				o_info = z_oldest.getinfo(n_file)
				if n_info.CRC != o_info.CRC:
					print(' * ' + n_file)
					should_patch = True
			else:
				print(' + ' + n_file)
				should_patch = True
			if should_patch:
				n_data = z_newest.read(n_file)
				z_patch.writestr(n_file, n_data, save_type)
		for o_file in o_files:
			if o_file not in n_files:
				z_patch.writestr(n_file + '.delete', ''.encode('utf-8'), zipfile.ZIP_STORED)
				print(' - ' + o_file)

		z_oldest.close()
		z_newest.close()
		z_patch.close()
	elif args.apply is not None:
		z_patch = zipfile.ZipFile(args.apply, 'r')
		if z_patch.desc is not None:
			print("Comment: ", z_patch.desc.decode('UTF-8'))
			os.system('pause')
			
		z_oldest = zipfile.ZipFile(args.file, 'r')
		z_newest = zipfile.ZipFile(args.output, 'w')
		o_files = z_oldest.namelist()
		p_files = z_patch.namelist()
		for o_file in o_files:
			n_info = None
			if o_file in p_files:
				print(' * ' + o_file)
				n_info = z_patch.getinfo(o_file)
				n_data = z_patch.read(o_file)
			else:
				n_info = z_oldest.getinfo(o_file)
				n_data = z_oldest.read(o_file)
			z_newest.writestr(o_file, n_data, n_info.compress_type)
			if o_file + '.delete' in p_files:
				print(' - ' + o_file)
		for p_file in p_files:
			if p_file.endswith('.delete'):
				continue
			if p_file not in o_files:
				print(' + ' + p_file)
				n_data = z_patch.read(p_file)
				n_info = z_patch.getinfo(p_file)
				z_newest.writestr(p_file, n_data, n_info.compress_type)
		z_patch.close()
		z_oldest.close()
		z_newest.close()

	print('All done')