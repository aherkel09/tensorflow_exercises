function eio=PARParser(varargin)
eio=cell(0);
runs=[];
options = struct('file', [],'path', pwd(), 'run', []);
 
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
    options.file=sort(options.file);
end

%iterate through par files; open and store each in the cell
%array
runs=nan(1,length(options.file));

for f=1:length(options.file)
    filename=fullfile(options.path, options.file{f});
    temp=readtable(filename, 'FileType', 'text', 'Delimiter', '\t');
    expinfo=struct();
    expinfo.run=f;
    expinfo.data=table2struct(temp);
    eio{1, f}=expinfo;
end

end