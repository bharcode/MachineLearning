#!/bin/bash

###############################
# Author : Bharath Cheluvaraju#
#                             #
###############################

echo "Generate file descriptors by parallizing mahout on hadoop"
rm ~/log_data/mobile/mobile.info
hadoop jar mahout-core-0.7-job.jar org.apache.mahout.classifier.df.tools.Describe -p ~/log_data/mobile/train.csv -f ~/log_data/mobile/mobile.info -d I 4 N 7 C L
if [ $? -ne 0 ]; then
    echo "Generation of RandomForest FileDescriptor Failed"
    exit 1
fi

# Training
echo "Training the RandomForest.."
rm -r ~/log_data/mob_pred_forest
hadoop jar mahout-examples-0.7-job.jar org.apache.mahout.classifier.df.mapreduce.BuildForest -Dmapred.job.name=GRMS -Dmapred.job.queue.name=$MY_QUEUE -Dmapred.max.split.size=1000000 -d ~/log_data/mobile/train.csv -ds ~/log_data/mobile/mobile.info -sl 4 -p -t 50 -o ~/log_data/mob_pred_forest
if [ $? -ne 0 ]; then
    echo "RandomForest Training failed."
    exit 1
fi

echo "Running RandomForest prediction on TestData"
rm -r ~/log_data/mobile_predictions
hadoop jar mahout-examples-0.7-job.jar org.apache.mahout.classifier.df.mapreduce.TestForest -Dmapred.job.name=GRMS -Dmapred.job.queue.name=$MY_QUEUE -i ~/log_data/mobile/test.csv -ds ~/log_data/mobile/mobile.info -m ~/log_data/mob_pred_forest -a -mr -o ~/log_data/mobile_predictions
if [ $? -ne 0 ]; then
    echo "RandomForest Prediction failed."
    exit 1
fi



