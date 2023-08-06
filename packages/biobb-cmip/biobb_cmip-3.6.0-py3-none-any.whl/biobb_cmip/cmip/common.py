""" Common functions for package biobb_cmip.cmip """
import re
import os

from typing import List, Dict, Tuple, Mapping, Union, Set, Sequence


def get_pdb_total_charge(pdb_file_path: str):
    # Biopython 1.9 does not capture charge of atoms in CMIP format
    # Should do it by hand
    total_charge = 0
    with open(pdb_file_path) as pdb_file:
        for line in pdb_file:
            if line[0:6].strip().upper() in ["ATOM", "HETATM"] and len(line) > 63:
                total_charge += float(line[55:63].strip())
    return total_charge


def probe_params_grid(probe_id: int = 0, readgrid: int = 2, pbfocus: int = 1, perfill: float = 0.6,
                      grid_int: Sequence[float] = (0.5, 0.5, 0.5)) -> Dict[str, str]:
    grid_dict = {}
    grid_dict[f"readgrid{probe_id}"] = f"{readgrid}"
    grid_dict[f"perfill{probe_id}"] = f"{perfill}"
    grid_dict['pbfocus'] = f"{pbfocus}"
    grid_dict['grid_int'] = f"INTX{probe_id}={grid_int[0]},INTY{probe_id}={grid_int[1]},INTZ{probe_id}={grid_int[2]}"

    return grid_dict

def params_grid(grid_type: str = 'cmip', readgrid: int = 0, perfill: float = 0.8,
                grid_int: Sequence[float] = (0.5, 0.5, 0.5),
                grid_dim: Sequence[float] = (64, 64, 64),
                grid_cen: Sequence[float] = (0.0, 0.0, 0.0)) -> Dict[str, str]:
    # grid_type older readgrid equivalences:
    #     2 proteina dist minima pecentatge, 4 distancia minima prot, 5 distancia al centre de masses
    #     1
    #     interaction = 0 , 3 explicita grid d'entrada
    #     cmip, titration, pbsolvation = 2, >3

    grid_dict = {}
    grid_dict[f"readgrid"] = f"{readgrid}"

    if grid_type in ['interaction', 'mip', 'energy', 'docking']:
        grid_dict['grid_cen'] = f"CENX={grid_cen[0]},CENY={grid_cen[1]},CENZ={grid_cen[2]}"
        grid_dict['grid_dim'] = f"DIMX={grid_dim[0]},DIMY={grid_dim[1]},DIMZ={grid_dim[2]}"
        grid_dict['grid_int'] = f"INTX={grid_int[0]},INTY={grid_int[1]},INTZ={grid_int[2]}"
    elif grid_type in ['solvation', 'titration']:
        grid_dict['perfill'] = f"{perfill}"
        grid_dict['grid_int'] = f"INTX={grid_int[0]},INTY={grid_int[1]},INTZ={grid_int[2]}"

    return grid_dict


def params_preset(execution_type: str) -> Dict[str, str]:
    params_dict = {}
    grid_dict = {}
    probe_grid_dict = {}
    if execution_type == 'titration':
        grid_dict = params_grid(grid_type='titration', readgrid=2, perfill=0.8, grid_int=(0.5, 0.5, 0.5) )
        params_dict = {
            'title': 'Titration',
            'tipcalc': 1,
            'calcgrid': 1,
            'irest': 0,
            'orest': 0,
            'coorfmt': 2,
            'dields': 2,
            'titration': 1, 'inifoc': 2, 'cutfoc': -0.5, 'focus': 1, 'ninter': 10, 'clhost': 1, 'titcut': 20.,
            'titwat': 10, 'titip': 10, 'titim': 10
        }
    elif execution_type == 'mip':
        grid_dict = params_grid(grid_type='mip', readgrid= 0,
                                grid_cen=(47.266, 83.4265, 54.174),
                                grid_dim=(46, 30, 37),
                                grid_int=(0.5, 0.5, 0.5))
        params_dict = {
            'title': 'MIP O-  Mehler Solmajer dielectric',
            'tipcalc': 0,
            'calcgrid': 1,
            'irest': 0,
            'orest': 0,
            'coorfmt': 2,
            'dields':  2,
            'cubeoutput': 1, 'carmip': -1, 'fvdw': 0.8
        }
#TODO 'carmip': 1,
    # wat: tipcalc: 1 + titration: 'inifoc': 2, 'cutfoc': -0.5, 'focus': 1, 'ninter': 10,
    elif execution_type == 'solvation':
        grid_dict = params_grid(grid_type='solvation', readgrid=2, perfill=0.2,
                                grid_int=(0.5, 0.5, 0.5))
        params_dict = {
            'title': 'Solvation & MEP',
            'tipcalc': 0,
            'calcgrid': 1,
            'irest': 0,
            'orest': 0,
            'coorfmt': 2,
            'cubeoutput': 1, 'vdw': 0,  'pbelec': 1,
            'novdwgrid': 1, 'solvenergy': 1, 'dielc': 1, 'dielsol': 80
        }

    elif execution_type == 'energy':
        grid_dict = params_grid(grid_type='energy', readgrid= 0,
                                grid_cen=(47.266, 83.4265, 54.174),
                                grid_dim=(46, 30, 37),
                                grid_int=(0.5, 0.5, 0.5))
        probe_grid_dict = probe_params_grid(probe_id= 0, readgrid= 2, pbfocus= 1, perfill= 0.6,
                                            grid_int=(1.5, 1.5, 1.5))
        params_dict = {
            'title': 'Docking Interaction energy calculation. PB electrostatics',
            'tipcalc': 3,
            'calcgrid': 1,
            'irest': 0,
            'orest': 0,
            'coorfmt': 2,
            'fvdw': 0.8, 'pbelec': 1, 'pbinic': 2, 'wgp': 0, 'ebyatom': 1
        }

    elif execution_type == 'docking':
        grid_dict = params_grid(grid_type='docking', readgrid= 0,
                                grid_cen=(47.266, 83.4265, 54.174),
                                grid_dim=(46, 30, 37),
                                grid_int=(0.5, 0.5, 0.5))

        params_dict = {
            'title': 'Docking Mehler Solmajer dielectric',
            'tipcalc': 2,
            'calcgrid': 1,
            'irest': 0,
            'orest': 1,
            'coorfmt': 2,
            'fvdw': 0.8, 'dields': 2, 'focus': 1, 'cutfoc': 100,
            'tiprot': 5, 'inifoc': 5, 'ninter': 20,
            'clhost': 1, 'minout': 50, 'splitpdb': 0
        }

    elif execution_type == 'docking_rst':
        params_dict = {
            'title': 'Docking from restart file',
            'readgrid': 0,
            'tipcalc': 2,
            'calcgrid': 1,
            'irest': 2,
            'orest': 1,
            'coorfmt': 2,
            'fvdw': 0.8, 'dields': 2, 'focus': 1, 'cutfoc': 100,
            'tiprot': 5, 'inifoc': 5, 'ninter': 20,
            'clhost': 1, 'minout': 50, 'splitpdb': 0, 'cutelec': 10.0
        }

    return {**params_dict, **grid_dict, **probe_grid_dict}


def read_params_file(input_params_path: str) -> Dict[str, str]:
    params_dict = {}
    with open(input_params_path) as input_params_file:
        params_dict['title']: input_params_file.readline()
        for line in input_params_file:
            line = line.replace(' ', '')
            if line.startswith('&'): continue
            param_list = line.split(',')
            for param in param_list:
                param_key, param_value = param.split("=")

                # Grid Values
                if len(param_key) > 3 and param_key[:3].startswith('INT'):
                    if params_dict.get('grid_int'):
                        params_dict['grid_int'] += f",{param_key}={param_value}"
                    else:
                        params_dict['grid_int'] = f"{param_key}={param_value}"
                elif len(param_key) > 3 and param_key[:3].startswith('CEN'):
                    if params_dict.get('grid_cen'):
                        params_dict['grid_cen'] += f",{param_key}={param_value}"
                    else:
                        params_dict['grid_cen'] = f"{param_key}={param_value}"
                elif len(param_key) > 3 and param_key[:3].startswith('DIM'):
                    if params_dict.get('grid_dim'):
                        params_dict['grid_dim'] += f",{param_key}={param_value}"
                    else:
                        params_dict['grid_dim'] = f"{param_key}={param_value}"
                # Rest of parameters
                else:
                    params_dict[param_key] = param_value
    return params_dict


def write_params_file(output_params_path: str, params_dict: Mapping[str, str]) -> str:
    with open(output_params_path, 'w') as output_params_file:
        output_params_file.write(f"{params_dict.pop('title', 'Untitled')}\n")
        output_params_file.write(f"&cntrl\n")
        for params_key, params_value in params_dict.items():
            if params_key in ['grid_int', 'grid_cen', 'grid_dim']:
                output_params_file.write(f" {params_value}\n")
            else:
                output_params_file.write(f" {params_key} = {params_value}\n")
        output_params_file.write(f"&end\n")
    return output_params_path


def create_params_file(output_params_path: str, input_params_path: str = None,
                       params_preset_dict: Mapping = None, params_properties_dict: Mapping = None) -> str:
    """ Gets a params dictionary and a presset and returns the path of the created params file for cmip.

    Args:


    Returns:
        str: params file path.
    """
    params_dict = {}

    if params_preset_dict:
        for k, v in params_preset_dict.items():
            params_dict[k] = v
    if input_params_path:
        input_params_dict = read_params_file(input_params_path)
        for k, v in input_params_dict.items():
            params_dict[k] = v
    if params_properties_dict:
        for k, v in params_properties_dict.items():
            params_dict[k] = v

    return write_params_file(output_params_path, params_dict)