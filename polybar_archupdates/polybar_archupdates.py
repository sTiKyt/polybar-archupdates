from subprocess import Popen, PIPE, DEVNULL
from time import sleep
import argparse


class ArchUpdates:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.icon = ""

        self.parser.add_argument("-pm", "--pacman", dest="pacman", help="Return number of pacman updates", action="store_true")


class DependencyError(Exception):
    pass

# ---Checking for dependencies ---

def check_dependency(name: str, command: str = "which"):
    try:
        dependency_status = Popen([f"{command}", f"{name}"], stdout=PIPE, stderr=DEVNULL).stdout.read().decode('utf-8')
    except ValueError("Dependency detection is impossible, skipping..."):
        dependency_status = None
    
    if dependency_status == 0 or dependency_status == '' or dependency_status is None:
        return False
    elif name in dependency_status:
        return True
    else:
        return False

# --- Dependencies ---
CHECK_POLYBAR = check_dependency('polybar')
# Ways to check pacman updates
CHECK_UPDATES = check_dependency('checkupdates')
CHECK_ARCH_UPDATES = check_dependency('checkarchupdates')
# Ways to check aur updates
CHECK_YAY = check_dependency('yay')

if not CHECK_POLYBAR:
    raise DependencyError("polybar doesn't seem to be installed.")

# Makes sure that at least one option is available for every check
PACMAN_UPDATE = True if CHECK_UPDATES or CHECK_ARCH_UPDATES else False
AUR_UPDATE = True if CHECK_YAY else False # More options to be added

if not PACMAN_UPDATE:
    raise DependencyError("Unable to find any pacman update checking method, make sure that at least one option(such as checkarchupdates) is installed")

if not AUR_UPDATE:
    raise DependencyError("Unable to find any AUR update checking method, make sure that at least one option(such as yay) is installed")


pacman_command = ''
aur_command = ''

if CHECK_UPDATES:
    pacman_command = ['checkupdates']
elif CHECK_ARCH_UPDATES:
    pacman_command = ['checkarchupdates']

if CHECK_YAY:
    aur_command = ["yay", "-Qua"]


pacman_updates = len(Popen(pacman_command, stdout=PIPE, stderr=DEVNULL).stdout.read().decode('utf-8').splitlines())
print(pacman_updates,' | ',pacman_command)

aur_updates = len(Popen(aur_command, stdout=PIPE, stderr=DEVNULL).stdout.read().decode('utf-8').splitlines())
print(aur_updates,' | ',aur_command)

total_updates = int(pacman_updates) + int(aur_updates)
print(total_updates)


while True:
    print(f'{pacman_updates}|{aur_updates}|{total_updates}', flush=True)
    sleep(5)

