class Unit(object):
    def __init__(self, name, kind, fundamental):
        self.kind = kind
        self.name = name
        self.fundamental = fundamental

metres = Unit("metres","length",100)
litres = Unit("litres","volume",1000)
centimetres = Unit("centimetres","length",1)
millilitres = Unit("millilitres","volume",1)

units = {"metres":metres, 
         "litres":litres,
         "centimetres":centimetres,
         "millilitres":millilitres}

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
        unit = units[symbol]
        self.coefficient=coefficient
        self.data={unit:power}

    def from_dictionary(self, data, coefficient=1):
        self.data=data
        self.coefficient=coefficient

    def from_lists(self, symbols=[], powers=[], coefficient=1):
        # TODO: make this work
        self.coefficient=coefficient
        self.data={units[symbol]: exponent for symbol,exponent
                in zip(symbols, powers)}

    def add(self, *others):
        my_kinds = [x.kind for x in self.data.keys()]
        my_kinds.sort()
        my_exponents = self.data.values()
        my_exponents.sort()
        for o in others:
            kinds = [x.kind for x in o.data.keys()]
            kinds.sort()
            exponents = o.data.values()
            exponents.sort()
            if my_kinds != kinds or my_exponents != exponents:
                print "non matching units"
                return Expression((self,))
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
        symbol_strings=[symbol_string(symbol.name, power)
                for symbol, power in self.data.iteritems()]
        prod='*'.join(symbol_strings)
        if not prod:
            return str(self.coefficient)
        if self.coefficient==1:
            return prod
        else:
            return str(self.coefficient)+'*'+prod

    def convertTo(self, unit):
        my_kinds = [x.kind for x in self.data.keys()]
        my_kinds.sort()
        my_exponents = self.data.values()
        my_exponents.sort()
        
        kinds = [x.kind for x in unit.data.keys()]
        kinds.sort()
        exponents = unit.data.values()
        exponents.sort()
        if my_kinds != kinds or my_exponents != exponents:
            print "non matching units"
            return None

        my_funds = [x.fundamental for x in self.data.keys()]
        my_funds.sort()

        funds = [x.fundamental for x in unit.data.keys()]
        funds.sort()

        for i,j in zip(my_funds,funds):
            self.coefficient*=float(i)/float(j)
        self.data = unit.data
    


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