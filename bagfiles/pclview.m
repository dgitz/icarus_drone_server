%PCL Viewer
close all
clear variables
clc
addpath 'matpcl';
pcl_folder = 'pointclouds2';
pcl_files = dir(pcl_folder);
pcl_files(1) = [];
pcl_files(1) = [];
cloud = [];
for i = 1:length(pcl_files)
    cloud = [cloud loadpcd([pcl_folder '/' pcl_files(i).name])];
end
scatter3(cloud(1,:),cloud(2,:),cloud(3,:))