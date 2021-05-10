import subprocess
import pyautogui
import keyboard
import psutil
import threading
import logging
import sys
import os
from time import sleep

logs_path = r'D:\logs'

logging.basicConfig(level = logging.DEBUG,
					format = '%(asctime)s : %(levelname)s : %(message)s',
					filename = os.path.join(logs_path, 'Converter.log'),
					filemode = 'w')

pyautogui.FAILSAFE = False

percent = 97
program = 'converter.exe'
i_sp = None

def main():
	global t2, i_sp
	logging.debug('def "main"')
	print('Working...')
	point = 0
	while True:
		try:
			tasks = subprocess.check_output(['tasklist'], stdin = None, stderr = None, universal_newlines = False, shell = False)
			logging.debug('Check')
			tasks = tasks.decode(encoding = 'ascii', errors = 'ignore').replace('\r', '').split('\n');               logging.debug('Decode')
			break
		except subprocess.CalledProcessError:
			logging.debug('Process not found')
			continue
	t2.start()
	while True:
		logging.debug('Start')
		try:
			while True:
				if i_sp is None:
					for i in tasks:
						if program in i:
							del  tasks[tasks.index(i) + 1:];                 logging.debug('Tasks['+ str(tasks.index(i) + 1) + ':] deleted')
							i_sp = i.split()
							p = psutil.Process(int(i_sp[1]))
				if keyboard.is_pressed('p'):
					logging.debug('Users pause')
					while not keyboard.is_pressed('c'):
						sleep(1)
					logging.debug('Users continue')
				try:
					pyautogui.click('continue.png') if pyautogui.locateOnScreen('continue.png') else None				
				except pyautogui.ImageNotFoundException:
					try:
						pyautogui.click('continue1.png') if pyautogui.locateOnScreen('continue1.png') else None
					except pyautogui.ImageNotFoundException:
						pass
				try:
					for i in tasks:
						logging.debug(i)
						if program not in i:
							del i
							continue
						logging.debug('PID = ' + i_sp[1]); 												 logging.debug('Memory: '+ i_sp[-1])
						if (int(i_sp[-1]) > 310000) or int(psutil.cpu_percent()) > percent:
							sleep(20); 																		   logging.debug('Sleep on max')
							pyautogui.click('pause.png'); 									logging.debug('Pause. Memory: ' + str(i_sp[-1]))
							while (int(i_sp[-1]) > 300000 and int(psutil.cpu_percent()) > 80) or (int(psutil.cpu_percent()) > percent):
								sleep(0.5)
							logging.debug('Memory after sleeping: ', i_sp[-1], end = '\t\t\r')
							pyautogui.click('continue.png'); 													   logging.debug('Continue')
						if pyautogui.locateOnScreen('convertation.png'):
							point += 1
							if point > 1:
								break
				except TypeError:
					continue
		except KeyboardInterrupt:
			print('End\t\t\t')
			input()
			logging.debug('KeyboardInterrupt. Exit of program')
			sys.exit()

def timer():
	global percent, i_sp
	logging.debug('def "timer"')
	i = -1
	k = 0
	try:
		while True:
			if keyboard.is_pressed('p'):
				logging.debug('Users pause')
				while not keyboard.is_pressed('c'):
					sleep(0.01)
				logging.debug('Users continue')
			elif keyboard.is_pressed('e'):
				logging.debug('Users exit')
				sys.exit()
			sleep(1)

			i += 1
			if i < 60:
				print(str(i) + ' s', end = '\t\r')
			elif 60 < i < 3600:
				print(str(i//60) + ' min ' + str(i%60) + ' s', end = '\t\r')

			k += 1
			if k == 30:
				k = 0
				if program not in subprocess.check_output(['tasklist'], stdin = None, stderr = None, shell = False, 
										universal_newlines = False).decode(encoding = 'ascii', errors = 'ignore'):
					logging.debug('Program not in tasklist')
					sys.exit()
				else:
					i_sp = None
	except KeyboardInterrupt:
		print('End\t\t\t')
		input(); 																		 logging.debug('KeyboardInterrupt. Exit of program')
		sys.exit()

if __name__ == '__main__':
	t1 = threading.Thread(target = main, args = ())
	t2 = threading.Thread(target = timer, args = ())
	t1.start()