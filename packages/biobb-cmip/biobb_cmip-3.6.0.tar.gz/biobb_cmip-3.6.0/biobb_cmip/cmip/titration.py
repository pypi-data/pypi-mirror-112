#!/usr/bin/env python3

"""Module containing the Titration class and the command line interface."""
import os
import argparse
import shutil
from pathlib import Path
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper
from biobb_cmip.cmip.common import create_params_file
from biobb_cmip.cmip.common import params_preset
from biobb_cmip.cmip.common import get_pdb_total_charge


class Titration:
    """
    | biobb_cmip Titration
    | Wrapper class for the CMIP titration module.
    | The CMIP titration module. CMIP titration module adds water molecules, positive ions (Na+) and negative ions (Cl-) in the energetically most favorable structure locations.

    Args:
        input_pdb_path (str): Path to the input PDB file. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_cmip/master/biobb_cmip/test/data/cmip/1kim_h.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_pdb_path (str): Path to the output PDB file. File type: output. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_cmip/master/biobb_cmip/test/reference/cmip/1kim_neutral.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_log_path (str): Path to the output Tritration log file LOG. File type: output. Accepted formats: log (edam:format_2330).
        input_vdw_params_path (str) (Optional): Path to the CMIP input Van der Waals force parameters, if not provided the CMIP conda installation one is used ("$CONDA_PREFIX/share/cmip/dat/vdwprm"). File type: input. Accepted formats: txt (edam:format_2330).
        input_params_path (str) (Optional): Path to the CMIP input parameters file. File type: input. Accepted formats: txt (edam:format_2330).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **params** (*dict*) - ({}) CMIP options specification.
            * **num_wats** (*int*) - (10) Number of water molecules to be added.
            * **neutral** (*bool*) - (False) Neutralize the charge of the system. If selected *num_positive_ions* and *num_negative_ions* values will not be taken into account.
            * **num_positive_ions** (*int*) - (10) Number of positive ions to be added (Tipatom IP=Na+).
            * **num_negative_ions** (*int*) - (10) Number of negative ions to be added (Tipatom IM=Cl-).
            * **titration_path** (*str*) - ("titration") Path to the CMIP Titration executable binary.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **container_path** (*str*) - (None)  Path to the binary executable of your container.
            * **container_image** (*str*) - ("cmip/cmip:latest") Container Image identifier.
            * **container_volume_path** (*str*) - ("/data") Path to an internal directory in the container.
            * **container_working_dir** (*str*) - (None) Path to the internal CWD in the container.
            * **container_user_id** (*str*) - (None) User number id to be mapped inside the container.
            * **container_shell_path** (*str*) - ("/bin/bash") Path to the binary executable of the container shell.


    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_cmip.cmip.titration import titration
            prop = { 'titration_path': 'titration' }
            titration(input_pdb_path='/path/to/myStructure.pdb',
                      output_pdb_path='/path/to/newStructure.pdb',
                      output_log_path='/path/to/newStructureLog.log',
                      properties=prop)

    Info:
        * wrapped_software:
            * name: CMIP Titration
            * version: 2.7.0
            * license: Apache-2.0
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl
    """

    def __init__(self, input_pdb_path: str, output_pdb_path: str, output_log_path: str,
                 input_vdw_params_path: str = None, input_params_path: str = None,
                 properties: dict = None, **kwargs) -> None:

        properties = properties or {}

        # Input/Output files
        self.io_dict = {
            "in": {"input_pdb_path": input_pdb_path, "input_vdw_params_path": input_vdw_params_path,
                   "input_params_path": input_params_path},
            "out": {"output_pdb_path": output_pdb_path, "output_log_path": output_log_path}
        }

        # Properties specific for BB
        self.neutral = properties.get('neutral', False)
        self.num_wats = properties.get('num_wats')
        self.num_positive_ions = properties.get('num_positive_ions')
        self.num_negative_ions = properties.get('num_negative_ions')
        self.titration_path = properties.get('titration_path', 'titration')
        self.output_params_path = properties.get('output_params_path', 'params')
        if not self.io_dict['in'].get('input_vdw_params_path'):
            self.io_dict['in']['input_vdw_params_path'] = f"{os.environ.get('CONDA_PREFIX')}/share/cmip/dat/vdwprm"
        self.params = {k: str(v) for k, v in properties.get('params', dict()).items()}

        # container Specific
        self.container_path = properties.get('container_path')
        self.container_image = properties.get('container_image', 'cmip/cmip:latest')
        self.container_volume_path = properties.get('container_volume_path', '/data')
        self.container_working_dir = properties.get('container_working_dir')
        self.container_user_id = properties.get('container_user_id')
        self.container_shell_path = properties.get('container_shell_path', '/bin/bash')

        # Properties common in all BB
        self.can_write_console_log = properties.get('can_write_console_log', True)
        self.global_log = properties.get('global_log', None)
        self.prefix = properties.get('prefix', None)
        self.step = properties.get('step', None)
        self.path = properties.get('path', '')
        self.remove_tmp = properties.get('remove_tmp', True)
        self.restart = properties.get('restart', False)

        # Check the properties
        fu.check_properties(self, properties)

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`Titration <cmip.titration.Titration>` object."""
        tmp_files = []

        # Get local loggers from launchlogger decorator
        out_log = getattr(self, 'out_log', None)
        err_log = getattr(self, 'err_log', None)

        # Restart if needed
        if self.restart:
            if fu.check_complete_files(self.io_dict["out"].values()):
                fu.log('Restart is enabled, this step: %s will the skipped' % self.step, out_log, self.global_log)
                return 0

        # Check if output_pdb_path ends with ".pdb"
        if not self.io_dict['out']['output_pdb_path'].endswith('.pdb'):
            fu.log('ERROR: output_pdb_path name must end in .pdb', out_log, self.global_log)
            raise ValueError("ERROR: output_pdb_path name must end in .pdb")

        container_io_dict = fu.copy_to_container(self.container_path, self.container_volume_path, self.io_dict)

        params_dir = fu.create_unique_dir()
        tmp_files.append(params_dir)
        # Adding neutral, num_negative_ions, num_positive_ions, num_wats
        if self.num_wats:
            self.params['titwat'] = str(self.num_wats)
        if self.num_positive_ions:
            self.params['titip'] = str(self.num_positive_ions)
        if self.num_negative_ions:
            self.params['titim'] = str(self.num_negative_ions)
        if self.neutral:
            charge = get_pdb_total_charge(self.io_dict['in']['input_pdb_path'])
            self.params['titip'] = '0'
            self.params['titim'] = '0'
            if int(round(charge)) > 0:
                self.params['titin'] = str(int(round(charge)))
            elif int(round(charge)) < 0:
                self.params['titip'] = abs(int(round(charge)))
            else:
                fu.log(f'Neutral flag activated however no positive or negative ions will be added because the system '
                       f'is already neutralized. System charge: {round(charge, 3)}', out_log, self.global_log)
            fu.log(f'Neutral flag activated. Current system charge: {round(charge, 3)}, '
                   f'positive ions to be added: {self.params["titip"]}, '
                   f'negative ions to be added: {self.params["titim"]}, '
                   f'final residual charge: {round(charge + int(self.params["titip"]) - int(self.params["titim"]), 3)}',
                   out_log, self.global_log)

        self.output_params_path = create_params_file(
            output_params_path=str(Path(params_dir).joinpath(self.output_params_path)),
            input_params_path=self.io_dict['in']['input_params_path'],
            params_preset_dict=params_preset(execution_type='titration'),
            params_properties_dict=self.params)

        if self.container_path:
            fu.log('Container execution enabled', out_log)
            shutil.copy2(self.output_params_path, container_io_dict.get("unique_dir"))
            self.output_params_path = str(Path(self.container_volume_path).joinpath(Path(self.output_params_path).name))

        cmd = [self.titration_path,
               '-i', self.output_params_path,
               '-vdw', container_io_dict['in']['input_vdw_params_path'],
               '-hs', container_io_dict['in']['input_pdb_path'],
               '-outpdb', container_io_dict['out']['output_pdb_path'][:-4],
               '-l', container_io_dict['out']['output_log_path']]

        cmd = fu.create_cmd_line(cmd, container_path=self.container_path,
                                 host_volume=container_io_dict.get("unique_dir"),
                                 container_volume=self.container_volume_path,
                                 container_working_dir=self.container_working_dir,
                                 container_user_uid=self.container_user_id,
                                 container_shell_path=self.container_shell_path,
                                 container_image=self.container_image,
                                 out_log=out_log, global_log=self.global_log)

        returncode = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log).launch()
        fu.copy_to_host(self.container_path, container_io_dict, self.io_dict)

        tmp_files.append(container_io_dict.get("unique_dir"))
        if self.remove_tmp:
            fu.rm_file_list(tmp_files, out_log=out_log)

        return returncode


def titration(input_pdb_path: str, output_pdb_path: str, output_log_path: str,
              input_vdw_params_path: str = None, input_params_path: str = None,
              properties: dict = None, **kwargs) -> int:
    """Create :class:`Titration <cmip.titration.Titration>` class and
    execute the :meth:`launch() <cmip.titration.Titration.launch>` method."""

    return Titration(input_pdb_path=input_pdb_path, output_pdb_path=output_pdb_path, output_log_path=output_log_path,
                     input_vdw_params_path=input_vdw_params_path, input_params_path=input_params_path,
                     properties=properties, **kwargs).launch()


def main():
    parser = argparse.ArgumentParser(description="Wrapper of the CMIP Titration module.",
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_pdb_path', required=True)
    required_args.add_argument('--output_pdb_path', required=True)
    required_args.add_argument('--output_log_path', required=True)
    parser.add_argument('--input_vdw_params_path', required=False)
    parser.add_argument('--input_params_path', required=False)

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    titration(input_pdb_path=args.input_pdb_path, output_pdb_path=args.output_pdb_path,
              output_log_path=args.output_log_path,
              input_vdw_params_path=args.input_vdw_params_path, input_params_path=args.input_params_path,
              properties=properties)


if __name__ == '__main__':
    main()
