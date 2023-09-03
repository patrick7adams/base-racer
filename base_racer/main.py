import math
import pygame
# Types of conversions necessary:
# int to bin, bin to int, hex to int, int to hex, bin to hex, hex to bin

str_int_dict = {str(i):i for i in range(10)}
str_int_dict.update({letter:val for letter,val in zip('abcdefghijklmnopqrstuvwxyz', range(10, 36))})
int_str_dict = {str(i):k for k, i in str_int_dict.items()}

def base_convert(A, baseA, baseB: int):
    """ Converts the base of the number to base. """
    num_int = sum(str_int_dict[num]*baseA**(len(A)-1-i) for i, num in enumerate(A))
    num_digits = math.floor(math.log(num_int, baseB))+1
    final_val = ''
    for i in range(num_digits, 0, -1):
      print(num_int)
      final_val = int_str_dict[str(num_int % baseB)] + final_val
      num_int //= baseB
    return final_val