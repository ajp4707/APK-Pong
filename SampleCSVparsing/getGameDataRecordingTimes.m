function [ recordingStart, recordingEnd ] = getGameDataRecordingTimes( gamedataFile )
%GetGameDataRecordingTimes Parses gamedataFiles from Pong to find start and
%end times
%   @param gamedataFile : string of gamedata csv filename
%   
%   @return recordingStart : struct with data about what time the recording
%   started
%   Call recordingStart.datetime to see the pretty string format
%
%   @return recordingEnd : struct with data about what time the recording
%   ended

recordingStart = struct();
recordingEnd = struct();

fid = fopen(gamedataFile);

if fid == -1
    disp('File read error. Did you provide the right file name? Is it in the right directory?')
else
    c = fread(fid,'uint8=>char')';

    % Assumption: File is in correct gamedata format. Thus, the start time is
    % at the beginning of the file, and the end time is at the end of the file.
    fullDateStr = c(1:20); %date strings are 20 characters long
    fullDateEnd = c(end-21:end-1);

    recordingStart.yearStr = fullDateStr(1:4); %yyyy
    recordingStart.monthStr = fullDateStr(5:6); %MM
    recordingStart.dayStr = fullDateStr(7:8); %dd
    recordingStart.hourStr = fullDateStr(9:10); %Note this military time (1pm = 13) so hour format is HH not hh
    recordingStart.minStr = fullDateStr(11:12); %mm
    recordingStart.secStr = fullDateStr(13:14); %ss
    recordingStart.fracSecStr = fullDateStr(15:20); %SSSSSS %microsec
    recordingStart.datetime =datetime(fullDateStr,'Format','yyyyMMddHHmmssSSSSSS');
    recordingStart.datetime.Format = 'yyyy-MM-dd HH:mm:ss.SSS'; 


    recordingEnd.yearStr = fullDateEnd(1:4); %yyyy
    recordingEnd.monthStr = fullDateEnd(5:6); %MM
    recordingEnd.dayStr = fullDateEnd(7:8); %dd
    recordingEnd.hourStr = fullDateEnd(9:10); %Note this military time (1pm = 13) so hour format is HH not hh
    recordingEnd.minStr = fullDateEnd(11:12); %mm
    recordingEnd.secStr = fullDateEnd(13:14); %ss
    recordingEnd.fracSecStr = fullDateEnd(15:20); %SSSSSS %microsec
    recordingEnd.datetime =datetime(fullDateEnd,'Format','yyyyMMddHHmmssSSSSSS');
    recordingEnd.datetime.Format = 'yyyy-MM-dd HH:mm:ss.SSS'; 
end
end

