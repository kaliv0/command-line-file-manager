import ast

import click

from file_manager.logs import log_messages


class LiteralOption(click.Option):

    def type_cast_value(self, ctx, value):
        try:
            return ast.literal_eval(value)
        except:
            raise click.BadParameter(log_messages.BAD_LITERAL.format(value=value))