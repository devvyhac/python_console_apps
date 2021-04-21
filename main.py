import os, sys, time
from colorama import Fore
from art import *

from methods.printer import get_input
from methods.list_tools import list_items, list_commands, list_tools
from methods.printer import print_msg, get_input, clear_console, print_tool_name
from methods.loader import Loader
from methods.run_tool import run_tool
from methods.confirm import confirm_exit
from methods.fancy import fancy_typo, fancy_text

commands = ["List Available Programs", "Exit"]
tools = [
         "Guess Game • [ Number Guessing Game ]", 
         "ATM Mock • [ ATM - Cash Deposit & Withdraw]",
         "Aboki $$ • [ Currency Converter ]",
         "Moon Spider • [ Web Crawler/Site Map Payload ]",
         "Auth Hoard • [ Password Wordlist Generator ]",
         "Auth Gen • [ Unique Single Password Generator ]"
        ]

clear_console()
is_active = True


toolname = fancy_typo("Termi Py", "fancy21")
loader = Loader(load_text="Loading {}".format(toolname), load_type="success", feedback="{} Successfully Loaded".format(toolname))
loader.load()
loader.terminate(timeout=1.5)
clear_console()

print_tool_name("Termi Py", "Devvyhac", "Team Trace Techie", "github.com/devvyhac")

def get_command():
  list_commands(commands) 
  option = get_input("\nEnter option")
    
  return option

def run_program():
  global is_active  
  while is_active:
    if not is_active:
      break
      
    try:
      option = int(get_command())
      
      if option == 91:
        confirm = confirm_exit("Do you really want to quit? Y/n: ")
        if confirm == True:
          sys.exit()
          
        pass
    
      elif option == 90:
        clear_console()
        reload = Loader(load_text="Fetching Tools", load_type="success")
        reload.load()
        reload.terminate(timeout=1)
        list_tools(tools)
    
      else:
        option = int(option)
        running = run_tool(option, tools, commands)
        continue

    
    except KeyboardInterrupt:
      if confirm_exit("Do you really want to quit? Y/n: "):
        break
        
      continue
    
    except ValueError:
      clear_console()
      loader = Loader(load_type="info", load_text="Wrong Entry! • Fetching Tools", feedback = "Invalid Entry, Use digits!")
      loader.load()
      loader.terminate(timeout=2)
      print_msg("error", "Only Digits are allowed!", clear=True)
      
      continue
      
      
    #except:
      #print("another new error")

run_program()

