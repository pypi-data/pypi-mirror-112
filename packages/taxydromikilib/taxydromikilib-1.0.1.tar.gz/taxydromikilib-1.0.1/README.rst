==============
taxydromikilib
==============

A small library to search taxydromiki for parsels and their status.


* Documentation: https://taxydromikilib.readthedocs.org/en/latest


Development Workflow
====================

The workflow supports the following steps

A small library to search taxydromiki for parsels and their status


* Documentation: http://taxydromikilib.readthedocs.io/en/latest/

Features
--------

* Searches taxydromikis site and returns a list of TrackingState objects for each state if any.

TrackingState objects expose the following attributes
    * status
    * location
    * date
    * time
    * is_final (if the current state concludes the delivery of the package)
