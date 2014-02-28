%trainnetwork

l = 0;
t1 = tic;
%classnet.trainparam.showcommandline = true
NEURONS = 80;
clear colnet
clear colnets
clear loop
trainingcomplete = false;
colnet = patternnet(NEURONS,TRAINFCN_CLASS);
colnet = init(colnet);
EMAILS = false;
train_limit = TRAIN_LIMIT_MAX;
save_colnet = false;
while(~trainingcomplete)
    l = l + 1;
    
    
    colnet.trainparam.max_fail = 100;
    colnet.trainparam.epochs = 30000;
    if strcmp(TRAINFCN_CLASS,'trainscg')
        dumb = 1
    else
        colnet.trainparam.lr = .1;
    end
    TRAINFCN_CLASS
    colnet.trainparam.lr
    [colnet,result] = train(colnet,TrainLocalizingColMatrix,TargetLocalizingColTrainMatrix);
    ycol = colnet(TrainLocalizingColMatrix);
    classescol = vec2ind(ycol);
    sum = 0;
    for i = 1:length(classescol)
        if TargetLocalizingColTrainMatrix(classescol(i),i) == 1
            sum = sum + 1;
        else
        end
    end
    loop(l).col_accuracy = 100*sum/length(classescol);
    
    tempstr = ['Column training iteration ' num2str(l) ': ' num2str(loop(l).col_accuracy) '/' num2str(train_limit) '%'];
    disp(tempstr);
    colnets(l).net = colnet;
    colnets(l).accuracy = loop(l).col_accuracy;
    COLNAME = ['colnet_' datestr(now,'mm-dd-yyyy_HH-MM-SS')];
    colnets(l).name = COLNAME;
    
    if  (loop(l).col_accuracy > train_limit)
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
        colnet = init(colnet);
        
    end
end
finishtime = toc(t1);
[a,index] = max([colnets(:).accuracy]);
colnet = colnets(index).net;
COLNAME = colnets(index).name;
accuracy = colnets(index).accuracy;

if accuracy > TRAIN_LIMIT_MIN
    save_colnet = true;
    fprintf(ResultFileID,['colnet,' COLNAME ',' TRAINFCN_CLASS ',' num2str(finishtime) ',' num2str(accuracy) ',' num2str(train_limit) ',' num2str(l) ',' Script ',' getComputerName ',' num2str(NEURONS) '\r\n']);
end
if save_rownet || save_colnet
    disp(['total training time: ' num2str(finishtime)])
end