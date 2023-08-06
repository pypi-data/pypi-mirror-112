import re
import time

from cloudshell.cli.command_mode import CommandMode


class AristaDefaultCommandMode(CommandMode):
    PROMPT = r">\s*$"
    ENTER_COMMAND = ""
    EXIT_COMMAND = ""

    def __init__(self, resource_config, api):
        """Initialize Default command mode.

        only for cases when session started not in enable mode
        :param resource_config:
        """
        self.resource_config = resource_config
        self._api = api

        CommandMode.__init__(
            self,
            AristaDefaultCommandMode.PROMPT,
            AristaDefaultCommandMode.ENTER_COMMAND,
            AristaDefaultCommandMode.EXIT_COMMAND,
        )


class AristaEnableCommandMode(CommandMode):
    PROMPT = (
        r"((?<=\n)|(?<=^))"  # new line or begin of the line that don't saved in match
        r"((?!\(config.*?\))(\w|-|\(|\)))*"  # \w or - or () and without (config)
        r"#\s*$"
    )
    ENTER_COMMAND = "enable"
    EXIT_COMMAND = ""

    def __init__(self, resource_config, api):
        """Initialize Enable command mode - default command mode for Arista Shells.

        :param resource_config:
        """
        self.resource_config = resource_config
        self._api = api
        self._enable_password = None

        CommandMode.__init__(
            self,
            AristaEnableCommandMode.PROMPT,
            AristaEnableCommandMode.ENTER_COMMAND,
            AristaEnableCommandMode.EXIT_COMMAND,
            enter_action_map=self.enter_action_map(),
        )

    @property
    def enable_password(self):
        if not self._enable_password:
            password = self.resource_config.enable_password
            self._enable_password = self._api.DecryptPassword(password).Value
        return self._enable_password

    def enter_action_map(self):
        return {
            "[Pp]assword": lambda session, logger: session.send_line(
                self.enable_password, logger
            )
        }


class AristaConfigCommandMode(CommandMode):
    MAX_ENTER_CONFIG_MODE_RETRIES = 5
    ENTER_CONFIG_RETRY_TIMEOUT = 5
    PROMPT = r"\(config.*\)#\s*$"
    ENTER_COMMAND = "configure terminal"
    EXIT_COMMAND = "end"

    def __init__(self, resource_config, api):
        """Initialize Config command mode.

        :param resource_config:
        """
        self.resource_config = resource_config
        self._api = api

        CommandMode.__init__(
            self,
            AristaConfigCommandMode.PROMPT,
            AristaConfigCommandMode.ENTER_COMMAND,
            AristaConfigCommandMode.EXIT_COMMAND,
            enter_action_map=self.enter_action_map(),
        )

    def enter_action_map(self):
        return {
            r"{}.*$".format(AristaEnableCommandMode.PROMPT): self._check_config_mode
        }

    def _check_config_mode(self, session, logger):
        error_message = "Failed to enter config mode, please check logs, for details"
        conf_prompt = AristaConfigCommandMode.PROMPT
        enable_prompt = AristaEnableCommandMode.PROMPT

        retry = 0
        output = session.hardware_expect(
            "", "{0}|{1}".format(conf_prompt, enable_prompt), logger
        )
        while (
            not re.search(conf_prompt, output)
            and retry < self.MAX_ENTER_CONFIG_MODE_RETRIES
        ):
            time.sleep(self.ENTER_CONFIG_RETRY_TIMEOUT)
            output = session.hardware_expect(
                AristaConfigCommandMode.ENTER_COMMAND,
                "{0}|{1}".format(enable_prompt, conf_prompt),
                logger,
            )
            retry += 1

        if not re.search(conf_prompt, output):
            raise Exception(error_message)

        session.send_line("", logger)


class AristaVrfCommandMode(CommandMode):
    PROMPT = r"\(vrf:{}\)#\s*$"
    DEFAULT_VRF_NAME = "default"
    ENTER_COMMAND = "routing-context vrf {}"
    NEW_ENTER_COMMAND = "cli vrf {}"
    EXIT_COMMAND = ENTER_COMMAND.format(DEFAULT_VRF_NAME)
    NEW_EXIT_COMMAND = NEW_ENTER_COMMAND.format(DEFAULT_VRF_NAME)
    DEPRECATED_VRF_COMMAND_PATTERN = r"deprecated\s*by\s*\S*cli vrf"

    class _parent_mode(object):
        prompt = AristaEnableCommandMode.PROMPT

    def __init__(self, vrf_name):
        self.vrf_name = vrf_name
        new_enter_command = self.NEW_ENTER_COMMAND.format(vrf_name)

        super(AristaVrfCommandMode, self).__init__(
            self.PROMPT.format(vrf_name),
            self.ENTER_COMMAND.format(vrf_name),
            exit_command=self.EXIT_COMMAND,
            enter_action_map={
                self.DEPRECATED_VRF_COMMAND_PATTERN: lambda session, logger: (
                    session.send_line(new_enter_command, logger)
                )
            },
            exit_action_map={
                self.DEPRECATED_VRF_COMMAND_PATTERN: lambda session, logger: (
                    session.send_line(self.NEW_EXIT_COMMAND, logger)
                )
            },
        )

        self.parent_node = self._parent_mode


CommandMode.RELATIONS_DICT = {
    AristaDefaultCommandMode: {AristaEnableCommandMode: {AristaConfigCommandMode: {}}}
}
