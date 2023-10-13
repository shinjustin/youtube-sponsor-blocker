import csv
import datetime
import webvtt
from pprint import pprint
import sponsorblock as sb
import random
import os
import json
import polars as pl
import pdb

nono_segments = (
        'sponsor',
        'selfpromo',
        'interaction',
        )

def get_segments(df):
    segments = list()
    for c in df.iter_rows():
        if c[2] in nono_segments:
            idx = nono_segments.index(c[2])
            seg = (idx+1, c[0], c[1])
            segments.append(seg)
    return segments


def vtt2csv(_id, segments):
    try:
        captions = webvtt.read(f'subs/{_id}.vtt')
    except:
        return
    for caption in captions:

        dt_format = "%H:%M:%S.%f"
        cap_start = datetime.datetime.strptime(caption.start, dt_format)
        cap_start = datetime.timedelta(hours=cap_start.hour,
                          minutes=cap_start.minute,
                          seconds=cap_start.second,
                          microseconds=cap_start.microsecond)
        cap_end = datetime.datetime.strptime(caption.end, dt_format)
        cap_end = datetime.timedelta(hours=cap_end.hour,
                          minutes=cap_end.minute,
                          seconds=cap_end.second,
                          microseconds=cap_end.microsecond)
        cat = 0
        for seg in segments:
            ad, seg_start, seg_end = seg
            seg_start = datetime.timedelta(seconds=float(seg_start))
            seg_end = datetime.timedelta(seconds=float(seg_end))
            if (cap_start >= seg_start and cap_start <= seg_end) or (cap_end >= seg_start and cap_end <= seg_end):
            #if cap_start >= seg_start or cap_end <= seg_end:
            #if (seg_start >= cap_start and seg_start <= cap_end) or (seg_end >= cap_start and seg_end <= cap_end):
                cat=ad
        if caption.text == '[Music]':
            cat = 0
        #print(cat, cap_start, cap_end, caption.text.replace('\n', ''))
        print(cat, caption.text.replace('\n', ''))

'''
def main1():
    dir = os.listdir('subs')
    vids = list()
    for cap_file in dir:
        _id = cap_file.replace('.vtt', '')
        segments = get_segments(_id)
        if segments:
            vid = (_id, segments)
            vids.append(vid)
        else:
            print('failed: ', _id)
    with open('test.json', 'w') as f:
        json.dump(vids, f)

def main2():
    with open('test.json', 'r') as f:
        vids = json.load(f)
    for vid in vids:
        vtt2csv(vid)
'''

def main():
    sub_dir = os.listdir('subs')
    #vids = [x.replace('.vtt', '') for x in sub_dir]
    #vids = vids[5:6]
    vids = ['vz-rpRYFhRo']

    csv_file = 'sponsorTimes.csv'
    q = (pl.scan_csv(csv_file)
         .select(pl.col(['startTime',
                         'endTime',
                         'category',
                         'votes',
                         'views',
                         'videoID',
                         ]))
         .filter((pl.col('videoID').is_in(vids)) &
                 (pl.col('votes')>100) &
                 (pl.col('category').is_in(nono_segments)) 
                 )
         )
    df = q.collect()

    for vid in vids:
        v_df = df.filter(pl.col('videoID')==vid)
        segments = get_segments(v_df)
        vtt2csv(vid, segments)

'''
# top 10 most voted
q = (pl.scan_csv('sponsorTimes.csv')
     .select(pl.col(['videoID','category','votes']))
     .filter(pl.col('category').is_in(nono_segments))
     .sort('votes', descending=True)
     )
print(q.collect().head(10))
'''
main()
