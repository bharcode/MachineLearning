#include "globals.h"
#include <fstream>
#include <utility>
#include <ctime>
#include <cstdlib>
#include <iostream>

using namespace std;

bool TEST = false;
const string CORPUS = "E:/data/facebook/Data/";
const int N_USER = 1862220;
string CANDIDATE_FN;
double *P;
double *Q;
int LOOP = 30;
int K = 10;
double global_avg = 0.2;
double lrate = 0.0005;
double lambda = 0.01;
double POSITIVE_SCORE = 1.0;
double NEGATIVE_SCORE = 0.0;
vector<int> *TRAIN;
vector<int> *CANDIDATE;
map< int, set<int> > TRUE_LINKS;
vector<int> TEST_USER;

void init()
{
	P = new double[(N_USER+1) * K];
	Q = new double[(N_USER+1) * K];
	srand(time(NULL));
	for(int i = 0, n = (N_USER+1) * K; i < n; i++) {
		P[i] = sqrt(global_avg / K) + ((rand()+0.0)/RAND_MAX - 0.5) * 0.5 * 0.01;
		Q[i] = sqrt(global_avg / K) + ((rand()+0.0)/RAND_MAX - 0.5) * 0.5 * 0.01;
	}	
	read_train();
	CANDIDATE_FN = "candidate.csv";
	read_candiate();
	if (!TEST) read_true_links();
}

void read_train()
{
	string dir = "validation/";
	if (TEST) dir = "test/";
	TRAIN = new vector<int>[N_USER+1];
	string train = CORPUS + dir + "train.csv";
	ifstream fs(train.c_str(), ifstream::in);
	int u1, u2;
	while (fs >> u1 >> u2) {
		TRAIN[u1].push_back(u2);
	}
	fs.close();
}

void read_candiate()
{
	string dir = "validation/";
	if (TEST) dir = "test/";
	CANDIDATE = new vector<int>[N_USER+1];
	string train = CORPUS + dir + CANDIDATE_FN;
	FILE *pf = fopen (train.c_str(), "r");
	const int MaxLen  = 1<<14;
	char  line[MaxLen];
	char *tok1, *tok2;
	int u1, u2;
	fgets(line, MaxLen, pf);
	while (fgets(line, MaxLen, pf)) {
		tok1 = strtok(line, ",");
		u1 = std::atoi(tok1);
		TEST_USER.push_back(u1);
		tok1 = strtok(NULL, ",");
		if (tok1 && strcmp(tok1, "\n") != 0) {
			tok2 = strtok(tok1, " ");
			while (tok2) {
				u2 = std::atoi(tok2);
				CANDIDATE[u1].push_back(u2);
				tok2 = strtok(NULL, " ");
			}
		}
	}
	fclose(pf);
}

void read_true_links()
{
	string dir = "validation/";
	string train = CORPUS + dir + "test.csv";
	FILE *pf = fopen (train.c_str(), "r");
	const int MaxLen  = 1<<14;
	char  line[MaxLen];
	char *tok1, *tok2;
	int u1, u2;
	while (fgets(line, MaxLen, pf)) {
		tok1 = strtok(line, ",");
		u1 = std::atoi(tok1);
		tok1 = strtok(NULL, ",");
		if (tok1 && strcmp(tok1, "\n") != 0) {
			tok2 = strtok(tok1, " ");
			while (tok2) {
				u2 = std::atoi(tok2);
				TRUE_LINKS[u1].insert(u2);
				tok2 = strtok(NULL, " ");
			}
		}
	}
	fclose(pf);
}