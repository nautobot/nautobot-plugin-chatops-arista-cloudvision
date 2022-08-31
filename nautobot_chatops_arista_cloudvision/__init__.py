"""Plugin declaration for nautobot_chatops_arista_cloudvision."""
# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
try:
    from importlib import metadata
except ImportError:
    # Python version < 3.8
    import importlib_metadata as metadata

from nautobot.extras.plugins import PluginConfig

__version__ = metadata.version(__name__)


class NautobotChatopsExtensionAristaConfig(PluginConfig):
    """Plugin configuration for the nautobot_chatops_arista_cloudvision plugin."""

    name = "nautobot_chatops_arista_cloudvision"
    verbose_name = "Nautobot Chatops Arista Cloudvision Integration"
    version = __version__
    author = "Network to Code, LLC"
    description = "Nautobot Chatops Arista Cloudvision Integration."
    base_url = "nautobot_chatops_arista_cloudvision"
    required_settings = []
    min_version = "1.2.0"
    max_version = "1.9999"
    default_settings = {}
    caching_config = {}


config = NautobotChatopsExtensionAristaConfig  # pylint:disable=invalid-name
