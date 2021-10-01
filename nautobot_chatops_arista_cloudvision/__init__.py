"""Plugin declaration for nautobot_chatops_arista_cloudvision."""

__version__ = "1.0.2"

from nautobot.extras.plugins import PluginConfig


class NautobotChatopsExtensionAristaConfig(PluginConfig):
    """Plugin configuration for the nautobot_chatops_arista_cloudvision plugin."""

    name = "nautobot_chatops_arista_cloudvision"
    verbose_name = "Nautobot Chatops Arista Cloudvision Integration"
    version = __version__
    author = "Network to Code, LLC"
    description = "Nautobot Chatops Arista Cloudvision Integration."
    base_url = "nautobot_chatops_arista_cloudvision"
    required_settings = []
    min_version = "1.0.0"
    max_version = "1.9999"
    default_settings = {}
    caching_config = {}


config = NautobotChatopsExtensionAristaConfig  # pylint:disable=invalid-name
