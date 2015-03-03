class Term(object):
    def __init__(self, *args):
        lead=args[0]
        if type(lead)==type(self):
            # Copy constructor
            self.data=dict(lead.data)
            self.coefficient=lead.coefficient
        elif type(lead)==int:
            self.from_constant(lead)
        elif type(lead)==str:
            self.from_symbol(*args)
        elif type(lead)==dict:
            self.from_dictionary(*args)
        else:
            self.from_lists(*args)
    def from_constant(self, constant):
        self.coefficient=constant
        self.data={}
    def from_symbol(self, symbol, coefficient=1, power=1):
        self.coefficient=coefficient
        self.data={symbol:power}
    def from_dictionary(self, data, coefficient=1):
        self.data=data
        self.coefficient=coefficient
    def from_lists(self, symbols=[], powers=[], coefficient=1):
        self.coefficient=coefficient
        self.data={symbol: exponent for symbol,exponent
                in zip(symbols, powers)}

    def add(self, *others):
        return Expression((self,)+others)
    def multiply(self, *others):
        result_data=dict(self.data)
        result_coeff=self.coefficient
        # Convert arguments to Terms first if they are
        # constants or integers
        others=map(Term,others)
        for another in others:
            for symbol, exponent in another.data.iteritems():
                if symbol in result_data:
                    result_data[symbol]+=another.data[symbol]
                else:
                    result_data[symbol]=another.data[symbol]
            result_coeff*=another.coefficient
        return Term(result_data,result_coeff)

    def __add__(self, other):
        return self.add(other)
    def __mul__(self, other):
        return self.multiply(other)

    def __rmul__(self, other):
        return self.__mul__(other)
    def __radd__(self, other):
        return self.__add__(other)

    def __str__(self):
        def symbol_string(symbol, power):
            if power==1:
                return symbol
            else:
                return symbol+'^'+str(power)
        symbol_strings=[symbol_string(symbol, power)
                for symbol, power in self.data.iteritems()]
        prod='*'.join(symbol_strings)
        if not prod:
            return str(self.coefficient)
        if self.coefficient==1:
            return prod
        else:
            return str(self.coefficient)+'*'+prod

### "ExpressionConstruct"

class Expression(object):
    def __init__(self, terms=[]):
        self.terms=list(terms)

    def add(self, *others):
        result=Expression(self.terms)
        for another in others:
            if type(another)==Term:
                result.terms.append(another)
            else:
                result.terms+=another.terms
        return result

    def multiply(self, another):
        # Distributive law left as exercise
        pass
    def __add__(self, other):
        return self.add(other)

    def __radd__(self, other):
        return self.__add__(other)

    def __str__(self):
        return '+'.join(map(str,self.terms))

### "withfunc"

x=Term('x')
y=Term('y')

first=Term(5).multiply(Term('x'),Term('x'),Term('y'))
second=Term(7).multiply(Term('x'))
third=Term(2)
expr=first.add(second,third)

### "withop"

x_plus_y=Term('x')+'y'
print x_plus_y.terms[0].data

five_x_ysq=Term('x')*5*'y'*'y'
print five_x_ysq.data, five_x_ysq.coefficient

### "RightUse"

print 5*Term('x')

### "HardTest"

fivex=5*Term('x')
print fivex.data, fivex.coefficient

### "UseString"

first=Term(5)*'x'*'x'*'y'
second=Term(7)*'x'
third=Term(2)
expr=first+second+third
print expr

### "Callable"

class MyCallable(object):
    def __call__(self, name):
        print "Hello, ", name

x=MyCallable()

x("James")
