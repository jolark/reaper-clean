"""
Reaper Cleaning script
"""
import os
from shutil import copyfile

def simplename(path):
	return path.split('\\')[-1]

def parse_reaper_filename(line):
	return line.split(' ')[-1].strip()[1:-1]

def is_wav_file_line(line):
	row = line.split(' ')
	return len(row) == 10 and row[-2] == 'FILE' and row[-1].endswith('.wav"\n')

def copy_to_newdir(path, file, newdir):
	copyfile(path + '/' + file, path + '/' + newdir + '/' + file)

def clean():
	path = os.getcwd()
	for file in os.listdir(path):
		if file.endswith('.rpp'):
			projectname = file[:-4]
			if not os.path.isdir(projectname):
				os.mkdir(projectname)
			# copy RPP in new folder
			copy_to_newdir(path, file, projectname)
			# copy RPP-BAK in new folder
			if os.path.exists(file + '-bak'):
				copy_to_newdir(path, file + '-bak', projectname)
			with open(file, 'r') as f:
				for line in f:
					if is_wav_file_line(line):
						wav = parse_reaper_filename(line)
						try:
							# copy WAV in new folder
							copy_to_newdir(path, wav, projectname)
							# copy REAPEAKS file in new folder
							rpk = wav + '.reapeaks'
							try:
								copy_to_newdir(path, rpk, projectname)
							except Exception as e:
								print('.reapeaks file not found for: ' + wav)
						except Exception as e:
							print('WAV file "' + wav + '" not in this folder and won\'t be cleaned.')
			f.close()

def main():
	clean()

if __name__ == '__main__':
	main()