for KILLPID in `ps ax | grep 'Xvfb' | awk ' { print $1;}'`; do 
  kill -9 $KILLPID;
done

for KILLPID in `ps ax | grep 'chromedriver' | awk ' { print $1;}'`; do 
  kill -9 $KILLPID;
done

for KILLPID in `ps ax | grep '\bchrome\b' | awk ' { print $1;}'`; do 
  kill -9 $KILLPID;
done
