"""Plugin declaration for nautobot_chatops_extension_arista."""

__version__ = "0.1.0"

from nautobot.extras.plugins import PluginConfig


class NautobotChatopsExtensionAristaConfig(PluginConfig):
    """Plugin configuration for the nautobot_chatops_extension_arista plugin."""

    name = "nautobot_chatops_extension_arista"
    verbose_name = "Nautobot Chatops Extension Arista"
    version = __version__
    author = "Network to Code, LLC"
    description = "Nautobot Chatops Extension Arista."
    base_url = "nautobot-chatops-extension-arista"
    required_settings = []
    min_version = "1.0.0"
    max_version = "1.9999"
    default_settings = {}
    caching_config = {}


config = NautobotChatopsExtensionAristaConfig  # pylint:disable=invalid-name
