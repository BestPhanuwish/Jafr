test_date="01/08/23"

for test in tests/*
do
    # change home directory to each test directory
    # thanks Preethom Pal in Ed for this method
    # https://edstem.org/au/courses/12949/discussion/1512143
    USER=anon
    export USER
    HOME=$test
    export HOME

    # reset the task or meeting md content in the file to be the origin
    if [ -e "$test/tasks_origin.md" ]; then
        cat "$test/tasks_origin.md" > "$test/tasks.md"
    fi
    if [ -e "$test/meetings_origin.md" ]; then
        cat "$test/meetings_origin.md" > "$test/meetings.md"
    fi

    # passwd file is mock argument since we doesn't need to test it
    # test time is set at 01/08/2023 for display test
    echo "$(basename "$test") is being tested"
    python3 jafr.py passwd $test_date < $test/test.in > $test/actual
    diff $test/test.out $test/actual
done