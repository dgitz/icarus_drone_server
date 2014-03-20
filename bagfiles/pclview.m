%PCL Viewer
close all
clear variables
clc
addpath 'matpcl';
pcl_folder = 'pointclouds1';
pcl_files = dir(pcl_folder);
pcl_files(1) = [];
pcl_files(1) = [];
clouds = [];
for i = 1:length(pcl_files)
    clouds = [clouds loadpcd([pcl_folder '/' pcl_files(i).name])];
end
scatter3(clouds(1,:),clouds(2,:),clouds(3,:))