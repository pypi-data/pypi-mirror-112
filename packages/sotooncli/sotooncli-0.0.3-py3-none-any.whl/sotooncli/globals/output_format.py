import json

import click
import yaml
from tabulate import tabulate

from sotooncli.param import SotoonParams

JSON_INDENT = 4

LIST_RESPONSE_TYPE = "list"
SINGLE_RESPONSE_TYPE = "single"

RESPONSE_DATA = {LIST_RESPONSE_TYPE: "items", SINGLE_RESPONSE_TYPE: "item"}

RAW_JSON_OUTPUT_FORMAT = "json-raw"
FORMATTED_JSON_OUTPUT_FORMAT = "json"
TABULAR_OUTPUT_FORMAT = "table"
YAML_OUTPUT_FORMAT = 'yaml'

output_types = [FORMATTED_JSON_OUTPUT_FORMAT, RAW_JSON_OUTPUT_FORMAT, TABULAR_OUTPUT_FORMAT, YAML_OUTPUT_FORMAT]


class OutputFormatOption(click.Option, SotoonParams):
    def __init__(self, default=output_types[0]):
        type_ = click.Choice(output_types)
        click.Option.__init__(self, ['-o', '--output'], show_default=True, type=type_)
        SotoonParams.__init__(self, name="output", placeholder="OUTPUT", is_required=False,
                              description=f"Output format. One of {output_types}.",
                              default_value=default)


def get_formatter(output_format):
    if output_format == RAW_JSON_OUTPUT_FORMAT:
        return JSONFormatter()
    elif output_format == TABULAR_OUTPUT_FORMAT:
        return TableFormatter()
    elif output_format == FORMATTED_JSON_OUTPUT_FORMAT:
        return PrettyJSONFormatter()
    elif output_format == YAML_OUTPUT_FORMAT:
        return YamlFormatter()
    else:
        raise click.BadParameter("Unknown output format")


class OutputFormatter:
    def format(self, data):
        pass

    def _get_data_key(self):
        if self.response_type in RESPONSE_DATA:
            return RESPONSE_DATA[self.response_type]
        else:
            raise click.ClickException("Invalid response type")

    def _get_data(self, data):
        self.response_type = data["type"]
        if not self.response_type:
            return
        self.data = data[self._get_data_key()]


class JSONFormatter(OutputFormatter):
    def format(self, data):
        self._get_data(data)
        return self.data


class PrettyJSONFormatter(OutputFormatter):
    def format(self, data):
        self._get_data(data)
        return json.dumps(self.data, indent=JSON_INDENT, sort_keys=True)


class TableFormatter(OutputFormatter):
    def format(self, data):
        self._get_data(data)
        try:
            return tabulate(self.data, headers="keys", tablefmt="pretty")
        except TypeError:
            return tabulate([self.data], headers="keys", tablefmt="pretty")


class YamlFormatter(OutputFormatter):
    def format(self, data):
        self._get_data(data)
        data_ = yaml.dump(self.data, default_flow_style=False)
        return data_
