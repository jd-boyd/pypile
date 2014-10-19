int func2(int x) {
  return x - 12;
}

int cref() {
  return func2(0xcafe) + 0xdeadbeef;
}

