#!/usr/bin/env python3
import os
import time
import datetime
import subprocess
import sys
import random

class AutoUpdateBanner:
    def __init__(self):
        self.colors = {
            'reset': '\033[0m',
            'bold': '\033[1m',
            'green': '\033[32m',
            'cyan': '\033[36m',
            'yellow': '\033[33m', 
            'red': '\033[31m',
            'blue': '\033[34m',
            'magenta': '\033[35m',
            'gray': '\033[90m'
        }
        self.team_name = "HAQ CYBER SQUAD"
        self.start_time = datetime.datetime.now()
        
    def color_text(self, text, color):
        return f"{self.colors[color]}{text}{self.colors['reset']}"
    
    def type_line(self, text, delay=0.02):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
    
    def run_command(self, cmd, description):
        """Run a command and show progress"""
        print(self.color_text(f"🔄 {description}...", 'yellow'), end='', flush=True)
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                print(self.color_text(" ✅", 'green'))
                return True
            else:
                print(self.color_text(" ❌", 'red'))
                return False
        except subprocess.TimeoutExpired:
            print(self.color_text(" ⏰", 'yellow'))
            return False
        except Exception as e:
            print(self.color_text(" ❌", 'red'))
            return False
    
    def system_update(self):
        """Complete system update"""
        print(self.color_text("╔══════════════════════════════════════╗", 'cyan'))
        print(self.color_text("║        SYSTEM UPDATE STARTING        ║", 'cyan'))
        print(self.color_text("╚══════════════════════════════════════╝", 'cyan'))
        print()
        
        update_commands = [
            ("apk update", "Updating package list"),
            ("apk upgrade", "Upgrading system packages"),
            ("apk fix", "Fixing broken packages"),
            ("pip3 install --upgrade pip", "Upgrading Python pip"),
            ("rm -rf /tmp/* /var/tmp/*", "Cleaning temporary files")
        ]
        
        success_count = 0
        for cmd, desc in update_commands:
            if self.run_command(cmd, desc):
                success_count += 1
            time.sleep(1)
        
        print()
        print(self.color_text(f"📊 Update Summary: {success_count}/{len(update_commands)} completed", 'cyan'))
        return success_count
    
    def get_system_info(self):
        """Get real-time system information"""
        info = {}
        
        try:
            # Basic system info
            info['username'] = os.getenv('USER', 'root')
            info['hostname'] = subprocess.getoutput('hostname').strip()
            
            # Date and time
            info['current_date'] = self.start_time.strftime("%d %B %Y")
            info['current_time'] = self.start_time.strftime("%I:%M:%S %p")
            info['timestamp'] = self.start_time.strftime("%Y%m%d_%H%M%S")
            
            # System info
            info['kernel'] = subprocess.getoutput('uname -s').strip()
            info['arch'] = subprocess.getoutput('uname -m').strip()
            info['shell'] = os.getenv('SHELL', 'sh').split('/')[-1]
            
            # Package info
            info['apk_packages'] = subprocess.getoutput('apk info | wc -l').strip()
            
            # Disk usage
            disk_info = subprocess.getoutput('df -h / | awk \'NR==2{print $3 "/" $2 " (" $5 ")"}\'').strip()
            info['disk_usage'] = disk_info if disk_info else 'n/a'
            
            # Memory info
            mem_info = subprocess.getoutput('free -h | awk \'NR==2{print $3 "/" $2}\'').strip()
            info['memory_usage'] = mem_info if mem_info else 'n/a'
            
            # Uptime
            uptime = subprocess.getoutput('uptime -p 2>/dev/null || cat /proc/uptime 2>/dev/null | awk \'{print int($1/3600)"h "int(($1%3600)/60)"m"}\'').strip()
            info['uptime'] = uptime if uptime else 'n/a'
            
            # Network IP
            ip_info = subprocess.getoutput('ip route get 1 2>/dev/null | awk \'{print $7;exit}\' || hostname -I 2>/dev/null | awk \'{print $1}\'').strip()
            info['ip_address'] = ip_info if ip_info else 'unknown'
            
        except Exception as e:
            print(f"Error getting system info: {e}")
            
        return info
    
    def show_animated_banner(self, info):
        """Show animated banner with system info"""
        os.system('clear')
        
        # Animated CRYPTICX banner
        cryptic_frames = [
            r"""
 ██████╗██████╗ ██╗   ██╗██████╗ ████████╗██╗ ██████╗██╗  ██╗
██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝██║██╔════╝╚██╗██╔╝
██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║   ██║██║      ╚███╔╝ 
██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   ██║██║      ██╔██╗ 
╚██████╗██║  ██║   ██║   ██║        ██║   ██║╚██████╗██╔╝ ██╗
 ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝   ╚═╝ ╚═════╝╚═╝  ╚═╝                                                         

            """,
            r"""
 ╔═╗╦═╗╦ ╦╦╔═╗╦╔═╗╦╔═╔═╗╦
 ╠═╣╠╦╝║ ║║║ ║║║╣ ╠╩╗║╣ ║
 ╩ ╩╩╚═╚═╝╩╚═╝╩╚═╝╩ ╩╚═╝╩
            """
        ]
        
        # Animate banner
        for frame in cryptic_frames:
            os.system('clear')
            banner_color = random.choice(['yellow', 'cyan', 'green', 'magenta'])
            print(self.color_text(frame, banner_color))
            time.sleep(0.3)
        
        # Team info
        print(self.color_text("╔══════════════════════════════════════╗", 'cyan'))
        print(self.color_text(f"║           {self.team_name}           ║", 'green'))
        print(self.color_text("╚══════════════════════════════════════╝", 'cyan'))
        print()
    
    def show_system_status(self, info):
        """Show real-time system status"""
        print(self.color_text("📊 REAL-TIME SYSTEM STATUS:", 'yellow'))
        print(self.color_text("═" * 45, 'cyan'))
        
        status_items = [
            f"👤 User: {info['username']}@{info['hostname']}",
            f"📅 Session: {info['current_date']}",
            f"⏰ Time: {info['current_time']}", 
            f"🐧 System: {info['kernel']} {info['arch']}",
            f"📦 Packages: {info['apk_packages']}",
            f"💾 Disk: {info['disk_usage']}",
            f"🧠 Memory: {info['memory_usage']}",
            f"🕐 Uptime: {info['uptime']}",
            f"🌐 IP: {info['ip_address']}",
            f"🐚 Shell: {info['shell']}"
        ]
        
        for item in status_items:
            self.type_line(item, 0.01)
            time.sleep(0.1)
        
        print(self.color_text("═" * 45, 'cyan'))
    
    def run_complete_setup(self):
        """Run complete auto-update and banner setup"""
        try:
            print(self.color_text("🚀 INITIATING AUTO SYSTEM UPDATE...", 'magenta'))
            time.sleep(1)
            
            # Step 1: System Update
            update_result = self.system_update()
            
            # Step 2: Get fresh system info
            print()
            print(self.color_text("🔍 GATHERING REAL-TIME SYSTEM INFORMATION...", 'cyan'))
            system_info = self.get_system_info()
            time.sleep(1)
            
            # Step 3: Show animated banner
            self.show_animated_banner(system_info)
            
            # Step 4: Show system status
            self.show_system_status(system_info)
            
            # Step 5: Final message
            print()
            if update_result >= 3:
                print(self.color_text("✅ SYSTEM UPDATE COMPLETED SUCCESSFULLY!", 'green'))
            else:
                print(self.color_text("⚠️  SYSTEM UPDATE PARTIALLY COMPLETED", 'yellow'))
            
            print(self.color_text(f"🎯 {self.team_name} - READY FOR OPERATIONS", 'cyan'))
            print(self.color_text(f"📝 Session started at: {system_info['current_time']}", 'gray'))
            print()
            
        except KeyboardInterrupt:
            print(self.color_text("\n\n⏹️ Update interrupted by user", 'red'))
        except Exception as e:
            print(self.color_text(f"\n\n❌ Error during update: {e}", 'red'))

def main():
    # Check if running in iSH
    if 'ish' not in subprocess.getoutput('uname -a').lower():
        print("⚠️ This script is optimized for iSH Shell")
        return
    
    auto_system = AutoUpdateBanner()
    auto_system.run_complete_setup()

if __name__ == "__main__":
    main()
