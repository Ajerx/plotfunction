import pydot


class Graph:
    def __init__(self, k, dictfornodes, p):

        self.k = k
        self.p = p
        self.dictfornodes = dictfornodes
        self.path = 'graph1.png'
        self.dictforgraph = {}
        self.edgesdict = {}
        self.initcalc()

    def initcalc(self):
        # di = {0: 7, 1: 5, 2: 2}

        graph = pydot.Dot(graph_type='digraph')

        self.count(self.k, self.dictfornodes)

        for i in range(0, self.p**self.k):
            self.dictforgraph[i] = pydot.Node("{}".format(i), shape = 'circle')
            graph.add_node(self.dictforgraph[i])

        print(self.dictforgraph)

        for key, value in self.edgesdict.items():
            graph.add_edge(pydot.Edge(self.dictforgraph[key], self.dictforgraph[value]))

        graph.write_png(self.path)
        # graph.write(self.path, format='png')

    def count(self, k, d):

        self.edgesdict = {}
        p_exp_k = self.p ** k
        for x in range(p_exp_k):
            temp = 0
            print('x:', x)
            for key, value in d.items():
                temp += value * (x ** key)
            print('Без mod: ', temp)
            print('С mod: ', temp % p_exp_k, '\n')

            self.edgesdict[x] = temp % p_exp_k

        print('edgesdict: ', self.edgesdict)




if __name__ == '__main__':
    d = Graph(2, {0: 7, 1: 5, 2: 2}, 2)
