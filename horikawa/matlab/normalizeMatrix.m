function Z=normalizeMatrix(M, droprows)
%normalizeMatrix takes a 3D matrix or cell array of 2D matrices, M,
%normalizes the values (i.e., applies zscore() to M(:,:,n) for 3D array, or
%to M{n} for cell array. The function additionally drops the rows from all  indicated
%in the droprows matrix. If droprows is omitted, all rows are retained
%prior to normalizing.
%
% Required arguments:
%   M:          a 3D matrix or a nx1 or 1xn cell array where each cell M{n}
%               contains a 2D array
% Optional arguments:
%   droprows:   an array of row indices to be omitted from M, PRIOR TO
%               normalizing. In order to permit convenient indexing from 
%               the end of a matrix with an unknown or variable number of
%               rows, droprows can contain index values less than 1, which
%               will be interpreted as indices relative to the last row of
%               the array.
%
% Outputs:
%   Z: an array of the same format as M, but containing normalized values.
%       Each 2D array is normalized along the columns (i.e., the value in
%       each cell for array n is the zscore calculated over M(:,c,n)
%
% Sample usage using a cell array containing 2D matrices of different size:
% M{1}=magic(10);
% M{2}=magic(12);
% M{3}=magic(14);
% droprows=[-2 -1 0 1 2 3]; %omit rows 1, 2, 3 and end, end-1 and end-2
% Z=normalizeMatrix(M, droprows);
% 
% Z=normalizeMatrix(M); %as above, but without dropping any rows
%
if (~exist('droprows','var'))
    droprows=[];
end

if (~iscell(M))
    %M is not a cell array, which is the easiest case
    M=dropRows(M, droprows);
    Z=zscore(M);%drop rows as required, then zscore
else
    if(iscell(M))
        %M is a cell array, so we have to apply droprows and zscore to each
        %cell element
        M=cellfun(@(x) dropRows(x, droprows), M, 'UniformOutput', false);
        Z=cellfun(@zscore, M, 'UniformOutput', false);
    end
end

%% Nested utility function dropRows(M,droprows)
    function M=dropRows(M,droprows)
        %receives matrix M and drops rows indexed by positive values in
        %droprows, and indexed from the end (e.g., M(end-1,:) for values
        %less than 1
        sz=size(M);
        keeprows=1:size(M,1); %rows to keep
        %convert negative droprows indices into end-relative values
        droprows=[droprows(droprows>0) droprows(droprows<1)+size(M,1)];
        keeprows(droprows)=[];%removes from rows to keep the set of rows to drop
        M=M(keeprows, :); %keep only the rows not flagged to be dropped
        %if M was 3D+, it will need to be reshaped
        sz(1)=size(M,1); %new number of rows in sz matrix, all other dimensions maintained as they were
        M=reshape(M, sz);
    end
end