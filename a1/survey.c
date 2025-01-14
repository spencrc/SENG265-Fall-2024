#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUFFER_SIZE 3000
#define QUESTION_LENGTH 120
#define NUMBER_OF_QUESTIONS 38
#define CATEGORIES 5
#define QUESTION_TYPE_SIZE 8
#define LEVELS_OF_AGREEMENT 6

typedef struct {
    char content[QUESTION_LENGTH];
    char type[QUESTION_TYPE_SIZE];
} question;

typedef struct {
    char field[100];
    char canadian[4];
    char dob[10];
    int  responses[NUMBER_OF_QUESTIONS];
} respondent;

int get_line(char* buffer) {  
    while ( fgets(buffer, BUFFER_SIZE, stdin) != NULL ) {
        if (buffer[0] == '#') continue;
        else { 
            buffer[strcspn(buffer, "\n")] = 0; 
            return 0; 
        }
    } return 1;
}

void get_bits(int* bits, char* buffer) {
    get_line(buffer);

    int split_line = 0;
    char* split_string = strtok(buffer, ",");

    while (split_string != NULL) {
        bits[split_line++] = atoi(split_string);
        split_string = strtok(NULL, ",");
    }
}

void retrieve_questions(question* questions, char* buffer) {
    get_line(buffer);
    
    int split_line = 0;
    char* split_string = strtok(buffer, ";");

    while (split_string != NULL) {
        question q;
        strcpy(q.content, split_string);
        questions[split_line++] = q;
        split_string = strtok(NULL, ";");
    } 
}

void retrieve_question_types(question* questions, char* buffer) {
    get_line(buffer);

    int split_line = 0;
    char* split_string = strtok(buffer, ";");

    while (split_string != NULL) {
        question q = questions[split_line];
        strcpy(q.type, split_string);
        questions[split_line++] = q;
        split_string = strtok(NULL, ";");
    } 
}

void retrieve_response_types(char** responses, char* buffer) {
    get_line(buffer);

    int split_line = 0;
    char* split_string = strtok(buffer, ",");

    while (split_string != NULL) {
        responses[split_line] = malloc(strlen(split_string) * sizeof(char));
        strcpy(responses[split_line], split_string);
        split_line++;
        split_string = strtok(NULL, ",");
    } 
}

int get_response(question q, char** responses, char* response) {
    int response_index = -1;
    for (int i = 0; i < LEVELS_OF_AGREEMENT; i++) {
        if (strcmp(responses[i], response) == 0) {
            response_index = i;
            break;
        }
    } 
    
    if (response_index == -1) { 
        printf("<<%s>>\n", response);
        exit(1);
    }

    return response_index;
}

respondent retrieve_respondent_data_and_responses(char* buffer, question* questions, char** responses) {
    int split_line = 0;
    char* split_string = strtok(buffer, ",");
    char* temp[100];
    respondent r;

    while (split_string != NULL) {
        split_string[strcspn(split_string, "\n")] = 0;
        temp[split_line++] = split_string;
        split_string = strtok(NULL, ",");
    }

    strcpy(r.field, temp[0]);
    strcpy(r.canadian, temp[1]);
    strcpy(r.dob, temp[2]);

    for (int i = 0; i < NUMBER_OF_QUESTIONS; i++) {
        int temp_idx = i + 3;
        r.responses[i] = get_response(questions[i], responses, temp[temp_idx]);
    }    

    return r;
}

int get_all_respondents(char* buffer, question* questions, char** responses, respondent** pointer_2_respondents) {
    int count = 0;
    while ( !get_line(buffer) ) {
        *pointer_2_respondents = (respondent*) realloc(*pointer_2_respondents, (count + 1) * sizeof(respondent));
        (*pointer_2_respondents)[count] = retrieve_respondent_data_and_responses(buffer, questions, responses);
        count++;
    }
    return count;
}

void initialize_float_array(float* array, int size) {
    for (int i = 0; i < size; i++) { //LOOP TO PROPERLY INTIALIZE ARRAY
        array[i] = 0.0;
    }
}

float sum_up_category(respondent* respondents, question* questions, int starting_question_idx, int category_question_total, int respondent_number) {
    float sum = 0.0;
    for (int i = starting_question_idx; i < category_question_total; i++) {
        int response = respondents[respondent_number].responses[i];
        if (strcmp(questions[i].type, "Direct") == 0) { //TYPE IS DIRECT
            sum += response + 1;
        } else { //TYPE IS REVERSE
            sum += LEVELS_OF_AGREEMENT - response;
        }
    }
    return sum;
}

void print_default_output(question* questions, char** responses) {
    printf("FOR EACH QUESTION BELOW, RELATIVE PERCENTUAL FREQUENCIES ARE COMPUTED FOR EACH LEVEL OF AGREEMENT\n");
    for (int i = 0; i < NUMBER_OF_QUESTIONS; i++) {
        printf("\n%s\n", questions[i].content);
        for (int j = 0; j < LEVELS_OF_AGREEMENT; j++) {
            printf("%.2f: %s\n", 0.0, responses[j]);
        }
    }
}

void print_output_with_frequencies(question* questions, respondent* respondents, char** responses, int total_respondents) {
    printf("FOR EACH QUESTION BELOW, RELATIVE PERCENTUAL FREQUENCIES ARE COMPUTED FOR EACH LEVEL OF AGREEMENT\n");
    for (int i = 0; i < NUMBER_OF_QUESTIONS; i++) {
        printf("\n%s\n", questions[i].content);
        
        float response_results[LEVELS_OF_AGREEMENT];
        initialize_float_array(response_results, LEVELS_OF_AGREEMENT);

        for (int r_idx = 0; r_idx < total_respondents; r_idx++) {
            int response = respondents[r_idx].responses[i];
            response_results[response] += 1;
        }
        for (int j = 0; j < LEVELS_OF_AGREEMENT; j++) {
            printf("%.2f: %s\n", response_results[j]/total_respondents * 100, responses[j]);
        }
    }
}
void generate_respondent_category_total(question* questions, respondent* respondents, float* personal_category_total, int index) {
    initialize_float_array(personal_category_total, CATEGORIES);
    personal_category_total[0] = sum_up_category(respondents, questions, 0, 8, index);
    personal_category_total[1] = sum_up_category(respondents, questions, 8, 18, index);
    personal_category_total[2] = sum_up_category(respondents, questions, 18, 28, index);
    personal_category_total[3] = sum_up_category(respondents, questions, 28, 34, index);
    personal_category_total[4] = sum_up_category(respondents, questions, 34, 38, index);
}

void print_respondent_averages(question* questions, respondent* respondents, int total_respondents) {
    printf("SCORES FOR ALL THE RESPONDENTS\n\n");

    for (int r_idx = 0; r_idx < total_respondents; r_idx++) {
        float personal_category_total[CATEGORIES];
        generate_respondent_category_total(questions, respondents, personal_category_total, r_idx);

        printf("C:%.2f,",personal_category_total[0]/8);
        printf("I:%.2f,",personal_category_total[1]/10);
        printf("G:%.2f,",personal_category_total[2]/10);
        printf("U:%.2f,",personal_category_total[3]/6);
        printf("P:%.2f\n",personal_category_total[4]/4);
    }
}

void print_averages_per_respondents(respondent* respondents, question* questions, int total_respondents) {
    printf("AVERAGE SCORES PER RESPONDENT\n\n");
    float total_category_total[CATEGORIES];
    initialize_float_array(total_category_total, CATEGORIES);

    for (int r_idx = 0; r_idx < total_respondents; r_idx++) {
        float personal_category_total[CATEGORIES];
        generate_respondent_category_total(questions, respondents, personal_category_total, r_idx);

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

int main() {
    int bits[4];
    question questions[NUMBER_OF_QUESTIONS];
    respondent* respondents = malloc(1 * sizeof(respondent));
    respondent** pointer_2_respondents = &respondents;
    char* responses[LEVELS_OF_AGREEMENT];
    char buffer[BUFFER_SIZE];

    get_bits(bits, buffer);
    retrieve_questions(questions, buffer);
    retrieve_question_types(questions, buffer);
    retrieve_response_types(responses, buffer);
    int total_respondents = get_all_respondents(buffer, questions, responses, pointer_2_respondents);

    printf("Examining Science and Engineering Students' Attitudes Towards Computer Science\nSURVEY RESPONSE STATISTICS\n\n");
    printf("NUMBER OF RESPONDENTS: %i\n\n", total_respondents);

    if (bits[0]) print_default_output(questions, responses); //PRINT OUTPUT STRUCTURE WITH ALL ZEROES FOR FREQUENCY
    if (bits[0] && (bits[1] || bits[2] || bits[3])) printf("\n"); //IF THERE ARE MORE THAN JUST THE FIRST BIT, DIVIDE THEM WITH A LINE

    if (bits[1]) print_output_with_frequencies(questions, respondents, responses, total_respondents); //PRINT OUTPUT STRUCTURE WITH FREQUENCY
    if (bits[1] && (bits[2] || bits[3])) printf("\n"); //SAME IDEA AS ABOVE, BUT WITH SECOND BIT

    if (bits[2]) print_respondent_averages(questions, respondents, total_respondents); //PRINT OUTPUT AVERAGE RESPONSE VALUE FOR EACH CATEGORY
    if (bits[2] && bits[3]) printf("\n"); //SAME AGAIN WITH THIRD BIT

    if (bits[3]) print_averages_per_respondents(respondents, questions, total_respondents); //PRINT OUT TOTAL AVERAGES IN EACH CATEGORY

    for (int i = 0; i < LEVELS_OF_AGREEMENT; i++) {
        free(responses[i]);
    }
    free(respondents);

    return 0;
}