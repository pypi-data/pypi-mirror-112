def UpperName(name):
  newname = ""
  splitName = name.split(" ")
  for name in splitName:
    newname += name.capitalize() + " "
  return newname[1:]