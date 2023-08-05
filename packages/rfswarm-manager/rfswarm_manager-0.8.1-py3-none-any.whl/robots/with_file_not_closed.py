import threading
import hashlib
from faker import Faker
import os
import shutil
import tempfile
import random
import time
from datetime import datetime

tempdir = tempfile.gettempdir()
filedir = os.path.join(tempdir, "with_file_not_closed")
files = {}


def hash_file(file):
	BLOCKSIZE = 65536
	hasher = hashlib.md5()
	hasher.update(str(os.path.getmtime(file)).encode('utf-8'))
	with open(file, 'rb') as afile:
		buf = afile.read(BLOCKSIZE)
		while len(buf) > 0:
			hasher.update(buf)
			buf = afile.read(BLOCKSIZE)
	return hasher.hexdigest()

def hasfilechanged(filedata):
	global files
	# print(filedata)
	newhash = hash_file(filedata["Filename"])
	# print("newhash:", newhash)
	if newhash != filedata["Filehash"]:
		print("File Changed:", filedata["Filename"], filedata["Filehash"], newhash)
		fid = filedata["FileID"]
		files[fid]["Filehash"] = newhash
	else:
		# print("File Unhanged:", filedata["Filename"], filedata["Filehash"], newhash)
		pass

def createfile():
	fdata = {}
	fake = Faker()
	fid = fake.name().replace(" ", "_")
	fname = os.path.join(filedir, fid + ".txt")
	fdata["FileID"] = fid
	fdata["Filename"] = fname
	fdata["Filehash"] = None
	with open(fname, "a") as f:
		for x in range(random.randrange(10)):
			f.write(fake.text())
	return fdata


def threadlancher():
	while True:
		print("		threadlancher:", datetime.now().isoformat(sep=' ',timespec='seconds'))
		# print(files)
		for f in files:
			# print(f)
			file= files[f]
			t = threading.Thread(target=hasfilechanged, args=(file, ))
			t.start()

		time.sleep(5)


# clean up any files from previous runs
if os.path.exists(filedir):
	if os.path.isdir(filedir):
		shutil.rmtree(filedir)
	if os.path.isfile(filedir):
		os.remove(filedir)

os.mkdir(filedir)

# create some ramdom files
for x in range(10):
	fdata = createfile()
	fid = fdata["FileID"]
	files[fid] = fdata

threadlancher()
