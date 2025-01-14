#ifndef _PROCESSING_H_
#define _PROCESSING_H_

/* add your include and prototypes here*/
#include <stdio.h>
#include <stdlib.h>
#include "dyn_survey.h"
#include "emalloc.h"

int get_response_index(char** possibleResponses, char* r, int numPossibleResponses);
response retrieve_response_data(char* buffer, question* questions, char** possibleResponses, int numQ, int numPossibleResponses);
int evaluate_condition_from_substring(char* condition, char* data);
int evaluate_conditions_with_response(char** conditions, response r, int numConditions);
response copy_response(response target, int numQ);
int filter_responses(response** ptrFR, response* responses, char** conditions, int numActualResponses, int numConditions, int numQ);
float sum_up_category(response* responses, question* questions, char** possibleResponses, int starting_question_idx, int category_question_total, int response_number, int numPossibleResponses);
void generate_respondent_category_total(question* questions, response* responses, char** possibleResponses, float* personal_category_total, int index, int numPossibleResponses);

#endif
