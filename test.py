mode = 'void'

bool_or_list = True if mode == 'bool' else False
void = bool_or_list and mode == 'void'

print(void)