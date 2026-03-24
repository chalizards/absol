import psutil
import time
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("/var/log/absol.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

DANGER_ZONE_PERCENT = 70.0 
KILL_THRESHOLD = 20.0
SAFE_LIST = ['systemd', 'gdm3', 'gnome-shell', 'Xorg', 'bash', 'zsh', 'sshd']

def get_memory_hog():
    hog = None
    max_mem = 0
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        try:
            mem = proc.info['memory_percent']
            if mem and mem > max_mem and proc.info['name'] not in SAFE_LIST:
                max_mem = mem
                hog = proc
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return hog

def calculate_sleep_time(current_ram_percent):
    if current_ram_percent < 40.0:
        return 30
    elif current_ram_percent < 60.0:
        return 10
    elif current_ram_percent < DANGER_ZONE_PERCENT:
        return 2
    else:
        return 0

def start_absol_watch():
    logging.info("🌙 Absol entrou nas sombras. Aguardando sinais de desastre...")
    
    while True:
        ram = psutil.virtual_memory()
        
        if ram.percent >= DANGER_ZONE_PERCENT:
            logging.warning(f"⚠️ Absol sentiu o perigo! RAM em {ram.percent}%.")
            target = get_memory_hog()
            
            if target and target.info['memory_percent'] > KILL_THRESHOLD:
                logging.warning(f"⚔️ Absol usou Night Slash em: {target.info['name']} (PID {target.info['pid']})")
                try:
                    target.kill()
                    logging.info("🛡️ Ameaça neutralizada. Notebook a salvo.")
                    time.sleep(10)
                except Exception as e:
                    logging.error(f"O ataque falhou: {e}")
        
        sleep_time = calculate_sleep_time(ram.percent)
        time.sleep(sleep_time)

if __name__ == '__main__':
    start_absol_watch()