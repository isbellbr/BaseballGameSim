import pandas as pd
import random



#Use these for the box score
team1scores = []
team2scores = []
scoring_plays_description = []
general_descriptions = []




def groundout_or_flyout(pitcher):
  go_range_max = pitcher.go_pct
  random_float = random.random()
  if random_float <= go_range_max:
    result = "Groundout"
  else:
    result = "Flyout"
  return result




  
def at_bat(hitter, pitcher):
  k_range_max = hitter.k_pct
  single_range_max = k_range_max + hitter.single_pct
  double_range_max = single_range_max + hitter.double_pct
  triple_range_max = double_range_max + hitter.triple_pct
  hr_range_max = triple_range_max + hitter.hr_pct
  random_float = random.random()
  if random_float <= k_range_max:
    result = "Strikeout"
  elif random_float <= single_range_max:
    result = "Single"
  elif random_float <= double_range_max:
    result = "Double"
  elif random_float <= triple_range_max:
    result = "Triple"
  elif random_float <= hr_range_max:
    result = "Home Run"
  else:
    result = groundout_or_flyout(pitcher)
  return result




  
#Description Creation Function
def create_description(inning, hitter_name, result, runs_scored):
  if result == "Single":
    scoring_plays_description.append("Inning " +str(inning) + ": " + hitter_name + " singles, scoring "+ str(runs_scored) + " runs.")
  elif result == "Double":
    scoring_plays_description.append("Inning " +str(inning) + ": " + hitter_name + " doubles, scoring "+ str(runs_scored) + " runs.")
  elif result == "Triple":
    scoring_plays_description.append("Inning " +str(inning) + ": " + hitter_name + " triples, scoring "+ str(runs_scored) + " runs.")
  elif result == "Home Run":
    scoring_plays_description.append("Inning " +str(inning) + ": " + hitter_name + " homers, scoring "+ str(runs_scored) + " runs.")
  elif result == "Flyout":
    scoring_plays_description.append("Inning " +str(inning) + ": " + str(runs_scored) + " run scores on a sacrifice fly by " + hitter_name)
  else:
    scoring_plays_description.append("Inning " +str(inning) + ": " + str(runs_scored) + " run scores on a RBI groundout by " + hitter_name)





    
#General Description Function
def general_description(inning, outs, hitter_name, pitcher_name, result, runs_scored):
  if runs_scored > 0:
      if result == "Single":
        general_descriptions.append("Inning " +str(inning) + ": " + str(outs) + "outs: "+ hitter_name + " singles, scoring "+ str(runs_scored) + " runs.")
      elif result == "Double":
        general_descriptions.append("Inning " +str(inning) + ": " + hitter_name + " doubles, scoring "+ str(runs_scored) + " runs.")
      elif result == "Triple":
        general_descriptions.append("Inning " +str(inning) + ": " + hitter_name + " triples, scoring "+ str(runs_scored) + " runs.")
      elif result == "Home Run":
        general_descriptions.append("Inning " +str(inning) + ": " + hitter_name + " homers, scoring "+ str(runs_scored) + " runs.")
      elif result == "Flyout":
        general_descriptions.append("Inning " +str(inning) + ": " + str(runs_scored) + " run scores on a sacrifice fly by " + hitter_name)
      else:
        general_descriptions.append("Inning " +str(inning) + ": " + str(runs_scored) + " run scores on a RBI groundout by " + hitter_name)
  else:
    #inning, outs, hitter_name, pitcher_name, result, runs_scored
    if result == "Strikeout":
      result = "strikes out"
    elif result == "Single":
      result = "singles"
    elif result == "Double":
      result = "doubles"
    elif result == "Triple":
      result = "triples"
    elif result == "Home Run":
      result = "homers"
    elif result == "Groundout":
      result = "grounds out"
    elif result == "Flyout":
      result = "flies out"
    general_descriptions.append("Inning " +str(inning) + ": " +str(outs) + "out(s): "+ hitter_name + "  " + result + " on a pitch by " + pitcher_name +". ") 

    #Hitter Class
class Hitter:
  def __init__(self, k_pct, single_pct, double_pct, triple_pct, hr_pct, batted_out_pct, walk_pct, name):
    self.k_pct = k_pct
    self.single_pct = single_pct
    self.double_pct = double_pct
    self.triple_pct = triple_pct
    self.hr_pct = hr_pct
    self.batted_out_pct = batted_out_pct
    self.walk_pct = walk_pct
    self.name = name




    
#Pitcher Class
class Pitcher:
  def __init__(self, k_pct, hit_pct, go_ao_pct, walk_pct, name):
    self.k_pct = k_pct
    self.hit_pct = hit_pct
    self.go_ao_pct = go_ao_pct
    self.walk_pct = walk_pct
    self.name = name
    self.go_pct = go_ao_pct/(1 + go_ao_pct)
    self.ao_pct = 1/(1 + go_ao_pct)
#Team Class
class Team:
  def __init__(self, starter,lineup, name, reliever1=None, reliever2=None, reliever3=None):
    self.starter = starter
    self.reliever1 = reliever1
    self.reliever2 = reliever2
    self.reliever3 = reliever3
    self.lineup = lineup
    self.name = name



    
#Game Class
class Game:
  def __init__(self, team1, team2, inning=1, lineup_position=0, outs=0, runner1pos=0, runner2pos=0, runner3pos=0):
    self.team1 = team1
    self.team2 = team2
    self.inning = inning
    self.outs = outs
    self.lineup_position = lineup_position
    self.current_hitter = team1.lineup[lineup_position]
    self.current_pitcher = team2.starter
    self.runner1pos = runner1pos
    self.runner2pos = runner2pos
    self.runner3pos = runner3pos
    self.teamAtBat = team1
    self.halfInningScore = 0
    self.team1score = 0
    self.team2score = 0









    
def updateGameSituation(game, result):
    if (result=="Strikeout"):
      #General Description
      general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 0)
      game.outs+=1
      game.lineup_position+=1
    elif (result=="Single"):
      game.lineup_position+=1
      if (game.runner3pos != 0):
        #The Bases are Loaded
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher, result, 2)
        game.halfInningScore+=2
        game.runner1pos=1
        game.runner2pos=2
        game.runner3pos=0
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 2)
      elif (game.runner2pos == 3 and game.runner1pos == 2):
        #Runner on Second and Third
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher, result, 2)
        game.halfInningScore+=2
        game.runner1pos=1
        game.runner2pos=0
        game.runner3pos=0
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 2)
      elif (game.runner2pos == 3 and game.runner1pos == 1):
        #Runner on First and Third
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher, result, 1)
        game.halfInningScore+=1
        game.runner1pos=1
        game.runner2pos=1
        game.runner3pos=0
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 1)
      elif (game.runner2pos == 2 and game.runner1pos == 1):
        #Runner on First and Second
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher, result, 1)
        game.halfInningScore+=1
        game.runner1pos=1
        game.runner2pos=0
        game.runner3pos=1
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 1)
      elif (game.runner1pos == 3):
        #Runner on Third
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher, result, 1)
        game.halfInningScore+=1
        game.runner1pos=1
        game.runner2pos=0
        game.runner3pos=0
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 1)
      elif (game.runner1pos == 2):
        #Runner on Second
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher, result, 1)
        game.halfInningScore+=1
        game.runner1pos=1
        game.runner2pos=0
        game.runner3pos=0
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 1)
      elif (game.runner1pos == 1):
        #Runner on Second
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 0)
        game.runner1pos=1
        game.runner2pos=0
        game.runner3pos=1
      #No runners on base
      else:
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 0)
        game.runner1pos = 1
        game.runner2pos = 0
        game.runner3pos = 0 
    elif (result=="Double"):
      game.lineup_position+=1
      if (game.runner3pos != 0):
        #The Bases are Loaded
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher, result, 2)
        game.halfInningScore+=2
        game.runner1pos=2
        game.runner2pos=3
        game.runner3pos=0
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 2)
      elif (game.runner2pos == 3 and game.runner1pos == 2):
        #Runner on Second and Third
#General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher, result, 2)
        game.halfInningScore+=2
        game.runner1pos=2
        game.runner2pos=0
        game.runner3pos=0
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 2)
      elif (game.runner2pos == 3 and game.runner1pos == 1):
        #Runner on First and Third
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher, result, 1)
        game.halfInningScore+=1
        game.runner1pos=2
        game.runner2pos=3
        game.runner3pos=0
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 1)
      elif (game.runner2pos == 2 and game.runner1pos == 1):
        #Runner on First and Second
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher, result, 1)
        game.halfInningScore+=1
        game.runner1pos=2
        game.runner2pos=3
        game.runner3pos=0
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 1)
      elif (game.runner1pos == 3):
        #Runner on Third
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher, result, 1)
        game.halfInningScore+=1
        game.runner1pos=2
        game.runner2pos=0
        game.runner3pos=0
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 1)
      elif (game.runner1pos == 2):
        #Runner on Second
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher, result, 1)
        game.halfInningScore+=1
        game.runner1pos=2
        game.runner2pos=0
        game.runner3pos=0
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 1)
      elif (game.runner1pos == 1):
        #Runner on First
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 0)
        game.runner1pos=2
        game.runner2pos=3
        game.runner3pos=0
      #No runners on base
      else:
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 0)
        game.runner1pos = 2
        game.runner2pos = 0
        game.runner3pos = 0
    elif (result=="Triple"):
      game.lineup_position+=1
      if (game.runner3pos != 0):
        #The Bases are Loaded
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 3)
        game.halfInningScore+=3
        game.runner1pos=3
        game.runner2pos=0
        game.runner3pos=0
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 3)
      elif (game.runner2pos == 3 and game.runner1pos == 2):
        #Runner on Second and Third
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 2)
        game.halfInningScore+=2
        game.runner1pos=3
        game.runner2pos=0
        game.runner3pos=0
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 2)
      elif (game.runner2pos == 3 and game.runner1pos == 1):
        #Runner on First and Third
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 2)
        game.halfInningScore+=2
        game.runner1pos=3
        game.runner2pos=3
        game.runner3pos=0
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 2)
      elif (game.runner2pos == 2 and game.runner1pos == 1):
        #Runner on First and Second
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 2)
        game.halfInningScore+=2
        game.runner1pos=3
        game.runner2pos=0
        game.runner3pos=0
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 2)
      elif (game.runner1pos == 3):
        #Runner on Third
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 1)
        game.halfInningScore+=1
        game.runner1pos=3
        game.runner2pos=0
        game.runner3pos=0
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 1)
      elif (game.runner1pos == 2):
        #Runner on Second
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 1)
        game.halfInningScore+=1
        game.runner1pos=3
        game.runner2pos=0
        game.runner3pos=0
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 1)
      elif (game.runner1pos == 1):
        #Runner on First
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 1)
        game.halfInningScore+=1
        game.runner1pos=3
        game.runner2pos=0
        game.runner3pos=0
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 1)
      #No runners on base
      else:
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 0)
        game.runner1pos = 3
        game.runner2pos = 0
        game.runner3pos = 0
    elif (result=="Home Run"):
      game.lineup_position+=1
      if (game.runner3pos != 0):
        #The Bases are Loaded
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 4)
        game.halfInningScore+=4
        game.runner1pos=0
        game.runner2pos=0
        game.runner3pos=0
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 4)
      elif (game.runner2pos == 3 and game.runner1pos == 2):
        #Runner on Second and Third
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 3)
        game.halfInningScore+=3
        game.runner1pos=0
        game.runner2pos=0
        game.runner3pos=0
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 3)
      elif (game.runner2pos == 3 and game.runner1pos == 1):
        #Runner on First and Third
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 3)
        game.halfInningScore+=3
        game.runner1pos=0
        game.runner2pos=0
        game.runner3pos=0
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 3)
      elif (game.runner2pos == 2 and game.runner1pos == 1):
        #Runner on First and Second
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 3)
        game.halfInningScore+=3
        game.runner1pos=0
        game.runner2pos=0
        game.runner3pos=0
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 3)
      elif (game.runner1pos == 3):
        #Runner on Third
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 2)
        game.halfInningScore+=2
        game.runner1pos=0
        game.runner2pos=0
        game.runner3pos=0
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 2)
      elif (game.runner1pos == 2):
        #Runner on Second
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 2)
        game.halfInningScore+=2
        game.runner1pos=0
        game.runner2pos=0
        game.runner3pos=0
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 2)
      elif (game.runner1pos == 1):
        #Runner on First
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 2)
        game.halfInningScore+=2
        game.runner1pos=0
        game.runner2pos=0
        game.runner3pos=0
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 2)
      #No runners on base
      else:
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 1)
        game.halfInningScore+=1
        game.runner1pos = 0
        game.runner2pos = 0
        game.runner3pos = 0
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 1)
    elif result== "Groundout":
      game.lineup_position+=1
      if (game.runner3pos != 0):
        #The Bases are Loaded
        if (game.outs < 2):
          #General Description
          general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 1)
          general_descriptions.append("Double Play!")
          game.halfInningScore+=1
          #Scoring Play! Add Description
          create_description(game.inning, game.current_hitter.name, result, 1)
        else:
          #General Description
          general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 0)
          general_descriptions.append("Double Play!")
        game.outs+=2
        game.runner1pos=3
        game.runner2pos=0
        game.runner3pos=0
        
      elif (game.runner2pos == 3 and game.runner1pos == 2):
        #Runner on Second and Third
        if (game.outs < 2):
          general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 1)
          game.halfInningScore+=1
          #Scoring Play! Add Description
          create_description(game.inning, game.current_hitter.name, result, 1)
        else:
          general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 0)
        game.outs+=1
        game.runner1pos=3
        game.runner2pos=0
        game.runner3pos=0
      elif (game.runner2pos == 3 and game.runner1pos == 1):
        #Runner on First and Third
        if (game.outs < 2):
          general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 1)
          general_description.append("Double Play!")
          game.halfInningScore+=1
          #Scoring Play! Add Description
          create_description(game.inning, game.current_hitter.name, result, 1)
        else:
          general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 0)
          general_description.append("Double Play!")
        game.outs+=2
        game.runner1pos=0
        game.runner2pos=0
        game.runner3pos=0
      elif (game.runner2pos == 2 and game.runner1pos == 1):
        #Runner on First and Second
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 0)
        general_descriptions.append("Double Play!")
        game.outs+=2
        game.runner1pos=3
        game.runner2pos=0
        game.runner3pos=0
      elif (game.runner1pos == 3):
        #Runner on Third
        if (game.outs < 2):
          general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 1)
          game.halfInningScore+=1
          #Scoring Play! Add Description
          create_description(game.inning, game.current_hitter.name, result, 1)
        else:
          general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 0)
        game.outs+=1
        game.runner1pos=0
        game.runner2pos=0
        game.runner3pos=0
      elif (game.runner1pos == 2):
        #Runner on Second
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 0)
        game.outs+=1
        game.runner1pos=3
        game.runner2pos=0
        game.runner3pos=0
      elif (game.runner1pos == 1):
        #Runner on First
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 0)
        general_descriptions.append("Double play!")
        game.outs+=2
        game.runner1pos=0
        game.runner2pos=0
        game.runner3pos=0
      #No runners on base
      else:
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 0)
        game.outs+=1
        game.runner1pos = 0
        game.runner2pos = 0
        game.runner3pos = 0
    elif result == "Flyout":
      game.lineup_position+=1
      if (game.runner3pos != 0):
        #The Bases are Loaded
        if (game.outs < 2):
          general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 1)
          game.halfInningScore+=1
          #Scoring Play! Add Description
          create_description(game.inning, game.current_hitter.name, result, 1)
        else:
          general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 0)
        game.outs+=1
        game.runner1pos=1
        game.runner2pos=2
        game.runner3pos=0
      elif (game.runner2pos == 3 and game.runner1pos == 2):
        #Runner on Second and Third
        if (game.outs < 2):
          general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 1)
          game.halfInningScore+=1
          #Scoring Play! Add Description
          create_description(game.inning, game.current_hitter.name, result, 1)
        else:
          general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 0)
        game.outs+=1
        game.runner1pos=3
        game.runner2pos=0
        game.runner3pos=0
      elif (game.runner2pos == 3 and game.runner1pos == 1):
        #Runner on First and Third
        if (game.outs < 2):
          general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 1)
          game.halfInningScore+=1
          #Scoring Play! Add Description
          create_description(game.inning, game.current_hitter.name, result, 1)
        else:
          general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 0)
        game.outs+=1
        game.runner1pos=1
        game.runner2pos=0
        game.runner3pos=0
      elif (game.runner2pos == 2 and game.runner1pos == 1):
        #Runner on First and Second
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 0)
        game.outs+=1
        game.runner1pos=1
        game.runner2pos=2
        game.runner3pos=0
      elif (game.runner1pos == 3):
        #Runner on Third
        if (game.outs < 2):
          general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 1)
          game.halfInningScore+=1
          #Scoring Play! Add Description
          create_description(game.inning, game.current_hitter.name, result, 1)
        else:
          general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 0)
        game.outs+=1
        game.runner1pos=0
        game.runner2pos=0
        game.runner3pos=0
      elif (game.runner1pos == 2):
        #Runner on Second
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 0)
        game.outs+=1
        game.runner1pos=3
        game.runner2pos=0
        game.runner3pos=0
      elif (game.runner1pos == 1):
        #Runner on First
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 0)
        game.outs+=1
        game.runner1pos=1
        game.runner2pos=0
        game.runner3pos=0
      #No runners on base
      else:
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 0)
        game.outs+=1
        game.runner1pos = 0
        game.runner2pos = 0
        game.runner3pos = 0
    else:
      print("There is an error")
    if (game.lineup_position == 9):
      game.lineup_position = 0
    game.current_hitter =    game.teamAtBat.lineup[game.lineup_position]






def simulate_half_inning(game):
  while game.outs < 3:
    at_bat_result = at_bat(game.current_hitter, game.current_pitcher)
    updateGameSituation(game, at_bat_result)
  if game.teamAtBat == game.team2:
    game.inning +=1

  if game.teamAtBat == game.team1:
    team1scores.append(game.halfInningScore)
  if game.teamAtBat == game.team2:
    team2scores.append(game.halfInningScore)
  if game.teamAtBat == game.team1:
    game.team1score+=game.halfInningScore
  if game.teamAtBat == game.team2:
    game.team2score+=game.halfInningScore
  general_descriptions.append("\n")
  if game.teamAtBat == game.team2:
    general_descriptions.append("End of Inning " + str(game.inning-1) + ".\nScore: " + game.team1.name + " " + str(game.team1score) + " " + game.team2.name + " " + str(game.team2score))
    general_descriptions.append("\n")
  game.outs = 0
  if game.teamAtBat == game.team1:
    game.current_pitcher = game.team1.starter
    game.teamAtBat = game.team2
  elif game.teamAtBat == game.team2:
    game.current_pitcher = game.team2.starter
    game.teamAtBat = game.team1
  game.current_hitter = game.teamAtBat.lineup[game.lineup_position]
  game.runner1pos = 0
  game.runner2pos = 0
  game.runner3pos = 0
  game.halfInningScore = 0




  
def simulate_game(game):
  is_game_over = False
  while is_game_over == False:
    simulate_half_inning(game)
    if game.inning > 9 and game.teamAtBat == game.team1:
      team1sum = 0
      for num in team1scores:
        team1sum+=num
      team2sum = 0
      for num in team2scores:
        team2sum+=num
      if (team1sum != team2sum):
        is_game_over = True
  #reset to default values for series and long sims
  game.inning = 1
  game.lineup_position = 0
  game.outs = 0
  game.runner1pos = 0
  game.runner2pos = 0
  game.runner3pos = 0
  game.current_hitter = game.team1.lineup[game.lineup_position]
  game.current_pitcher = game.team2.starter
  game.teamAtBat = game.team1
  game.halfInningScore = 0
  game.team1score = 0
  game.team2score = 0
      
      
      
      
      

def simulate_many_games(game, num_games):
  team1wins = 0
  team2wins = 0
  for i in range(num_games):
    simulate_game(game)
    team1sum = 0
    for num in team1scores:
      team1sum+=num
    team2sum = 0
    for num in team2scores:
      team2sum+=num
    if team1sum > team2sum:
      team1wins+=1
    elif team1sum < team2sum:
      team2wins+=1
    for i in range(len(team1scores)):
      team1scores.remove(team1scores[0])
      team2scores.remove(team2scores[0])
  team1pct = team1wins/num_games
  team2pct = team2wins/num_games
  return [team1pct, team2pct]




        
def create_hitter(PAs, strikeouts, hits, doubles, triples, homers, walks, name):
  k_pct = strikeouts/PAs
  hit_pct = hits/PAs
  double_pct = doubles/PAs
  triple_pct = triples/PAs
  homer_pct = homers/PAs
  single_pct = hit_pct-double_pct-triple_pct-homer_pct
  walk_pct = walks/PAs
  batted_ball_out_pct = 1-hit_pct-k_pct-walk_pct
  
  new_hitter = Hitter(k_pct, single_pct, double_pct, triple_pct, homer_pct, batted_ball_out_pct, walk_pct, name)
  return new_hitter
  
      
      
        

#Astros
verlander = Pitcher(0.278, hit_pct=0.186, walk_pct=0.041, go_ao_pct=(0.66), name="Justin Verlander")
altuve = create_hitter(604, 87, 158, 39, 0, 28, 66, "Jose Altuve")
pena = create_hitter(558, 135, 132, 20, 2, 22, 22, "Jeremy Pena")
yordan = create_hitter(561, 106, 144, 29, 2, 37, 78, "Yordan Alvarez")
bregman = Hitter(0.117, 0.1245, 0.057, 0, 0.035, 0.5335, 0.133, "Alex Bregman")
tucker = create_hitter(609, 95, 140, 28, 1, 30, 59, "Kyle Tucker")
gurriel = create_hitter(584, 73, 132, 40, 0, 8, 30, "Yuli Gurriel")
mancini = create_hitter(587, 135, 124, 23, 1, 18, 53, "Trey Mancini")
chas = create_hitter(407, 106, 88, 12, 2, 14, 46, "Chas McCormick")
vazquez = create_hitter(426, 69, 109, 23, 0, 9, 22, "Christian Vazquez")
astros_lineup = [altuve, pena, yordan, bregman, tucker, gurriel, mancini, chas, vazquez]




#Phillies
wheeler = Pitcher(0.269, "Update Later", 1.11, "Update Later", "Zach Wheeler")
schwarber = create_hitter(669, 200, 126, 21, 3, 46, 86, "Kyle Schwarber")
hoskins = create_hitter(672, 169, 145, 33, 2, 30, 72, "Rhys Hoskins")
realmuto = create_hitter(562, 119, 139, 26, 5, 22, 41, "JT Realmuto")
harper = Hitter(0.204, 0.138, 0.066, 0.0023, 0.04205, 0.43945, 0.108, "Bryce Harper")
castellanos = create_hitter(558, 130, 138, 27, 0, 13, 29, "Nick Castellanos")
bohm = create_hitter(631, 110, 164, 24, 3, 13, 31, "Alec Bohm")
segura = create_hitter(387, 58, 98, 9, 0, 10, 25, "Jean Segura")
stott = create_hitter(466, 89, 100, 19, 2, 10, 36, "Bryson Stott")
marsh = create_hitter(461, 158, 104, 18, 4, 11, 28, "Brandon Marsh")
phillies_lineup = [schwarber, hoskins, realmuto, harper, castellanos, bohm, segura, stott, marsh]




#define teams
astros = Team(starter=verlander, lineup=astros_lineup, name="Houston Astros")
phillies = Team(wheeler, phillies_lineup, "Philadelphia Phillies")


#Main menu
choice = int(input("Choose a simulation method: Game Recap (1), Play by Play (2), Many Games (3) "))





#Game Recap
if choice==1:
  team1 = int(input("Choose an away team: Astros (1) or Phillies (2) "))
  print("\n")
  if team1==1:
    current_game = Game(astros, phillies)
    away_team = astros
    home_team = phillies
  if team1==2:
    current_game = Game(phillies, astros)
    away_team = phillies
    home_team = astros
  #define game
  simulate_game(current_game)
  team1sum = 0
  for num in team1scores:
    team1sum+=num
  team2sum = 0
  for num in team2scores:
    team2sum+=num
  box_score = {'1': [team1scores[0],team2scores[0]], '2': [team1scores[1],team2scores[1]], '3': [team1scores[2],team2scores[2]], '4': [team1scores[3],team2scores[3]], '5': [team1scores[4],team2scores[4]], '6': [team1scores[5],team2scores[5]], '7': [team1scores[6],team2scores[6]], '8': [team1scores[7],team2scores[7]], '9': [team1scores[8],team2scores[8]], "Final": [team1sum, team2sum]}
  if len(team1scores)>9:
    extra_inning = 10
    while extra_inning<len(team1scores):
      box_score[str(extra_inning)] = [team1scores[extra_inning-1], team2scores[extra_inning-1]]
      extra_inning+=1
  box_score_df = pd.DataFrame(data=box_score, index=[away_team.name, home_team.name])
  print(box_score_df)
  print("\nScoring Plays: ")
  for item in scoring_plays_description:
    print(item)




#Play by Play    
if choice==2:
  team1 = int(input("Choose an away team: Astros (1) or Phillies (2) "))
  if team1==1:
    current_game = Game(astros, phillies)
    away_team = astros
    home_team = phillies
  if team1==2:
    current_game = Game(phillies, astros)
    away_team = phillies
    home_team = astros
  #define game
  simulate_game(current_game)
  print("Full play by play:")
  for item in general_descriptions:
    print(item)
  print("\n")
  team1sum = 0
  for num in team1scores:
    team1sum+=num
  team2sum = 0
  for num in team2scores:
    team2sum+=num
  box_score = {'1': [team1scores[0],team2scores[0]], '2': [team1scores[1],team2scores[1]], '3': [team1scores[2],team2scores[2]], '4': [team1scores[3],team2scores[3]], '5': [team1scores[4],team2scores[4]], '6': [team1scores[5],team2scores[5]], '7': [team1scores[6],team2scores[6]], '8': [team1scores[7],team2scores[7]], '9': [team1scores[8],team2scores[8]], "Final": [team1sum, team2sum]}
  box_score_df = pd.DataFrame(data=box_score, index=[away_team.name, home_team.name])
  print(box_score_df)





#Many Games
if choice==3:
  team1 = int(input("Choose an away team: Astros (1) or Phillies (2) "))
  if team1==1:
    current_game = Game(astros, phillies)
  if team1==2:
    current_game = Game(phillies, astros)
    
  num_games = int(input("How many games do you want to simulate? "))
  win_pcts = simulate_many_games(current_game, num_games)
  print("You simulated " + str(num_games) + " games.")
  print("The " + current_game.team1.name + " won  " + str(win_pcts[0]*100) + " percent of the time.")
  print("The " + current_game.team2.name + " won  " + str(win_pcts[1]*100) + " percent of the time.")
  