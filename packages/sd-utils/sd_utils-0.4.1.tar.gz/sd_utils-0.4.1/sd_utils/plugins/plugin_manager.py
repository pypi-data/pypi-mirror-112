from sd_utils.plugins.plugin_base import PluginBase
from typing import Any, ClassVar, final


class PluginManager:
    def __init__(self):
        self._plugins = {}

    @final
    def register(self, name: str, on_register_params: dict = {}, **kwargs):
        """
        decorator for registering a plugin to this instance of a
        plugin manager

        Args:
            name (str): the name to register this plugin under
            **kwargs: parameters to be passed to the plugin
                class when constructed
        """

        def decorator(plugin: ClassVar[PluginBase]):
            if name in self._plugins:
                raise ValueError(f"Plugin with name [{name}] already exists")

            class Wrapper:
                def __init__(self, plugin):
                    self.name = name
                    self.plugin = plugin

            w = Wrapper(plugin(**kwargs))

            self._plugins[name] = w
            try:
                w.plugin.on_register(
                    self.get_on_register_params(name, **on_register_params)
                )
            except NotImplementedError:
                # dont need to implement this hook
                pass

            return w

        return decorator

    @final
    def run(
        self, name: str, on_search_params: dict = {}, on_find_params: dict = {}
    ) -> Any:
        """
        runs a given plugin.

        Note: this function iterates over all plugins and will call the
        on_search for each plugin before executing the on_find hook
        for the plugin being searched for.

        This function should not be used just to iterate over every plugin.
        instead the iterate_all function should be used

        Args:
            name (str): the name of the plugin to run
            on_search_params (dict): parameters to pass to
                the get_on_search_params function
            on_find_params (dict): parameters to pass to
                the get_on_find_params functions

        Returns:
            Any: The value returned by running the to_find
                function of the called plugin
        """

        to_run = None
        for plugin_name, wrapper in self._plugins.items():
            if name == plugin_name:
                to_run = wrapper
            try:
                wrapper.plugin.on_search(
                    self.get_on_search_params(name, **on_search_params)
                )
            except NotImplementedError:
                # just skip if its not implemented
                pass

        if to_run is None:
            raise ValueError(f"Unable to find plugin with name [{name}]")

        return to_run.plugin.on_find(
            self.get_on_find_params(name, **on_find_params)
        )

    @final
    def iterate_all(self, on_iterate_params: dict = {}):
        """
        Iterates over all the plugins without directly calling
        one of them. Only hook used is on_iterate

        Args:
            on_iterate_params (dict): a list of parameters to pass
                to the on_iterate hook
        """
        for name, wrapper in self._plugins.items():
            try:
                wrapper.plugin.on_iterate(
                    self.get_on_iterate_params(name, **on_iterate_params)
                )
            except NotImplementedError:
                # just skip if its not implemented
                pass

    def get_on_search_params(self, name: str, **kwargs) -> Any:
        """
        function that generates parameters for the on
        search function of a plugin given its name

        Args:
            name (str): the name of the command to
                call on_search for
            **kwargs: any arguments sent from the run
                function

        Returns:
            Any: the arguments to be sent to the on_search function
        """
        return kwargs

    def get_on_find_params(self, name: str, **kwargs) -> Any:
        """
        function that generates parameters for the on
        find function of a plugin given its name

        Args:
            name (str): the name of the command to
                call on_find for
            **kwargs: any arguments sent from the run
                function

        Returns:
            Any: the arguments to be sent to the on_find function
        """
        return kwargs

    def get_on_register_params(self, name: str, **kwargs) -> Any:
        """
        function that generates parameters for the on
        register function of a plugin given its name

        Args:
            name (str): the name of the command to
                call on_register for
            **kwargs: any arguments sent from the
                register function

        Returns:
            Any: the arguments to be sent to the
                on_register function
        """
        return kwargs

    def get_on_iterate_params(self, name: str, **kwargs) -> Any:
        """
        function that generates parameters for the on
        iterate_all function of a plugin given its name

        Args:
            name (str): the name of the command to
                call iterate_all for
            **kwargs: any arguments sent from the
                iterate_all function

        Returns:
            Any: the arguments to be sent to the
                iterate_all function
        """
        return kwargs
