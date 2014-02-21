function [ B ] = randomizelist( A )
%Randomize Collection
L = randperm(length(A));
for i = 1:length(L)
    B(i) = A(L(i));
end

end