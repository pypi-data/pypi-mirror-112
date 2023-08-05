# auto generated by update_py.py

import argparse
import json
import multiprocessing
import os
import subprocess
import sys
import tempfile
import time
import traceback

from linker import __version__ as linker_version

from . import __version__ as trader_version
from .gun_helpers import (CONFIG_DEFAULT_PATH, CONFIG_FOLDER, FIST_FAIL_MARK,
                          FIST_READY_MARK, print_fist_fail_mark,
                          print_fist_ready_mark)

LOGO_PRINT = '''
  _                 _                 _ _       _
 | |_ _ __ __ _  __| | ___ _ __ ___  | (_)_ __ | | __
 | __| '__/ _` |/ _` |/ _ \ '__/ __| | | | '_ \| |/ /
 | |_| | | (_| | (_| |  __/ |  \__ \_| | | | | |   <
  \__|_|  \__,_|\__,_|\___|_|  |___(_)_|_|_| |_|_|\_\

    ----------------
    info@puyuan.tech
    trader: {}
    linker: {}
    ----------------
'''.format(trader_version, linker_version)


class ConsoleEntrance(object):

    FIST_TYPES = ['master', 'tg', 'mg', 'tr', 'mr', 'oms', 'rms', 'bs', 'algo', 'rr', 'nn', 'pp', 'tp']  # ALL fist type supported
    RECORDER_TYPES = ['csv', 'kdb', 'influxdb']
    NOTIFICATION_TYPES = ['wxwork']

    HELP_MSG = '''
----------------------
gun <command> [<args>]

The most commonly used boxing commands are:
    help            show help info
    ctl             control panel for services
    version         get version
    config          config related ops
    status          show master status
    inspect         better status
    start           start process in background, foreground exit when inited
    stop            stop with a fist_name, 'gun stop \*' to stop all fists except master
    run             run process in foreground
    log             config logs
    account         config accounts
    key             generate rsa/curve keys
    db              db operations
    cmd             send command message to some fist or all
    runs            using a config.json like run.json to run all (like docker-compose)

    encrypt/decrypt to encrypt/decrypt data

    supported fist_type: {}
----------------------
'''.format(FIST_TYPES)

    def __init__(self):
        pass

    def _log(self, sub_cmd, msg):
        from linker.logger import Logger
        logger = Logger.get_logger('gun')
        logger.info(f'[{sub_cmd}] {msg}')

    def parse_and_execute(self):
        entry_parser = argparse.ArgumentParser(description='Trader Command Tool', usage=self.HELP_MSG)
        entry_parser.add_argument('command', help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = entry_parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command: ' + args.command + '\n')
            entry_parser.print_help()
            exit(1)

        # ------ parser start ------
        self.main_parser = argparse.ArgumentParser(description='gun run')
        self.main_parser.add_argument('-t', '--proc_type', choices=self.FIST_TYPES, help='process type')
        self.main_parser.add_argument('-f', '--fist_name', help='fist name')
        self.main_parser.add_argument('-g', '--gateway_name', help='gateway name')
        self.main_parser.add_argument('-a', '--acc_tag', help='account tag')
        self.main_parser.add_argument('-r', '--router_name', help='router name')
        self.main_parser.add_argument('-o', '--oms_name', help='oms name')
        self.main_parser.add_argument('-s', '--secondary_router_name', help='market router for mock')
        self.main_parser.add_argument('-p', '--package_name', help='package name')
        self.main_parser.add_argument('-d', '--db', action='store_true', help='enable db module')
        self.main_parser.add_argument('-j', '--json', action='store_true', help='load data from json config file')
        self.main_parser.add_argument('--disable_console_logger', action='store_true', help='redirect console logger to /dev/null after the fist was ready')
        # master usage
        self.main_parser.add_argument('--curve_key_name', help='specify the name of curve key used by master')
        self.main_parser.add_argument('--curve_key_dir', help='specify the path(dir) of curve key used by master')
        # gateway usage
        self.main_parser.add_argument('--proxy', action='store_true', help='use proxy settings in config.json')
        self.main_parser.add_argument('--sub', nargs='*', default=[], help='subscribe content, e.g. trade:ticker snap:ticker1,ticker2')
        self.main_parser.add_argument('--record_order', action='store_true', help='use sqlite database settings in config.json to record orders')
        # router usage
        self.main_parser.add_argument('--rt', choices=self.RECORDER_TYPES, help='recorder type like kdb/influxdb')
        self.main_parser.add_argument('--dir', help='recorder csv directory')
        self.main_parser.add_argument('--host', help='recorder host addr (str)')
        self.main_parser.add_argument('--port', help='recorder port (number)', type=int)
        self.main_parser.add_argument('--udp_port', help='recorder udp port (number)', type=int)
        self.main_parser.add_argument('--nt', choices=self.NOTIFICATION_TYPES, help='notification type like wxwork')
        self.main_parser.add_argument('--url', help='notification webhook url (str)')
        # parameter server usage
        self.main_parser.add_argument('--files_path', help='path of param files')
        # ------ parser end ------
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def help(self):
        print(self.HELP_MSG)

    def ctl(self):
        os.system("supervisorctl -c {}/supervisor/supervisord.conf".format(CONFIG_FOLDER))

    def version(self):
        print(LOGO_PRINT)

    def status(self):
        os.system("linker_status")

    def runs(self):
        argvs = sys.argv[2:]
        print(argvs)
        from .invoker import run_invoke
        run_invoke(argvs)

    def stop(self):
        fist_name = sys.argv[2]
        # create a fist and call related function
        from trader.gun_helpers import GunClientHelper
        helper = GunClientHelper('__killer', CONFIG_DEFAULT_PATH)
        helper.stop(fist_name)

    def join(self):
        fist_name = sys.argv[2]
        from trader.gun_helpers import GunClientHelper
        helper = GunClientHelper('__joiner', CONFIG_DEFAULT_PATH)
        helper.join(fist_name, join_wait_seconds=2)

    def run(self):
        if len(sys.argv) <= 2:
            print('[error] must specify -f --fist_type')
            print_fist_fail_mark()
            exit(0)
        fist_type = sys.argv[2]
        args = None
        if fist_type not in self.FIST_TYPES:
            if fist_type.startswith('-'):
                args = self.main_parser.parse_args(sys.argv[2:])
                fist_type = args.proc_type
        if fist_type not in self.FIST_TYPES:
            print_fist_fail_mark()
            self.main_parser.error('\n[UNSUPPORTED_TYPE] {} is not in supported list: {}'.format(fist_type, self.FIST_TYPES))
            return
        else:
            if args is None:
                args = self.main_parser.parse_args(sys.argv[3:])

            if args.disable_console_logger:
                from .gun_helpers import GUN_FALGS
                GUN_FALGS.DISABLE_CONSOLE_LOGGER = True

            self._run_instance(fist_type, args)

    def start(self):
        args = list(sys.argv)
        args[1] = 'run'
        cmd = ' '.join(args)
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        subprocess.Popen(cmd, shell=True, stdout=temp_file.file, stderr=subprocess.STDOUT, cwd='/shared/runtime')
        self._log('gun_start', 'start process and redirecting output... \n(psedo_cmd)\n{} > {} 2>&1\n'.format(cmd, temp_file.name))
        with open(temp_file.name) as f:
            while True:
                time.sleep(0.1)
                lines = f.readlines()
                if len(lines):
                    for line in lines:
                        print(line, end='')
                        exit_code = 0 if FIST_READY_MARK in line else (1 if FIST_FAIL_MARK in line else -1)
                        if exit_code != -1:
                            exit(exit_code)

    def _run_instance(self, fist_type, args):

        if fist_type in ['tg', 'mg']:
            if args.gateway_name is None or (fist_type == 'tg' and args.acc_tag is None):
                print_fist_fail_mark()
                self.main_parser.error('\n\n[MISSING_ARGS] tg requires -g -a, mg requires -g')
                return
            from trader.gun_helpers import Gateway, PythonGateway
            try:
                if args.package_name:
                    PythonGateway(args.package_name, fist_type, args.gateway_name, args.router_name, args.oms_name, sub_config=args.sub,
                                  fist_name=args.fist_name, acc_tag=args.acc_tag, use_proxy=args.proxy, from_json=args.json).run()
                else:
                    Gateway(fist_type, args.gateway_name, args.acc_tag, args.router_name, args.oms_name, args.record_order, args.secondary_router_name).run()
            except:
                print(traceback.format_exc())
                print_fist_fail_mark()

        elif fist_type in ['tr', 'mr']:
            from trader.gun_helpers import Router
            try:
                Router(fist_type, args.fist_name).run()
            except:
                print(traceback.format_exc())
                print_fist_fail_mark()

        elif fist_type in ['oms']:
            from trader.gun_helpers import GunOrderManagerService
            try:
                GunOrderManagerService(args.fist_name, args.router_name).run()
            except:
                print(traceback.format_exc())
                print_fist_fail_mark()

        elif fist_type in ['rms']:
            from trader.gun_helpers import RiskManagementService
            try:
                RiskManagementService(fist_name=args.fist_name, router1=args.router_name).run()
            except:
                print(traceback.format_exc())
                print_fist_fail_mark()

        elif fist_type in ['bs']:
            from trader.gun_helpers import BasketServer
            try:
                BasketServer(fist_name=args.fist_name, trade_router=args.router_name).run()
            except:
                print(traceback.format_exc())
                print_fist_fail_mark()

        elif fist_type in ['algo']:
            from trader.gun_helpers import AlgoServer
            try:
                if args.router_name:
                    trade_router, market_router = args.router_name.split('/')
                else:
                    trade_router, market_router = None, None
                AlgoServer(algo_type=args.fist_name, trade_router=trade_router, market_router=market_router).run()
            except:
                print(traceback.format_exc())
                print_fist_fail_mark()

        elif fist_type in ['rr']:
            if args.rt not in self.RECORDER_TYPES:
                print_fist_fail_mark()
                self.main_parser.error('\n\n[MISSING_ARGS] rr requires --rt, and only {} are supported'.format(str(self.RECORDER_TYPES)))
                return
            from trader.gun_helpers import GunRecorder
            router_names = args.router_name.split('/') if args.router_name else None
            try:
                if args.rt == 'csv':
                    _dir = args.dir or os.environ.get('CSV_FOLDER')
                    if _dir:
                        GunRecorder(args.fist_name, router_names, csv_dir=_dir).run()
                    else:
                        self.main_parser.error('\n\n[MISSING_ARGS] rr [csv] requires valid directory to store data')
                elif args.rt == 'kdb':
                    _host = args.host or 'localhost'
                    _port = args.port or os.environ.get('KDB_PORT')
                    if _host and _port:
                        GunRecorder(args.fist_name, router_names, kdb_host=args.host, kdb_port=args.port).run()
                    else:
                        self.main_parser.error('\n\n[MISSING_ARGS] rr [kdb] requires valid host and port')
                elif args.rt == 'influxdb':
                    _host = args.host or os.environ.get('INFLUXDB_HOST') or 'localhost'
                    _port = args.port or os.environ.get('INFLUXDB_PORT')
                    if _host and _port:
                        GunRecorder(args.fist_name, router_names, influx_host=args.host, influx_port=args.port, influx_udp_port=args.udp_port).run()
                    else:
                        self.main_parser.error('\n\n[MISSING_ARGS] rr [influxdb] requires valid host and port. host={} port={}'.format(_host, _port))
            except:
                print(traceback.format_exc())
                print_fist_fail_mark()

        elif fist_type in ['nn']:
            from trader.gun_helpers import GunNotificationCenter
            try:
                if args.nt == 'wxwork':
                    _url = args.url or os.environ.get('WXWORK_URL')
                    if _url:
                        GunNotificationCenter(args.fist_name, wxwork_url=_url).run()
                    else:
                        self.main_parser.error('\n\n[MISSING_ARGS] nn [wxwork] requires valid url')
            except:
                print(traceback.format_exc())
                print_fist_fail_mark()

        elif fist_type in ['pp']:
            from trader.gun_helpers import GunParamServer
            try:
                GunParamServer(args.fist_name, args.files_path).run()
            except:
                print(traceback.format_exc())
                print_fist_fail_mark()

        elif fist_type in ['tp']:
            from trader.gun_helpers import GunTunnelPeer
            try:
                GunTunnelPeer(args.fist_name, args.gateway_name, args.files_path).run()
            except Exception:
                print(traceback.format_exc())
                print_fist_fail_mark()

        elif fist_type in ['master']:
            import liblinker
            from .helpers import KeyHelper
            from trader.constant import CURVE_KEY_DIR
            try:
                if args.curve_key_dir:
                    curve_key_dir = args.curve_key_dir
                else:
                    curve_key_dir = CURVE_KEY_DIR
                master = liblinker.Master(KeyHelper.get_private_key(args.curve_key_name, curve_key_dir))
                master.start()
                print_fist_ready_mark()
                master.join()
            except:
                print(traceback.format_exc())
                print_fist_fail_mark()

        else:
            print_fist_fail_mark()
            raise NotImplementedError('process type "{}" not implemented yet'.format(fist_type))

    def config(self):
        from trader.gun_helpers import ConfigHelper
        parser = argparse.ArgumentParser(description="gun update_config")
        me_group = parser.add_mutually_exclusive_group()
        me_group.add_argument('-u', '--upgrade', action="store_true", help='to upgrade config file')
        me_group.add_argument('-c', '--check', action='store_true', help='to check config file')
        parser.add_argument('-d', '--config_dir', type=str, default=CONFIG_FOLDER, help='directory where config file was stored')
        args = parser.parse_args(sys.argv[2:])

        config_helper = ConfigHelper(args.config_dir)
        if args.upgrade:
            # backup config file
            config_helper.backup_config()
            # upgrade config file
            config_helper.update_config()
            print('current_version: {}'.format(config_helper.current_config_version))
            config_helper.dump_config()
            print("finished updating config")

        elif args.check:
            print('config path: {}'.format(config_helper.config_path))
            config_helper.check_version()

        else:
            config_helper.open_config_to_edit()

    def log(self):
        from trader.gun_helpers import LogHelper

        parser = argparse.ArgumentParser(description="gun log")
        parser.add_argument('action', choices=['clean', 'tail', 'ls'], help='action to take')
        parser.add_argument('-t', '--expired_time', help='log expired time (int)', type=int)
        parser.add_argument('-f', '--fist_name', help='fist name')
        parser.add_argument('-p', '--path', nargs='*', default=[], help='log path, e.g. /shared/log /opt/log')
        args = parser.parse_args(sys.argv[2:])

        paths = []
        if len(args.path):
            for arg in args.path:
                assert os.path.isdir(arg), '"{}" is not an existing directory'.format(arg)
                paths.append(os.path.abspath(arg))

        log_helper = LogHelper(paths)

        if args.action == 'clean':
            if args.expired_time is not None:
                log_helper.clean_expired_log(args.expired_time)
            else:
                parser.error('\n\n[MISSING_ARGS] [clean] requires expired time')

        elif args.action == 'tail':
            if args.fist_name:
                log_helper.tail_latest_log(args.fist_name)
            else:
                parser.error('\n\n[MISSING_ARGS] [tail] requires fist name')

        elif args.action == 'ls':
            log_helper.show_fist_list()

    def account(self):
        from .helpers import AccountHelper, KeyHelper

        parser = argparse.ArgumentParser(description="gun update_config")
        parser.add_argument('action', choices=['list', 'new', 'delete'], help='action to take')
        parser.add_argument('-a', '--acc_tag', help='account name')
        parser.add_argument('-k', '--key_name', help='encryption key')
        parser.add_argument('-c', '--content', nargs='*', default=[], help='config content, e.g. key1:value1 key2:value2')
        parser.add_argument('-f', '--force', action='store_true', help='force save/delete')
        args = parser.parse_args(sys.argv[2:])

        acc_helper = AccountHelper()
        if args.action == 'new':
            assert None not in [args.acc_tag], '-a is required'
            if args.key_name is not None:
                assert KeyHelper.key_exists(args.key_name), 'key "{}" not existed!'.format(args.key_name)
            acc_config = {}
            if len(args.content):
                for arg in args.content:
                    key, value = arg.split(':')
                    acc_config[key] = value
            else:
                print('[warning] no config content specified')
            acc_helper.save_account(args.acc_tag, acc_config, args.key_name, force=args.force)

        elif args.action == 'list':
            accounts = acc_helper.get_accounts()
            print('total accounts: {}'.format(len(accounts)))
            for idx, account in enumerate(accounts, 1):
                print('{}. {}\n{}'.format(idx, account.acc_tag, json.dumps(account.acc_config, indent=2)))
                if account.key_name is not None:
                    print('(encrypted with key "{}")'.format(account.key_name))

        elif args.action == 'delete':
            assert None not in [args.acc_tag], '-a is required'
            acc_helper.delete_account(args.acc_tag)

    def _show_key(self, key_name, key_path):
        from .helpers import KeyHelper

        if not KeyHelper.key_exists(key_name, key_path):
            print('[error] key "{}" not exists at {}'.format(key_name, key_path))
        else:
            _, public_key_path = KeyHelper.get_key_paths(key_name, key_path)
            print('showing "{}" keys:'.format(key_name))
            print()
            print('1. private_key (path: (hidden)):')
            print()
            print('(hidden)')
            print()
            with open(public_key_path) as f:
                print('2. public_key (path: {}):'.format(public_key_path))
                print()
                print(''.join(f.readlines()))
                print()
            print('to save the public key in another location')
            print('please create a file with name "{}.pub"'.format(key_name))
            print('then copy/paste the above public key to the file (including the BEGIN/END lines, if exist)')

    def _list_keys(self, key_path):
        from .helpers import KeyHelper
        key_names = KeyHelper.get_existed_key_names(key_path)
        print('total keys: {}'.format(len(key_names)))
        print('\n'.join(['{}. {}'.format(idx, name) for idx, name in enumerate(key_names, 1)]))

    def key(self):
        import linker.rsa_encrypter as rsa
        from zmq import curve_keypair
        from trader.constant import USER_RSA_KEY_DIR, CURVE_KEY_DIR
        from .helpers import KeyHelper

        parser = argparse.ArgumentParser(description='gun key')
        parser.add_argument('action', choices=['list', 'show', 'new', 'delete'], help='action to take')
        parser.add_argument('-k', '--key_name', default='default_key', help='key name')
        parser.add_argument('-t', '--key_type', choices=['rsa', 'curve'], default='rsa', help='key type')
        parser.add_argument('-f', '--force', action='store_true', help='force delete/save')
        args = parser.parse_args(sys.argv[2:])
        if args.key_type == 'rsa':
            key_path = USER_RSA_KEY_DIR
        elif args.key_type == 'curve':
            key_path = CURVE_KEY_DIR
        else:
            assert False, f'invalid key type: {args.key_type}, not support'

        if args.action == 'new':
            if KeyHelper.key_exists(args.key_name, key_path) and not args.force:
                print('[warning] skip adding "{}", key already existed at {}'.format(args.key_name, key_path))
                print('to overwrite, please specify -f')
            else:
                if key_path == USER_RSA_KEY_DIR:
                    private_key, public_key = rsa.gen_rsa_keys()
                else:
                    # this branch must be curve key
                    public_key, private_key = curve_keypair()
                private_key_path, public_key_path = KeyHelper.get_key_paths(args.key_name, key_path)
                KeyHelper.write_key_to_file(private_key, private_key_path)
                KeyHelper.write_key_to_file(public_key, public_key_path)
                self._show_key(args.key_name, key_path)

        elif args.action == 'show':
            self._show_key(args.key_name, key_path)

        elif args.action == 'delete':
            if not KeyHelper.key_exists(args.key_name, key_path):
                print('[warning] skipped, key "{}" not exists at {}'.format(args.key_name, key_path))
            else:
                private_key_path, public_key_path = KeyHelper.get_key_paths(args.key_name, key_path)
                os.remove(private_key_path)
                os.remove(public_key_path)
                print('[info] key "{}" at {} has been removed'.format(args.key_name, key_path))

        elif args.action == 'list':
            self._list_keys(key_path)

    def db(self):
        from .database.models import Base
        from .database.connector import DatabaseConnector

        parser = argparse.ArgumentParser(description='gun db')
        parser.add_argument('action', choices=['create', 'init', 'drop', 'print', 'exec', 'migrate'], help='actions to take')
        parser.add_argument('sql', nargs='*', default=[], help='sql to execute')
        parser.add_argument('--db', default='db_core', help='db to operate on')
        args = parser.parse_args(sys.argv[2:])

        db_name = args.db
        if args.action == 'create':
            print('creating databse "{}"'.format(db_name))
            engine = DatabaseConnector(db='').get_engine()
            engine.execute('CREATE DATABASE IF NOT EXISTS {}'.format(db_name))
            print('done!')

        elif args.action == 'init':
            # create tables
            print('creating tables on {}...'.format(db_name))
            Base.metadata.create_all(bind=DatabaseConnector(db=db_name).get_engine())
            print('done!')

        elif args.action == 'drop':
            engine = DatabaseConnector(db='').get_engine()
            print('to drop db "{}"...'.format(db_name))
            engine.execute('DROP DATABASE {}'.format(db_name))
            print('done!')

        elif args.action == 'print':
            engine = DatabaseConnector()
            print(engine)

        elif args.action in ['exec', 'migrate']:
            def _exec_sql(engine, sql):
                print('[exec] (on: {})'.format(args.db))
                print(sql + (';' if not sql.endswith(';') else ''))
                print()
                try:
                    res = engine.execute(sql)
                except Exception as e:
                    print('[error]')
                    print(e)
                else:
                    print('[result]')
                    if res and res.returns_rows:
                        rows = res.fetchall()
                        for r in rows:
                            print('\t'.join([str(e) for e in r]) if r else '')
                    else:
                        print('(empty/not-parsed)')

            if args.action == 'exec':
                if not args.sql:
                    parser.error('must also provide a valid sql statement')
                sql = ' '.join(args.sql)
                sqls = [sql]
            elif args.action == 'migrate':
                from .database.migrate_scripts import DB_MIGRATE_SQLS
                sqls = DB_MIGRATE_SQLS.get(db_name, [])

            print('#{} sql(s) to run...'.format(len(sqls)))
            if len(sqls) == 0:
                return
            engine = DatabaseConnector(db=args.db).get_engine()
            for idx, s in enumerate(sqls, 1):
                print(f'{idx} {"#" * 100}')
                _exec_sql(engine, s)
                print()

    def encrypt(self):
        from .helpers import KeyHelper
        from linker import rsa_encrypter as rsa

        parser = argparse.ArgumentParser()
        parser.add_argument('-k', '--key_name', default='default_key', help='specify the key to use in encryption')
        parser.add_argument('data', help='the data to encrypt')
        args = parser.parse_args(sys.argv[2:])

        assert KeyHelper.key_exists(args.key_name), 'key "{}" not found'.format(args.key_name)

        _, public_key_path = KeyHelper.get_key_paths(args.key_name)
        encrypted_data = rsa.encode_msg(args.data, public_pem_file=public_key_path)
        print('encrypted data:')
        print()
        print(encrypted_data)
        print()

    def decrypt(self):
        from .helpers import KeyHelper
        from linker import rsa_encrypter as rsa

        parser = argparse.ArgumentParser()
        parser.add_argument('-k', '--key_name', default='default_key', help='specify the key to use in decryption')
        parser.add_argument('data', help='the data to decrypt')
        args = parser.parse_args(sys.argv[2:])

        assert KeyHelper.key_exists(args.key_name), 'key "{}" not found'.format(args.key_name)

        private_key_path, _ = KeyHelper.get_key_paths(args.key_name)
        decrypted_data = rsa.decode_msg(args.data, private_pem_file=private_key_path)
        print('decrypted data:')
        print()
        print(decrypted_data)
        print()

    def cmd(self):
        from trader.gun_helpers import CmdFist

        parser = argparse.ArgumentParser(description='gun cmd')
        parser.add_argument('-f', '--target_fist', help='which fist to send this cmd ("*") for all', required=True)
        me_group = parser.add_mutually_exclusive_group(required=True)
        me_group.add_argument('-c', '--content', help='message content in string format (json-parsable)')
        me_group.add_argument('-p', '--file_path', help='file of which content is sent as cmd')
        parser.add_argument('-w', '--wait_time', default=-1, help='seconds to wait for response, if -1 quit until the first rsp', type=int)
        args = parser.parse_args(sys.argv[2:])
        print('[cmd]', args.content or args.file_path)

        content = None
        if args.content:
            content = json.loads(args.content)
        elif args.file_path:
            content = json.load(open(args.file_path))

        cmd = CmdFist('__cmd__')
        cmd.create_fist()
        cmd.start()
        rid = cmd.send_req_command(args.target_fist, content)
        if rid > 0:
            rsp = cmd.get_rsp(rid, args.wait_time)
            print('[rsp]', rsp)
        else:
            print('[error] failed to request from master')
        cmd.stop()
        cmd.join()

    def env(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('action', choices=['init', 'ls', 'register'], help='actions to take')
        parser.add_argument('--env_name', help='name of the current environment')
        parser.add_argument('--private_ip', help='private ip for current env')
        parser.add_argument('--public_ip', help='public ip for current env')
        parser.add_argument('--init', action='store_true')
        parser.add_argument('--docker_container', action='store_true', help='get public/private ip from env vars HOSTNAME')
        args = parser.parse_args(sys.argv[2:])

        from linker.structs import EnvInfo
        from .gun_helpers import EnvHelper

        if args.action == 'ls':
            print('current env:', EnvHelper.get_env_name())
            return

        if args.docker_container:
            if any([a is not None for a in [args.private_ip, args.public_ip]]):
                parser.error('"--docker_container" will automatically set env info, no need to specify IPs')
            hostname = os.environ.get('HOSTNAME')
            if not hostname:
                parser.error('could not find "HOSTNAME" in current env variables')
            args.env_name = args.env_name or hostname   # use hostname as env_name if the later is not specified
            args.private_ip = args.public_ip = hostname

        if any([a is None for a in [args.env_name, args.private_ip, args.public_ip]]):
            parser.error('missing args (name){} (private){} (pubilc){}'.format(args.env_name, args.private_ip, args.public_ip))

        env_info = EnvInfo(env_name=args.env_name, private_ip=args.private_ip, public_ip=args.public_ip)

        if args.init or args.action == 'init':
            EnvHelper.set_current_env_name(env_info.env_name)

        if args.action == 'register':
            EnvHelper.register_env_info(env_info)

    def proxy(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('action', choices=['set', 'ls'], help='actions to take')
        parser.add_argument('--http_proxy', type=str, help='in the "protocal://host:port" format')
        args = parser.parse_args(sys.argv[2:])

        if args.action == 'set':
            if args.http_proxy is None:
                parser.error('missing arg --http_proxy')
            config = json.load(open(CONFIG_DEFAULT_PATH))
            config['http_proxy'] = args.http_proxy
            json.dump(config, open(CONFIG_DEFAULT_PATH, 'w+'))

        if args.action in ['ls', 'set']:
            config = json.load(open(CONFIG_DEFAULT_PATH))
            print('http_proxy:', config['http_proxy'])

    def inspect(self):
        from .gun_helpers import GunInspector
        parser = argparse.ArgumentParser()
        parser.add_argument('option', choices=GunInspector.get_options(), help='inspect options')
        parser.add_argument('-s', '--sort_by', type=str, help='sort data by a column')
        parser.add_argument('-g', '--group_by', type=str, help='group data by a column')
        parser.add_argument('-r', '--reverse', action='store_true', help='reverse sort results')
        args = parser.parse_args(sys.argv[2:])

        inspector = GunInspector()
        inspector.inspect(args.option, sort_by=args.sort_by, group_by=args.group_by, reverse=args.reverse)

    def ip(self):
        import requests
        try:
            ip = requests.get('http://ifconfig.me', timeout=(1, 3)).content.decode().strip()
            print('current public ip: ', ip)
        except requests.exceptions.ReadTimeout:
            print('failed to get public ip: Timeout!')
        except KeyboardInterrupt:
            print()

    def remote(self):
        from .helpers.websocket import DEFAULT_PORT

        parser = argparse.ArgumentParser()
        parser.add_argument('option', choices=['run', 'exec'])
        parser.add_argument('-s', '--service', choices=['dispatcher', 'executor'])
        parser.add_argument('-H', '--hostname', default='0.0.0.0', type=str)
        parser.add_argument('-p', '--port', default=DEFAULT_PORT, type=int)
        parser.add_argument('-c', '--command', type=str)
        parser.add_argument('-d', '--cwd', default='/shared/runtime/', type=str)
        args = parser.parse_args(sys.argv[2:])

        if args.option == 'run':

            if args.service == 'dispatcher':
                from .helpers.remote_exec import RemoteExecDispatcher
                dispatcher = RemoteExecDispatcher(args.hostname, args.port)
                dispatcher.run()
                dispatcher.join()

            elif args.service == 'executor':
                from .helpers.remote_exec import RemoteExecExecutor
                executor = RemoteExecExecutor(args.hostname, args.port)
                executor.run()
                executor.join()

            else:
                raise RuntimeError('please specify a service type with -s')

        elif args.option == 'exec':

            assert args.command, 'empty command'
            from .helpers.remote_exec import RemoteExecRequester
            requester = RemoteExecRequester(args.hostname, args.port)
            requester.run()
            output = requester.send_cmd(args.command, args.cwd)
            print('*' * 20 + 'output' + '*' * 20)
            print(output)
            requester.disconnect()
