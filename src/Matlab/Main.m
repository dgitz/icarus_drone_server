%Main.m
%Main
close all
clear variables
clc
main_run = true;

NetworkStatus = false;
SCALE_FACTOR = .5;
TRAIN_LIMIT_MAX = 92;
SUB_GRIDS = 9; %SUB_GRIDS^.5 SHOULD BE AN INTEGER
train_limit = TRAIN_LIMIT_MAX;
EMAILS = true;
TRAINFCN_CLASS = 'trainscg';
saveimages = false;
SHOW_IMAGES = true;
MAKE_MOVIE = false;
Script = 'Script2';
if ~SHOW_IMAGES
    MAKE_MOVIE = false;
end
RATIO = .75;
PAUSES = false;
SHUFFLE = true;
ResultFileID = fopen('Results.csv','at');
trainfcns = {'traingd','trainscg','traincgf','traincgp','traingda','traingdm','traingdx','trainoss'}
while(main_run)
    
    SampleName = 'IARC';
    choice = input('What would you like to do? \n[P]ick Pixel Targets \n[L]oad Network \nTrain [C]lassification Network \nTrain [O]bject Localizing Network \nA[U]tomated Training \n[A]cquire Images \n or [E]xit. ','s');
    switch choice
        case 'P'
            PickTargetPixels;
        case 'E'
            main_run = false;
            break;
        case 'L'
            LoadTrainingSamples;
            choice = input('[C]lassifier Network or [O]bject Localizing Networks? ','s');
            switch choice
                case 'C'
                    LoadClassNetwork;
                    NetworkStatus = true;
                case 'O'
                    LoadObjectNetwork;
                    NetworkStatus = true;
            end      
        case 'A'
            AcquireImage
            main_run = false;
            break;
        case 'C'
            LoadTrainingSamples;
            TrainClassNetwork;
            SaveClassNetwork;
            NetworkStatus = true;
        case 'O'
            LoadTrainingSamples;
            TrainObjectNetwork;
        case 'U'
            LoadTrainingSamples;
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
                            TrainObjectNetwork;
                            SaveObjectNetwork;
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