#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import logging, ssl, httplib, urllib, json
from base64 import b64encode
from bin.main.rally.BuildBatch import BuildBatch
from main.resources.rally.FetchReference import FetchReference

logger = logging.getLogger(__name__)
logger.debug("In Update Object")

baseURL = '/slm/webservice/v2.0/'

isFeature = 'F' in formattedID

userAndPass = b64encode(b"%s:%s")%(configuration.userName, configuration.password)

values = []
query = FetchReference(userAndPass, configuration.url)

conn = httplib.HTTPSConnection(configuration.url,"443",context=ssl._create_unverified_context())
headers = {'Authorization' : 'Basic %s' %userAndPass}

curURL =  baseURL + '/portfolioitem/feature?fetch=FormattedID&query=(FormattedID%20%3D%20' + formattedID + ')' if isFeature else baseURL + 'hierarchicalrequirement?fetch=FormattedID&query=(FromattedID%20%3D%20' + formattedID + ')'

conn.request('GET', curURL, "", headers)

request = conn.getresponse()

reqJson = json.loads(request.read())

objectRef = reqJson.get('QueryResult').get('Results')[0].get('_ref')

for i in fields:
    check = i.upper()
    searchMe = fields[i].replace(" ", "%20")

    if check == 'MILESTONE':
        url = '/slm/webservice/v2.0/milestone?fetch=Name&query=(Name%20%3D%20\"' + searchMe + '\")'
        ref = query.getValue(url, userAndPass)

        value = "\"Milestones\" : { \"Milestone\": \"%s\""%ref if ref != "" else ""

        values.append(value)

    elif check == 'ITERATION'
        url = '/slm/webservice/v2.0/iteration?fetch=Name&query=((Project.Name%20%3D%20Tech)%20AND%20(Name%20contains%20\"' + searchMe + '\")'
        ref = query.getValue(url, userAndPass)

        value = "\"Iteration\": \"%s\""%ref if ref != "" else ""

        values.append(value)

    elif check == 'RELEASE':
        url = '/slm/webservice/v2.0/release?fetch=Name&query=((Project.Name%20%3D%20Tech)%20AND%20(Name%20contains%20\"' + searchMe + '\")'
        ref = query.getValue(url, userAndPass)

        value = "\"Release\": \"%s\","%ref if ref != "" else ""

        values.append(value)
    
    elif check == 'STATE' and not isFeature:
        url = '/slm/webservice/v2.0/flowstate?fetch=Name&query=((Name%20%3D%20\"' + team.replace(" ", "%20")) + '\")%20AND%20(Project.Name%20%3D%20\"' + searchMe + '\")' 
        ref = query.getValue(url, userAndPass)

        value = "\"FlowState\":{\"_ref\": \"%s\""%ref if ref != "" else ""

        values.append(value)

    elif check == 'DESCRIPTION':

        values.append("\"Description\": \"%s\","%fields[i])

    elif check == 'NOTES':

        values.append("\"Notes\": \"%s\","%fields[i])

    elif check == 'ACCEPTANCE CRITERIA':

        values.append("\"c_AcceptanceCriteria\": \"%s\","%fields[i])

    elif check == 'STATE':

        values.append("\"State\": \"%s\","%fields[i])

    else:
        logger.debug("Field " + i + " not supported")

buildBatch = BuildBatch(objectRef)

data = buildBatch.buildJson(values)

headers = {'Authorization' : 'Basic %s', 'ZSESSIONID' : '%s' %(userAndPass, configuration.apiKey)}

conn.request('POST', '/slm/webservice/v2.0/batch', data, headers)

request = conn.getresponse()

print request.read()