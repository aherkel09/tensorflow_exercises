function [eio, runs]=PARParser(varargin)
eio=cell(0);
runs=[];

% define defaults at the beginning of the code so that you do not need to
% scroll way down in case you want to change something or if the help is
% incomplete
options = struct('file', [],'path', pwd(), 'run', [], 'subject', 'no_name');

% read the acceptable names
optionNames = fieldnames(options);

% count arguments
nArgs = length(varargin);
if round(nArgs/2)~=nArgs/2
    error('This function requires propertyName/propertyValue pairs')
end

%Populate options with argument values
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

%If no list of files is passed, spawn dialog box
if (isempty(options.file))
    FilterSpec=['*.par'];
    [filename,pathname] = uigetfile(FilterSpec, 'Select 1 or more par files', ...
        'MultiSelect','on');
    options.file=filename;
    options.path=pathname;
    %%if there are multiple filenames, sort them
    if (iscell(filename))
        options.file=sort(options.file);
    else
        %otherwise put the lone file in a cell array
        options.file={options.file};
    end
end

%iterate through par files; open and store each in the cell
%array
runs=nan(1,length(options.file));
for f=1:length(options.file)
    filename=fullfile(options.path, cell2mat(options.file{f}));
    temp=readtable(filename, 'FileType', 'text', 'Delimiter', '\t');
    temp=table2struct(temp);
    expinfo=struct();
    expinfo.run=f;
    expinfo.subject=options.subject;
    fnames=fieldnames(temp);
    newnames={'timestamp', 'condition', 'rt', 'response'};
    N=numel(temp);
    for k=1:numel(fnames)
        [data(1:N).(newnames{k})] = deal(temp.(fnames{k})) ;
    end
    expinfo.data=data;
    runs(f)=f;
    eio{f}=expinfo;
end

end