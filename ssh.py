#fastest way to run tasks: asynchronous pool
from multiprocessing import Pool
import time
import os
import sys
import pathlib

import paramiko

#https://stackoverflow.com/questions/3485428/creating-multiple-ssh-connections-at-a-time-using-paramiko
def sshHost(host, private_key):
	print("TEST")
	try:
		key = paramiko.RSAKey.from_private_key_file(private_key)
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(host, username='root', pkey=key)
		stdin, stdout, stderr = client.exec_command('ls -l')
		print(stdout.readlines())
	except:
		print("Oops!",sys.exc_info()[0],"occured.")
		print("Couldn't connect to " + host)


def readFile(filename):
	_file = None
	try:
		#open file in read only mode, raise errors as ValueError
		_file = open(filename, mode='r', errors='strict')
		lines = [line for line in _file]
		#lines = [line.strip() for line in _file if len(line.strip()) > 0]
		_file.close()
		return lines
	except PermissionError as error:
		print("Could not open the file " + filename + " due to insufficient permissions")
		sys.exit(error.errno)
	except FileNotFoundError as error:
		print("Could not find the file " + filename)
		sys.exit(error.errno)
	except OSError:
		print("Could not complete opening the file " + filename)
		sys.exit(error.errno)
	except ValueError:
		print("Could not read the file encoding")
		sys.exit(1)

def readHosts(filename):
	lines = readFile(filename)
	return [line.strip() for line in lines if len(line.strip()) > 0]

def readKey(filename):
	lines

if __name__ == "__main__":
	hosts = readHosts(sys.argv[1])
	print(hosts)
	#check if the key is present
	#use pathlib to expand out ~ and get RSA key
	try:
		key = paramiko.RSAKey.from_private_key_file(str(pathlib.Path.home()) + "/.ssh/developer_key")
	except PasswordRequiredException as e:
		print("Password is required")
		sys.exit(e.errno)
	key = str(pathlib.Path.home()) + "/.ssh/developer_key"
	pool = Pool(processes=10)
	print("TEST")
	#use nohup to maintain the session
	results = [pool.apply_async(sshHost, args=(host, key,)) for host in hosts]
	print([res.get(timeout=10) for res in results])
