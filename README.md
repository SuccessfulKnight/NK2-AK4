# NK2-AK4
 
Innhold

    -ssh-router.py - Python script for grunnleggende set up av LAN og ssh på router

    - switch-router.py - Python script for

    - hsrp.yaml - Ansible Playbook script for oppsett av HSRP på både mgmt VLAN og bruker VLAN

    - dhcp.yaml - Ansible Playbook script for oppsett av DHCP på bruker VLAN

    - etherchannel.yaml - Ansible Playbook for oppsett Etherchannel Trunk

    - vlan.yaml - Anisble Playbook for å legge til VLAN på enheter

Forutsetninger

    - Python3 installert

    - pyserial er installert med pip install pyserial

    - Ansible installert

    - Seriellkabel koblet til routere eller switcher (Kun nødvendig for bruk av python script)

Set opp router

    - Kjør ssh-router.py 
        - sørg at du er tilkoblet cisco routeren med seriell kabel og hvilken input er brukt som f.eks COM1 eller /dev/tty0
    - Baudrate eller speed er har en standard på 9600 så du kan bare trykke enter
    - hva skal hostname på routeren skal være som f.eks (ciscorouter1)
    - Hva skal domene være f.eks (cisco.local)
    - IP på lag 3 er koblingen til routeren med lager 3 switchen
    - IP på lag 2 er koblingen til routeren med lager 2 switchene 
    - Username er brukernavnet du skal bruke for å SSH inn på routeren
    - Password er passordet du skal bruker for å SSH inn på routeren
    - Key_gen er størrelsen på RSA nøkkelen bruk f.eks 2048
    - VLAN network1 er nettverket på på lag 3 siden for å fikse access-listen bruk f.eks 10.10.12.0
    - VLAN network 2 er nettverkett på lag 2 siden for folse acces--listen bruk f.eks 10.10..13.0
    - VLAN dette blir ditt MGMT VLAN id
    - VLAN ip på subinterfacen på lag 3
    - VLAN ip på subinterface på lag 2
    - Hva slags interface bruker du? f.eks GigabitEthernet eller FastEthernet?
    - Hvilken port bruker du på lag 3 siden som f.esk GigabitEthernet0/1 eller GigabitEthernet1/0/1
    - Hvilken port bruker du på lag 2 siden som f.esk GigabitEthernet0/1 eller GigabitEthernet1/0/1
    - Nå må du bare vente

Set opp Switch
    - Kjør switch-router.py 
        - sørg at du er tilkoblet cisco routeren med seriell kabel og hvilken input er brukt som f.eks COM1 eller /dev/tty0 
    - Baudrate eller speed er har en standard på 9600 så du kan bare trykke enter
    - hva skal hostname på routeren skal være som f.eks (ciscoswitch1)
    - Hva skal domene være f.eks (cisco.local)
    - Username er brukernavnet du skal bruke for å SSH inn på routeren
    - Password er passordet du skal bruker for å SSH inn på routeren
    - Key_gen er størrelsen på RSA nøkkelen bruk f.eks 2048
    - ip som du skal bruke å ssh in velg da vlan IP
    - Gateway er nødvendig på noen switcher for å sette opp SSH gi default gateway til en av routerene
    - VLAN1 er MGMT VLAN som skal brukes med IPen og sørg det er samme VLAN id som på routeren
    - VLAN2 er bruker VLAN
    - Så velger du hva som tilkoblingen som skal trunkes i mot routeren og hvilken er access for mgmt og brukeren

Ansible
    - se i host filen og sett opp riktig IP addresse
    - kjør ansible-playbook -i hosts hsrp.yaml for å sette opp, lag endringer som er nødvendig for deg
    - kjør ansible-playbook -i hosts dhcp.yaml for å sette opp, lag endringer i filen som er nødvendig for deg
    - kjør ansible-playbook -i hosts etherchannel.yaml for å sette opp, lag endringer i filen som er nødvendig for deg