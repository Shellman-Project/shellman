#!/usr/bin/env bats

setup() {
  mkdir -p tmp
  echo -e "line 1\nline 2\nerror\nline 4" > tmp/test.txt
}

teardown() {
  rm -rf tmp
}

@test "count_lines returns correct match count" {
  run ./bin/shellman count_lines tmp/test.txt --contains error
  [ "$status" -eq 0 ]
  [[ "$output" =~ "Matching lines: 1" ]]
}

@test "count_lines handles missing files" {
  run ./bin/shellman count_lines tmp/missing.txt
  [ "$status" -ne 0 ]
}
