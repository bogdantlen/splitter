from os import mkdir
# from re import escape
from pydub import AudioSegment


def main():
    file = input('Enter file name with extension: ').split('.')
    print('Loading file...')
    song = AudioSegment.from_file('.'.join(file), file[-1])
    tracks = [
        tuple(line.rstrip('\n').split(';')) for line in open('tracks.txt')
    ]
    last = len(tracks) - 1
    metadata = get_meta()
    path = '{0} - {1} ({2})'.format(metadata['artist'], metadata['album'],
                                    metadata['year'])
    mkdir('./' + path)
    for i, track in enumerate(tracks):
        print('Processing: ' + track[0])
        s_part = []
        if i == 0: s_part = song[:to_mil(tracks[i + 1][1])]
        elif i == last: s_part = song[to_mil(track[1]):]
        else: s_part = song[to_mil(track[1]):to_mil(tracks[i + 1][1])]
        metadata['track'] = i + 1
        metadata['title'] = track[0]
        s_part.export(
            './{0}/{1}.mp3'.format(path, track[0]),
            format='mp3',
            bitrate='320k',
            parameters=['-c:a', 'libmp3lame'],
            tags=metadata)
        print('OK')
    print('Done!')
    return None


def get_meta():
    metadata = {
        'artist': 'Unknown artist',
        'album': 'Unknown album',
        'year': '0',
        'genre': ''
    }
    for m in metadata:
        inp = input('Enter {} (press Enter to skip): '.format(m))
        if len(inp):
            metadata[m] = inp
    metadata['track'] = 0
    metadata['title'] = ''
    # metadata['year'] = int(metadata['year'])
    return metadata


def to_mil(stamp):
    spl_stamp = [int(i) for i in stamp.split(':')]
    if len(spl_stamp) == 2: return (spl_stamp[0] * 60 + spl_stamp[1]) * 1000
    elif len(spl_stamp) == 3:
        return (spl_stamp[0] * 3600 + spl_stamp[1] * 60 + spl_stamp[2]) * 1000


if __name__ == '__main__':
    main()
