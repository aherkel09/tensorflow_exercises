function [expinfo]=ParseAndTag(varargin)

options = struct('nruns', 0, 'subject', 'none', 'dir', pwd(), 'tr', 0, 'condition', [], 'duration', 0);
optionNames = fieldnames(options);

% error handling courtesy of Chris McNorgan
for pair = reshape(varargin,2,[]) % pair is {propName;propValue}
    inpName = lower(pair{1}); % make case insensitive
    
    if any(strcmp(inpName,optionNames))
        options.(inpName) = pair{2};
    else
        error('%s is not a recognized parameter name',inpName)
    end
end

% initialize cell arrays for par & timecourse files
par_files=cell(1, options.nruns);

for i=36:options.nruns
    % determine correct number of 0's to prepend to run string 
    % (e.g. 001, 035, &c.)
    if (i > 99)
        zeros='';
    elseif (i > 9)
        zeros='0';
    else
        zeros='00';
    end
        
    run = append(zeros, num2str(i)); % construct run number
    par_file={[append(run, '\horikawa.par')]}; % construct par filename
    par_files{1, i}=par_file; % put filename in cell array
    
end

% set subdir where PARParser will look for files
subdir=append(options.dir, options.subject, '\bold'); 

% run PARParser.m for a single subject & store output in expinfo
expinfo=PARParser('file', par_files, 'path', subdir, 'run', [1], 'subject', options.subject);

% drop lausanne parcellation regions 1 & 5 from both hemispheres,
% run loadFSTS.m
ldrop=[1 5];
rdrop=[1 5];
mnidrop=[1 5];

% FIXME: need to pass files to loadFSTS
[M, hemis]=loadFSTS('ldrop', ldrop, 'rdrop', rdrop, 'mnidrop', mnidrop);

% scale timeseries data from loadFSTS
thresh=1.96;
ZM=normalizeMatrix(M);
[BIN, SCALED]=binarizeMatrix(ZM, 'thresh', thresh);
SCALED=cellfun(@(x) round(x,4), SCALED, 'UniformOutput', false); % round scaled values

% store info from par files & scaled timeseries matrix in DAT
for i=36:options.nruns
    DAT{i}.expinfo=expinfo{i};
    DAT{i}.mat=SCALED{i};
end

% run TSTagger.m
TSTagger('tr', options.tr, 'condition', options.condition, 'dat', DAT, 'duration', options.duration);

end

