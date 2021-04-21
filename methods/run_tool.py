import sys, os, time, threading
from colorama import Fore 

from .printer import print_msg, clear_console
from .loader import Loader

from crawler import spider
from crawler.web_crawler import web_crawler

from pass_maker.password_generator import generate_password
from pass_maker.one_password import yield_one_password

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
         },
      4: {
           "func": lambda: web_crawler(spider),
           "name": "Moon Spider"
         },
      5: {
           "func": lambda: generate_password(),
           "name": "Auth Hoard"
         },
      6: {
           "func": lambda: yield_one_password(), 
           "name": "Auth Gen"
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
    