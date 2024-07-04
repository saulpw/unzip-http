# unzip-http version history

# v0.5.1 (2024-07-03)

- add RemoteZipInfo.extract() method
- handle large (>64k) central dir
- only warn on missing Accept-Ranges header
  - e.g. S3 does not send it but still supports Range Requests

# v0.4 (2022-07-13)

- expand support for the unzip_http library to Python v3.6

## API

* parse date_time in ZipInfo
* add RemoveZipFile.extractall()

# v0.3 (2022-07-06)

* add MIT license to file to make it vendorable
* expand support for the unzip_http library to Python v3.7
    - (unzip-http bin still requires Python v3.8)

## API

* add zip_size attribute (thanks @bousqui #6)
* add symbols for eocd magics (thanks @bousqui #6)
* make RemoteZipFile a context handler
* RemoteZipFile.files now a cached property

# v0.2 (2022-06-29)

## Features

- show sizes in bytes instead of MB
- support ZIP64 (requested by @bousqi #4)

## Bugfixes

- fix off-by-one: range-requests are inclusive of end byte (reported by @bousqi #3)
