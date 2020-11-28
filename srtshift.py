import sys
import re


def try_match_timeslot(line):
    m = re.match(
        '([0-9][0-9]):([0-9][0-9]):([0-9][0-9]),([0-9][0-9][0-9]) --> ([0-9][0-9]):([0-9][0-9]):([0-9][0-9]),([0-9][0-9][0-9])', line)
    if m:
        return {
            'from': {
                'hour': int(m.group(1)),
                'min': int(m.group(2)),
                'sec': int(m.group(3)),
                'ms': int(m.group(4)),
            },
            'to': {
                'hour': int(m.group(5)),
                'min': int(m.group(6)),
                'sec': int(m.group(7)),
                'ms': int(m.group(8)),
            }
        }
    return False


def ts2ms(ts):
    return ts['hour']*3600*1000 + ts['min']*60*1000 + ts['sec']*1000 + ts['ms']


def ms2ts(ms):
    hour = ms // (3600*1000)
    ms -= hour * (3600*1000)
    minute = ms // (60*1000)
    ms -= minute * (60*1000)
    sec = ms // 1000
    ms -= sec * 1000
    return {
        'hour': hour,
        'min': minute,
        'sec': sec,
        'ms': ms
    }


def shift_time(ts, t):
    return ms2ts(ts2ms(ts)+t)


def shift_timeslot(m, t):
    return {
        'from': shift_time(m['from'], t),
        'to': shift_time(m['to'], t)
    }


f = open(sys.argv[1])
for line in f:
    line = line.rstrip()
    m = try_match_timeslot(line)
    if m:
        m2 = shift_timeslot(m, int(sys.argv[2]))
        print(f'{m2["from"]["hour"]:02d}:{m2["from"]["min"]:02d}:{m2["from"]["sec"]:02d},{m2["from"]["ms"]:03d} --> {m2["to"]["hour"]:02d}:{m2["to"]["min"]:02d}:{m2["to"]["sec"]:02d},{m2["to"]["ms"]:03d}')
        continue
    print(line)
