#ifndef _OUTPUT_H_
#define _OUTPUT_H_

/* add your include and prototypes here*/
#include <stdio.h>
#include <stdlib.h>
#include "processing.h"
#include "dyn_survey.h"

void bit_1(question* questions, response* responses, char** possibleResponses, int numQ, int numPossibleResponses, int total_respondents);
void bit_2(question* questions, response* responses, char** possibleResponses, int total_respondents, int numPossibleResponses);
void bit_3(question* questions, response* responses, char** possibleResponses, int total_respondents, int numPossibleResponses); 

#endif
