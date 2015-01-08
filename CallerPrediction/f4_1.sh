#!/bin/bash

###############################
# Author : Bharath Cheluvaraju#
#                             #
###############################

echo "Generate file descriptors by parallizing mahout on hadoop"
rm ~/kgl_caller_pred/mobile/mobile.info
hadoop jar mahout-core-0.7-job.jar org.apache.mahout.classifier.df.tools.Describe -p ~/kgl_caller_pred/mobile/train.csv -f ~/kgl_caller_pred/mobile/mobile.info -d I 5 C 5 N L
if [ $? -ne 0 ]; then
    echo "Generation of RandomForest FileDescriptor Failed"
    exit 1
fi

# Training
echo "Training the RandomForest.."
rm -r ~/kgl_caller_pred/mob_pred_forest
hadoop jar mahout-examples-0.7-job.jar org.apache.mahout.classifier.df.mapreduce.BuildForest -Dmapred.job.name=GRMS -Dmapred.job.queue.name=$MY_QUEUE -Dmapred.max.split.size=1000000 -d ~/kgl_caller_pred/mobile/train.csv -ds ~/kgl_caller_pred/mobile/mobile.info -sl 4 -p -t 100 -o ~/kgl_caller_pred/mob_pred_forest
if [ $? -ne 0 ]; then
    echo "RandomForest Training failed."
    exit 1
fi

echo "Running RandomForest prediction on TestData"
rm -r ~/kgl_caller_pred/mobile_predictions
hadoop jar mahout-examples-0.7-job.jar org.apache.mahout.classifier.df.mapreduce.TestForest -Dmapred.job.name=GRMS -Dmapred.job.queue.name=$MY_QUEUE -i ~/kgl_caller_pred/mobile/test.csv -ds ~/kgl_caller_pred/mobile/mobile.info -m ~/kgl_caller_pred/mob_pred_forest -a -mr -o ~/kgl_caller_pred/mobile_predictions
if [ $? -ne 0 ]; then
    echo "RandomForest Prediction failed."
    exit 1
fi



