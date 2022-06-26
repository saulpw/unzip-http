from dataclasses import dataclass

import sys
import io
import time
import zlib
import struct
import fnmatch

import urllib3


def error(s):
    raise Exception(s)


@dataclass
class RemoteZipInfo:
    filename:str = ''
    date_time:int = 0
    header_offset:int = 0
    compress_type:int = 0
    compress_size:int = 0
    file_size:int = 0


class RemoteZipFile:
    fmt_endcdir = 'IHHHHIIH'
    fmt_cdirentry = '<IHHHHIIIIHHHHHII'
    fmt_localhdr = '<IHHHIIIIHH'

    def __init__(self, url):
        self.url = url
        self.http = urllib3.PoolManager()

    @property
    def files(self):
        return {r.filename:r for r in self.infolist()}

    def infolist(self):
        resp = self.http.request('HEAD', self.url)
        r = resp.headers.get('Accept-Ranges', '')
        if r != 'bytes':
            error(f"Accept-Ranges header must be 'bytes' ('{r}')")

        sz = int(resp.headers['Content-Length'])
        resp = self.get_range(sz-65536, 65536)
        i = resp.data.rfind(b'\x50\x4b\x05\x06')

        magic, disk_num, disk_start, disk_num_records, total_num_records, cdir_bytes, cdir_start, comment_len = struct.unpack_from(self.fmt_endcdir, resp.data, offset=i)

        filehdr_index = 65536 - (sz - cdir_start)
        cdir_end = filehdr_index + cdir_bytes
        while filehdr_index < cdir_end:
            sizeof_cdirentry = struct.calcsize(self.fmt_cdirentry)

            magic, ver, ver_needed, flags, method, date_time, crc, \
                complen, uncomplen, fnlen, extralen, commentlen, \
                disknum_start, internal_attr, external_attr, local_header_ofs = \
                    struct.unpack_from(self.fmt_cdirentry, resp.data, offset=filehdr_index)

            filename = resp.data[filehdr_index+sizeof_cdirentry:filehdr_index+sizeof_cdirentry+fnlen]

            filehdr_index += sizeof_cdirentry + fnlen + extralen + commentlen

            yield RemoteZipInfo(filename.decode(), date_time, local_header_ofs, method, complen, uncomplen)

    def get_range(self, start, n):
        return self.http.request('GET', self.url, headers={'Range': f'bytes={start}-{start+n-1}'}, preload_content=False)

    def matching_files(self, *globs):
        for f in self.files.values():
            if any(fnmatch.fnmatch(f.filename, g) for g in globs):
                yield f

    def open(self, fn):
        if isinstance(fn, str):
            f = list(self.matching_files(fn))
            if not f:
                error(f'no files matching {fn}')
            f = f[0]
        else:
            f = fn

        sizeof_localhdr = struct.calcsize(self.fmt_localhdr)
        r = self.get_range(f.header_offset, sizeof_localhdr)
        localhdr = struct.unpack_from(self.fmt_localhdr, r.data)
        magic, ver, flags, method, dos_datetime, _, _, uncomplen, fnlen, extralen = localhdr
        if method == 0: # none
            return self.get_range(f.header_offset + sizeof_localhdr + fnlen + extralen, f.compress_size)
        elif method == 8: # DEFLATE
            resp = self.get_range(f.header_offset + sizeof_localhdr + fnlen + extralen, f.compress_size)
            return RemoteZipStream(resp, f)
        else:
            error(f'unknown compression method {method}')

    def open_text(self, fn):
        return io.TextIOWrapper(io.BufferedReader(self.open(fn)))


class RemoteZipStream(io.RawIOBase):
    def __init__(self, fp, info):
        self.raw = fp
        self._decompressor = zlib.decompressobj(-15)
        self._buffer = bytes()

    def readable(self):
        return True

    def readinto(self, b, /):
        r = self.read(len(b))
        b[:len(r)] = r
        return len(r)

    def read(self, n):
        while n > len(self._buffer):
            r = self.raw.read(2**18)
            if not r:
                break
            self._buffer += self._decompressor.decompress(r)

        ret = self._buffer[:n]
        self._buffer = self._buffer[n:]

        return ret
