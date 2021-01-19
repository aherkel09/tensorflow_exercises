function [BIN, SCALED]=binarizeMatrix(Z, varargin)
%function [BIN, SCALED]=binarizeMatrix(Z, thresh, clip)
%binarizeMatrix takes a normalized matrix, Z, and scales and binarizes its
%elements: 
%positive values are set to 1 and negative values ar set to 0. If thresh is
%set to a nonzero value, elements with an absolute value less than thresh
%are set to NaN. If a clipping value, clip, is provided, elements with an
%absolute value exceeding clip are first set to NaN before binarizing.
%Required Parameters:
%   Z: a normalized matrix or cell array
%
%Optional Parameters:
%   thresh: the z-score threshold above which the absolute values of the
%       normalized values in Z will be set to 1 (for positive values above the
%       threshold) or 0 (for negative values below the negative threshold)
%   clip:   the z-score above which the absolute values will be set to NaN
%   precision: values are rounded to PRECISION decimal points
%Sample usage:
%thresh=1.96;
%clip=3.0;
%[BIN, SCALED]=binarizeMatrix(Z, 'thresh', thresh, 'clip', clip, 'precision', 2);
%
options = struct('thresh',1, ...
    'clip', inf, ...
    'precision', 1);

% read the acceptable names
optionNames = fieldnames(options);

% count arguments
nArgs = length(varargin);
if (isstruct(varargin))
    options=varargin;
else
    if round(nArgs/2)~=nArgs/2
        error('This function needs propertyName/propertyValue pairs')
    end
    
    for pair = reshape(varargin,2,[]) % pair is {propName;propValue}
        inpName = lower(pair{1}); % make case insensitive
        
        if any(strcmp(inpName,optionNames))
            % overwrite defaults
            options.(inpName) = pair{2};
        else
            error('%s is not a recognized parameter name',inpName)
        end
    end
end

if(options.thresh==0)
    options.thresh=realmin; %workaround to allow a threshold of approx. zero
end
if (~iscell(Z))
    %Z is not a cell array, which is the easiest case
    SCALED=scaleMatrix(Z,options.clip, options.thresh, options.precision);
    BIN=SCALED;
    BIN(0<BIN & BIN<1)=nan;
else
    if(iscell(Z))
        %M is a cell array, so we have to apply droprows and zscore to each
        %cell element
        SCALED=cellfun(@(x) scaleMatrix(x, options.clip, options.thresh, options.precision), Z, 'UniformOutput', false);
        BIN=cellfun(@(x) nanBin(x), SCALED, 'UniformOutput', false);
    end
end

%%Nested utility function scale matrix
    function SM=scaleMatrix(M, clip, thresh, precision)
        M(abs(M)>clip)=nan; %remove items to be clipped
        M=M/thresh;%scale in terms of thresholds
        M(M>1)=1;%anything above +threshold=1
        M(M<-1)=-1; %anything below -threshold=-1
        M=M+1;%shift values from range -1:1 to 0:2
        M=M/2;%now values range from 0:1
        %subtly shift values so that mean value for each column is ~0.5
        meansignal=nanmean(M);%what is the current mean of each column?
        %use log to determine exponent required to shift each mean to 0.5
        centerexp=repmat(power(log10(meansignal),-1).*log10(0.5),size(M,1),1);
        %raise each value to the required exponent. 0s and 1s will be
        %unaffected
        precis=power(10,precision);
        SM=round(precis*M.^centerexp)/precis;
        
    end
%%Nested utility function sets all non 0-1 values to nan
    function BIN=nanBin(M)
        BIN=M;
        BIN(0<BIN & BIN<1)=nan;
    end
end