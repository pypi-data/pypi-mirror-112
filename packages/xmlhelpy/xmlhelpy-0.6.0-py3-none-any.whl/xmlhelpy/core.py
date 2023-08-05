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
from inspect import isclass

import click
from lxml import etree

from .types import Bool


class Group(click.Group):
    """Group wrapper class that uses the custom decorators."""

    def __init__(self, *args, version, **kwargs):
        super().__init__(*args, **kwargs)
        # Backreference to a potential parent group.
        self.parent = None
        self.version = version

    def group(self, *args, **kwargs):
        """Shortcut decorator for subgroups."""
        from .decorators import group

        def decorator(func):
            cmd = group(*args, **kwargs)(func)
            self.add_command(cmd)
            return cmd

        return decorator

    def command(self, *args, **kwargs):
        """Shortcut decorator for commands."""
        from .decorators import command

        def decorator(func):
            cmd = command(*args, **kwargs)(func)
            self.add_command(cmd)
            return cmd

        return decorator

    def environment(self, *args, **kwargs):
        """Shortcut decorator for environments."""
        from .decorators import environment

        def decorator(func):
            env = environment(*args, **kwargs)(func)
            self.add_command(env)
            return env

        return decorator

    def add_command(self, cmd, name=None):
        cmd.parent = self

        # Inherit the group's version.
        if cmd.version is None:
            cmd.version = self.version

        super().add_command(cmd, name=name)


class Command(click.Command):
    """Command wrapper class with additional arguments."""

    def __init__(self, *args, description, example, version, **kwargs):
        super().__init__(*args, **kwargs)
        # Backreference to a potential parent group.
        self.parent = None
        self.description = description

        if self.description is None:
            self.description = self.help.split("\n")[0] if self.help else ""

        self.example = example
        self.version = version

    def format_help(self, ctx, formatter):
        self.format_usage(ctx, formatter)

        if self.example:
            formatter.write_text(f"Example: {ctx.command_path} {self.example}")

        self.format_help_text(ctx, formatter)
        self.format_options(ctx, formatter)
        self.format_epilog(ctx, formatter)

    def to_xml(self):
        """Convert the command to an XML tag."""
        program_elem = etree.Element("program")

        name = self.name
        parent = self.parent

        while parent is not None:
            name = f"{parent.name} {name}"
            parent = parent.parent

        program_elem.set("name", name)
        program_elem.set("description", self.description)

        if self.example:
            program_elem.set("example", f"{name} {self.example}")

        if self.version is not None:
            program_elem.set("version", self.version)

        return program_elem


class Environment(Command):
    """Command wrapper class for environments."""

    def to_xml(self):
        """Convert the environment to an XML tag."""
        env_elem = super().to_xml()
        env_elem.tag = "env"

        return env_elem


class ParameterMixin:
    """Mixin that each parameter should inherit from."""

    def __init__(self, *args, description, param_type, **kwargs):
        if isclass(param_type):
            param_type = param_type()

        super().__init__(*args, **kwargs, type=param_type)
        self.description = description
        self.param_type = param_type

    def to_xml(self, *args):
        """Convert the parameter to an empty XML tag."""
        param_elem = etree.Element("param")

        param_elem.set("description", self.description)
        param_elem.attrib.update(self.param_type.xml_attrs)

        return param_elem


class Argument(ParameterMixin, click.Argument):
    """Argument wrapper class with additional arguments."""

    def to_xml(self, index, *args):
        """Convert the argument to an XML tag.

        The tag will include the attributes corresponding to this argument.
        """
        # pylint: disable=arguments-differ
        param_elem = super().to_xml()
        param_elem.set("name", f"arg{index}")

        if self.required:
            param_elem.set("required", "true")

        if self.default:
            param_elem.set("default", self.param_type.to_string(self.default))

        if self.nargs != 1:
            param_elem.set("nargs", str(self.nargs))

        return param_elem


class Option(ParameterMixin, click.Option):
    """Option wrapper class with additional arguments."""

    def __init__(self, *args, is_flag, default, char, param_type, **kwargs):
        if is_flag:
            default = False
            param_type = Bool

        super().__init__(
            *args, is_flag=is_flag, default=default, param_type=param_type, **kwargs
        )
        self.char = char

    def to_xml(self, *args):
        """Convert the option to an XML tag.

        The tag will include the attributes corresponding to this option.
        """
        param_elem = super().to_xml()
        param_elem.set("name", self.name)

        if self.char is not None:
            param_elem.set("char", self.char)

        if self.is_flag:
            param_elem.set("type", "flag")

        if self.required:
            param_elem.set("required", "true")

        if self.default is not None:
            param_elem.set("default", self.param_type.to_string(self.default))

        if self.nargs != 1:
            param_elem.set("nargs", str(self.nargs))

        return param_elem

    def get_default(self, ctx):
        """Get the default value of this option.

        If the parameter is a flag, i.e. ``is_flag`` is ``True``, then the default value
        for flags will be returned.
        """
        if self.is_flag:
            return self.default

        return super().get_default(ctx)
