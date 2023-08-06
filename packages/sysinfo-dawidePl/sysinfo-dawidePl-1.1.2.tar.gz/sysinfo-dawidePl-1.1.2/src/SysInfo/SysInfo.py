import psutil
import platform
from datetime import datetime

class SysInfo(object):
	def __init__(self):
		self.units = ["", "K", "M", "G", "T", "P"]
		self.factor = 1024
		self.func_dict = {
			'system': self.get_system,
			'uptime': self.get_uptime,
			'cpu': self.get_cpu_data,
			'ram': self.get_ram_data,
			'disk': self.get_disk_data
		}
		self.sys_args = ['system', 'uptime', 'cpu', 'ram', 'disk']
	
	def get_size(self, bytes: int, suffix="B") -> str:
		for unit in self.units:
			if bytes < self.factor:
				return f"{bytes:.2f}{unit}{suffix}"
			
			bytes /= self.factor
	
	def percentage(self, part, whole, precision = 1) -> str:
		return f"{float(part)/float(whole):.{int(precision)}%}"

	def get_system(self) -> str:
		distro = platform.linux_distribution()

		return f"{platform.system()} {' '.join(distro)}"
	
	def get_uptime(self) -> str:
		bt = datetime.fromtimestamp(psutil.boot_time())

		return f"{bt.day} days {bt.hour}h {bt.minute}m {bt.second}s"
	
	def get_cpu_data(self) -> str:
		usage = f"{psutil.cpu_percent()}%"
		frequency = f"{psutil.cpu_freq().current:.2f}Mhz"

		return f"CPU usage: {usage}\nCPU Frequency: {frequency}"
	
	def get_ram_data(self) -> str:
		ram = psutil.virtual_memory()

		total = self.get_size(ram.total)
		used = self.get_size(ram.used)
		used_percent = self.percentage(ram.used, ram.total)

		return f"{used} of {total} ( {used_percent} ) of RAM is used."
	
	def get_disk_data(self, show_partitions : bool = False) -> str:
		partitions = psutil.disk_partitions()

		if show_partitions:
			partition_info = []

			for partition in partitions:
				try:
					partition_usage = psutil.disk_usage(partition.mountpoint)
				except PermissionError:
					continue
					
				total = self.get_size(partition_usage.total)
				used = self.get_size(partition_usage.used)
				used_percentage = self.get_size(partition_usage.percent)

				partition_info.append(f"{used} of {total} ( {used_percentage} ) of disk space is used.")
			
			return "\n".join(partition_info)
		else:
			sum_total = 0
			sum_used = 0

			for partition in partitions:
				try:
					partition_usage = psutil.disk_usage(partition.mountpoint)
				except PermissionError:
					continue
				
				sum_total += partition_usage.total
				sum_used += partition_usage.used
			
			sum_used_percent = self.percentage(sum_used, sum_total)
			sum_total = self.get_size(sum_total)
			sum_used = self.get_size(sum_used)

			return f"{sum_used} of {sum_total} ( {sum_used_percent} ) of disk space is used."


	# ----------------------------------------------------

	def data(self) -> str:
		system = self.get_system()
		uptime = self.get_uptime()
		cpu_data = self.get_cpu_data()
		ram_data = self.get_ram_data()
		disk_data = self.get_disk_data()

		return f"{system}\n\nUptime: {uptime}\n\n{cpu_data}\n\nRAM data:\n{ram_data}\n\nDisk data:\n{disk_data}"
	
	def get_data(self, sys_arg: str) -> str:
		if sys_arg == "help":
			available_args = []

			for key in self.func_dict:
				available_args.append(key)
			
			return "Available arguments:\n{}".format('\n'.join(available_args))

		elif sys_arg in self.sys_args:
			return self.func_dict[sys_arg]()
		else:
			return self.data()