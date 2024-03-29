DOMAIN_MAPPINGS = {
    'AL': '10YAL-KESH-----5',
    'AT': '10YAT-APG------L',
    'BA': '10YBA-JPCC-----D',
    'BE': '10YBE----------2',
    'BG': '10YCA-BULGARIA-R',
    'BY': '10Y1001A1001A51S',
    'CH': '10YCH-SWISSGRIDZ',
    'CZ': '10YCZ-CEPS-----N',
    'DE': '10Y1001A1001A83F',
    'DK': '10Y1001A1001A65H',
    'EE': '10Y1001A1001A39I',
    'ES': '10YES-REE------0',
    'FI': '10YFI-1--------U',
    'FR': '10YFR-RTE------C',
    'GB': '10YGB----------A',
    'GB-NIR': '10Y1001A1001A016',
    'GR': '10YGR-HTSO-----Y',
    'HR': '10YHR-HEP------M',
    'HU': '10YHU-MAVIR----U',
    'IE': '10YIE-1001A00010',
    'IT': '10YIT-GRTN-----B',
    'LT': '10YLT-1001A0008Q',
    'LU': '10YLU-CEGEDEL-NQ',
    'LV': '10YLV-1001A00074',
    # 'MD': 'MD',
    'ME': '10YCS-CG-TSO---S',
    'MK': '10YMK-MEPSO----8',
    'MT': '10Y1001A1001A93C',
    'NL': '10YNL----------L',
    'NO': '10YNO-0--------C',
    'PL': '10YPL-AREA-----S',
    'PT': '10YPT-REN------W',
    'RO': '10YRO-TEL------P',
    'RS': '10YCS-SERBIATSOV',
    'RU': '10Y1001A1001A49F',
    'RU-KGD': '10Y1001A1001A50U',
    'SE': '10YSE-1--------K',
    'SI': '10YSI-ELES-----O',
    'SK': '10YSK-SEPS-----K',
    'TR': '10YTR-TEIAS----W',
    'UA': '10YUA-WEPS-----0',
    'DE-AT-LU': '10Y1001A1001A63L',
    'DE-LU': '10Y1001A1001A82H'
}

BIDDING_ZONES = DOMAIN_MAPPINGS.copy()
BIDDING_ZONES.update({
    'DE': '10Y1001A1001A63L',  # DE-AT-LU
    'LU': '10Y1001A1001A63L',  # DE-AT-LU
    'DE-50HZ': '10YDE-VE-------2',
    'DE-AMPRION': '10YDE-RWENET---I',
    'DE-TENNET': '10YDE-EON------1',
    'DE-TRANSNET': '10YDE-ENBW-----N',
    'IT-NORD': '10Y1001A1001A73I',
    'IT-NORD-AT': '10Y1001A1001A80L',
    'IT-NORD-FR': '10Y1001A1001A81J',
    'IT-NORD-CH': '10Y1001A1001A68B',
    'IT-CNOR': '10Y1001A1001A70O',
    'IT-CSUD': '10Y1001A1001A71M',
    'IT-SUD': '10Y1001A1001A788',
    'IT-FOGN': '10Y1001A1001A72K',
    'IT-ROSN': '10Y1001A1001A77A',
    'IT-BRNN': '10Y1001A1001A699',
    'IT-PRGP': '10Y1001A1001A76C',
    'IT-SARD': '10Y1001A1001A74G',
    'IT-SICI': '10Y1001A1001A75E',
    'IT-GR': '10Y1001A1001A66F',
    'NO-1': '10YNO-1--------2',
    'NO-2': '10YNO-2--------T',
    'NO-3': '10YNO-3--------J',
    'NO-4': '10YNO-4--------9',
    'NO-5': '10Y1001A1001A48H',
    'SE-1': '10Y1001A1001A44P',
    'SE-2': '10Y1001A1001A45N',
    'SE-3': '10Y1001A1001A46L',
    'SE-4': '10Y1001A1001A47J',
    'DK-1': '10YDK-1--------W',
    'DK-2': '10YDK-2--------M',
    'IE-SEM': '10Y1001A1001A59C',
    'UA': '10Y1001C--00003F'
})

TIMEZONE_MAPPINGS = {
    'AL': 'Europe/Tirane',
    'AT': 'Europe/Vienna',
    'BA': 'Europe/Sarajevo',
    'BE': 'Europe/Brussels',
    'BG': 'Europe/Sofia',
    'BY': 'Europe/Minsk',
    'CH': 'Europe/Zurich',
    'CZ': 'Europe/Prague',
    'DE': 'Europe/Berlin',
    'DE-50HZ': 'Europe/Berlin',
    'DE-AMPRION': 'Europe/Berlin',
    'DE-TENNET': 'Europe/Berlin',
    'DE-TRANSNET': 'Europe/Berlin',
    'DE-LU': 'Europe/Berlin',
    'DK': 'Europe/Copenhagen',
    'EE': 'Europe/Tallinn',
    'ES': 'Europe/Madrid',
    'FI': 'Europe/Helsinki',
    'FR': 'Europe/Paris',
    'GB': 'Europe/London',
    'GB-NIR': 'Europe/Belfast',
    'GR': 'Europe/Athens',
    'HR': 'Europe/Zagreb',
    'HU': 'Europe/Budapest',
    'IE': 'Europe/Dublin',
    'IE-SEM': 'Europe/Dublin',
    'IT': 'Europe/Rome',
    'LT': 'Europe/Vilnius',
    'LU': 'Europe/Luxembourg',
    'LV': 'Europe/Riga',
    # 'MD': 'MD',
    'ME': 'Europe/Podgorica',
    'MK': 'Europe/Skopje',
    'MT': 'Europe/Malta',
    'NL': 'Europe/Amsterdam',
    'NO': 'Europe/Oslo',
    'PL': 'Europe/Warsaw',
    'PT': 'Europe/Lisbon',
    'RO': 'Europe/Bucharest',
    'RS': 'Europe/Belgrade',
    'RU': 'Europe/Moscow',
    'RU-KGD': 'Europe/Kaliningrad',
    'SE': 'Europe/Stockholm',
    'SI': 'Europe/Ljubljana',
    'SK': 'Europe/Bratislava',
    'TR': 'Europe/Istanbul',
    'UA': 'Europe/Kiev',
    'IT-NORD': 'Europe/Rome',
    'IT-CNOR': 'Europe/Rome',
    'IT-CSUD': 'Europe/Rome',
    'IT-SUD': 'Europe/Rome',
    'IT-FOGN': 'Europe/Rome',
    'IT-ROSN': 'Europe/Rome',
    'IT-BRNN': 'Europe/Rome',
    'IT-PRGP': 'Europe/Rome',
    'IT-SARD': 'Europe/Rome',
    'IT-SICI': 'Europe/Rome',
    'DE-AT-LU': 'Europe/Berlin',
    'NO-1': 'Europe/Oslo',
    'NO-2': 'Europe/Oslo',
    'NO-3': 'Europe/Oslo',
    'NO-4': 'Europe/Oslo',
    'NO-5': 'Europe/Oslo',
    'SE-1': 'Europe/Stockholm',
    'SE-2': 'Europe/Stockholm',
    'SE-3': 'Europe/Stockholm',
    'SE-4': 'Europe/Stockholm',
    'DK-1': 'Europe/Copenhagen',
    'DK-2': 'Europe/Copenhagen'
}

PSRTYPE_MAPPINGS = {
    'A03': 'Mixed',
    'A04': 'Generation',
    'A05': 'Load',
    'B01': 'Biomass',
    'B02': 'Fossil Brown coal/Lignite',
    'B03': 'Fossil Coal-derived gas',
    'B04': 'Fossil Gas',
    'B05': 'Fossil Hard coal',
    'B06': 'Fossil Oil',
    'B07': 'Fossil Oil shale',
    'B08': 'Fossil Peat',
    'B09': 'Geothermal',
    'B10': 'Hydro Pumped Storage',
    'B11': 'Hydro Run-of-river and poundage',
    'B12': 'Hydro Water Reservoir',
    'B13': 'Marine',
    'B14': 'Nuclear',
    'B15': 'Other renewable',
    'B16': 'Solar',
    'B17': 'Waste',
    'B18': 'Wind Offshore',
    'B19': 'Wind Onshore',
    'B20': 'Other',
    'B21': 'AC Link',
    'B22': 'DC Link',
    'B23': 'Substation',
    'B24': 'Transformer'}

DOCSTATUS = {'A05': 'Active', 'A09': 'Cancelled', 'A13': 'Withdrawn'}

BSNTYPE = {'A29': 'Already allocated capacity (AAC)',
           'A43': 'Requested capacity (without price)',
           'A46': 'System Operator redispatching',
           'A53': 'Planned maintenance',
           'A54': 'Unplanned outage',
           'A85': 'Internal redispatch',
           'A95': 'Frequency containment reserve',
           'A96': 'Automatic frequency restoration reserve',
           'A97': 'Manual frequency restoration reserve',
           'A98': 'Replacement reserve',
           'B01': 'Interconnector network evolution',
           'B02': 'Interconnector network dismantling',
           'B03': 'Counter trade',
           'B04': 'Congestion costs',
           'B05': 'Capacity allocated (including price)',
           'B07': 'Auction revenue',
           'B08': 'Total nominated capacity',
           'B09': 'Net position',
           'B10': 'Congestion income',
           'B11': 'Production unit'}

MARKETAGREEMENTTYPE = {'A01':'Daily',
                       'A02':'Weekly',
                       'A03':'Monthly',
                       'A04':'Yearly',
                       'A05':'Total',
                       'A06':'Long term',
                       'A07':'Intraday',
                       'A13':'Hourly'}

DOCUMENTTYPE = {'A09': 'Finalised schedule',
                'A11': 'Aggregated energy data report',
                'A25': 'Allocation result document',
                'A26': 'Capacity document',
                'A31': 'Agreed capacity',
                'A44': 'Price Document',
                'A61': 'Estimated Net Transfer Capacity',
                'A63': 'Redispatch notice',
                'A65': 'System total load',
                'A68': 'Installed generation per type',
                'A69': 'Wind and solar forecast',
                'A70': 'Load forecast margin',
                'A71': 'Generation forecast',
                'A72': 'Reservoir filling information',
                'A73': 'Actual generation',
                'A74': 'Wind and solar generation',
                'A75': 'Actual generation per type',
                'A76': 'Load unavailability',
                'A77': 'Production unavailability',
                'A78': 'Transmission unavailability',
                'A79': 'Offshore grid infrastructure unavailability',
                'A80': 'Generation unavailability',
                'A81': 'Contracted reserves',
                'A82': 'Accepted offers',
                'A83': 'Activated balancing quantities',
                'A84': 'Activated balancing prices',
                'A85': 'Imbalance prices',
                'A86': 'Imbalance volume',
                'A87': 'Financial situation',
                'A88': 'Cross border balancing',
                'A89': 'Contracted reserve prices',
                'A90': 'Interconnection network expansion',
                'A91': 'Counter trade notice',
                'A92': 'Congestion costs',
                'A93': 'DC link capacity',
                'A94': 'Non EU allocations',
                'A95': 'Configuration document',
                'B11': 'Flow-based allocations'}

# neighbouring bidding zones that have cross-border flows
NEIGHBOURS = {
    'BE': ['NL', 'DE-AT-LU', 'FR', 'GB', 'DE-LU'],
    'NL': ['BE', 'DE-AT-LU', 'DE-LU', 'GB', 'NO-2'],
    'DE-AT-LU': ['BE', 'CH', 'CZ', 'DK-1', 'DK-2', 'FR', 'IT-NORD', 'IT-NORD-AT', 'NL', 'PL', 'SE-4', 'SI'],
    'FR': ['BE', 'CH', 'DE-AT-LU', 'DE-LU', 'ES', 'GB', 'IT-NORD', 'IT-NORD-FR'],
    'CH': ['AT', 'DE-AT-LU', 'DE-LU', 'FR', 'IT-NORD', 'IT-NORD-CH'],
    'AT': ['CH', 'CZ', 'DE-LU', 'HU', 'IT-NORD', 'SI'],
    'CZ': ['AT', 'DE-AT-LU', 'DE-LU', 'PL', 'SK'],
    'GB': ['BE', 'FR', 'IE-SEM', 'NL'],
    'NO-2': ['DK-1', 'NL', 'NO-5'],
    'HU': ['AT', 'HR', 'RO', 'RS', 'SK', 'UA'],
    'IT-NORD': ['CH', 'DE-AT-LU', 'FR', 'SI', 'AT', 'IT-CNOR'],
    'ES': ['FR', 'PT'],
    'SI': ['AT', 'DE-AT-LU', 'HR', 'IT-NORD'],
    'RS': ['AL', 'BA', 'BG', 'HR', 'HU', 'ME', 'MK', 'RO'],
    'PL': ['CZ', 'DE-AT-LU', 'DE-LU', 'LT', 'SE-4', 'SK', 'UA'],
    'ME': ['AL', 'BA', 'RS'],
    'DK-1': ['DE-AT-LU', 'DE-LU', 'DK-2', 'NO-2', 'SE-3'],
    'RO': ['BG', 'HU', 'RS', 'UA'],
    'LT': ['BY', 'LV', 'PL', 'RU-KGD', 'SE-4'],
    'BG': ['GR', 'MK', 'RO', 'RS', 'TR'],
    'SE-3': ['DK-1', 'FI', 'NO-1', 'SE-4'],
    'LV': ['EE', 'LT', 'RU'],
    'IE-SEM': ['GB'],
    'BA': ['HR', 'ME', 'RS'],
    'NO-1': ['NO-2', 'NO-3', 'NO-5', 'SE-3'],
    'SE-4': ['DE-AT-LU', 'DE-LU', 'DK-2', 'LT', 'PL'],
    'NO-5': ['NO-1', 'NO-2', 'NO-3'],
    'SK': ['CZ', 'HU', 'PL', 'UA'],
    'EE': ['FI', 'LV', 'RU'],
    'DK-2': ['DE-AT-LU', 'DE-LU', 'SE-4'],
    'FI': ['EE', 'NO-4', 'RU', 'SE-1', 'SE-3'],
    'NO-4': ['SE-2', 'FI', 'SE-1'],
    'SE-1': ['FI', 'NO-4', 'SE-2'],
    'SE-2': ['NO-3', 'NO-4', 'SE-3'],
    'DE-LU': ['AT', 'BE', 'CH', 'CZ', 'DK-1', 'DK-2', 'FR', 'NL', 'PL', 'SE-4'],
    'MK': ['BG', 'GR', 'RS'],
    'PT': ['ES'],
    'GR': ['AL', 'BG', 'IT-BRNN', 'IT-GR', 'MK', 'TR'],
    'NO-3': ['NO-4', 'NO-5', 'SE-2'],
    'IT':['AT', 'FR', 'GR', 'MT', 'ME', 'SI', 'CH'],
    'IT-BRNN': ['GR', 'IT-SUD'],
    'IT-SUD': ['IT-BRNN', 'IT-CSUD', 'IT-FOGN', 'IT-ROSN'],
    'IT-FOGN': ['IT-SUD'],
    'IT-ROSN': ['IT-SICI', 'IT-SUD'],
    'IT-CSUD': ['IT-CNOR', 'IT-SARD', 'IT-SUD'],
    'IT-CNOR': ['IT-NORD', 'IT-CSUD', 'IT-SARD'],
    'IT-SARD': ['IT-CNOR', 'IT-CSUD'],
    'IT-SICI': ['IT-ROSN', 'MT'],
    'MT': ['IT-SICI']
}
