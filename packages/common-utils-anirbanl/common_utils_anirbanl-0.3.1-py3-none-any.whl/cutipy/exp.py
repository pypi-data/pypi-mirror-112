import argparse
import functools
import time, sys, os
from cutipy.putils import *
from cutilib.fm import JSON
from pathlib import Path
from cutilib.wandb import Wandb

def experiment(_func=None, *,
               work_dir='.',
               expt_name='default',
               expt_id=f"{time.time()}",
               wandb_loc=None
               ):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args):
            parser = argparse.ArgumentParser()
            parser.add_argument("--hp", type=deserialize_hp, help="hyperparameters")
            parser.add_argument("--hp_json", type=str, help="JSON file containing hyperparameters")
            new_args = parser.parse_args()

            if new_args.hp:
                print(f"****HP Arguments: {new_args.hp}")
            else:
                new_args.hp = deepdict(JSON.load(new_args.hp_json))
                print(f"****HP Arguments from JSON: {new_args.hp}")

            expt_loc = os.path.join(work_dir, f"{expt_name}-{expt_id}")
            ### Create experiment directory
            Path(expt_loc).mkdir(parents=True, exist_ok=False)
            new_args.hp.expdir = os.path.abspath(expt_loc)
            new_args.hp.hostname = os.uname()
            new_args.hp.starttime = time.time()

            ### Dump hp to json in work_dir
            JSON.dump(new_args.hp.AsDict(), Path(os.path.join(expt_loc, 'pre_exp.json')))

            if wandb_loc and Path(wandb_loc).exists():
                # This json is a dict with two keys: key and entity
                wandb_cred = JSON.load(Path(wandb_loc))
                wandb_obj = Wandb(
                    **wandb_cred,
                    dir = new_args.hp.expdir,
                    config = new_args.hp.AsDict(),
                    project = expt_name,
                    name = expt_id
                )
                func.__globals__.update(wdb=wandb_obj)
            '''
            DANGER: Modifying global namespace of main method to include hp.
            Find less hackier ways later
            Based on https://stackoverflow.com/questions/39600106/using-a-decorator-to-bring-variables-into-decorated-function-namespace
            '''
            global_vars, local_vars = {'func': func, 'args': args}, {}
            func.__globals__.update(hp=new_args.hp)
            exec('_result = func(*args)', global_vars, local_vars)
            value = local_vars['_result']

            # Updating runtime stats
            func.__globals__['hp'].endtime = time.time()
            func.__globals__['hp'].timetaken = func.__globals__['hp'].endtime - new_args.hp.starttime
            ### Dump final hp to json in work_dir for including run stats
            JSON.dump(func.__globals__['hp'].AsDict(), Path(os.path.join(expt_loc, 'post_exp.json')))

            return value
        return wrapper

    if _func is None:
        return decorator
    else:
        return decorator(_func)

@experiment
def main():
    print('Hello World!')
    print('***MAGIC****')
    print(hp)
    print(f"Working expt dir: {hp.expdir}")
    print(f"Hostname: {hp.hostname}")

@experiment(work_dir='root',expt_name='anirbanl',expt_id='2')
def test():
    print('Hello World!')
    print('***MAGIC****')
    print(hp)
    print(f"Working expt dir: {hp.expdir}")
    print(f"Hostname: {hp.hostname}")

@experiment(work_dir='root',
            expt_name='anirbanl',
            expt_id='3',
            wandb_loc='../my_wandb.json')
def withwandb():
    print('Hello World!')
    print('***MAGIC****')
    print(hp)
    print(f"Working expt dir: {hp.expdir}")
    print(f"Hostname: {hp.hostname}")



if __name__ == '__main__':
    #main()
    #test()
    withwandb()
