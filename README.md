# DigitalOcean simple VPN setup 🐍

Setup your own personal [VPN] server hosted on [DigitalOcean] with a single command.

## Install

Checkout repo and launch:
```shell
git clone https://github.com/GeorgiyDemo/digitalocean_vpn
cd digitalocean_vpn
python3 main.py
```

## Requirements

* [requests]
* [python_digitalocean]

## Configure setup

Read below how to get *YOUR_TOKEN*, *YOUR_FINGERPRINT* and *KEY_DIR*. First is needed to create/destroy droplets by your account, ssh fingerprint and directory is to be able to access created droplet using SSH

Once script is finished, you need to download .ovpn file via wget or web:
```shell
wget -O "ready.ovpn" --no-check-certificate https://IP:8080/ 
```

## Obtain DigitalOcean API key

* Visit https://cloud.digitalocean.com/settings/api/tokens
* Click on "Generate new token" (or skip if you already have it)
* Copy generated token
* Replace "YOUR_TOKEN" string in main.py

## Obtain DIR and DigitalOcean SSH key fingerprint
* Generate new keys:
```shell
ssh-keygen -t RSA
```
* Default *KEY_DIR* is $HOME/.ssh/, but you can replace it by your own
* Visit https://cloud.digitalocean.com/settings/security
* Click on "Add ssh key" (or skip if you already have it)
* Copy ssh key fingerprint
* Replace "YOUR_FINGERPRINT" string in main.py

## Tweak VPN

If you want to modify vpn just replace line 61 in main.py

```python
os.system('ssh -i '+key_dir+' root@'+droplet_ip+' "yum install git -y && git clone https://github.com/georgiydemo/VPN && cd VPN && chmod +x docker.sh && ./docker.sh"')
```

## License

[MIT] - Do whatever you want, attribution is nice but not required

[VPN]: https://en.wikipedia.org/wiki/Virtual_private_network
[DigitalOcean]: https://www.digitalocean.com/
[requests]: https://github.com/requests/requests
[python_digitalocean]: https://github.com/koalalorenzo/python-digitalocean
[MIT]: https://tldrlegal.com/license/mit-license