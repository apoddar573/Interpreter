# Interpreter
Built a python based Interpreter for a PASCAL like language. 

## Syntax of the Given Toy Language

Assignment statement:
```
a := b;
```

while statement:
```
while a>=b do 
 N := m;
 a := b;
 done
```

if statement:
```
if a=b then
 a := 9;
else 
 b := 5;
fi
```

print statements:            
```
print "Hi!";                 #for avoiding new line character at the end
print a;
println b;
println "Hi!";               #for printing a new line at the end
```

functions:
```
function fact(a, b)
begin 
a := 5;
b := 4;
return a*b;
end
```

We have used parsing and attempted to solve the problem using an Object Oriented Approach rather than a functional approach.

## Working of the Interpreter

The code in interpretor1104.py is efficiently interpreting assignment statements, if statements and while loops.
The code is also able to run while loops inside if statements, if inside if and while inside while.
However, the code is unable to run if statements inside while loops for some reason.
Also, we cannot assign negative values in the beginning even though the variables can take negative values during the run time of the program. there is no such restriction for decimals.

The code prints the dictionary of the set of variables and functions at the termination of the program.

This code can also work for functions. The one problems still remaining is of the if statements inside while loops. The input variables to the function should be variables and cannot be numbers or values directly. 


When using print statements also, we cannot print a value(eg,print a+b;). We have to define a variable and then print that variable for the value( d := a+b; print d;)

Apart from the function definition, it identifies zerodivisionerror and variable mismatch when a function is called with wrong number of variables. 
Also, it prints the time of execution of the program.






