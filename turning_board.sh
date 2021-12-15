cd ./src/Controls

case "$OSTYPE" in
  linux*)   python3 ./turing_board_motor_test.py /dev/tty/ACM0;;
  msys*)    py ./turing_board_motor_test.py COM8;;
  *)        echo "unknown: $OSTYPE" ;;
esac