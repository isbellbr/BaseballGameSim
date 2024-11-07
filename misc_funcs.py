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