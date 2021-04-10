import sys, os, time, threading
from colorama import Fore 

from .printer import print_msg, clear_console
from .loader import Loader

from number_guessing_game.guess_game import Guess
from ATM_Mock.atm import ATM_Mock
from currency_converter.converter import converter

player = Guess()

def run_tool(index, tools, commands, delay=1.2):
  try:
    switcher = {
      1: {
           "func": lambda: player.guess_it(),
           "name": "Guess Game"
         },
      2: {
           "func": lambda: ATM_Mock(),
           "name": "ATM Mock"
         },
      3: {
           "func": lambda: converter(), 
           "name": "Aboki $$"
         }
    }
    
    if switcher[index]:
      
      clear_console()
      loader = Loader(load_text="Starting {}".format(switcher[index]['name'].upper()), load_type="success", feedback="Program loads Successfully!")
      loader.load()
      loader.terminate(timeout=1)
      clear_console()
      
      return switcher[index]['func']()
    
  except KeyError:
    clear_console()
    loader = Loader(load_type="info", load_text="Selected Tools, Not Available! • Fetching Tools", feedback = "Invalid Entry, Use digits!")
    loader.load()
    loader.terminate(timeout=1, seize= 2)
    
    print_msg("error", "Option {}•[{}]•{} not Valid!".format(Fore.CYAN, index, Fore.RED), clear=True)
    
    #list_items(tools, commands)
    
  #except:
    # print_msg("err", "Option {0}•[{1}]•{2} not Valid!"\
      #.format(color.LIGHTYELLOW_EX, index, color.RED), color=color)
    