import config
import os
import utils
import threading
import server
from optparse import OptionParser
import logging
import transfer
import json
import time

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S')

def init():
	parse = OptionParser()
	parse.add_option('-v', '--sharefolder', dest='sharefolder', help='folder you tend to share, default current folder')
	parse.add_option('-p', '--port', dest='server_port', help='server port you tend to open for socket, default 8888')
	parse.add_option('-q', '--scan_port', dest='scan_port', help='scan_port port you tend to open for socket')
	parse.add_option('-r', '--scan_server', dest='scan_server', help='scan_server  you tend to open for socket')

	options = parse.parse_args()[0]

	if options.server_port:
		config.server_port = int(options.server_port)
	if options.sharefolder:
		config.shared_folder = options.sharefolder
	if options.scan_port:
		config.scan_port = int( options.scan_port )
	if options.scan_server:
		config.scan_server = options.scan_server
	if not os.path.exists(config.default_save_folder):
		raise Exception("save folder not exists")
	if not os.path.exists(config.shared_folder):
		raise Exception("shared folder not exists")

def get_files(each_ip, rel_path, file_dir_list):

	logging.debug(rel_path)
	data = file_dir_list

	for key, value in sorted(data.items(), key=lambda d: d[1], reverse=True):

		path_list = [os.path.join(rel_path, key)]

		logging.debug("{} {}", key == 'download', key)

		if value and (not key == 'download'):
			transfer_thread = transfer.Client_transfer((each_ip, config.scan_port), json.dumps(path_list))
			transfer_thread.start()

			while not transfer_thread.recvd_content:
				pass

			data = json.loads(transfer_thread.recvd_content)

			dir = os.path.join(config.default_save_folder, rel_path, key)

			logging.debug(dir)

			if not os.path.isdir(dir):
				os.mkdir(dir)
			get_files(each_ip, os.path.join(rel_path, key), data)

		else:
			transfer_thread = transfer.Client_transfer((each_ip, config.scan_port), json.dumps(path_list),
													   os.path.join(config.default_save_folder, rel_path, path_list[-1]))
			transfer_thread.start()


def main():
	init()
	threading.Thread(target=server.server_run).start()

	effective_ip = utils.scan_lan()
	while True:
		for each_ip in effective_ip:
			print(each_ip + ":" + str(config.scan_port))
			transfer_thread = transfer.Client_transfer((each_ip, config.scan_port), "*")
			transfer_thread.start()
			# time.sleep(config.sleep_time)
			while not transfer_thread.recvd_content:
				pass
			data = json.loads(transfer_thread.recvd_content)

			get_files(each_ip, '', data)
		time.sleep(3)



if __name__ == "__main__":
	main()
