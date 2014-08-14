#ifndef _GLOBALS_H_
#define _GLOBALS_H_

#include <vector>
#include <set>
#include <map>
#include <string>
using namespace std;

extern bool TEST;
extern const string CORPUS;
extern string CANDIDATE_FN;
extern const int N_USER;
extern double *P;
extern double *Q;
extern int LOOP;
extern int K;
extern double global_avg;
extern double lrate;
extern double lambda;
extern double POSITIVE_SCORE;
extern double NEGATIVE_SCORE;
extern vector<int> *TRAIN;
extern vector<int> *CANDIDATE;
extern map< int, set<int> > TRUE_LINKS;
extern vector<int> TEST_USER;

void init();
void read_train();
void read_candiate();
void read_true_links();

inline int rand_int(int max) {
	int n_buk = max / RAND_MAX + 1;
	int buk = rand() % n_buk;
	int r = buk * RAND_MAX + rand() % RAND_MAX;
	if (r > max) return max;
	return r;
}

inline bool score_cmp(const pair<int,double> a, const pair<int,double> b)
{
	return a.second > b.second;
}

#endif