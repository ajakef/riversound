path = '/home/jake/Work/StreamAcoustics/Sawtooths/TrailCreek/2021-05-17/'
path_infrasound = path + 'mseed'
path_audio = path + 'AM006'
t1 = obspy.UTCDateTime('2021-05-12T00_00_00')
t2 = obspy.UTCDateTime('2021-05-12T01_00_00')
st = read_infrasound_audio(t1, t2, path_infrasound, path_audio)

assert len(st) == 2
assert len(st.select(station='')[0].data) == (30*192000)
assert len(st.select(station='101')[0].data) == (3600*100)

