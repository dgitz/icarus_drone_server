%trainnetwork

l = 0;
t1 = tic;
%classnet.trainparam.showcommandline = true
NEURONS = 20;
clear classnet
trainingcomplete = false;
classnet = patternnet(NEURONS,TRAINFCN_CLASS);
EMAILS = false;
classnet.trainparam.max_fail = 100;
classnet.trainparam.epochs = 3000;
classnet = train(classnet,TrainMatrix,TargetTrainMatrix);
while(~trainingcomplete)
    l = l + 1;
    %view(net)
    y = classnet(TrainMatrix);
    perf = perform(classnet,TargetTrainMatrix,y);
    classes = vec2ind(y);
    sum = 0;
    for i = 1:length(classes)
        if TargetTrainMatrix(classes(i),i) == 1
            sum = sum + 1;
        else
        end
    end
    loop(l).accuracy = (100*sum)/length(classes);
    tempstr = ['training iteration ' num2str(l) ': ' num2str(loop(l).accuracy) '%'];
    disp(tempstr);
    if loop(l).accuracy > train_limit
        networkstatus = true;
        trainingcomplete = true;
        NETNAME = ['classnet_' datestr(now,'mm-dd-yy_HH-MM-SS')];
        if EMAILS
            %send_mail_message('davidgitz','Finished training network',['Finished training ', TRAINFCN_CLASS, ' network with ', num2str(loop(l).accuracy) '% accuracy.']);
        end
    else
        if mod(l,2) == 0
            train_limit = train_limit * .99;
            if EMAILS
                send_mail_message('davidgitz','continuing to train network ',[tempstr ' with accuracy decreased to: ' num2str(train_limit)]);
            end
        end
        classnet = init(classnet);
        classnet = train(classnet,TrainMatrix,TargetTrainMatrix);
    end
end
finishtime = toc(t1);
fprintf(ResultFileID,['classnet,' NETNAME ',' num2str(finishtime) ',' num2str(loop(l).accuracy) ',' num2str(train_limit) ',' num2str(l) ',' Script '\r\n']);
disp(['total training time: ' num2str(finishtime)])