__author__ = 'Parag Baxi <parag.baxi@gmail.com>'
__license__ = 'Apache License 2.0'

import lxml.objectify
from lxml.builder import E
import qualysapi


# Setup connection to QualysGuard API.
qgc = qualysapi.connect()
#
# API v1 call: Scan the New York & Las Vegas asset groups
# The call is our request's first parameter.
call = 'scan'
# The parameters to append to the url is our request's second parameter.
parameters = {'scan_title': 'Go big or go home', 'asset_groups': 'New York&Las Vegas', 'option': 'Initial+Options'}
# Note qualysapi will automatically convert spaces into plus signs for API v1 & v2.
# Let's call the API and store the result in xml_output.
xml_output = qgc.request(call, parameters)
#
# API v1 call: Print out all IPs associated with asset group "Looneyville Texas".
# Note that the question mark at the end is optional.
call = 'asset_group_list.php?'
# We can still use strings for the data (not recommended).
parameters = 'title=Looneyville Texas'
# The request returns a unicode string, let's convert it to a string.
xml_output = xml_output.encode('utf-8')
# Let's objectify the xml_output string.
root = lxml.objectify.fromstring(xml_output)
# Print out the IPs.
print root.ASSET_GROUP.SCANIPS.IP.text
# Prints out:
# 10.0.0.102
#
# API v2 call: Print out DNS name for a range of IPs.
call = '/api/2.0/fo/asset/host/'
parameters = {'action': 'list', 'ips': '10.0.0.10-10.0.0.11'}
xml_output = qgc.request(call, parameters).encode('utf-8')
root = lxml.objectify.fromstring(xml_output)
# Iterate hosts and print out DNS name.
for host in root.RESPONSE.HOST_LIST.HOST:
    print host.IP.text, host.DNS.text
# Prints out:
# 10.0.0.10 mydns1.qualys.com
# 10.0.0.11 mydns2.qualys.com
#
# API v3 WAS call: Print out number of webapps.
call = '/count/was/webapp'
# Note that this call does not have a payload so we don't send any data parameters.
xml_output = qgc.request(call).encode('utf-8')
root = lxml.objectify.fromstring(xml_output)
# Print out count of webapps.
print root.count.text
# Prints out:
# 89
#
# API v3 WAS call: Print out number of webapps containing title 'Supafly'.
call = '/count/was/webapp'
# We can send a string XML for the data.
parameters = '<ServiceRequest><filters><Criteria operator="CONTAINS" field="name">Supafly</Criteria></filters></ServiceRequest>'
xml_output = qgc.request(call, parameters).encode('utf-8')
root = lxml.objectify.fromstring(xml_output)
# Print out count of webapps.
print root.count.text
# Prints out:
# 3
#
# API v3 WAS call: Print out number of webapps containing title 'Lightsabertooth Tiger'.
call = '/count/was/webapp'
# We can also send an lxml.builder E object.
parameters = (
    E.ServiceRequest(
        E.filters(
            E.Criteria('Lightsabertooth Tiger', field='name',operator='CONTAINS'))))
xml_output = qgc.request(call, parameters).encode('utf-8')
root = lxml.objectify.fromstring(xml_output)
# Print out count of webapps.
print root.count.text
# Prints out:
# 0
# Too bad, because that is an awesome webapp name!
#
# API v3 Asset Management call: Count tags.
call = '/count/am/tag'
xml_output = qgc.request(call).encode('utf-8')
root = lxml.objectify.fromstring(xml_output)
# We can use XPATH to find the count.
print root.xpath('count')[0].text
# Prints out:
# 840
#
# API v3 Asset Management call: Find asset by name.
call = '/search/am/tag'
parameters = '''<ServiceRequest>
        <preferences>
            <limitResults>10</limitResults>
        </preferences>
        <filters>
            <Criteria field="name" operator="CONTAINS">PB</Criteria>
        </filters>
    </ServiceRequest>'''
xml_output = qgc.request(call, parameters).encode('utf-8')