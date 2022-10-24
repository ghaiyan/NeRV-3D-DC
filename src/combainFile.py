combine =[]

with open("/home/ghaiyan/project/3d/chrtest/test.hic") as xh:
  with open('/home/ghaiyan/project/3d/chrtest/bins.txt') as yh:
    with open("/home/ghaiyan/project/3d/chrtest/test-has.hic","w") as zh:
      #Read first file
      xlines = xh.readlines()
      #Read second file
      ylines = yh.readlines()
      #Combine content of both lists
      #combine = list(zip(ylines,xlines))
      #Write to third file
      for i in range(len(xlines)):
        line = ylines[i].strip() + ' ' + xlines[i]
        zh.write(line)