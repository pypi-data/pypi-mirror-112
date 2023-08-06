from sd_utils.plugins.plugin_base import PluginBase
from typing import ClassVar, List
from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module


def collect_plugins(
    registering_file: str,
    registering_file_name: str,
    cls: ClassVar[PluginBase] = PluginBase,
    exclude_files: List[str] = [],
    assert_one_per_source: bool = True,
) -> List[str]:
    """
    collects all the plugins of a given type in the given directory
    then returns the list of plugins processed

    Args:
        registering_file (str): should be `__file__` of the calling file
        registering_file_name (str): should be `__name__` of the calling file
        cls (ClassVar[PluginBase]): the type of plugin to collect
        exclude_files (List[str]): any file to exclude from being collected
            as a plugin
        assert_one_per_source (bool): asserts that only 1 plugin may be
            defined in each source file
            
    Returns:
        List[str]: a list of all the plugin files collected. should be
            stored in the calling files `__all__` variable
    """
    exports = []

    # iterate through the modules in the current package
    package_dir = str(Path(registering_file).resolve().parent)
    for (_, module_name, _) in iter_modules([package_dir]):

        # import the module and iterate through its attributes
        module = import_module(f"{registering_file_name}.{module_name}")
        plugin_count = 0
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)

            if isinstance(attribute, cls) and module_name not in exclude_files:
                if assert_one_per_source and plugin_count == 1:
                    raise ValueError(
                        f"Cannot define multiple pluigns in a single source file [{module_name}]"
                    )
                # Add the class to this package's variables
                exports.append(module_name)
                plugin_count += 1
    return exports
