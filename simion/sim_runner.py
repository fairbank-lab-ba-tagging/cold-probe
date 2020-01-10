# Tool for running simion simulations with several different parameters

from os import listdir, path, system, mkdir
import pandas as pd
import sys
from sim_helper import fly2_base_string, SIMION_path
from joblib import Parallel, delayed

# %%


def read_sims_file(file_path):
    """Takes a path to a csv file outlining the simulations to run.
    prepend command options with c_
    prepend adjustable variables with a_
    """

    df = pd.read_csv(file_path)
    print('Simulation Parameters...')
    print(df)
    return df


def create_fly2(sim_num, num_ions):
    """Creates a .fly2 file for each simulation to run.
    Currently only changes number of ions to fly
    """

    string = fly2_base_string.format(num=num_ions)
    string = string.replace('@', '{').replace('#', '}')

    file_path = project_path + 'fly2s\\ions_{}.fly2'.format(sim_num)
    f = open(file_path, 'w')
    f.write(string)
    f.close()

    return file_path


def create_command(iob_path, fly2_path, command_arg_list, adjustable_arg_list):
    """Creates the final command string to be run
    """

    command_base = "{simion} --nogui fly {fly_args} --particles={fly2_path} {iob_path}"

    fly_args = ''
    for param, val in command_arg_list:
        fly_args += ' --{p}={v}'.format(p=param[2:], v=val)

    for param, val in adjustable_arg_list:
        fly_args += ' --adjustable {name}={v}'.format(name=param[2:], v=val)

    return command_base.format(simion=SIMION_path,
                               fly_args=fly_args,
                               fly2_path=fly2_path,
                               iob_path=iob_path)


def get_commands():
    """Reads the sims file for the parameters then creates the commands.
    returns a list of commands to be run.
    """

    commands = []

    sims_df = read_sims_file(project_path + 'sims.csv')

    # print('Commands:')
    for sim in sims_df.iterrows():
        series = sim[1]

        sim_num = series.sim
        num_ions = series.num_ions
        fly2_path = create_fly2(sim_num=sim_num, num_ions=num_ions)

        command_args = [arg for arg in series.index if arg[0:2] == 'c_']
        adj_args = [arg for arg in series.index if arg[0:2] == 'a_']

        command_tuples = [(param, val) for param, val in zip(command_args, series[command_args])]
        adj_tuples = [(param, val) for param, val in zip(adj_args, series[adj_args])]

        iob_path = series.iob_path

        command_string = create_command(iob_path=project_path + iob_path,
                                        fly2_path=fly2_path,
                                        command_arg_list=command_tuples,
                                        adjustable_arg_list=adj_tuples)
        commands.append(command_string)
        print(command_string)

    return commands


if __name__ == '__main__':

    project_path = sys.argv[1]
    project_path = path.abspath(project_path) + '\\'
    print('Project Path: {}'.format(project_path))

    if not path.exists(project_path + '\\fly2s'):
        print('Creating "fly2s" dir...')
        mkdir(project_path + '\\fly2s')

    if not path.exists(project_path + '\\outputs'):
        print('Creating "outputs" dir...')
        mkdir(project_path + '\\outputs')

    commands = get_commands()
    Parallel(n_jobs=4)(delayed(system)(command) for command in commands)
