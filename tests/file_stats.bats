#!/usr/bin/env bats

setup() {
  mkdir -p tmp
  echo "line one" > tmp/testfile.log
}

teardown() {
  rm -rf tmp
}

@test "shows lines, size and extension" {
  run ./bin/shellman file_stats tmp/testfile.log
  [ "$status" -eq 0 ]
  [[ "$output" =~ "Lines:" ]]
  [[ "$output" =~ "Size:" ]]
  [[ "$output" =~ "Extension: .log" ]]
}
