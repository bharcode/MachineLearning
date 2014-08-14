#include "MF.h"
#include "globals.h"

#include <algorithm>
#include <fstream>
#include <iostream>
using namespace std;

void MF_train()
{
	int count, u, a, b, ui, ai, bi, hit;
	double rmse, avg, pre_a, pre_b, e, t, ap_sum, ap;
	vector< pair<int, double> > pre_node;
	for (int lp = 1; lp <= LOOP; lp++) {
		rmse = avg = 0;
		count = 0;
		for (u = 1; u <= N_USER; u++) {
			ui = u * K;
			for (vector<int>::iterator it = TRAIN[u].begin(); it != TRAIN[u].end(); it++) {
				a = *it;
				while (true) {
					b = rand_int(N_USER-1) + 1;
					if (find(TRAIN[u].begin(), TRAIN[u].end(), b) == TRAIN[u].end()/* &&
						find(CANDIDATE[u].begin(), CANDIDATE[u].end(), b) == CANDIDATE[u].end()*/)
						break;
				}
				ai = a * K;
				bi = b * K;
				pre_a = pre_b = 0;
				for (int k = 0; k < K; k++) {
					pre_a += P[ui+k] * Q[ai+k];
					pre_b += P[ui+k] * Q[bi+k];
				}
				e = (pre_a - pre_b) - (POSITIVE_SCORE - NEGATIVE_SCORE);
				count ++;
				rmse += e * e;
				avg += pre_a + pre_b;
				for(int k = 0; k < K; k++) {
					t = P[ui+k];
					P[ui+k] -= lrate * (e * (Q[ai+k] - Q[bi+k]) + lambda * P[ui+k]);
					Q[ai+k] -= lrate * (e * t + lambda * Q[ai+k]);
					Q[bi+k] -= lrate * (-e * t + lambda * Q[bi+k]);
				}
			}
		}
		rmse = sqrt(rmse/count);
		avg /= (count * 2);
		cout << "Loop " << lp << "\tRMSE:" << rmse << " AVG:" << avg << " COUNT:" << count << endl;

		count = 0;
		ap_sum = 0;
		if (!TEST) {
			for (vector<int>::iterator u_it = TEST_USER.begin(); u_it != TEST_USER.end(); u_it++) {
				u = *u_it;
				pre_node.clear();
				ui = u * K;
				for (vector<int>::iterator it = CANDIDATE[u].begin(); it != CANDIDATE[u].end(); it++) {
					a = *it;
					ai = a * K;
					pre_a = 0;
					for (int k = 0; k < K; k++)
						pre_a += P[ui+k] * Q[ai+k];
					pre_node.push_back(make_pair(a, pre_a));
				}
				sort(pre_node.begin(), pre_node.end(), score_cmp);
				ap = 0;
				hit = 0;
				if (TRUE_LINKS[u].size() > 0) {
					for (int i = 0; i < 10 && i < pre_node.size(); i++) {
						if (TRUE_LINKS[u].find(pre_node[i].first) != TRUE_LINKS[u].end()) {
							hit ++;
							ap += (double)hit / (i+1);
						}
					}
					ap /= TRUE_LINKS[u].size();
				}
				ap_sum += ap;
				count ++;
			}
			cout << "Validation AP: " << ap_sum / count << " ,count: " << count << endl;
		}
	}

	if (TEST) {
		char out_line[200];
		char buf[20];
		ofstream out((CORPUS + "test/MF_output.csv").c_str(), ofstream::out);
		out << "source_node,destination_nodes" << endl;
		for (vector<int>::iterator u_it = TEST_USER.begin(); u_it != TEST_USER.end(); u_it++) {
			u = *u_it;
			pre_node.clear();
			ui = u * K;
			for (vector<int>::iterator it = CANDIDATE[u].begin(); it != CANDIDATE[u].end(); it++) {
				a = *it;
				ai = a * K;
				pre_a = 0;
				for (int k = 0; k < K; k++)
					pre_a += P[ui+k] * Q[ai+k];
				pre_node.push_back(make_pair(a, pre_a));
			}
			sort(pre_node.begin(), pre_node.end(), score_cmp);	
			sprintf(out_line, "%d,", u);
			for (int i = 0; i < 10 && i < pre_node.size(); i++) {
				sprintf(buf, " %d", pre_node[i].first);
				strcat(out_line, buf);
			}
			out << out_line << endl;
		}
		out.close();
	}	
}