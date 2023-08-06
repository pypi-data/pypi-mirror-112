import click

from sotooncli import requests
from sotooncli.globals.config import ConfigOption
from sotooncli.globals.options import get_params_from_file_option
from sotooncli.globals.output_format import OutputFormatOption, get_formatter
from sotooncli.param import SotoonArgument, SotoonParams
from sotooncli.state import State

output_format_opt = OutputFormatOption()
global_options = [ConfigOption(), get_params_from_file_option(), output_format_opt]


class SotoonCommand:
    def __init__(self, description, args, opts, parent=None):
        self.parent_opts = []
        self.parent_args = []
        if parent:
            self.parent_opts = parent.get_all_opts()
            self.parent_args = parent.get_args()
        self.args = args
        self.opts = opts

        self.help = description
        if args:
            self.help += f'\b\bArguments:'
            for arg in args:
                self.help += f'\n\n{arg.metavar}\t{arg.description}'

    def get_cli_params(self):
        return self.args + self.get_all_opts() + global_options

    def get_branch_params(self):
        return self.args + self.get_all_opts() + self.parent_args

    def get_all_opts(self):
        return self.opts + self.parent_opts

    def get_args(self):
        return self.args


class GroupCommand(click.Group, SotoonCommand):
    def __init__(self, name, description, capsule, args, opts, parent=None):
        SotoonCommand.__init__(self, description, args, opts, parent)
        params = self.get_cli_params()
        click.Group.__init__(self, name=name, params=params, short_help=capsule,
                             help=self.help)


class ExecutableCommand(click.Command, SotoonCommand):
    def __init__(self, name, description, capsule, args, opts, parent):
        SotoonCommand.__init__(self, description, args, opts, parent)
        params = self.get_cli_params()
        click.Command.__init__(self, params=params, callback=self.callback, name=name, short_help=capsule,
                               help=self.help)

    def get_cli_params(self):
        return self.args + self.get_all_opts() + global_options

    def callback(self, *args, **kwargs):
        ctx = click.get_current_context()
        path = ctx.command_path.split(' ')[1:]
        state = ctx.find_object(State)
        params = self._merge(state, ctx)
        # mocked execute in tests
        result = requests.execute(path, params)
        self._output(result, state, ctx)

    def _merge(self, state, ctx):
        merged = dict()
        for p in self.get_branch_params():
            if isinstance(p, SotoonParams):
                value = p.get_value(state, ctx)
                if p.is_required and value is None:
                    if isinstance(p, SotoonArgument):
                        cls = "Argument"
                    else:
                        cls = "Option"
                    raise click.BadParameter(f"{cls} {p.name} is required")
                merged[p.name] = value
            else:
                raise click.ClickException(f"Internal Error, type:{type(p)}")
        return merged

    @staticmethod
    def _output(data, state, ctx):
        output_format = output_format_opt.get_value(state, ctx)
        formatter = get_formatter(output_format)
        click.echo(formatter.format(data))
