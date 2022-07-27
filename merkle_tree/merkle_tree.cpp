#include <iostream>
#include "tree.h"
#include "sha256.h"
using namespace std;

int main()
{
	string check_str = "";
	vector<string> v;
	int i = 0;
	//便于展示输出的代码
	while (i<7) //输入叶子节点
	{
		string str;
		str = to_string(i);
		v.push_back(str);//在vector最后添加一个新元素
		i++;
	}
	//10w叶子节点代码
	//while (i < 10000)
	//{
	//	string str;
	//	str = to_string(i);
	//	v.push_back(str);//在vector最后添加一个新元素
	//  i++;
	//}

	tree ntree;
	ntree.buildBaseLeafes(v);
	cout << "构建Merkle树过程:" << endl << endl;
	ntree.buildTree();

	cout << endl;
	cout << "想验证的数据: " << endl;
	cin >> check_str; //输入想验证的叶子节点
	check_str = sha2::hash256_hex_string(check_str);

	cout << "想验证的数据的哈希值: " << check_str << endl;

	if (ntree.verify(check_str))//验证有无这个节点 树有无改变
	{
		cout << endl << endl;
		cout << "Merkle树上存在验证的数据的叶子结点" << endl;
	}
	else
	{
		cout << "Merkle树上不存在验证的数据" << endl;
	}
	return 0;
}
