from math import sqrt
from PIL import Image,ImageDraw

class bicluster:
    def __init__(self,vec,left=None,right=None,distance=0.0,id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance


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

# Pearson correlation to find similarity between 2 list of numbers
def pearson(v1,v2):
    # Simple sums
    sum1 = sum(v1)
    sum2 = sum(v2)

    # Sums of the squares
    sum1Sq = sum([pow(v,2) for v in v1])
    sum2Sq = sum([pow(v,2) for v in v2])

    # Sum of the products 
    pSum = sum([v1[i]*v2[i] for i in range(len(v1))])

    # Calculate r (Pearson score)
    num = pSum - (sum1*sum2/len(v1))
    den = sqrt((sum1Sq-pow(sum1,2)/len(v1))*(sum2Sq-pow(sum2,2)/len(v1)))

    if den == 0: return 0

    return 1.0 - num/den


# The hcluster algorithm

def hcluster(row,distance=pearson):
    distances={}
    currentclustid=-1

    # Clusters are initially just the rows
    clust=[bicluster(row[i],id=i) for i in range(len(row))]

    while len(clust)>1:
        lowestpair = (0,1)
        closest = distance(clust[0].vec,clust[1].vec)

        # looping through every pair looking for the smallest distance
        for i in range(len(clust)):
            for j in range(i+1,len(clust)):
                # distances in the cache of distance calculations
                if (clust[i].id,clust[j].id) not in distances:
                    distances[(clust[i].id,clust[j].id)] = distance(clust[i].vec,clust[j].vec)
                d = distances[(clust[i].id,clust[j].id)]

                if d<closest:
                    closest = d
                    lowestpair=(i,j)

        # calculating the average of the 2 clusters
        mergevec = [(clust[lowestpair[0]].vec[i]+clust[lowestpair[1]].vec[i])/2.0 for i in range (len(clust[0].vec))]

        # creating a new cluster
        newcluster=bicluster(mergevec,left=clust[lowestpair[0]],right=clust[lowestpair[1]],distance=closest,id=currentclustid)                    

        # clusted ids that weren't in the original set are negative
        currentclustid-=1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)
    return clust[0]    

def printclust(clust,labels=None,n=0):
    # indent to make a hierarchy layout
    for i in range(n): print (' '),
    if clust.id<0:
        # negative id means that this is a branch
        print ('-')
    else:
        # positive id means that this is an endpoint
        if labels == None: print (clust.id)
        else: print (labels[clust.id])
    # now print the right and left branches
    if clust.left!=None: printclust(clust.left,labels=labels,n=n+1)
    if clust.right!=None: printclust(clust.right,labels=labels,n=n+1)


def getheight(clust):
    # if end point or leaf return 1
    if clust.left == None and clust.right == None: return 1
    
    # or the height of the tree is the height of its left and right sub trees
    return getheight(clust.left)+getheight(clust.right)

def getdepth(clust):
    # The distance of an endpoint is 0.0
    if clust.left == None and clust.right == None: return 0
    
    # The distance of a branch is the greate of its two sides
    return max(getdepth(clust.left),getdepth(clust.right))+clust.distance

def drawdendrogram(clust,labels,jpeg='clusters.jpg'):
    # height and width
    h = getheight(clust)*20
    w = 1200
    depth=getdepth(clust)

    # width is fixedm so scale distances accordingly
    scaling=float(w-150)/depth

    # create a new image with a white background
    img = Image.new('RGB',(w,h),(255,255,255))
    draw = ImageDraw.Draw(img)

    draw.line((0,h/2,10,h/2),fill=(255,0,0))

    # Draw the first node
    drawnode(draw,clust,10,(h/2),scaling,labels)
    img.save(jpeg,'JPEG')


def drawnode(draw,clust,x,y,scaling,labels):
    if clust.id<0:
        h1=getheight(clust.left)*20
        h2=getheight(clust.right)*20
        top=y-(h1+h2)/2
        bottom=y+(h1+h2)/2

        # Line length
        ll = clust.distance*scaling

        # Vertical line from this cluster to children
        draw.line((x,top+h1/2,x,bottom-h2/2),fill=(255,0,0))

        # Horizontal line to left item
        draw.line((x,top+h1/2,x+ll,top+h1/2),fill=(255,0,0))

        # Horizontal line to right item
        draw.line((x,bottom-h2/2,x+ll,bottom-h2/2),fill=(255,0,0))

        # Call the function to draw the left and right nodes
        drawnode(draw,clust.left,x+ll,top+h1/2,scaling,labels)
        drawnode(draw,clust.right,x+ll,bottom-h2/2,scaling,labels)
    else:
        # If this is an endpoint, draw the item label
        draw.text((x+5,y-7),labels[clust.id],(0,0,0))