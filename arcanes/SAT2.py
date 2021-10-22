__author__ = 'Gastaldi'
__Filename__ = 'SAT'
__Creationdate__ = '02/10/2020'

import PileCNF as p
from math import factorial


def combin(n, k):
    return factorial(n)//(factorial(k)*factorial(n - k))


def ImportCNF(name):
    '''

    :param name: name of file
    :return: list with this form [[Nb_lit, Nb_clause], [Lit_Claus1], [Lit_Claus2], ... , [Lit_Claus n]]
    '''
    with open(name, 'r') as filin:
        line = filin.readlines()
    CNF = dict()
    CNF['nb_lit'] = int(line[0].split()[1])
    CNF['nb_clause'] = int(line[1].split()[1])
    i = 0
    for Literal in line[2:]:
        X = Literal.split()
        CNF[i] = [int(X[i]) for i in range(2, len(X), 1)]
        i += 1
    return CNF


def ExportCNF(name, CNF):
    files = open(name, "w")
    files.write('literal: ' + str(CNF['nb_lit']) + '\n')
    files.write('clause: ' + str(CNF['nb_clause']) + '\n')
    for i in range(len(CNF.values()) - 2):
        files.write(str(i + 1) + ' :')
        for val in list(CNF[i]):
            files.write(' ' + str(val))
        files.write('\n')
    files.close()


def PrepareCNF(CNF):
    ClauseState = [False] * CNF['nb_clause']
    LenClause = [len(CNF[i]) for i in range(len(CNF.values()) - 2)]
    LiteralState = [0] * (CNF['nb_lit'] + 1)
    return ClauseState, LenClause, LiteralState


def countLit(CNF):
    compt = {0: 0}
    for i in range(CNF['nb_clause']):
        for lit in CNF[i]:
            if lit in compt.keys():
                compt[lit] += 1
            else:
                compt[lit] = 1
    return compt


def ClauseUnitary(CNF, ClauseState, LenClause, LiteralState):
    for i in range(CNF['nb_clause']):
        if LenClause[i] == 1:
            if not ClauseState[i]:
                for lit in CNF[i]:
                    if LiteralState[abs(lit)] == 0:
                        LiteralState[abs(lit)] = 2
                        return lit, LiteralState
    return False, LiteralState


def ClausePur(CNF, ClauseState, LenClause, LiteralState):
    test = [None] * (CNF['nb_lit'] + 1)
    for i in range(len(ClauseState)):
        if not ClauseState[i]:
            for lit in CNF[i]:
                if LiteralState[abs(lit)] == 0:
                    if test[abs(lit)] == -lit:
                        test[abs(lit)] = 0
                    elif test[abs(lit)] != 0:
                        test[abs(lit)] = lit
    for val in test:
        if val != 0 and val != None:
            LiteralState[abs(val)] += 1
            return val, LiteralState
    return False, LiteralState


def FirstSatisfy(countLit, LiteralState):
    keys = 0
    maxi = -1
    for key, val in countLit.items():
            if maxi < val and LiteralState[abs(key)] == 0:
                maxi = val
                keys = key
    LiteralState[abs(keys)] += 1
    return keys, LiteralState


def FirstFail(countLit, LiteralState):
    lit, State = FirstSatisfy(countLit, LiteralState)
    return -lit, State


def HStandard(countLit, LiteralState):
    lit = LiteralState.index(0, 1)
    LiteralState[abs(lit)] += 1
    return lit, LiteralState


def OneStep(CNF, Lit, ClauseState, LenClause, LiteralState, countList, pile):
    for i in range(len(ClauseState)):
        if Lit in CNF[i]:
            ClauseState[i] = True
            LenClause[i] -= 1
            for l in CNF[i]:
                countList[l] -= 1
        elif -Lit in CNF[i]:
            LenClause[i] -= 1
    countList[Lit] = 0
    countList[-Lit] = 0
    if Lit > 0:
        pile.Pil(abs(Lit), True)
    else:
        pile.Pil(abs(Lit), False)
    return ClauseState, LenClause, LiteralState, countList, pile


def Back(CNF, ClauseState, LenClause, LiteralState, countList, pile):
    lit, val = pile.Pop()
    if not val:
        lit = -lit
    ValT = pile.getLit().copy()
    for i in range(len(ValT)):
        if not pile.getVal()[i]:
            ValT[i] = - ValT[i]
    for i in range(CNF['nb_clause']):
        if ClauseState[i]:
            if lit in CNF[i]:
                LenClause[i] += 1
                ClauseState[i] = False
                for litCNF in CNF[i]:
                    if not ClauseState[i] and litCNF in ValT:
                        ClauseState[i] = True
                if not ClauseState[i]:
                    for litCNF in CNF[i]:
                        countList[litCNF] += 1
            elif -lit in CNF[i]:
                LenClause[i] += 1
        else:
            for litCNF in CNF[i]:
                if litCNF == lit or litCNF == - lit:
                    LenClause[i] += 1
                    countList[litCNF] += 1
    return ClauseState, LenClause, LiteralState, countList, pile, lit


def DPLL(CNF, Heuristique = HStandard, all_model = False):
    ClauseState, LenClause, LiteralState = PrepareCNF(CNF)
    countList = countLit(CNF)
    Pile = p.PileCNF()
    NeedNextLit = True
    Continue = True
    Fback = False
    Model = []
    node = 1
    while (False in ClauseState or all_model) and Continue:
        if NeedNextLit:
            NextLit, LiteralState = ClauseUnitary(CNF, ClauseState, LenClause, LiteralState)
            if not NextLit:
                NextLit, LiteralState = ClausePur(CNF, ClauseState, LenClause, LiteralState)
            if not NextLit:
                NextLit, LiteralState = Heuristique(countList, LiteralState)
        if not Fback:
            ClauseState, LenClause, LiteralState, countList, Pile = OneStep(CNF, NextLit, ClauseState, LenClause, LiteralState, countList, Pile)
            node += 1
        i = 0
        back = True
        NeedNextLit = True
        while i < CNF['nb_clause'] and back:
            if (not ClauseState[i] and LenClause[i] == 0) or Fback:
                back = False
                Fback = False
                ClauseState, LenClause, LiteralState, countList, pile, lastlit = Back(CNF, ClauseState, LenClause, LiteralState, countList, Pile)
                if LiteralState[abs(lastlit)] == 1:
                    NeedNextLit = False
                    NextLit = -lastlit
                    LiteralState[abs(lastlit)] += 1
                elif LiteralState[abs(lastlit)] == 2:
                    while LiteralState[abs(lastlit)] == 2:
                        LiteralState[abs(lastlit)] = 0
                        ClauseState, LenClause, LiteralState, countList, pile, lastlit = Back(CNF, ClauseState,
                                                                                              LenClause, LiteralState,
                                                                                              countList, Pile)
                    if not lastlit:
                        Continue = False
                    else:
                        NeedNextLit = False
                        NextLit = -lastlit
                        LiteralState[abs(lastlit)] += 1
            i += 1
        if not (False in ClauseState):
            Model += [(Pile.Val, Pile.Literral)]
            Fback = True
            NeedNextLit = False
    return Model, node


def pigeon(n):
    clause = n + n * combin(n - 1, 2) + (n - 1) * combin(n, 2)
    CNF = {i:[] for i in range(clause)}
    CNF['nb_clause'] = clause
    CNF['nb_lit'] = n * (n - 1)
    clause_nb = 0
    for i in range(1, n + 1, 1):
        for j in range(1, n, 1):
            CNF[clause_nb] += [((i - 1) * (n - 1) + j)]
        clause_nb += 1
    for i in range(1, n + 1, 1):
        for j in range(1, n, 1):
            for k in range(j + 1, n, 1):
                CNF[clause_nb] += [-((i - 1) * (n - 1) + j), -((i - 1) * (n - 1) + k)]
                clause_nb += 1
    for i in range(1, n, 1):
        for j in range(1, n + 1, 1):
            for k in range(j + 1, n + 1, 1):
                CNF[clause_nb] += [-((j - 1) * (n - 1) + i), -((k - 1) * (n - 1) + i)]
                clause_nb += 1
    return CNF

def Reine(n):
    CNF = {i:[] for i in range(n)}
    CNF['nb_lit'] = n * n
    clause_nb = 0
    for i in range(1, n + 1, 1):
        for j in range(1, n + 1, 1):
            CNF[clause_nb] += [((i - 1) * n + j)]
        clause_nb += 1
    for i in range(1, n + 1, 1):
        for j in range(1, n + 1, 1):
            for k in range(j + 1, n + 1, 1):
                CNF[clause_nb] = [-((i - 1) * n + j), -((i - 1) * n + k)]
                clause_nb += 1
                CNF[clause_nb] = [-((j - 1) * n + i), -((k - 1) * n + i)]
                clause_nb += 1
    for i in range(1, n, 1):
        for j in range(i, ((n - i) * (n + 1)) + i + 1, n + 1):
            for k in range(j + n + 1, ((n - i) * (n + 1)) + i + 1, n + 1):
                CNF[clause_nb] = [-j, -k]
                clause_nb += 1
                if i != 1:
                    CNF[clause_nb] = [-(j + (i - 1) * (n - 1)), -(k + (i - 1) * (n - 1))]
                    clause_nb += 1
    for i in range(n, 1, -1):
        for j in range(i, (i * (n - 1)) + i, n - 1):
            for k in range(j + n - 1, (i * (n - 1)) + i, n - 1):
                CNF[clause_nb] = [-j, -k]
                clause_nb += 1
                if i != n:
                    CNF[clause_nb] = [-(j + (n - i) * (n + 1)), -(k + (n - i) * (n + 1))]
                    clause_nb += 1
    CNF['nb_clause'] = len(CNF.values()) - 1
    return CNF




