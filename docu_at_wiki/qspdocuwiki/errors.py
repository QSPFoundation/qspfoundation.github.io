class ConverterError(Exception):
    """Base error for expected converter failures."""


class ConfigError(ConverterError):
    """The converter configuration is invalid."""


class ConversionError(ConverterError):
    """A source page cannot be converted without losing content."""


class StateError(ConverterError):
    """The local incremental state file is invalid."""
