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
        VectorClassCount = 0;
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
                tempstr = mylist(j).name(11:length(mylist(j).name));
                trainitems(index).centery = str2num(tempstr(1:findstr(tempstr,'_')-1));
                trainitems(index).centerx = str2num(tempstr(findstr(tempstr,'_')+1:findstr(tempstr,'.')-1));
                
 
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
        VectorLocalizingCount = 0;
        for index = 1:length(trainitems)
            trainitems(index).origimage = imread(trainitems(index).path);
            trainitems(index).procimage = preprocess(trainitems(index).origimage,Script);
            trainitems(index).vector = reshape(trainitems(index).procimage,[],1);
            if ~strcmp(trainitems(index).class,'None')
                VectorLocalizingCount = VectorLocalizingCount + 1;
                [height,width,c] = size(trainitems(index).origimage);
                trainitems(index).row = ceil(ROWS*trainitems(index).centery/height);
                trainitems(index).col = ceil(COLS*trainitems(index).centerx/width);
                if SHOW_IMAGES_LOAD
                    DrawGrid
                    
                end
            end
            disp(['Loaded: ' num2str(index) '/' num2str(length(trainitems)) ' patterns.']);
        end
        if SHUFFLE
            trainitems = randomizelist(trainitems);
        end
        VectorClassCount = length(trainitems);
        VectorLength = length(trainitems(1).vector);
        TrainVectorClassCount = round(RATIO*VectorClassCount); 
        TestVectorClassCount = VectorClassCount-TrainVectorClassCount;        
        TrainVectorLocalizingCount = round(RATIO*VectorLocalizingCount);
        TestVectorLocalizingCount = VectorLocalizingCount-TrainVectorLocalizingCount;
        
        TrainClassMatrix = zeros(VectorLength,TrainVectorClassCount);
        TestClassMatrix = zeros(VectorLength,TestVectorClassCount);
        TargetClassTrainMatrix = zeros(length(Answers),TrainVectorClassCount);
        TargetClassTestMatrix = zeros(length(Answers),TestVectorClassCount);
        
        TrainLocalizingRowMatrix = zeros(VectorLength,TrainVectorLocalizingCount);
        TestLocalizingRowMatrix = zeros(VectorLength,TestVectorLocalizingCount);
        TargetLocalizingRowTrainMatrix = zeros(ROWS,TrainVectorLocalizingCount);
        TargetLocalizingRowTestMatrix = zeros(ROWS,TestVectorLocalizingCount);
        TrainLocalizingColMatrix = zeros(VectorLength,TrainVectorLocalizingCount);
        TestLocalizingColMatrix = zeros(VectorLength,TestVectorLocalizingCount);
        TargetLocalizingColTrainMatrix = zeros(COLS,TrainVectorLocalizingCount);
        TargetLocalizingColTestMatrix = zeros(COLS,TestVectorLocalizingCount);
        
        trainindex = 0;
        testindex = 0;
        for i = 1:length(trainitems)
            if i <= TrainVectorClassCount
                trainindex = trainindex + 1;
                TrainClassMatrix(:,trainindex) = trainitems(i).vector;
            else
                testindex = testindex + 1;
                TestClassMatrix(:,testindex) = trainitems(i).vector;
            end
        end
        
        trainindex = 0;
        testindex = 0;
        for i = 1:length(trainitems)
            if ~strcmp(trainitems(i).class,'None')
                if trainindex < TrainVectorLocalizingCount
                    if trainindex >207
                    end
                    trainindex = trainindex + 1;
                    TrainLocalizingRowMatrix(:,trainindex) = trainitems(i).vector;
                    TrainLocalizingColMatrix(:,trainindex) == trainitems(i).vector;
                else
                    testindex = testindex + 1;
                    TestLocalizingRowMatrix(:,testindex) = trainitems(i).vector;
                    TestLocalizingColMatrix(:,testindex) = trainitems(i).vector;
                end
            end
        end
        
        trainindex = 0;
        testindex = 0;
        for i = 1:VectorLocalizingCount
            if ~strcmp(trainitems(i).class,'None')
                for j = 1:ROWS
                    if j == trainitems(i).row
                        if trainindex < TrainVectorLocalizingCount
                            trainindex = trainindex + 1;
                            TargetLocalizingRowTrainMatrix(j,trainindex) = 1;
                        else
                            testindex = testindex + 1;
                            TargetLocalizingRowTestMatrix(j,testindex) = 1;
                        end
                    end
                end
            end
        end
        trainindex = 0;
        testindex = 0;
        for i = 1:VectorLocalizingCount
            if ~strcmp(trainitems(i).class,'None')
                for j = 1:COLS
                    if j == trainitems(i).col
                        if trainindex < TrainVectorLocalizingCount
                            trainindex = trainindex + 1;
                            TargetLocalizingColTrainMatrix(j,trainindex) = 1;
                        else
                            testindex = testindex + 1;
                            TargetLocalizingColTestMatrix(j,testindex) = 1;
                        end
                    end
                end
            end
        end
        trainindex = 0;
        testindex = 0;
        for i = 1:VectorClassCount
            for j = 1:length(Answers)
                if strcmp(Answers{j}, trainitems(i).class)
                    if i <= TrainVectorClassCount
                        trainindex = trainindex + 1;
                        TargetClassTrainMatrix(j,trainindex) = 1;
                    else
                        
                        testindex = testindex + 1;
                        TargetClassTestMatrix(j,testindex) = 1;
                    end
                end
            end
        end
end

