#include <stdio.h>
int cref();

int main()
{
  int ret = cref();
  printf("ret 0x%0x\n", ret>>2);
  return 0;
}
