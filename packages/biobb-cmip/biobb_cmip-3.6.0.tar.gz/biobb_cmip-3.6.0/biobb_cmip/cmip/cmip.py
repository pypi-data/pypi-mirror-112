#!/usr/bin/env python3

"""Module containing the Cmip class and the command line interface."""
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


class Cmip:
    """
    | biobb_cmip Titration
    | Wrapper class for the CMIP cmip module.
    | The CMIP cmip module. CMIP cmip module compute classical molecular interaction potentials.

    Args:
        input_pdb_path (str): Path to the input PDB file. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_cmip/master/biobb_cmip/test/data/cmip/1kim_h.pdb>`_. Accepted formats: pdb (edam:format_1476).
        input_probe_pdb_path (str) (Optional): Path to the input probe file in PDB format. File type: input. Accepted formats: pdb (edam:format_1476).
        output_pdb_path (str) (Optional): Path to the output PDB file. File type: output. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_cmip/master/biobb_cmip/test/reference/cmip/1kim_neutral.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_grd_path (str) (Optional): Path to the output grid file in GRD format. File type: output. Accepted formats: grd (edam:format_2330).
        output_cube_path (str) (Optional): Path to the output grid file in cube format. File type: output. Accepted formats: cube (edam:format_2330).
        output_rst_path (str) (Optional): Path to the output restart file. File type: output. Accepted formats: txt (edam:format_2330).
        output_byat_path (str) (Optional): Path to the output atom by atom energy file. File type: output. Accepted formats: txt (edam:format_2330).
        input_vdw_params_path (str) (Optional): Path to the CMIP input Van der Waals force parameters, if not provided the CMIP conda installation one is used ("$CONDA_PREFIX/share/cmip/dat/vdwprm"). File type: input. Accepted formats: txt (edam:format_2330).
        input_params_path (str) (Optional): Path to the CMIP input parameters file. File type: input. Accepted formats: txt (edam:format_2330).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **execution_type** (*str*) - ("mip") Default options for the params file. Each one creates a different params file. Values: mip (MIP O-  Mehler Solmajer dielectric), solvation (Solvation & MEP), energy (Docking Interaction energy calculation. PB electrostatics), docking (Docking Mehler Solmajer dielectric), docking_rst (Docking from restart file).
            * **params** (*dict*) - ({}) CMIP options specification.
            * **cmip_path** (*str*) - ("cmip") Path to the CMIP cmip executable binary.
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

            from biobb_cmip.cmip.cmip import cmip
            prop = { 'cmip_path': 'cmip' }
            cmip(input_pdb_path='/path/to/myStructure.pdb',
                      output_pdb_path='/path/to/newStructure.pdb',
                      output_log_path='/path/to/newStructureLog.log',
                      properties=prop)

    Info:
        * wrapped_software:
            * name: CMIP cmip
            * version: 2.7.0
            * license: Apache-2.0
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl
    """

    def __init__(self, input_pdb_path: str, input_probe_pdb_path: str = None, output_pdb_path: str = None,
                 output_grd_path: str = None, output_cube_path: str = None, output_rst_path: str = None,
                 output_byat_path: str = None, input_vdw_params_path: str = None, input_params_path: str = None,
                 properties: dict = None, **kwargs) -> None:

        properties = properties or {}

        self.combined_params_path = properties.get('combined_params_path', 'params')

        # Input/Output files
        self.io_dict = {
            "in": {"input_pdb_path": input_pdb_path, "input_probe_pdb_path": input_probe_pdb_path,
                   "input_vdw_params_path": input_vdw_params_path, "input_params_path": input_params_path},
            "out": {"output_pdb_path": output_pdb_path, "output_grd_path": output_grd_path,
                    "output_cube_path": output_cube_path, "output_rst_path": output_rst_path,
                    "output_byat_path": output_byat_path}
        }

        # Properties specific for BB
        self.cmip_path = properties.get('cmip_path', 'cmip')
        self.execution_type = properties.get('execution_type', 'mip')
        self.params = {k: str(v) for k, v in properties.get('params', dict()).items()}

        if not self.io_dict['in'].get('input_vdw_params_path'):
            self.io_dict['in']['input_vdw_params_path'] = f"{os.environ.get('CONDA_PREFIX')}/share/cmip/dat/vdwprm"
        self.io_dict['in']['combined_params_path'] = properties.get('combined_params_path', 'params')

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
        """Execute the :class:`Cmip <cmip.cmip.Cmip>` object."""
        tmp_files = []

        # Get local loggers from launchlogger decorator
        out_log = getattr(self, 'out_log', None)
        err_log = getattr(self, 'err_log', None)

        # Restart if needed
        if self.restart:
            if fu.check_complete_files(self.io_dict["out"].values()):
                fu.log('Restart is enabled, this step: %s will the skipped' % self.step, out_log, self.global_log)
                return 0

        # Check if output_pdb_path ends with ".pdb" and does not contain underscores
        if self.io_dict['out']['output_pdb_path']:
            if (not self.io_dict['out']['output_pdb_path'].endswith('.pdb')) or ("_" in str(Path(self.io_dict['out']['output_pdb_path']).name)):
                fu.log(f"ERROR: output_pdb_path ({self.io_dict['out']['output_pdb_path']}) name must end in .pdb and not contain underscores", out_log, self.global_log)
                raise ValueError(f"ERROR: output_pdb_path ({self.io_dict['out']['output_pdb_path']}) name must end in .pdb and not contain underscores")

        combined_params_dir = fu.create_unique_dir()
        tmp_files.append(combined_params_dir)
        self.io_dict['in']['combined_params_path'] = create_params_file(
            output_params_path=str(Path(combined_params_dir).joinpath(self.io_dict['in']['combined_params_path'])),
            input_params_path=self.io_dict['in']['input_params_path'],
            params_preset_dict=params_preset(execution_type=self.execution_type),
            params_properties_dict=self.params)

        container_io_dict = fu.copy_to_container(self.container_path, self.container_volume_path, self.io_dict)

        cmd = [self.cmip_path,
               '-i', container_io_dict['in']['combined_params_path'],
               '-vdw', container_io_dict['in']['input_vdw_params_path'],
               '-hs', container_io_dict['in']['input_pdb_path']]

        if container_io_dict["in"].get("input_probe_pdb_path") and Path(
                self.io_dict["in"].get("input_probe_pdb_path")).exists():
            cmd.append('-pr')
            cmd.append(container_io_dict["in"].get("input_probe_pdb_path"))

        if container_io_dict["out"].get("output_pdb_path"):
            cmd.append('-outpdb')
            cmd.append(container_io_dict['out']['output_pdb_path'])

        if container_io_dict["out"].get("output_grd_path"):
            cmd.append('-grdout')
            cmd.append(container_io_dict["out"]["output_grd_path"])

        if container_io_dict["out"].get("output_cube_path"):
            cmd.append('-cube')
            cmd.append(container_io_dict["out"]["output_cube_path"])

        if container_io_dict["out"].get("output_rst_path"):
            cmd.append('-rst')
            cmd.append(container_io_dict["out"]["output_rst_path"])
        if container_io_dict["out"].get("output_byat_path"):
            cmd.append('-byat')
            cmd.append(container_io_dict["out"]["output_byat_path"])

        cmd = fu.create_cmd_line(cmd,
                                 container_path=self.container_path,
                                 host_volume=container_io_dict.get("unique_dir"),
                                 container_volume=self.container_volume_path,
                                 container_working_dir=self.container_working_dir,
                                 container_user_uid=self.container_user_id,
                                 container_shell_path=self.container_shell_path,
                                 container_image=self.container_image,
                                 out_log=out_log, global_log=self.global_log)

        returncode = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log).launch()

        # CMIP removes or adds a .pdb extension from pdb output name
        if self.io_dict['out'].get('output_pdb_path'):
            if self.container_path:
                container_pdb_path = str(Path(container_io_dict.get('unique_dir')).joinpath(Path(container_io_dict["out"].get("output_pdb_path")).name))
            else:
                container_pdb_path = self.io_dict['out'].get('output_pdb_path')
            if Path(container_pdb_path[:-4]).exists():
                shutil.move(container_pdb_path[:-4], container_pdb_path)
            elif Path(container_pdb_path + ".pdb").exists():
                shutil.move(container_pdb_path + ".pdb", container_pdb_path)

        fu.copy_to_host(self.container_path, container_io_dict, self.io_dict)

        # Replace "ATOMTM" tag for "ATOM  "
        output_pdb_path = self.io_dict['out'].get('output_pdb_path')
        if output_pdb_path:
            with open(output_pdb_path) as pdb_file:
                list_pdb_lines = pdb_file.readlines()
            with open(output_pdb_path, 'w') as pdb_file:
                for line in list_pdb_lines:
                    pdb_file.write(line.replace('ATOMTM', 'ATOM  '))

        tmp_files.append(container_io_dict.get("unique_dir"))
        if self.remove_tmp:
            fu.rm_file_list(tmp_files, out_log=out_log)

        return returncode


def cmip(input_pdb_path: str, input_probe_pdb_path: str = None, output_pdb_path: str = None,
         output_grd_path: str = None, output_cube_path: str = None, output_rst_path: str = None,
         output_byat_path: str = None, input_vdw_params_path: str = None, input_params_path: str = None,
         properties: dict = None, **kwargs) -> int:
    """Create :class:`Cmip <cmip.cmip.Cmip>` class and
    execute the :meth:`launch() <cmip.cmip.Cmip.launch>` method."""

    return Cmip(input_pdb_path=input_pdb_path, input_probe_pdb_path=input_probe_pdb_path, output_pdb_path=output_pdb_path,
                output_grd_path=output_grd_path, output_cube_path=output_cube_path, output_rst_path=output_rst_path,
                output_byat_path=output_byat_path, input_vdw_params_path=input_vdw_params_path, input_params_path=input_params_path,
                properties=properties, **kwargs).launch()


def main():
    parser = argparse.ArgumentParser(description="Wrapper of the CMIP cmip module.",
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_pdb_path', required=True)
    parser.add_argument('--input_probe_pdb_path', required=False)
    parser.add_argument('--output_pdb_path', required=True)
    parser.add_argument('--output_grd_path', required=True)
    parser.add_argument('--output_cube_path', required=True)
    parser.add_argument('--output_rst_path', required=True)
    parser.add_argument('--output_byat_path', required=True)
    parser.add_argument('--input_vdw_params_path', required=False)
    parser.add_argument('--input_params_path', required=False)

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    cmip(input_pdb_path=args.input_pdb_path, input_probe_pdb_path=args.input_probe_pdb_path, output_pdb_path=args.output_pdb_path,
         output_grd_path=args.output_grd_path, output_cube_path=args.output_cube_path, output_rst_path=args.output_rst_path,
         output_byat_path=args.output_byat_path, input_vdw_params_path=args.input_vdw_params_path, input_params_path=args.input_params_path,
         properties=properties)


if __name__ == '__main__':
    main()
