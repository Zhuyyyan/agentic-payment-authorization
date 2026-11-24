import argparse
from .simulation.experiments import run
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--n',type=int);p.add_argument('--seeds',type=int);a=p.parse_args();run(a.n,a.seeds)
