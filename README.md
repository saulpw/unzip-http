# unzip-http

Extract individual files from .zip files over http without downloading the entire archive.

## Install

    pip install unzip-http

## Usage

    unzip-http [-l] [-f] [-o] <url> <filenames..>

Extract <filenames> from a remote .zip at `<url>` to stdout.

A filename can be a wildcard glob; all matching files are extracted in this case.

Specify multiple filenames as distinct arguments (separated with spaces on the command line).

Note: HTTP server must send `Accept-Ranges: bytes` and `Content-Length` in headers (most do).

Options:

- `-l`: List files in remote .zip file (default if no filenames given)
- `-f`: Recreate folder structure from .zip file when extracting (instead of extracting files to the current directly to the current directory)
- `-o`: Write files to stdout (if multiple files, concatenate them in zipfile order)

# Python module `unzip_http`

    import unzip_http

    rzf = unzip_http.RemoteZipFile('https://example.com/foo.zip')
    binfp = rzf.open('bar.bin')
    txtfp = rzf.open_text('baz.txt')

# Credits

`unzip-http` was written by [Saul Pwanson](https://saul.pw) and made available for use under the MIT License.
