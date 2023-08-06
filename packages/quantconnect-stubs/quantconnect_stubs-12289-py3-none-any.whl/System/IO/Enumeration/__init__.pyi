import abc
import typing

import System
import System.Collections
import System.Collections.Generic
import System.IO
import System.IO.Enumeration
import System.Runtime.ConstrainedExecution

System_IO_Enumeration_FileSystemEnumerable_TResult = typing.TypeVar("System_IO_Enumeration_FileSystemEnumerable_TResult")
System_IO_Enumeration_FileSystemEnumerator_TResult = typing.TypeVar("System_IO_Enumeration_FileSystemEnumerator_TResult")


class FileSystemEntry:
    """Lower level view of FileSystemInfo used for processing and filtering find results."""

    @property
    def _directoryEntry(self) -> typing.Any:
        ...

    @_directoryEntry.setter
    def _directoryEntry(self, value: typing.Any):
        ...

    @property
    def FileName(self) -> System.ReadOnlySpan[str]:
        ...

    @property
    def Directory(self) -> System.ReadOnlySpan[str]:
        """The full path of the directory this entry resides in."""
        ...

    @Directory.setter
    def Directory(self, value: System.ReadOnlySpan[str]):
        """The full path of the directory this entry resides in."""
        ...

    @property
    def RootDirectory(self) -> System.ReadOnlySpan[str]:
        """The full path of the root directory used for the enumeration."""
        ...

    @RootDirectory.setter
    def RootDirectory(self, value: System.ReadOnlySpan[str]):
        """The full path of the root directory used for the enumeration."""
        ...

    @property
    def OriginalRootDirectory(self) -> System.ReadOnlySpan[str]:
        """The root directory for the enumeration as specified in the constructor."""
        ...

    @OriginalRootDirectory.setter
    def OriginalRootDirectory(self, value: System.ReadOnlySpan[str]):
        """The root directory for the enumeration as specified in the constructor."""
        ...

    @property
    def Attributes(self) -> int:
        """This property contains the int value of a member of the System.IO.FileAttributes enum."""
        ...

    @property
    def Length(self) -> int:
        ...

    @property
    def CreationTimeUtc(self) -> System.DateTimeOffset:
        ...

    @property
    def LastAccessTimeUtc(self) -> System.DateTimeOffset:
        ...

    @property
    def LastWriteTimeUtc(self) -> System.DateTimeOffset:
        ...

    @property
    def IsDirectory(self) -> bool:
        ...

    @property
    def IsHidden(self) -> bool:
        ...

    @property
    def IsReadOnly(self) -> bool:
        ...

    @property
    def IsSymbolicLink(self) -> bool:
        ...

    @property
    def _info(self) -> typing.Any:
        ...

    @_info.setter
    def _info(self, value: typing.Any):
        ...

    @typing.overload
    def ToFileSystemInfo(self) -> System.IO.FileSystemInfo:
        ...

    @typing.overload
    def ToFileSystemInfo(self) -> System.IO.FileSystemInfo:
        ...

    @typing.overload
    def ToFullPath(self) -> str:
        """Returns the full path of the find result."""
        ...

    @typing.overload
    def ToFullPath(self) -> str:
        """Returns the full path of the find result."""
        ...

    def ToSpecifiedFullPath(self) -> str:
        """Returns the full path for find results, based on the initially provided path."""
        ...


class FileSystemEnumerable(typing.Generic[System_IO_Enumeration_FileSystemEnumerable_TResult], System.Object, typing.Iterable[System_IO_Enumeration_FileSystemEnumerable_TResult]):
    """Enumerable that allows utilizing custom filter predicates and tranform delegates."""

    @property
    def ShouldIncludePredicate(self) -> typing.Callable[[System.IO.Enumeration.FileSystemEntry], bool]:
        ...

    @ShouldIncludePredicate.setter
    def ShouldIncludePredicate(self, value: typing.Callable[[System.IO.Enumeration.FileSystemEntry], bool]):
        ...

    @property
    def ShouldRecursePredicate(self) -> typing.Callable[[System.IO.Enumeration.FileSystemEntry], bool]:
        ...

    @ShouldRecursePredicate.setter
    def ShouldRecursePredicate(self, value: typing.Callable[[System.IO.Enumeration.FileSystemEntry], bool]):
        ...

    def __init__(self, directory: str, transform: typing.Callable[[System.IO.Enumeration.FileSystemEntry], System_IO_Enumeration_FileSystemEnumerable_TResult], options: System.IO.EnumerationOptions = None) -> None:
        ...

    def FindPredicate(self, entry: System.IO.Enumeration.FileSystemEntry) -> bool:
        """Delegate for filtering out find results."""
        ...

    def FindTransform(self, entry: System.IO.Enumeration.FileSystemEntry) -> System_IO_Enumeration_FileSystemEnumerable_TResult:
        """Delegate for transforming raw find data into a result."""
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.Generic.IEnumerator[System_IO_Enumeration_FileSystemEnumerable_TResult]:
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.IEnumerator:
        ...


class FileSystemEnumerator(typing.Generic[System_IO_Enumeration_FileSystemEnumerator_TResult], System.Runtime.ConstrainedExecution.CriticalFinalizerObject, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def Current(self) -> System_IO_Enumeration_FileSystemEnumerator_TResult:
        ...

    def __init__(self, directory: str, options: System.IO.EnumerationOptions = None) -> None:
        """
        Encapsulates a find operation.
        
        :param directory: The directory to search in.
        :param options: Enumeration options to use.
        """
        ...

    def ContinueOnError(self, error: int) -> bool:
        """
        Called when a native API returns an error that would normally cause a throw.
        Return true to continue, or false to throw the default exception for the given error.
        
        This method is protected.
        
        :param error: The native error code.
        """
        ...

    @typing.overload
    def Dispose(self) -> None:
        ...

    @typing.overload
    def Dispose(self, disposing: bool) -> None:
        """
        Override for any additional cleanup.
        
        This method is protected.
        
        :param disposing: True if called while disposing. False if called from finalizer.
        """
        ...

    @typing.overload
    def MoveNext(self) -> bool:
        ...

    @typing.overload
    def MoveNext(self) -> bool:
        ...

    def OnDirectoryFinished(self, directory: System.ReadOnlySpan[str]) -> None:
        """
        Called whenever the end of a directory is reached.
        
        This method is protected.
        
        :param directory: The path of the directory that finished.
        """
        ...

    def Reset(self) -> None:
        ...

    def ShouldIncludeEntry(self, entry: System.IO.Enumeration.FileSystemEntry) -> bool:
        """
        Return true if the given file system entry should be included in the results.
        
        This method is protected.
        """
        ...

    def ShouldRecurseIntoEntry(self, entry: System.IO.Enumeration.FileSystemEntry) -> bool:
        """
        Return true if the directory entry given should be recursed into.
        
        This method is protected.
        """
        ...

    def TransformEntry(self, entry: System.IO.Enumeration.FileSystemEntry) -> System_IO_Enumeration_FileSystemEnumerator_TResult:
        """
        Generate the result type from the current entry;
        
        This method is protected.
        """
        ...


class FileSystemName(System.Object):
    """Provides methods for matching file system names."""

    @staticmethod
    def MatchesSimpleExpression(expression: System.ReadOnlySpan[str], name: System.ReadOnlySpan[str], ignoreCase: bool = True) -> bool:
        """Return true if the given expression matches the given name. '*' and '?' are wildcards, '\\' escapes."""
        ...

    @staticmethod
    def MatchesWin32Expression(expression: System.ReadOnlySpan[str], name: System.ReadOnlySpan[str], ignoreCase: bool = True) -> bool:
        """
        Return true if the given expression matches the given name. Supports the following wildcards:
        '*', '?', '<', '>', '"'. The backslash character '\\' escapes.
        
        :param expression: The expression to match with, such as "*.foo".
        :param name: The name to check against the expression.
        :param ignoreCase: True to ignore case (default).
        """
        ...

    @staticmethod
    def TranslateWin32Expression(expression: str) -> str:
        """
        Change '*' and '?' to '<', '>' and '"' to match Win32 behavior. For compatibility, Windows
        changes some wildcards to provide a closer match to historical DOS 8.3 filename matching.
        """
        ...


