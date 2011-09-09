import sys
import re

def replace(input_file, regex, dest):
  in_f = open(input_file, 'r')
  in_str = in_f.read()
  in_f.close()

  out_f = open(input_file, 'w')
  p = re.compile(regex)#,re.S|re.I) # some times not work.
  #search = re.search(regex, in_str)
  #match.group()
  out_str = p.sub(dest, in_str)
  out_f.write(out_str)
  out_f.close()


replace(sys.argv[1], sys.argv[2], sys.argv[3])
