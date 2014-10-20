int func8(int a, int b, int c, int d, int e, int f, int g, int h) {
  return a+b+c+d+e+f+g+h;
}

int cref() {
  return func8(0xcafe, 12, 5, 0x22, 0x23, 0x24, 9, 10) + 0xdeadbeef;
}

