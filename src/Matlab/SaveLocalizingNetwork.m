%Save Localizing Network
if save_rownet
    disp(['Trained Network: ' ROWNAME])
    rownet.name = [ROWNAME];
    save([pwd '/../../trained_nets/' ROWNAME],'rownet');
    if EMAILS
        send_mail_message('davidgitz','Finished training network',['Finished training ' ROWNAME ' network of type: ' TRAINFCN_CLASS ' with ', num2str(loop(l).row_accuracy) '% accuracy.']);
    end
end
if save_colnet
    disp(['Trained Network: ' COLNAME])
    colnet.name = [COLNAME];
    save([pwd '/../../trained_nets/' COLNAME],'colnet');
    if EMAILS
        send_mail_message('davidgitz','Finished training network',['Finished training ' COLNAME ' network of type: ' TRAINFCN_CLASS ' with ', num2str(loop(l).col_accuracy) '% accuracy.']);
    end
end