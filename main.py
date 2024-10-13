import time
import sys
import random
import os
from datetime import datetime
import ctypes
import math
import shutil
import sys
debug_mode: bool = False
variables = {}
aliases = {}
def debug(message: str) -> None:
    if debug_mode:
        print(f"DEBUG: {message}")
initial_art = """
      ___           ___           ___           ___           ___           ___           ___     
     /\  \         /\  \         /\  \         /\  \         /\__\         /\__\         /\  \    
    |::\  \       /::\  \       /::\  \        \:\  \       /::|  |       /::|  |       /::\  \   
    |:|:\  \     /:/\:\  \     /:/\:\__\        \:\  \     /:/:|  |      /:/:|  |      /:/\:\  \  
  __|:|\:\  \   /:/ /::\  \   /:/ /:/  /    ___  \:\  \   /:/|:|  |__   /:/|:|  |__   /:/  \:\  \ 
 /::::|_\:\__\ /:/_/:/\:\__\ /:/_/:/__/___ /\  \  \:\__\ /:/ |:| /\__\ /:/ |:| /\__\ /:/__/ \:\__\.
 \:\~~\  \/__/ \:\/:/  \/__/ \:\/:::::/  / \:\  \ /:/  / \/__|:|/:/  / \/__|:|/:/  / \:\  \ /:/  /
  \:\  \        \::/__/       \::/~~/~~~~   \:\  /:/  /      |:/:/  /      |:/:/  /   \:\  /:/  / 
   \:\  \        \:\  \        \:\~~\        \:\/:/  /       |::/  /       |::/  /     \:\/:/  /  
    \:\__\        \:\__\        \:\__\        \::/  /        |:/  /        |:/  /       \::/  /   
     \/__/         \/__/         \/__/         \/__/         |/__/         |/__/         \/__/    


"""


def animate_text(text, delay=0.0001) -> None:
    """Animates the given text with a rainbow effect.

    Args:
        text (str): The text to animate.
        delay (float, optional): The delay between color changes (default=0.1).
    """

    colors = [
        "\033[31m",  # Red
        "\033[33m",  # Yellow
        "\033[32m",  # Green
        "\033[36m",  # Cyan
        "\033[34m",  # Blue
        "\033[35m",  # Magenta
        "\033[37m"   # White
    ]

    for i in range(len(text)):
        color_index = random.randint(0, len(colors) - 1)
        colored_text = colors[color_index] + text[i] + "\033[0m"
        sys.stdout.write(colored_text)
        sys.stdout.flush()
        time.sleep(delay)
    print()


animate_text(initial_art)

def interpret(file: str) -> None:
    with open(file, "r") as f:
        for line in f.readlines():
            run(line)

def M_info() -> None:
    print("""
    RADC
    Copyright 2024, Mario Pisano
    under the MIT license
    """)
    

def log(information: str) -> None:
    with open("log.txt", "a") as f:
        f.write(f"{datetime.now()} - {information}\n")


def read(filename: str, folder: str = "apps/data") -> str:
    file_path = os.path.join(folder, filename)
    if not os.path.exists(file_path):
        return ""
    
    try:
        with open(file_path, "r") as f:
            return f.read()
    except Exception as e:
        log(f"Errore nella lettura del file {filename}: {e}")
        return ""

def directory_exists(directory: str) -> bool:
    return os.path.exists(directory)

def directory_exists_create(directory: str) -> None:
    if not os.path.exists(directory):
        os.makedirs(directory)



def source() -> None:
    for file in os.listdir(os.getcwd()):
        with open(file, "r") as f:
            print(f.read())


def system_info() -> None:
    # Informazioni sul sistema operativo
    print(f"Sistema Operativo: {os.name}")
    print(f"Directory corrente: {os.getcwd()}")
    print(f"Nome utente: {os.getlogin()}")
    print(f"Spazio libero su disco: {shutil.disk_usage(os.getcwd()).free / (1024 * 1024 * 1024):.2f} GB")


def battery_info() -> None:
    # Informazioni sullo stato della batteria (solo per Windows)
    if os.name == 'nt':
        SYSTEM_POWER_STATUS = ctypes.Structure
        class SYSTEM_POWER_STATUS(ctypes.Structure):
            _fields_ = [("ACLineStatus", ctypes.c_byte),
                        ("BatteryFlag", ctypes.c_byte),
                        ("BatteryLifePercent", ctypes.c_byte),
                        ("SystemStatusFlag", ctypes.c_byte),
                        ("BatteryLifeTime", ctypes.c_ulong),
                        ("BatteryFullLifeTime", ctypes.c_ulong)]

        status = SYSTEM_POWER_STATUS()
        if ctypes.windll.kernel32.GetSystemPowerStatus(ctypes.byref(status)):
            print(f"Percentuale batteria: {status.BatteryLifePercent}%")
        else:
            print("Impossibile ottenere informazioni sulla batteria.")
    else:
        print("Questa funzione è disponibile solo su Windows.")


def ram_info() -> None:
    # Informazioni sulla memoria RAM disponibile
    if os.name == 'nt':
        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [("dwLength", ctypes.c_ulong),
                        ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong),
                        ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong),
                        ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong),
                        ("ullAvailVirtual", ctypes.c_ulonglong),
                        ("sullAvailExtendedVirtual", ctypes.c_ulonglong)]
        memory_status = MEMORYSTATUSEX()
        memory_status.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory_status))
        total_memory = memory_status.ullTotalPhys / (1024 ** 3)
        available_memory = memory_status.ullAvailPhys / (1024 ** 3)
        print(f"Memoria totale: {total_memory:.2f} GB")
        print(f"Memoria disponibile: {available_memory:.2f} GB")
    else:
        print("Questa funzione è disponibile solo su Windows.")
        
def run(line):
    try:
        parts = line.split(" ")
        opcode = parts[0]

        # Check if the command is an alias and substitute
        if opcode in aliases:
            line = aliases[opcode]
            parts = line.split(" ")
            opcode = parts[0]

        match opcode:
            case "exit":
                print("Exiting...")
                exit()
            case "help":
                print("Available commands: exit, set, get, echo, debug_vars, delete, def, loop, alias")
            case _ if opcode.startswith("$"):
                # Variable assignment
                var_name = opcode.replace("$", "")
                var_value = " ".join(parts[2:]).strip()

                if var_value:
                    try:
                        # Evaluate and store the value
                        variables[var_name] = eval(var_value, {"__builtins__": None, "math": math, "lambda": lambda: None}, variables)
                        print(f"Assigned ${var_name} = {variables[var_name]}")
                        debug(f"Variable {var_name} assigned value: {variables[var_name]}")
                    except Exception as e:
                        print(f"ERROR: Invalid expression for variable ${var_name}: {e}")
                else:
                    print(f"ERROR: No value provided for ${var_name}")
            case "echo":
                tosay = " ".join(parts[1:])
                print(f"> {eval(tosay, {'__builtins__': None, 'math': math}, variables)}")
                debug(f"Echo output: {eval(tosay, {'__builtins__': None, 'math': math}, variables)}")
            case "debug_vars":
                print("Current variables:", variables)
                debug(f"Current variables: {variables}")
            case "set":
                if len(parts) < 3:
                    print("ERROR: Usage: set var_name value")
                    return
                var_name = parts[1]
                var_value = " ".join(parts[2:]).strip()
                if var_value:
                    variables[var_name] = eval(var_value, {"__builtins__": None, "math": math}, variables)
                    print(f"Set ${var_name} = {variables[var_name]}")
                    debug(f"Variable {var_name} set to {variables[var_name]}")
                else:
                    print(f"ERROR: No value provided for ${var_name}")
            case "get":
                if len(parts) < 2:
                    print("ERROR: Usage: get var_name")
                    return
                var_name = parts[1]
                if var_name in variables:
                    print(f"${var_name} = {variables[var_name]}")
                    debug(f"Retrieved variable {var_name} with value {variables[var_name]}")
                else:
                    print(f"ERROR: Variable ${var_name} is not defined.")
            case "delete":
                if len(parts) < 2:
                    print("ERROR: Usage: delete var_name")
                    return
                var_name = parts[1]
                if var_name in variables:
                    del variables[var_name]
                    print(f"Deleted variable ${var_name}.")
                    debug(f"Variable {var_name} deleted.")
                else:
                    print(f"ERROR: Variable ${var_name} is not defined.")
            case _ if opcode == "def":
                # Handle lambda function definitions
                if len(parts) < 3:
                    print("ERROR: Usage: def func_name args -> expression")
                    return

                func_name = parts[1]
                args, body = line.replace("def", "").replace(func_name, "").split("->")

                if func_name in variables:
                    print(f"ERROR: Function ${func_name} is already defined.")
                    return

                # Define the lambda function and store it
                try:
                    lambda_func = eval(f"lambda {args}: {body}", {"__builtins__": None, "math": math}, variables)
                    variables[func_name] = lambda_func
                    print(f"Defined lambda ${func_name} with args ({args})")
                    debug(f"Defined lambda function {func_name} with arguments {args} and body {body}")
                except Exception as e:
                    print(f"ERROR: Invalid lambda definition for ${func_name}: {e}")
                
            case "loop":
                if len(parts) < 3:
                    print("ERROR: Usage: loop n command")
                    return
                try:
                    n = int(parts[1])
                    command = " ".join(parts[2:])
                    for _ in range(n):
                        run(command)
                except Exception as e:
                    print(f"ERROR: Invalid loop: {e}")
            case "alias":
                if len(parts) < 3:
                    print("ERROR: Usage: alias name command")
                    return
                alias_name = parts[1]
                alias_command = " ".join(parts[2:])
                aliases[alias_name] = alias_command
                print(f"Alias '{alias_name}' set for command: {alias_command}")
                debug(f"Alias '{alias_name}' mapped to command: {alias_command}")
            case "pause":
                input("Press Enter to continue...")

            
            case "log":
                if len(parts) < 2:
                    print("ERROR: Usage: log message")
                    return
                message = " ".join(parts[1:])
                log(message)

            case "source":
                source()

            case "directory_exists":
                if len(parts) < 2:
                    print("ERROR: Usage: directory_exists directory")
                    return
                directory = "".join(parts[1:])
                print(directory_exists(directory))

            case "directory_exists_create":
                if len(parts) < 2:
                    print("ERROR: Usage: directory_exists_create directory")
                    return
                directory = "".join(parts[1:])
                directory_exists_create(directory)

            
            case "read":
                if len(parts) < 2:
                    print("ERROR: Usage: read filename")
                    return
                filename = "".join(parts[1:])
                print(read(filename))

            case "system_info":
                system_info()
            case "ram_info":
                ram_info()
            case "battery_info":
                battery_info()
            case _ if opcode == "include" or "interpret":
                if len(parts) < 2:
                    print("ERROR: Usage: include/interpret filename")
                    return
                filename = "".join(parts[1:])
                interpret(filename)
                
            case _:
                debug(f"Unknown opcode: {opcode}")

    except Exception as e:
        print(f"ERROR: {e}")



M_info()
if __name__ == "__main__":
    while True:
        command_line = input("> ").lower()

        run(command_line)
