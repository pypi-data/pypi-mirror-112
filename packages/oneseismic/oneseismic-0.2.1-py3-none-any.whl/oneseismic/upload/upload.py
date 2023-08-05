import collections
import io
import json
import math
import numpy as np
import segyio
import segyio._segyio

from segyio.tools import native

def splitarray(a, n):
    """Split array into chunks of size N

    Split the array into chunks of size N. The last chunk may be smaller.

    Parameters
    ----------
    a : array_like
    n : int

    Yields
    ------
    a : array_like

    Examples
    --------
    >>> list(splitarray([1, 2, 3, 4, 5], 2))
    [[1, 2], [3, 4], [5]]
    >>> list(splitarray([1, 2, 3, 4, 5], 3))
    [[1, 2, 3], [4, 5]]
    >>> list(splitarray([1, 2, 3, 4, 5, 6], 3))
    [[1, 2, 3], [4, 5, 6]]
    """
    a = np.asarray(a)
    for i in range(0, len(a), n):
        yield a[i:i+n]

class attrset:
    def __init__(self, key1s, key2s, shape, dtype):
        mkfile = lambda: np.zeros(shape = shape, dtype = dtype)
        self.files = collections.defaultdict(mkfile)

        # map line-numbers to the fragment ID
        self.key1s = {k: i // shape[0] for i, k in enumerate(key1s)}
        self.key2s = {k: i // shape[1] for i, k in enumerate(key2s)}

        # map line-numbers to its index/offset/position in the fragment
        self.off1s = {k: i % shape[0] for i, k in enumerate(key1s)}
        self.off2s = {k: i % shape[1] for i, k in enumerate(key2s)}

        self.shape = shape
        self.traceno = 0
        self.limits = {}

    def commit(self, key1):
        index1 = self.key1s[key1]
        if self.limits[index1] == self.traceno:
            # todo: cache.
            js = set(self.key2s.values())
            i = index1

            # since self.files is a defaultdict, which means that even though an
            # (i,j,k) has never been written to before, it is generated and yielded
            # by the generator. This ensures that fragments or even holes [1] with
            # no data still get explicit representation when uploaded to
            # oneseismic.
            # [1] this happens quite often, especially at the edges of surveys
            for j in js:
                ident = (i, j)
                yield ident, self.files[ident]
                del self.files[ident]

        self.traceno += 1

    def put(self, key1, key2, header):
        """Put a trace

        Put a trace read from the input into the fileset. This function assumes
        the trace is parsed to native floats. This function should be called
        once for every trace in the input.

        Parameters
        ----------
        key1 : int
            line-no in dimension 0
        key2 : int
            line-no in dimension 1
        trace : np.array of float
        """
        # determine what file this trace goes into
        # this is the (i, j, _) fragment ID
        index1 = self.key1s[key1]
        index2 = self.key2s[key2]

        # the offset in a specific file the trace starts at
        i = self.off1s[key1]
        j = self.off2s[key2]

        fragment = self.files[(index1, index2)]
        fragment[i, j] = self.extract(header)

    def setlimits(self, last_trace):
        """
        fileset needs to know when the last trace of a lane is read, to safely
        commit (and prune) files. This means figuring out what traceno is that last
        for every lane, which in theory could be any line.

        Returns a dict of all dimension 0 fragment IDs, and the last trace number
        in that line.

        Parameters
        ----------
        last_trace : dict
            A dict of { lineno: traceno }, as read from scan 'key1-last-trace'
        """
        limits = collections.defaultdict(int)
        for k, v in last_trace.items():
            x = self.key1s[int(k)]
            limits[x] = max(int(v), limits[x])

        self.limits.update(limits)

class fileset:
    """Files of a volume

    The fileset class implements a simple virtual write-only file system. It
    internally handles the addresing from line numbers to fragment IDs.

    A "file" in this sense is just a numpy array (as a buffer) that can be
    uploaded as-is as a fragment. The parameters are generally obtained by
    parsing the output of the oneseismic scan program.

    Parameters
    ----------
    key1s : list of int
    key2s : list of int
    key3s : list of int
    fragment_shape : tuple of int

    Notes
    -----
    Right now, oneseismic is not mature enough to properly handle "holes" in
    the volumes, and require explicit padding.  The fileset class is aware of
    this and will generate padding fragments when necessary. This may change in
    the future and should not be relied on.
    """
    def __init__(self, key1s, key2s, key3s, fragment_shape):
        mkfile = lambda: np.zeros(shape = fragment_shape, dtype = np.float32)
        # fileset is built on the files dict, which is a mapping from (i,j,k)
        # fragment IDs to arrays. When a new fragment is accessed, a full
        # zero-cube will be created, so there is no need to keep track of what
        # needs padding.
        self.files = collections.defaultdict(mkfile)

        # map line-numbers to the fragment ID
        self.key1s = {k: i // fragment_shape[0] for i, k in enumerate(key1s)}
        self.key2s = {k: i // fragment_shape[1] for i, k in enumerate(key2s)}

        # map line-numbers to its index/offset/position in the fragment
        self.off1s = {k: i %  fragment_shape[0] for i, k in enumerate(key1s)}
        self.off2s = {k: i %  fragment_shape[1] for i, k in enumerate(key2s)}

        # samples/depth is implicitly indexed when read, so store how many
        # fragments there are in height
        self.zsections = math.ceil(len(key3s) / fragment_shape[2])
        self.fragment_shape = fragment_shape
        self.traceno = 0
        self.limits = {}

    def commit(self, key1):
        """
        Commit a "lane", yielding all completed. This function assumes that the
        last trace in the lane has been given to put(). The lane are all files
        with the same i (i,j,k) fragment ID as the one computed from key1.

        Commit can and should be called once for every put().

        Parameters
        ----------
        key1 : int
            line-number of any dimension 0 line in the lane to commit

        Returns
        -------
        files : generator of (guid, np.array)

        Notes
        -----
        Commit will prune files whenever it can, to keep resource usage low,
        but can in pathological cases end up storing the original volume in
        memory. Calling commit() on the same lane twice will result in the
        second call giving all zero-padded files.
        """
        index1 = self.key1s[key1]
        if self.limits[index1] == self.traceno:
            # todo: cache.
            js = set(self.key2s.values())
            ks = set(range(self.zsections))
            i = index1

            # since self.files is a defaultdict, which means that even though an
            # (i,j,k) has never been written to before, it is generated and yielded
            # by the generator. This ensures that fragments or even holes [1] with
            # no data still get explicit representation when uploaded to
            # oneseismic.
            # [1] this happens quite often, especially at the edges of surveys
            for j in js:
                for k in ks:
                    ident = (i, j, k)
                    yield ident, self.files[ident]
                    del self.files[ident]

        self.traceno += 1

    def put(self, key1, key2, trace):
        """Put a trace

        Put a trace read from the input into the fileset. This function assumes
        the trace is parsed to native floats. This function should be called
        once for every trace in the input.

        Parameters
        ----------
        key1 : int
            line-no in dimension 0
        key2 : int
            line-no in dimension 1
        trace : np.array of float
        """
        # determine what file this trace goes into
        # this is the (i, j, _) fragment ID
        index1 = self.key1s[key1]
        index2 = self.key2s[key2]

        # the offset in a specific file the trace starts at
        i = self.off1s[key1]
        j = self.off2s[key2]

        for index3, tr in enumerate(splitarray(trace, self.fragment_shape[2])):
            fragment = self.files[(index1, index2, index3)]
            fragment[i, j, :len(tr)] = tr

    def setlimits(self, last_trace):
        """
        fileset needs to know when the last trace of a lane is read, to safely
        commit (and prune) files. This means figuring out what traceno is that last
        for every lane, which in theory could be any line.

        Returns a dict of all dimension 0 fragment IDs, and the last trace number
        in that line.

        Parameters
        ----------
        last_trace : dict
            A dict of { lineno: traceno }, as read from scan 'key1-last-trace'
        """
        limits = collections.defaultdict(int)
        for k, v in last_trace.items():
            x = self.key1s[int(k)]
            limits[x] = max(int(v), limits[x])

        self.limits.update(limits)


class cdpset(attrset):
    def __init__(self, *args, **kwargs):
        self.prefix = 'attributes/cdp'
        self.ext = '2f32'
        dtype = np.dtype((np.float, 2))
        super().__init__(dtype = dtype, *args, **kwargs)

    def extract(self, header):
        scale = header[segyio.su.scalco]
        # SEG-Y specifies that a scaling of 0 should be interpreted as identity
        if scale == 0:
            scale = 1

        cdpx = header[segyio.su.cdpx]
        cdpy = header[segyio.su.cdpy]

        if scale > 0:
            return (cdpx * scale, cdpy * scale)
        else:
            return (cdpx / -scale, cdpy / -scale)


def upload(meta, fragment_shape, src, filesys):
    """Upload volume to oneseismic

    Parameters
    ----------
    meta : dict
        The parsed output of the scan program
    fragment_shape : tuple of int
    src : io.BaseIO
    blob : azure.storage.blob.BlobServiceClient
    """
    word1 = meta['key-words'][0]
    word2 = meta['key-words'][1]
    key1s = meta['dimensions'][0]
    key2s = meta['dimensions'][1]
    key3s = meta['dimensions'][2]
    guid  = meta['guid']

    key1s.sort()
    key2s.sort()
    key3s.sort()

    # Seek past the textual headers and the binary header
    src.seek(int(meta['byteoffset-first-trace']), io.SEEK_CUR)

    # Make a custom dtype that corresponds to a header and a trace. This
    # assumes all traces are of same length and sampled similarly, which is
    # a safe assumption in practice. This won't be checked though, the check
    # belongs in the scan program.
    #
    # The dtype is quite useful because it means the input can be read into the
    # numpy array as a buffer, and then passed on directly as numpy arrays to
    # put()
    dtype = np.dtype([
        ('header', 'b', 240),
        ('samples', 'f4', len(key3s)),
    ])
    trace = np.array(1, dtype = dtype)
    fmt = meta['format']

    files = fileset(key1s, key2s, key3s, fragment_shape)
    files.setlimits(meta['key1-last-trace'])
    shapeident = '-'.join(map(str, fragment_shape))
    prefix = f'src/{shapeident}'

    attrs = [
        cdpset(key1s, key2s, (256, 512)),
    ]
    for attr in attrs:
        attr.setlimits(meta['key1-last-trace'])

    filesys.mkdir(guid)
    filesys.cd(guid)

    while True:
        break
        n = src.readinto(trace)
        if n == 0:
            break

        header = segyio.field.Field(buf = trace['header'], kind = 'trace')
        data = native(data = trace['samples'], format = fmt)

        key1 = header[word1]
        key2 = header[word2]
        files.put(key1, key2, data)

        for attr in attrs:
            attr.put(key1, key2, header)
            #attr.put(key1, key2, trace)

        for ident, fragment in files.commit(key1):
            ident = '-'.join(map(str, ident))
            name = f'{prefix}/{ident}.f32'
            #print('uploading', name)
            with filesys.open(name, mode = 'wb') as f:
                continue
                f.write(fragment)

        for attr in attrs:
            for ident, block in attr.commit(key1):
                ident = '-'.join(map(str, ident))
                name = f'{attr.prefix}/{ident}'
                try:
                    name = f'{name}.{attr.ext}'
                except AttributeError:
                    pass
                print('uploading', name)

                with filesys.open(name, mode = 'wb') as f:
                    print(block)
                    f.write(block)

    manifest = {
        'format-version': 1,
        'guid': guid,
        'data': [
            {
                'file-extension': 'f32',
                'filters': [],
                'shapes': [list(fragment_shape)],
                'prefix': 'src',
                'resolution': 'source',
            },
        ],
        'attributes': [
            {
                'type': 'cdp',
                'layout': 'tiled',
                'file-extension': '2f32',
                'labels': ['CDP X', 'CDP Y'],
                'shape': [[256, 512]],
                'prefix': 'cdp',
            },
        ],
        'line-numbers': [
            key1s,
            key2s,
            key3s,
        ],
        'line-labels': ['inline', 'crossline', 'depth'],
    }

    with filesys.open('manifest.json', mode = 'wb') as f:
        print(manifest)
        f.write(json.dumps(manifest).encode())
