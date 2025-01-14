#include "dyn_survey.h"
#include "input_handling.h"
#include "processing.h"
#include "output.h"

int main() {
    char buffer[BUFFER_SIZE];
    int* bits = emalloc(1);
    question* questions = emalloc(1);
    char** possibleResponses = emalloc(1);
    response* responses = emalloc(1);
    char** conditions = emalloc(1);
    response* filteredResponses = emalloc(1 * sizeof(response));

    int** ptrB = &bits;
    question** ptrQ = &questions;
    char*** ptrPR = &possibleResponses;
    response** ptrR = &responses;
    char*** ptrC = &conditions;
    response** ptrFR = &filteredResponses;

    get_bits(ptrB, buffer);
    int numQ = retrieve_questions(ptrQ, buffer); //fills our array of questions with the content of each question from input file
    retrieve_question_types(questions, buffer); //sets the "type" field of each question within the array of questions using info from input file
    int numPossibleResponses = retrieve_response_types(ptrPR, buffer); //iterates through line containing a list (separated by commas) to find all possible responses, storing the # of them
    int numActualResponses = get_number_of_responses(buffer); //reads line containing integer number of responses
    get_all_responses(ptrR, questions, possibleResponses, numQ, numActualResponses, buffer, numPossibleResponses);
    int numConditions = store_condition_strings(ptrC, buffer);
    int numFilteredResponses = filter_responses(ptrFR, responses, conditions, numActualResponses, numConditions, numQ);

    printf("Examining Science and Engineering Students' Attitudes Towards Computer Science\nSURVEY RESPONSE STATISTICS\n\n");
    printf("NUMBER OF RESPONDENTS: %i\n\n", numFilteredResponses);

    if (bits[0]) bit_1(questions, filteredResponses, possibleResponses, numQ, numPossibleResponses, numFilteredResponses); //PRINT OUTPUT STRUCTURE WITH FREQUENCY
    if (bits[1] && bits[2]) printf("\n"); //IF THERE ARE MORE THAN JUST THE FIRST BIT, DIVIDE THEM WITH A LINE

    if (bits[1]) bit_2(questions, filteredResponses, possibleResponses, numFilteredResponses, numPossibleResponses);
    if (bits[2]) printf("\n"); //SAME IDEA AS ABOVE, BUT WITH SECOND BIT

    if (bits[2]) bit_3(questions, filteredResponses, possibleResponses, numFilteredResponses, numPossibleResponses); //SAME AGAIN WITH THIRD BIT

    free(bits);
    free(questions);
    for (int i = 0; i < numPossibleResponses; i++) {
        free(possibleResponses[i]);
    } free(possibleResponses);
    for (int i = 0; i < numActualResponses; i++) {
        free(responses[i].answers); 
        free(responses[i].respondent.dob);
        free(responses[i].respondent.canadian);
        free(responses[i].respondent.field);
    } free(responses);
    for (int i = 0; i < numConditions; i++) {
        free(conditions[i]);
    } free(conditions);
    for (int i = 0; i < numFilteredResponses; i++) {
        free(filteredResponses[i].answers);
        free(filteredResponses[i].respondent.dob);
        free(filteredResponses[i].respondent.canadian);
        free(filteredResponses[i].respondent.field);
    } free(filteredResponses);
    return 0;
}