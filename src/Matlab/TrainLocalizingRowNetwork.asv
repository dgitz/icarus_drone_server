%trainnetwork

l = 0;
t1 = tic;
%classnet.trainparam.showcommandline = true
NEURONS = 80;
clear rownet
clear rownets
clear loop
trainingcomplete = false;
rownet = patternnet(NEURONS,TRAINFCN_CLASS);
rownet = init(rownet);
EMAILS = false;
train_limit = TRAIN_LIMIT_MAX;
save_rownet = false;
while(~trainingcomplete)
    l = l + 1;
    rownet.trainparam.max_fail = 100;
    rownet.trainparam.epochs = 30000;
    if strcmp(TRAINFCN_CLASS,'trainscg')
        dumb = 1
    else
        rownet.trainparam.lr = .001;
    end
    TRAINFCN_CLASS
    rownet.trainparam.lr
    rownet = train(rownet,TrainLocalizingRowMatrix,TargetLocalizingRowTrainMatrix);
    yrow = rownet(TrainLocalizingRowMatrix);
    
    perfrow = perform(rownet,TargetLocalizingRowTrainMatrix,yrow);
    classesrow = vec2ind(yrow);
    
    sum = 0;
    for i = 1:length(classesrow)
        if TargetLocalizingRowTrainMatrix(classesrow(i),i) == 1
            sum = sum + 1;
        else
        end
    end
    loop(l).row_accuracy = 100*(sum)/length(classesrow);
    tempstr = ['Row training iteration ' num2str(l) ': ' num2str(loop(l).row_accuracy) '/' num2str(train_limit) '%'];
    disp(tempstr);
    ROWNAME = ['rownet_' datestr(now,'mm-dd-yyyy_HH-MM-SS')];
    rownets(l).net = rownet;
    rownets(l).name = ROWNAME;
    rownets(l).accuracy = loop(l).row_accuracy;
    
    if (loop(l).row_accuracy > train_limit)
        networkstatus = true;
        trainingcomplete = true;
        
        if EMAILS
            %send_mail_message('davidgitz','Finished training network',['Finished training ', TRAINFCN_CLASS, ' network with ', num2str(loop(l).accuracy) '% accuracy.']);
        end
    elseif train_limit < TRAIN_LIMIT_MIN
        networkstatus = true;
        trainingcomplete = true;
    else    
        
        if mod(l,2) == 0
            train_limit = train_limit * .99;
            if EMAILS
                send_mail_message('davidgitz','continuing to train network ',[tempstr ' with accuracy decreased to: ' num2str(train_limit)]);
            end
        end
        rownet = init(rownet);       
        
    end
end

finishtime = toc(t1);
[a,index] = max([rownets(:).accuracy]);
rownet = rownets(index).net;
ROWNAME = rownets(index).name;
accuracy = rownets(index).accuracy;

if accuracy > TRAIN_LIMIT_MIN
    save_rownet = true;
    fprintf(ResultFileID,['rownet,' ROWNAME ',' TRAINFCN_CLASS ',' num2str(finishtime) ',' num2str(accuracy) ',' num2str(train_limit) ',' num2str(l) ',' Script ',' getComputerName num2str(NEURONS) '\r\n']);
    disp(['total training time: ' num2str(finishtime)])
end