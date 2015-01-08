#!/bin/bash

###############################
# Author : Bharath Cheluvaraju#
#                             #
###############################

echo "Generate file descriptors by parallizing mahout on hadoop"
rm $PWD/mobile/mobile.info
hadoop jar mahout-core-0.7-job.jar org.apache.mahout.classifier.df.tools.Describe -p $PWD/mobile/train.csv -f $PWD/mobile/mobile.info -d 140 N L
if [ $? -ne 0 ]; then
    echo "Generation of RandomForest FileDescriptor Failed"
    exit 1
fi

# Training
echo "Training the RandomForest.."
rm -r $PWD/mob_pred_forest
hadoop jar mahout-examples-0.7-job.jar org.apache.mahout.classifier.df.mapreduce.BuildForest -Dmapred.job.name=GRMS -Dmapred.job.queue.name=$MY_QUEUE -Dmapred.max.split.size=1000000 -d $PWD/mobile/train.csv -ds $PWD/mobile/mobile.info -sl 12 -p -t 100 -o $PWD/mob_pred_forest
if [ $? -ne 0 ]; then
    echo "RandomForest Training failed."
    exit 1
fi

echo "Running RandomForest prediction on TestData"
rm -r $PWD/mobile_predictions
hadoop jar mahout-examples-0.7-job.jar org.apache.mahout.classifier.df.mapreduce.TestForest -Dmapred.job.name=GRMS -Dmapred.job.queue.name=$MY_QUEUE -i $PWD/mobile/test.csv -ds $PWD/mobile/mobile.info -m $PWD/mob_pred_forest -a -mr -o $PWD/mobile_predictions
if [ $? -ne 0 ]; then
    echo "RandomForest Prediction failed."
    exit 1
fi



