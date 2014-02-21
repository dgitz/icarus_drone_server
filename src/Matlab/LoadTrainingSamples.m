%LoadTrainingSamples
SampleName = 'IARC';
RATIO = .75;
trainitems(1).class = '';
trainitems(1).path = '';
trainitems(1).origimage = [];
trainitems(1).procimage = [];
trainitems(1).vector = [];
switch SampleName
    case 'IARC'
        t1 = tic;
        VectorCount = 0;
        VectorLength = 0;
        traindir = [pwd '/../../media/RealImages/'];
        environdir = [pwd '/../../media/EnvironmentImages/'];
        folderlist = dir(traindir);
        folderlist(1) = [];
        folderlist(1) = [];
        filelist = [];
        index = 0;
        for i = 1:length(folderlist)
            mydir = [traindir folderlist(i).name];
            Answers{i} = folderlist(i).name;
            mylist = dir(mydir);
            mylist(1) = [];
            mylist(1) = [];
            for j = 1:length(mylist)
                index = index + 1;
                trainitems(index).class = folderlist(i).name;
                trainitems(index).path = [mydir '/' mylist(j).name];
                
                %trainitem(index).origimage = imread(trainitem(index).path);
            end        
        end
        mylist = dir(environdir);
        mylist(1) = [];
        mylist(1) = [];
        Answers{length(Answers)+1} = 'None';
        index = length(trainitems);
        for j = 1:length(mylist)
            index = index + 1;
            trainitems(index).class = 'None';
            trainitems(index).path = [environdir '/' mylist(j).name];
            
        end
        for j = 1:length(trainitems)
            trainitems(j).origimage = imread(trainitems(j).path);
            trainitems(j).procimage = preprocess(trainitems(j).origimage,Script);
            trainitems(j).vector = reshape(trainitems(j).procimage,[],1);
            disp(['Loaded: ' num2str(j) '/' num2str(length(trainitems)) ' patterns.']);
        end
        if SHUFFLE
            trainitems = randomizelist(trainitems);
        end
        VectorCount = length(trainitems);
        VectorLength = length(trainitems(1).vector);
        TrainVectorCount = round(RATIO*VectorCount); 
        TestVectorCount = VectorCount-TrainVectorCount;
        TrainMatrix = zeros(VectorLength,TrainVectorCount);
        TestMatrix = zeros(VectorLength,TestVectorCount);
        TargetTrainMatrix = zeros(length(Answers),TrainVectorCount);
        TargetTestMatrix = zeros(length(Answers),TestVectorCount);
        trainindex = 0;
        testindex = 0;
        for i = 1:length(trainitems)
            if i <= TrainVectorCount
                trainindex = trainindex + 1;
                TrainMatrix(:,trainindex) = trainitems(i).vector;
            else
                testindex = testindex + 1;
                TestMatrix(:,testindex) = trainitems(i).vector;
            end
        end
        trainindex = 0;
        testindex = 0;
        for i = 1:VectorCount
            for j = 1:length(Answers)
                if strcmp(Answers{j}, trainitems(i).class)
                    if i <= TrainVectorCount
                        trainindex = trainindex + 1;
                        TargetTrainMatrix(j,trainindex) = 1;
                    else
                        
                        testindex = testindex + 1;
                        TargetTestMatrix(j,testindex) = 1;
                    end
                end
            end
        end
end

