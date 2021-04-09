"""

Currently there is no input validation so the program may crash when not given correct input. 

Works only on linux systems.

Requires Nmap to be installed:
	- sudo apt install python3-nmap
	
For more information about the preset scans I used, visit this link. https://www.securesolutions.no/zenmap-preset-scans/
 
"""

import nmap, re, json, os
from datetime import datetime

# Global variable
scanner = nmap.PortScanner()

def show_banner():
	print("\nNmap Scanner Tool")
	print("-----------------------------------------------------\n")
	

def get_ip():
	ip_addr = input("Enter IP address: ")
	print("The IP you entered is: ", ip_addr)
	return ip_addr

def show_options():
	response = input("""\nEnter Type of Scan:
			1) Ping Scan 
			2) Quick Scan
			3) Quick Scan Plus
			4) Intense Scan
			5) Intense Scan plus UDP (Requires root privileges)
			6) Intense Scan, all tcp ports (Can take 10+ minutes)
			7) Intense Scan, no ping (Can take 5+ minutes)
			8) Check Ports Status
			9) Compare Previous Scans \n""")
			
	print("\nYou have selected option: ", response)
			
	return int(response)

def get_current_time():
	current_time = str(datetime.now())
	# Remove milliseconds
	time = current_time[:-7]
	return time

def output_to_file(result):
	choice = input("""\nScan Complete. \nWould you like to export these results to a text file? 
		       1) Yes
		       2) No\n""")

	choice = int(choice)
	if choice == 1:
		
		# Create a directory to store scans in.
		if os.path.isdir("Scans") == False:
			os.mkdir("Scans")
			
		file_name = ("Scan_results - " + get_current_time() + ".txt")
		text_file= open("Scans/"+file_name, "w")
		text_file.write(str(result))
		text_file.close()
		print("\nResults saved to 'Scans/" + file_name + "'.")
	else:
		print("\nExiting now without saving.\n")
	
		
def check_ports(ip_addr):

	# Port range should be between: 0 - 65535
	
	print("\nPlease specify a range for which ports you want to scan: ")
	port_min = input("Enter min port: ")
	port_max = input("Enter max port: ")
	print()

	# Loop through ports
	for port in range(int(port_min), int(port_max) + 1):
		try:
		    result = scanner.scan(ip_addr, str(port), '-sV')
		    port_status = (result['scan'][ip_addr]['tcp'][port]['state'])
		    print("Port " + str(port) + " is " + str(port_status))
		    
		except:
		    print("Can't scan port " + str(port))
		    
		    
def compare_scans():	

	# Getting current directory to make is easy to copy and paste file scan names.
	directory_path = os.getcwd()
	files_in_directory = os.listdir(directory_path)
	
	print("\nPrevious scans in this directory: \n")
	
	scans_found = 0
	
	for file_name in files_in_directory:
		if("Scan_results" in file_name):
			print("\t" + file_name)
			scans_found = scans_found + 1
	
	if(scans_found == 0):
		print("\tNo scans found. Please run some scans first.")
	else:
		print("\nPlease copy the file names you want to compare into the fields below.")
		file_name1 = input("\nEnter name of first file: ")
		file_name2= input("\nEnter name of second file: ")
		
		file1 = directory_path + "/" + file_name1
		file2 = directory_path + "/" + file_name2

		# Read the scans
		f1 = open(file1, "r")   
		f2 = open(file2, "r")   
		
		print("\nDifferences: \n")
		  
		# Comparing the two files line by line (Credit to: https://origin.geeksforgeeks.org/how-to-compare-two-text-files-in-python/)
		i = 0
		  
		for line1 in f1: 
			i += 1
			  
			for line2 in f2: 
				  
				# matching line1 from both files 
				if line1 != line2:   
					print("Line ", i, ":") 
					# else print that line from both files 
					print("\tFile 1:", line1, end='') 
					print("\tFile 2:", line2, end='') 
				break
		   
		f1.close()                                        
		f2.close()     
	
	
def run_scan(ip_addr, user_option):
	
	# Ping Scan
	if user_option == 1:
	   # print("Nmap Version: ", scanner.nmap_version())
		print("\nStarting scan now, this may take a while...")
		result = scanner.scan(ip_addr, arguments='-sn')
		json_result=json.dumps(result, indent=4, sort_keys=True)
		print(json_result)
		output_to_file(json_result)
	   
	# Quick Scan
	elif user_option == 2:
		#print("Nmap Version: ", scanner.nmap_version())
		print("\nStarting scan now, this may take a while...")
		result = scanner.scan(ip_addr, arguments='-T4 -F')
		json_result=json.dumps(result, indent=4, sort_keys=True)
		print(json_result)

		output_to_file(json_result)

	# Quick Scan Plus
	elif user_option == 3:
		#print("Nmap Version: ", scanner.nmap_version())
		print("\nStarting scan now, this may take a while...")
		result = scanner.scan(ip_addr, arguments='-T4 -F')
		json_result=json.dumps(result, indent=4, sort_keys=True)
		print(json_result)

		output_to_file(json_result)

	# Intense Scan
	elif user_option == 4:
		#print("Nmap Version: ", scanner.nmap_version())
		print("\nStarting scan now, this may take a while...")
		result = scanner.scan(ip_addr, arguments='-T4 -A -v')
		json_result=json.dumps(result, indent=4, sort_keys=True)
		print(json_result)
		
		output_to_file(json_result)

	# Intense Scan plus UDP
	elif user_option == 5:
		#print("Nmap Version: ", scanner.nmap_version())
		print("\nStarting scan now, this may take a while...")
		result = scanner.scan(ip_addr, arguments='-sS -sU -T4 -A -v')
		json_result=json.dumps(result, indent=4, sort_keys=True)
		print(json_result)
		
		output_to_file(json_result)

	# Intense Scan, all TCP ports
	elif user_option == 6:
		#print("Nmap Version: ", scanner.nmap_version())
		print("\nStarting scan now, this may take a while...")
		result = scanner.scan(ip_addr, arguments='-p 1-65535 -T4 -A -v')
		json_result=json.dumps(result, indent=4, sort_keys=True)
		print(json_result)
		
		output_to_file(json_result)

	# Intense Scan, no ping
	elif user_option == 7:
		#print("Nmap Version: ", scanner.nmap_version())
		print("\nStarting scan now, this may take a while...")
		result =scanner.scan(ip_addr, arguments='-T4 -A -v -Pn')
		json_result=json.dumps(result, indent=4, sort_keys=True)
		print(json_result)
		
		output_to_file(json_result)

	elif user_option == 8:
		check_ports(ip_addr)
		
	elif user_option == 9:
		compare_scans()

	else:
		print("Please enter a valid option")

def main():
	show_banner()
	user_option = show_options()
	
	# Skips the IP address function for comparing text files as it is not needed.
	if (user_option != 9):
		ip_addr = get_ip()
	else:
	# Assigning a placeholder value
		ip_addr = ''
		
	run_scan(ip_addr, user_option)

if __name__== "__main__":
	main()
