


class SequenceAlignment(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.solution = []
        self.delta_e=30
        self.apha ={'A':{'A':0,'C':110,'G':48,'T':94},'C':{'A':110,'C':0,'G':118,'T':48},'G':{'A':48,'C':118,'G':0,'T':110},'T':{'A':94,'C':48,'G':110,'T':0}}
    delta = lambda self, x, y,alpha, i, j: alpha[x[i]][y[j]]

    def find_solution(self, OPT, m, n):
        if m == 0 and n == 0:
            return

        # We can only do insert if n != 0, align if there are element in both x, y, etc.
        insert = OPT[m][n - 1] + self.delta_e if n != 0 else float("inf")
        align = (
            OPT[m - 1][n - 1] + self.delta(self.x, self.y,self.apha, m - 1, n - 1)
            #OPT[m - 1][n - 1] + self.apha[x[m]][y[n]]
            if m != 0 and n != 0
            else float("inf")
        )
        delete = OPT[m - 1][n] + self.delta_e if m != 0 else float("inf")
        print(insert,align,delete)
        best_choice = min(insert, align, delete)

        if best_choice == insert:
            self.solution.append("insert_" + str(self.y[n - 1]))
            return self.find_solution(OPT, m, n - 1)

        elif best_choice == align:
            self.solution.append("align_" + str(self.y[n - 1]))
            return self.find_solution(OPT, m - 1, n - 1)

        elif best_choice == delete:
            self.solution.append("remove_" + str(self.x[m - 1]))
            return self.find_solution(OPT, m - 1, n)

    def alignment(self):
        n = len(self.y)
        m = len(self.x)
        OPT = [[0 for i in range(n + 1)] for j in range(m + 1)]

        for i in range(0, m + 1):
            OPT[i][0] = i*self.delta_e
            #print(OPT[i][0])

        for j in range(0, n + 1):
            OPT[0][j] = j*self.delta_e
           # print(OPT[0][j])


        for i in range(1, m + 1):
            for j in range(1, n + 1):
                OPT[i][j] = min(
                    OPT[i - 1][j - 1] + self.delta(self.x, self.y,self.apha, i - 1, j - 1),
                    OPT[i - 1][j] + self.delta_e,
                    OPT[i][j - 1] + self.delta_e,
                )  # align, delete, insert respectively

        self.find_solution(OPT, m, n)
        #print(OPT[m][n])
        return (OPT[m][n], self.solution[::-1])


if __name__ == '__main__':
    x = 'A'
    y = 'AT'
    print('We we want to transform: ' + x + ' to: ' + y)
    sqalign = SequenceAlignment(x, y)
    min_edit, steps = sqalign.alignment()
    print('Minimum amount is : ' + str(min_edit))
    print('And the way to do it is: ' + str(steps))


