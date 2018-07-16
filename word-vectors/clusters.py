def readFile(filename):
    lines = [line for line in open(filename,'r')]

    # Firdt line is the column titles
    colnames=lines[0].strip().split('\t')[1:]
    rownames = []
    data = []
    for line in lines[1:]:
        p=line.strip().split('\t')
        # First column in each row is the rowname
        rownames.append(p[0])
        # The data for this row is the remainder of the row
        data.append([float(x) for x in p[1:]])
    # print ("Rownames\n",rownames)
    # print ("\nColnames\n",colnames)
    # print ("\ndata\n",data)
    return rownames,colnames,data    