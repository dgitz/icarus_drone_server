function [ newim ] = preprocess( im,script,factor )
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
if script == 'Script1'
newim = rgb2gray(im);
newim = imresize(newim,.5);
elseif script == 'Script2'
    newim = imresize(im,.5);
    newim = rgb2hsv(newim);
    newim = newim(:,:,3);
    newim = im2bw(newim,.8);
elseif script == 'Script3'
    
    filter = rgb2hsv(im);

    filter = filter(:,:,3);
    filter = im2bw(filter,.8);
    filter = double(filter)/255;
    newim = zeros(size(im));
    
    newim(:,:,1) = double(im(:,:,1)) .* filter;
    newim(:,:,2) = double(im(:,:,2)) .* filter;
    newim(:,:,3) = double(im(:,:,3)) .* filter;
    newim = 255*newim;
    newim = rgb2gray(newim);
end
end

