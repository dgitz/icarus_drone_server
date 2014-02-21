function [ newim ] = preprocess( im,script )
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
if script == 'Script1'
newim = rgb2gray(im);
newim = imresize(newim,.25);
elseif script == 'Script2'
    newim = imresize(im,.5);
    newim = rgb2hsv(newim);
    newim = newim(:,:,3);
    newim = im2bw(newim,.8);
end
end

