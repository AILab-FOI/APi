from src.utils.helpers import cycle
from src.utils.errors import APiIOError, APiHolonConfigurationError
from src.config.settings import settings

from uuid import uuid4


try:
    from yaml import CLoader as Loader, load
except ImportError:
    from yaml import Loader, load

_CONFIG_FILE_NAME_TEMPLATE = "{file_name}.cfg"


class APiRegistrationService:
    """
    Registration service that sets up the APi communication channels
    and registers the holon on the XMPP server(s) according to rules
    given in config file.
    """

    def __init__(self, mas_name: str):
        """
        Initializes the registration service.
        """

        self.mas_name = mas_name

        try:
            fh = open(_CONFIG_FILE_NAME_TEMPLATE.format(file_name=mas_name))
        except IOError as e:
            raise APiIOError(
                "Missing holon configuration file or permission issue.\n" + str(e)
            )

        self.services = []
        self._load(fh)
        self.next = lambda: cycle(self.services).__next__()
        self.MAX_RETRIES = 4

    def _load(self, fh):
        """
        Loads the holon configuration file and parses it into a dictionary.
        """

        try:
            self.descriptor = load(fh.read(), Loader)
        except Exception as e:
            err = "Holon configuration file cannot be loaded.\n" + str(e)
            raise APiHolonConfigurationError(err)
        try:
            self.services = self.descriptor["registration-services"]
        except Exception as e:
            err = "Holon configuration file has invalid format.\n" + str(e)
            raise APiHolonConfigurationError(err)
        if not self.services:
            err = "Holon configuration file does not list any services."
            raise APiHolonConfigurationError(err)
        try:
            self.min_port = int(self.descriptor["port-range"]["min"])
            self.max_port = int(self.descriptor["port-range"]["max"])
        except Exception as e:
            err = "Holon configuration file has invalid format.\n" + str(e)
            raise APiHolonConfigurationError(err)

    def register(self, holon_name: str):
        """
        Registers the holon on the XMPP server(s) according to rules
        given in config file.
        """

        username = "%s_%s_%s" % (self.mas_name, holon_name, str(uuid4().hex))
        password = str(uuid4().hex)
        host = settings.xmpp_host

        return ("%s@%s" % (username, host), password)
