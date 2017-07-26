import digitalocean, random, requests, time, os
from random import choice
from string import digits

ssh_fingerprint = "YOUR_FINGERPRINT"
key = "YOUR_TOKEN"
key_dir = str(os.path.expanduser("~"))+"/.ssh/KEY"

location_list = ["ams2","sgp1","lon1","ams3","fra1","tor1","blr1"]
buf_location =""
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
		    print("* Создали новый дроплет '"+"Droplet"+buf_name+"' в "+str(buf_location))
		    headers = {'Content-Type': 'application/json','Authorization': 'Bearer '+key}
		    r = requests.get("https://api.digitalocean.com/v2/droplets?page=1&per_page=50", headers=headers).json()
		    droplet_id = r["droplets"][len(r["droplets"])-1]["id"]
		    print("* ID созданного дроплета: "+str(droplet_id))

		    #Добавляем теги к последнему созданному дроплету
		    tag = digitalocean.Tag(token=key, name=buf_name)
		    tag.create()
		    tag.add_droplets(str(droplet_id))
		    print("* Добавили тег "+str(buf_name)+" к дроплету с ID "+str(droplet_id))

		    #Получаем IP дроплета по тегу
		    r = requests.get("https://api.digitalocean.com/v2/droplets?page=1&per_page=1&tag_name="+buf_name, headers=headers).json()
		    droplet_ip = r["droplets"][0]["networks"]["v4"][0]["ip_address"]
		    print("* IP созданного дроплета: "+str(droplet_ip)+"\n* Ожидание развертки ssh (+-60 сек.)")

		    #Подключаемся к дроплету через SSH по ключам, чуть ждем
		    time.sleep(60)
		    print("* Исполняем основной сценарий..")
		    os.system('ssh -i '+key_dir+' root@'+droplet_ip+' "yum install git -y && git clone https://github.com/georgiydemo/VPN && cd VPN && chmod +x docker.sh && ./docker.sh"')

def destroy():

	tag = input("Введите тег дроплета (цифры после слова Droplet)\n=> ")

	headers = {'Content-Type': 'application/json','Authorization': 'Bearer '+key}
	r = requests.delete('https://api.digitalocean.com/v2/droplets?tag_name='+tag, headers=headers)
	if (r.status_code == 204):
		print("Успешно удалили дроплет 'Droplet"+tag+"'")
	elif (r.status_code == 404):
		print("Дроплет с тегом '"+tag+"' не найден")
	else:
		print("Ой! Что-то пошло не так")	
		
my_droplets = manager.get_all_droplets()
print("Текущие серверы на аккаунте:")
for i in range(len(my_droplets)):
	print(my_droplets[i])

menu = int(input("\nДействия:\n1. Создать ovpn-сервер\n2. Удалить ovpn-сервер\n=> "))
if (menu == 1):
	create()
if (menu == 2):
	destroy()