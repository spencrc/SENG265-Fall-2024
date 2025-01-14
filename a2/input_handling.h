#ifndef _INPUT_HANDLING_H_
#define _INPUT_HANDLING_H_

/* add your include and prototypes here*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "dyn_survey.h"
#include "processing.h"
#include "emalloc.h"

int get_line(char* buffer);
int get_bits(int** ptrB, char* buffer);
int retrieve_questions(question** ptrQ, char* buffer);
int retrieve_question_types(question* questions, char* buffer);
int retrieve_response_types(char*** ptrPR, char* buffer);
int get_number_of_responses(char* buffer);
void get_all_responses(response** ptrR, question* questions, char** possibleResponses, int numQ, int numActualResponses, char* buffer, int numPossibleResponses);
int store_condition_strings(char*** ptrC, char* buffer);

#endif
