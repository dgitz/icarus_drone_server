%trainnetwork

l = 0;
t1 = tic;
%classnet.trainparam.showcommandline = true
save_net = true;
NEURONS = 40;
clear classnet
clear classnets
trainingcomplete = false;
classnet = patternnet(NEURONS,TRAINFCN_CLASS);
EMAILS = false;
classnet.trainparam.max_fail = 100;
classnet.trainparam.epochs = 3000;
classnet = train(classnet,TrainClassMatrix,TargetClassTrainMatrix);
save_net = false;
while(~trainingcomplete)
    l = l + 1;
    %view(net)
    y = classnet(TrainClassMatrix);
    perf = perform(classnet,TargetClassTrainMatrix,y);
    classes = vec2ind(y);
    sum = 0;
    for i = 1:length(classes)
        if TargetClassTrainMatrix(classes(i),i) == 1
            sum = sum + 1;
        else
        end
    end
    loop(l).accuracy = (100*sum)/length(classes);
    tempstr = ['training iteration ' num2str(l) ': ' num2str(loop(l).accuracy) '/' num2str(train_limit) '%'];
    NETNAME = ['classnet_' datestr(now,'mm-dd-yyyy_HH-MM-SS')];
    classnets(l).net = classnet;
    classnets(l).accuracy = loop(l).accuracy;
    classnets(l).name = NETNAME;
    disp(tempstr);
    if loop(l).accuracy > train_limit
        networkstatus = true;
        trainingcomplete = true;
        NETNAME = ['classnet_' datestr(now,'mm-dd-yyyy_HH-MM-SS')];
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
        classnet = train(classnet,TrainClassMatrix,TargetClassTrainMatrix);
    end
end
finishtime = toc(t1);
[a,index] = max([classnets(:).accuracy]);
classnet = classnets(index).net;
NETNAME = classnets(index).name;
accuracy = classnets(index).accuracy;

if accuracy > TRAIN_LIMIT_MIN
    save_net = true;
fprintf(ResultFileID,['classnet,' NETNAME ',' TRAINFCN_CLASS ',' num2str(finishtime) ',' num2str(accuracy) ',' num2str(train_limit) ',' num2str(l) ',' Script ',' getComputerName, ',' num2str(NEURONS) '\r\n']);
disp(['total training time: ' num2str(finishtime)])
end