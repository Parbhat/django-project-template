# -*- coding: utf-8 -*-
"""
    {{ project_name }}.libs.common.utils.server
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A collection of functions pertainting to server inspection.

    :copyright: (c) 2015
"""
import httplib
import xmlrpclib


def supervisor_process_states(domain, port, timeout=1):
    """
    Return the state of all available supervisor processes.
    """
    class TimeoutTransport(xmlrpclib.Transport):
        def __init__(self, timeout, *args, **kwargs):
            self.timeout = timeout
            return xmlrpclib.Transport.__init__(self, *args, **kwargs)

        def make_connection(self, host):
            return httplib.HTTPConnection(host, timeout=self.timeout)

    transport = TimeoutTransport(timeout)
    server = xmlrpclib.Server('http://%s:%s/RPC2' % (domain, port),
            transport=transport)
    results = {}
    for info in server.supervisor.getAllProcessInfo():
        results[info['name']] = info['statename']
    return results
