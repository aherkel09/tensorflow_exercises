function [M, hemis]=loadFSTS(varargin)
%%Loads a set of FreeSurfer time series files. File names may be specified
%%as arguments. If not specified, the user will be prompted to select the
%%set of input files. Other optional arguments may perform additional
%%operations on the data.
%
% Optional arguments:
%   'nomni', TRUE/FALSE: a flag indicating whether the script should skip
%           loading subcortical time series in mni305 space. Default: FALSE
%   'lnames', lnames: a cell array of strings designating the time series
%           files for left hemisphere regions (default: empty)
%   'rnames', rnames: a cell array of strings designating the time series
%           files for right hemisphere regions (default: empty)
%   'mninames', mninames: a cell array of strings designating the time
%           series files for mni305 regions (default: empty)
%   'ldrop', d: a matrix corresponding to the lh columns (regions) to be
%           omitted from the returned matrix. (default: omit none)
%   'rdrop', d: a matrix corresponding to the rh columns (regions) to be
%           omitted from the returned matrix. (default: omit none)
%   'mnidrop', d: a matrix corresponding to the subcortical columns
%           (regions) to be omitted from the returned matrix. (default:
%           omit none)
%   'automatch', TRUE/FALSE: a flag inidicating whether to match the lh,
%           rh and mnitime series files by filename
%           (e.g., 'lh_run1.wav.txt' automatically paired with
%           'rh_run1.wav.txt' and mni_run1.wav.txt).
%           This argument is only used when either lnames or rnames are
%           omitted and is intended to make it easier to load corresponding
%           time series files. (default: TRUE)
%   'autolh', 'left_pattern': a string used with the automatch feature that
%           is used to identify the left hemisphere member of grouped time
%           series files. (default: 'lh')
%   'autorh', 'right_pattern': a string used with the automatch feature
%           that is used to identify the right hemisphere member of grouped
%           time series files. (default: 'rh')
%   'automni', 'mni_pattern': a string used with the automatch feature that
%           is used to identify the mni space member of grouped time series
%           files. (default: 'subcort')
%
% Returns:
%    M:     A cell array of length t, where t is the number of time series
%       matrices loaded. M is a cell array because the matrices may contain
%       different numbers of time points/samples. If it turns out that the
%       matrices have the same number of rows and columns, you can always
%       use cell2mat(M) to convert M into a 3D matrix.
%   hemis:  A 1xn array, where n is the sum of the number of columns
%           retained from all regions. Columns corresponding to
%           left-hemisphere regions contain a 1; 0 for right. -1 for
%           subcortical.
%
% Usage:
% %In this first example, the user will be prompted to locate 1+ time
% %series files (with the '.wav.txt' extension). The user will first be
% %prompted to find files matching the pattern '*lh*.wav.txt', for the lh
% %surface segmentations. Because automatch is set to TRUE by default, the
% %corresponding '*rh*.wav.txt' filenames will also be assumed. This is a
% %useful approach if your data is organized with a regular filename
% %pattern (e.g., 'lh_run1.wav.txt', 'rh_run1.wav.txt', 'lh_run2.wav.txt',
% %'rh_run2.wav.txt', ... etc.)
% M=loadFSTS();
%
% %In this next example, automatch is toggled off. Use this if your time
% %series filenames do not have corresponding patterns that differ only by
% %the presence of a 'lh' vs 'rh' string (e.g., 'ts_1.wav.txt',
% %'ts_2.wav.txt', ..., etc.). This seems like a silly way to organize your
% %data, however; I merely included this option in case you are a silly
% %person.
% M=loadFSTS('automatch', FALSE);

% lnames={'lh.myaparc_250_01.wav.txt', 'lh.myaparc_250_02.wav.txt'};
% rnames={'rh.myaparc_250_01.wav.txt', 'rh.myaparc_250_02.wav.txt'};
% M=loadFSTS('lfiles', lnames, 'rfiles', rnames, 'ldropregions', [1 5]);

% define defaults at the beginning of the code so that you do not need to
% scroll way down in case you want to change something or if the help is
% incomplete
%% Part 0: Defaults; parsing parameters
options = struct('nomni', false, 'lnames',{''},'rnames',{''}, 'mninames', {''}, ...
    'ldrop', [], 'rdrop', [], 'mnidrop', [], ...
    'automatch', true, 'autolh', 'lh', 'autorh', 'rh', 'automni', 'subcort');

% read the acceptable names
optionNames = fieldnames(options);

% count arguments
nArgs = length(varargin);
if round(nArgs/2)~=nArgs/2
    error('loadFSTS() needs propertyName/propertyValue pairs')
end

for pair = reshape(varargin,2,[]) % pair is {propName;propValue}
    inpName = lower(pair{1}); % make case insensitive
    
    if any(strcmp(inpName,optionNames))
        % overwrite options. If you want you can test for the right class here
        % Also, if you find out that there is an option you keep getting wrong,
        % you can use "if strcmp(inpName,'problemOption'),testMore,end"-statements
        options.(inpName) = pair{2};
    else
        error('%s is not a recognized parameter name',inpName)
    end
end

%% Part 1: Get the filenames if required
while((length(options.lnames) ~= length(options.rnames)) ...
        || length(options.lnames)==0 )
    warntext=sprintf('You have either not specified files to open or they are unmatched.');
    warntext=sprintf('%s\nYou will now be prompted to select matching file sets.', warntext);
    warning(warntext);
    FilterSpec=['*' options.autolh '*.wav.txt'];
    %get lhfiles
    [lFileName,PathName] = uigetfile(FilterSpec, 'Select 1 or more LEFT HEMISPHERE Time Series files', ...
        'MultiSelect','on');
    options.lnames=fullfile(PathName, lFileName);
    %get rh files
    if(options.automatch)
        rFileName=strrep(lFileName, options.autolh, options.autorh);
        options.rnames=fullfile(PathName, rFileName);
        if ~options.nomni %figure out subcortical files if required
            mniFileName=strrep(lFileName, options.autolh, options.automni);
            options.mninames=fullfile(PathName, mniFileName);
        end
    else
        FilterSpec=['*' options.autorh '*.wav.txt'];
        %get rhfiles
        [rFileName,PathName] = uigetfile(FilterSpec, 'Select the matching RIGHT HEMISPHERE Time Series files', ...
            'MultiSelect','on');
        options.rnames=fullfile(PathName, rFileName);
        
        %figure out subcortical files if required
        if ~options.nomni
            FilterSpec=['*' options.automni '*.wav.txt'];
            [mniFileName,PathName] = uigetfile(FilterSpec, 'Select the matching SUBCORTICAL Time Series files', ...
                'MultiSelect','on');
            options.mninames=fullfile(PathName, mniFileName);
        end
    end
end

%% Part 2: Load each of the matched files
M=cell(length(options.lnames),1); %matrices go in a cell array because they can be of differing sizes. Each cell holds a time x regions matrix
hemis=[];
for i=1:length(options.lnames)
    % output names to console
    disp(options.lnames{i});
    disp(options.rnames{i});
    disp(options.mninames{i});
    
    ldat=load(options.lnames{i});
    rdat=load(options.rnames{i});
    if ~options.nomni
        mnidat=load(options.mninames{i});
        mnikeep=1:size(mnidat,2);
    else
        mnidat=[];
        mnikeep=[];
    end
    
    %check out how we specify which columns we keep:
    %by default, we keep all the columns
    lkeep=1:size(ldat,2);
    rkeep=1:size(rdat,2);
    %next, we remove from this set any columns indicated in
    %options.?dropregions:
    lkeep(options.ldrop)=[];
    rkeep(options.rdrop)=[];
    mnikeep(options.mnidrop)=[];
    
    ldat=ldat(:,lkeep);
    rdat=rdat(:,rkeep);
    mnidat=mnidat(:,mnikeep);
    
    M{i}=[ldat rdat mnidat];
    %finally, hemis tracks which columns are left/right hemisphere. Only do this 1ce
    if(isempty(hemis))
        hemis=[ones(1, (size(ldat,2))) zeros(1,size(rdat,2)) -1*ones(1,size(mnidat,2))];
    end
end

%%END FUNCTION
end