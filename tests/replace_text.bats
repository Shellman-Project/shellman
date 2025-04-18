#!/usr/bin/env bats

setup() {
  mkdir -p tmp
  echo -e "start here\nstart again\nnothing to see" > tmp/sample.txt
}

teardown() {
  rm -rf tmp
}

@test "replaces text correctly with --in-place" {
  run ./bin/shellman replace_text tmp --find start --replace end --ext txt --in-place
  [ "$status" -eq 0 ]
  grep -q "end here" tmp/sample.txt
  grep -q "end again" tmp/sample.txt
}

@test "does not modify file without --in-place" {
  cp tmp/sample.txt tmp/original.txt
  run ./bin/shellman replace_text tmp --find start --replace end --ext txt
  [ "$status" -eq 0 ]
  grep -q "start here" tmp/sample.txt
  diff tmp/sample.txt tmp/original.txt > /dev/null
}

@test "preview mode shows diff" {
  run ./bin/shellman replace_text tmp --find start --replace end --ext txt --preview
  [ "$status" -eq 0 ]
  [[ "$output" =~ "---" ]]  # diff header expected
  [[ "$output" =~ "+end here" ]]
}

@test "skips file if text not found" {
  echo "this is fine" > tmp/nothing.txt
  run ./bin/shellman replace_text tmp --find NOMATCH --replace new --ext txt
  [ "$status" -eq 0 ]
  [[ "$output" == *"No files matched"* ]]
}
