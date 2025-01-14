#include "processing.h"

int get_response_index(char** possibleResponses, char* r, int numPossibleResponses) {
    int response_index = -1;
    for (int i = 0; i < numPossibleResponses; i++) {
        if (strcmp(possibleResponses[i], r) == 0) {
            response_index = i;
            break;
        }
    } 
    
    if (response_index == -1) { 
        printf("<<%s>> was the response. This is invalid, so the program will now exit\n", r);
        exit(1);
    }

    return response_index;
}

response retrieve_response_data(char* buffer, question* questions, char** possibleResponses, int numQ, int numPossibleResponses) {
    int split_line = 0;
    char* split_string = strtok(buffer, ",");
    char* temp[100];
    response r;
    respondent p;

    r.answers = (int*) emalloc(numQ * sizeof(int));

    while (split_string != NULL) {
        split_string[strcspn(split_string, "\n")] = 0;
        //temp[split_line] = emalloc(strlen(split_string) + 1);
        temp[split_line++] = split_string;
        split_string = strtok(NULL, ",");
    }

    p.field = (char*) emalloc(strlen(temp[0])+1);
    p.canadian = (char*) emalloc(strlen(temp[1])+1);
    p.dob = (char*) emalloc(strlen(temp[2])+1);
    strcpy(p.field, temp[0]);
    strcpy(p.canadian, temp[1]);
    strcpy(p.dob, temp[2]);
    r.respondent = p;

    for (int i = 0; i < numQ; i++) {
        int temp_idx = i + 3;
        r.answers[i] = get_response_index(possibleResponses, temp[temp_idx], numPossibleResponses);
    }    

    return r;
}

int evaluate_condition_from_substring(char* condition, char* data) {
    char substring[strlen(condition)-1]; //-1 instead of +2 to account for null pointer
    strncpy(substring, condition+2, strlen(condition)-1); //+2 to shift conditions[i]'s starting pos in strncpy to index 2
    return !strcmp(substring, data);
}

int evaluate_conditions_with_response(char** conditions, response r, int numConditions) {
    int overall_eval = 1;

    if (numConditions > 1) {
        //printf("%d\n", numConditions);
    }

    for (int i = 0; i < numConditions; i++) {
        int current_eval = 0;
        
        if (conditions[i][0] == '0') current_eval = evaluate_condition_from_substring(conditions[i], r.respondent.field);
        else if (conditions[i][0] == '1') current_eval = evaluate_condition_from_substring(conditions[i], r.respondent.canadian);
        else if (conditions[i][0] == '2') {
            int split_line = 0;
            char tempC[strlen(conditions[i])+1]; //temp string not to ruin conditions string
            char tempDOB[strlen(r.respondent.dob)+1]; //temp string not to ruin DOB
            int min_age = 1;
            int age = -1;
            int max_age = -1;
            int date[3]; //formatted like this: [0] = yyyy; [1] = mm; [2] = dd;

            strcpy(tempC, conditions[i]);
            strcpy(tempDOB, r.respondent.dob);

            char* split_conditions_str = strtok(tempC, ",");
            while (split_conditions_str != NULL) {
                if (split_line == 1) min_age = atoi(split_conditions_str); //convert first element to integer to store as min_age
                else if (split_line == 2) max_age = atoi(split_conditions_str); //convert second element to integer to store as max_age
                split_line++;
                split_conditions_str = strtok(NULL, ",");
            } split_line = 0;

            char* split_dob = strtok(tempDOB, "-");
            while (split_dob != NULL) {
                date[split_line++] = atoi(split_dob); //see date[] definition
                split_dob = strtok(NULL, "-");
            }

            age = CURRENT_YEAR - date[0];
            if ((date[1] > CURRENT_MONTH) || (date[1] == CURRENT_MONTH && date[2] > CURRENT_DAY)) {
                age--;
            }

            if (age >= min_age && age <= max_age) current_eval = 1;
        }
        overall_eval = (overall_eval && current_eval);
    } //printf("eval: %d\n", overall_eval);

    return overall_eval; //returning 1 means response fits criteria, returning 0 means it does not
}

response copy_response(response target, int numQ) {
    response r;
    respondent p;

    p.field = emalloc(strlen(target.respondent.field));
    p.canadian = emalloc(strlen(target.respondent.canadian));
    p.dob = emalloc(strlen(target.respondent.dob));
    r.respondent = p;

    r.answers = (int*) emalloc(numQ * sizeof(int));

    for (int i = 0; i < numQ; i++) r.answers[i] = target.answers[i];
    return r;
}

int filter_responses(response** ptrFR, response* responses, char** conditions, int numActualResponses, int numConditions, int numQ) {
    int count = 0;

    if (numConditions <= 0) {
        *ptrFR = realloc(*ptrFR, sizeof(responses));
        for (int i = 0; i < numActualResponses; i++) (*ptrFR)[i] = copy_response(responses[i], numQ);
        return numActualResponses;
    }

    for (int i = 0; i < numActualResponses; i++) {
        response r = responses[i];
        if (evaluate_conditions_with_response(conditions, r, numConditions)) {
            *ptrFR = realloc(*ptrFR, (count + 1) * sizeof(response));
            (*ptrFR)[count++] = copy_response(r, numQ);
        }
    }

    return count;
}

float sum_up_category(response* responses, question* questions, char** possibleResponses, int starting_question_idx, int category_question_total, int response_number, int numPossibleResponses) {
    float sum = 0.0;
    for (int i = starting_question_idx; i < category_question_total; i++) {
        int answer = responses[response_number].answers[i];
        if (strcmp(questions[i].type, "Direct") == 0) { //TYPE IS DIRECT
            sum += answer + 1;
        } else { //TYPE IS REVERSE
            sum += numPossibleResponses - answer;
        }
    }
    return sum;
}

void generate_respondent_category_total(question* questions, response* responses, char** possibleResponses, float* personal_category_total, int index, int numPossibleResponses) {
    memset(personal_category_total, 0, CATEGORIES * sizeof(float));
    personal_category_total[0] = sum_up_category(responses, questions, possibleResponses, 0, 8, index, numPossibleResponses);
    personal_category_total[1] = sum_up_category(responses, questions, possibleResponses, 8, 18, index, numPossibleResponses);
    personal_category_total[2] = sum_up_category(responses, questions, possibleResponses, 18, 28, index, numPossibleResponses);
    personal_category_total[3] = sum_up_category(responses, questions, possibleResponses, 28, 34, index, numPossibleResponses);
    personal_category_total[4] = sum_up_category(responses, questions, possibleResponses, 34, 38, index, numPossibleResponses);
}