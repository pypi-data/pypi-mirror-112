## ArchFinder - mirrorlist builder
A script that writes a mirrolist of Arch Linux mirrors, according with your preferences, e.g. countries, delay, sync time and protocols (https, ipv4...). This project was made just for learning purposes.  


### Dependencies
* [pip](https://pip.pypa.io/en/stable/)
* [urllib3](https://urllib3.readthedocs.io/en/latest/index.html)


### Installation
    pip install archfinder


### Usage
#### - API
    # Example

    # Creates a pool that keeps track one connection 
    fetcher = MirrorsFetcher()
    
    # Downloads json file containing all mirrors and decodes it
    mirrors = fetcher.parseJsonMirrors()
    
    # Filter by protocols, countries...
    filter = Filter(mirrors)
    filter.filterByHttps()
    filter.filterByLocation(["Portugal", "SpAiN", "US"])
    mirrors = filter.mirrors
    
    # Sort mirrors by delay or sync time...
    sort = Sort(mirrors)
    sort.sortByDelay()
    mirrors = sort.mirrors

    # Writes the mirrorlist and stores in the current directory
    writer = MirrorlistWriter(changer.mirrors)
    writer.writeMirrorlist(writeNormal=True)

#### - Command line
    archsfinder [ARGS...]

or

    python -m archfinder [ARGS...]


### Arguments
    -h, --help            
    Show this help message and exit
    
    -p <protocol>, --protocol <protocol>
    Specifies the protocol used [ http | https | rsync]
    
    -l <name or code>, --location <name or code>
    Indicates the countries (by name or code) where each mirror 
    resides. If more than one is passed, you should write with 
    commas without spaces: Germany,Spain. Furthermore, if some 
    country has two or more names, you must write the list inside 
    quotation marks: "Portugal,United States".
    
    -i <ipv>, --internet-protocol <ipv>
    Specifies which internet protocol version is used 
    by each mirror [ipv4 | ipv6 | ipv4,ipv6]    
    
    -o, --isos            
    Searches for mirrors with ISOs
  
    -d, --delay           
    Sort by average mirroring delay
  
    -a, --duration-average
    Sort by duration average it took to connect 
    and retrieve the last_sync file from url
    
    -s, --duration-standard
    Sort by the lowest standard deviation of the 
    connect and retrieval time
  
    -g, --group-by-country
    Group mirrors by country
  
    -n <value>, --number-of-mirrors <value>
    The max number of mirrors (> 0) to write in the mirrorlist

    -t <hour>, --time-distance <hour>
    Filters by elapsed time range (1..24) between the current 
    and the last mirror sync (current - sync < range). This 
    operation ignores mirrors whose synchronization has more 
    than one day. Also the ones that doens't contain any info 
    about last sync (empty string) are placed last

    -v, --version         
    Show program's version number and exit


### Notes of usage
#### - Through the command line
* You can only choose a sort method;
* Grouping by countries is a type of sort method.


### Changes 
#### 0.0.1 (13-7-2021)
* First release.