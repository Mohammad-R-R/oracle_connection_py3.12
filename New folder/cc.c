#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX 100

typedef struct {
    char* data[MAX];
    int top;
} Stack;

void initStack(Stack* stack) {
    stack->top = -1;
}

int isEmpty(Stack* stack) {
    return stack->top == -1;
}

void push(Stack* stack, char* value) {
    stack->data[++(stack->top)] = strdup(value);
}


char* pop(Stack* stack) {
    if (isEmpty(stack)) {
        return NULL;
    }
    return stack->data[(stack->top)--];
}

void readFile(char* filename, char* expression) {
    FILE* file = fopen(filename, "r");
    if (file == NULL) {
        fprintf(stderr, "Error opening file.\n");
        exit(1);
    }
    fgets(expression, MAX, file);
    fclose(file);
}

void generateThreeAddressCode(char* expression) {
    Stack stack;
    initStack(&stack);
    char* token = strtok(expression, " ");
    int tempCount = 1;
    char result[10];

    while (token != NULL && token[0] != '#') {
        if (isalpha(token[0])) {
            push(&stack, token);
        } else {
            char* operand2 = pop(&stack);
            char* operand1 = pop(&stack);
            sprintf(result, "T%d", tempCount++);
            printf("%s = %s %c %s\n", result, operand1, token[0], operand2);
            push(&stack, result);
        }
        token = strtok(NULL, " ");
    }
}

int main() {
    char expression[MAX];
    readFile("input.txt", expression);
    generateThreeAddressCode(expression);
    return 0;
}
