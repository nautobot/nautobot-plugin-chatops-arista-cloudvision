"""Plugin declaration for nautobot_plugin_chatops_cloudvision."""

__version__ = "0.1.0"

from nautobot.extras.plugins import PluginConfig


class NautobotChatopsExtensionAristaConfig(PluginConfig):
    """Plugin configuration for the nautobot_plugin_chatops_cloudvision plugin."""

    name = "nautobot_plugin_chatops_cloudvision"
    verbose_name = "Nautobot Plugin Chatops Cloudvision"
    version = __version__
    author = "Network to Code, LLC"
    description = "Nautobot Plugin Chatops Cloudvision."
    base_url = "nautobot_plugin_chatops_cloudvision"
    required_settings = []
    min_version = "1.0.0"
    max_version = "1.9999"
    default_settings = {}
    caching_config = {}


config = NautobotChatopsExtensionAristaConfig  # pylint:disable=invalid-name
