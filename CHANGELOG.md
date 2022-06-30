# unzip-http version history

# v0.2 (2022-06-29)

## Features

- show sizes in bytes instead of MB
- support ZIP64 (requested by @bousqi #4)

## Bugfixes

- fix off-by-one: range-requests are inclusive of end byte (reported by @bousqi #3)
