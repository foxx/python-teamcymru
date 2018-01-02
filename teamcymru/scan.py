import socket
from ipaddress import ip_address


class IPToASN:

    CYMRU_WHOIS = 'whois.cymru.com'
    timeout = 45

    class ASNParseError(Exception):
        """
        An Exception for when the ASN parsing failed.
        """

    class ASNLookupError(Exception):
        """
        An Exception raised when ASN lookup fails
        """


    def __init__(self, ips=[], timeout=None):

        if timeout: # Socket's .settimeout takes care at validating this
            self.timeout = timeout

        # Validate and assign IP addresses
        self.ips = self._build_up_ip_addresses(ips)
        self.hits = 0

    def lookup(self, refresh=False):
        if refresh or not hasattr(self, '_cached_results'):
            response = self.scan()
            self._cached_results = self.parse_fields_whois(response)
            self.hits += 1
        return self._cached_results


    @property
    def ips_query_str(self):
        ips_str = '\r\n'.join([str(ip) for ip in self.ips])
        return """begin
verbose
%s
end\r\n""" % (ips_str, )


    def scan(self, retry_count=3):

        try:
            # Create the connection for the Cymru whois query.
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.settimeout(self.timeout)
            # log.debug('ASN query for {0}'.format(self.address_str))
            conn.connect((self.CYMRU_WHOIS, 43))

            # Query the Cymru whois server, and store the results.
            conn.send((self.ips_query_str).encode("utf-8"))

            data = ''
            while True:

                d = conn.recv(4096).decode()
                data += d

                if not d:
                    break
            conn.close()

            return str(data)

        except (socket.timeout, socket.error) as e:
            if retry_count > 0:
                return self.scan(retry_count - 1)
            else:
                raise self.ASNLookupError('ASN lookup failed.')

        except:
            raise self.ASNLookupError('ASN lookup failed.')


    def parse_fields_whois(self, response):
        """
        The function for parsing ASN fields from a whois response.
        Args:
            response (:obj:`str`): The response from the ASN whois server.
        Returns:
            A list of IPResult: The ASN lookup results
            ::
                {
                    'ip' (str) - The IP address itself
                    'asn' (str) - The Autonomous System Number
                    'asn_date' (str) - The ASN Allocation date
                    'asn_registry' (str) - The assigned ASN registry
                    'asn_cidr' (str) - The assigned ASN CIDR
                    'asn_country_code' (str) - The assigned ASN country code
                    'asn_description' (str) - The ASN description
                }
        Raises:
            ASNRegistryError: The ASN registry is not known.
            ASNParseError: ASN parsing failed.
        """

        try:
            result = []
            for linenumber, line in enumerate(response.splitlines()):
                if linenumber == 0:
                    continue

                if '|' not in line:
                    ip = self.ips[linenumber-1]
                    ip_result = IPResult(ip, error=line)
                    result.append(ip_result)
                    continue

                # Parse out the ASN information.
                temp = line.split('|')
                ret = {
                    'asn': temp[0].strip(),
                    'ip': temp[1].strip(),
                    'asn_cidr': temp[2].strip(),
                    'asn_country_code': temp[3].strip().upper(),
                    'asn_registry': temp[4].strip(),
                    'asn_date': temp[5].strip(),
                    'asn_description': temp[6].strip(),
                }

                result.append(IPResult(**ret))

        except Exception as e:
            raise self.ASNParseError('Parsing failed for "{0}" with exception: {1}.'
                                     ''.format(response, e)[:100])

        return result


    def _build_up_ip_addresses(self, ips):

        if not isinstance(ips, list):
            err = "IPs need to be a list, got %s object" % (type(ips).__name__, )
            raise ValueError(err)

        if len(ips) == 0:
            err = "You need to provide at least one IP address"
            raise ValueError(err)

        # Remove duplicates
        ips = list(set(ips))
        valid_ips = []

        for ip in ips:
            # let this raise the original ValueError exception in case on of the
            # IP addresses is not valid. It's fairly expressive and Pythonic.
            valid_ips.append(ip_address(ip))

        return valid_ips


class IPResult:

    def __init__(self, ip, asn=None, asn_cidr=None, asn_country_code=None,
                 asn_registry=None, asn_date=None, asn_description=None,
                 error=None):
        self.ip = ip
        self.asn = asn
        self.asn_cidr = asn_cidr
        self.asn_country_code = asn_country_code
        self.asn_registry = asn_registry
        self.asn_date = asn_date
        self.asn_description = asn_description
        self.error = error

    def has_error(self):
        return self.error is not None

    def __repr__(self):
        if self.error:
            return "<IP: %s, Has Error>" % (self.ip, )
        return "<IP: %s, ASN: %s>" % (self.ip, self.asn)
