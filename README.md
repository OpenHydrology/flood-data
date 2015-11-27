# UK Flood Data

Additional flood data for use in OH Auto Statistical (web version)

File validator status: [![Build Status](https://travis-ci.org/faph/flood-data.svg)](https://travis-ci.org/faph/flood-data)

This repository contains flood flow data *additional* to the data included in
the National River Flow Archive ([NRFA](http://nrfa.ceh.ac.uk/)). The web 
version of OH Auto Statistical pulls in these additional data to allow flood
frequency-magnitude estimation using the most up to date data available.

This respository is available for *anyone* using the OH Auto Statistical
software. All users of the software will also benefit from your data
updates.

To add your data, please use [the GitHub pull request approach]
(https://help.github.com/articles/using-pull-requests/). You can either
work online or create a local copy ("clone") of this repository to work in
(recommended).

For each station you want to update, do the following:

1. Create and switch to a new branch named `station-{nrfa_id}`
2. Create your `.cd3` and `.am` files and save these into the `data` folder.
3. Make sure to set or check QMED and growth curve suitability as appropriate.
4. Create a GitHub "pull request" to request merging of your data back into
   this repository.
5. We will review your data and merge it.

**Your updates will become available for anybody using OH Auto Statistical.
Please make sure your updates are correct and are from a reliable source.**
