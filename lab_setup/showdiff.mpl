ShowDerivative :=
 proc(fx,x0,h,xmin,xmax,ymin,ymax)
  local dy,x1,y0,y1,m,n,p0,p1,p2,p3,p4;
  y0 := evalf(subs(x=x0,fx));
  dy := simplify(diff(fx,x));
  m  := evalf(subs(x=x0,dy));
  x1 := evalf(x0+h);
  y1 := evalf(subs(x=x1,fx));
  n  := evalf((y1-y0)/h);

  p0 := plot(fx,x=xmin..xmax,ymin..ymax,
             color=red);
  p1 := PLOT(CURVES([[x0,0],[x0,y0],[0,y0]]));
  p2 := plot(y0 + m*(x-x0),x=xmin..xmax,ymin..ymax,
             color=blue);
  p3 := PLOT(CURVES([[x1,0],[x1,y1],[0,y1]]));
  p4 := plot(y0 + n*(x-x0),x=xmin..xmax,ymin..ymax,
             color=green);

  print(plots[display](p0,p1,p2,p3,p4));
#  print('y' = fx, 'dy'/'dx' = dy);
#  print('x'[0] = x0,'y'[0] = y0);
#  print('x'[1] = x1,'y'[1] = y1);
#  print(`Slope of the chord (shown in green):`);
#  print((``(y1) - ``(y0))/(``(x0) - ``(x1)) = n);
#  print(abs('dy'/'dx')[x='x'[0]] = m);
 end:

# ShowDerivative(x^2,1,0.5,-1,2,0,4);

MakeSpreadsheet := 
 proc()
  with(Spread);
  ssid := CreateSpreadsheet();
  SetCellFormula(ssid,"A1","'y'");
  SetCellFormula(ssid,"B1","'dy'/'dx'");
  SetCellFormula(ssid,"C1","'x'[0]");
  SetCellFormula(ssid,"D1","'y'[0]");
  SetCellFormula(ssid,"E1","'dy'/'dx',`at x` = 'x'[0]");

  SetCellFormula(ssid,"A2","x^2");
  SetCellFormula(ssid,"B2","diff(~A1,x)");
  SetCellFormula(ssid,"C2","1");
  SetCellFormula(ssid,"D2","subs(x=~C2,~A2)");
  SetCellFormula(ssid,"E2","subs(x=~C2,~B2)");

  SetCellFormula(ssid,"A4","");
  SetCellFormula(ssid,"B4","");
  SetCellFormula(ssid,"C4","");
  SetCellFormula(ssid,"D4","");
  SetCellFormula(ssid,"E4","");

  SetCellFormula(ssid,"A5","");
  SetCellFormula(ssid,"B5","");
  SetCellFormula(ssid,"C5","");
  SetCellFormula(ssid,"D5","");
  SetCellFormula(ssid,"E5","");

 end: