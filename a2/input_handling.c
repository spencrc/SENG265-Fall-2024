#include "input_handling.h"

int get_line(char* buffer) {  
    while ( fgets(buffer, BUFFER_SIZE, stdin) != NULL ) {
        if (buffer[0] == '#') continue;
        else { 
            buffer[strcspn(buffer, "\n")] = 0; 
            return 0; 
        }
    } return 1;
}

int get_bits(int** ptrB, char* buffer) {
    get_line(buffer);

    int split_line = 0;
    char* split_string = strtok(buffer, ",");

    while (split_string != NULL) {
        *ptrB = (int*) realloc(*ptrB, (split_line + 1) * sizeof(int));
        (*ptrB)[split_line++] = atoi(split_string);
        split_string = strtok(NULL, ",");
    }

    return split_line;
}

int retrieve_questions(question** ptrQ, char* buffer) {
    get_line(buffer);
    
    int split_line = 0;
    char* split_string = strtok(buffer, ";");

    while (split_string != NULL) {
        *ptrQ = (question*) realloc(*ptrQ, (split_line + 1) * sizeof(question));
        strcpy((*ptrQ)[split_line].content, split_string);
        split_line++;
        split_string = strtok(NULL, ";");
    } 
    return split_line;
}

int retrieve_question_types(question* questions, char* buffer) {
    get_line(buffer);

    int split_line = 0;
    char* split_string = strtok(buffer, ";");

    while (split_string != NULL) {
        question q = questions[split_line];
        strcpy(q.type, split_string);
        questions[split_line++] = q;
        split_string = strtok(NULL, ";");
    } 
    return split_line;
}

int retrieve_response_types(char*** ptrPR, char* buffer) {
    get_line(buffer);

    *ptrPR = realloc(*ptrPR, strlen(buffer));
    int split_line = 0;
    char* split_string = strtok(buffer, ",");

    while (split_string != NULL) {
        (*ptrPR)[split_line] = emalloc((strlen(split_string) + 1) * sizeof(char));
        strcpy((*ptrPR)[split_line], split_string);
        split_line++;
        split_string = strtok(NULL, ",");
    } 
    return split_line;
}

int get_number_of_responses(char* buffer) {
    get_line(buffer);
    return atoi(buffer);
}

void get_all_responses(response** ptrR, question* questions, char** possibleResponses, int numQ, int numActualResponses, char* buffer, int numPossibleResponses) {
    *ptrR = realloc(*ptrR, (numActualResponses + 1) * sizeof(response));
    for (int i = 0; i < numActualResponses; i++) {
        get_line(buffer);
        (*ptrR)[i] = retrieve_response_data(buffer, questions, possibleResponses, numQ, numPossibleResponses);
    }
}

int store_condition_strings(char*** ptrC, char* buffer) {
    int count = 0;
    while ( !get_line(buffer) ) {
        *ptrC = realloc(*ptrC, (count+1) * BUFFER_SIZE);
        (*ptrC)[count] = emalloc(strlen(buffer) + 1);
        strcpy((*ptrC)[count], buffer);
        count++;
    }
    return count;
}