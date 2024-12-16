# TP2 : QUENTIN LANGUILLON

🌞 **Configuration de `router.tp2.efrei`**

Mise d'ip fixe a router.tp2.efrei en 10.2.1.254 en modifiant le fichier sysconf pour la carte enp0s8

Recuperation ip du NAT de GNS3 en cnfigurant le meme fichier mais la carte enp0s3

Verification de connection au NAT (enp0s3)et ip fixe(enp0s8) via: 
```
[rocky@localhost *]$ ip a
1: 10: ‹LOOPBACK, UP, LOWERUP> mtu 65536 gdisc noqueue state UNKNOWN group default qlen 1000
link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
inet 127.0.0.1/8 scope host lo
valid_ift forever preferred_Ift forever
inet6 ::1/128 scope host
valid lft forever preferred_ift forever

2: enpOs3: <BROADCAST, MULTICAST,UP ,LOUER UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
link/ether 08:00:27:1f:00:72 brd ff:ff:ff:ff:ff:ff
inet 192.168.122.247/24 brd 192.168.122.255 scope global dynamic nopref ixroute enpis3
valid_Ift 2646sec preferred_ift 2646sec
inet6 fe80::a00:27ff :felf:72/64 scope link
valid_ift forever preferred_Ift forever

3: enp@s8: <BROADCAST,MULTICAST,UP, LOWER UP > mtu
Tinkether 88:08:27:80:94:43 brd WER Tit 15disc fq codel state UP group default glen 188a
inet 10.2.1.254/24 brd 10.2.1.255 scope global nopref ixroute enpßs8
valid ift forever preferred_ift forever
ineto feß0: :a00:27ff:fe80:948/64 scope link
valid_ift forever preferred_ift forever
```
###### Lancer ping pour verifier connexion internet: 
```
[rocky@localhost *]$ ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 tt1=61 time=23.4 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=61 time=26.7 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=61 time=30.9 ms
64 bytes from 8.8.8.8: icmp_seg=4 ttl=61 time=74.7 ms
-- 8.8.8.8 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3009ms
rtt min/aug/max/mdev = 23.354/38.909/74.700/20.834 ms
``` 
###### Autoriser les communications dans le routeur.tp2.efrei:s
```bash
# autoriser la comm
[rocky@localhost *]$ sudo firewall-cmd --add-masquerade
success

# ajout la relance meme apres reboot
[rocky@localhost *]$ sudo firewall-cmd --add-masquerade --permanent
success
```

🌞 **Configuration de `node1.tp2.efrei`**

###### Mettre une ip statique en 10.2.1.1 avec la commande:
```
ip 10.2.1.1
```
###### Mettre en place la route par default avec ip router:
```
ip 10.2.1.1 255.255.255.0 10.2.1.254
```
###### Verifier la config en faisant un ping vers internet:
```
PC1> ping 10.2,1.254
64 bytes from 10,2,1,254 icmp_seq=1 ttl=64 time=1,604 ms
64 bytes from 10,2,1,254 icmp_seq=2 ttl=64 time=2.077 ms
64 bytes from 10,2,1,254 icmp_seq=3 ttl=64 time=1,989 ms
64 bytes from 10,2,1,254 icmp_seq=4 ttl=64 time=1,630 ms
64 bytes from 10,2,1,254 icmp_seq=5 ttl=64 time=1,964 ms

```
###### Verifier via traceroute:
```
trace 8.8.8.8
trace to 8,8.8,8, 8 hops max, press CtrI+C to stop
 1  10.2.1.254   1.498 ms 0.853 ms 1.142 ms
 2  192.168.122.1   1.947 ms 1.692 ms 1.599 ms
 3  10.0.3.2   1.424 ms 0.496 ms 0.513 ms
 4  *  *  *
 5  *  *  *
 6  213.19.202.145   63.774 ms 97.896 ms 101.960 ms
 7  171.75.10.21   100.460 ms 102,698 ms 99.468 ms
 8  4.68.70.210   101.944 ms 71.409 ms 137.059 ms
```


🌞 **Afficher la CAM Table du switch**
Affichage de la CAM table via la commande:
```
IOU1#show mac address-table
              Mac Address Table
------------------------------------------------------

Vlan      Mac Address           Type            Ports
----      -----------           -------         ------
   1      0050.7966.6800        DYNAMIC         Et1/2
   1      0800.2780.9d48        DYNAMIC         Et0/3
Total Mac Addresses for this criterion: 2
```

🌞 **Install et conf du serveur DHCP** sur `dhcp.tp2.efrei`
Création d'une deuxieme rocky
Installation dhcp-server
Mise en place config dhcpd comme vu sur tp1
```
authoritative;
subnet 10.2.1.0 netmask 255.255.255.0 {
	range 10.2.1.10 10.2.1.50;
	option broadcast-address 10.2.1.1;
	option routers 10.2.1.254;
}
```
Et application de la config avec la commande:
```
systemctl enable --now dhcpd
```


🌞 **Test du DHCP** sur `node1.tp2.efrei`
##### info de base
```
VPCS> show ip
NAME            :VPCS[1]
IP/MASK         :10.2.1.1/24
GATEWAY         :10.2.1.254
DNS
МАС             :00:50:79:66:68:00
LPORT           :20006    
RHOST: PORT     :127.0.0.1:20007
MTU             :1500
```
##### Tentative de recuperation ip :
```
VPCS> dhop
DDORA IP 10.2,1,10/24 GW 10,2.1.254
```
##### Addresse reçu par le dhcp vérification config:
```
VPCS> show ip

NAME          : VPCS[1]
IP/MASK       : 10.2.1.10/24
GATEWAY       : 10.2.1.254
DNS           : -
DHCP SERVER   : 10.2.1.253
DHCP LEASE    : 43149, 43200/21600/37800
MAC           : 00:50:79:66:68:00
LPORT         : 20006
RHOST:PORT    : 127.0.0.1:20007
MTU           : 1500
```



🌞 **Wireshark it !**

[trame dora](DORA-wire.pcapng)

On peut voir dans le Offer du DORA l'ip proposé par le dhcp


# III. ARP

## 1. Les tables ARP

🌞 **Affichez la table ARP de `router.tp2.efrei`**

Affichage table arp pour verifier les que les deux machines sont présente:
```
VPCS> arp
08:00:27:80:9d: 48    10.2,1,254 expires in 92 seconds  (node1.tp2.efrei)
08:00:27:49:a0:17     10,2,1,253 expires in 115 seconds (dhcp.tp2.efrei)
```

🌞 **Capturez l'échange ARP avec Wireshark**
[trame arp](Arp-request-dhcp.pcapng)

## 2. ARP poisoning

**Insérer une machine attaquante dans la topologie. Un Kali linux, ou n'importe quel autre OS de votre choix.**

🌞 **Envoyer une trame ARP arbitraire**

Mise en place de Kali et commande arping sur victime:
```
sudo arping -c 1 -U -s 01:02:03:04:05:06 -S 1.2.3.4 10.2.1.10
```
utilisation d'argument:
-c 1 : Envoie une seule trame ARP.
-U : Force une mise à jour ARP unicast vers la cible.
-s : Spécifie une adresse MAC falsifiée.
-S : Spécifie une adresse IP falsifiée.

Resultat commande:
```
arping -c 1 -U -s 01:02:03:04:05:06 -S 1.2.3.4 10.2.1.10
ARPING 10.2.1.10
Timeout

--- 10.2.1.10 statistics ---
1 packets transmitted, 0 packets received, 100% unanswered (0 extra)
```
On peut voir la trame avec Wireshark
[trame arping](arping-request.pcapng)

🌞 **Mettre en place un ARP MITM**
Activation IP forwarding en modifiant le fichier /proc/sys/net/ipv4/ip_forward
Modification de la ligne passant de 0 à 1
Utilisation de arpspoof pour pranker la victime et le routeur
```
sudo arpspoof -i eth0 -t 10.2.1.10(v) 10.2.1.254(r)
sudo arpspoof -i eth0 -t 10.2.1.254(r) 10.2.1.10(v)
```

🌞 **Capture Wireshark `arp_mitm.pcap`**
Recuperation des échanges d'un ping 1.1.1.1 partant de victime et passant par routeur
[trame arparp_mitm](Ping-Victime-Vu-par-Kali.pcapng)

🌞 **Réaliser la même attaque avec Scapy**


[script python](HAAAAAAAAAAAAAAAAAAAAAA.py)