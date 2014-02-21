%Save Classifier Network

disp(['Trained Network: ' NETNAME])
classnet.name = [NETNAME];
save([pwd '/../../trained_nets/' NETNAME],'classnet');
if EMAILS
    send_mail_message('davidgitz','Finished training network',['Finished training ' NETNAME ' network of type: ' TRAINFCN_CLASS ' with ', num2str(loop(l).accuracy) '% accuracy.']);
end