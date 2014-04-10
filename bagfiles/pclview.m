%PCL Viewer
close all
clear variables
clc
addpath 'matpcl';
pcl_folder = 'pointclouds4';
pcl_files = dir(pcl_folder);
pcl_files(1) = [];
pcl_files(1) = [];
cloud = [];
for i = 1:length(pcl_files)
    cloud = [cloud loadpcd([pcl_folder '/' pcl_files(i).name])];
end
[a,b] = size(cloud);
% for i = 1:b
%     if max(cloud(:,i)) > 10
%         cloud(:,i) = [];
%     end
% end
scatter3(cloud(1,1:1000),cloud(2,1:1000),cloud(3,1:1000))