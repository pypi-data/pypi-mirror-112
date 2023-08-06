# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.

from __future__ import annotations
import argparse
import datetime
from enum import Enum
import json
import os
import time
import typing
from pathlib import Path
import platform
import psutil
import shutil
import subprocess
import sys
import uuid
from tqdm import tqdm
from urllib.request import urlretrieve
import zipfile

__version__ = '0.3.14'
__af_version__ = '3.8'
__khiva_version__ = '0.5.0'
__khiva_python_version__ = '0.5.0'
__khiva_worker_version__ = '0.5.0'
__libsodium_version__ = 'v142'
__server_version__ = '1.2'
__kotlin_worker_version__ = '1.0'
__hadoop_version__ = '2.8.1'
__cristal_ui_version__ = '0.30.0'

__shapelets_home__ = Path.home() / '.shapelets'
if not __shapelets_home__.exists():
    __shapelets_home__.mkdir()

__libs_folder__ = __shapelets_home__ / 'libs'
if not __libs_folder__.exists():
    __libs_folder__.mkdir()

__runtime_folder__ = __shapelets_home__ / 'runtime'
if not __runtime_folder__.exists():
    __runtime_folder__.mkdir()

# Added this in order to support python 3.8 and above
# Our libraries loads c modules using ctypes, KNOWN ISSUES
if sys.version_info.major == 3 and sys.version_info.minor == 8:
    os.add_dll_directory(f"{__libs_folder__}")

__runtime_path_env__ = os.environ.copy()
__runtime_path_env__['PATH'] = f"{__libs_folder__}{os.pathsep}{__runtime_path_env__['PATH']}"
__runtime_path_env__['JAVA_OPTS'] = f"-Djava.library.path={__libs_folder__}"
__runtime_path_env__['SHAPELETS_SHARED_FOLDER'] = str(__shapelets_home__)
# Required by KHIVA library
__runtime_path_env__['KHIVA_DLL_DIR'] = f"{__libs_folder__}"

__blob_store_root__ = 'https://shapeletsbinaries.blob.core.windows.net'
__af_store_root__ = f"{__blob_store_root__}/arrayfire"
__khiva_store_root__ = f"{__blob_store_root__}/khiva"
__khiva_python_store_root__ = f"{__blob_store_root__}/khiva-python"
__khiva_python_worker_store_root__ = f"{__blob_store_root__}/python-khiva-worker"
__khiva_kotlin_worker_store_root__ = f"{__blob_store_root__}/kotlin-khiva-worker"
__libsodium_store_root__ = f"{__blob_store_root__}/libsodium"
__server_store_root__ = f"{__blob_store_root__}/shapelets"
__hadoop_store_root__ = f"{__blob_store_root__}/hadoop"
__cristal_ui_store_root__ = f"{__blob_store_root__}/cristal-ui"

__khiva_python_artifact__ = f"khiva-{__khiva_python_version__}-py3-none-any.whl"
__khiva_python_worker_artifact__ = f"shapelets_python_worker-{__khiva_worker_version__}-py3-none-any.whl"
__khiva_kotlin_worker_artifact__ = f"kotlin-worker-{__kotlin_worker_version__}.zip"
__server_artifact__ = f"server-{__server_version__}.zip"
__hadoop_artifact__ = f"hadoop-{__hadoop_version__}.zip"
__cristal_ui_artifact__ = f"cristal-ui-{__cristal_ui_version__}.zip"

__pip_install__ = [sys.executable, '-m', 'pip', 'install']

__runtime_path_env__['__HADOOP_HOME__'] = f"{__libs_folder__}{os.pathsep}hadoop-{__hadoop_version__}"


class ProcessType(Enum):
    PYTHON_WORKER = 'python'
    KOTLIN_WORKER = 'kotlin'
    SERVER = 'server'

    @staticmethod
    def type_of(process_type: str) -> ProcessType:
        return dict({
            'python': ProcessType.PYTHON_WORKER,
            'kotlin': ProcessType.KOTLIN_WORKER,
            'server': ProcessType.SERVER,
        }).get(process_type)


class ShapeletsProcess:
    """
    Represents a Shapelets process, one of the types defined by ProcessType.
    """

    _DETACHED_PROCESS_FLAG = 0x08000000  # no terminal window, detached process

    @staticmethod
    def pid_files():
        return (file for file in os.listdir(__runtime_folder__) if file.endswith('.txt'))

    @staticmethod
    def report_status():
        for pid_file in ShapeletsProcess.pid_files():
            ShapeletsProcess.load_from_file(pid_file).print_status()

    @staticmethod
    def load_from_file(pid_file: str) -> ShapeletsProcess:
        with open(__runtime_folder__ / pid_file, 'r') as pid_metadata:
            metadata = json.load(pid_metadata)
            instance = ShapeletsProcess(ProcessType.type_of(metadata['type']))
            instance.process_port = metadata['port']
            instance.process_backend = metadata['backend']
            instance.process_start = metadata['start']
            instance.process_cwd = metadata['cwd']
            instance.process_pid = metadata['pid']
        return instance

    def __init__(self, process_type: ProcessType, process_port: str = '8443', process_backend: str = 'CPU'):
        self.process_cwd = str(uuid.uuid1())
        self.process_type = process_type
        self.process_port = process_port
        self.process_backend = process_backend
        self.process_pid = None
        self.process_start = None

    def run_detached(self, command: typing.List[str]):
        # check can run and do maintenance
        for pid_file in ShapeletsProcess.pid_files():
            proc = ShapeletsProcess.load_from_file(pid_file)
            if (proc.process_type == self.process_type and proc.process_port == self.process_port):
                if proc.is_running:
                    return
                else:
                    proc.clear_persisted()
        process_cwd = __runtime_folder__ / self.process_cwd
        process_cwd.mkdir()
        self.process_pid = str(subprocess.Popen(
            command,
            creationflags=ShapeletsProcess._DETACHED_PROCESS_FLAG,
            env=__runtime_path_env__,
            cwd=process_cwd).pid)
        self.process_start = str(datetime.datetime.utcnow())
        self._persist()

    @property
    def is_running(self) -> bool:
        return psutil.pid_exists(int(self.process_pid))

    def kill(self):
        if self.is_running:
            process = psutil.Process(int(self.process_pid))
            for proc in process.children(recursive=True):
                proc.kill()
            process.kill()
            print(self)

    def tail_logs(self):
        logs_file = __runtime_folder__ / self.process_cwd / 'log'
        if self.process_type == ProcessType.SERVER:
            logs_file /= 'log.txt'
        if self.process_type == ProcessType.KOTLIN_WORKER:
            logs_file /= 'kotlin-worker.log'
        if self.process_type == ProcessType.PYTHON_WORKER:
            logs_file /= 'worker-python.log'
        try:
            with open(logs_file, 'r') as file:
                line = ''
                while True:
                    tmp = file.readline()
                    if tmp is not None:
                        line += tmp
                        if line.endswith('\n'):
                            print(line, end='')
                            line = ''
                    else:
                        time.sleep(1)
        except KeyboardInterrupt:
            pass

    def to_dict(self):
        return {
            'type': self.process_type.value,
            'port': self.process_port,
            'backend': self.process_backend,
            'start': self.process_start,
            'cwd': self.process_cwd,
            'pid': self.process_pid,
        }

    def clear_persisted(self):
        os.remove(__runtime_folder__ / self._persist_file_name)
        for _ in range(3):
            try:
                shutil.rmtree(__runtime_folder__ / self.process_cwd)
            except:
                time.sleep(1)
                pass

    @property
    def _persist_file_name(self):
        return f"{self.process_cwd}_{self.process_type.value}_{self.process_pid}.txt"

    def _persist(self):
        with open(__runtime_folder__ / self._persist_file_name, 'w') as pid_file:
            json.dump(self.to_dict(), pid_file, indent=4)
        print(self)
        print(self)

    def __str__(self):
        str_repr = f"{self.process_type.value} "
        str_repr += f"{'OK' if self.is_running else 'DEAD'}: "
        str_repr += f"port:{self.process_port}, "
        str_repr += f"backend:{self.process_backend}, "
        str_repr += f"start:{self.process_start}, "
        str_repr += f"cwd:{self.process_cwd}, "
        str_repr += f"pid:{self.process_pid}"
        return str_repr

    def print_status(self):
        print(self)


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def _download_resource(base_url: str,
                       dst_root: Path,
                       file_name: str,
                       force: bool = False,
                       unzip: bool = True,
                       pip_install: bool = False) -> Path:
    src_url = f"{base_url}/{file_name}"
    dst_artifact = dst_root / file_name
    if dst_artifact.exists() and not force:
        print(f"Artifact [{file_name}] already downloaded, try again with [-f True]")
    else:
        print(f"Downloading {src_url} to {dst_root}")
        with DownloadProgressBar(unit='B',
                                 unit_scale=True,
                                 unit_divisor=1024,
                                 miniters=1,
                                 desc=src_url.split('/')[-1]) as progress_bar:
            urlretrieve(src_url, dst_artifact, reporthook=progress_bar.update_to)
        if unzip:
            with zipfile.ZipFile(dst_artifact, 'r') as zip_ref:
                for file in tqdm(iterable=zip_ref.namelist(), total=len(zip_ref.namelist())):
                    zip_ref.extract(member=file, path=dst_root)
    if pip_install:
        subprocess.check_call(
            __pip_install__ + [str(dst_artifact)],
            env=__runtime_path_env__)
    return dst_artifact


def install_command(force: bool = False):
    system_name = platform.system().lower()
    _download_resource(
        __af_store_root__,
        __libs_folder__,
        f"arrayfire-full-{system_name}-{__af_version__}.zip",
        force=force)
    _download_resource(
        __khiva_store_root__,
        __libs_folder__,
        f"khiva-{system_name}-{__khiva_version__}.zip",
        force=force)
    _download_resource(
        __khiva_python_store_root__,
        __libs_folder__,
        __khiva_python_artifact__,
        force=force,
        pip_install=True)
    _download_resource(
        __khiva_python_worker_store_root__,
        __libs_folder__,
        __khiva_python_worker_artifact__,
        force=force,
        unzip=False,
        pip_install=True)
    _download_resource(
        __libsodium_store_root__,
        __libs_folder__,
        f"libsodium-{system_name}-{__libsodium_version__}.zip",
        force=force)
    _download_resource(
        __hadoop_store_root__,
        __libs_folder__,
        __hadoop_artifact__,
        force=force)
    _download_resource(
        __cristal_ui_store_root__,
        __libs_folder__,
        __cristal_ui_artifact__,
        force=force)
    _download_resource(
        __server_store_root__,
        __libs_folder__,
        __server_artifact__,
        force=force)
    _download_resource(
        __khiva_kotlin_worker_store_root__,
        __libs_folder__,
        __khiva_kotlin_worker_artifact__,
        force=force)


def worker_command_start(worker_type: str, port: str, backend: str):
    worker_type = ProcessType.type_of(worker_type)
    if worker_type == ProcessType.PYTHON_WORKER:
        proc = ShapeletsProcess(ProcessType.PYTHON_WORKER, process_port=port, process_backend=backend)
        proc.run_detached(['python-worker', '-p', port, '-b', backend])
    elif worker_type == ProcessType.KOTLIN_WORKER:
        if platform.system().lower() == 'windows':
            specific_script = 'kotlin-worker.bat'
        else:
            specific_script = 'kotlin-worker'
        kotlin_exe = str(__libs_folder__ / f'kotlin-worker-{__kotlin_worker_version__}' / 'bin' / specific_script)
        proc = ShapeletsProcess(ProcessType.KOTLIN_WORKER, process_port=port, process_backend=backend)
        proc.run_detached([kotlin_exe, '--port', port, '--backend', backend])
    else:
        sys.stderr.write(f"unknown worker type: {worker_type}")
        sys.exit(-1)


def server_command_start():
    if platform.system().lower() == 'windows':
        specific_script = 'server.bat'
    else:
        specific_script = 'server'
    server_exe = str(__libs_folder__ / f'server-{__server_version__}' / 'bin' / specific_script)
    ShapeletsProcess(ProcessType.SERVER).run_detached([server_exe])


def start_all_command():
    worker_command_start(ProcessType.PYTHON_WORKER.value, '52000', 'CPU')
    worker_command_start(ProcessType.KOTLIN_WORKER.value, '53666', 'CPU')
    server_command_start()


def stop_command(process_pid: str = None):
    stop_all = process_pid is None or process_pid in ('*', 'all', 'ALL', '.')
    for pid_file in ShapeletsProcess.pid_files():
        proc = ShapeletsProcess.load_from_file(pid_file)
        if stop_all or proc.process_pid == process_pid:
            proc.kill()
            proc.clear_persisted()


def tail_command(system_pid: str):
    for pid_file in ShapeletsProcess.pid_files():
        proc = ShapeletsProcess.load_from_file(pid_file)
        if proc.process_pid == system_pid:
            proc.tail_logs()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Shapelets run-time tools')
    subparsers = parser.add_subparsers(dest='command')

    # install command
    install_parser = subparsers.add_parser('install', help='Installs required 3rd party libs')
    install_parser.add_argument('-f', '--force', default=False, type=bool)

    # start command
    start_parser = subparsers.add_parser('start', help='Starts a Shapelets process')
    start_command_parser = start_parser.add_subparsers(dest='start_command')
    start_worker_parser = start_command_parser.add_parser('worker', help='Starts a Shapelets worker')
    start_worker_parser.add_argument('-t', '--type',
                                     choices=[ProcessType.PYTHON_WORKER.value,
                                              ProcessType.KOTLIN_WORKER.value],
                                     default=ProcessType.PYTHON_WORKER.value,
                                     type=str)
    start_worker_parser.add_argument('-p', '--port', default='52000', type=str)
    start_worker_parser.add_argument('-b', '--backend', choices=['CPU', 'GPU'], default='CPU', type=str)
    start_server_parser = start_command_parser.add_parser('server', help='Starts the Shapelets server')

    # status command
    status_parser = subparsers.add_parser('status', help='Reports the status of the system')

    # stop command
    stop_parser = subparsers.add_parser('stop', help='Stops a Shapelets process by pid')
    stop_parser.add_argument('-p', '-pid', '--pid', type=str,
                             help='["*", "all", "ALL", "." to stop all], pid or type (1st col)')

    # logs command
    tail_parser = subparsers.add_parser('tail', help='Tails the logs for a Shapelets process by pid')
    tail_parser.add_argument('-p', '-pid', '--pid', type=str, help='pid or type (1st col)')

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()

    elif args.command == 'install':
        install_command(args.force)

    elif args.command == 'start':
        if args.start_command is None:
            start_all_command()
        elif args.start_command == 'server':
            server_command_start()
        elif args.start_command == 'worker':
            worker_command_start(args.type, args.port, args.backend)

    elif args.command == 'status':
        ShapeletsProcess.report_status()

    elif args.command == 'stop':
        stop_command(args.pid)

    elif args.command == 'tail':
        if not args.pid:
            tail_parser.print_help()
        else:
            tail_command(args.pid)
