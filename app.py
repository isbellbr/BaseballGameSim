from flask import Flask, render_template, request
import random
import teams
import misc_funcs

app = Flask(__name__)

import pandas as pd


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
  hitter_or_pitcher = random.random()
  random_float = random.random()
  if (hitter_or_pitcher < 0.5):
    k_range_max = hitter.k_pct
    single_range_max = k_range_max + hitter.single_pct
    double_range_max = single_range_max + hitter.double_pct
    triple_range_max = double_range_max + hitter.triple_pct
    hr_range_max = triple_range_max + hitter.hr_pct
  else:
    k_range_max = pitcher.k_pct
    mod_single_pct = hitter.single_pct*pitcher.hit_pct
    mod_double_pct = hitter.double_pct*pitcher.hit_pct
    mod_triple_pct = hitter.triple_pct*pitcher.hit_pct
    mod_homer_pct = hitter.hr_pct*pitcher.hit_pct
    single_range_max = k_range_max + mod_single_pct
    double_range_max = single_range_max + mod_double_pct 
    triple_range_max = double_range_max + mod_triple_pct
    hr_range_max = triple_range_max + mod_homer_pct

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




#Helper Function for the Description Creation Functions
def desc_helper(result):
  if result == "Single":
    desc = " singles, scoring "
  elif result == "Double":
    desc = " doubles, scoring "
  elif result == "Triple":
    desc = "triples, scoring "
  elif result == "Home Run":
    desc = " homers, scoring "
  elif result == "Flyout":
    desc = " run scores on a sacrifice fly by "
  else:
    desc = " run scores on a RBI groundout by "
  return desc


#Run-Scoring Description Creation Function  
def create_description(inning, hitter_name, result, runs_scored):
  desc = desc_helper(result)
  
  #If not a flyout and not a groundout
  if result != "Flyout" and result != "Groundout":
    scoring_plays_description.append("Inning " +str(inning) + 
                                     ": " + hitter_name + desc + str(runs_scored) + " run(s).")
  #If a flyout or a groundout
  else:
    scoring_plays_description.append("Inning " +str(inning) 
                                     + ": " + str(runs_scored) + desc + hitter_name + ".")


    
#General Description Function (For Play-by-Play)
def general_description(inning, outs, hitter_name, 
                        pitcher_name, result, runs_scored):
  if runs_scored > 0:
      desc = desc_helper(result)
      
      #If not a flyout or groundout
      if result != "Flyout" or result != "Groundout":
        general_descriptions.append("Inning " +
                                    str(inning) + ": " + hitter_name 
                                    + desc + str(runs_scored) + 
                                    " run(s).")
      else:
        general_descriptions.append("Inning " +str(inning) 
                                    + ": " + str(runs_scored) 
                                    + desc + hitter_name)

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
    general_descriptions.append("Inning " +str(inning) + ": " +str(outs) 
                                + "out(s): "+ hitter_name + "  " + result 
                                + " on a pitch by " + pitcher_name +". ") 

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
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 2)
        game.halfInningScore+=2
        game.runner1pos=1
        game.runner2pos=2
        game.runner3pos=0
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 2)
      elif (game.runner2pos == 3 and game.runner1pos == 2):
        #Runner on Second and Third
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 2)
        game.halfInningScore+=2
        game.runner1pos=1
        game.runner2pos=0
        game.runner3pos=0
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 2)
      elif (game.runner2pos == 3 and game.runner1pos == 1):
        #Runner on First and Third
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 1)
        game.halfInningScore+=1
        game.runner1pos=1
        game.runner2pos=2
        game.runner3pos=0
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 1)
      elif (game.runner2pos == 2 and game.runner1pos == 1):
        #Runner on First and Second
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 1)
        game.halfInningScore+=1
        game.runner1pos=1
        game.runner2pos=3
        game.runner3pos=0
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 1)
      elif (game.runner1pos == 3):
        #Runner on Third
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 1)
        game.halfInningScore+=1
        game.runner1pos=1
        game.runner2pos=0
        game.runner3pos=0
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 1)
      elif (game.runner1pos == 2):
        #Runner on Second
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 1)
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
        game.runner2pos=3
        game.runner3pos=0
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
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 2)
        game.halfInningScore+=2
        game.runner1pos=2
        game.runner2pos=3
        game.runner3pos=0
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 2)
      elif (game.runner2pos == 3 and game.runner1pos == 2):
        #Runner on Second and Third
#General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 2)
        game.halfInningScore+=2
        game.runner1pos=2
        game.runner2pos=0
        game.runner3pos=0
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 2)
      elif (game.runner2pos == 3 and game.runner1pos == 1):
        #Runner on First and Third
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 1)
        game.halfInningScore+=1
        game.runner1pos=2
        game.runner2pos=3
        game.runner3pos=0
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 1)
      elif (game.runner2pos == 2 and game.runner1pos == 1):
        #Runner on First and Second
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 1)
        game.halfInningScore+=1
        game.runner1pos=2
        game.runner2pos=3
        game.runner3pos=0
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 1)
      elif (game.runner1pos == 3):
        #Runner on Third
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 1)
        game.halfInningScore+=1
        game.runner1pos=2
        game.runner2pos=0
        game.runner3pos=0
        #Scoring Play! Add Description
        create_description(game.inning, game.current_hitter.name, result, 1)
      elif (game.runner1pos == 2):
        #Runner on Second
        #General Description
        general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 1)
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
          general_descriptions.append("Double Play!")
          game.halfInningScore+=1
          #Scoring Play! Add Description
          create_description(game.inning, game.current_hitter.name, result, 1)
        else:
          general_description(game.inning, game.outs, game.current_hitter.name, game.current_pitcher.name, result, 0)
          general_descriptions.append("Double Play!")
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
        game.runner1pos=2
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
    game.current_hitter =  game.teamAtBat.lineup[game.lineup_position]

def simulate_half_inning(game):
  while game.outs < 3:
    at_bat_result = at_bat(game.current_hitter, game.current_pitcher)
    updateGameSituation(game, at_bat_result)
  if game.teamAtBat == game.team2:
    game.inning +=1

  if game.teamAtBat == game.team1:
    team1scores.append(game.halfInningScore)
    game.team1score+=game.halfInningScore

  if game.teamAtBat == game.team2:
    team2scores.append(game.halfInningScore)
    game.team2score+=game.halfInningScore

  general_descriptions.append("\n")
  if game.teamAtBat == game.team2:
    general_descriptions.append("End of Inning " + str(game.inning-1) + ".<b>Score: </b>" + game.team1.name + " " + str(game.team1score) + " " + game.team2.name + " " + str(game.team2score) + ".")
    general_descriptions.append("<br>")
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

#Astros
verlander = Pitcher(0.278, hit_pct=0.186, walk_pct=0.041, go_ao_pct=(0.66), name="Justin Verlander")

#Phillies
wheeler = Pitcher(0.269, hit_pct=0.223, walk_pct = 0.050, go_ao_pct=1.11, name="Zach Wheeler")

burnes = Pitcher(0.378, hit_pct=0.186, walk_pct=0.041, go_ao_pct=(0.66), name="Corbin Burnes")

team_lineups = teams.get_lineups()

#define teams
astros = Team(starter=verlander, lineup=team_lineups["Astros"], name="Houston Astros")
phillies = Team(starter = wheeler, lineup = team_lineups["Phillies"], name = "Philadelphia Phillies")
orioles = Team(starter=burnes, lineup=team_lineups["Orioles"], name = "Baltimore Orioles")

teams = {"Astros": astros, "Phillies": phillies, "Orioles": orioles}
  

#Function for providing output to the user based on their choice of simulation mode
def printToUser(choice, home_team, away_team, num_games=0):
  df_html = None
  to_return = None
  str_to_return = None
  away_team = teams[away_team]
  home_team = teams[home_team]
  
  #Game Recap
  if choice=="1":
    to_return = ""

    current_game = Game(away_team, home_team)
    #define game
    simulate_game(current_game)
    team1sum = 0
    for num in team1scores:
      team1sum+=num
    team2sum = 0
    for num in team2scores:
      team2sum+=num
    box_score = {'1': [team1scores[0],team2scores[0]], '2': [team1scores[1],team2scores[1]], '3': [team1scores[2],team2scores[2]], '4': [team1scores[3],team2scores[3]], '5': [team1scores[4],team2scores[4]], '6': [team1scores[5],team2scores[5]], '7': [team1scores[6],team2scores[6]], '8': [team1scores[7],team2scores[7]], '9': [team1scores[8],team2scores[8]]}
    
    #If there's extra innings, add them to the box score
    if len(team1scores)>9:
      extra_inning = 10
      while extra_inning<=len(team1scores):
        box_score[str(extra_inning)] = [team1scores[extra_inning-1], team2scores[extra_inning-1]]
        extra_inning+=1

    #Add the final score to the box score
    box_score["Final"] = [team1sum, team2sum]

    box_score_df = pd.DataFrame(data=box_score, index=[away_team.name, home_team.name])
    df_html = box_score_df.to_html(classes='data', header="true")
    #print(box_score_df)
    to_return = "<b>Scoring Plays</b><br>"
    for item in scoring_plays_description:
      to_return += ("\n" + item)

    scoring_plays_description.clear()
    general_descriptions.clear()
    team1scores.clear()
    team2scores.clear()

    return to_return, df_html




  #Play by Play    
  if choice=="2":
    current_game = Game(away_team, home_team)
    #define game
    simulate_game(current_game)

    str_to_return = "<b>Full play by play</b><br>"
    #print("Full play by play:")
    for item in general_descriptions:
      str_to_return += (item + "\n")
   #print("\n")
    team1sum = 0
    for num in team1scores:
      team1sum+=num
    team2sum = 0
    for num in team2scores:
      team2sum+=num
    box_score = {'1': [team1scores[0],team2scores[0]], '2': [team1scores[1],team2scores[1]], '3': [team1scores[2],team2scores[2]], '4': [team1scores[3],team2scores[3]], '5': [team1scores[4],team2scores[4]], '6': [team1scores[5],team2scores[5]], '7': [team1scores[6],team2scores[6]], '8': [team1scores[7],team2scores[7]], '9': [team1scores[8],team2scores[8]]}
    
    #If there's extra innings, add them to the box score
    if len(team1scores)>9:
      extra_inning = 10
      while extra_inning<=len(team1scores):
        box_score[str(extra_inning)] = [team1scores[extra_inning-1], team2scores[extra_inning-1]]
        extra_inning+=1

    #Add the final score to the box score
    box_score["Final"] = [team1sum, team2sum]

    box_score_df = pd.DataFrame(data=box_score, index=[away_team.name, home_team.name])
    #Convert df to html and display
    df_html = box_score_df.to_html(classes='data', header="true")

    scoring_plays_description.clear()
    general_descriptions.clear()
    team1scores.clear()
    team2scores.clear()

    return str_to_return, df_html

  #Many Games
  if choice=="3":
    current_game = Game(away_team, home_team)
      
    #num_games = int(input("How many games do you want to simulate? "))
    win_pcts = simulate_many_games(current_game, num_games)
    to_return = "<b>You simulated " + str(num_games) + " games.</b>"
    to_return += "\n" + ("The " + current_game.team1.name + 
                         " won  " + str(round(win_pcts[0]*100, 2)) + " percent of the time.")
    to_return += "\n" + ("The " + current_game.team2.name + 
                         " won  " + str(round(win_pcts[1]*100, 2)) + " percent of the time.")
    
    scoring_plays_description.clear()
    general_descriptions.clear()
    team1scores.clear()
    team2scores.clear()

    return to_return, df_html




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    mode = request.form.get('mode')
    num_games = request.form.get('num_games')
    home_team = request.form.get('home_team')
    away_team = request.form.get('away_team')

    # Convert num_games to integer if provided
    num_games = int(num_games) if num_games.isdigit() else None

    result = None
    
    result, df_html = printToUser(mode, home_team, away_team, num_games)
    if (mode != "3"):
      result = result.replace('.', '.<br>')
    else:
      result = result.replace("s.", "s.<br>")
    return render_template('index.html', result=result, table=df_html)

if __name__ == '__main__':
    app.run(debug=True)