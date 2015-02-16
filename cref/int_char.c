int int_char(int x) {
  return (x << 6) | 0x000f;
}

int cref() {
  return int_char(4);
}

