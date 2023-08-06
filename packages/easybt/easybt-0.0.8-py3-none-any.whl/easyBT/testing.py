from binarytree import BinaryTree,BinarySearchTree
 
bt=BinaryTree()
x=[5,6,3,2,4,1,1.5]
# x=[1,2,None,None,5,6]
# x=[1,2,None,4,5,6]
# x=[6,2,8,0,4,7,9,'*','*',3,5]
# root=bt.DesializeTree(x)

"""
python3 -m pip install --user --upgrade setuptools wheel
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
python3 -m twine upload --https://github.com/EasyBinaryTree/EasyBT.git https://test.pypi.org/legacy/ dist/*


python3 setup.py sdist bdist_wheel
twine upload --skip-existing dist/* or twine upload dist/*

"""

# bt.VisualizeTree(root)
# print(bt.Diameter.__doc__)
# print(bt.__doc__)

bst=BinarySearchTree()
root=None
root=bst.createBST(data=x)
    
print(bst.InOrderTraversal(root))
# bst.VisualizeTree(root)
bst.insertInBST(root,7)
bst.insertInBST(root,0)
x=[10,9,12,11,-2,-3,-4]

root=bst.createBST(data=x,root=root)
bst.deleteNode(root,3)
print(bst.InOrderTraversal(root))
# bst.VisualizeTree(root)
print(bst.SerializeTree.__code__)