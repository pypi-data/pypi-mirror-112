import time
import curses
import sys
from SysInfo import SysInfo

sysinfo = SysInfo()

def main(window):
	curses.curs_set(0)

	arg = sys.argv[1] if len(sys.argv) > 1 else None

	while True:
		window.clear()

		data = sysinfo.get_data(arg)

		try:
			window.addstr(0, 0, data)
		except curses.error:
			pass

		window.refresh()

		time.sleep(0.5)

curses.wrapper(main)