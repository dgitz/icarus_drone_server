#!/usr/bin/python

#import roslib
import os
import time
import imp
import random
import pybrain
import pdb
import cv2
import numpy as np
import math
from pybrain.datasets import ClassificationDataSet
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer
from pybrain.structure.modules import TanhLayer
from pybrain.structure.modules import SigmoidLayer
from optparse import OptionParser
from os import listdir
from os.path import isfile,join
import pickle
import time
import zipfile
import zlib
import pp


parser = OptionParser("trainnets.py [options]")
parser.add_option("--TrainNet",dest="TrainNets",default="ALL")#Options are: ALL,CLASSNET,ROWNET,COLNET
parser.add_option("--Verbose",dest="Verbose",default=False)
parser.add_option("--UseParallel",dest="UseParallel",default='True')
parser.add_option('--TrainMode',dest="TrainMode",default="Real",help="Real,Simulated")
(opts,args) = parser.parse_args()
TrainNets = opts.TrainNets
Verbose = opts.Verbose
if opts.UseParallel=='False':
	UseParallel=False
elif opts.UseParallel=='True':
	UseParallel=True
if opts.Verbose=='False':
	Verbose=False
elif opts.Verbose=='True':
	Verbose=True
<<<<<<< HEAD
packagepath = os.getcwd()
pdb.set_trace()
=======
packagepath = roslib.packages.get_pkg_dir('icarus_drone_server')
helperpath = packagepath + '/src/icarus_helper.py'
icarus_helper = imp.load_source('icarus_helper',helperpath)
>>>>>>> 53363936bc01a7bbbc8be849bc64d70695cb8be0
if opts.TrainMode=='Real':
	trainimage_dir = packagepath +'/media/RealImages/'
elif opts.TrainMode=='Simulated':
	trainimage_dir = packagepath +'/media/SimulatedImages/'

	names = listdir(trainimage_dir)
	names = sorted(names)
	for i in range(len(names)):
		print "{}. {}".format(i,names[i])
	choice = raw_input("Please Select a folder: ")
	if choice == '':
	  choice = len(names)-1
	else:
	  choice = int(choice)
	print 'Selected: {}'.format(names[choice])
	trainimage_dir = trainimage_dir + '/' + names[choice] + '/'
masterimage_dir = packagepath +'/media/MasterImages/'
environmentimage_dir = packagepath +'/media/EnvironmentImages/'
trainnednets_dir = packagepath +'/trained_nets/'
'''Global Variables'''
RESIZEFACTOR = 0.25
ROWSECTORS = 3
COLSECTORS = 3

ppservers = ()
job_server = pp.Server(4,ppservers=ppservers)

masterimage_names = [ f for f in os.listdir(masterimage_dir) if os.path.isfile(os.path.join(masterimage_dir,f)) ]
masterimage_paths = [''] * len(masterimage_names)
for i in range(len(masterimage_names)):
	masterimage_paths[i] = masterimage_dir + masterimage_names[i]
	masterimage_names[i] = masterimage_names[i][0:masterimage_names[i].find('.')]
masterimage_names.append('None')
tempfolder_classes = os.listdir(trainimage_dir)
trainitems = []

for f in range(len(tempfolder_classes)):
	temppath = trainimage_dir + tempfolder_classes[f] + '/'
	tempfiles = os.listdir(temppath)
	for t in range(len(tempfiles)):
		myclass = tempfolder_classes[f]
		mypath = temppath + tempfiles[t]
		myindex = 0#int(tempfiles[t][5:9])
		tempstr = tempfiles[t][tempfiles[t].find('_')+1:]
		mycentery = int(tempstr[0:tempstr.find('_')])
		mycenterx = int(tempstr[tempstr.find('_')+1:tempstr.find('.')])
		myorigimage = cv2.imread(mypath)
		myprocimage = icarus_helper.preprocess(myorigimage)		
		trainitems.append(icarus_helper.train_item(trainclass=myclass,trainindex=0,trainpath=mypath,traincenterx=mycenterx,traincentery=mycentery,trainorigimage=myorigimage,trainprocimage=myprocimage))
		
tempfiles = os.listdir(environmentimage_dir)

for t in range(len(tempfiles)):
	myclass = 'None'
	mypath = environmentimage_dir + tempfiles[t]
	myindex = 0
	mycentery = 0
	mycenterx = 0
	myorigimage = cv2.imread(mypath)
	myprocimage = icarus_helper.preprocess(myorigimage)
	trainitems.append(icarus_helper.train_item(trainclass=myclass,trainindex=0,trainpath=mypath,traincenterx=mycenterx,traincentery=mycentery,trainorigimage=myorigimage,trainprocimage=myprocimage))

class_data = []
for i in range(len(trainitems)):
	height,width = trainitems[i].trainprocimage.shape
	row = math.ceil(ROWSECTORS*float(trainitems[i].traincentery)/float(height*2))
	col = math.ceil(COLSECTORS*float(trainitems[i].traincenterx)/float(width*2))
	vector = trainitems[i].trainprocimage.reshape([1,height*width]).astype('int')
	class_data.append([trainitems[i].trainclass,vector,trainitems[i].trainprocimage])
	
random.shuffle(class_data)
#random.shuffle(loc_data)
class_names = []
class_vectors = []
loc_vectors = []
#loc_rows = []
#loc_cols = []

for d in range(len(class_data)):
	class_names.append(class_data[d][0])
	class_vectors.append(class_data[d][1])
'''for d in range(len(loc_data)):
	
	loc_rows.append('Row{}'.format(int(loc_data[d][0])))
	loc_cols.append('Column{}'.format(int(loc_data[d][1])))
	loc_vectors.append(loc_data[d][2])
'''
def savenet(name,net):
	filename = name +'_' + time.strftime("%Y_%m_%d_%H_%M_%S")
	writepath = trainnednets_dir + filename
	myfile = open((writepath+'.txt'),'w')
	pickle.dump(net,myfile)
	myfile.close
	zf = zipfile.ZipFile((writepath+'.zip'),mode='w')
	zf.write((writepath+'.txt'),compress_type=zipfile.ZIP_DEFLATED)
	zf.close()
	os.remove((writepath+'.txt'))
def testnet(name,net,testdata,vectors,answers,labels,verbose):
	successrate = 0.0
	for i in range(len(vectors)):
		out = net.activate(tuple(vectors[i].reshape(1,-1)[0]))
		if verbose:
			print "Calculated Class: {} Actual Class: {}".format(labels[out.argmax()],answers[i])
		if labels[out.argmax()] == answers[i]:
			successrate = successrate + 1.0
	successrate = successrate/len(vectors)
	print "{} Success Rate: {:.2f}%".format(name,100.0*successrate) 
	return successrate

def trainnet(name,net,trainer,traindata,testdata,vectors,answers,labels,verbose,trainnetsdir):
	print 'Training: {}'.format(name)
	iterationcount = 1
	for i in range(iterationcount):
		trainer.trainEpochs(20)
		#trainer.trainUntilConvergence()
		train_result =  pybrain.utilities.percentError(trainer.testOnClassData(),traindata['class'])
		test_result = pybrain.utilities.percentError(trainer.testOnClassData(dataset=testdata),testdata['class'])
		if verbose:
			print "epoch: %4d" % trainer.totalepochs, \
			  "  train error: %5.2f%%" % train_result, \
			  "  test error: %5.2f%%" % test_result
		
		

def trainnets():
	'''Function Variables'''
	SPLITFACTOR = 0.25
	MINSUCCESS = 0.7
	#classtypes = ['TanhLayer']
	#OUTCLASSs = [TanhLayer]
	#HIDDENCLASSs = [TanhLayer]
	#LEARNRATEs = [.04]
	#MOMENTUMs = [.4]
	#WEIGHTDECAYs = [.3]
	#HIDDENNEURONs = [10]
	classtypes =['SigmoidLayer']
	OUTCLASSs =[SigmoidLayer]
	HIDDENCLASSs = [SigmoidLayer]
        LEARNRATEs = [.05]#np.linspace(.01,.09,num=10)
	MOMENTUMs = [.5]#np.linspace(.1,.9,num=10)
	WEIGHTDECAYs = [.5]#np.linspace(.1,.9,num=10)
	HIDDENNEURONs = [(10),(5,5),(5,5,5),(5,5,5,5)]
    	IterationMax = len(classtypes)*len(OUTCLASSs)*len(HIDDENCLASSs)*len(LEARNRATEs)*len(MOMENTUMs)*len(WEIGHTDECAYs)*len(HIDDENNEURONs)
    	IterationCounter = 0
	resultfile_path = packagepath + '/scripts/results.csv'
	resultfile = open(resultfile_path,'w')
	class_net_DS = ClassificationDataSet(class_vectors[0].shape[1],class_labels=masterimage_names)
	for i in range(len(class_vectors)):
		for j in range(len(masterimage_names)):
			if class_names[i] == masterimage_names[j]:
				break

		class_net_DS.addSample(class_vectors[i],[j])


	class_net_TestData,class_net_TrainData = class_net_DS.splitWithProportion(SPLITFACTOR)
	try:
		class_net_TrainData._convertToOneOfMany()
		class_net_TestData._convertToOneOfMany() 
	except IndexError:
		print 'Possibly not all Targets present in Training Data.'
		pdb.set_trace()
	
	
	'''rowlabels = []
	for i in range(1,ROWSECTORS+1):
		rowlabels.append('Row{}'.format(i))
	row_net_DS = ClassificationDataSet(loc_vectors[0].shape[1],class_labels=rowlabels)
	for i in range(len(loc_vectors)):
		for j in range(len(rowlabels)):
			if loc_rows[i] == rowlabels[j]:
				break
		row_net_DS.addSample(loc_vectors[i],j)


	row_net_TestData,row_net_TrainData = row_net_DS.splitWithProportion(SPLITFACTOR)
	try:
		row_net_TrainData._convertToOneOfMany()
		row_net_TestData._convertToOneOfMany() 
	except IndexError:
		print 'Possibly not all Targets present in Training Data.'
		pdb.set_trace()
	collabels = []
	for i in range(1,COLSECTORS+1):
		collabels.append('Column{}'.format(i))
	col_net_DS = ClassificationDataSet(loc_vectors[0].shape[1],class_labels=collabels)
	for i in range(len(loc_vectors)):
		for j in range(len(collabels)):
			if loc_cols[i] == collabels[j]:
				break
		col_net_DS.addSample(loc_vectors[i],j)


	col_net_TestData,col_net_TrainData = col_net_DS.splitWithProportion(SPLITFACTOR)
	try:
		col_net_TrainData._convertToOneOfMany()
		col_net_TestData._convertToOneOfMany() 
	except IndexError:
		print 'Possibly not all Targets present in Training Data.'
		pdb.set_trace()
	'''	
	jobs = []
	netstrained = False
	classnet_successrate = 0.0
	rownet_successrate = 0.0
	colnet_successrate = 0.0
	classnet_done = False
	rownet_done = False
	colnet_done = False
	trainindex = 0

	for o in range(len(OUTCLASSs)):
		for h in range(len(HIDDENCLASSs)):
			for m in range(len(MOMENTUMs)):
				for w in range(len(WEIGHTDECAYs)):
					for n in range(len(HIDDENNEURONs)):
						for l in range(len(LEARNRATEs)):
						    starttime_classnet = time.time()
						    starttime_rownet = time.time()
						    starttime_colnet = time.time()
						    trainindex = trainindex + 1
						    #print 'Train Count: {}'.format(trainindex)
						    if (TrainNets == 'CLASSNET') or (TrainNets == 'ALL'):
						        class_net = buildNetwork( class_net_TrainData.indim, HIDDENNEURONs[n], class_net_TrainData.outdim,bias=True, hiddenclass=HIDDENCLASSs[h],outclass=OUTCLASSs[o] )
						        class_net_trainer = BackpropTrainer(class_net,dataset=class_net_TrainData,learningrate=LEARNRATEs[l],momentum=MOMENTUMs[m],verbose=Verbose,weightdecay=WEIGHTDECAYs[w])
						        if UseParallel:
						            print 'Training Classification ANN in Parallel'
					    
						            job = job_server.submit(func=trainnet,args=('class_net',class_net,class_net_trainer,class_net_TrainData,class_net_TestData,class_vectors,class_names,masterimage_names,Verbose,trainnednets_dir),modules=
						("random","pybrain","math","time"))
						            jobs.append(job)
						        else:
						            print 'Training Classification ANN in Sequence'
						            trainnet('class_net',class_net,class_net_trainer,class_net_TrainData,class_net_TestData,class_vectors,class_names,masterimage_names,Verbose,trainnednets_dir)
						    if (TrainNets == 'ROWNET') or (TrainNets == 'ALL'):
						        row_net = buildNetwork( row_net_TrainData.indim, HIDDENNEURONs[n], row_net_TrainData.outdim, bias=True,hiddenclass=HIDDENCLASSs[h],outclass=OUTCLASSs[o] )
						        row_net_trainer = BackpropTrainer(row_net,dataset=row_net_TrainData,learningrate=LEARNRATEs[l],momentum=MOMENTUMs[m],verbose=Verbose,weightdecay=WEIGHTDECAYs[w])		
						        if UseParallel:
						            print 'Training Row ANN in Parallel'
						            job = job_server.submit(func=trainnet,args=('row_net',row_net,row_net_trainer,row_net_TrainData,row_net_TestData,loc_vectors,loc_rows,rowlabels,Verbose,trainnednets_dir),modules=
						("random","pybrain","math","time"))
						        else:
						            print 'Training Row ANN in Sequence'
						            trainnet('row_net',row_net,row_net_trainer,row_net_TrainData,row_net_TestData,loc_vectors,loc_rows,rowlabels,Verbose,trainnednets_dir)
						    if (TrainNets == 'COLNET') or (TrainNets == 'ALL'):
						        col_net = buildNetwork( col_net_TrainData.indim, HIDDENNEURONs[n], col_net_TrainData.outdim, bias=True,hiddenclass=HIDDENCLASSs[h],outclass=OUTCLASSs[o] )
						        col_net_trainer = BackpropTrainer(col_net,dataset=col_net_TrainData,learningrate=LEARNRATEs[l],momentum=MOMENTUMs[m],verbose=Verbose,weightdecay=WEIGHTDECAYs[w])	
						        if UseParallel:
						            print 'Training Column ANN in Parallel'
						            job = job_server.submit(func=trainnet,args=('col_net',col_net,col_net_trainer,col_net_TrainData,col_net_TestData,loc_vectors,loc_cols,collabels,Verbose,trainnednets_dir),modules=
						("random","pybrain","math","time"))
						            jobs.append(job)
						        else:
						            print 'Training Column ANN in Sequence'
						            trainnet('col_net',col_net,col_net_trainer,col_net_TrainData,col_net_TestData,loc_vectors,loc_cols,collabels,Verbose,trainnednets_dir)
						    if UseParallel:	
						        for job in jobs:
						            job()
						        #job_server.print_stats()
						    if (TrainNets == 'CLASSNET') or (TrainNets == 'ALL'):
						        elaptime_classnet = time.time()-starttime_classnet
						        classnet_successrate = testnet('class_net',class_net,class_net_TestData,class_vectors,class_names,masterimage_names,Verbose)
						        tempstr = '{},{:.3f},{},{},{},{:.3f},{},{:.1f}\r\n'.format('class_net',100*classnet_successrate,classtypes[o],classtypes[h],MOMENTUMs[m],WEIGHTDECAYs[w],HIDDENNEURONs[n],elaptime_classnet)
						        resultfile.write(tempstr)
							savenet('class_net',class_net)
						    if (TrainNets == 'ROWNET') or (TrainNets == 'ALL'):
						        elaptime_rownet = time.time()-starttime_rownet
						        rownet_successrate = testnet('row_net',row_net,row_net_TestData,loc_vectors,loc_rows,rowlabels,Verbose)
						        tempstr = '{},{:.3f},{},{},{},{:.3f},{},{:.1f}\r\n'.format('row_net',100*rownet_successrate,classtypes[o],classtypes[h],MOMENTUMs[m],WEIGHTDECAYs[w],HIDDENNEURONs[n],elaptime_rownet)
						        resultfile.write(tempstr)
							savenet('row_net',row_net)	
						    if (TrainNets == 'COLNET') or (TrainNets == 'ALL'):
						        elaptime_colnet = time.time()-starttime_colnet
						        colnet_successrate = testnet('col_net',col_net,col_net_TestData,loc_vectors,loc_cols,collabels,Verbose)
						        tempstr = '{},{:.3f},{},{},{},{:.3f},{},{:.1f}\r\n'.format('col_net',100*colnet_successrate,classtypes[o],classtypes[h],MOMENTUMs[m],WEIGHTDECAYs[w],HIDDENNEURONs[n],elaptime_colnet)
						        resultfile.write(tempstr)
							savenet('col_net',col_net)
						    IterationCounter = IterationCounter + 1
						    print 'Iteration: {}/{} Completed'.format(IterationCounter,IterationMax)
				resultfile.close()
		
trainnets()



