from binarytree import BinaryTree  
 
bt=BinaryTree()
x=[1,2,3,4,5,6]
# x=[1,2,None,None,5,6]
# x=[1,2,None,4,5,6]
# x=[6,2,8,0,4,7,9,'*','*',3,5]
root=bt.DesializeTree(x)
print(bt.InOrderTraversal(root))
# print(bt.PreOrderTraversal(root))
# print(bt.SerializeTree(root))
# print(bt.InOrderTraversal(root))
print(bt.LevelOrderTraversal(root))
# print(bt.SerializeTree(root))

# python3 -m pip install --user --upgrade setuptools wheel
# python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# python3 -m twine upload --https://github.com/EasyBinaryTree/EasyBT.git https://test.pypi.org/legacy/ dist/*


# python3 setup.py sdist bdist_wheel
# twine upload --skip-existing dist/* or twine upload dist/*
bt.VisualizeTree(root)
