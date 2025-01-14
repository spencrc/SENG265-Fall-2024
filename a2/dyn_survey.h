#ifndef _DYN_SURVEY_H_
#define _DYN_SURVEY_H_

/* add your library includes, constants and typedefs here*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "emalloc.h"

#define BUFFER_SIZE 3000
#define CATEGORIES 5
#define QUESTION_TYPE_SIZE 8
#define CURRENT_DAY 16
#define CURRENT_MONTH 10
#define CURRENT_YEAR 2024

typedef struct {
    char content[120];
    char type[120];
} question;

typedef struct {
    char*       field;
    char*       canadian;
    char*       dob;
} respondent;

typedef struct {
    respondent respondent;
    int*       answers;
} response;

#endif
