int func2(int x, int y) {
  return x + y;
}

int cref() {
  return func2(0xcafe, 12) + 0xdeadbeef;
}

