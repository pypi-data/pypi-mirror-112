"""Command line script for J3."""
import glob
import importlib

from uvicorn.supervisors.multiprocess import Multiprocess
from j3.reloader import ChangeReloader
import logging
import os
import sys
from argparse import ArgumentParser, Namespace, RawTextHelpFormatter
from inspect import getmembers
from pathlib import Path
from textwrap import dedent
from typing import Any, Optional, Sequence, cast

import jinja2
import uvicorn
from pkg_resources import resource_string
from sqlalchemy.sql.schema import MetaData
from starlette.routing import BaseRoute
from uvicorn.config import Config
from uvicorn.server import Server

from j3.config import J3Config
from j3.core import AbstractJ3, J3Error, J3InitError
from j3.event import MessageHandlerMap
from j3.logging import get_logger
from j3.utils import Fore, Style, bold, cwd, fg, scan_resource_dir

YELLOW, CYAN, RED, GREEN, WHITE = (
    Fore.YELLOW,
    Fore.CYAN,
    Fore.RED,
    Fore.GREEN,
    Fore.WHITE,
)
WHITE_EX, CYAN_EX = Fore.LIGHTWHITE_EX, Fore.LIGHTCYAN_EX
BRIGHT, RESET_ALL = Style.BRIGHT, Style.RESET_ALL

TEMPLATE_DIR = "templates/app"


logger = get_logger("j3.command")


class J3Command:
    def __init__(self):
        """Constructor.

        작업 순서:
            1. `<pkg_name>/config.py` 위치를 찾기 위해 앱 name 을 구한다.
            2. <pkg_name> 은 암시적으로는 현재 경로의 이름인데, `setup.cfg` 파일에
               `[j3]` 섹션에도 지정 가능하다.
            3. config 파일을 로드해서 나머지 정보를 읽는다.
        """
        self.path = Path(os.path.abspath("."))
        self.msa = cast(J3Config, J3Config.load_from_config(self.path))
        config_module_name = f"{self.msa.module_name}.config"
        self.config_module = importlib.import_module(config_module_name)

    def print_warn(self, msg: str):
        print(f"{bold('J3 WARNING:', YELLOW)} {msg}")

    def is_init(self):
        """이미 초기화된 프트젝트인지 확인합니다.

        체크 방법:`
            현재 디렉토리가 비어 있지 않은 경우 초기화된 프로젝트로 판단합니다.
        """
        return any(self.path.iterdir())

    def config(self, ns: Namespace):
        """
        앱에서 오버라이드된 config.xxx 를 실행한다.
        """
        config_banner = "J3 Configuration"
        config_module_doc = self.config_module.__doc__.strip(".\n\t ")
        module = importlib.import_module(self.msa.module_name + ".config." + ns.config)
        if config_module_doc:
            module_doc = " : " + bold(module.__doc__, CYAN) if module.__doc__ else ""
            config_banner = f"⚙️  {bold(config_module_doc, YELLOW)}{module_doc}"
        self.banner(config_banner)
        getattr(module, "run")(self.msa)

    def init(self, force=False):
        """J3 앱 프로젝트 디렉토리를 권장 구조로 초기화 합니다."""
        if self.is_init():
            if force:
                self.print_warn(f"*{bold('force')}* initializing project...")
            else:
                raise J3InitError(f"project already initialized at: {self.path}")

        with cwd(self.path):
            res_names = scan_resource_dir(TEMPLATE_DIR)

            assert res_names

            for res_name in res_names:
                res_name.startswith("templates/app/app/")
                res_name2 = res_name.replace(
                    "templates/app/app/", f"templates/app/{self.msa.name}/"
                )
                # XXX: Temporary fix
                if "__pycache__" in res_name:
                    continue
                rel_path = res_name2.replace(TEMPLATE_DIR + "/", "")
                target_path = self.path / rel_path
                target_path.parent.mkdir(parents=True, exist_ok=True)
                text = resource_string("j3", res_name)
                text = text.decode()

                if target_path.name.endswith(".j2"):  # Jinja2 template
                    target_path = target_path.parent / target_path.name[:-3]
                    template = jinja2.Template(text)
                    text = template.render(msa=self.msa)

                target_path.write_text(text, encoding="utf8")

            # if self._name:
            #    (self.path / "app").rename(self._name)

    def init_app(self, init_routes=True):
        """J3 앱을 초기화 합니다."""
        logger.info(bold("Load config and initialize app..."))
        bullet = bold("✓" if os.name != "nt" else "v", GREEN)
        num_domains = len(self.load_domain())

        num_domains and logger.info(
            f"{bullet} init {fg('domain models', CYAN)}... %s",
            bold(f"{num_domains}", YELLOW) + " models loaded.",
        )

        num_tables = len(self.load_orm_mappers().tables)
        num_tables and logger.info(
            f"{bullet} init {fg('ORM mappings', CYAN)}.... %s",
            bold(f"{num_tables}", YELLOW) + " tables mapped.",
        )

        if init_routes:
            num_routes = len(self.load_routes())
            num_routes and logger.info(
                f"{bullet} init {fg('API endpoints', CYAN)}... %s",
                bold(f"{num_routes}", YELLOW) + " routes installed.",
            )

            self.msa.init_fastapi()

        msg_handlers = self.load_msg_handlers()
        num_handlers = len(msg_handlers)
        num_handlers and logger.info(
            f"{bullet} init {fg('event handlers', CYAN)}.. %s handlers mounted.",
            bold(f"{num_handlers}", YELLOW),
        )

        db_url = self.msa.get_db_url()
        db_url and logger.info(
            f"{bullet} init {fg('database', CYAN)}........ %s",
            bold(f"{db_url}", YELLOW),
        )

        return self.msa

    def banner(self, msg, icon=""):
        """프로젝트 배너를 표시합니다."""
        if os.name == "nt":
            icon = ""
        term_width = os.get_terminal_size().columns
        banner_width = min(75, term_width)
        print("─" * banner_width)
        print(f"{icon} {msg}")
        print("─" * banner_width)

    def info(self):
        """J3 앱 정보를 출력합니다."""
        dot = bold("-", YELLOW)
        self.banner(f"{bold('J3 App Information')}", icon="💡")
        print(dot, fg("Name", CYAN), "  :", fg(self.msa.name, WHITE_EX))
        print(dot, fg("Title", CYAN), " :", fg(self.msa.title, WHITE_EX))
        print(dot, fg("Module", CYAN), ":", fg(self.msa.module_name, WHITE_EX))
        print(dot, fg("Path", CYAN), "  :", fg(self.path, WHITE_EX))

    def run(
        self,
        app_name: Optional[str] = None,
        dry_run=False,
        reload=True,
        banner=True,
        **kwargs,
    ):
        """J3 애플리케이션을 실행합니다."""
        if banner:
            msg = "".join(
                [
                    bold("Launching J3: ", CYAN),
                    bold(self.msa.title, WHITE),
                ]
            )
            self.banner(msg, icon="🚀")

        if not app_name:
            app_name = f"{self.msa.module_name}.__main__:app"

        if not dry_run:
            sys.path.insert(0, str(self.path))
            if os.name == "nt":
                content = (uvicorn_init := Path(uvicorn.__file__)).read_text()
                if "colorama" not in content:
                    uvicorn_init.write_text(
                        content + "\nfrom colorama import init; init()"
                    )
            self._uvicon_run(app_name, reload=reload, port=self.msa.get_api_port())

    def _uvicon_run(self, app, **kwargs) -> None:
        config = Config(app, **kwargs)
        server = Server(config=config)

        if (config.reload or config.workers > 1) and not isinstance(app, str):
            logger = logging.getLogger("uvicorn.error")
            logger.warning(
                "You must pass the application as an import string to enable 'reload' or "
                "'workers'."
            )
            sys.exit(1)

        if config.should_reload:
            sock = config.bind_socket()
            ChangeReloader(config, target=server.run, sockets=[sock]).run()
        elif config.workers > 1:
            sock = config.bind_socket()
            Multiprocess(config, target=server.run, sockets=[sock]).run()
        else:
            server.run()

    def load_domain(self) -> list[type]:
        """도메인 클래스를 로드합니다.

        ./<package_dir>/domain/**/*.py 파일을 읽어서 클래스 타입 리스트를 리턴합니다.
        """
        domains = list[type]()

        for fname in glob.glob("./" + str(self.msa.module_path) + "/domain/*.py"):
            if Path(fname).name.startswith("_"):
                continue
            module_name = fname[2:-3].replace("/", ".").replace("\\", ".")
            module = importlib.import_module(module_name)

            members = getmembers(module)
            for name, member in members:
                if name.startswith("_"):
                    continue
                if type(member) != type:
                    continue
                if member.__module__ != module_name:
                    continue
                domains.append(member)

        return domains

    def load_orm_mappers(self) -> MetaData:
        fastmsa_orm = importlib.import_module("j3.orm")
        metadata = MetaData()
        setattr(fastmsa_orm, "metadata", metadata)

        mapper_file_path = self.msa.module_path / "adapters" / "orm.py"
        mapper_paths = list[Path]()

        if mapper_file_path.exists():
            mapper_paths = [mapper_file_path]
        else:
            mapper_paths = [
                Path(p) for p in glob.glob(f"{self.msa.module_path}/adapters/orm/*.py")
            ]

        mapper_paths = [p.relative_to(self.msa.module_path) for p in mapper_paths]

        for path in mapper_paths:
            if path.name.startswith("_"):
                continue
            mapper_modname = ".".join(
                [self.msa.module_name or self.msa.name] + list(path.parts)
            )[:-3]
            module = importlib.import_module(mapper_modname)
            # 모듈에 `init_mappers()` 함수가 있다면 호출합니다.
            init_mappers = getattr(module, "init_mappers", None)
            if init_mappers and callable(init_mappers):
                init_mappers(metadata)

        return metadata

    def load_routes(self) -> list[BaseRoute]:
        from j3.api import app

        modules = []

        for fname in glob.glob(f"./{self.msa.module_path}/routes/*.py"):
            if Path(fname).name.startswith("_"):
                continue
            module_name = fname[2:-3].replace("/", ".").replace("\\", ".")
            if sys.modules.get(module_name):
                continue
            module = importlib.import_module(module_name)
            modules.append(module)

        routes: list[Any] = app.routes
        return [
            r
            for r in routes
            if hasattr(r, 'endpoint') and r.endpoint.__module__.startswith(self.msa.module_name + ".routes")
        ]

    def load_msg_handlers(self, msa: Optional[AbstractJ3] = None) -> MessageHandlerMap:
        from j3.event import MESSAGE_HANDLERS, messagebus

        modules = []

        for fname in glob.glob(f"./{self.msa.module_path}/handlers/*.py"):
            if Path(fname).name.startswith("_"):
                continue
            module_name = fname[2:-3].replace("/", ".").replace("\\", ".")
            if sys.modules.get(module_name):
                continue
            module = importlib.import_module(module_name)
            modules.append(module)

        messagebus.msa = msa or self.msa  # Dependency Injection
        messagebus.uow = (msa and msa.uow) or self.msa.uow

        return MESSAGE_HANDLERS


class J3CommandParser:
    """콘솔 커맨드 명령어 파서.

    실제 작업은 `J3Command` 객체에 위임합니다.
    """

    def __init__(self):
        """기본 생성자."""
        self._cmd = J3Command()
        has_app_config = not self._cmd.msa.is_implicit_name
        app_title = bold("J3 Framework")

        if has_app_config:
            app_title = bold(self._cmd.msa.title, YELLOW)

        self.parser = ArgumentParser(
            "j3",
            description=f"✨ {app_title} : {fg('command line utility', CYAN_EX)}",
        )
        self._subparsers = self.parser.add_subparsers(dest="command")

        handlers = []

        if has_app_config:
            handlers += [
                self._cmd.config,
                self._cmd.run,
                self._cmd.info,
            ]
        else:
            handlers.append(self._cmd.init)

        # init subparsers
        for handler in handlers:
            command = handler.__name__
            # 핸들러 함수의 주석을 커맨드라인 도움말로 변환하기 위한 작업입니다.
            doc = None

            command_doc = None
            try:
                command_doc = importlib.import_module(
                    self._cmd.msa.module_name + "." + command
                ).__doc__
            except:
                pass

            if handler.__doc__:
                lines = handler.__doc__.splitlines()
                doc = command_doc or (lines[0] + "\n" + dedent("\n".join(lines[1:])))
            parser = self._subparsers.add_parser(
                command,
                description=bold(doc, YELLOW),
                formatter_class=RawTextHelpFormatter,
            )
            if command == "init":
                parser.add_argument(
                    "--force", action="store_true", help="무조건 프로젝트 구조 덮어쓰기"
                )
                parser.add_argument(
                    "--title",
                    action="store_const",
                    help="외부에 보여질 앱 제목",
                    const="",
                )
            if command == "run":
                parser.add_argument("app_name", metavar="app_name", nargs="?")

            if command == "config":
                # config 디렉토리가 있을 경우
                config_parsers = parser.add_subparsers(dest="config", required=True)
                config_path = self._cmd.msa.module_path / "config"
                if (config_path).is_dir():
                    for config_name in [
                        it.name.split(".")[0]
                        for it in config_path.iterdir()
                        if not it.name.startswith("_")
                    ]:
                        module_name = (
                            self._cmd.msa.module_name + ".config." + config_name
                        )
                        module_doc = None
                        try:
                            module_doc = importlib.import_module(module_name).__doc__
                        except:
                            pass
                        config_parsers.add_parser(
                            config_name,
                            formatter_class=RawTextHelpFormatter,
                            description=module_doc,
                        )

    def parse_args(self, args: Sequence[str]):
        """콘솔 명령어를 해석해서 적절한 작업을 수행합니다."""
        if not args:
            self.parser.print_help()
            return

        ns = self.parser.parse_args(args)
        try:
            if hasattr(self, ns.command):
                # 커맨드 명령어와 동일한 이름의 메소드가 파서 클래스에 있으면
                # 그 메소드를 호출해서 적당한 처리 후 실제 메소드를 호출합니다.
                getattr(self, ns.command)(ns)
            else:
                # 아닐 경우 J3Command 클래스에서 핸를러를 호출합니다.
                getattr(self._cmd, ns.command)()
        except J3Error as e:
            print(
                f"{bold('J3 ERROR:', RED)} {fg(e.message, YELLOW)}",
                file=sys.stderr,
            )

    def init(self, ns: Namespace):
        """`init` 명령어 처리."""
        self._cmd.init(force=ns.force)

    def run(self, ns: Namespace):
        """`run` 명령어 처리."""
        self._cmd.run(app_name=ns.app_name)

    def config(self, ns: Namespace):
        """`config` 명령어 처리."""
        self._cmd.config(ns)


def console_main():
    parser = J3CommandParser()
    parser.parse_args(sys.argv[1:])


if __name__ == "__main__":
    console_main()
