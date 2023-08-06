from typing import Any


class PluginBase:
    """
    """

    def __init__(self, **kwargs):
        """
        """
        pass

    def on_register(self, data: Any = None):
        """
        runs when this plugin is registered with
        the plugin manager

        Args:
            data (Any): any parameters passed to this
                plugin from the plugin manager
        """
        raise NotImplementedError

    def on_search(self, data: Any = None):
        """
        runs when the manager begins a query for
        any plugin.

        Args:
            data (Any): any parameters passed to this
                plugin from the plugin manager
        """
        raise NotImplementedError

    def on_find(self, data: Any = None) -> Any:
        """
        runs when the manager specifically queries this plugin

        Args:
            data (Any): any parameters passed to this
                plugin from the plugin manager
        """
        raise NotImplementedError

    def on_iterate(self, data: Any = None):
        """
        runs when the manager specifically calls iterate_all

        Args:
            data (Any): any parameters passed to this
                plugin from the plugin manager
        """
        raise NotImplementedError
