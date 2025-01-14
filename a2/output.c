#include "output.h"

void bit_1(question* questions, response* responses, char** possibleResponses, int numQ, int numPossibleResponses, int total_respondents) {
    printf("FOR EACH QUESTION BELOW, RELATIVE PERCENTUAL FREQUENCIES ARE COMPUTED FOR EACH LEVEL OF AGREEMENT\n");
    for (int i = 0; i < numQ; i++) {
        printf("\n%s\n", questions[i].content);
        
        float response_results[numPossibleResponses];
        memset(response_results, 0, numPossibleResponses * sizeof(float));

        for (int j = 0; j < total_respondents; j++) {
            int r_idx = responses[j].answers[i]; 
            response_results[r_idx] += 1;
        }
        for (int j = 0; j < numPossibleResponses; j++) {
            printf("%.2f: %s\n", response_results[j]/total_respondents * 100, possibleResponses[j]);
        }
    }
}

void bit_2(question* questions, response* responses, char** possibleResponses, int total_respondents, int numPossibleResponses) {
    printf("SCORES FOR ALL THE RESPONDENTS\n\n");
    for (int r_idx = 0; r_idx < total_respondents; r_idx++) {
        float personal_category_total[CATEGORIES];
        generate_respondent_category_total(questions, responses, possibleResponses, personal_category_total, r_idx, numPossibleResponses);

        printf("C:%.2f,",personal_category_total[0]/8);
        printf("I:%.2f,",personal_category_total[1]/10);
        printf("G:%.2f,",personal_category_total[2]/10);
        printf("U:%.2f,",personal_category_total[3]/6);
        printf("P:%.2f\n",personal_category_total[4]/4);
    }
}

void bit_3(question* questions, response* responses, char** possibleResponses, int total_respondents, int numPossibleResponses) {
    printf("AVERAGE SCORES PER RESPONDENT\n\n");
    float total_category_total[CATEGORIES];
    memset(total_category_total, 0, CATEGORIES * sizeof(float));
    //initialize_float_array(total_category_total, CATEGORIES);

    for (int r_idx = 0; r_idx < total_respondents; r_idx++) {
        float personal_category_total[CATEGORIES];
        generate_respondent_category_total(questions, responses, possibleResponses, personal_category_total, r_idx, numPossibleResponses);

        for (int i = 0; i < CATEGORIES && total_category_total != NULL; i++) {
            total_category_total[i] += personal_category_total[i];;
        }
    }

    printf("C:%.2f,",total_category_total[0]/8/total_respondents);
    printf("I:%.2f,",total_category_total[1]/10/total_respondents);
    printf("G:%.2f,",total_category_total[2]/10/total_respondents);
    printf("U:%.2f,",total_category_total[3]/6/total_respondents);
    printf("P:%.2f\n",total_category_total[4]/4/total_respondents);
}