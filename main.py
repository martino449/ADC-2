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
ignore_errors: bool = False
variables = {}
aliases = {}
def debug(message: str) -> None:
    if debug_mode:
        print(f"DEBUG: {message}")

def error(error: str) -> None:
    if not ignore_errors:
        print(f"ERROR: {error}")


def help_command() -> None:
    print("""
    Available commands:
    - exit: Exits the interpreter.
    - set var_name value: Sets a variable to a given value.
    - get var_name: Retrieves the value of a variable.
    - delete var_name: Deletes a variable.
    - echo expression: Evaluates and prints an expression.
    - debug_vars: Prints the current variables.
    - debug_activate: Activates debug mode.
    - alias name command: Creates a command alias.
    - loop n command: Repeats a command n times.
    - lambda func_name args -> expression: Defines a lambda function.
    - pause: Pauses the interpreter until Enter is pressed.
    - log message: Logs a message to a file.
    - source: Prints the content of all files in the current directory.
    - directory_exists directory: Checks if a directory exists.
    - directory_exists_create directory: Creates a directory if it doesn't exist.
    - read filename: Reads and prints the content of a file.
    - include filename: Executes commands from a file.
    - trueloop command: Repeats a command infinitely.
    """)


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



    RADC
    Copyright 2024, Mario Pisano
    under the MIT license

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


def run(line):
    global debug_mode
    global ignore_errors
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
                help_command()
            case _ if opcode.startswith("$"):
                # Variable assignment
                var_name = opcode.replace("$", "")
                var_value = " ".join(parts[2:]).strip()

                if var_value:
                    try:
                        # Evaluate and store the value
                        variables[var_name] = eval(var_value, {"__builtins__": None, "math": math, "lambda": lambda: None}, variables)

                        debug(f"Variable {var_name} assigned value: {variables[var_name]}")
                    except Exception as e:
                        error(f"Invalid expression for variable ${var_name}: {e}")
                else:
                    error(f"No value provided for ${var_name}")
            case "echo":
                tosay = " ".join(parts[1:])
                print(f"> {eval(tosay, {'__builtins__': None, 'math': math}, variables)}")
                debug(f"Echo output: {eval(tosay, {'__builtins__': None, 'math': math}, variables)}")
            case "debug_vars":
                print("Current variables:", variables)
                debug(f"Current variables: {variables}")
            case "set":
                if len(parts) < 3:
                    error("Usage: set var_name value")
                    return
                var_name = parts[1]
                var_value = " ".join(parts[2:]).strip()
                if var_value:
                    variables[var_name] = eval(var_value, {"__builtins__": None, "math": math}, variables)
                    debug(f"Variable {var_name} set to {variables[var_name]}")
                else:
                    error(f"No value provided for ${var_name}")
            case "get":
                if len(parts) < 2:
                    error("Usage: get var_name")
                    return
                var_name = parts[1]
                if var_name in variables:
                    print(variables[var_name])
                    debug(f"Retrieved variable {var_name} with value {variables[var_name]}")
                else:
                    error(f"Variable ${var_name} is not defined.")
            case "delete":
                if len(parts) < 2:
                    error("Usage: delete var_name")
                    return
                var_name = parts[1]
                if var_name in variables:
                    del variables[var_name]

                    debug(f"Variable {var_name} deleted.")
                else:
                    error(f"Variable ${var_name} is not defined.")
            case "lambda":
                # Handle lambda function definitions
                if len(parts) < 3:
                    error("Usage: def func_name args -> expression")
                    return

                func_name = parts[1]
                args, body = line.replace("lambda", "").replace(func_name, "").split("->")

                if func_name in variables:
                    error(f"Function ${func_name} is already defined.")
                    return

                # Define the lambda function and store it
                try:
                    lambda_func = eval(f"lambda {args}: {body}", {"__builtins__": None, "math": math}, variables)
                    variables[func_name] = lambda_func

                    debug(f"Defined lambda function {func_name} with arguments {args} and body {body}")
                except Exception as e:
                    error(f"Invalid lambda definition for ${func_name}: {e}")
                

            case "ignore_errors":
                ignore_errors = not ignore_errors
                debug(f"Ignore errors: {ignore_errors}")
            case "loop":
                if len(parts) < 3:
                    error("Usage: loop n command")
                    return
                try:
                    n = int(parts[1])
                    command = " ".join(parts[2:])
                    for _ in range(n):
                        run(command)
                except Exception as e:
                    error(f"Invalid loop: {e}")
            case "alias":
                if len(parts) < 3:
                    error("Usage: alias name command")
                    return
                alias_name = parts[1]
                alias_command = " ".join(parts[2:])
                aliases[alias_name] = alias_command

                debug(f"Alias '{alias_name}' mapped to command: {alias_command}")
            case "pause":
                input("Press Enter to continue...")

            
            case "log":
                if len(parts) < 2:
                    error("Usage: log message")
                    return
                message = " ".join(parts[1:])
                log(message)

            case "source":
                source()

            case "directory_exists":
                if len(parts) < 2:
                    error("Usage: directory_exists directory")
                    return
                directory = "".join(parts[1:])
                print(directory_exists(directory))

            case "directory_exists_create":
                if len(parts) < 2:
                    error("Usage: directory_exists_create directory")
                    return
                directory = "".join(parts[1:])
                directory_exists_create(directory)

            
            case "read":
                if len(parts) < 2:
                    error("Usage: read filename")
                    return
                filename = "".join(parts[1:])
                print(read(filename))


            case "include":
                if len(parts) < 2:
                    error("Usage: include filename")
                    return
                filename = "".join(parts[1:])
                interpret(filename)

            
            case "trueloop":
                while True:
                    run("".join(parts[1:]))


            case "debug_activate":
                debug_mode = True
                debug("Debug mode activated")
                
                
            case _ if opcode.startswith("#"):
                debug(f"Ignoring Comment: {opcode[1:]}")
                
            case _:
                if opcode == "":
                    pass
                elif opcode in variables:
                    print(variables[opcode])
                    debug(f"Retrieved variable {opcode} with value {variables[opcode]}")
                else:
                    debug(f"Unknown opcode: {opcode}")

    except Exception as e:
        error(f"{e}")





if __name__ == "__main__":
    while True:
        command_line = input("> ").lower()
        run(command_line)
