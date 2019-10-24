
pattoo-agents JSON Data Formatting
==================================

Introduction
------------

This is a sample of the formatting of JSON data created by ``pattoo-agents``. This data is either sent to, or retrieved from, a remote ``pattoo`` server.

.. code-block:: json

   {
      "agent_program" : "pattoo-agent-os-spoked",
      "agent_id" : "f95784520cdf96cdcc6125378d9d90f47db8caf6d31543f60d828a3182ccec0f",
      "timestamp" : 1570413300,
      "agent_hostname" : "swim",
      "devices" : {
         "swim" : {
           "system" : {
              "data_type" : null,
              "description" : "Operating System",
              "data" : [
                 [
                    null,
                    "Linux"
                 ]
              ]
           },
           "distribution" : {
              "description" : "Linux Distribution",
              "data" : [
                 [
                    null,
                    "Ubuntu 18.04 Bionic Beaver"
                 ]
              ],
              "data_type" : null
           },
           "release" : {
              "data_type" : null,
              "data" : [
                 [
                    null,
                    "4.15.0-65-generic"
                 ]
              ],
              "description" : "Kernel Version"
           },
           "version" : {
              "data_type" : null,
              "data" : [
                 [
                    null,
                    "#74-Ubuntu SMP Tue Sep 17 17:06:04 UTC 2019"
                 ]
              ],
              "description" : "Kernel Type"
           },
           "network_bytes_sent" : {
              "data_type" : 64,
              "data" : [
                 [
                    "enp3s0f1",
                    0
                 ],
                 [
                    "lo",
                    26923324
                 ],
                 [
                    "wlp2s0",
                    461076329
                 ]
              ],
              "description" : "Bytes (Out)"
           },
           "cpu_count" : {
              "data_type" : 1,
              "data" : [
                 [
                    null,
                    8
                 ]
              ],
              "description" : "CPU Count"
           },
           "disk_usage_percent" : {
              "data_type" : 1,
              "data" : [
                 [
                    "/",
                    23.2
                 ],
                 [
                    "/boot/efi",
                    1.2
                 ],
                 [
                    "/data",
                    92
                 ]
              ],
              "description" : "Partition Utilization (%)"
           }
         }
      }
   }

Formatting
----------
