from __future__ import print_function
import csv, math, random, sys, random
#Calculates Entropy of a node
def Entropy_Calc(rows):
    from math import log
    Results = pure_counts(rows)
    ent_value = 0.0
    for r in Results.keys():
        if (len(rows) == 0):
            prob = 0.0
        else:
            prob = float(Results[r]) / float(len(rows))
        if (prob == 0):
            ent_value = 0.0
        else:
            ent_value = ent_value - prob * log(prob, 2)
    return ent_value

#calculates IG and returns the attribute with max IG
def Information_gain(rows, column_count):
    entropy_old = Entropy_Calc(rows)
    max_IG = 0.0
    informationgain = 0.0
    flag = 0
    for i in range(0, column_count):
        set0, set1 = Divide_Set(rows, i)
        if (len(set0) > 0 and len(set1) > 0):
            rowslength = len(rows)
            p = float(len(set0)) / float(len(rows))
            informationgain = entropy_old - (p * Entropy_Calc(set0) + (1 - p) * Entropy_Calc(set1))
            # print ("i is ",i," - Info is  :",Info)
            if (informationgain > max_IG):
                max_IG = informationgain
                this_attribute = i
                flag = 1
    if (flag == 1):
        # print (attribute)
        return this_attribute
    else:
        return -2

#Node constructor
class tree_node:
    def __init__(self, column=-1, pure=None, value=None, left_child=None, right_child=None, number=None, name=None,
                 count=None, keep=None, numOf0=0, numOf1=0, parent=None):
        self.col = column
        self.pure = pure
        self.value = value
        self.leftchild = left_child
        self.rightchild = right_child
        self.number = number
        self.name = name
        self.keep = keep
        self.noof1 = numOf1
        self.noof0 = numOf0
        self.parent = parent


def Build_Decision_Tree(rows, attribute_length, val):
    global keep
    global leaf_count
    if len(rows) == 0:
        keep = keep + 1
        return tree_node()
    index_ofAttribute = Information_gain(rows, attribute_length)
    if (index_ofAttribute == -2):
        if (pure_counts(rows)['0'] > pure_counts(rows)['1']):
            attri_value = 0
            keep = keep + 1
            leaf_count = leaf_count + 1
            return tree_node(pure=pure_counts(rows), value=attri_value, keep=keep, numOf0=pure_counts(rows)['0'])
        else:
            attri_value = 1
            keep = keep + 1
            leaf_count = leaf_count + 1
            return tree_node(pure=pure_counts(rows), value=attri_value, keep=keep, numOf1=pure_counts(rows)['1'])
    else:

        set0, set1 = Divide_Set(rows, index_ofAttribute)
        right_child_ = Build_Decision_Tree(set1, attribute_length, 1)
        left_child_ = Build_Decision_Tree(set0, attribute_length, 1)
        keep = keep + 1
        temp = tree_node(column=attributes[index_ofAttribute], value=val, left_child=left_child_, right_child=right_child_, number=index_ofAttribute,
                         keep=keep, numOf0=pure_counts(rows)['0'], numOf1=pure_counts(rows)['1'])
        right_child_.parent = temp
        left_child_.parent = temp
        return temp


def Divide_Set(rows, columns):
    set0 = []
    set1 = []
    for row in rows:
        if (row[columns] == '0'):
            set0 = set0 + [row]
        else:
            set1 = set1 + [row]
    return (set0, set1)



def Numbering_node(tree, node_count):
    if (tree is None):
        return node_count
    if (tree.pure is not None):
        tree.keep = 0
        return node_count
    if (tree is not None):
        node_count = node_count + 1;
        tree.keep = node_count
        node_count = Numbering_node(tree.rightchild, node_count)
        node_count = Numbering_node(tree.leftchild, node_count)
    return node_count


def Leaf_counts(decisiontree, count):
    # print(tree.pure)
    if (decisiontree is None):
        return 0
    if (decisiontree.pure is not None):
        return 1
    else:
        count = count + Leaf_counts(decisiontree.leftchild, count) + Leaf_counts(decisiontree.rightchild, count)
        return count


def depth_of_tree(decisiontree):
    depth_1 = 0
    depth_2 = 0
    if (decisiontree is None):
        return 0
    else:
        depth_1 = 1 + depth_of_tree(decisiontree.rightchild)
        depth_2 = 1 + depth_of_tree(decisiontree.leftchild)
        if (depth_1 > depth_2):
            return depth_1
        else:
            return depth_2


def print_Decision_tree(decision_tree, bar=''):
    if decision_tree.pure != None:
        if (decision_tree.pure['0'] > decision_tree.pure['1']):
            print(0)
        else:
            print(1)
    else:
        print('\n' + bar, str(decision_tree.col) + ' = ' + str(decision_tree.keep), end=": ")
        print_Decision_tree(decision_tree.rightchild, bar + '| ')
        if (decision_tree.value == 1):
            val = 0
        else:
            val = 1
        print(bar, str(decision_tree.col) + '=' + str(val), end=": ")
        print_Decision_tree(decision_tree.leftchild, bar + '| ')


def classification(newinput, decisiontree):
    if decisiontree.pure != None:
        return decisiontree.pure
    else:
        v = newinput[decisiontree.number]
        branch = None
        if v == '1':
            branch = decisiontree.rightchild
        else:
            branch = decisiontree.leftchild
    return classification(newinput, branch)


def calculate_accuracy(data, tree):
    cnt = 0
    tmp = -1
    for row in data:
        tmp = tmp + 1
        if (classification(row, tree)['1'] >= classification(row, tree)['0']):
            if (row[-1] == '1'):
                cnt = cnt + 1
        else:
            if row[-1] == '0':
                cnt = cnt + 1
    acc = cnt / float(len(data))
    return acc

def total_no_nodes(decision_tree):
    cnt = 1
    if (decision_tree is None):
        return 0
    if (decision_tree is not None):
        cnt = cnt + total_no_nodes(decision_tree.rightchild)
        cnt = cnt + total_no_nodes(decision_tree.leftchild)
    return cnt



def Find__node(decision_tree, keep):
    tree_node = None
    if (decision_tree is None):
        return None
    elif (decision_tree.keep == keep):
        return decision_tree

    if (decision_tree is not None):
        tree_node = Find__node(decision_tree.rightchild, keep)
        if (tree_node is None):
            tree_node = Find__node(decision_tree.leftchild, keep)
    return tree_node

def find_parentnode(decision_Tree):
    if (decision_Tree is None):
        return None
    elif (decision_Tree.parent is not None):
        return find_parentnode(decision_Tree.parent)
    else:
        return decision_Tree



def find_depthofTree(decision_tree, number, node_depth):
    if (decision_tree is None):
        return 0
    elif (decision_tree.keep == number):
        return node_depth

    down_Level = find_depthofTree(decision_tree.leftchild, number, node_depth + 1);
    if (down_Level != 0):
        return down_Level
    down_Level = find_depthofTree(decision_tree.rightchild, number, node_depth + 1);
    return down_Level


def pure_counts(rows):
    pure_cnt = {}
    pure_cnt['1'] = 0
    pure_cnt['0'] = 0
    for row in rows:
        r = row[len(row) - 1]
        pure_cnt[r] += 1
    return pure_cnt

def decisionTree_Pruning(tree, pruning_factor):
    totaltree_depth = depth_of_tree(tree) - 2
    tree_copy = tree
    total_internalNode = Numbering_node(tree_copy, 0)
    prune_cnt = int(pruning_factor * total_internalNode)
    while (prune_cnt > 0):
        selected_Node = random.randint(2, (total_internalNode))
        required_Node = Find__node(tree_copy, selected_Node)
        if (required_Node is not None):
            if (required_Node.pure is None and (depth_of_tree(tree_copy) - find_depthofTree(tree_copy, selected_Node, 0)) < 4):
                if (required_Node.noof0 > required_Node.noof1):
                    p = float(required_Node.noof0) / (required_Node.noof1 + required_Node.noof0)
                else:
                    p = float(required_Node.noof1) / (required_Node.noof1 + required_Node.noof0)
                if (p > 0.5):
                    prune_cnt = prune_cnt - 1
                    required_Node.rightchild = None
                    required_Node.leftchild = None
                    required_Node.pure = {'1': required_Node.noof0, '0': required_Node.noof1}
                    Tree_new = find_parentnode(required_Node)
                    tree_copy = Tree_new
                    total_internalNode = Numbering_node(tree_copy, 0)
    return tree_copy



def main():
    test_set = []
    test_Attributes = []
    validation_set = []
    validation_attributes = []
    with open(sys.argv[2], 'r') as CSV_filedata:
        csvReader_2 = csv.reader(CSV_filedata)
        validation_attributes = csvReader_2.next()
        for row in csvReader_2:
            validation_set += [row]
        CSV_filedata.close()
    with open(sys.argv[3], 'r') as CSV_filedata:
        csvReader_1 = csv.reader(CSV_filedata)
        test_Attributes = csvReader_1.next()
        for row in csvReader_1:
            test_set += [row]
        CSV_filedata.close()
    with open(sys.argv[1], 'r') as CSV_filedata:
        reader = csv.reader(CSV_filedata)
        training_set = []
        first_inputLine = reader.next()
        global attributes
        global keep
        global leaf_count
        keep = 0
        leaf_count = 0
        attributes = {}
        attribute_values = []
        total_datasetcases = []
        i = 0
        for column in first_inputLine[0:-1]:
            attributes[i] = column
            i = i + 1
        attribute_values = {'0', '1'}
        for row in reader:
            total_datasetcases += [row]
            case = (row[0:-1], row[-1])
            training_set += [case]
        attributes_left = []
        for i in range(0, len(attributes)):
            attributes_left = attributes_left + [i]
        set0, set1 = Divide_Set(total_datasetcases, 13)
        Decision_Tree = Build_Decision_Tree(total_datasetcases, len(attributes), 1)
        cnt = total_no_nodes(Decision_Tree)
        pruning_factor = float(sys.argv[4])
        j = 1
        while (j > 0):
            j = 0
            Decision_Tree = Build_Decision_Tree(total_datasetcases, len(attributes), 1)
            print('----------------------------------------------------------------------------------\n')
            print('Pre-Pruned Accuracy of Decision Tree is:')
            print('------------------------------------')
            print('Total No. of training instances: = ', len(total_datasetcases))
            print('Total No. of training attributes: = ', len(attributes))
            print('Total No. of nodes in the decision Tree: = ', keep)
            print('Total No. of leaf nodes in the decision tree: = ', Leaf_counts(Decision_Tree, 0))
            train_accuracy = calculate_accuracy(total_datasetcases, Decision_Tree)
            print('Calculated Accuracy of the model on the training data-set: = ', train_accuracy * 100, '%\n\n')

            pre_validation_accuracy = calculate_accuracy(validation_set, Decision_Tree)
            print('Total No. of validation instances: = ', len(validation_set))
            print('Total No.of validation attributes: = ', len(validation_attributes) - 1)
            print('Calculated Accuracy of the model on the validation data-set before pruning: = ', pre_validation_accuracy * 100,
                  '%\n\n')

            test_accuracy = calculate_accuracy(test_set, Decision_Tree)
            print('Total No. of testing instances: = ', len(test_set))
            print('Total No. testing attributes: = ', len(test_Attributes) - 1)
            print('Calculated Accuracy of the model on the testing data-set: = ', test_accuracy * 100, '%')
            print('--------------------------------------------------------------------------------------\n')
            print('Post-Pruned Accuracy of Decision Tree is:')
            print('--------------------------------------------------------------------------------------')

            prune_count = int(pruning_factor * Numbering_node(Decision_Tree, 0))
            print('Given Pruning Factor: ', pruning_factor)
            print('No. of nodes to be pruned = ', prune_count)
            Depth_ofDecisionTree = depth_of_tree(Decision_Tree) - 2

            Pruned_decisionTree = decisionTree_Pruning(Decision_Tree, pruning_factor)
            post_validation_accuracy = calculate_accuracy(validation_set, Pruned_decisionTree)
            i = 0
            tmp = 0
            Keep_Copy = keep

            while (pre_validation_accuracy > post_validation_accuracy):
                i = i + 1
                if (i > 10):
                    break
                Decision_Tree = Build_Decision_Tree(total_datasetcases, len(attributes), 1)
                temptreepruned = decisionTree_Pruning(Decision_Tree, pruning_factor)
                tmp = calculate_accuracy(validation_set, temptreepruned)
                if (tmp > post_validation_accuracy):
                    post_validation_accuracy = tmp
                    Pruned_decisionTree = temptreepruned

            print('Total No. of training instances = ', len(total_datasetcases))
            print('Total No.  training attributes = ', len(attributes))
            print('Total No.  of nodes in the tree = ', total_no_nodes(Pruned_decisionTree))
            print('Total No.  of leaf nodes in the tree = ', Leaf_counts(Pruned_decisionTree, 0))
            train_accuracy = calculate_accuracy(total_datasetcases, Pruned_decisionTree)
            print('Calculated Accuracy of the model on the training data-set after pruning = ', train_accuracy * 100, '%\n\n')

            validation_accuracy = calculate_accuracy(validation_set, Pruned_decisionTree)
            print('Total No. of validation instances = ', len(validation_set))
            print('Total No. of validation attributes = ', len(validation_attributes) - 1)
            print('Calculated Accuracy of the model on the validation data-set after pruning = ', validation_accuracy * 100,
                  '%\n\n')

            test_accuracy = calculate_accuracy(test_set, Pruned_decisionTree)
            print('Total No. of testing instances = ', len(test_set))
            print('Total No. of testing attributes = ', len(test_Attributes) - 1)
            print('Calculated Accuracy of the model on the testing dataset after pruning = ', test_accuracy * 100, '%')

    print_Decision_tree(Decision_Tree)

    print_Decision_tree(Pruned_decisionTree)


if __name__ == "__main__":
    main()