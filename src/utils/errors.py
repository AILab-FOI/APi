#!/usr/bin/env python3


class APiIOError(IOError):
    """Exception thrown when a file (usually agent definition) is not present."""

    pass


class APiCommunicationError(IOError):
    """
    Exception thrown when there is a communication error (e.g. someone tries to
    write to and agent that does not accept input on this channel.
    """

    pass


class APiAgentDefinitionError(Exception):
    """Exception thrown when an agent definition file is not parsable."""

    pass


class APiHolonConfigurationError(Exception):
    """Exception thrown when a holon configuration file is not parsable."""

    pass


class XMPPRegisterException(Exception):
    """Exception thrown when the system cannot register at a XMPP registration service"""

    pass


class APiChannelDefinitionError(Exception):
    """Exception thrown when a channel is ill-defined"""

    pass


class APiShellInitError(Exception):
    """Exception thrown when shell server hasn't been initialized"""

    pass


class APiHTTPSWarning(Warning):
    """Warning when HTTP is used instead of HTTPS"""

    pass


class APiCallbackException(Exception):
    """Exception thrown when a callback fails"""

    pass
