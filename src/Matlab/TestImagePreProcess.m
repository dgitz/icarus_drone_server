%TestImagePreProcess
close all
clear variables
clc
Script = 'Script2';
SHUFFLE = false;
LoadTrainingSamples;
keep trainitems
skip = floor(length(trainitems)/100);
for i = 1:length(trainitems)
    if mod(i,skip) == 0
        figure(1)
        title(['Image: ' num2str(i) '/' num2str(length(trainitems)) ' Class: ' trainitems(i).class]);
        hold on
        subplot(2,1,1)
        imshow(trainitems(i).origimage);
        subplot(2,1,2)
        imshow(trainitems(i).procimage);
        pause(.1)
    end
end