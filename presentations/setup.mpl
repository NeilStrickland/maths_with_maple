# This uses a framework that is now deprecated to convert the presentations into
# something more like a PowerPoint slideshow.  It may be possible to refactor it.

with(Worksheet):
with(XMLTools):

os_makedirectory :=
proc(dir::string)
 local parts,parent;
 parts := [util_slashsplit(dir)];
 parent := "";
 while parts <> [] do
  if parent = "" then
   parent := parts[1];
  else
   parent := cat(parent,"\\",parts[1]);
  fi;
  parts := parts[2..-1];
  if not(os_direxists(parent)) then
   os_system(cat("mkdir \"",parent,"\""));
  fi;
 od;
 NULL;
end:

os_direxists := 
proc(dir)
 try
  return isdir(dir);
 catch :
  return false;
 end;
end:

os_system :=
proc()
 local ignoreerror,ret,msg;

 ret := ssystem(sprintf(args));

 if ret[1] <> 0 then
  msg := 
   sprintf("%s\n%s %A\n%s %A\n%s %A\n",
    "Operating system error:",

    "Command:",sprintf(args),

    "Return value:",ret[1],
    "Output:",ret[2]);
  ERROR(msg);
 fi;

 RETURN(ret[2]);
end:

util_slashsplit :=
proc(s::string)
 local b,n,t,i;

 b := subs(92 = 47,convert(s,bytes)):
 n := nops(b):
 while (n > 0 and b[n] = 47) do n := n - 1; od;
 if (n = 0) then RETURN(); fi;
 t := select((i,x) -> x[i] = 47,[seq(i,i=1..n)],b):
 t := [0,op(t),n+1]:
 seq(convert(b[(t[i]+1)..(t[i+1]-1)],bytes),i=1..nops(t)-1);

end:

presdir := 
 "U:\\Teach\\MAS100\\presentations":

currentdir(presdir):

if not(member(presdir,[libname])) then
 libname := libname,presdir;
fi;

content_as_TEXT := 
 proc(file::string)
  local t,line;
  t := NULL;
  line := readline(file);
  while (line <> 0) do
   if length(line) <= 10 then 
    line := cat(``,line,` `);
   fi;
   t := t,line;
   line := readline(file);
  od;
  return(TEXT(t));
 end:

#long_xml := ReadFile("demo/long.mws"):
save_help := 
 proc(tpc)
  local file,txt;
  global presdir;
  file := cat(tpc,".mws");
  txt := content_as_TEXT(file);
  print(
   INTERFACE_HELP(
    'insert',
    'topic'=convert(tpc,name),
    'active'=true,
    'text'=txt,
    'helpfile'=convert(presdir,name)
   )
  );
 end:

split_worksheet :=
 proc(nam::string) 
  local whole,parts,part,vrsion,styles,view,newview,pnums,child,i,
        file0,file,txt,topic,hfile;
  global libname,PARTS;
  whole := Worksheet:-ReadFile(cat(nam,".mws"));
  parts := NULL;
  part  := NULL;
  vrsion := GetChild(whole,1);
  styles := GetChild(whole,2);
  view   := GetChild(whole,-2);
  newview :=
   XMLElement("View-Properties",[],
    [XMLElement("Zoom",["percentage" = "150"],[])]);
  pnums  := GetChild(whole,-1);
  for i from 3 to ContentModelCount(whole) - 2 do
   child := GetChild(whole,i);
   if ElementTypeName(child) = "Pagebreak" then
    if [part] <> [] then
     parts :=
      parts,
      XMLDocument(XMLElement("Worksheet",[],[vrsion,newview,styles,part,pnums]));
     part := NULL; 
    fi;
   else
    part := part,child;
   fi;
  od; 
  if [part] <> [] then
   parts :=
    parts,
    XMLElement("Worksheet",[],[vrsion,newview,styles,part,pnums]);
   part := NULL; 
  fi;
  parts := [parts];
  PARTS := parts;

  os_makedirectory(nam);
  for i from 1 to nops(parts) do
   part := parts[i];
   if i < nops(parts) then
    part := 
     AddChild(
      part,
      XMLElement(
       "Text-field",
       ["layout" = "Normal", "style" = "Hyperlink"],
       [XMLElement(
         "Hyperlink",
         ["hyperlink" = "true",
          "linktarget" = sprintf("Help:%s/%d",nam,i+1),
          "style" = "hyperlink"],
         ["Next"]
        )
       ]
      ),
      ContentModelCount(part) - 1
     );
   fi;
   file := sprintf("%s/%d.mws",nam,i);
   Worksheet:-WriteFile(
    file,
    XMLDocument(part),
    format = "mws"
   );
   fclose(file);
   txt := content_as_TEXT(file);
   hfile := convert(currentdir(),name);
   topic := convert(sprintf("%s/%d",nam,i),name);
   print(
    INTERFACE_HELP(
     'insert',
     'topic'=topic,
     'active'=true,
     'text'=txt,
     'helpfile'=convert(hfile,name)
    )
   );
  od;
  NULL
 end:
