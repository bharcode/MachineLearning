cp data/f1_te mobile/test.csv
cp data/f1_tr mobile/train.csv
sh f1.sh
if [ $? -ne 0 ];then
    echo "f1 failed"
    exit 1
fi
cp mobile_predictions/test.csv.out f1

cp data/f2_te mobile/test.csv
cp data/f2_tr mobile/train.csv
sh f2.sh
if [ $? -ne 0 ];then
    echo "f2 failed"
    exit 1
fi

cp mobile_predictions/test.csv.out f2

cp data/f3_te mobile/test.csv
cp data/f3_tr mobile/train.csv
sh f3.sh
if [ $? -ne 0 ];then
    echo "f3 failed"
    exit 1
fi
cp mobile_predictions/test.csv.out f3

cp data/f3_te mobile/test.csv
cp data/f3_tr mobile/train.csv
sh f3_1.sh
if [ $? -ne 0 ];then
    echo "f3_1 failed"
    exit 1
fi
cp mobile_predictions/test.csv.out f3_1

cp data/f4_te mobile/test.csv
cp data/f4_tr mobile/train.csv
sh f4.sh
if [ $? -ne 0 ];then
    echo "f4 failed"
    exit 1
fi
cp mobile_predictions/test.csv.out f4

cp data/f4_te mobile/test.csv
cp data/f4_tr mobile/train.csv
sh f4_1.sh
if [ $? -ne 0 ];then
    echo "f4_1 failed"
    exit 1
fi
cp mobile_predictions/test.csv.out f4_1

paste f1 f2 f3 f3_1 f4 f4_1 > final_predictions/predictions.csv
rm f1 f2 f3 f3_1 f4 f4_1
