#!/usr/bin/env python3
import serial
import time

def send_command(ser, command, wait=1):
    """
    Sender en kommando til den serielle porten og venter et gitt antall sekunder.
    """
    ser.write((command + '\r\n').encode('utf-8'))
    time.sleep(wait)

def main():
    # Hent inn variabler fra bruker
    serial_port = input("Seriellport (f.eks. COM3 eller /dev/ttyS3): ")
    baudrate = input("Baudrate (default 9600): ") or "9600"
    device_hostname = input("Gi switchen et hostname (f.eks. SWITCH1): ")
    domain_name = input("Ditt domene (f.eks. example.local): ")
    username = input("Ønsket brukernavn: ")
    password = input("Ønsket passord: ")
    ip = input("IP-Addresse og subnett: ")
    gateway = input("Default Gateway: ")
    key_gen = input("Ønsket key_gen: ")
    vlan1 = input("Ønsket mgmt VLAN: ")
    vlan2 = input("Ønsket bruker VLAN: ")
    interface1 = input("Hvilken interface er trunk?: ")
    interface2 = input("Hvilken interface er trunk?: ")
    interface3 = input("Hvilken interface er access?: ")
    interface4 = input("Hvilken interface er access?: ")
    

    # Koble til seriellport
    try:
        with serial.Serial(port=serial_port, baudrate=int(baudrate), timeout=1) as ser:
            print(f"Koblet til {serial_port} med {baudrate} baud.\n")

            # Forenklet "vent på prompt" – i praksis kan man lese data fra ser, men her antas at vi har CLI tilgjengelig
            time.sleep(2)

            # Gå i enable-modus
            send_command(ser, "enable")
            # Dersom enheten spør om passord for enable, legg inn en send_command(ser, <enable_passord>)

            # Global config
            send_command(ser, "configure terminal")

            # Sett hostname
            send_command(ser, f"hostname {device_hostname}")

            # Sett domene
            send_command(ser, f"ip domain-name {domain_name}")

            # Opprett brukerkonto
            send_command(ser, f"username {username} privilege 15 secret {password}")

            # Generer RSA-nøkkel (1024 bit)
            send_command(ser, f"crypto key generate rsa modulus {key_gen}")
            time.sleep(1)
            
            send_command(ser, f"ip default-gateway {gateway}")
            
            #lag 3
            send_command(ser, f"vlan {vlan1}")
            send_command(ser, f"exit")
            send_command(ser, f"vlan {vlan2}")
            send_command(ser, f"exit")
            send_command(ser, f"interface {interface1}")
            send_command(ser, f"switchport mode trunk")
            send_command(ser, f"exit")
            send_command(ser, f"vlan {vlan1}")
            send_command(ser, f"exit")
            send_command(ser, f"interface {interface2}")
            send_command(ser, f"switchport mode trunk")
            send_command(ser, f"exit")
            send_command(ser, f"interface {interface3}")
            send_command(ser, f"switchport mode access")
            send_command(ser, f"switchport access vlan {vlan1}")
            send_command(ser, f"exit")
            send_command(ser, f"interface {interface4}")
            send_command(ser, f"switchport mode access")
            send_command(ser, f"switchport access vlan {vlan2}")
            send_command(ser, f"exit")
            
            send_command(ser, f"interface Vlan{vlan1}")
            send_command(ser, f"ip add {ip}")
            send_command(ser, f"no shutdown")
            send_command(ser, f"exit")
            


            # Konfigurer VTY-linjer for SSH
            send_command(ser, "line vty 0 4")
            send_command(ser, "transport input ssh")
            send_command(ser, "login local")
            send_command(ser, "exit")

            # (Valgfritt) Deaktiver Telnet
            # send_command(ser, "line vty 0 15")
            # send_command(ser, "transport input none")
            # send_command(ser, "transport input ssh")
            # send_command(ser, "exit")

            print("SSH er nå konfigurert på switchen!\n")
    except serial.SerialException as e:
        print(f"Kunne ikke åpne port {serial_port}: {e}")

if __name__ == "__main__":
    main()