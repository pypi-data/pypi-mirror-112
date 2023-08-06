from typing import Any
from pencil_pusher.configs.manager import ConfigManager
from pencil_pusher.configs.base import ConfigParamBase
from pencil_pusher.configs import config_manager


@config_manager.register("sidebar")
class SidebarConfigParam(ConfigParamBase):
    """
    Processes the sidebar config parameter

    Note: validation only validates config name
        and config type (string array)
    """

    def on_iterate(self, data: Any):
        """
        This is the validate function
        """
        if data["type"] == ConfigManager.VALIDATE:
            self._validate(data["contents"])
            self.set_defined()

    def _validate(self, contents: dict) -> bool:
        """
        Validates the parameter is included in the
        config file since it is a required field
        """
        if "sidebar" not in contents:
            # set default value
            contents["sidebar"] = False
            return True

        if not isinstance(contents["sidebar"], bool):
            raise ValueError("sidebar config parameter is not of type bool")

        return True
