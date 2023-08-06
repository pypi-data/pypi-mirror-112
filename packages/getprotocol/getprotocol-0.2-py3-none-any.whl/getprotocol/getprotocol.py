#!/usr/bin/python3

import requests
import sys
import argparse


class FindProtocol:
    '''
    Finds if the server has http or https protocol support
    and what we should use going forward with other tools
    '''

    def __init__(self, host, quiet):
        self.http = False
        self.https = False
        self.isHostDown = False

        self.host = host
        self.quiet = quiet


    def stripEveryThing(self):
        '''
        Return the stripped host with all http/https/www
        protocols removal

        >>> host = 'https://doesntevenexistlol.com'
        >>> finalHost = FindProtocol(host)
        >>>
        >>> 'https://' in finalHost.stripEveryThing()
        False
        '''

        self.host = self.host.replace('https://', '')
        self.host = self.host.replace('http://', '')
        self.host = self.host.replace('www.', '')
        self.host = self.host.replace('https://www.', '')
        self.host = self.host.replace('http://www.', '')

        self.host = self.host.split("/")[0]
        return(self.host)


    def getProtocol(self):
        '''
        See if the protocol is http or https and return it
        based on Location header in response (if it is)

        It also returns true if the host is down, let's say
        the host doesn't even exist?

        >>> host = 'https://doesntevenexistlol.com'
        >>> finalHost = FindProtocol(host)
        >>>
        >>> finalHost.getFinalURL()
        'HostDown'
        '''
        protocol    = ''
        hostname    = f"http://{self.stripEveryThing()}"

        try:
            response    = requests.get(hostname,
                allow_redirects = False,
                timeout = 1,
            )

            # print(response)
            # print(response.status_code)
            # print(response.headers)
            # print(response.text[:200])

            if 'Location' in response.headers:
                if 'https://' in response.headers['Location']:
                    protocol = 'https'

                else:
                    protocol = 'http'

            else:
                protocol = 'http'

            return(protocol)

        except requests.exceptions.ConnectionError:
            return(None)


    def getFinalURL(self):
        '''
        Returns 'HostDown' if the host doesn't exist or
        doesn't resolve and returns https://host.tld if
        the domain exists
        '''

        protocol    = self.getProtocol()

        if protocol != None:
            hostname    = self.stripEveryThing()
            url         = f"{protocol}://{hostname}"
            return(url)

        else:
            hostname    = self.stripEveryThing()
            
            if self.quiet != True:
                return(f'{hostname}:HostDownOrInvalid')


def addArguments():
    '''
    Args
    '''

    parser = argparse.ArgumentParser(description='')
    parser._optionals.title = "Basic Help"

    opts = parser.add_argument_group(f'Script Arguments')
    opts.add_argument('-t', '--target',  action="store",      dest="host",  default=False, help='Host to check protocol for')

    others = parser.add_argument_group(f'Optional Arguments')
    others.add_argument('-q', '--quiet', action="store_true", dest="quiet", default=False, help='To not print if host is down')

    args = parser.parse_args()
    return(args, parser)


def main():
    args, parser = addArguments()

    if args.host:
        host = args.host
        finalHost = FindProtocol(host, args.quiet)

        hostName  = finalHost.getFinalURL()
        print(hostName)

    elif not args.host:
        urls = []
        userInput = sys.stdin

        for lines in userInput:
            lines = lines.strip()
            if lines != "":
                urls.append(lines)

        for hosts in urls:
            finalHost = FindProtocol(hosts, args.quiet)
            hostName  = finalHost.getFinalURL()
            if hostName: print(hostName)

    else:
    	parser.print_help()
    	exit()


if __name__ == '__main__':
    main()
