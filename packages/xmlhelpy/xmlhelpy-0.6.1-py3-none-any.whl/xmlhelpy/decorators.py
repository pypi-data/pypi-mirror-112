# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import keyword
import string

import click

from .core import Argument
from .core import Command
from .core import Environment
from .core import Group
from .core import Option
from .formatting import print_commands
from .formatting import print_version
from .formatting import print_xmlhelp
from .types import String


def _duplicate_param(func, msg):
    function_name = (
        f"{func.__module__}.{func.__name__}"
        if func.__module__ is not None
        else func.__name__
    )
    raise Exception(f"{function_name}: {msg}")


def _check_name(func, name):
    if not hasattr(func, "__param_names__"):
        func.__param_names__ = set()

    if name in func.__param_names__:
        _duplicate_param(func, f"Name '{name}' specified twice.")

    func.__param_names__.add(name)


def _check_char(func, name, char):
    if char is not None:
        if not hasattr(func, "__param_chars__"):
            func.__param_chars__ = set()

        if char in func.__param_chars__:
            _duplicate_param(func, f"Char '{char}' specified twice.")

        func.__param_chars__.add(char)


def group(name=None, version=None, cls=Group):
    """Decorator to register a new command group.

    Group names will be listed before the actual command name in the generated xmlhelp.

    :param name: (optional) The name of the group. Defaults to the name of the decorated
        function with underscores replaced by dashes.
    :param version: (optional) The version of the group as string. This version will be
        inherited by all commands and subgroups of this group that do not explicitely
        specify their own version.
    :param cls: (optional) The class to use for the command group.
    """

    def decorator(func):
        _check_name(func, "commands")

        click.option(
            "--commands",
            help="Print a list of all commands this group contains and exit.",
            is_flag=True,
            is_eager=True,
            expose_value=False,
            callback=print_commands,
        )(func)

        _check_name(func, "version")

        click.option(
            "--version",
            help="Print the version of this group and exit.",
            is_flag=True,
            is_eager=True,
            expose_value=False,
            callback=print_version,
        )(func)

        return click.group(cls=cls, name=name, version=version)(func)

    return decorator


def command(name=None, description=None, example=None, version=None, cls=Command):
    """Decorator to register a new command or underlying tool.

    :param name: (optional) The name of the command. Defaults to the name of the
        decorated function with underscores replaced by dashes.
    :param description: (optional) The description of the command to be shown in the
        xmlhelp. Defaults to the first line of the docstring of the decorated function.
    :param example: (optional) An example of using the command.
    :param version: (optional) The version of the command as string.
    :param cls: (optional) The class to use for the command.
    """

    def decorator(func):
        _check_name(func, "xmlhelp")

        click.option(
            "--xmlhelp",
            help="Print the XML help and exit.",
            is_flag=True,
            is_eager=True,
            expose_value=False,
            callback=print_xmlhelp,
        )(func)

        _check_name(func, "version")

        click.option(
            "--version",
            help="Print the version of this command and exit.",
            is_flag=True,
            is_eager=True,
            expose_value=False,
            callback=print_version,
        )(func)

        if hasattr(func, "__param_names__"):
            del func.__param_names__
        if hasattr(func, "__param_chars__"):
            del func.__param_chars__

        cmd = click.command(
            cls=cls,
            name=name,
            version=version,
            example=example,
            description=description,
        )(func)

        return cmd

    return decorator


def environment(
    name=None, description=None, example=None, version=None, cls=Environment
):
    """Decorator to register a new environment.

    Environments are almost identical to regular commands. They automatically include
    the ``--env-exec`` option and use the ``env`` tag for the root element in the
    xmlhelp.

    :param name: (optional) The name of the environment. Defaults to the name of the
        decorated function with underscores replaced by dashes.
    :param description: (optional) The description of the environment to be shown in the
        xmlhelp. Defaults to the first line of the docstring of the decorated function.
    :param example: (optional) An example of using the environment.
    :param version: (optional) The version of the environment as string.
    :param cls: (optional) The class to use for the environment.
    """

    def decorator(func):
        _check_name(func, "env-exec")

        click.option(
            "--env-exec",
            help="Command string to be executed inside the environment.",
            multiple=True,
        )(func)

        env = command(
            cls=cls,
            name=name,
            version=version,
            example=example,
            description=description,
        )(func)

        return env

    return decorator


def argument(
    name, description="", nargs=1, param_type=String, required=True, default=None
):
    """Decorator to add an argument parameter to a command.

    Arguments are positional parameters with less possibilities than options that are
    also required by default.

    :param name: The name of the argument.
    :param description: (optional) The description of the argument.
    :param nargs: (optional) The number of arguments (separated by spaces) to expect.
        ``-1`` can be specified for a single argument to allow for an unlimited number
        of arguments.
    :param param_type: (optional) The type of the argument parameter, either as class or
        instance. See :mod:`xmlhelpy.types` for the possible parameter types.
    :param required: (optional) Flag indicating wether the argument is required or not.
    :param default: (optional) The default value to take if the argument is not given.
    """

    def decorator(func):
        _check_name(func, name)

        click.argument(
            name,
            cls=Argument,
            description=description,
            nargs=nargs,
            param_type=param_type,
            required=required,
            default=default,
        )(func)

        return func

    return decorator


def option(
    name,
    description="",
    nargs=1,
    param_type=String,
    required=False,
    default=None,
    char=None,
    var_name=None,
    is_flag=False,
):
    """Decorator to add an option parameter to a command.

    Options are non-positional parameters or flags.

    :param name: The full name of the option, which has to be given as
        ``--<name> <value>`` when invoking the command.
    :param description: (optional) The description of the option.
    :param nargs: (optional) The number of arguments (separated by spaces) to expect.
    :param param_type: (optional) The type of the option parameter, either as class or
        instance. See :mod:`xmlhelpy.types` for the possible parameter types.
    :param required: (optional) Flag indicating wether the option is required or not.
    :param default: (optional) The default value to take if the option is not given.
    :param char: (optional) A shorthand for an option consisting of a single ASCII
        letter, which has to be given as ``-<char> <value>`` when invoking the command.
    :param var_name: (optional) The name of the variable that will be passed into the
        executing function. Defaults to the name in lowercase, with dashes replaced by
        underscores.
    :param is_flag: (optional) Flag indicating wether the option is a flag. Flags are
        special options that do not require a value. They always use :class:`.Bool` as
        type and always use ``False`` as default value.
    """

    def decorator(func):
        # It is best to deal with the parameter names here already before passing them
        # to the original option decorator.
        if "/" in name:
            raise click.BadOptionUsage(name, "Name cannot contain slashes.")

        if char is not None and char not in string.ascii_letters:
            raise click.BadOptionUsage(name, "Invalid char value.")

        if var_name is not None and (
            keyword.iskeyword(var_name) or not var_name.isidentifier()
        ):
            raise click.BadOptionUsage(name, "Invalid variable name.")

        _check_name(func, name)
        _check_char(func, name, char)

        param_decls = ["--" + name]

        if char is not None:
            param_decls.append("-" + char)

        if var_name is not None:
            param_decls.append(var_name)

        click.option(
            *param_decls,
            cls=Option,
            description=description,
            nargs=nargs,
            param_type=param_type,
            required=required,
            default=default,
            char=char,
            is_flag=is_flag,
            show_default=True,
        )(func)

        return func

    return decorator
