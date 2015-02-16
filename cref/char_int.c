int char_int(int x) {
  return (x >> 8) << 2;
}

int cref() {
  return char_int(0x10f);
}

