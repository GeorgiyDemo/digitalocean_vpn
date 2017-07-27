import digitalocean, random, requests, time, os
from random import choice
from string import digits

ssh_fingerprint = "YOUR_FINGERPRINT"
key = "YOUR_TOKEN"
key_dir = str(os.path.expanduser("~"))+"/.ssh/KEY"

location_list = ["ams2","sgp1","lon1","ams3","fra1","tor1","blr1"]
location_names ={"ams2": "Amsterdam2 (Nederlands)",
				 "sgp1": "Singapore1 (Singapore)",
				 "lon1": "London1 (United Kingdom)",
				 "ams3": "Amsterdam3 (Nederlands)",
				 "fra1": "Frankfurt1 (Germany)",
				 "tor1": "Torronto1 (Canada)",
				 "blr1": "Bengaluru1 (India)",
				}
buf_location = ""
buf_name = ""

manager = digitalocean.Manager(token=key)

def create():

	ssh_keys = manager.get_all_sshkeys()
	buf_name = ''.join(choice(digits) for i in range(6))
	buf_location = location_list[random.randint(0,6)]
	droplet = digitalocean.Droplet(token=key,
		                            name="Droplet"+buf_name,
		                            region=buf_location,
		                            image='centos-7-x64',
		                            size_slug='512mb',
		                            ssh_keys=ssh_keys)
	droplet.create()

	actions = droplet.get_actions()
	for action in actions:
		action.load()

		if (action.status == "in-progress"):
			print("* New droplet '"+"Droplet"+buf_name+"' in "+location_names[str(buf_location)])
			headers = {'Content-Type': 'application/json','Authorization': 'Bearer '+key}
			r = requests.get("https://api.digitalocean.com/v2/droplets?page=1&per_page=50", headers=headers).json()
			droplet_id = r["droplets"][len(r["droplets"])-1]["id"]
			print("* Droplet's ID: "+str(droplet_id))

			#Adding tags to the droplet
			tag = digitalocean.Tag(token=key, name=buf_name)
			tag.create()
			tag.add_droplets(str(droplet_id))
			print("* Tag "+str(buf_name)+" was added to droplet's ID "+str(droplet_id))

			#Getting droplet's IP
			r = requests.get("https://api.digitalocean.com/v2/droplets?page=1&per_page=1&tag_name="+buf_name, headers=headers).json()
			droplet_ip = r["droplets"][0]["networks"]["v4"][0]["ip_address"]
			print("* Droplet's IP: "+str(droplet_ip)+"\n* Waiting for ssh connection (1 min)..")
			
			#SSH connection
			time.sleep(60)
			print("* Let's go!")
			os.system('ssh -i '+key_dir+' root@'+droplet_ip+' "yum install git -y && git clone https://github.com/georgiydemo/VPN && cd VPN && chmod +x docker.sh && ./docker.sh"')

def destroy():

	tag = input("Input the droplet's tag (numbers after the word 'Droplet')\n=> ")

	headers = {'Content-Type': 'application/json','Authorization': 'Bearer '+key}
	r = requests.delete('https://api.digitalocean.com/v2/droplets?tag_name='+tag, headers=headers)
	if (r.status_code == 204):
		print("Droplet"+tag+"' removed")
	elif (r.status_code == 404):
		print("Droplet with tag '"+tag+"' not found")
	else:
		print("Something went wrong :c")	
		
my_droplets = manager.get_all_droplets()
print("All droplets:")
for i in range(len(my_droplets)):
	print(my_droplets[i])

menu = int(input("\nActions:\n1. Create ovpn server\n2. Remove ovpn server\n=> "))
if (menu == 1):
	create()
if (menu == 2):
	destroy()