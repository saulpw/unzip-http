# unzip-http

Extract individual files from .zip files over http without downloading the entire archive.

## Install

    pip install unzip-http

## Usage

    unzip-http <url.zip> <filenames..>

Extract <filenames> from a remote .zip at <url> to stdout.

If no filenames given, displays .zip contents (filenames and sizes).

Each filename can be a wildcard glob; all matching files are concatenated and sent to stdout in zipfile order.

Note: HTTP server must send `Accept-Ranges: bytes` and `Content-Length` in headers.

# Python module `unzip_http`

    import unzip_http

    rzf = unzip_http.RemoteZipFile('https://example.com/foo.zip')
    binfp = rzf.open('bar.bin')
    txtfp = rzf.open_text('baz.txt')

# Credits

`unzip-http` was written by [Saul Pwanson](https://saul.pw) and made available for use under the MIT License.
