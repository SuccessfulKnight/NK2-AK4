#!/usr/bin/env python3
import serial
import time

def send_command(ser, command, wait=10):
    ser.write((command + '\r\n').encode('utf-8'))
    time.sleep(wait)

def main():
    # Hent inn variabler fra bruker
    serial_port = input("Seriellport (f.eks. COM4 eller /dev/ttyUSB0): ")
    baudrate = input("Baudrate (default 9600): ") or "9600"
    device_hostname = input("Gi ruteren et hostname (f.eks. ROUTER1): ")
    domain_name = input("Ditt domene (f.eks. example.local): ")
    ip1 = input("IP-Addresse og subnett på lag3 port?: ")
    ip2 = input("IP-Addresse og subnett på lag2 port?: ")
    username = input("Ønsket brukernavn: ")
    password = input("Ønsket passord: ")
    key_gen = input("Ønsket key_gen: ")
    vlnet = input("Ønsket Vlan network på lag 3 siden: ")
    vlnet2 = input("Ønsket Vlan network på lag 2 siden: ")
    vlan = input("Ønsket Vlan: ")
    vlip1 = input("Ønsket VLAN IP og subnett på lag 3?: ")
    vlip2 = input("Ønsket VLAN IP og subnett på lag 2?: ")
    inter = input("Hva slags interface er i bruk? som f.eks GiagabitEthernet eller FastEthernet")
    nummer1 = input("Hva er nummeret på interfacen på lag 3?: ")
    nummer2 = input("Hva er nummeret på interfacen på lag 2?: ")

    # Koble til seriellport
    try:
        with serial.Serial(port=serial_port, baudrate=int(baudrate), timeout=1) as ser:
            print(f"Koblet til {serial_port} med {baudrate} baud.\n")
            
            send_command(ser,"no")
            send_command(ser,"yes")
            send_command(ser,"lol")
            
            # Gå i enable-modus
            send_command(ser, "enable")
            # Hvis ruteren spør om passord for enable:
            # send_command(ser, <enable_passord>)

            # Konfigurer SSH
            send_command(ser, "configure terminal")
            send_command(ser, f"hostname {device_hostname}")
            send_command(ser, f"ip domain-name {domain_name}")
            send_command(ser, f"interface {inter}{nummer1}")
            send_command(ser, f"ip add {ip1}")
            send_command(ser, "no shutdown")
            send_command(ser, "exit")
            send_command(ser, f"interface {inter}{nummer1}.{vlan}")
            send_command(ser, f"encapsulation dot1Q {vlan}")
            send_command(ser, f"ip add {vlip1}")
            send_command(ser, "no shutdown")
            send_command(ser, "exit")
            send_command(ser, f"interface {inter}{nummer2}")
            send_command(ser, f"ip add {ip2}")
            send_command(ser, "no shutdown")
            send_command(ser, "exit")
            send_command(ser, f"interface {inter}{nummer2}.{vlan}")
            send_command(ser, f"encapsulation dot1Q {vlan}")
            send_command(ser, f"ip add {vlip2}")
            send_command(ser, "no shutdown")
            send_command(ser, "exit")
            
            # Opprett brukerkonto
            send_command(ser,  f"username {username} privilege 15 secret {password}")

            # Generer RSA-nøkkel (2048 bit)
            send_command(ser, f"crypto key generate rsa modulus {key_gen}")
            
            send_command(ser, f"access-list 12 permit {vlnet} 0.0.0.255")
            send_command(ser, f"access-list 13 permit {vlnet2} 0.0.0.255")
            send_command(ser, "access-list 14 deny 10.10.125.0 0.0.0.255")
            
            send_command(ser, f"ip route 0.0.0.0 0.0.0.0 gig{nummer1}")
            send_command(ser, f"ip route 0.0.0.0 0.0.0.0 gig{nummer2}")

            # Konfigurer linjer for SSH
            
            send_command(ser, "line vty 0 4")
            send_command(ser, "access-class 12 in")
            send_command(ser, "access-class 13 in")
            send_command(ser, "access-class 14 in")
            send_command(ser, "transport input ssh")
            send_command(ser, "login local")
            send_command(ser, "exit")

            print("SSH er nå konfigurert på ruteren!\n")
    except serial.SerialException as e:
        print(f"Kunne ikke åpne port {serial_port}: {e}")

if __name__ == "__main__":
    main()
