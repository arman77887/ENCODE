import requests
import time
import os
import sys
from datetime import datetime

class StudentsInformationSystem:
    def __init__(self):
        self.username = "Haq Cyber Squad"
        self.password = "Safwan Al Sadaf"
        self.login_attempts = 0
        self.max_attempts = 3
        self.session = requests.Session()
        self.version = "Professional Edition v3.0"
        self.setup_headers()
    
    def setup_headers(self):
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/json',
            'Connection': 'keep-alive'
        })
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_red_banner(self):
        self.clear_screen()
        print("\033[91m")
        print("=" * 80)
        print(" " * 25 + "STUDENTS INFORMATION SYSTEM")
        print("=" * 80)
        print("\033[0m")
    
    def login_system(self):
        while self.login_attempts < self.max_attempts:
            self.display_red_banner()
            
            print("\n" + "=" * 40)
            print("          SECURE LOGIN PORTAL")
            print("=" * 40)
            
            username_input = input("\nEnter Username: ")
            password_input = input("Enter Password: ")
            
            if username_input == self.username and password_input == self.password:
                print("\n\033[92m✓ Authentication Successful! Initializing System...\033[0m")
                time.sleep(2)
                return True
            else:
                self.login_attempts += 1
                rem = self.max_attempts - self.login_attempts
                print(f"\n\033[91m✗ Invalid credentials! {rem} attempts remaining.\033[0m")
                time.sleep(2)
                
                if self.login_attempts >= self.max_attempts:
                    print("\n\033[91m🚫 Maximum login attempts exceeded. System locking...\033[0m")
                    time.sleep(3)
                    return False
        
        return False
    
    def display_developer_info(self):
        print("\033[96m")
        print("╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║                         DEVELOPMENT TEAM INFORMATION                        ║")
        print("╠══════════════════════════════════════════════════════════════════════════════╣")
        print("║                                                                              ║")
        print("║     Organization:    Haq Cyber Squad                                         ║")
        print("║     Lead Developer:  Safwan Al-Sadaf                                         ║")
        print("║     Project Manager: Haq Cyber Team                                          ║")
        print("║     System Architect: Security Research Division                             ║")
        print("║     Mobile Division: Haq Cyber Mobile Team                                   ║")
        print("║     Web Division:    Haq Cyber Web Team                                      ║")
        print("║                                                                              ║")
        print("╠══════════════════════════════════════════════════════════════════════════════╣")
        print("\033[0m")
    
    def display_dashboard(self):
        self.clear_screen()
        print("\033[95m")
        print("=" * 80)
        print(" " * 20 + "🏫 STUDENTS INFORMATION SYSTEM - PROFESSIONAL EDITION")
        print("=" * 80)
        print("\033[0m")
        self.display_developer_info()
    

    # ------------------------ FIXED: REAL API INTEGRATION ------------------------
    def get_real_student_data(self, eiin):
        """Fetch real student data from API server."""
        try:
            api_url = f"https://lmnx9.appletolha.com/eiin.info?eiin={eiin}"
            print(f"\n\033[93m📡 Connecting to Server...\033[0m")
            
            response = self.session.get(api_url, timeout=10)
            response.raise_for_status()

            info = response.json()   # Root JSON (NO "result")

            return {
                "eiin": info.get("eiinNo", "N/A"),
                "institute": info.get("instituteName", "N/A"),
                "institute_bn": info.get("instituteNameBn", "N/A"),
                "division": info.get("divisionName", "N/A"),
                "district": info.get("districtName", "N/A"),
                "thana": info.get("thanaName", "N/A"),
                "type": info.get("instituteTypeName", "N/A"),
                "mobile": info.get("mobile", "N/A"),
                "email": info.get("email", "N/A"),
                "address": info.get("mouzaNameBn", "N/A")
            }

        except Exception as e:
            print(f"\033[91m⚠️ API Error: {str(e)}\033[0m")
            return None
    # ---------------------------------------------------------------------


    def fetch_student_info(self, eiin):
        try:
            print(f"\n\033[93m🔍 Searching Server for EIIN: {eiin}\033[0m")
            time.sleep(1)

            student_data = self.get_real_student_data(eiin)
            return student_data

        except Exception as e:
            print(f"\033[91m⚠️ Error fetching data: {str(e)}\033[0m")
            return None
    

    def display_student_info(self, s):
        print("\n" + "=" * 70)
        print(" " * 20 + "🎓 INSTITUTE INFORMATION")
        print("=" * 70)
        
        if s:
            print(f"\n\033[94m📝 Institute Details:\033[0m")
            print("-" * 50)
            print(f"  • EIIN: {s['eiin']}")
            print(f"  • Institute: {s['institute']}")
            print(f"  • Institute (BN): {s['institute_bn']}")
            print(f"  • Division: {s['division']}")
            print(f"  • District: {s['district']}")
            print(f"  • Thana: {s['thana']}")
            print(f"  • Address: {s['address']}")
            print(f"  • Type: {s['type']}")
            print(f"  • Mobile: {s['mobile']}")
            print(f"  • Email: {s['email']}")
        else:
            print("\033[91m❌ No information found.\033[0m")
        
        print("=" * 70)
    
    def student_info_section(self):
        while True:
            self.clear_screen()
            self.display_dashboard()
            
            print("\n" + "=" * 50)
            print(" " * 10 + "🔎 STUDENT INFORMATION SEARCH PORTAL")
            print("=" * 50)
            
            reg = input("\n🎯 Enter EIIN or type 'exit': ").strip()
            
            if reg.lower() == "exit":
                return 'continue'
            
            data = self.fetch_student_info(reg)
            
            self.clear_screen()
            self.display_dashboard()
            self.display_student_info(data)
            
            print("\n1. Search Another EIIN\n2. Main Menu\n3. Exit")
            choice = input("Your choice: ")
            
            if choice == "2": return 'continue'
            if choice == "3": return 'exit'
    
    def exit_system(self):
        self.clear_screen()
        print("\033[92m")
        print("=" * 60)
        print(" " * 20 + "🌟 Thank You! 🌟")
        print("=" * 60)
        print("\n" + " " * 15 + "Thank you for using Students Information System")
        print("\n" + "=" * 60)
        print("\033[0m")
        time.sleep(2)
    
    def run_system(self):
        if not self.login_system():
            self.exit_system()
            return
        
        while True:
            self.clear_screen()
            self.display_dashboard()
            
            print("\n1. 🔍 Search EIIN")
            print("2. Exit")
            
            choice = input("\nYour choice: ").strip()
            
            if choice == '1':
                r = self.student_info_section()
                if r == 'exit':
                    break
            elif choice == '2':
                break
        
        self.exit_system()

def main():
    system = StudentsInformationSystem()
    system.run_system()

if __name__ == "__main__":
    main()