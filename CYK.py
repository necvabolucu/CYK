from nltk import grammar, parse
from nltk.parse.generate import generate
from nltk.tree import Tree


class CYKParser():
    def __init__(self):
        self.grammar = grammar.FeatureGrammar.fromstring(open("french-grammar.txt", "r").readlines())
        self.cng_grammar = self.grammar.chomsky_normal_form()
        
    def find_children(self, nt, trees):
        child = []
        for tree in trees:
            if tree.label() == nt:
                child.append(tree)
        return child
        
    def find_lhs(self, non_term_list1, non_term_list2, tree_up, tree_down):
        non_term_list = []
        trees = []
        for nt in non_term_list1: # for each non terminal in first cell
            prod = self.cng_grammar.productions(rhs = nt)
            for pr in prod:
            
                if pr.rhs()[1] in non_term_list2:
                    non_term_list.append(pr.lhs())

                    left = self.find_children(nt,tree_up)
                    right = self.find_children(pr.rhs()[1],tree_down)
                    
                    for l_tree in left:
                        for r_tree in right:
                            x = Tree(pr.lhs(),[l_tree,r_tree])
                            if x not in trees:                        
                                trees.append(x)

        return non_term_list ,trees


    def parse(self, sentence):
        n = len(sentence)
        
        chart = [[ set() for i in range(n+1)] for i in range(n+1)]
        nodes_back = [[[] for i in range(n+1)] for i in range(n+1)]
        
        #find diagonals
        for i in range(n):
            for prod in self.grammar.productions(rhs=sentence[i]):
                chart[i][i+1].add(prod.lhs())
                nodes_back[i][i+1].append(Tree(prod.lhs(), [prod.rhs()[0]]))
                
        for width in range(2,n+1):
            for i in range(0,n-width+1):
                for j in range(1, width):
                    prods,trees = self.find_lhs(chart[i][i+j],chart[i+j][i+width],nodes_back[i][i+j],nodes_back[i+j][i+width])

                    for pr in prods:
                        chart[i][i+width].add(pr)   
                    for tree in trees:
                        nodes_back[i][i+width].append(tree)

        return chart,nodes_back
    
    def print_trees(self, trees):
        n = len(trees)
        count = 1
        for tree in trees:
            if count<n:
                print(tree[count])
                # if tree.label() == start:
                count += 1
        
    def checkparser(self, sentence):
        print("Check parser")
        chart,nodes_back = self.parse(sentence)
        print('---->Sentence is in the parser')
        self.print_trees(nodes_back)

def main():
    """Implemented scratch CYK parser"""
    cyk = CYKParser()
    sentence = "un garcon parle la poisson".split()
    cyk.checkparser(sentence)
    
def nltkparser():
    """NLTK CYK parser"""
    g =  grammar.FeatureGrammar.fromstring(open("french-grammar1.txt", "r").readlines())
    parser = parse.FeatureEarleyChartParser(g)

    tokens = "un garcon parle la poisson".split()

    trees = parser.parse(tokens)
    for tree in trees: print(tree)

main()
# nltkparser()