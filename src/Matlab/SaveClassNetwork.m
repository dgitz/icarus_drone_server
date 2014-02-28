%Save Classifier Network
if save_net
    disp(['Trained Network: ' NETNAME])
    classnet.name = [NETNAME];
    save([pwd '/../../trained_nets/' NETNAME],'classnet');
    if EMAILS
        send_mail_message('davidgitz','Finished training network',['Finished training ' NETNAME ' network of type: ' TRAINFCN_CLASS ' with ', num2str(accuracy) '% accuracy.']);
    end
end