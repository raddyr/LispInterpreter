ttype = {}

for op in ['+','-','*','/','<','<=','>','>=','!=','==','&&','||','|','&','<<','>>','^','%']:
    ttype[op] = {}
    for left in ['string', 'int', 'float']:
        ttype[op][left] = {}

        # operacje porownania
        if op in ['<','<=','>','>=','!=','==']:
            for right in ['string', 'int', 'float']:
                if (left != 'string' and right != 'string') or (left == right == 'string'):
                    ttype[op][left][right] = 'int'
                else:
                    ttype[op][left][right] = 'None'

        # operacje arytmetyczne
        if op in ['+','-','*','/']:
            for right in ['string','int','float']:
                if (left == right == 'int'):
                    ttype[op][left][right] = 'int'
                elif (left != 'string' and right != 'string'):
                    ttype[op][left][right] = 'float'
                elif (left == 'string' and right == 'string' and op == '+'):
                    ttype[op][left][right] = 'string'
                elif (left == 'string' and right == 'int' and op == '*'):
                    ttype[op][left][right] = 'string'
                else:
                    ttype[op][left][right] = 'None'

        # operacje binarne i logiczne, modulo
        if op in ['&&','||','|','&','<<','>>','^','%']:
            for right in ['string','int','float']:
                if left == 'int' and right == 'int':
                    ttype[op][left][right] = 'int'
                else:
                    ttype[op][left][right] = 'None'
 
