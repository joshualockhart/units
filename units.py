import copy 

class IncompatibleUnitsError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

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

    def equals(self, unit):
        n = unit.to(self)
        if n != -1:
            if n.coefficient == self.coefficient:
                return True
        return False

        unit_ = copy.copy(unit)
        if unit_.to(self) != None:
            if unit_.coefficient == self.coefficient:
                return True
        return False
    
    def add(self, *others):
        others_ = [o.to(self) for o in others]

        for o in others_:
            if o == -1:
                raise IncompatibleUnitsError("You're a twit")
                return Expression((self,))

        return Expression((self,)+tuple(others_))

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
        return str(self.coefficient)+' '+prod

    def to(self, other):
        my_kinds = [x.kind for x in self.data.keys()]
        my_kinds.sort()
        
        kinds = [x.kind for x in other.data.keys()]
        kinds.sort()
        
        if my_kinds != kinds:
            raise IncompatibleUnitsError("You're a twit")
            return -1

        c = self.coefficient

        for u in self.data.keys():
            for key in other.data.keys():
                if key.kind == u.kind:
                    if other.data[key] != self.data[u]:
                        raise IncompatibleUnitsError("You're a twit")
                        return -1
                    else:
                        my_fund = u.fundamental
                        fund = key.fundamental
                        c*=float(my_fund)/float(fund)**self.data[u]


        return Term(other.data,c)

    def value(self):
        return self.coefficient

    def unit(self):
        string = ""

        for key in self.data.keys():
            if self.data[key]>1:
                string += key.name+"^"+str(self.data[key]) + " "
            else:
                string += key.name + " "
        return string
        


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
"""
centimetres = Term('centimetres')
metres = Term('metres')
litres = Term('litres')
millilitres = Term('millilitres')

print (5*metres).equals(500*centimetres)

quit()

y = 5*centimetres*5*centimetres
print (y).to(metres*metres)

print ""

print (5*millilitres*metres).to(litres*metres).unit()
"""