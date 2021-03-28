import json, time, sqlite3, string, random
from random import randint
from methods.printer import get_input, print_tool_name, print_msg, clear_console
from methods.loader import Loader
# from methods.confirm import confirm_exit


class Guess:
  def __init__(self):
    self.active = True
    self.min = 0
    self.max = 10
    self.set_correct(self.min, self.max)
    self.chances = 5
    self.attempts = self.chances
    self.level = 1
    self.score = 0
    self.set_highscore()
    self.current_player = []
  
  def set_correct(self, min, max):
    self.correct = randint(min, max)
    
  def get_correct(self):
    return self.correct
    
  def set_player_name(self):
    while True:
      try:
        self.player_name = get_input("Enter Username")
        if len(self.player_name) < 3:
          raise Exception("Please make your Username at least 3 characters")
        break
      except Exception as e:
        print_msg("error", e)
        continue
        
  def set_highscore(self):
    try:
      conn = sqlite3.connect("number_guessing_game/players.db")
      cursor = conn.cursor()
      
      cursor.execute("SELECT name, score FROM Highscore where id=1")
      self.highscore = list(cursor.fetchone())
      
      if self.score >= self.highscore[1]:
        cursor.execute("UPDATE Highscore SET name='{}', score={} where id=1"\
          .format(self.current_player[1], self.score))
        
        cursor.execute("SELECT name, score FROM Highscore where id=1")
        self.highscore = list(cursor.fetchone())

        conn.commit()
      
    except sqlite3.Error as e:
      print_msg("error", "can't set high")
      conn.rollback()
      
    finally:
      conn.close()

        
  def set_play_data(self):
    try:
      conn = sqlite3.connect("number_guessing_game/players.db")
      cursor = conn.cursor()
      
      if self.score > self.current_player[3]:
        cursor.execute("UPDATE Players SET level={}, score={} where pid='{}' and name='{}'"\
          .format(self.level, self.score, self.current_player[0], self.current_player[1]))
        
        conn.commit()
      
    except sqlite3.Error as e:
      print_msg("error", "can't set play")
      conn.rollback()
      
    finally:
      conn.close()
    
  def set_player_data(self):
    try:
      
      characters = string.ascii_letters + string.digits
      new_player_id = ""
      for i in range(10):
        new_player_id += random.choice(characters)
      
      conn = sqlite3.connect("number_guessing_game/players.db")
      cursor = conn.cursor()
      
      cursor.execute("SELECT * FROM Players where name='{}'".format(self.player_name))
      player = cursor.fetchone()
      
      if player:
        self.current_player = list(player)
        self.current_player.append("old")
      
      else:
        sql = "INSERT INTO Players(pid, name, level, score) VALUES('{0}', '{1}', {2}, {3})"\
          .format(str(new_player_id), 
          self.player_name,
          self.level, self.score)
        
        cursor.execute(sql)
        
        cursor.execute("SELECT * FROM Players where pid='{}' and name='{}'"\
          .format(str(new_player_id), self.player_name))
          
        self.current_player = list(cursor.fetchone())
        self.current_player.append("new")
        
        conn.commit()
        
        
    except sqlite3.Error as e:
      conn.rollback()
      print_msg("error", e)
      
     
    finally:
      conn.close()
      
  def get_guess(self):
    while True:
      try:
        self.trial = int(get_input("Enter your Guess"))
        break
      except ValueError:
        print_msg("error", "Only Numbers are allowed, try again")
        continue
  
  def increase_chances(self, addition):
      self.chances += addition
      self.attempts = self.chances
      
  def proceed(self):
    self.level += 1
    self.max += 5
    self.increase_chances(2)
    self.set_correct(self.min, self.max)
    self.score += 10
    
    self.set_play_data()
    self.set_highscore()
    
    loader = Loader(load_text="Loading Stage •[{}]•".format(self.level), load_type="success")
    loader.load()
    loader.terminate(timeout=.4, seize=1.1)

    clear_console()
    
    print_msg("info", "Highscore •[{}]• By {}"\
      .format(self.highscore[1], self.highscore[0], art=True))
    
    print_msg("info", "Guess the Number between {} and {}"\
      .format(self.min, self.max, art=True))

    print_msg("info", f"Player: {self.current_player[1]} <•> Stage: [• {self.level} •], Score: [• {self.score} •]", art=False)
  
        
  def compare_guess(self):
    # print(self.trial, self.correct)
    if self.trial == self.correct:
      print_msg("success", "You guessed right! going to next level")
      time.sleep(1)
      self.proceed()
          
    elif self.trial > self.correct:
      self.attempts -= 1
      print_msg("info", "Your guess is greater than the correct number")
      print_msg("warning", f"You have •[{self.attempts}]• Attempts left, try again")
          
    elif self.trial < self.correct:
      self.attempts -= 1
      print_msg("info", "Your guess is less than the correct number")
      print_msg("warning", f"You have •[{self.attempts}]• Attempts left, try again")

  
  def guess_it(self, show_tips=True):
    if show_tips:
      print_tool_name("Guess Py", "Devvyhac", "Team Trace Techie", "github.com/devvyhac")
      print_msg("info", """  This is a number guessing game, 
  where you need to guess the correct number 
  to proceed to the next level.
 
  TIP: There will be an hint 
  that tells you whether your guess is 
  greater than or less than the correct number.
  
  ENJOY 😊. \n""", art=False)

    self.set_player_name()
    
    clear_console()
    
    self.set_player_data()
    if self.current_player[-1] == "old":
      print_msg("success", "Welcome back, {}".format(self.current_player[1]))
    else:
      print_msg("success", "New Player! {}".format(self.current_player[1]))
    
    print_msg("info", "Highscore •[{}]• By {}"\
      .format(self.highscore[1], self.highscore[0], art=True))
    
    print_msg("info", "Guess the Number between {} and {}"\
      .format(self.min, self.max, art=True))

    print_msg("info", f"Player: {self.current_player[1]} <•> Stage: [• {self.level} •], Score: [• {self.score} •]", art=False)
    self.get_guess()
    
    while self.active != False:
      try:
        self.compare_guess()
        self.get_guess()
        
        if self.attempts < 2:
          clear_console()
          print_msg("error", "GAME OVER!!!")
          time.sleep(3)
          self.active = False
          break
        
      except KeyboardInterrupt:
          print("Quiting game")
          time.sleep(1)
          self.active = False
          break



