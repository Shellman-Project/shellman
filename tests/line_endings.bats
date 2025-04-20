#!/usr/bin/env bats

setup() {
  mkdir -p tmp
  echo -e "line1\r\nline2\r\n" > tmp/crlf.txt
  echo -e "line1\nline2\n" > tmp/lf.txt
  cp tmp/crlf.txt tmp/work.txt
}

teardown() {
  rm -rf tmp
}

@test "line_endings converts CRLF to LF" {
  run ./bin/shellman line_endings --file tmp/work.txt --to lf
  [ "$status" -eq 0 ]
  run file tmp/work.txt
  [[ "$output" =~ "ASCII text" ]]
  ! grep -q $'\r' tmp/work.txt
}

@test "line_endings converts LF to CRLF" {
  cp tmp/lf.txt tmp/work.txt
  run ./bin/shellman line_endings --file tmp/work.txt --to crlf
  [ "$status" -eq 0 ]
  run file tmp/work.txt
  [[ "$output" =~ "ASCII text" ]]
  grep -q $'\r' tmp/work.txt
}

@test "line_endings errors on missing --to" {
  run ./bin/shellman line_endings --file tmp/lf.txt
  [ "$status" -ne 0 ]
  [[ "$output" =~ "--to required" ]]
}

@test "line_endings errors on invalid --to value" {
  run ./bin/shellman line_endings --file tmp/lf.txt --to unknown
  [ "$status" -ne 0 ]
  [[ "$output" =~ "--to must be 'lf' or 'crlf'" ]]
}

@test "line_endings works on directory with extension filter" {
  cp tmp/lf.txt tmp/test1.sh
  cp tmp/crlf.txt tmp/test2.txt
  run ./bin/shellman line_endings --dir tmp --ext .sh --to crlf
  [ "$status" -eq 0 ]
  grep -q $'\r' tmp/test1.sh
}
