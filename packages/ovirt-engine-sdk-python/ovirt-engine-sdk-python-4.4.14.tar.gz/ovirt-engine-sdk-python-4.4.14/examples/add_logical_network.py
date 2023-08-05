#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (c) 2017 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import logging

import ovirtsdk4 as sdk
import ovirtsdk4.types as types

logging.basicConfig(level=logging.DEBUG, filename='example.log')

# This example will connect to the server and create new logical network.

# Create the connection to the server:
connection = sdk.Connection(
    url='https://engine40.example.com/ovirt-engine/api',
    username='admin@internal',
    password='redhat123',
    ca_file='ca.pem',
    debug=True,
    log=logging.getLogger(),
)

# Get the reference to the networks service:
networks_service = connection.system_service().networks_service()

# Use the "add" method to create new VM logical network in data center
# called "mydc", with VLAN tag 100 and MTU 1500.
network = networks_service.add(
    network=types.Network(
        name='mynetwork',
        description='My logical network',
        data_center=types.DataCenter(
            name='mydc'
        ),
        vlan=types.Vlan(id='100'),
        usages=[types.NetworkUsage.VM],
        mtu=1500,
    ),
)

# Close the connection to the server:
connection.close()
