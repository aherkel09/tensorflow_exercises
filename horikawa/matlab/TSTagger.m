function TSTagger(varargin)
%% function TSTagger(varargin)
% Isolate TimeSeries data associated with each condition in a .mat runtime
% file
% 
% Mandatory arguments:
%   condition: a cell array of condition codes matching values in the
%       condition column
%
%	tr: scan interval (E.g. 2.047)
%   dat: a cell array of structs: {dat.expinfo, dat.mat}, where expinfo comes
%     from the PsychToolBox runtime .mat files, and mat is a normalized 
%     timepoints x regions matrix of BOLD data generated by the
%     gettimecourses.sh BASH script 
%   
% Optional arguments:
%   duration: a scalar indicating the number of seconds for each event
%   (default: 5)
%
%   volumes_dropped: number of INITIAL volumes dropped (i.e., volumes from 
%       the start of the run), either as a single value or else as a vector
%       of numbers. If a single value is provided, it will be applied to
%       all paired data files, otherwise the values will be applied to the
%       corresponding dat argument cell
%
%   precision: input values will be rounded to PRECISION decimal places
%   (default: 3)
%
%   jitter: n vectors will be generated for each event, where each element
%   vector is randomly selected from the lower quartile, median or upper
%   quartile of values within the window. (default: 1 - only 1 vector using
%   the median is generated for each event)
%
%   jitter_p: jittered vectors will have jitter_p proportion of values
%   randomly replaced with the lower and upper quartile value. (default:
%   0.1, where 0.05 are replaced by lower, and 0.05 are replaced by upper)
%
%   bias: when jittering, the lower and upper quartile values will be
%   pulled towards the median value with a weighting of bias:1. (default:
%   2, meaning that each jittered value is weighted 2:1 in favour of the
%   median)
%
% Sample Usage: 
% for i=1:12
%   DAT{i}.expinfo=eio{i};
%   DAT{i}.mat=SCALED{i};
% end
% hifam=[11 21 31]; %Condition codes for hi familiar Semcat experiment
% lofam=[12 22 32];
% TR=2.047; %TR in the semcat experiment
% DROPVOLS=4; %We dropped the first 4 volumes when processing the data
% TSTagger('tr', TR, 'volumes_dropped', DROPVOLS, 'condition', ...
%      hifam, 'dat', DAT); 

% define defaults at the beginning of the code so that you do not need to
% scroll way down in case you want to change something or if the help is
% incomplete
options = struct('tr', 0,'volumes_dropped', 0, 'condition', 0, 'cmap', [], 'dat', [], 'precision', 3, 'jitter', 1, 'jitter_p', .10, 'bias', 2, 'duration', 5);
 
% read the acceptable names
optionNames = fieldnames(options);

% count arguments
nArgs = length(varargin);
if round(nArgs/2)~=nArgs/2
    error('TSTagger needs propertyName/propertyValue pairs')
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

if (isempty(options.dat))
    error('No taggable data or incorrect data provided');
end

%Ensure volumes_dropped is either a single value, or else has a value for
%each .mat file
if(length(options.volumes_dropped)>1 && ...
        length(options.volumes_dropped)<length(options.dat))
    error('You are tagging %d runs, but specified volumes_dropped for only %d of them', ...
        length(options.dat), length(options.volumes_dropped));    
end

%Finally, if any volumes are dropped, we need a TR in order to interpet the
%TR in terms of timestamps
if(options.tr==0)
    error('You must specify the TR!');
end

upsample=4; %measurements per TR
offsetseconds=1; %seconds
windowsize=options.duration; %seconds

%Should be good to go. Iterate through all files
here=pwd();

for r=1:numel(options.dat)
    d=options.dat{r};
    mat=d.mat;
    expinfo=d.expinfo;
    %We may have a CONDITON on our hands...
    if isfield(expinfo.data, 'conditon')
        [expinfo.data.condition] = expinfo.data.conditon;
    end
    
    %Figure out how many volumes were dropped from the data to modify
    %timestamps
    if(length(options.volumes_dropped)>1)
        dvols=options.volumes_dropped(r);
    else
        dvols=options.volumes_dropped;
    end
    tempts=[expinfo.data.timestamp];
    tempcn=[expinfo.data.condition];
    %Calculate timestamp correction for dropped volumes
    timecorr = options.tr * dvols;
    tempts=tempts - timecorr;
    %Now convert timestamps to volumes at original sampling rate
    vols=tempts/options.tr;
    
    %4x the sampling rate of the timeseries (e.g., TR=2 -> TR=0.5)
    upmat=zeros( upsample * size(mat,1), size(mat,2) );
    for region=1:size(mat,2)
        upmat(:,region)=interp( mat(:,region), upsample );
    end
    upvols=round( vols * upsample ); %upsample volume indices
    
    targets=ismember(tempcn,options.condition);
    targetvols=upvols(targets);
    targettags=tempcn(targets);
    numpatterns=options.jitter*length(find(targets));
    taggeddata=nan(numpatterns,size(mat,2)+1); %preallocate tagged data matrix
    window_lo=upsample*offsetseconds;
    window_hi=window_lo+upsample*windowsize;
    tagged_rowidx=0; %this is the easiest way to track which row(s) the next event is being written to
    for c=1:length(targetvols)
        tagged_row_start=tagged_rowidx+1;
        tagged_row_end=tagged_rowidx+options.jitter;
        %preallocate matrix to hold desired number of patterns for event
        thesepatterns=nan(options.jitter,size(mat,2));
        thistag=double(targettags(c));
        timewindow=(window_lo:window_hi)+targetvols(c);
        %What if your time window extends past the end of the BOLD data?
        timewindow(timewindow>size(upmat,1))=[]; %delete offending indices
        if(length(timewindow)<5)
            continue; %if we end up with a useless snippet just skip this event
        end
        timeclip=upmat(timewindow,:);
        medclip=median(timeclip);
        %upperclip will be the top quartile
        upperfilter=(timeclip>medclip);
        upperclip=timeclip;
        upperclip(~upperfilter)=nan;
        upperclip=nanmedian(upperclip);
         %lowerclip will be the lower quartile
        lowerfilter=(timeclip<medclip);
        lowerclip=timeclip;
        lowerclip(~lowerfilter)=nan;
        lowerclip=nanmedian(lowerclip);
        timeclip=[lowerclip;medclip;upperclip]; %3 possible vals (lo,med,hi) for each region
        if(options.jitter==1)
            %if we just want one pattern (the median) per event:
            thesepatterns=[timeclip(2,:), thistag];
        else
            %we want multiple patterns per event:
            thesepatterns=nan(options.jitter,size(mat,2)+1); %preallocate for speed
            rowsel=nan(1,size(mat,2));
            %10 percent of values will be shifted towards lower quartile
            %10 percent will be shifted towards upper quartile
            part1=floor(length(rowsel) * (options.jitter_p/2.0));
            part2=part1*2;
            rowsel(1:part1)=1;
            rowsel(part1+1:part2)=3;
            rowsel(part2+1:end)=2;
            thesepatterns(1,:)=[timeclip(2,:), thistag]; %first pattern is the median
            %subsequent patterns are jitters of the median
            for patidx=2:options.jitter
                tempcol=randperm(size(mat,2));
                temprow=rowsel(tempcol); %randomized vector of rows e.g., 1,1,3,2,1,3,...
                thispattern=nan(1,length(tempcol));  
                thispattern(temprow==1)=timeclip(1,temprow==1);
                thispattern(temprow==2)=timeclip(2,temprow==2);
                thispattern(temprow==3)=timeclip(3,temprow==3);
                thispattern=mean([thispattern;timeclip(2,:);timeclip(2,:)]); %pull the pattern towards the median
                thispattern(thispattern<0)=0; %the values should be bound by 0 and 1
                thispattern(thispattern>1)=1;
                thesepatterns(patidx,:)=[round(thispattern, options.precision) thistag];
            end  
        end
        %at this point, we have either a 1x(nodes+tags) or a
        %jitteredx(nodes+tags) matrix called thesepatterns
        %append these patterns to the list
        taggeddata(tagged_row_start:tagged_row_end,:)=round(thesepatterns, options.precision);
        tagged_rowidx=tagged_rowidx+options.jitter; %update our index for the next event
    end
    %write out tagged data to CSV;
    prefix=sprintf('%s_%03d', expinfo.subject, expinfo.run);
    csvwrite([prefix '.csv'], taggeddata);
end


end
