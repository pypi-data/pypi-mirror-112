"""
options: base configuration and file management classes for denovo projects
Corey Rayburn Yung <coreyrayburnyung@gmail.com>
Copyright 2020-2021, Corey Rayburn Yung
License: Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0)

Contents:
    FileFormat (object): contains data needed for a Clerk-compatible file 
        format.
    formats (Dict[str, FileFormat]): a dictionary of the default supported file
        formats.
    Clerk (object): interface for denovo file management classes and methods.
    Distributor (object): base class for loading or saving items.
    FileLoader (Distributor): handles file input.
    FileSaver (Distributor): handles file output.
     
"""
from __future__ import annotations
import abc
import copy
import dataclasses
import importlib.util
import pathlib
from typing import (Any, Callable, ClassVar, Dict, Hashable, Iterable, List, 
                    Mapping, MutableMapping, MutableSequence, Optional, 
                    Sequence, Set, Tuple, Type, Union)

import denovo


@dataclasses.dataclass
class FileFormat(object):
    """File format information.

    Args:
        name (str): the format name which should match the key when a FileFormat
            instance is stored.
        module (str): name of module where object to incorporate is, which can 
            either be a denovo or non-denovo module. Defaults to 'denovo'.
        extension (str): actual file extension to use. Defaults to None.
        load_method (str): name of import method in 'module' to use. If module 
            is None, the Distributor looks for the method as a local attribute. 
            Defaults to None.
        save_method (str): name of export method in 'module' to use. If module 
            is None, the Distributor looks for the method as a local attribute. 
            Defaults to None.
        parameters (Mapping[Any, Any]]): shared parameters that may be passed to 
            the import or export methods with a common name structure. Defaults 
            to None.

    """
    name: str = None
    module: str = 'denovo'
    extension: str = None
    load_method: str = None
    save_method: str = None
    parameters: Mapping[str, str] = dataclasses.field(default_factory = dict)
    

formats: Dict[str, FileFormat] = {
    'csv': FileFormat(
        name = 'csv',
        module =  'pandas',
        extension = '.csv',
        load_method = 'read_csv',
        save_method = 'to_csv',
        parameters = {
            'encoding': 'file_encoding',
            'index_col': 'index_column',
            'header': 'include_header',
            'low_memory': 'conserve_memory',
            'nrows': 'test_size'}),
    'excel': FileFormat(
        name = 'excel',
        module =  'pandas',
        extension = '.xlsx',
        load_method = 'read_excel',
        save_method = 'to_excel',
        parameters = {
            'index_col': 'index_column',
            'header': 'include_header',
            'nrows': 'test_size'}),
    'feather': FileFormat(
        name = 'feather',
        module =  'pandas',
        extension = '.feather',
        load_method = 'read_feather',
        save_method = 'to_feather',
        parameters = {'nthreads': 'threads'}),
    'hdf': FileFormat(
        name = 'hdf',
        module =  'pandas',
        extension = '.hdf',
        load_method = 'read_hdf',
        save_method = 'to_hdf',
        parameters = {
            'columns': 'included_columns',
            'chunksize': 'test_size'}),
    'json': FileFormat(
        name = 'json',
        module =  'pandas',
        extension = '.json',
        load_method = 'read_json',
        save_method = 'to_json',
        parameters = {
            'encoding': 'file_encoding',
            'columns': 'included_columns',
            'chunksize': 'test_size'}),
    'stata': FileFormat(
        name = 'stata',
        module =  'pandas',
        extension = '.dta',
        load_method = 'read_stata',
        save_method = 'to_stata',
        parameters = {'chunksize': 'test_size'}),
    'text': FileFormat(
        name = 'text',
        module =  None,
        extension = '.txt',
        load_method = '_import_text',
        save_method = '_export_text'),
    'png': FileFormat(
        name = 'png',
        module =  'seaborn',
        extension = '.png',
        save_method = 'save_fig',
        parameters = {
            'bbox_inches': 'visual_tightness', 
            'format': 'visual_format'}),
    'pickle': FileFormat(
        name = 'pickle',
        module =  None,
        extension = '.pickle',
        load_method = '_pickle_object',
        save_method = '_unpickle_object')}   
    
default_parameters: Dict[str, Any] = {
    'file_encoding': 'windows-1252',
    'index_column': True,
    'include_header': True,
    'conserve_memory': False,
    'test_size': 1000,
    'threads': -1,
    'visual_tightness': 'tight', 
    'visual_format': 'png'}

   
@dataclasses.dataclass
class Clerk(object):
    """File and folder management for denovo.

    Creates and stores dynamic and static file paths, properly formats files
    for import and export, and provides methods for loading and saving
    denovo, pandas, and numpy objects.

    Args:
        settings (Settings): a Settings instance, preferably with a section 
            named 'files' with file-management related settings. If 'settings' 
            does ot have file configuration options or if 'settings' is None, 
            internal defaults will be used. Defaults to None.
        root_folder (Union[str, pathlib.Path]): the complete path from which the 
            other paths and folders used by Clerk are ordinarily derived 
            (unless you decide to use full paths for all other options). 
            Defaults to None. If not passed, the parent folder of the current 
            working workery is used.
        input_folder (Union[str, pathlib.Path]]): the input_folder subfolder 
            name or a complete path if the 'input_folder' is not off of
            'root_folder'. Defaults to 'input'.
        output_folder (Union[str, pathlib.Path]]): the output_folder subfolder
            name or a complete path if the 'output_folder' is not off of
            'root_folder'. Defaults to 'output'.
        formats (MutableMapping[str, FileFormat]): a dictionary of file_formats
            and keys with the denovo str names of those formats. Defaults to the
            global 'formats' variable.
        parameters (MutableMapping[str, str]): keys are the denovo names of 
            parameters and values are the values which should be passed to the
            Distributor instances when loading or savings files. Defaults to the
            global 'default_parameters' variable.

    """
    settings: denovo.Settings = None
    root_folder: Union[str, pathlib.Path] = None
    input_folder: Union[str, pathlib.Path] = 'input'
    output_folder: Union[str, pathlib.Path] = 'output'
    formats: MutableMapping[str, FileFormat] = dataclasses.field(
        default_factory = lambda: formats)
    parameters: MutableMapping[str, str] = dataclasses.field(
        default_factory = lambda: default_parameters) 
    
    """ Initialization Methods """

    def __post_init__(self) -> None:
        """Initializes class instance attributes."""
        # Validates core folder paths and writes them to disk.
        self.root_folder = self.root_folder or pathlib.Path('..')
        self.root_folder = self.validate(path = self.root_folder)
        self.input_folder = self._validate_io_folder(path = self.input_folder)
        self.output_folder = self._validate_io_folder(path = self.output_folder)
        # Gets default parameters for file transfers from 'settings'.
        base = copy.deepcopy(default_parameters)
        base.update(self.parameters)
        self.parameters = base
        # Adds and/overrides 'parameters' from 'settings'.
        self._add_settings()
        # Creates FileLoader and FileSaver instances for loading and saving
        # files.
        self.loader = FileLoader(clerk = self)
        self.saver = FileSaver(clerk = self)
        return self

    """ Public Methods """
  
    def load(self,
             file_path: Union[str, pathlib.Path] = None,
             folder: Union[str, pathlib.Path] = None,
             file_name: str = None,
             file_format: Union[str, FileFormat] = None,
             **kwargs) -> Any:
        """Imports file by calling appropriate method based on file_format.

        If needed arguments are not passed, default values are used. If
        'file_path' is passed, 'folder' and 'file_name' are ignored.

        Args:
            file_path (Union[str, Path]]): a complete file path.
                Defaults to None.
            folder (Union[str, Path]]): a complete folder path or the
                name of a folder stored in 'clerk'. Defaults to None.
            file_name (str): file name without extension. Defaults to
                None.
            file_format (Union[str, FileFormat]]): object with
                information about how the file should be loaded or the key to
                such an object stored in 'clerk'. Defaults to None
            **kwargs: can be passed if additional options are desired specific
                to the pandas or python method used internally.

        Returns:
            Any: depending upon method used for appropriate file format, a new
                variable of a supported type is returned.

        """
        return self.loader.transfer(file_path = file_path,
                                    folder = folder,
                                    file_name = file_name,
                                    file_format = file_format,
                                    **kwargs)

    def save(self,
             item: Any,
             file_path: Union[str, pathlib.Path] = None,
             folder: Union[str, pathlib.Path] = None,
             file_name: str = None,
             file_format: Union[str, FileFormat] = None,
             **kwargs) -> None:
        """Exports file by calling appropriate method based on file_format.

        If needed arguments are not passed, default values are used. If
        file_path is passed, folder and file_name are ignored.

        Args:
            item (Any): object to be save to disk.
            file_path (Union[str, pathlib.Path]]): a complete file path.
                Defaults to None.
            folder (Union[str, pathlib.Path]]): a complete folder path or the
                name of a folder stored in 'clerk'. Defaults to None.
            file_name (str): file name without extension. Defaults to
                None.
            file_format (Union[str, FileFormat]]): object with
                information about how the file should be loaded or the key to
                such an object stored in 'clerk'. Defaults to None
            **kwargs: can be passed if additional options are desired specific
                to the pandas or python method used internally.

        """
        self.saver.transfer(item = item,
                            file_path = file_path,
                            folder = folder,
                            file_name = file_name,
                            file_format = file_format,
                            **kwargs)
        return self

    def validate(self, path: Union[str, pathlib.Path],
                 test: bool = True,
                 create: bool = True) -> pathlib.Path:
        """Turns 'file_path' into a pathlib.Path.

        Args:
            path (Union[str, pathlib.Path]): str or Path to be validated. If
                a str is passed, the method will see if an attribute matching
                'path' exists and if that attribute contains a Path.
            test (bool): whether to test if the path exists. Defaults to True.
            create (bool): whether to create the folder path if 'test' is True,
                but the folder does not exist. Defaults to True.

        Raises:
            TypeError: if 'path' is neither a str nor Path.
            FileNotFoundError: if the validated path does not exist and 'create'
                is False.

        Returns:
            pathlib.Path: derived from 'path'.

        """
        if isinstance(path, str):
            if (hasattr(self, path) 
                    and isinstance(getattr(self, path), pathlib.Path)):
                validated = getattr(self, path)
            else:
                validated = pathlib.Path(path)
        elif isinstance(path, pathlib.Path):
            validated = path
        else:
            raise TypeError(f'path must be a str or Path type')
        if test and not validated.exists():
            if create:
                self._write_folder(folder = validated)
            else:
                raise FileNotFoundError(f'{validated} does not exist')
        return validated
      
    """ Private Methods """

    def _validate_io_folder(self, 
                            path: Union[str, pathlib.Path]) -> pathlib.Path:
        """Validates an import or export path.

        Args:
            path (Union[str, pathlib.Path]): path to be validated.

        Returns:
            pathlib.Path: validated path.
            
        """
        try:
            return self.validate(path = path, create = False)
        except FileNotFoundError:
            return self.validate(path = self.root_folder / path)

    def _add_settings(self) -> None:
        """Returns default parameters for file transfers from 'settings'."""
        for section in ['files', 'filer', 'clerk']:
            if section in self.settings:
                self.parameters.update(self.settings[section])
        return self

    def _write_folder(self, folder: Union[str, pathlib.Path]) -> None:
        """Writes folder to disk.

        Parent folders are created as needed.

        Args:
            folder (Union[str, Path]): intended folder to write to disk.

        """
        pathlib.Path.mkdir(folder, parents = True, exist_ok = True)
        return self

    def _make_unique_path(self, 
                          folder: Union[pathlib.Path, str],
                          name: str) -> pathlib.Path:
        """Creates a unique path to avoid overwriting a file or folder.

        Thanks to RealPython for this bit of code:
        https://realpython.com/python-pathlib/.

        Args:
            folder (Path): the folder where the file or folder will be located.
            name (str): the basic name that should be used.

        Returns:
            Path: with a unique name. If the original name conflicts with an
                existing file/folder, a counter is used to find a unique name
                with the counter appended as a suffix to the original name.

        """
        counter = 0
        while True:
            counter += 1
            path = pathlib.Path(folder) / name.format(counter)
            if not path.exists():
                return path


@dataclasses.dataclass
class Distributor(abc.ABC):
    """Base class for loading and saving classes.

    Args:
        clerk (Clerk): a related Clerk instance.

    """
    clerk: Clerk

    """ Private Methods """

    def _check_file_format(self,
                           file_format: Union[str, FileFormat]) -> FileFormat:
        """Selects 'file_format' or returns FileFormat instance intact.

        Args:
            file_format (Union[str, FileFormat]): name of file format or a
                FileFormat instance.

        Raises:
            TypeError: if 'file_format' is neither a str nor FileFormat type.

        Returns:
            FileFormat: appropriate instance.

        """
        if isinstance(file_format, FileFormat):
            return file_format
        elif isinstance(file_format, str):
            return self.clerk.formats[file_format]
        else:
            raise TypeError('file_format must be a str or FileFormat type')
    
    def _combine(self, 
                 folder: str,
                 file_name: str = None,
                 extension: str = None) -> pathlib.Path:
        """Converts strings to pathlib Path object.

        If 'folder' matches an attribute, the value stored in that attribute
        is substituted for 'folder'.

        If 'name' and 'extension' are passed, a file path is created. Otherwise,
        a folder path is created.

        Args:
            folder (str): folder for file location.
            name (str): the name of the file.
            extension (str): the extension of the file.

        Returns:
            Path: formed from string arguments.

        """
        try:
            folder = getattr(self, folder)
        except (AttributeError, TypeError):
            pass
        if file_name and extension:
            return pathlib.Path(folder).joinpath(f'{file_name}.{extension}')
        else:
            return pathlib.Path(folder)
    
    def _get_parameters(self,
                        file_format: FileFormat,
                        **kwargs) -> Mapping[Any, Any]:
        """Creates complete parameters for a file input/output method.

        Args:
            file_format (FileFormat): an instance with information about the
                needed and optional parameters.
            kwargs: additional parameters to pass to an input/output method.

        Returns:
            Mapping[Any, Any]: parameters to be passed to an input/output 
                method.

        """
        if file_format.parameters:
            for key, value in file_format.parameters:
                if value not in kwargs:
                    kwargs[key] = self.parameters[value]
        return kwargs

    def _prepare_transfer(self, 
                          file_path: Union[str, pathlib.Path],
                          folder: Union[str, pathlib.Path],
                          file_name: str,
                          file_format: Union[str, FileFormat]) -> (
                              Sequence[Union[pathlib.Path, FileFormat]]):
        """Prepares file path related arguments for loading or saving a file.

        Args:
            file_path (Union[str, Path]): a complete file path.
            folder (Union[str, Path]): a complete folder path or the name of a
                folder stored in 'clerk'.
            file_name (str): file name without extension.
            file_format (Union[str, FileFormat]): object with information about
                how the file should be loaded or the key to such an object
                stored in 'clerk'.
            **kwargs: can be passed if additional options are desired specific
                to the pandas or python method used internally.

        Returns:
            Sequence: of a completed Path instance and FileFormat instance.

        """
        if file_path:
            file_path = denovo.tools.pathlibify(item = file_path)
            if not file_format:
                file_format = [f for f in self.clerk.formats.values()
                               if f.extension == file_path.suffix[1:]][0]
        file_format = self._check_file_format(file_format = file_format)
        extension = file_format.extension
        if not file_path:
            file_path = self.combine(folder = folder, 
                                     file_name = file_name,
                                     extension = extension)
        return file_path, file_format


@dataclasses.dataclass
class FileLoader(Distributor):
    """Manages file importing for denovo.

    Args:
        clerk (Clerk): related Clerk instance.

    """
    clerk: Clerk

    """ Public Methods """

    def load(self, **kwargs):
        """Calls 'transfer' method with **kwargs."""
        return self.transfer(**kwargs)

    def transfer(self,
                 file_path: Union[str, pathlib.Path] = None,
                 folder: Union[str, pathlib.Path] = None,
                 file_name: str = None,
                 file_format: Union[str, FileFormat] = None,
                 **kwargs) -> Any:
        """Imports file by calling appropriate method based on file_format.

        If needed arguments are not passed, default values are used. If
        file_path is passed, folder and file_name are ignored.

        Args:
            file_path (Union[str, Path]]): a complete file path.
                Defaults to None.
            folder (Union[str, Path]]): a complete folder path or the
                name of a folder stored in 'clerk'. Defaults to None.
            file_name (str): file name without extension. Defaults to
                None.
            file_format (Union[str, FileFormat]]): object with
                information about how the file should be loaded or the key to
                such an object stored in 'clerk'. Defaults to None
            **kwargs: can be passed if additional options are desired specific
                to the pandas or python method used internally.

        Returns:
            Any: depending upon method used for appropriate file format, a new
                variable of a supported type is returned.

        """
        file_path, file_format = self._prepare_transfer(
            file_path = file_path,
            folder = folder,
            file_name = file_name,
            file_format = file_format)
        parameters = self._get_parameters(file_format = file_format, **kwargs)
        if file_format.module:
            tool = file_format.load('import_method')
        else:
            tool = getattr(self, file_format.import_method)
        return tool(file_path, **parameters)


@dataclasses.dataclass
class FileSaver(Distributor):
    """Manages file exporting for denovo.

    Args:
        clerk (Clerk): related Clerk instance.

    """
    clerk: Clerk

    """ Public Methods """

    def save(self, **kwargs):
        """Calls 'transfer' method with **kwargs."""
        return self.transfer(**kwargs)

    def transfer(self,
                 item: Any,
                 file_path: Union[str, pathlib.Path] = None,
                 folder: Union[str, pathlib.Path] = None,
                 file_name: str = None,
                 file_format: Union[str, FileFormat] = None,
                 **kwargs) -> None:
        """Exports file by calling appropriate method based on file_format.

        If needed arguments are not passed, default values are used. If
        file_path is passed, folder and file_name are ignored.

        Args:
            item (Any): object to be save to disk.
            file_path (Union[str, Path]]): a complete file path.
                Defaults to None.
            folder (Union[str, Path]]): a complete folder path or the
                name of a folder stored in 'clerk'. Defaults to None.
            file_name (str): file name without extension. Defaults to
                None.
            file_format (Union[str, FileFormat]]): object with
                information about how the file should be loaded or the key to
                such an object stored in 'clerk'. Defaults to None
            **kwargs: can be passed if additional options are desired specific
                to the pandas or python method used internally.

        """
        file_path, file_format = self._prepare_transfer(
            file_path = file_path,
            folder = folder,
            file_name = file_name,
            file_format = file_format)
        parameters = self._get_parameters(file_format = file_format, **kwargs)
        if file_format.module:
            getattr(item, file_format.export_method)(item, **parameters)
        else:
            getattr(self, file_format.export_method)(item, **parameters)
        return self
