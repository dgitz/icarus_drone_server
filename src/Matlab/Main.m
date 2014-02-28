%Main.m
%Main
close all
clear variables
clc
SHUFFLE = true;
ROWS = 6;
COLS = 6;
Script = 'Script4';
%SCALE_FACTOR = .5;
SHOW_IMAGES_LOAD = false;
SHOW_IMAGES_RUN = true;
LoadTrainingSamples;
%pack
%keep trainitems Script SHUFFLE TargetTestMatrix TargetTrainMatrix TrainMatrix TestMatrix
main_run = true;

NetworkStatus = false;

TRAIN_LIMIT_MAX = 92;
TRAIN_LIMIT_MIN = 50;
SUB_GRIDS = 9; %SUB_GRIDS^.5 SHOULD BE AcN INTEGER
train_limit = TRAIN_LIMIT_MAX;
EMAILS = true;
TRAINFCN_CLASS = 'trainscg';
saveimages = false;

MAKE_MOVIE = false;

if ~SHOW_IMAGES_RUN
    MAKE_MOVIE = false;
end
RATIO = .75;
PAUSES = false;

ResultFileID = fopen([pwd '/Results/ ' datestr(now,'mm-dd-yyyy_HH-MM-SS') '.csv'],'wt');
trainfcns = {'traingd','trainscg','traincgf','traincgp','traingda','traingdm','traingdx','trainoss'}
while(main_run)
    
    SampleName = 'IARC';
    %choice = input('What would you like to do? \n[P]ick Pixel Targets \n[L]oad Network \nTrain [C]lassification Network \nTrain [O]bject Localizing Network \nA[U]tomated Training \n[A]cquire Images \n or [E]xit. ','s');
    choice = input('What would you like to do? \n[T]est Image Processing \nTrain [L]ocalizing Network \nTrain [C]lassification Network \nA[U]tomated Training \nor [E]xit. ','s');
    
    switch choice
        case 'T'
            TestImagePreProcess
            NetworkStatus = false;
        case 'P'
            PickTargetPixels;
        case 'E'
            main_run = false;
            break;
        case 'L'
            TrainClassNetwork;
        case 'A'
            AcquireImage
            main_run = false;
            break;
        case 'C'
            TrainClassNetwork;
            SaveClassNetwork;
            NetworkStatus = true;
        case 'O'
            TrainObjectNetwork;
        case 'U'
            choice = input('[C]lassifier Network or [O]bject Localizing Networks? ','s');
            for i = 1:length(trainfcns)
                train_limit = TRAIN_LIMIT_MAX;
                try
                    TRAINFCN_CLASS  =trainfcns{i};
                    tempstr = ['Training with ' TRAINFCN_CLASS ' training function.'];
                    disp(tempstr)
                    switch choice
                        case 'C'
                        TrainClassNetwork;
                        SaveClassNetwork;
                        case 'O'
                            TrainLocalizingRowNetwork;
                            TrainLocalizingColNetwork;
                            SaveLocalizingNetwork;
                    end
                    NetworkStatus = true;
                catch err
                    disp(err);
                end
            end
    end
    if NetworkStatus
        choice = input('What would you like to do? \n[S]tart Over \n[L]ive Run \n[T]est Network \n[G]enerate XML \nS[A]ve Net \n or [E]xit. ','s');
        switch choice
            case 'T'
                choice = input('[C]lassifier Network or [O]bject Localizing Networks? ','s');
                switch choice
                    case 'C'
                        TestClassNetwork;
                    case 'O'
                        TestObjectNetwork;
                end           
            case 'A'
                SaveClassNetwork
            case 'S'
                break;
            case 'E'
                run = false;
                break;
            case 'L'
                LiveRun;
            case 'G'
                choice = input('[C]lassifier Network [O]bject Localizing Networks? ','s');
                switch choice
                    case 'C'
                        GenerateNetXML( classnet,Answers );
                    case 'O'
                        %GenerateNetXML(
                end
        end
    end
end
fclose(ResultFileID);