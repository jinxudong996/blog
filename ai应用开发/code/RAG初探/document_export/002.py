from langchain_community.document_loaders import JSONLoader


def print_docs(title, docs):
	print(title)
	if not docs:
		print("(无结果)")
		return
	for i, d in enumerate(docs, 1):
		print(f"{i}. {d.page_content}")


if __name__ == "__main__":
	print("=== JSONLoader 加载结果 ===")

	# 1. 主角信息
	print("\n1. 主角信息：")
	main_loader = JSONLoader(
		file_path="../../data/人物.json",
		jq_schema='.mainCharacter | "姓名：" + .name + "，背景：" + .backstory',
		text_content=True,
	)
	main_docs = main_loader.load()
	print_docs("主角：", main_docs)

	# 2. 支持角色信息
	print("\n2. 支持角色信息：")
	support_loader = JSONLoader(
		file_path="../../data/人物.json",
		jq_schema='.supportCharacters[] | "姓名：" + .name + "，背景：" + .background',
		text_content=True,
	)
	support_docs = support_loader.load()
	print_docs("支持角色：", support_docs)

	# 3. 基本信息（可选）
	print("\n3. 基本信息：")
	info_loader = JSONLoader(
		file_path="../../data/人物.json",
		jq_schema='"标题：" + .gameTitle + "，引擎：" + .basicInfo.engine + "，发行：" + .basicInfo.releaseDate',
		text_content=True,
	)
	info_docs = info_loader.load()
	print_docs("游戏信息：", info_docs)
