"""A module that does stuff like parsing text commands and processing commands"""

import re
import shlex
import inspect

__version__ = "2.1.0"

_CVT_FLOAT_PTR = re.compile(r"^[-+]?(\d*[.])\d*$")
_CVT_INT_PTR = re.compile(r"^[-+]?\d+$")


class CmdBaseException(Exception):
    """base exception of this module"""

    def __init__(self, message, *args):
        self.message = message
        self.args = args
        super().__init__(self.message)

    def __str__(self):
        return self.message


class ParsingError(Exception):
    """raised when parsing error..."""


class ProcessError(Exception):
    """raised when error occurred during processing commands without error handler"""

    def __init__(self, message, exception):
        self.message = message
        self.exception = exception
        super().__init__(self.message)


class MissingRequiredArgument(CmdBaseException):
    """raised when command's positional argument is missing"""

    def __init__(self, message, param):
        self.message = message
        self.param = param
        super().__init__(self.message)


class Cmd:
    """main class for parsing commands"""

    def __init__(self, command_string, prefix="/", max_args=0, convert_args=False):
        self.parsed_command = None
        self.name = None
        self.args = []
        self.args_count = len(self.args)
        self.command_string = command_string
        self.convert_args = convert_args
        self.prefix = prefix
        self.max_args = max_args

        # parse command
        res = re.match(rf"^{self.prefix}(?P<args>.*)", self.command_string)
        argres = []
        if res is not None:
            argres = shlex.split("".join(res.group("args")))
        argsc = len(argres)

        if self.max_args == 0:
            self.max_args = argsc

        if argsc > self.max_args:
            raise ParsingError(f"arguments exceeds max arguments: ({self.max_args})")

        for i in range(len(argres), self.max_args):  # insert empty arguments
            argres.insert(i, "")

        if argres:
            self.parsed_command = {
                "name": argres[0],
                "args": argres[1:],
                "args_count": argsc,
            }

            if convert_args:
                self._cvt_cmd()

            self.name = self.parsed_command["name"]
            self.args = self.parsed_command["args"]
            self.args_count = self.parsed_command["args_count"]

    def get_dict(self):
        """return parsed command"""
        return self.parsed_command

    def _get_args_type_char(self, max_args=0):
        """get command arguments data types in char format"""
        argtype = list()

        if max_args == 0:
            for arg in self.parsed_command["args"][
                0 : self.parsed_command["args_count"]
            ]:
                if not arg:
                    continue

                argtype.append(type(arg).__name__[0])  # get type char
        else:
            for arg in self.parsed_command["args"][0:max_args]:
                if not arg:
                    continue

                argtype.append(type(arg).__name__[0])  # get type char

        return argtype

    def _cvt_cmd(self):
        """evaluate literal arguments"""
        cvt = [(_CVT_FLOAT_PTR, float), (_CVT_INT_PTR, int)]

        for i in range(len(self.parsed_command["args"])):
            if not self.parsed_command["args"][i]:
                break  # empty args

            for cvt_ in cvt:
                res = cvt_[0].match(self.parsed_command["args"][i])

                if res:
                    self.parsed_command["args"][i] = cvt_[1](
                        self.parsed_command["args"][i]
                    )
                    break  # has found the correct data type

    def match_args(self, format_match, max_args=0):
        """match argument formats, only works with converted arguments"""

        # format example: 'ssf', arguments: ['hell','o',10.0] matched

        if max_args <= 0 and self.max_args > -1:
            max_args = self.max_args

        if not format_match:
            raise ValueError("no format specified")

        format_match = format_match.replace(" ", "")
        format_match = list(format_match)

        argtype = self._get_args_type_char(max_args)

        if len(format_match) != len(argtype):
            raise ValueError("format length is not the same as the arguments length")

        return self._match_args(argtype, format_match)

    def _match_args(self, argtype, format_match):
        """match arguments by arguments data types"""
        matched = 0
        for i, arg_type in enumerate(argtype):
            arg_len = len(str(self.parsed_command["args"][i]))
            if arg_type in ("i", "f"):
                if format_match[i] == "s":
                    matched += 1  # allow int or float as 's' format
                elif format_match[i] == "c" and arg_len == 1 and arg_type == "i":
                    matched += 1  # and char if only a digit for int
                elif arg_type == format_match[i]:
                    matched += 1
            elif arg_type == "s":
                if format_match[i] == "c" and arg_len == 1:
                    matched += 1
                elif arg_type == format_match[i]:
                    matched += 1

        if matched == len(format_match):
            return True

        return False

    def process_cmd(self, callback, error_handler_callback=None, attrs=None):
        """process command..."""
        if attrs is None:
            attrs = {}

        if type(callback).__name__ != "function":
            raise TypeError("callback is not a function")
        if (
            error_handler_callback
            and type(error_handler_callback).__name__ != "function"
        ):
            raise TypeError("error handler callback is not a function")

        if not isinstance(attrs, dict):
            raise TypeError("attributes must be in dict object")

        for attr in attrs:
            setattr(callback, attr, attrs[attr])

        if error_handler_callback is not None:
            for attr in attrs:
                setattr(error_handler_callback, attr, attrs[attr])

        ret = None
        try:
            cargspec = inspect.getfullargspec(callback)
            cparams = cargspec.args
            cdefaults = cargspec.defaults

            if cdefaults is None:
                if len(self.parsed_command["args"]) < len(cparams):
                    raise MissingRequiredArgument(
                        "missing required argument: "
                        + cparams[len(self.parsed_command["args"])],
                        param=cparams[len(self.parsed_command["args"])],
                    )

            else:

                posargs_length = len(cparams) - len(cdefaults)

                if len(self.parsed_command["args"]) < posargs_length:
                    raise MissingRequiredArgument(
                        "missing required argument: "
                        + cparams[len(self.parsed_command["args"])],
                        param=cparams[len(self.parsed_command["args"])],
                    )

                if (len(self.parsed_command) - posargs_length) < len(cdefaults):
                    for darg in cdefaults:
                        self.parsed_command["args_count"] += 1
                        self.parsed_command["args"].insert(
                            self.parsed_command["args_count"], darg
                        )

            if cargspec.varargs is None:
                ret = callback(*self.parsed_command["args"][: len(cparams)])
            else:
                ret = callback(
                    *self.parsed_command["args"][: self.parsed_command["args_count"]]
                )

        except Exception as exception:
            if error_handler_callback is None:
                raise ProcessError(
                    "an error occurred during processing callback '"
                    + f"{callback.__name__}()' for command '{self.parsed_command['name']}, "
                    + "no error handler callback specified, exception: ",
                    exception,
                ) from exception

            error_handler_callback(error=exception)

        for attr in attrs:
            delattr(callback, attr)

        if error_handler_callback is not None:
            for attr in attrs:
                delattr(error_handler_callback, attr)

        return ret

    def __str__(self):
        message = (
            "<"
            + f'Raw: "{self.command_string}", '
            + f'Name: "{self.name}", '
            + f"Args: {self.args[0:self.args_count]}>"
        )

        return message

    async def aio_process_cmd(self, callback, error_handler_callback=None, attrs=None):
        """coroutine process cmd"""
        if attrs is None:
            attrs = {}

        if type(callback).__name__ != "function":
            raise TypeError("callback is not a function")
        if (
            error_handler_callback
            and type(error_handler_callback).__name__ != "function"
        ):
            raise TypeError("error handler callback is not a function")

        if not isinstance(attrs, dict):
            raise TypeError("attributes must be in dict object")

        for attr in attrs:
            setattr(callback, attr, attrs[attr])

        if error_handler_callback is not None:
            for attr in attrs:
                setattr(error_handler_callback, attr, attrs[attr])

        ret = None
        try:
            cargspec = inspect.getfullargspec(callback)
            cparams = cargspec.args
            cdefaults = cargspec.defaults

            if cdefaults is None:
                if len(self.parsed_command["args"]) < len(cparams):
                    raise MissingRequiredArgument(
                        "missing required argument: "
                        + cparams[len(self.parsed_command["args"])],
                        param=cparams[len(self.parsed_command["args"])],
                    )

            else:

                posargs_length = len(cparams) - len(cdefaults)

                if len(self.parsed_command["args"]) < posargs_length:
                    raise MissingRequiredArgument(
                        "missing required argument: "
                        + cparams[len(self.parsed_command["args"])],
                        param=cparams[len(self.parsed_command["args"])],
                    )

                if (len(self.parsed_command) - posargs_length) < len(cdefaults):
                    for darg in cdefaults:
                        self.parsed_command["args_count"] += 1
                        self.parsed_command["args"].insert(
                            self.parsed_command["args_count"], darg
                        )

            if cargspec.varargs is None:
                ret = await callback(*self.parsed_command["args"][: len(cparams)])
            else:
                ret = await callback(
                    *self.parsed_command["args"][: self.parsed_command["args_count"]]
                )

        except Exception as exception:
            if error_handler_callback is None:
                raise ProcessError(
                    "an error occurred during processing callback '"
                    + f"{callback.__name__}()' for command '{self.parsed_command['name']}, "
                    + "no error handler callback specified, exception: ",
                    exception,
                ) from exception

            await error_handler_callback(error=exception)

        for attr in attrs:
            delattr(callback, attr)

        if error_handler_callback is not None:
            for attr in attrs:
                delattr(error_handler_callback, attr)

        return ret
