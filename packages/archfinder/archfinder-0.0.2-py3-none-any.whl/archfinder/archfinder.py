r'''
archfinder permits to write a mirrorlist of Arch Linux database.

Copyright (C) 2021 Francisco Braço-Forte f.s.f.b2001@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

#!/usr/bin/env python3

import sys
import json
import os
from typing import (
    Any, Callable, Dict, List, Tuple, Union
) 
import urllib3
from argparse import ArgumentParser
import time
from io import TextIOWrapper
import re

AUTHOR  = 'Francisco Braço-Forte'
VERSION = '0.0.2'

# Json File containing all Arch Linux mirrors.
MIRRORS_STATUS_URL = 'https://archlinux.org/mirrors/status/json/'

# Default name of mirrorlist.
FILE_NAME = 'mirrorlist'

# Identifiers of each information about 
# a mirror used in the json file.
URLS         = 'urls'
ACTIVE       = 'active'
PROTOCOL     = 'protocol'
HTTP         = 'http'
HTTPS        = 'https'
RSYNC        = 'rsync'
COUNTRY      = 'country'
COUNTRY_CODE = 'country_code'
DELAY        = 'delay'
DURATION_AVG = 'duration_avg'
DURATION_STD = 'duration_stddev'
IPV4         = 'ipv4'
IPV6         = 'ipv6'
LAST_SYNC    = 'last_sync'
ISOS         = 'isos'
URL          = 'url'

# Identifiers of each option flag.
PROTO             = 'protocol'
LOCATION          = 'location'
GROUP_BY_COUNTRY  = 'group_by_country'
IPV               = 'internet_protocol'
ISOS_FILES        = 'isos'
DELAY_TIME        = 'delay'
DURATION_AVERAGE  = 'duration_average'
DURATION_STANDARD = 'duration_standard'
NUMBER_OF_MIRRORS = 'number_of_mirrors'
TIME_PASSED       = 'time_passed'

# Specifies the write mode.
WRITE_NORMAL    = True
WRITE_COUNTRIES = False

# Auxiliar constant used to calculate 
# the elapsed time.
ONE_DAY_IN_SECS = 24 * 3600

# Identifiers of each sorting method.
DEL     = 0b1000
AVG     = 0b0100
STD     = 0b0010
GROUP   = 0b0001

class MirrorsFetcher:
    r'''
    Responsable of download json mirrors file and
    convert into a list of mirrors.

    :param customHeaders: 
        Just in case you don't want to use the
        pre-defined by PoolManager class.
    '''
    def __init__(self, customHeaders: Dict[str, Any] = None):
        self._pool = urllib3.PoolManager(num_pools=1, headers=customHeaders)

    def parseJsonMirrors(self) -> List[Dict[str, Union[int, str, float, bool]]]:
        r'''
        Downloads and parses the file to a list of dictionaries.
        Only reaturns activated mirrors
        '''
        request = self._pool.request('GET', MIRRORS_STATUS_URL)
        if request.status != 200:
            sys.exit('While requesting json file: '
                     'HTTP response status code {0}'.format(request.status)
            )        
        fileDecoded = request.data.decode(encoding='utf-8')
        try:
            mirrors = json.loads(fileDecoded)[URLS]
        except json.JSONDecodeError as error:
            sys.exit('While parsing json file: {0}'.format(error.msg))
        finally:
            self._pool.clear()
        return list(filter(lambda mirror: mirror[ACTIVE], mirrors))

class MirrorsManipulator:
    r'''
    Abstart class responsable of holding 
    the mirrors list used by Filter and
    Sorter 
    '''
    def __init__(self, mirrors: List[Dict[str, Union[int, str, float, bool]]]):
        self._mirrors = mirrors
    
    @property
    def mirrors(self) -> Union[List[Dict[str, Union[int, str, float, bool]]], filter]:
        r'''
        Returns the current list or filter of mirrors.
        '''
        return self._mirrors

    def decreaseList(self, limit: int) -> None:
        r'''
        Limits the number of mirrors.

        :precondition: 
            limits is not None and limit > 0

        :param limit: 
            max number of mirrors to maintain.
        '''
        if isinstance(self.mirrors, filter):
            self._mirrors = list(self._mirrors)
        self._mirrors = self._mirrors[:limit]

class Filter(MirrorsManipulator):
    r'''
    Offers a collection of options capable 
    of select the intended mirrors by their 
    characteristics.
    '''
    def __init__(self, mirrors: List[Dict[str, Union[int, str, float, bool]]]):
        super().__init__(mirrors)

    def fetchLocations(self) -> Tuple[Dict[str, None], Dict[str, None]]:
        r'''
        Groups all possible locations by contries 
        and their codes. Country name and its code
        are lowered so makes easy to compare with
        the list of countries choosen by the user.  
        '''
        if not isinstance(self.mirrors, list):
            raise TypeError('On fetchLocations function: self.mirrors isn\'t a list')
        countries = {}
        codes     = {}
        for mirror in self.mirrors:
            countries[mirror[COUNTRY].lower()]  = None
            codes[mirror[COUNTRY_CODE].lower()] = None
        return countries, codes

    def _filterByProtocol(self, protocol: str) -> None:
        r'''
        Filters the mirrors by the specified protocol.

        :precondition:
            protocol is not None

        :param protocol:
            pretended scheme.
        '''
        self._mirrors = filter(
            lambda mirror: mirror[PROTOCOL] == protocol, 
            self._mirrors
        )

    def filterByHttp(self) -> None:
        r'''
        Filters the mirrors by HTTP protocol.
        '''
        self._filterByProtocol(HTTP)

    def filterByHttps(self) -> None:
        r'''
        Filters the mirrors by HTTPS protocol.
        '''
        self._filterByProtocol(HTTPS)

    def filterByRsync(self) -> None:
        r'''
        Filters the mirrors by RSYNC protocol.
        '''
        self._filterByProtocol(RSYNC)

    def filterByLocation(self, locations: List[str]) -> None:
        r'''
        Filters the mirrors by a specified list of
        countries or respetive code (can be mixed).

        :precondition:
            locations is not None

        :param locations: 
            countries/codes.
        '''
        # Ensures that are in lower case and converts
        # into a dict so speeds up the search
        locations = {l.lower() : None for l in locations}
        self._mirrors = filter(
            lambda mirror: mirror[COUNTRY].lower() in locations or \
                           mirror[COUNTRY_CODE].lower() in locations,
            self._mirrors
        )

    def _filterByIPv(self, ipvSearcher: Callable[[Dict[str, Any]], bool]) -> None:
        r'''
        Filters the mirrors that support a certain 
        internet protocol.

        :precondition:
            ipvSearcher is not None

        :param ipvSearcher: protocol fetcher
        '''
        self._mirrors = filter(ipvSearcher, self._mirrors)

    def filterByIPv4(self) -> None:
        r'''
        Filters the mirrors that supports IPv4.
        '''
        self._filterByIPv(lambda mirror: mirror[IPV4])

    def filterByIPv6(self) -> None:
        r'''
        Filters the mirrors that supports IPv6.
        '''
        self._filterByIPv(lambda mirror: mirror[IPV6])

    def filterByIPv4andIPv6(self) -> None:
        r'''
        Filters the mirrors that supports IPv4 and IPv6.
        '''
        self._filterByIPv(
            lambda mirror: mirror[IPV4] and mirror[IPV6]
        )

    def filterByISOs(self) -> None:
        r'''
        Filters the mirrors that have ISO's.
        '''
        self._mirrors = filter(
            lambda mirror : mirror[ISOS], 
            self._mirrors
        )

    def _checkMirrorSync(self, mirror: Dict[str, Any], timeLimit: int) -> bool:
        r'''
        Checks the last time that the mirror was synced and 
        evaluates the time elapsed until now, according the 
        defined limit. Mirrors with an undated synchronization
        in the current month or year will be discarded as well 
        as those that have more than one day apart.

        :precondition:
            mirror is not None and    \
            timeLimit is not None and \
            0 <= timeLimit <= 24 and  \ 
            inSeconds(timeLimit)

        :param mirror:
            Mirror to assess.

        :param timeLimit:
            Amplitude.
        '''
        mirrorDateTime = mirror[LAST_SYNC]
        if mirrorDateTime is None: 
            return False
        # Each sync date has the following format:
        # Y - year 
        # M - month
        # D - day
        #
        # h - hour 
        # m - minute 
        # s - second
        #
        # Y-M-DTh:m:sZ 
        # T and Z are arbitrary chars. 
        # I think that means TimeZone
        # 
        # e.g. 
        # 12-3-2021T23:13:56Z
        syncDate, syncTime = mirrorDateTime.split('T')
        year, month, day = map(int, syncDate.split('-'))
        hour, minute, second = map(int, syncTime[:-1].split(':'))
        currentTime = time.localtime(time.time())
        if currentTime.tm_mon != month or currentTime.tm_year != year:
            return False
        numDays = currentTime.tm_mday - day
        if numDays > 1:
            return False
        syncTimeInSecs = (hour * 3600) + \
                         (minute * 60) + \
                          second
        currTimeInSecs = (currentTime.tm_hour * 3600) + \
                         (currentTime.tm_min * 60) + \
                          currentTime.tm_sec
        if numDays == 1: 
            return currTimeInSecs + (ONE_DAY_IN_SECS - syncTimeInSecs) <= timeLimit 
        else:
            # Zero days have passed
            return currTimeInSecs - syncTimeInSecs <= timeLimit

    def filterByTimeSync(self, amplitude: int) -> None:
        r'''
        Filters the mirrors by last synced time, according 
        with the amplitude. 

        :precondition:
            amplitude is not None

        :param amplitude:
            Time bound.
        '''
        # Calculus on _checkMirrorSync are made in seconds
        amplitude *= 3600
        self._mirrors = (
            mirror for mirror in self._mirrors 
                        if self._checkMirrorSync(mirror, amplitude)
        )

class Sort(MirrorsManipulator):
    r'''
    Sorts the mirrors as you want based on 
    "time metrics". Some insights about 
    these values were taken from:
    https://archlinux.org/mirrors/status/
    '''
    def __init__(self, mirrors: List[Dict[str, Union[int, str, float, bool]]]):
        super().__init__(mirrors)

    def _sortByMetric(self, param: str) -> None:
        r'''
        Sorts the mirrors in ascending order.

        :precondition:
            param is not None

        :param param:
            Pretended parameter.
        '''
        getKey = lambda mirror: p if (p := mirror[param]) is not None \
                                  else -1.0
        self._mirrors = sorted(
            self._mirrors, 
            key=getKey,
            reverse=False
        )

    def sortByDelay(self) -> None:
        r'''
        Sorts the mirrors by delay time (last_check - last_sync).
        '''
        self._sortByMetric(DELAY)

    def sortByDurationAvg(self) -> None:
        r'''
        Sorts the mirrors by average delay. That is, the 
        time it took to connect and retrieve the last_sync 
        from the mirror. This value depends on your current 
        geolocation.
        '''
        self._sortByMetric(DURATION_AVG)

    def sortByDurationStd(self) -> None:
        r'''
        Sorts the mirrors by standard deviation of the connect 
        and retrieval time. A high standard deviation can 
        indicate an unstable or overloaded mirror.
        '''
        self._sortByMetric(DURATION_STD)

    def groupByCountries(self) -> None:
        r'''
        Sorts by countries name (i.e. grouped) in ascending order. 
        Some locations doesn't have the country specified, meaning 
        that is just an empty string, so them appears in first 
        place on the list.
        '''
        getKey = lambda mirror: mirror[COUNTRY]
        self._mirrors = sorted(
            self._mirrors, 
            key=getKey, 
            reverse=False
        )

class ArgumentsManager:
    r'''
    Holds all arguments in order to manipulate
    the mirrorlist.
    '''
    def __init__(self):
        self._args = ArgumentParser(
            usage='{0} [ARGS ...]'.format(sys.argv[0]),
            description='Generates a mirrorlist of Arch Linux packages database'
        )

    def buildArguments(self) -> None:
        r'''
        Generates each argument.
        '''
        sortGroup = self._args.add_mutually_exclusive_group(required=False)
        self._args.add_argument(
            '-p', '--protocol',
            dest=PROTO,
            action='store', 
            type=str,
            default=HTTPS,
            choices=[HTTP, HTTPS, RSYNC],
            metavar='<protocol>',
            required=False,
            help='Specifies the protocol used [ {0} | {1} | {2}]'.format(HTTP, HTTPS, RSYNC)
        )
        self._args.add_argument(
            '-l', '--location',
            dest=LOCATION,
            action='store',
            type=str,
            metavar='<name or code>',
            required=False,
            help='Indicates the countries (by name or code) where each mirror resides. '
                 'If more than one is passed, you should write with commas without ' 
                 'spaces: Germany,Spain. Furthermore, if some country has two or more names, '
                 'you must write the list inside quotation marks: "Portugal,United States".')
        self._args.add_argument(
            '-i', '--internet-protocol',
            dest=IPV,
            action='store',
            type=str,
            default=IPV4,
            choices=[IPV4, IPV6, IPV4 + ',' + IPV6],
            metavar='<ipv>',
            required=False,
            help='Specifies which internet protocol version is used [ipv4 | ipv6 | ipv4,ipv6]'
        )
        self._args.add_argument(
            '-o', '--isos',
            dest=ISOS_FILES,
            action='store_true',
            help='Searches for mirrors with ISOs'
        )
        sortGroup.add_argument(
            '-d', '--delay',
            dest=DELAY_TIME,
            action='store_true',
            help='Sort by average mirroring delay'
        )
        sortGroup.add_argument(
            '-a', '--duration-average',
            dest=DURATION_AVERAGE,
            action='store_true',
            help='Sort by duration average it took to connect and retrieve '
                 'the last_sync file from url'
        )
        sortGroup.add_argument(
            '-s', '--duration-standard',
            dest=DURATION_STANDARD,
            action='store_true',
            help='Sort by the lowest standard deviation of the '
                 'connect and retrieval time'
        )
        sortGroup.add_argument(
            '-g', '--group-by-country',
            dest=GROUP_BY_COUNTRY,
            action='store_true',
            help='Group mirrors by country'
        )
        self._args.add_argument(
            '-n', '--number-of-mirrors',
            dest=NUMBER_OF_MIRRORS,
            action='store',
            type=int,
            metavar='<value>',
            required=False,
            help='The max number of mirrors (> 0) to write in the mirrorlist'
        )
        self._args.add_argument(
            '-t', '--time-distance',
            dest=TIME_PASSED,
            action='store',
            type=int,
            choices=range(1, 25),
            metavar='<hour>',
            required=False,
            help='Filters by elapsed time range (1..24) between the current '
                 'and the last mirror sync (current - sync < range). This '
                 'operation ignores mirrors whose synchronization has more '
                 'than one day. Also the ones that doens\'t contain any ' 
                 'info about last sync (empty string) are placed last'
        )
        self._args.add_argument(
            '-v', '--version',
            action='version',
            version='{0} {1}'.format(sys.argv[0], VERSION)
        )

    def _selectLocations(self, locations: str, mirrorsFilter: Filter) -> None:
        r'''
        Evaluates syntactically and selects the countries 
        (or respective codes) that were choosed.
        
        e.g.
        France,United States,PT
        '''
        e = re.compile(
            r'^([a-zA-Z]{1,}( [a-zA-Z]{1,})*)(,[a-zA-Z]{1,}( [a-zA-Z]{1,})*)*$'
        )
        if not e.match(locations):
            self._args.exit(
                1, 
                'usage: {0}\n'
                '{1} error: invalid countries list: {2}\n'.format(self._args.usage,
                                                                  sys.argv[0],
                                                                  locations)
            )
        locs = []
        countries, codes = mirrorsFilter.fetchLocations()
        for location in locations.split(','):
            lloc = location.lower()
            if lloc in countries or lloc in codes:
                locs.append(lloc)
            else:
                self._args.exit(
                    1, 
                    'usage: {0}\n'
                    '{1} error: unrecognized country: {2}\n'.format(self._args.usage, 
                                                                    sys.argv[0], 
                                                                    location)
                )
        mirrorsFilter.filterByLocation(locs)
    
    def _defineSyncAmplitude(self, timeDist : int, mirrorsFilter: Filter): 
        r'''
        Selects the mirrors that were updated in 
        the past timeDist hours (between 1 and 24 hours)
        '''   
        mirrorsFilter.filterByTimeSync(timeDist)

    def _chooseProtocol(self, protocol: str, mirrorsFilter: Filter) -> None:
        r'''
        Chooses the preferred protocol.
        '''
        if protocol == HTTP:
            mirrorsFilter.filterByHttp()
        elif protocol == HTTPS:
            mirrorsFilter.filterByHttps()
        else:
            mirrorsFilter.filterByRsync()

    def _chooseIPv(self, ipv: str, mirrorsFilter: Filter) -> None:
        r'''
        Selects mirrors with the specified
        internet protocol.
        '''
        if ipv == IPV4:
            mirrorsFilter.filterByIPv4()
        elif ipv == IPV6:
            mirrorsFilter.filterByIPv6()
        else:
            mirrorsFilter.filterByIPv4andIPv6()

    def _chooseWithISOs(self, mirrorsFilter: Filter) -> None:
        r'''
        Selects mirrors with ISO files.
        '''
        mirrorsFilter.filterByISOs()

    def _chooseSortingMethod(self, option: int, mirrorsSort: Sort) -> None:
        r'''
        Selects the way how mirrors are ordered.
        If will sort by country name so the
        write mode changes.

        :param option:
            Sort method described by 4 bits.
            (Left most)
            1º - Delay;
            2º - Average;
            3º - Standard;
            4º - Grouping.
            All zero means Delay by default.

        :returns the write mode.
        '''
        {
            DEL   : mirrorsSort.sortByDelay,
            AVG   : mirrorsSort.sortByDurationAvg,
            STD   : mirrorsSort.sortByDurationStd,
            GROUP : mirrorsSort.groupByCountries,
        }.get(option, mirrorsSort.sortByDelay)()
        return WRITE_NORMAL if option != GROUP \
                            else WRITE_COUNTRIES

    def _limitMirrorsNum(self, limit : int, mirrorsSort: Sort) -> None:
        r'''
        Restricts the max number of mirrors.
        '''
        if limit < 1:
            self._args.exit(
                1,
                'usage: {0}\n'
                '{1}: error: argument -n/--number-of-mirrors: '
                'invalid choice: {2} (choose a number >= 1)\n'.format(self._args.usage,
                                                                      sys.argv[0],
                                                                      limit
                )
            ) 
        mirrorsSort.decreaseMirrorList(limit)

    def analizeArguments(self, 
                         mirrors: List[Dict[str, Union[int, str, float, bool]]]
    ) -> Tuple[bool, List[Dict[str, Union[int, str, float, bool]]]]:
        r'''
        Parses the arguments and changes the mirrorlist
        depending on the arguments.

        :returns the write mode.
        '''
        parsedArgs = vars(self._args.parse_args(sys.argv[1:]))
        if parsedArgs[NUMBER_OF_MIRRORS] is not None and parsedArgs[GROUP_BY_COUNTRY]:
            self._args.exit(
                1,
                'usage {0}\n' 
                '{1} error: argument -n/--number-of-mirrors: not allowed '
                'with argument -g/--group-by-country\n'.format(self._args.usage, 
                                                               sys.argv[0]
                )
            )
        mirrorsFilter = Filter(mirrors)
        if parsedArgs[LOCATION]:
            self._selectLocations(parsedArgs[LOCATION], mirrorsFilter)
        if parsedArgs[TIME_PASSED] is not None:
            self._defineSyncAmplitude(parsedArgs[TIME_PASSED], mirrorsFilter)
        self._chooseProtocol(parsedArgs[PROTO], mirrorsFilter)
        self._chooseIPv(parsedArgs[IPV], mirrorsFilter)
        if parsedArgs[ISOS_FILES]:
            self._chooseWithISOs(mirrorsFilter)
        mirrors = mirrorsFilter.mirrors
        mirrorsSort = Sort(mirrors)
        sortingOption = (parsedArgs[DELAY_TIME]        << 3) | \
                        (parsedArgs[DURATION_AVERAGE]  << 2) | \
                        (parsedArgs[DURATION_STANDARD] << 1) | \
                         parsedArgs[GROUP_BY_COUNTRY]      
        writeMode = self._chooseSortingMethod(sortingOption, mirrorsSort)
        if parsedArgs[NUMBER_OF_MIRRORS] is not None:
            self._limitMirrorsNum(parsedArgs[NUMBER_OF_MIRRORS], mirrorsSort)
        mirrors = mirrorsSort.mirrors
        return writeMode, mirrors

class MirrorlistWriter:
    r'''
    Creates a mirrorlist based on a 
    list of mirrors.
    '''
    def __init__(self):
        pass
    
    def _writeBlocksByCountry(self, 
                              file: TextIOWrapper, 
                              mirrors: List[Dict[str, Union[int, str, float, bool]]]
    ) -> None:
        r'''
        Writes the mirrorlist by countries.

        e.g.

        ## United Kingdom
        Server = https://ftp.helloworld.uk
        Server = http://nothing.com

        (...)
        ## Portugal
        Server = http://lol.pt
        
        (...)
        '''
        if len(mirrors) == 0:
            return
        countryBlock = mirrors[0][COUNTRY]
        file.write('## {0}\n'.format(
            countryBlock if countryBlock != ''
                         else 'Unknow location')
        )
        for mirror in mirrors:
            if (country := mirror[COUNTRY]) != countryBlock:
                countryBlock = country
                file.write('\n## {0}\n'.format(countryBlock))
            file.write('#Server = {0}\n'.format(mirror[URL]))

    def _writeNormal(self, 
                     file: TextIOWrapper, 
                     mirrors: List[Dict[str, Union[int, str, float, bool]]]
    ) -> None:
        r'''
        Writes mirror by mirror normally.

        e.g.

        Server = https://ftp.helloworld.uk
        Server = http://nothing.com
        (...)
        '''
        for mirror in mirrors:
            file.write('#Server = {0}\n'.format(mirror[URL]))

    def writeMirrorlist(self, 
                        writeNormal: bool, 
                        mirrors: List[Dict[str, Union[int, str, float, bool]]]
    ) -> None:
        r'''
        Writes normally the mirrorlist.
        '''
        if os.path.exists(FILE_NAME):
            print(
                'Already exists a file with the '
                'name "{0}" in the current dir!'.format(FILE_NAME)
            )
            response = input('Do you want to rewrite it? [Y/N] ').upper()
            if response == 'Y' or response == '':
                pass
            elif response == 'N': 
                sys.exit('Exited!')
            else: 
                sys.exit('Invalid option passed!')
        with open(FILE_NAME, 'w') as file:
            tformat = time.strftime('%Y-%m-%d | %H:%M:%S', time.localtime())
            file.write(
                '## Arch Linux Mirrorlist\n'
                '## Last update: {0}\n\n'.format(tformat)
            )
            if writeNormal:
                self._writeNormal(file, mirrors)
            else:
                self._writeBlocksByCountry(file, mirrors)

def main() -> None:
    args = ArgumentsManager()
    args.buildArguments()
    handler = MirrorsFetcher()
    mirrors = handler.parseJsonMirrors()
    writeMode, mirrors = args.analizeArguments(mirrors)
    writer = MirrorlistWriter()
    writer.writeMirrorlist(writeMode, mirrors)

if __name__ == '__main__':
    main()