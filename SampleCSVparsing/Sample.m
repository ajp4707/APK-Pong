%% Sample script to demo getGameDataRecordingTimes
[start, en] = getGameDataRecordingTimes('gamedata_2022-04-08-17-08-39.csv');
disp(start.datetime);
disp(en.datetime);
