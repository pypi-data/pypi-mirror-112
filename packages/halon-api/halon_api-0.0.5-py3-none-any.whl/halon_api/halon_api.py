import base64
import requests
from requests.models import HTTPError


class HalonAPI:
    def __init__(
        self,
        host: str,
        user: str,
        password: str,
        version: str = "5.6.0",
        secure: bool = True,
        verify: bool = True,
        port: int = None,
    ) -> None:
        """Initialize a HalonAPI object.

        Arguments:
        host -- The fqdn of the Halon server
        user -- The user to access Halon as
        password -- The password for the Halon user
        version -- The version of the Halon API to use
        secure -- Control the use of HTTPS
        verify: Verify certificate on host (Bool) or full chain CA_BUNDLE .pem file
        port: The port to use. Will override 443 for https and 80 for http
        """
        if secure:
            p = "https"
        else:
            p = "http"

        if port:
            port = f":{port}"
        else:
            port = ""

        self.base_url = f"{p}://{host}{port}/api/{version}"
        self.auth = requests.auth.HTTPBasicAuth(user, password)
        self.verify = verify
        # The session to use for all requests (HTTP pooling)
        # self.session = requests.Session()
        # self.headers = {}

        # Don't warn about cert not being verified if user disabled verification
        if not verify:
            requests.urllib3.disable_warnings(
                requests.urllib3.exceptions.InsecureRequestWarning
            )

    def _request(self, method, path, payload={}, params={}) -> dict:
        """Perform a get request."""

        try:
            r = requests.request(
                method=method,
                url=self.base_url + path,
                auth=self.auth,
                json=payload,
                params=params,
                # headers=self.headers,
                verify=self.verify,
            )

            # Raise exception on HTTP error codes
            r.raise_for_status()

        except HTTPError as e:
            # Re-raise exception with Halon error messsage
            j = r.json()
            raise HTTPError(j.get("message")) from e

        # Return True on "no content" response
        if r.status_code == 204:
            return True

        return r.json()

    """ HARDWARE """

    def reboot_system(self) -> bool:
        """Reboot the system."""
        return self._request("POST", "/system:reboot")

    def shut_down_system(self) -> bool:
        """Shut down the system."""
        return self._request("POST", "/system:shutdown")

    """ TIME """

    def get_system_time(self) -> str:
        """Get the current system time as string in format 'YYYY-MM-DDTHH:MM:SSZ'."""
        return self._request("GET", "/system/time")["time"]

    def set_system_time(self, time: str) -> bool:
        """Set the system time

        Arguments:
        time -- Time in format 'YYYY-MM-DDTHH:MM:SSZ'
        """
        payload = {"time": time}
        return self._request("PUT", "/system/time", payload=payload)

    def get_system_uptime(self) -> int:
        """Get the current system uptime in seconds."""
        return self._request("GET", "/system/uptime")["uptime"]

    """ UPDATE """

    def get_software_version(self) -> str:
        """Get the current Halon version."""
        return self._request("GET", "/system/versions/current")["version"]

    def get_latest_software_version(self) -> list:
        """Get the latest Halon versions. This includes the current version"""
        return self._request("GET", "/system/versions/latest")

    def get_update_status(self) -> dict:
        """Get update status. Error code 500 if no update in progress"""
        return self._request("GET", "/system/update")

    def cancel_pending_update(self) -> bool:
        """Cancel a pending update"""
        return self._request("DELETE", "/system/update")

    def download_update(self, version: str) -> bool:
        """Begin downloading (prefetching) an update"""
        payload = {"version": version}
        return self._request("POST", "/system/update:download", payload=payload)

    def install_update(self, version: str) -> bool:
        """Install an update. If on system, it will be downloaded."""
        payload = {"version": version}
        return self._request("POST", "/system/update:install", payload=payload)

    """ DNS """

    def clear_dns_cache(self, filter: str) -> bool:
        """Clear the DNS cache

        Arguments:
        filter -- A filter matching the DNS records to clear
        """
        params = {"filter[name]": filter}
        return self._request("DELETE", "/system/dns/cache", params=params)

    """ COMMANDS """

    """ FILES """

    def read_file(
        self, path: str, size_offset: int = 0, size_limit: int = 1024
    ) -> dict:
        """Read a file from disk"""
        params = {"path": path, "offset": size_offset, "limit": size_limit}
        return self._request("GET", "/system/files", params=params)

    def write_file(self, path: str, data: bytes) -> bool:
        """Write a file to disk"""
        encoded = base64.b64encode(data)
        params = {"path": path}
        payload = {"data": encoded.decode("ascii")}
        return self._request("PUT", "/system/files", params=params, payload=payload)

    def clear_file(self, path: str):
        """Clear a file on disk"""
        params = {"path": path}
        return self._request("DELETE", "/system/files", params=params)

    def get_file_size(self, path: str):
        """Get the size of a file in bytes"""
        params = {"path": path}
        return self._request("POST", "/system/files:size", params=params)

    """ REVISIONS """

    def list_config_revisions(self, offset: int = 0, limit: int = 5) -> list:
        """List the config revisions.

        Arguments:
        offset -- The offset, in pages, to use (>= 0).
        limit -- Maximum number of items to return (1 .. 10000).
        """
        params = {"offset": offset, "limit": limit}
        return self._request("GET", "/config/revisions", params=params)

    def get_config_revision(self, id: str = "HEAD", type: int = None) -> dict:
        """Get a single config revision.

        Arguments:
        id -- A positive integer or the string 'HEAD'
        type -- The config type. Can only be used with HEAD or a test config (-1 .. 5).
        """
        params = {"type": type}
        return self._request("GET", f"/config/revisions/{id}", params=params)

    def create_config_revision(
        self, id: str, config: list, message: str = "Created through API"
    ) -> int:
        """Add a configuration revision. Config is a list of dicts.
        One dict pr. parameter. Return new configuration ID"""
        payload = {"config": config, "message": message}
        return self._request("POST", f"/config/revisions/{id}", payload=payload)["id"]

    """ TESTING/LIVESTAGING """

    def start_config_test(
        self, config: list, id: str = None, conditions: dict = None
    ) -> bool:
        """Start a new configuration test"""
        # payload = {"config": config, "id": id, "conditions": conditions}
        raise NotImplementedError()

    def get_config_test_status(self) -> dict:
        """Get the status of the running config test"""
        raise NotImplementedError()

    def get_test_config(self, id: str, type: int = None) -> dict:
        """Get the test configuration"""
        # params = {"type": type}
        raise NotImplementedError()

    def cancel_config_test(self, id: str) -> bool:
        """Cancel the running configuration test"""
        raise NotImplementedError()

    def debug_config_test(self, id: str) -> dict:
        """Debug the running config test"""
        raise NotImplementedError()

    def check_config(self, config: list) -> bool:
        """Check a configuration for errors"""
        raise NotImplementedError()

    """ EMAIL """

    def list_email_history(
        self,
        filter: str = None,
        offset: int = 0,
        limit: int = 5,
        sortby: str = None,
        total: bool = False,
    ) -> dict:
        """Get emails from history"""
        params = {
            "filter": filter,
            "offset": offset,
            "limit": limit,
            "total": str(total).lower(),
            "sortby": sortby,
        }
        return self._request("GET", "/email/history", params=params)

    def get_email(self, id: int) -> dict:
        """Get an email from history"""
        return self._request("GET", f"/email/history/{id}")["email"]

    """ LICENSE """

    def get_license(self) -> dict:
        """Get license information for the system"""
        return self._request("GET", "/license")

    def refresh_license(self) -> bool:
        """Refresh the license information"""
        return self._request("POST", "/license:refresh")

    def import_license_key(self, key: str) -> bool:
        """Import a license key (for offline use)"""
        payload = {"key": key}
        return self._request("PUT", "/license/key", payload=payload)

    """ STATS """

    def list_stats(
        self,
        name: str = None,
        namespace: str = None,
        legend: str = None,
        offset: int = 0,
        limit: int = 5,
    ) -> list:
        """List the stat entries"""
        params = {
            "filter[name]": name,
            "filter[namespace]": namespace,
            "filter[legend]": legend,
            "offset": offset,
            "limit": limit,
        }
        return self._request("GET", "/stats", params=params)

    def clear_stats(
        self, name: str = None, namespace: str = None, legend: str = None
    ) -> int:
        """Clear stat entries matched by filter. Returns number of accected stats"""
        params = {
            "filter[name]": name,
            "filter[namespace]": namespace,
            "filter[legend]": legend,
        }
        return self._request("DELETE", "/stats", params=params)["affected"]

    """ GRAPHS """

    def list_graphs(self, offset: str = 0, limit: str = 5) -> list:
        """List the graph databases"""
        params = {"offset": offset, "limit": limit}
        return self._request("GET", "/graphs", params=params)

    def export_graph(self, id: str) -> str:
        """Export a graph databases"""
        return self._request("GET", f"/graphs/{id}")["data"]

    def clear_graph(self, id: str) -> bool:
        """Clear a graph databases"""
        return self._request("DELETE", f"/graphs/{id}")

    """ SCRIPTS """

    def check_hsl_script(
        self, script: str, config: list, type: str, compat: int = None
    ) -> list:
        raise NotImplementedError()

    def run_hsl_script(
        self,
        script: str,
        config: list,
        preamble: str = None,
        postamble: str = None,
    ) -> str:
        raise NotImplementedError()

    def debug_hsl_script(self, id: str) -> dict:
        raise NotImplementedError()

    def get_hsl_include_graph(self, script: str, config: list, type: str) -> dict:
        raise NotImplementedError()
