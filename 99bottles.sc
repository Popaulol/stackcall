def 0
      1  2  3  4  5  6  7  8  9
  10 11 12 13 14 15 16 17 18 19
  20 21 22 23 24 25 26 27 28 29
  30 31 32 33 34 35 36 37 38 39
  40 41 42 43 44 45 46 47 48 49
  50 51 52 53 54 55 56 57 58 59
  60 61 62 63 64 65 66 67 68 69
  70 71 72 73 74 75 76 77 78 79
  80 81 82 83 84 85 86 87 88 89
  90 91 92 93 94 95 96 97 98 99

  1 call
end

# main loop
def 1
  dup        # 99, 98, 97, ...,  2,  1
  100 -      #  1,  2,  3, ..., 98, 99
  99 swap // #  0,  0,  0, ...,  0,  1
  2 +        #  2,  2,  2, ...,  2,  3
  call
  1 call
end

# print lyrics for one iteration
def 2
  5  call    # _ BoBotW
  32 putchar # <space>
  4  call    # _ BoB
  32 putchar # <space>
  6  call    # T1DPiA
  32 putchar # <space>
  1  swap -
  5  call    # _-1 BoBotW
  10 putchar # \n
  drop
end

# last and exit
def 3
  5   call    # 1 BoBotW
  32  putchar # <space>
  4   call    # 1 BoB
  32  putchar # <space>
  6   call    # T1DPiA
  32  putchar # <space>
  78  putchar # N
  77  putchar # M
  66  putchar # B
  111 putchar # o
  66  putchar # B
  111 putchar # o
  116 putchar # t
  87  putchar # W
  exit
end

# _ BoB
def 4
  dup
  out         # _
  32  putchar # <space>
  66  putchar # B
  111 putchar # o
  66  putchar # B
end

# _ BoBotW
def 5
  4   call    # _ BoB
  111 putchar # o
  116 putchar # t
  87  putchar # W
end

# T1DPiA
def 6
  84  putchar # T
  49  putchar # 1
  68  putchar # D
  80  putchar # P
  105 putchar # i
  65  putchar # A
end
